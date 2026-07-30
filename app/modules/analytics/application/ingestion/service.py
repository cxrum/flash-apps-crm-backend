from __future__ import annotations

from datetime import UTC, datetime

from app.core.bus.contract import IAsyncEventBus
from app.modules.analytics.application.events_bus.factories.param_update_event import (
    UpdateParamMessageFactory,
    UpdateParamValue,
)
from app.modules.analytics.application.events_bus.factories.sdk_event import SdkEventMessageFactory
from app.modules.analytics.application.exception import AnalyticsClickNotFound, AnalyticsPlatformNotFound
from app.modules.analytics.application.ingestion.commands import (
    SdkEventCommand,
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
)
from app.modules.analytics.application.ingestion.event_builder import (
    ConversionEventBuilder,
    MetricsEventBuilder,
    RevenueEventBuilder,
)
from app.modules.analytics.application.ingestion.exception import (
    IdempotencyKeyProcessing,
    IdempotencyStateLost,
    InvalidInstallKey,
    RevenueDataRequired,
    UnsupportedEventType,
)
from app.modules.analytics.application.ingestion.protocol import IngestionServiceProtocol
from app.modules.analytics.application.ingestion.responses import SdkInstallResponse
from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.analytics.domain.events.AnalyticsEventEntity import AnalyticsEventEntity
from app.modules.analytics.domain.install.AnalyticsInstallEntity import AnalyticsInstallEntity
from app.modules.analytics.domain.redis.repo import IdempotencyKeyRepositoryProtocol, IdempotencyKeyStatus
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol, AnalyticsUnitOfWorkProtocol
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.analytics.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.modules.analytics.domain.currency.entity import Money


