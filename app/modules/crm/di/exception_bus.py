import logging
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.bus.contract import IAsyncExceptionBus
from app.core.bus.di import get_in_memory_exception_event_bus
from app.core.bus.type import ExceptionEventFactory
from app.core.bus.exception.stub import AsyncStubExceptionHandler
from app.core.exception import BaseBoundaryException
from app.modules.crm.core.config import settings
from app.modules.crm.core.exception_resolver import MessageResolver
from app.modules.crm.infra.exception import BaseInfraException

logger = logging.getLogger(__name__)
FastAPIExceptionHandler = Callable[[Request, Any], Awaitable[JSONResponse]]


def get_exception_event_subscribers() -> tuple[tuple[str, AsyncStubExceptionHandler], ...]:
    return ((ExceptionEventFactory.from_raw_exception(RuntimeError()).EVENT_NAME, AsyncStubExceptionHandler()),)


def build_crm_exception_handler(
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPIExceptionHandler:
    bus = get_in_memory_exception_event_bus() if exception_bus is None else exception_bus

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
                content={"detail": msg, **event.payload},
            )
        else:
            return JSONResponse(
                status_code=code,
                content={"detail": msg},
            )

    return handler


build_boundary_exception_handler = build_crm_exception_handler


def register_fastapi_exception_handlers(
    app: FastAPI,
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPI:
    app.add_exception_handler(Exception, build_crm_exception_handler(exception_bus))
    return app
