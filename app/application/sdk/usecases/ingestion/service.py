from __future__ import annotations

from datetime import UTC, datetime

from app.application.exceptions import ApplicationError
from app.application.s2s.commands import S2SClickCommand
from app.application.sdk.entities import SdkEventCommand, SdkEventsCommand, SdkInstallCommand
from app.application.sdk.events.builder import _BaseSdkEventBuilder, ConversionEventBuilder, MetricsEventBuilder, RevenueEventBuilder
from app.application.sdk.usecases.ingestion.responses import SdkEventResponse, SdkInstallResponse
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.uow import CrmUnitOfWorkProtocol


class IngestionService:
    def __init__(
        self,
        uow: CrmUnitOfWorkProtocol,
    ) -> None:
        self._uow = uow



    def _resolve_platform_id(self, install_key: str, uow: CrmUnitOfWorkProtocol,) -> int:
        platform = uow.app_platform_repo.get_by_install_key(install_key)
        
        if platform is None or platform.platform_id is None:
            raise ApplicationError(f"Unknown install_key: {install_key}")
        
        return platform.platform_id

    def _resolve_click(self, command: SdkInstallCommand, app_platform_id: int, uow: CrmUnitOfWorkProtocol,) -> CrmClickEntity:
        click_id = command.click_id or CrmClickEntity.generated_click_id(command.idempotency_key)
        existing = uow.click_repo.get_by_id(click_id)
        
        if existing is not None:
            existing.validate_platform_match(app_platform_id)
            return existing

        return uow.click_repo.insert(
            CrmClickEntity.create_synthetic(
                click_id=click_id,
                app_platform_id=app_platform_id,
                params=command.params
            )
        )

    def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse:

        with self._uow as uow:
            app_platform_id = self._resolve_platform_id(command.install_key, uow)
            click = self._resolve_click(command, app_platform_id, uow)
            
            saved_install = uow.install_repo.save(
                CrmInstallEntity(
                    click_id=click.click_id,
                    app_platform_id=app_platform_id,
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
        
            uow.event_repo.insert(event)
        
        return SdkInstallResponse(
            click_id=click.click_id, 
            app_user_id=saved_install.app_user_id
        )

    
    def _make_event_builder(
        self,
        *,
        batch_idempotency_key: str,
        index: int,
        click_id: str,
        app_user_id: int | None,
        event: SdkEventCommand,
    ):
        builder_kwargs = {
            "event_id": f"{batch_idempotency_key}:{index}:{event.key}",
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


    
    def process_batch_events(self, command: SdkEventsCommand) -> SdkEventResponse:
        
        # TODO Make event processing in another service with async workers.
        # Use an EventLogObserver for saving logs. Keep here only validation
          
        with self._uow as uow:
            app_platform_id = self._resolve_platform_id(command.install_key, uow)
            click = uow.click_repo.get_by_id(command.click_id)
            
            if click is None:
                raise ApplicationError("Click does not exist")
            
            click.validate_platform_match(app_platform_id)

            install = uow.install_repo.get_by_click_id(click.click_id)
            events_list: list[EventEntity] = []
            
            for index, event in enumerate(command.events):
                builder = self._make_event_builder(
                    batch_idempotency_key=command.idempotency_key,
                    index=index,
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
                    builder = (
                        builder
                        ._set_amount(event.amount)
                        ._set_currency(event.currency)
                        ._set_amount_in_usd(None)
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
        
        return SdkEventResponse(
            received=len(command.events),
            inserted=len(inserted),
            ignored_duplicates=len(command.events) - len(inserted),
        )