class IngestionService(IngestionServiceProtocol):
    def __init__(
        self,
        uow_factory: AnalyticsUnitOfWorkFactoryProtocol,
        async_event_bus: IAsyncEventBus,
        currency_service: CurrencyConvertorClientProtocol,
        idempotency_repo: IdempotencyKeyRepositoryProtocol,
    ) -> None:
        self._uow_factory = uow_factory
        self._async_event_bus = async_event_bus
        self._currency_service = currency_service
        self._idempotency_repo = idempotency_repo

    def _resolve_platform(
        self,
        install_key: str,
        uow: AnalyticsUnitOfWorkProtocol,
    ) -> CrmAppPlatformEntity:
        platform = uow.app_platform_repo.get_by_install_key(install_key)

        if platform is None or platform.platform_id is None:
            raise InvalidInstallKey(install_key)

        return platform

    def _resolve_click(
        self,
        command: SdkInstallCommand,
        app_platform_id: int,
        uow: AnalyticsUnitOfWorkProtocol,
    ) -> AnalyticsClickEntity:
        click_id = command.click_id or AnalyticsClickEntity.generate_click_id()
        existing = uow.click_repo.get_by_id(click_id)

        if existing is not None:
            existing.validate_platform_match(app_platform_id)
            return existing

        return uow.click_repo.insert(
            AnalyticsClickEntity.create_synthetic(app_platform_id=app_platform_id, params=command.params)
        )

    @staticmethod
    def _scope(operation: str, context: str, idempotency_key: str) -> str:
        return f"{operation}:{context}:{idempotency_key}"

    async def _start_idempotent_request(self, key: str) -> str | None:
        claim = await self._idempotency_repo.acquire(key)
        if claim.status is IdempotencyKeyStatus.COMPLETED:
            return None
        if not claim.is_owner:
            raise IdempotencyKeyProcessing(key)

        return claim.owner_token

    async def _finish_idempotent_request(self, key: str, owner_token: str) -> None:
        if not await self._idempotency_repo.complete(key, owner_token):
            raise IdempotencyStateLost(key)

    async def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse | None:
        key = self._scope("install", command.install_key, command.idempotency_key)
        owner_token = await self._start_idempotent_request(key)
        if owner_token is None:
            return None

        try:
            response = await self._process_install(command)
        except BaseException:
            await self._idempotency_repo.release(key, owner_token)
            raise

        await self._finish_idempotent_request(key, owner_token)
        return response

    async def _process_install(self, command: SdkInstallCommand) -> SdkInstallResponse:

        with self._uow_factory.create() as uow:
            app_platform = self._resolve_platform(command.install_key, uow)

            if app_platform is None or app_platform.platform_id is None:
                raise AnalyticsPlatformNotFound()

            click = self._resolve_click(command, app_platform.platform_id, uow)

            if click is None or click.click_id is None:
                raise AnalyticsClickNotFound("")

            saved_install = uow.install_repo.save(
                AnalyticsInstallEntity(
                    click_id=click.click_id,
                    app_platform_id=app_platform.platform_id,
                    device_data=command.device.model_dump(mode="python"),
                )
            )

            event = MetricsEventBuilder(
                event_id=command.idempotency_key,
                click_id=click.click_id,
                event_key="install",
                app_user_id=saved_install.app_user_id,
                payload={
                    "install_key": command.install_key,
                    "params": dict(command.params),
                    "device": command.device.model_dump(mode="python"),
                },
            ).build()

            saved_event = uow.event_repo.insert(event)

        await self._async_event_bus.publish(SdkEventMessageFactory.from_event(saved_event))

        return SdkInstallResponse(click_id=click.click_id, app_user_id=saved_install.app_user_id)

    def _make_event_builder(
        self,
        *,
        idempotency_key: str,
        click_id: str,
        app_user_id: int | None,
        event: SdkEventCommand,
    ):
        builder_kwargs = {
            "event_id": idempotency_key,
            "click_id": click_id,
            "event_key": event.key,
            "app_user_id": app_user_id,
        }

        if event.type == "metric":
            return MetricsEventBuilder(**builder_kwargs)

        if event.type == "conversion" and event.amount is not None:
            return RevenueEventBuilder(**builder_kwargs)

        if event.type == "conversion":
            return ConversionEventBuilder(**builder_kwargs)

        raise UnsupportedEventType(event.type)

    async def process_batch_events(self, command: SdkEventsCommand) -> bool:
        key = self._scope("events", f"{command.install_key}:{command.click_id}", command.idempotency_key)
        owner_token = await self._start_idempotent_request(key)
        if owner_token is None:
            return False

        try:
            await self._process_batch_events(command)
        except BaseException:
            await self._idempotency_repo.release(key, owner_token)
            raise

        await self._finish_idempotent_request(key, owner_token)
        return True

    async def _process_batch_events(self, command: SdkEventsCommand) -> None:
        with self._uow_factory.create() as uow:
            app_platform = self._resolve_platform(command.install_key, uow)
            click = uow.click_repo.get_by_id(command.click_id)

            if click is None:
                raise AnalyticsClickNotFound(command.click_id)

            if app_platform is None or app_platform.platform_id is None:
                raise AnalyticsPlatformNotFound()

            click.validate_platform_match(app_platform.platform_id)

            install = uow.install_repo.get_by_click_id(click.click_id)
            events_list: list[AnalyticsEventEntity] = []
            keys: list[str] = []

            for _, event in enumerate(command.events):
                exist_event = uow.event_repo.get_by_id(event.idempotency_key)
                if exist_event is not None or event.idempotency_key in keys:
                    continue

                keys.append(event.idempotency_key)

                builder = self._make_event_builder(
                    idempotency_key=event.idempotency_key,
                    click_id=click.click_id,
                    app_user_id=install.app_user_id if install is not None else None,
                    event=event,
                )

                builder = builder._set_event_time_utc(event.event_time or datetime.now(tz=UTC))._set_payload(
                    dict(event.params)
                )

                if isinstance(builder, RevenueEventBuilder):
                    if event.currency is None or event.amount is None:
                        raise RevenueDataRequired()

                    amount_in_usd = self._currency_service.convert(
                        Money(base=event.currency, value=event.amount), "USD"
                    )
                    builder = (
                        builder._set_amount(event.amount)
                        ._set_currency(event.currency)
                        ._set_amount_in_usd(amount_in_usd.value)
                    )
                else:
                    builder = builder._set_amount(None)._set_currency(None)._set_amount_in_usd(None)
                events_list.append(builder.build())
            inserted = uow.event_repo.insert_many(events_list)

        await self._async_event_bus.publish_many(SdkEventMessageFactory.from_events(inserted))

    async def update_params(self, command: SdkParamsUpdateCommand) -> bool:
        key = self._scope("params-update", command.click_id, command.idempotency_key)
        owner_token = await self._start_idempotent_request(key)
        if owner_token is None:
            return False

        try:
            await self._update_params(command)
        except BaseException:
            await self._idempotency_repo.release(key, owner_token)
            raise

        await self._finish_idempotent_request(key, owner_token)
        return True

    async def _update_params(self, command: SdkParamsUpdateCommand) -> None:
        with self._uow_factory.create() as uow:
            click = uow.click_repo.get_by_id(command.click_id)

            if click is None:
                raise AnalyticsClickNotFound(command.click_id)

        value = UpdateParamValue(
            click_id=command.click_id, params=command.params, occurred_at=command.event_time or datetime.now(UTC)
        )

        await self._async_event_bus.publish(UpdateParamMessageFactory.from_raw_payload(value=value))
