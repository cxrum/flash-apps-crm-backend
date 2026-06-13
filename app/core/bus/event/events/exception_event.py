from __future__ import annotations

from typing import Any

from app.core.bus.event.events.exception import (
    InvalidExceptionEventContext,
    InvalidExceptionEventMessage,
    InvalidExceptionEventType,
)
from app.core.bus.type import EventMessage


class ExceptionEvent(EventMessage):
    EVENT_NAME = "system.exception.occurred"

    @property
    def exception_type(self) -> str:
        value = self.payload["exception_type"]
        if not isinstance(value, str):
            raise InvalidExceptionEventType()
        return value

    @property
    def exception_message(self) -> str:
        value = self.payload["exception_message"]
        if not isinstance(value, str):
            raise InvalidExceptionEventMessage()
        return value

    @property
    def context(self) -> dict[str, Any]:
        value = self.payload["context"]
        if not isinstance(value, dict):
            raise InvalidExceptionEventContext()
        return dict(value)


class ExceptionEventFactory:
    @classmethod
    def from_raw_exception(cls, exc: Exception, context: dict[str, Any] = {}) -> ExceptionEvent:
        event = ExceptionEvent(
            name=ExceptionEvent.EVENT_NAME,
            payload={"exception_type": type(exc).__name__, "exception_message": str(exc), "context": context},
        )
        return event
