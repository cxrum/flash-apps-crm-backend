from __future__ import annotations

from typing import Any

from app.domain.event_bus.entity import DomainEventMessage
from app.domain.exceptions import DomainError


class ExceptionEvent(DomainEventMessage):
    EVENT_NAME = "system.exception.occurred"

    @property
    def exception_type(self) -> str:
        value = self.payload["exception_type"]
        if not isinstance(value, str):
            raise DomainError("ExceptionEvent.exception_type must be str")
        return value

    @property
    def exception_message(self) -> str:
        value = self.payload["exception_message"]
        if not isinstance(value, str):
            raise DomainError("ExceptionEvent.exception_message must be str")
        return value

    @property
    def context(self) -> dict[str, Any]:
        value = self.payload["context"]
        if not isinstance(value, dict):
            raise DomainError("ExceptionEvent.context must be dict")
        return dict(value)
