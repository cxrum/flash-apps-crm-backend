from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from app.application.events_bus.factories.param_update_event import UpdateParamMessageFactory, UpdateParamValue
from app.application.exceptions import ApplicationError
from app.application.sdk.ingestion.commands import SdkEventCommand, SdkEventsCommand, SdkInstallCommand, SdkParamsUpdateCommand
from app.application.sdk.ingestion.event_builder import ConversionEventBuilder, MetricsEventBuilder, RevenueEventBuilder
from app.application.events_bus.factories.sdk_event import SdkEventMessageFactory
from app.application.sdk.ingestion.responses import SdkEventResponse, SdkInstallResponse, SdkUpdateParamsResponse
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.currency.entity import Money
from app.domain.event_bus.service_protocol import IAsyncEventBus
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol



class IngestionService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        async_event_bus: IAsyncEventBus,
        currency_service: CurrencyConvertorClientProtocol
    ) -> None:
        self._uow_factory = uow_factory
        self._async_event_bus = async_event_bus
        self._currency_service = currency_service


    def _resolve_platform(self, install_key: str, uow: UnitOfWorkProtocol,) -> CrmAppPlatformEntity:
        platform = uow.app_platform_repo.get_by_install_key(install_key)
        
        if platform is None or platform.platform_id is None:
            raise ApplicationError(f"Unknown install_key: {install_key}")
        
        return platform

    def _resolve_click(self, command: SdkInstallCommand, app_platform_id: int, uow: UnitOfWorkProtocol,) -> CrmClickEntity:
        click_id = command.click_id or CrmClickEntity.generate_click_id()
        existing = uow.click_repo.get_by_id(click_id)
        
        if existing is not None:
            existing.validate_platform_match(app_platform_id)
            return existing

        return uow.click_repo.insert(
            CrmClickEntity.create_synthetic(
                app_platform_id=app_platform_id,
                params=command.params
            )
        )

    async def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse:

        with self._uow_factory.create() as uow:
            app_platform = self._resolve_platform(command.install_key, uow)
            
            if app_platform.platform_id is None:
                raise ApplicationError(f"Unknown platfrom")
            
            
            click = self._resolve_click(command, app_platform.platform_id, uow)
            
            saved_install = uow.install_repo.save(
                CrmInstallEntity(
                    click_id=click.click_id,
                    app_platform_id=app_platform.platform_id,
                    device_data=command.device.model_dump(mode="python"),
                )
            )
            
            event = (
                MetricsEventBuilder(
                    event_id=command.idempotency_key,
                    click_id=click.click_id,
                    event_key="install",
                    app_user_id=saved_install.app_user_id,
                    payload={
                            "install_key": command.install_key,
                            "params": dict(command.params),
                            "device": command.device.model_dump(mode="python"),
                        }
                    )
                .build()    
            )
            
            saved_event = uow.event_repo.insert(event)
            
        await self._async_event_bus.publish(SdkEventMessageFactory.from_event(saved_event))
        
        return SdkInstallResponse(
            click_id=click.click_id, 
            app_user_id=saved_install.app_user_id
        )

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

        raise ApplicationError(f"Unsupported event type: {event.type}")
    
    # TODO Move event processing logic to an async background process. 
    async def process_batch_events(self, command: SdkEventsCommand):
        with self._uow_factory.create() as uow:
            app_platform = self._resolve_platform(command.install_key, uow)
            click = uow.click_repo.get_by_id(command.click_id)       
            
            if app_platform.platform_id is None:
                raise ApplicationError(f"Unknown platfrom")
            
            if click is None:
                raise ApplicationError("Click does not exist")
            
            click.validate_platform_match(app_platform.platform_id)

            install = uow.install_repo.get_by_click_id(click.click_id)
            events_list: list[EventEntity] = []
            keys: list[str] = []
            
            for _, event in enumerate(command.events):
                
                exist_event = uow.event_repo.get_by_id(event.idempotency_key) 
                if exist_event is not None or event.idempotency_key in keys:
                    continue
                
                keys.append(event.key)
                
                builder = self._make_event_builder(
                    idempotency_key=event.idempotency_key,
                    click_id=click.click_id,
                    app_user_id=install.app_user_id if install is not None else None,
                    event=event,
                )

                builder = (
                    builder
                    ._set_event_time_utc(event.event_time or datetime.now(tz=UTC))
                    ._set_payload(dict(event.params))
                )

                if isinstance(builder, RevenueEventBuilder):
                    
                    if event.currency is None or event.amount is None:
                        raise ApplicationError("Revenue error")
                    
                    amount_in_usd = self._currency_service.convert(
                        Money(
                            base=event.currency,
                            value=event.amount
                        ),
                        "USD"
                    )
                    builder = (
                        builder
                        ._set_amount(event.amount)
                        ._set_currency(event.currency)
                        ._set_amount_in_usd(amount_in_usd.value)
                    )
                else:
                    builder = (
                        builder
                        ._set_amount(None)
                        ._set_currency(None)
                        ._set_amount_in_usd(None)
                    )
                events_list.append(builder.build())
            inserted = uow.event_repo.insert_many(events_list)
            
        await self._async_event_bus.publish_many(SdkEventMessageFactory.from_events(inserted))
        
    
    async def udate_params(self, command: SdkParamsUpdateCommand):
        with self._uow_factory.create()  as uow:
            click = uow.click_repo.get_by_id(command.click_id)
            
            if click is None:
                raise ApplicationError(f"Unknown platfrom")
            
            if click is None:
                raise ApplicationError("Click does not exist")
            
        value = UpdateParamValue(
            click_id=command.click_id,
            params=command.params,
            occured_at=command.event_time or datetime.now(UTC)
        )
        
        await self._async_event_bus.publish(UpdateParamMessageFactory.from_raw_payload(value=value))