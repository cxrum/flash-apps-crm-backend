from app.modules.crm.application.sdk.exception import SdkException


class SdkS2SException(SdkException):
    def __init__(self, message_key: str = "internal", context: dict[str, object] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class UnknownAppCode(SdkS2SException):
    def __init__(self, app_code: str):
        super().__init__("sdk.s2s.app_code.unknown", {"app_code": app_code}, 404)


class PlatformNotConfigured(SdkS2SException):
    def __init__(self, platform: str, app_code: str):
        super().__init__(
            "sdk.s2s.platform.not_configured",
            {"platform": platform, "app_code": app_code},
            404,
        )


class ResolvedPlatformInvalid(SdkS2SException):
    def __init__(self):
        super().__init__("sdk.s2s.platform.invalid", {}, 500)


class SignatureMismatch(SdkS2SException):
    def __init__(self):
        super().__init__("sdk.s2s.signature.mismatch", {}, 401)
