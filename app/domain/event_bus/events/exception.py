from typing import Any, Dict

from app.domain.exceptions import DomainException


class EventBusException(DomainException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 400):
        super().__init__(message_key, context, code)


class InvalidRawEventTime(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.raw_event.event_time.invalid", {}, 400)


class InvalidRawEventPayload(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.raw_event.payload.invalid", {}, 400)


class InvalidUpdateCurrentParamUpdatedAt(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.update_params.updated_at.invalid", {}, 400)


class InvalidValueUpdateUpdatedAt(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.audit.updated_at.invalid", {}, 400)


class InvalidExceptionEventType(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.exception_event.type.invalid", {}, 400)


class InvalidExceptionEventMessage(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.exception_event.message.invalid", {}, 400)


class InvalidExceptionEventContext(EventBusException):
    def __init__(self):
        super().__init__("domain.event_bus.exception_event.context.invalid", {}, 400)
