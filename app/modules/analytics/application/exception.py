from typing import Any, Dict

from app.modules.analytics.core.exception import AnalyticsApplicationException


class AnalyticsSdkException(AnalyticsApplicationException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class AnalyticsClickNotFound(AnalyticsSdkException):
    def __init__(self, click_id: str):
        super().__init__("sdk.click.not_found", {"click_id": click_id}, 404)


class AnalyticsPlatformNotFound(AnalyticsSdkException):
    def __init__(self):
        super().__init__("general.platform.not_found", {}, 404)


class AnalyticsEventValueException(AnalyticsSdkException):
    def __init__(self, message_key: str, context: Dict[str, Any] | None = None, code: int = 400):
        super().__init__(message_key, context or {}, code)
