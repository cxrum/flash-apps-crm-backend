from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.core.bus.type import EventMessage
from app.modules.analytics.handlers.update_param.event import UpdateCurrentParamMessage
from app.modules.crm.application.base import JsonDict


@dataclass(frozen=True)
class UpdateParamValue:
    click_id: str
    params: JsonDict
    occurred_at: datetime


class UpdateParamMessageFactory:
    DEFAULT_SOURCE = "sdk"

    @classmethod
    def from_raw_payload(
        cls,
        value: UpdateParamValue,
        *,
        name: str = UpdateCurrentParamMessage.EVENT_NAME,
        metadata: Mapping[str, Any] | None = None,
    ) -> EventMessage:

        message_metadata = {
            "source": cls.DEFAULT_SOURCE,
            **dict(metadata or {}),
        }

        payload = {"click_id": value.click_id, "params": value.params, "updated_at": value.occurred_at}

        return UpdateCurrentParamMessage(
            name=name, payload=payload, metadata=message_metadata, occurred_at=value.occurred_at
        )

    @classmethod
    def from_raw_payloads(
        cls,
        values: Sequence[UpdateParamValue],
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[EventMessage]:
        return [cls.from_raw_payload(value, metadata=metadata) for value in values]
