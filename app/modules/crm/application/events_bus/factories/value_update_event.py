from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.core.bus.event.events.audit_event import CrmAuditEvent
from app.core.bus.type import EventMessage

JsonDict = dict[str, Any]


@dataclass(frozen=True)
class AuditEventValue:
    crm_user_id: int
    old_value: JsonDict
    new_value: JsonDict
    updated_at: datetime
    app_id: int | None = None
    entity_id: str | int | None = None
    ignore_fields: Sequence[str] = ()


class ValueChangedEventFactory:
    DEFAULT_SOURCE = "crm"

    @classmethod
    def from_raw_payload(
        cls,
        value: AuditEventValue,
        *,
        name: str = CrmAuditEvent.EVENT_NAME,
        metadata: Mapping[str, Any] | None = None,
    ) -> EventMessage:
        message_metadata = {
            "source": cls.DEFAULT_SOURCE,
            **dict(metadata or {}),
        }

        payload = {
            "crm_user_id": value.crm_user_id,
            "app_id": value.app_id,
            "entity_id": None if value.entity_id is None else str(value.entity_id),
            "old_value": value.old_value,
            "new_value": value.new_value,
            "ignore_fields": list(value.ignore_fields),
            "updated_at": value.updated_at,
        }

        return CrmAuditEvent(
            name=name,
            payload=payload,
            metadata=message_metadata,
            occurred_at=value.updated_at,
        )

    @classmethod
    def from_raw_payloads(
        cls,
        values: Sequence[AuditEventValue],
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[EventMessage]:
        return [cls.from_raw_payload(value, metadata=metadata) for value in values]
