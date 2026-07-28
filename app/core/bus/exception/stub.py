import logging

from app.core.bus.contract import AsyncEventMessageHandler
from app.core.bus.exception_event import ExceptionEvent
from app.core.bus.type import EventMessage
from app.modules.crm.infra.exception import BaseInfraException

logger = logging.getLogger("app.application.exception_bus.handlers.stub")


class AsyncStubExceptionHandler(AsyncEventMessageHandler):
    async def handle(self, message: EventMessage) -> None:
        if not isinstance(message, ExceptionEvent):
            raise BaseInfraException(
                f"AsyncStubExceptionHandler expected ExceptionEvent, got {type(message).__name__}"
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
