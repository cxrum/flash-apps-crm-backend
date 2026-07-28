from typing import Any, Dict

from app.core.exception import BaseBoundaryException


MESSAGE_CATALOG: dict[str, str] = {
    "domain.event_bus.raw_event.event_time.invalid": "RawEventMessage.event_time_utc must be datetime",
    "domain.event_bus.raw_event.payload.invalid": "RawEventMessage.payload['payload'] must be dict",
    "domain.event_bus.update_params.updated_at.invalid": "UpdateCurrentParamMessage.updated_at must be datetime",
    "domain.event_bus.audit.updated_at.invalid": "AuditEventMessage.updated_at must be datetime",
    "domain.event_bus.exception_event.type.invalid": "ExceptionEvent.exception_type must be str",
    "domain.event_bus.exception_event.message.invalid": "ExceptionEvent.exception_message must be str",
    "domain.event_bus.exception_event.context.invalid": "ExceptionEvent.context must be dict",
}


class EventBusException(BaseBoundaryException):
    def __init__(self, message_key: str = "internal", context: Dict[str, Any] = {}, code: int = 400):
        super().__init__(message_key, context, code)
        self.args = (MESSAGE_CATALOG.get(message_key, "Internal server error"),)


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
