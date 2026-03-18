from datetime import UTC, datetime

from app.application.exceptions import ApplicationError
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.click import CrmClickEntity
from app.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.event_bus.base_event import DomainEventMessage
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.uow import UnitOfWorkFacotyProtocol, UnitOfWorkProtocol


class AsyncUpdateParamHandler(AsyncEventMessageHandler):
    
    def __init__(self, uow_factory: UnitOfWorkFacotyProtocol) -> None:
        self.__uow_factory = uow_factory
    
    @staticmethod
    def _update_params(uow: UnitOfWorkProtocol, *, params: dict, click_id: str, params_dictionary: list[CrmParamDefinitionEntity], updated_at: datetime | None = None)->list[CrmCurrentParamEntity]:
        
        new_params = []
        
        for definiton in params_dictionary:
            value = definiton.get_param_value(params)

            if value is None:
                continue
            
            current_param = uow.current_param_repo.get_by_click_and_key(click_id, definiton.machine_key)
            
            if updated_at is None:
                _updated_at = datetime.now(UTC)
            else:
                _updated_at = updated_at
                
            if current_param is None:
                current_param = CrmCurrentParamEntity(
                    click_id=click_id,
                    param_key=definiton.machine_key,
                    updated_at=_updated_at,
                )

            current_param.update_param(definiton.overwrite_policy, value)
            new_params.append(current_param)
        
        if new_params == []:
            raise ApplicationError(
                f"AsyncUpdateParamHandler did not produce any params for click_id='{click_id}' "
                f"from payload keys={sorted(params.keys())}"
            )
        
        updatet_params = uow.current_param_repo.create_or_update_many(new_params)
        return updatet_params
    
    
    async def handle(self, message: DomainEventMessage) -> None:
        if not isinstance(message, UpdateCurrentParamMessage):
            raise ApplicationError(
                "AsyncUpdateParamHandler expected UpdateCurrentParamMessage, "
                f"got {type(message).__name__}"
            )
        
        with self.__uow_factory.create() as uow:
            
            click = uow.click_repo.get_by_id(message.click_id)
            
            if click is None:
                raise ApplicationError(
                    f"AsyncUpdateParamHandler could not find click with id='{message.click_id}'"
                )
            
            app_platform = uow.app_platform_repo.get_by_id(click.app_platform_id)
            
            if app_platform is None:
                raise ApplicationError(
                    "AsyncUpdateParamHandler could not find app platform "
                    f"with id='{click.app_platform_id}' for click_id='{message.click_id}'"
                )
            
            params_dictionary = uow.param_definition_repo.list_by_app_id(app_platform.app_id)
            
            if not params_dictionary:
                raise ApplicationError(
                    "AsyncUpdateParamHandler could not find param definitions "
                    f"for app_id='{app_platform.app_id}' and click_id='{message.click_id}'"
                )
            
            self._update_params(
                uow,
                click_id=message.click_id,
                params=message.params,
                params_dictionary=params_dictionary
            )
