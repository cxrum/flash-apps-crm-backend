from dataclasses import dataclass

from app.application.exceptions import ApplicationError
from app.domain.uow import UnitOfWorkFacotyProtocol

@dataclass(frozen=True)
class ChechUserAccessToAppCommand:
    app_id: int
    user_id: int 

class CrmUsersService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFacotyProtocol,
    ) -> None:
        self._uow_factory = uow_factory
    
    def get_user(self,): ...
    
    def update_user(self, ): ...
    
    def _user_has_acces_to_app(self, command: ChechUserAccessToAppCommand) -> bool:
        return True
    
    def resolve_user_by_uuid(self, ): ...
    
    def list_roles(self,): ...
    
    def check_user_app_access(self, app_id: int, crm_user_id: int | None) -> None:
        if crm_user_id is None:
            raise ApplicationError("CRM user context is required")

        has_access = self._user_has_acces_to_app(
            ChechUserAccessToAppCommand(
                app_id=app_id,
                user_id=crm_user_id,
            )
        )
        if not has_access:
            raise ApplicationError(f"App doesnt exsit")

    def is_user_admin_permision_access(self, crm_user_id: int | None, app_id: int) -> bool:
        return True
    
    def is_user_manager_permision_access(self, crm_user_id: int | None, app_id: int) -> bool:
        return True
        
        
