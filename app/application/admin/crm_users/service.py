from dataclasses import dataclass

from app.application.exceptions import ApplicationError
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.uow import UnitOfWorkFacotyProtocol, UnitOfWorkProtocol
from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity

    
@dataclass(frozen=True)
class UserPermission:
    code: str
    descrition: str | None = None


class CrmUsersService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFacotyProtocol,
    ) -> None:
        self._uow_factory = uow_factory
    
    def _get_user_access(self, uow: UnitOfWorkProtocol, *, app_id: int, crm_user_id: int) -> CrmUserAppAccessEntity | None:
        access = uow.user_app_access_repo.get_by_user_and_app(user_id=crm_user_id, app_id=app_id)
        return access
    
    def _get_user_role(self, uow: UnitOfWorkProtocol, *, crm_user_id: int, app_id: int) -> CrmRoleEntity:
        access = self._get_user_access(uow, crm_user_id = crm_user_id, app_id = app_id)
        
        if access is None:
            raise ApplicationError()
        
        role = uow.role_repo.get_by_id(access.role_id)
        
        if role is None:
            raise ApplicationError()
        
        return role
            
    def list_permisions(self, *,  app_id: int, crm_user_id: int) -> list[UserPermission]:
        mapped: list[UserPermission] = []
        
        with self._uow_factory.create() as uow:
            permisions = uow.user_permissions_repo.list_by_user_id_per_app(app_id=app_id, user_id=crm_user_id)
            mapped = [
                UserPermission(
                    code=it.code,
                    descrition=it.description
                ) for it in permisions
            ]
            
        return mapped
    
    def check_user_app_access(self, *,  crm_user_id: int, app_id: int) -> None:
        with self._uow_factory.create() as uow:
            access = self._get_user_access(uow, crm_user_id = crm_user_id, app_id = app_id)
        
        if  access is not None:
            raise ApplicationError(f"App doesnt exsit")

    def is_user_admin_permision_access(self, *, crm_user_id: int, app_id: int) -> bool:
        with self._uow_factory.create() as uow:
            return self._get_user_role(uow, crm_user_id=crm_user_id, app_id=app_id).is_admin_role()
            
    def is_user_manager_permision_access(self, *, crm_user_id: int, app_id: int) -> bool:
        with self._uow_factory.create() as uow:
            return self._get_user_role(uow, crm_user_id=crm_user_id, app_id=app_id).is_manager_role()
        
