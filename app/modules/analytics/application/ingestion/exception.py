from typing import Any, Dict

from app.modules.crm.application.sdk.exception import EventValueException, SdkException


class SdkIngestionException(SdkException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 500):
        super().__init__(message_key, context, code)


class InvalidInstallKey(SdkIngestionException):
    def __init__(self, install_key: str):
        super().__init__("sdk.ingestion.install_key.invalid", {"install_key": install_key}, 400)


class UnsupportedEventType(SdkIngestionException):
    def __init__(self, event_type: str):
        super().__init__("sdk.ingestion.event.type.unsupported", {"event_type": event_type}, 400)


class RevenueDataRequired(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.ingestion.revenue.data.required", {}, 400)


class EventIdRequired(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.event.id.required", {}, 400)


class EventClickIdRequired(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.click.id.required", {}, 400)


class MoneyValueNegative(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.money.value.negative", {}, 400)


class BuilderEventTypeMismatch(SdkIngestionException):
    def __init__(self, *, builder: str, event_type: str):
        super().__init__(
            "sdk.event.builder.type.invalid",
            {"builder": builder, "event_type": event_type},
            400,
        )


class EventKeyRequired(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.event.key.required", {}, 400)


class InvalidEventPayload(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.event.payload.invalid", {}, 400)


class ReservedEventPayloadKeys(SdkIngestionException):
    def __init__(self):
        super().__init__("sdk.event.payload.reserved", {}, 400)


class RevenueAmountRequired(EventValueException):
    def __init__(self):
        super().__init__("sdk.event.revenue.amount.required")


class RevenueCurrencyRequired(EventValueException):
    def __init__(self):
        super().__init__("sdk.event.revenue.currency.required")


class RevenueCurrencyInvalid(EventValueException):
    def __init__(self):
        super().__init__("sdk.event.revenue.currency.invalid")
