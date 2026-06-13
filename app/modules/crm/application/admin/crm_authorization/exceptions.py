from typing import Any, Dict

from app.modules.crm.application.admin.exception import AdminException


class AuthorizationException(AdminException):
    def __init__(self, message_key: str = "admin.authorization.denied", context: Dict[str, Any] = {}, code: int = 403):
        super().__init__(message_key, context, code)


class AdminAccessRequired(AuthorizationException):
    def __init__(self):
        super().__init__("admin.authorization.admin_required", {}, 403)


class RoleNotFound(AuthorizationException):
    def __init__(self):
        super().__init__("admin.authorization.role.not_found", {}, 404)


class PermissionNotFound(AuthorizationException):
    def __init__(self):
        super().__init__("admin.authorization.permission.not_found", {}, 404)
