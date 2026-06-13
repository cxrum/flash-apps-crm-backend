from typing import Any, Dict

from app.modules.crm.application.exception import GeneralException
from app.modules.crm.core.exception_resolver import MessageResolver


class SdkException(GeneralException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)
        self.args = (MessageResolver().resolve(message_key, context),)


class ClickNotFound(SdkException):
    def __init__(self, click_id: str):
        super().__init__("sdk.click.not_found", {"click_id": click_id}, 404)


class EventValueException(SdkException):
    def __init__(self, message_key: str, context: Dict[str, Any] | None = None, code: int = 400):
        super().__init__(message_key=message_key, code=code, context=context or {})


class MetricMoneyValueException(EventValueException):
    def __init__(self):
        super().__init__("metric.money.value")


class RevenueValueException(EventValueException):
    def __init__(self):
        super().__init__("revenue.money.value")


class ConversionMoneyValueException(EventValueException):
    def __init__(self):
        super().__init__("conversion.money.value")
