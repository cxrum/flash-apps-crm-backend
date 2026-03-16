from __future__ import annotations

from datetime import UTC, datetime

from app.application.exceptions import ApplicationError
from app.application.sdk.entities import SdkEventCommand, SdkEventsCommand, SdkInstallCommand, SdkParamsUpdateCommand
from app.application.sdk.usecases.ingestion.event_builder import ConversionEventBuilder, MetricsEventBuilder, RevenueEventBuilder
from app.application.events_bus.factories.sdk_event import SdkEventMessageFactory
from app.application.events_bus.service import IEventBus
from app.application.sdk.usecases.ingestion.responses import SdkEventResponse, SdkInstallResponse, SdkUpdateParamsResponse
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.currency.entity import Money
from app.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.uow import CrmUnitOfWorkProtocol



class IngestionService:
    def __init__(
        self,
        uow: CrmUnitOfWorkProtocol,
        event_bus: IEventBus,
        currency_service: CurrencyConvertorClientProtocol
    ) -> None:
        self._uow = uow
        self._event_bus = event_bus
        self._currency_service = currency_service


    def _resolve_platform(self, install_key: str, uow: CrmUnitOfWorkProtocol,) -> CrmAppPlatformEntity:
        platform = uow.app_platform_repo.get_by_install_key(install_key)
        
        if platform is None or platform.platform_id is None:
            raise ApplicationError(f"Unknown install_key: {install_key}")
        
        return platform

    def _resolve_click(self, command: SdkInstallCommand, app_platform_id: int, uow: CrmUnitOfWorkProtocol,) -> CrmClickEntity:
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

    def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse:

        with self._uow as uow:
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
            self._event_bus.publish(SdkEventMessageFactory.from_event(saved_event))
        
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

    @staticmethod
    def _update_params(uow: CrmUnitOfWorkProtocol, *, params: dict, click_id: str, params_dictionary: list[CrmParamDefinitionEntity], updated_at: datetime | None = None)->list[CrmCurrentParamEntity]:
        
        new_params = []
        
        for definiton in params_dictionary:
            value = definiton.get_param_value(params)

            if value is None:
                continue
                
            current_param = uow.current_param_repo.get_by_click_and_key(click_id, definiton.machine_key)
            
            if current_param is not None:
                if updated_at is None:
                    _updated_at = datetime.now(UTC)
                else:
                    _updated_at = updated_at
                
                current_param = uow.current_param_repo.save(
                    CrmCurrentParamEntity(
                        click_id=click_id,
                        param_key=definiton.machine_key,
                        updated_at=_updated_at
                    )
                )
            
            current_param.update_param(definiton.overwrite_policy, value)
            new_params.append(current_param)
            
        updatet_params = uow.current_param_repo.save_many(new_params)
        return updatet_params
    
    def process_batch_events(self, command: SdkEventsCommand) -> SdkEventResponse:
        with self._uow as uow:
            app_platform = self._resolve_platform(command.install_key, uow)
            click = uow.click_repo.get_by_id(command.click_id)       
            
            if app_platform.platform_id is None:
                raise ApplicationError(f"Unknown platfrom")
            
            default_param_dictionary = uow.param_definition_repo.list_by_app_id(None) 
            app_param_dictionary = uow.param_definition_repo.list_by_app_id(app_platform.platform_id) 
            params_dictionary = default_param_dictionary + app_param_dictionary
            
            if click is None:
                raise ApplicationError("Click does not exist")
            
            click.validate_platform_match(app_platform.platform_id)

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
                    
                IngestionService._update_params(
                    uow, 
                    params=event.params, 
                    click_id=click.click_id, 
                    params_dictionary=params_dictionary
                )
                
                events_list.append(builder.build())
            
            inserted = uow.event_repo.insert_many(events_list)
            self._event_bus.publish_many(SdkEventMessageFactory.from_events(inserted))
        
        return SdkEventResponse(
            received=len(command.events),
            inserted=len(inserted),
        )
    
    def udate_params(self, command: SdkParamsUpdateCommand) -> SdkUpdateParamsResponse:
        with self._uow as uow:
            click = uow.click_repo.get_by_id(command.click_id)
            
            if click is None:
                raise ApplicationError(f"Unknown platfrom")
            
            default_param_dictionary = uow.param_definition_repo.list_by_app_id(None) 
            app_param_dictionary = uow.param_definition_repo.list_by_app_id(click.app_platform_id) 
            params_dictionary = default_param_dictionary + app_param_dictionary
            
            if click is None:
                raise ApplicationError("Click does not exist")
            
            updatet_params = IngestionService._update_params(
                uow, 
                params=command.params, 
                click_id=click.click_id, 
                params_dictionary=params_dictionary,
                updated_at=command.event_time
            )
            
        return SdkUpdateParamsResponse(
            received=len(command.params),
            inserted=len(updatet_params)
        )