from datetime import datetime

from app.modules.crm.application.base import BaseResponse


class RoleResponseValue(BaseResponse):
    role_id: int
    key: str
    name: str


class ListRolesResponse(BaseResponse):
    roles: list[RoleResponseValue]


class GrantUserAppAccessResponse(BaseResponse):
    app_id: int
    crm_user_id: int
    access: RoleResponseValue


class RemoveUserAppAccessResponse(BaseResponse):
    app_id: int
    crm_user_id: int


class PermissionResponseValue(BaseResponse):
    code: str
    description: str | None = None
    permission_id: int | None = None


class ListPermissionsResponse(BaseResponse):
    permissions: list[PermissionResponseValue]


class ListUserPermissionResponse(BaseResponse):
    app_id: int
    crm_user_id: int
    permissions: list[PermissionResponseValue]


class GrantUserPermissionResponse(BaseResponse):
    app_id: int
    crm_user_id: int
    permission: PermissionResponseValue


class RemoveUserPermissionResponse(BaseResponse):
    app_id: int
    crm_user_id: int
    permission: PermissionResponseValue


class CrmUserResponseValue(BaseResponse):
    full_name: str
    email: str
    role: str
    is_active: bool = True
    crm_user_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ListAppUsersResponse(BaseResponse):
    users: list[CrmUserResponseValue]
