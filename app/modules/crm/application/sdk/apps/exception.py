from typing import Any, Dict

from app.modules.crm.application.sdk.exception import SdkException


class SdkAppException(SdkException):
    def __init__(
        self,
        message_key: str = "internal",
        context: Dict[str, Any] = {},
        code: int = 500,
    ):
        super().__init__(message_key, context, code)


class SdkAppNotFound(SdkAppException):
    def __init__(self, app_id: int):
        super().__init__("sdk.app.not_found", {"app_id": app_id}, 404)


class InvalidAppPlatform(SdkAppException):
    def __init__(self, platform: str):
        super().__init__("sdk.app.platform.invalid", {"platform": platform}, 400)


class SdkAppCreateFailed(SdkAppException):
    def __init__(self):
        super().__init__("sdk.app.save.failed", {}, 500)


class SdkAppPlatformNotFound(SdkAppException):
    def __init__(self, platform_id: int | None = None):
        context = {"platform_id": platform_id} if platform_id is not None else {}
        super().__init__("sdk.app.platform.not_found", context, 404)


class SdkAppPlatformCreateFailed(SdkAppException):
    def __init__(self):
        super().__init__("sdk.app.platform.save.failed", {}, 500)


class SdkAppPlatformRepositoryEmptyEntity(SdkAppException):
    def __init__(self):
        super().__init__("sdk.app.platform.repository.empty", {}, 500)


class SdkAppPlatformByInstallKeyNotFound(SdkAppException):
    def __init__(self, install_key: str):
        super().__init__(
            "sdk.app.platform.by_install_key.not_found",
            {"install_key": install_key},
            404,
        )
