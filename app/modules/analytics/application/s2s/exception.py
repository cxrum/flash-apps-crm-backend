from typing import Any, Dict

from app.modules.crm.application.sdk.exception import SdkException


class S2SException(SdkException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class UnknownAppCode(S2SException):
    def __init__(self, app_code: str):
        super().__init__("sdk.s2s.app_code.unknown", {"app_code": app_code}, 404)


class PlatformNotConfigured(S2SException):
    def __init__(self, platform: str, app_code: str):
        super().__init__("sdk.s2s.platform.not_configured", {"platform": platform, "app_code": app_code}, 404)


class SignatureMismatch(S2SException):
    def __init__(self):
        super().__init__("sdk.s2s.signature.mismatch", {}, 401)


class ResolvedPlatformInvalid(S2SException):
    def __init__(self):
        super().__init__("sdk.s2s.platform.invalid", {}, 500)
