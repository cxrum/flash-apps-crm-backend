from typing import Any, Dict

from app.core.exception import BaseBoundaryException
from app.modules.analytics.core.exception_resolver import AnalyticsMessageResolver


class AnalyticsExceptionBase(BaseBoundaryException):
    def __init__(self, message_key: str, context: Dict[str, Any], code: int):
        super().__init__(message_key, context, code)


class AnalyticsApplicationException(AnalyticsExceptionBase):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class AnalyticsDomainException(AnalyticsExceptionBase):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)
        self.args = (AnalyticsMessageResolver().resolve(message_key, context),)
