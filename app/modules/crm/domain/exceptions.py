from typing import Any, Dict

from app.core.exception import BaseBoundaryException


class DomainException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


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


class PlatformInstallKeyMustBeUniqPerApp(DomainException):
    def __init__(self, install_key: str | None = None):
        context = {"install_key": install_key} if install_key is not None else {}
        super().__init__("domain.platform.install_key.duplicate", context, 409)
