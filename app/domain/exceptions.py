from typing import Any, Dict

from app.core.exception_resolver import MessageResolver


class DomainError(Exception):
    pass


class DomainException(DomainError):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        self.message_key = message_key
        self.context = context
        self.code = code
        super().__init__(MessageResolver().resolve(message_key, context))


class AppNotFoundError(DomainException):
    def __init__(self, app_id: int | None = None):
        context = {"app_id": app_id} if app_id is not None else {}
        super().__init__("domain.app.not_found", context, 404)


class PlatformDoestExist(DomainException):
    def __init__(self, platform: str | None = None):
        context = {"platform": platform} if platform is not None else {}
        super().__init__("domain.platform.doesnt_exist", context, 404)


class PlatformStatusDoestExist(DomainException):
    def __init__(self, status: str | None = None):
        context = {"status": status} if status is not None else {}
        super().__init__("domain.platform.status.doesnt_exist", context, 404)


class AppStatusDoestExist(DomainException):
    def __init__(self, status: str | None = None):
        context = {"status": status} if status is not None else {}
        super().__init__("domain.app.status.doesnt_exist", context, 404)
