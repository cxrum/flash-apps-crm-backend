from datetime import datetime
from typing import Any

from app.core.bus.type import EventMessage


class RawEventMessage(EventMessage):
    EVENT_NAME = "analytics.event.raw.save"

    @property
    def event_id(self) -> str:
        return str(self.payload["event_id"])

    @property
    def click_id(self) -> str:
        return str(self.payload["click_id"])

    @property
    def event_type(self) -> str:
        return str(self.payload["event_type"])

    @property
    def event_key(self) -> str:
        return str(self.payload["event_key"])

    @property
    def app_user_id(self) -> int | None:
        value = self.payload.get("app_user_id")
        return int(value) if value is not None else None

    @property
    def amount(self) -> float | None:
        value = self.payload.get("amount")
        return float(value) if value is not None else None

    @property
    def currency(self) -> str | None:
        value = self.payload.get("currency")
        return str(value) if value is not None else None

    @property
    def amount_usd(self) -> float | None:
        value = self.payload.get("amount_usd")
        return float(value) if value is not None else None

    @property
    def event_time_utc(self) -> datetime:
        value = self.payload["event_time_utc"]
        if not isinstance(value, datetime):
            raise TypeError("event_time_utc must be a datetime")
        return value

    @property
    def raw_payload(self) -> dict[str, Any]:
        value = self.payload.get("payload", {})
        if not isinstance(value, dict):
            raise TypeError("payload must be a dict")
        return dict(value)


class MetricEventMessage(RawEventMessage):
    EVENT_NAME = "analytics.event.metric.save"


class ConversionEventMessage(RawEventMessage):
    EVENT_NAME = "analytics.event.conversion.save"


class UpdateCurrentParamMessage(EventMessage):
    EVENT_NAME = "sdk.update.current_params.request"

    @property
    def click_id(self) -> str:
        return str(self.payload["click_id"])

    @property
    def params(self) -> dict:
        return dict(self.payload["params"])

    @property
    def updated_at(self) -> datetime:
        value = self.payload["updated_at"]
        if not isinstance(value, datetime):
            raise TypeError("updated_at must be a datetime")
        return value
