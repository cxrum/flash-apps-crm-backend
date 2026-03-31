from dataclasses import dataclass

from app.application.admin.crm_authorization.commands import GrantUserAppAccess, GrantUserAppPermission, ListPermissionCommand, ListAppUsersCommand, ListUserPermissionCommand, RemoveUserAppAccess, RemoveUserAppPermission
from app.application.admin.crm_authorization.mappers import AuthenticationCommandsMapper
from app.application.admin.crm_authorization.responses import GrantUserAppAccessResponse, GrantUserPermissionResponse, ListAppUsersResponse, ListPermissionsResponse, ListUserPermissionResponse, RemoveUserAppAccessResponse, RemoveUserPermissionResponse
from app.application.exceptions import ApplicationError
from app.application.mapper import PaginationMapper
from app.core.utils.general_mapper import GeneralMapper
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.domain.user import CrmUserEntity
from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity

    

class CrmAuthorizationService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
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
            
    def list_user_permissions(self, command: ListUserPermissionCommand) -> ListUserPermissionResponse:

        with self._uow_factory.create() as uow:
            permissions = uow.user_permissions_repo.list_by_user_id_per_app(
                app_id=command.app_id, 
                user_id=command.crm_user_id,
                pagination=PaginationMapper.pagination_from_command(command)
            )
            
        return ListUserPermissionResponse(
            app_id=command.app_id,
            crm_user_id=command.crm_user_id,
            permissions=[AuthenticationCommandsMapper.permission_domain_to_value(it) for it in permissions]
        )
    
    def check_user_app_access(self, *,  crm_user_id: int, app_id: int) -> None:
        with self._uow_factory.create() as uow:
            access = self._get_user_access(uow, crm_user_id = crm_user_id, app_id = app_id)
        
        if  access is not None:
            raise ApplicationError(f"App doesn't exist")

    def is_user_admin_permission_access(self, *, crm_user_id: int, app_id: int) -> bool:
        with self._uow_factory.create() as uow:
            return self._get_user_role(uow, crm_user_id=crm_user_id, app_id=app_id).is_admin_role()
            
    def is_user_manager_permission_access(self, *, crm_user_id: int, app_id: int) -> bool:
        with self._uow_factory.create() as uow:
            return self._get_user_role(uow, crm_user_id=crm_user_id, app_id=app_id).is_manager_role()
    
    def list_permissions(self, command: ListPermissionCommand) -> ListPermissionsResponse:
        
        with self._uow_factory.create() as uow:
            permissions = uow.permission_repo.list_all(
                pagination=PaginationMapper.pagination_from_command(command)
            )
            
        return ListPermissionsResponse(
            permissions=[AuthenticationCommandsMapper.permission_domain_to_value(it) for it in permissions]
        )
    
    def list_app_users(
        self,
        command: ListAppUsersCommand
    ) -> ListAppUsersResponse:
        self.is_user_admin_permission_access(crm_user_id=command.crm_user_id, app_id=command.app_id)
        
        with self._uow_factory.create() as uow:
            user_access = uow.user_app_access_repo.list_by_app_id(command.app_id)
            users: list[tuple[CrmUserEntity, CrmRoleEntity]] = []
            
            for access in user_access:
                user = uow.user_repo.get_by_id(access.user_id)
                role = uow.role_repo.get_by_id(access.role_id)
                
                if user is None:
                    raise ApplicationError
                
                if role is None:
                    raise ApplicationError
                
                users.append((user, role))
        
        return ListAppUsersResponse(
            users=[AuthenticationCommandsMapper.user_domain_to_value(it) for it in users]
        )

    def grant_permission(
        self,
        command: GrantUserAppPermission
    ) -> GrantUserPermissionResponse:
        
        self.is_user_admin_permission_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id
        )

        with self._uow_factory.create() as uow:
            manager = uow.user_repo.get_by_id(command.manager_id)
            
            if manager is None or manager.user_id is None:
                raise ApplicationError
            
            app = uow.app_repo.get_by_id(command.app_id)
            
            if app is None or app.app_id is None:
                raise ApplicationError
            
            permission = uow.permission_repo.get_by_id(command.permission_id)
            
            if permission is None or permission.permission_id is None:
                raise ApplicationError
            
            new_permission = uow.user_permissions_repo.save(
                CrmUserPermissionEntity(
                    user_id=manager.user_id,
                    app_id=command.app_id,
                    permission_id=command.permission_id
                )
            )
            
        return GrantUserPermissionResponse(
            app_id=app.app_id,
            crm_user_id=manager.user_id,
            permission=AuthenticationCommandsMapper.permission_domain_to_value(permission)
        )
    
    
    def remove_permission(
        self,
        command: RemoveUserAppPermission
    ) -> RemoveUserPermissionResponse:
        self.is_user_admin_permission_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id
        )
        
        with self._uow_factory.create() as uow:
            user_permissions = uow.user_permissions_repo.list_by_user_id_per_app(
                user_id=command.crm_user_id,
                app_id=command.app_id,
            )
            removed_permission = None
            for permission in user_permissions:
                if command.permission_id == permission.permission_id:
                    removed = uow.user_permissions_repo.delete(command.crm_user_id, command.permission_id)
                    removed_permission = uow.permission_repo.get_by_id(removed.permission_id)
                    break
            
            if removed_permission is None:
                raise ApplicationError()
            
        return RemoveUserPermissionResponse(
            app_id=command.app_id,
            crm_user_id=command.crm_user_id,
            permission=AuthenticationCommandsMapper.permission_domain_to_value(removed_permission)
        ) 
            
    def grant_app_access(
        self,
        command: GrantUserAppAccess
    ) -> GrantUserAppAccessResponse:
        
        self.is_user_admin_permission_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id
        )
             
        with self._uow_factory.create() as uow:
            manager = uow.user_repo.get_by_email(command.manager_email)
            if manager is None or manager.user_id is None:
                raise ApplicationError
            
            app = uow.app_repo.get_by_id(command.app_id)
            
            if app is None or app.app_id is None:
                raise ApplicationError
            
            role = uow.role_repo.get_by_id(command.role_id)
            
            if role is None or role.role_id is None:
                raise ApplicationError
            
            app_access = uow.user_app_access_repo.save(
                CrmUserAppAccessEntity(
                    user_id=manager.user_id,
                    app_id=command.app_id,
                    role_id=command.role_id
                )
            )
            
        return GrantUserAppAccessResponse(
            app_id=app.app_id,
            crm_user_id=manager.user_id,
            access=AuthenticationCommandsMapper.role_domain_to_value(role)
        )
    
    def remove_app_access(
        self,
        command: RemoveUserAppAccess
    ) -> RemoveUserAppAccessResponse:
        
        self.is_user_admin_permission_access(
            crm_user_id=command.crm_user_id,
            app_id=command.app_id
        )

        with self._uow_factory.create() as uow:
            manager = uow.user_repo.get_by_id(command.manager_id)
            
            if manager is None or manager.user_id is None:
                raise ApplicationError
            
            app = uow.app_repo.get_by_id(command.app_id)
            
            if app is None or app.app_id is None:
                raise ApplicationError
            
            app_access = uow.user_app_access_repo.delete(
                user_id=manager.user_id,
                app_id=command.app_id
            )
            
        return RemoveUserAppAccessResponse(
            app_id=app.app_id,
            crm_user_id=manager.user_id
        )
    