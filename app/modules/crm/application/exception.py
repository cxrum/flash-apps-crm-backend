from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class GeneralException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class UserNotFound(GeneralException):
    def __init__(self):
        super().__init__("general.user.not_found", {}, 404)


class AppNotFound(GeneralException):
    def __init__(self):
        super().__init__("general.app.not_found", {}, 404)


class PlatformNotFound(GeneralException):
    def __init__(self):
        super().__init__("general.platform.not_found", {}, 404)


class DuplicateRequest(GeneralException):
    def __init__(self):
        super().__init__("general.platform.not_found", {}, 404)


class RoleNotFound(GeneralException):
    def __init__(self):
        super().__init__("general.role.not_found", {}, 404)
