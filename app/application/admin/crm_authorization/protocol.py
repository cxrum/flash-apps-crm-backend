from typing import Protocol

from app.application.admin.crm_authorization.commands import (
    DeleteAppAccessCommand,
    GrantUserAppAccess,
    GrantUserAppPermission,
    ListAppUsersCommand,
    ListPermissionCommand,
    ListRolesCommand,
    ListUserPermissionCommand,
    ListUsersWithAccessCommand,
    RemoveUserAppAccess,
    RemoveUserAppPermission,
    ShareAppAccessCommand,
)
from app.application.admin.crm_authorization.responses import (
    GrantUserAppAccessResponse,
    GrantUserPermissionResponse,
    ListAppUsersResponse,
    ListPermissionsResponse,
    ListRolesResponse,
    ListUserPermissionResponse,
    RemoveUserAppAccessResponse,
    RemoveUserPermissionResponse,
)
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity, Roles
from app.domain.uow import UnitOfWorkProtocol


class CrmAuthorizationServiceProtocol(Protocol):
    def get_user_role(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
    ) -> CrmRoleEntity: ...

    def required_user_role(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
        level: Roles = Roles.MANAGER,
    ) -> CrmRoleEntity: ...

    def has_user_role(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
        level: Roles = Roles.MANAGER,
    ) -> bool: ...

    def get_user_permissions(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
    ) -> list[CrmPermissionEntity]: ...

    def has_user_permission(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
        permission_code: str,
    ) -> bool: ...

    def required_user_permission(
        self,
        uow: UnitOfWorkProtocol,
        *,
        crm_user_id: int,
        app_id: int,
        permission_code: str,
    ) -> CrmPermissionEntity | None: ...

    def is_user_admin_permission_access(self, *, crm_user_id: int, app_id: int) -> bool: ...
    def is_user_manager_permission_access(self, *, crm_user_id: int, app_id: int) -> bool: ...

    def is_user_permission_access(
        self,
        *,
        crm_user_id: int,
        app_id: int,
        permission_code: str,
    ) -> bool: ...

    def list_user_permissions(
        self,
        command: ListUserPermissionCommand,
    ) -> ListUserPermissionResponse: ...

    def has_user_app_access(self, *, crm_user_id: int, app_id: int) -> None: ...

    def list_permissions(self, command: ListPermissionCommand) -> ListPermissionsResponse: ...
    def list_roles(self, command: ListRolesCommand) -> ListRolesResponse: ...

    def share_app_access(
        self,
        command: ShareAppAccessCommand,
    ) -> GrantUserAppAccessResponse: ...

    def delete_app_access(
        self,
        command: DeleteAppAccessCommand,
    ) -> RemoveUserAppAccessResponse: ...

    def list_users_with_access(
        self,
        command: ListUsersWithAccessCommand,
    ) -> ListAppUsersResponse: ...

    def list_app_users(self, command: ListAppUsersCommand) -> ListAppUsersResponse: ...

    def grant_permission(
        self,
        command: GrantUserAppPermission,
    ) -> GrantUserPermissionResponse: ...

    def remove_permission(
        self,
        command: RemoveUserAppPermission,
    ) -> RemoveUserPermissionResponse: ...

    def grant_app_access(
        self,
        command: GrantUserAppAccess,
    ) -> GrantUserAppAccessResponse: ...

    def remove_app_access(
        self,
        command: RemoveUserAppAccess,
    ) -> RemoveUserAppAccessResponse: ...
