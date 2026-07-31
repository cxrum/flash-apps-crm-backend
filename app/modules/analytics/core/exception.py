from typing import Any

from app.core.exception import BaseBoundaryException


class AnalyticsExceptionBase(BaseBoundaryException):
    def __init__(self, message_key: str, context: dict[str, Any], code: int):
        super().__init__(message_key, context, code)


class AnalyticsApplicationException(AnalyticsExceptionBase):
    def __init__(self, message_key: str = "internal", context: dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class AnalyticsDomainException(AnalyticsExceptionBase):
    def __init__(self, message_key: str = "internal", context: dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)
