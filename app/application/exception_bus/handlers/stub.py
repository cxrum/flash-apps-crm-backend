import logging

from app.application.exceptions import ApplicationError
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.exception_event import ExceptionEvent
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler


logger = logging.getLogger(__name__)


class AsyncStubExceptionHandler(AsyncEventMessageHandler):
    async def handle(self, message: DomainEventMessage) -> None:
        if not isinstance(message, ExceptionEvent):
            raise ApplicationError(
                "AsyncStubExceptionHandler expected ExceptionEvent, "
                f"got {type(message).__name__}"
            )

        logger.error(
            "Stub exception handler received %s: %s",
            message.exception_type,
            message.exception_message,
            extra={
                "correlation_id": message.correlation_id,
                "event_name": message.name,
                "exception_context": message.context,
            },
        )
