from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class EventMessage:
    name: str
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid1()))
    payload: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))


class ExceptionEvent(EventMessage):
    EVENT_NAME = "system.exception.occurred"

    @property
    def exception_type(self) -> str:
        value = self.payload["exception_type"]
        return value

    @property
    def exception_message(self) -> str:
        value = self.payload["exception_message"]
        return value

    @property
    def context(self) -> dict[str, Any]:
        value = self.payload["context"]
        return dict(value)


class ExceptionEventFactory:
    @classmethod
    def from_raw_exception(cls, exc: Exception, context: dict[str, Any] = {}) -> ExceptionEvent:
        event = ExceptionEvent(
            name=ExceptionEvent.EVENT_NAME,
            payload={"exception_type": type(exc).__name__, "exception_message": str(exc), "context": context},
        )
        return event
