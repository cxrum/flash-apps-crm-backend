from typing import Any, Dict

from app.modules.crm.domain.exceptions import DomainException


class RoleAccessException(DomainException):
    def __init__(self, message_key: str = "domain.role.access.denied", context: Dict[str, Any] = {}, code: int = 403):
        super().__init__(message_key, context, code)


class AdminAccessRequired(RoleAccessException):
    def __init__(self):
        super().__init__("domain.role.access.admin_required", {}, 403)


class ManagerAccessRequired(RoleAccessException):
    def __init__(self):
        super().__init__("domain.role.access.manager_required", {}, 403)
