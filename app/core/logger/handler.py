import logging

from app.core.bus.contract import AsyncEventMessageHandler
from app.core.bus.type import EventMessage, ExceptionEvent
from app.core.exception import BusException

logger = logging.getLogger(__name__)


class AsyncLoggerExceptionHandler(AsyncEventMessageHandler):
    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, ExceptionEvent):
            raise BusException(f"AsyncLoggerExceptionHandler expected ExceptionEvent, got {type(message).__name__}")

        logger.error(
            "[ERROR] %s: %s",
            message.exception_type,
            message.exception_message,
            extra={
                "correlation_id": message.correlation_id,
                "event_name": message.name,
                "exception_context": message.context,
            },
        )
