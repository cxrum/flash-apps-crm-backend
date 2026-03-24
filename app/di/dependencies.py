import logging
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.exception_bus.handlers.stub import AsyncStubExceptionHandler
from app.application.events_bus.handlers.conversion import AsyncConversionHandler
from app.application.events_bus.handlers.metric import AsyncMetricHandler
from app.application.events_bus.handlers.update_param import AsyncUpdateParamHandler
from app.application.s2s.servicie import S2SService
from app.application.sdk.usecases.apps.service import AppService
from app.application.sdk.usecases.ingestion.service import IngestionService
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.event_bus.events.crm_events import ConversionEventMessage, MetricEventMessage
from app.domain.event_bus.events.exception_event import ExceptionEvent
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage
from app.domain.event_bus.service_protocol import (
    AsyncEventMessageHandler,
    IAsyncEventBus,
    IAsyncExceptionBus,
)
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWorkFactory
from app.infra.db.session import SessionFactory
from app.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus
from app.infra.exception_bus.exception_bus import AsyncExceptionBusAdapter
from app.infra.services.currency import CurrencyConvertorClient
from app.infra.services.encription import EncryptionService


AsyncHandlerSubscription = tuple[str, AsyncEventMessageHandler]
FastAPIExceptionHandler = Callable[[Request, Exception], Awaitable[JSONResponse]]

SHARED_ASYNC_MEMORY_BUS = InMemoryAsyncEventBus()
SHARED_ASYNC_MEMORY_EXCEPTION_BUS = AsyncExceptionBusAdapter(InMemoryAsyncEventBus())
logger = logging.getLogger(__name__)


def get_uow_factory() -> UnitOfWorkFactoryProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)


def get_app_seacrets_encryptor() -> EncryptionServiceProtocol:
    return EncryptionService()


def get_currecncy_client() -> CurrencyConvertorClientProtocol:
    return CurrencyConvertorClient()


def get_in_memory_event_bus() -> IAsyncEventBus:
    return SHARED_ASYNC_MEMORY_BUS


def get_in_memory_exception_event_bus() -> IAsyncExceptionBus:
    return SHARED_ASYNC_MEMORY_EXCEPTION_BUS


def build_update_param_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncUpdateParamHandler(uow_factory)


def build_metric_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncMetricHandler(uow_factory)


def build_conversion_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncConversionHandler(uow_factory)


def build_stub_exception_handler() -> AsyncEventMessageHandler:
    return AsyncStubExceptionHandler()


@lru_cache
def get_exception_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    return (
        (ExceptionEvent.EVENT_NAME, build_stub_exception_handler()),
    )


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


@lru_cache
def get_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    uow_factory = get_uow_factory()

    return (
        (
            UpdateCurrentParamMessage.EVENT_NAME,
            build_update_param_handler(uow_factory),
        ),
        (
            MetricEventMessage.EVENT_NAME,
            build_metric_handler(uow_factory),
        ),
        (
            ConversionEventMessage.EVENT_NAME,
            build_conversion_handler(uow_factory),
        ),
    )


def register_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncEventBus | None = None,
) -> IAsyncEventBus:
    handlers = (
        get_event_subscribers()
        if async_handlers is None
        else tuple(async_handlers)
    )
    event_bus = (
        get_in_memory_event_bus()
        if async_memory_bus is None
        else async_memory_bus
    )

    for event_name, handler in handlers:
        event_bus.subscribe(event_name, handler)

    return event_bus


def wire_application_buses(
    event_bus: IAsyncEventBus | None = None,
    exception_bus: IAsyncExceptionBus | None = None,
) -> tuple[IAsyncEventBus, IAsyncExceptionBus]:
    wired_exception_bus = register_exception_event_handlers(
        async_memory_bus=exception_bus,
    )
    wired_event_bus = register_event_handlers(
        async_memory_bus=event_bus,
    )
    return wired_event_bus, wired_exception_bus


def build_fastapi_exception_handler(
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPIExceptionHandler:
    bus = (
        get_in_memory_exception_event_bus()
        if exception_bus is None
        else exception_bus
    )

    async def handler(request: Request, exc: Exception) -> JSONResponse:
        event = ExceptionEvent(
            name=ExceptionEvent.EVENT_NAME,
            payload={
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "context": {
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client_host": None if request.client is None else request.client.host,
                },
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

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    return handler


def register_fastapi_exception_handlers(
    app: FastAPI,
    exception_bus: IAsyncExceptionBus | None = None,
) -> FastAPI:
    app.add_exception_handler(
        Exception,
        build_fastapi_exception_handler(exception_bus),
    )
    return app


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    event_bus, exception_bus = wire_application_buses(
        event_bus=get_in_memory_event_bus(),
        exception_bus=get_in_memory_exception_event_bus(),
    )
    register_fastapi_exception_handlers(app, exception_bus)

    app.state.event_bus = event_bus
    app.state.exception_bus = exception_bus

    await exception_bus.start()
    await event_bus.start()
    try:
        yield
    finally:
        await event_bus.stop()
        await exception_bus.stop()


def get_sdk_app_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_seacrets_encryptor),
) -> AppService:
    return AppService(uow_factory, encryption_service)


def get_sdk_ingestion_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    currency_service: CurrencyConvertorClientProtocol = Depends(get_currecncy_client),
) -> IngestionService:
    return IngestionService(uow_factory, event_bus, currency_service)


def get_s2s_service(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
) -> S2SService:
    return S2SService(uow_factory)
