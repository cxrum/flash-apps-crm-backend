

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Sequence

from app.application.base import JsonDict
from app.domain.event_bus.base_event import DomainEventMessage
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage

@dataclass(frozen=True)
class UpdateParamValue:
    click_id: str
    params: JsonDict
    occured_at: datetime

class UpdateParamMessageFactory:
    DEFAULT_SOURCE = "sdk"

    @classmethod
    def from_raw_payload(
        cls,
        value: UpdateParamValue,
        *,
        name: str = UpdateCurrentParamMessage.EVENT_NAME,
        metadata: Mapping[str, Any] | None = None,
    ) -> DomainEventMessage:
        
        message_metadata = {
            "source": cls.DEFAULT_SOURCE,
            **dict(metadata or {}),
        }
        
        payload = {
            "click_id": value.click_id,
            "params": value.params,
            "occured_at": value.occured_at
        }
        
        return UpdateCurrentParamMessage(
            name=name,
            payload=payload,
            metadata=message_metadata,
            occurred_at=value.occured_at
        )

    @classmethod
    def from_raw_payloads(
        cls,
        values: Sequence[UpdateParamValue],
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[DomainEventMessage]:
        return [
            cls.from_raw_payload(value, metadata=metadata)
            for value in values
        ]
