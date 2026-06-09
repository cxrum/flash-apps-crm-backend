from datetime import datetime
from typing import Any

from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.exception import InvalidValueUpdateUpdatedAt


class ValueChangedEvent(DomainEventMessage):
    EVENT_NAME = "crm.update.audit.log"

    @property
    def crm_user_id(self) -> int:
        return int(self.payload["crm_user_id"])

    @property
    def app_id(self) -> int | None:
        value = self.payload.get("app_id")
        return None if value is None else int(value)

    @property
    def entity_id(self) -> str | None:
        value = self.payload.get("entity_id")
        return None if value is None else str(value)

    @property
    def old_value(self) -> dict[str, Any]:
        return dict(self.payload["old_value"])

    @property
    def new_value(self) -> dict[str, Any]:
        return dict(self.payload["new_value"])

    @property
    def ignore_fields(self) -> tuple[str, ...]:
        value = self.payload.get("ignore_fields", ())
        if isinstance(value, str):
            return (value,)
        return tuple(str(item) for item in value)

    @property
    def updated_at(self) -> datetime:
        value = self.payload["updated_at"]
        if not isinstance(value, datetime):
            raise InvalidValueUpdateUpdatedAt()
        return value
