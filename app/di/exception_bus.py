from functools import lru_cache
import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exception import BaseBoundaryException
from app.core.exception_resolver import MessageResolver
from app.domain.event_bus.events.exception_event import ExceptionEvent, ExceptionEventFactory
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler, IAsyncExceptionBus


from collections.abc import Awaitable, Callable, Sequence

from app.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus
from app.infra.exception import BaseInfraException
from app.infra.exception_bus.exception_bus import AsyncExceptionBusAdapter
from app.infra.exception_bus.handlers.stub import AsyncStubExceptionHandler


logger = logging.getLogger(__name__)


SHARED_ASYNC_MEMORY_EXCEPTION_BUS = AsyncExceptionBusAdapter(InMemoryAsyncEventBus())
FastAPIExceptionHandler = Callable[[Request, Any], Awaitable[JSONResponse]]
AsyncHandlerSubscription = tuple[str, AsyncEventMessageHandler]


def get_in_memory_exception_event_bus() -> IAsyncExceptionBus:
    return SHARED_ASYNC_MEMORY_EXCEPTION_BUS


def build_stub_exception_handler() -> AsyncEventMessageHandler:
    return AsyncStubExceptionHandler()


@lru_cache
def get_exception_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    return (
        (ExceptionEvent.EVENT_NAME, build_stub_exception_handler()),
    )

def build_exception_handler(
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPIExceptionHandler:
    bus = (
        get_in_memory_exception_event_bus()
        if exception_bus is None
        else exception_bus
    )

    resolver = MessageResolver()

    async def handler(request: Request, exc: Exception) -> JSONResponse:
        event = ExceptionEventFactory.from_raw_exception(
            exc=exc,
            context={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_host": None if request.client is None else request.client.host,
            },
        )

        try:
            await bus.publish(event)
        except Exception:
            logger.exception(
                "Failed to publish exception event",
                extra={
                    "path": request.url.path,
                    "exception_type": type(exc).__name__,
                },
            )
        
        
        if isinstance(exc, BaseBoundaryException):
            msg = resolver.resolve(exc.message_key, exc.context)     
            code = getattr(exc, "code", 400)
        elif isinstance(exc, BaseInfraException):
            msg = resolver.resolve("internal", {})
            code = 503
        else:
            msg = resolver.resolve("internal", {})
            code = 500

        if settings.debug_mode:
            return JSONResponse(
                status_code=code,
                content={"details": msg, **event.payload} ,
            )
        else:
            return JSONResponse(
                status_code=code,
                content={"details": msg},
            )

    return handler


def register_fastapi_exception_handlers(
    app: FastAPI,
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPI:
    app.add_exception_handler(Exception, build_exception_handler(exception_bus))
    return app


def register_exception_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncExceptionBus | None = None,
) -> IAsyncExceptionBus:
    handlers = (
        get_exception_event_subscribers()
        if async_handlers is None
        else tuple(async_handlers)
    )
    exception_bus = (
        get_in_memory_exception_event_bus()
        if async_memory_bus is None
        else async_memory_bus
    )

    for event_name, handler in handlers:
        exception_bus.subscribe(event_name, handler)

    return exception_bus

