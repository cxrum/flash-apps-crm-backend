from pydantic import Field

from app.application.base import FlexibleCommand, PaginationCommand


class ShareAppAccessCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    manager_id: int
    role_code: str = Field(alias="role_code_slug")


class ListUsersWithAccessCommand(PaginationCommand):
    crm_user_id: int
    app_id: int | None = None


class DeleteAppAccessCommand(FlexibleCommand):
    crm_user_id: int
    manager_id: int
    app_id: int | None = None


class CreateRoleCommand(FlexibleCommand):
    crm_user_id: int
    name: str | None = None
    description: str | None = None
    permissions: list[str] = Field(default_factory=list)
    app_ids: list[int] = Field(default_factory=list)


class ListRolesCommand(PaginationCommand):
    crm_user_id: int
    app_id: int | None = None
    
class ListUserPermissionCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    
class ListAppUsersCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    
class ListPermissionCommand(PaginationCommand):
    pass

class GrantUserAppAccess(FlexibleCommand):
    crm_user_id: int
    app_id: int
    role_id: int
    manager_email: str
    
class RemoveUserAppAccess(FlexibleCommand):
    crm_user_id: int
    manager_id: int
    app_id: int
    
class GrantUserAppPermission(FlexibleCommand):
    crm_user_id: int
    manager_id: int
    app_id: int
    permission_id: int
    
class RemoveUserAppPermission(FlexibleCommand):
    crm_user_id: int
    app_id: int
    permission_id: int
    
