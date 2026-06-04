from dataclasses import dataclass

from app.application.admin.crm_authorization.commands import DeleteAppAccessCommand, GrantUserAppAccess, GrantUserAppPermission, ListAppUsersCommand, ListPermissionCommand, ListRolesCommand, ListUserPermissionCommand, ListUsersWithAccessCommand, RemoveUserAppAccess, RemoveUserAppPermission, ShareAppAccessCommand
from app.application.admin.crm_authorization.exceptions import AdminAccessRequired, AuthorizationException, PermissionNotFound, RoleNotFound
from app.application.admin.crm_authorization.mappers import AuthenticationCommandsMapper
from app.application.admin.crm_authorization.responses import GrantUserAppAccessResponse, GrantUserPermissionResponse, ListAppUsersResponse, ListPermissionsResponse, ListRolesResponse, ListUserPermissionResponse, RemoveUserAppAccessResponse, RemoveUserPermissionResponse
from app.application.exception import AppNotFound, GeneralException, UserNotFound
from app.application.mapper import PaginationMapper
from app.core.utils.general_mapper import GeneralMapper
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity, Roles
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

    def _required_share_role(self, uow: UnitOfWorkProtocol, *, crm_user_id: int, app_id: int) -> CrmRoleEntity:
        role = self.get_user_role(uow=uow, crm_user_id=crm_user_id, app_id=app_id)
        role.required_share_app_access()
        return role
    
    def get_user_role(self, uow: UnitOfWorkProtocol, *, crm_user_id: int, app_id: int) -> CrmRoleEntity:
        access = self._get_user_access(uow, crm_user_id = crm_user_id, app_id = app_id)
        
        if access is None:
            raise AuthorizationException()
        
        role = uow.role_repo.get_by_id(access.role_id)
        
        if role is None:
            raise AuthorizationException()
        
        return role
            
    def required_user_role(self, uow: UnitOfWorkProtocol, *, crm_user_id: int, app_id: int, level: Roles = Roles.MANAGER) -> CrmRoleEntity:
        role = self.get_user_role(uow=uow, crm_user_id=crm_user_id, app_id=app_id)
        role.required(level)        
        return role
    
    def has_user_role(self, uow: UnitOfWorkProtocol, *, crm_user_id: int, app_id: int, level: Roles = Roles.MANAGER) -> bool:
        role = self.get_user_role(uow=uow, crm_user_id=crm_user_id, app_id=app_id)
        return role.compare(level) 

    def is_user_admin_permission_access(self, *, crm_user_id: int, app_id: int) -> bool:
        with self._uow_factory.create() as uow:
            return self.has_user_role(
                uow,
                crm_user_id=crm_user_id,
                app_id=app_id,
                level=Roles.ADMIN,
            )

    def is_user_manager_permission_access(self, *, crm_user_id: int, app_id: int) -> bool:
        with self._uow_factory.create() as uow:
            return self.has_user_role(
                uow,
                crm_user_id=crm_user_id,
                app_id=app_id,
                level=Roles.MANAGER,
            )
            
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
    
    def has_user_app_access(self, *,  crm_user_id: int, app_id: int) -> None:
        with self._uow_factory.create() as uow:
            access = self._get_user_access(uow, crm_user_id = crm_user_id, app_id = app_id)
        
        if  access is None:
            raise AuthorizationException()

    def list_permissions(self, command: ListPermissionCommand) -> ListPermissionsResponse:
        
        with self._uow_factory.create() as uow:
            permissions = uow.permission_repo.list_all(
                pagination=PaginationMapper.pagination_from_command(command)
            )
            
        return ListPermissionsResponse(
            permissions=[AuthenticationCommandsMapper.permission_domain_to_value(it) for it in permissions]
        )

    def list_roles(self, command: ListRolesCommand) -> ListRolesResponse:
        with self._uow_factory.create() as uow:
            roles = uow.role_repo.list_all(
                pagination=PaginationMapper.pagination_from_command(command)
            )

        return ListRolesResponse(
            roles=[AuthenticationCommandsMapper.role_domain_to_value(it) for it in roles]
        )

    def share_app_access(self, command: ShareAppAccessCommand) -> GrantUserAppAccessResponse:
        with self._uow_factory.create() as uow:
            self._required_share_role(
                uow,
                crm_user_id=command.crm_user_id,
                app_id=command.app_id,
            )

            manager = uow.user_repo.get_by_id(command.manager_id)
            if manager is None or manager.user_id is None:
                raise UserNotFound()

            app = uow.app_repo.get_by_id(command.app_id)
            if app is None or app.app_id is None:
                raise AppNotFound()

            role = uow.role_repo.get_by_code(command.role_code)
            if role is None or role.role_id is None:
                raise RoleNotFound()

            existing_access = uow.user_app_access_repo.get_by_user_and_app(
                user_id=manager.user_id,
                app_id=command.app_id,
            )

            if existing_access is not None and existing_access.role_id != role.role_id:
                uow.user_app_access_repo.delete(
                    user_id=manager.user_id,
                    app_id=command.app_id,
                )

            uow.user_app_access_repo.save(
                CrmUserAppAccessEntity.create(
                    user_id=manager.user_id,
                    app_id=command.app_id,
                    role_id=role.role_id,
                )
            )

        return GrantUserAppAccessResponse(
            app_id=app.app_id,
            crm_user_id=manager.user_id,
            access=AuthenticationCommandsMapper.role_domain_to_value(role),
        )

    def delete_app_access(self, command: DeleteAppAccessCommand) -> RemoveUserAppAccessResponse:
        if command.app_id is None:
            raise AppNotFound()

        with self._uow_factory.create() as uow:
            self._required_share_role(
                uow,
                crm_user_id=command.crm_user_id,
                app_id=command.app_id,
            )

            manager = uow.user_repo.get_by_id(command.manager_id)
            if manager is None or manager.user_id is None:
                raise UserNotFound()

            app = uow.app_repo.get_by_id(command.app_id)
            if app is None or app.app_id is None:
                raise AppNotFound()

            existing_access = uow.user_app_access_repo.get_by_user_and_app(
                user_id=manager.user_id,
                app_id=command.app_id,
            )
            if existing_access is None:
                raise AuthorizationException()

            uow.user_app_access_repo.delete(
                user_id=manager.user_id,
                app_id=command.app_id,
            )

        return RemoveUserAppAccessResponse(
            app_id=app.app_id,
            crm_user_id=manager.user_id,
        )

    def list_users_with_access(
        self,
        command: ListUsersWithAccessCommand,
    ) -> ListAppUsersResponse:
        if command.app_id is None:
            raise AppNotFound()

        with self._uow_factory.create() as uow:
            self._required_share_role(
                uow,
                crm_user_id=command.crm_user_id,
                app_id=command.app_id,
            )

            user_access = uow.user_app_access_repo.list_by_app_id(
                command.app_id,
                pagination=PaginationMapper.pagination_from_command(command),
            )
            users: list[tuple[CrmUserEntity, CrmRoleEntity]] = []

            for access in user_access:
                user = uow.user_repo.get_by_id(access.user_id)
                role = uow.role_repo.get_by_id(access.role_id)

                if user is None:
                    raise UserNotFound()

                if role is None:
                    raise RoleNotFound()

                users.append((user, role))

        return ListAppUsersResponse(
            users=[AuthenticationCommandsMapper.user_domain_to_value(it) for it in users]
        )
    
    def list_app_users(
        self,
        command: ListAppUsersCommand
    ) -> ListAppUsersResponse:
        
        with self._uow_factory.create() as uow:
            self.required_user_role(
                uow, 
                crm_user_id=command.crm_user_id, 
                app_id=command.app_id, 
                level=Roles.ADMIN
            )
            
            user_access = uow.user_app_access_repo.list_by_app_id(command.app_id)
            users: list[tuple[CrmUserEntity, CrmRoleEntity]] = []
            
            for access in user_access:
                user = uow.user_repo.get_by_id(access.user_id)
                role = uow.role_repo.get_by_id(access.role_id)
                
                if user is None:
                    raise UserNotFound()
                
                if role is None:
                    raise RoleNotFound()
                
                users.append((user, role))
        
        return ListAppUsersResponse(
            users=[AuthenticationCommandsMapper.user_domain_to_value(it) for it in users]
        )

    def grant_permission(
        self,
        command: GrantUserAppPermission
    ) -> GrantUserPermissionResponse:
        
        with self._uow_factory.create() as uow:
            self.required_user_role(
                uow, 
                crm_user_id=command.crm_user_id, 
                app_id=command.app_id, 
                level=Roles.ADMIN
            )
            
            manager = uow.user_repo.get_by_id(command.manager_id)
            
            if manager is None or manager.user_id is None:
                raise UserNotFound()
            
            app = uow.app_repo.get_by_id(command.app_id)
            
            if app is None or app.app_id is None:
                raise AppNotFound()
            
            permission = uow.permission_repo.get_by_id(command.permission_id)
            
            if permission is None or permission.permission_id is None:
                raise PermissionNotFound()
            
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
        with self._uow_factory.create() as uow:
            self.required_user_role(
                uow, 
                crm_user_id=command.crm_user_id, 
                app_id=command.app_id, 
                level=Roles.ADMIN
            )
            
            user_permissions = uow.user_permissions_repo.list_by_user_id_per_app(
                user_id=command.crm_user_id,
                app_id=command.app_id,
            )
            removed_permission = None
            for permission in user_permissions:
                if command.permission_id == permission.permission_id:
                    removed = uow.user_permissions_repo.delete(
                        user_id=command.crm_user_id, 
                        permission_id=command.permission_id,
                        app_id=command.app_id
                    )
                    removed_permission = uow.permission_repo.get_by_id(removed.permission_id)
                    break
            
            if removed_permission is None:
                raise GeneralException()
            
        return RemoveUserPermissionResponse(
            app_id=command.app_id,
            crm_user_id=command.crm_user_id,
            permission=AuthenticationCommandsMapper.permission_domain_to_value(removed_permission)
        ) 
            
    def grant_app_access(
        self,
        command: GrantUserAppAccess
    ) -> GrantUserAppAccessResponse:
             
        with self._uow_factory.create() as uow:
            self.required_user_role(
                uow, 
                crm_user_id=command.crm_user_id, 
                app_id=command.app_id, 
                level=Roles.ADMIN
            )
            
            manager = uow.user_repo.get_by_email(command.manager_email)
            if manager is None or manager.user_id is None:
                raise GeneralException
            
            app = uow.app_repo.get_by_id(command.app_id)
            
            if app is None or app.app_id is None:
                raise GeneralException
            
            role = uow.role_repo.get_by_id(command.role_id)
            
            if role is None or role.role_id is None:
                raise GeneralException
            
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
        
        with self._uow_factory.create() as uow:
            self.required_user_role(
                uow, 
                crm_user_id=command.crm_user_id, 
                app_id=command.app_id, 
                level=Roles.ADMIN
            )
            
            manager = uow.user_repo.get_by_id(command.manager_id)
            
            if manager is None or manager.user_id is None:
                raise GeneralException
            
            app = uow.app_repo.get_by_id(command.app_id)
            
            if app is None or app.app_id is None:
                raise GeneralException
            
            app_access = uow.user_app_access_repo.delete(
                user_id=manager.user_id,
                app_id=command.app_id
            )
            
        return RemoveUserAppAccessResponse(
            app_id=app.app_id,
            crm_user_id=manager.user_id
        )
    
