from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, Protocol

from app.core.bus.contract import AsyncEventMessageHandler, IAsyncEventBus, IAsyncExceptionBus
from app.core.bus.event.bus import InMemoryAsyncEventBus
from app.core.bus.exception.bus import AsyncExceptionBusAdapter
from app.core.bus.type import ExceptionEvent
from app.core.logger.handler import AsyncLoggerExceptionHandler


SHARED_ASYNC_MEMORY_BUS = InMemoryAsyncEventBus()
SHARED_ASYNC_MEMORY_EXCEPTION_BUS = AsyncExceptionBusAdapter(InMemoryAsyncEventBus())
AsyncHandlerSubscription = tuple[str, AsyncEventMessageHandler]


def get_in_memory_event_bus() -> IAsyncEventBus:
    return SHARED_ASYNC_MEMORY_BUS


def get_in_memory_exception_event_bus() -> IAsyncExceptionBus:
    return SHARED_ASYNC_MEMORY_EXCEPTION_BUS


def build_logger_exception_handler() -> AsyncEventMessageHandler:
    return AsyncLoggerExceptionHandler()


def get_exception_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    return ((ExceptionEvent.EVENT_NAME, build_logger_exception_handler()),)


def register_exception_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncExceptionBus | None = None,
) -> IAsyncExceptionBus:
    handlers = get_exception_event_subscribers() if async_handlers is None else tuple(async_handlers)
    exception_bus = get_in_memory_exception_event_bus() if async_memory_bus is None else async_memory_bus

    for event_name, handler in handlers:
        exception_bus.subscribe(event_name, handler)

    return exception_bus


EventBusFactory = Callable[[], IAsyncEventBus]
ExceptionBusFactory = Callable[[], IAsyncExceptionBus]


class EventBusRegistrar(Protocol):
    def __call__(self, *, async_memory_bus: IAsyncEventBus | None = None) -> IAsyncEventBus: ...


EventBusRegistration = tuple[EventBusFactory, EventBusRegistrar]


class ExceptionBusRegistrar(Protocol):
    def __call__(self, *, async_memory_bus: IAsyncExceptionBus | None = None) -> IAsyncExceptionBus: ...


def wire_application_buses(
    *,
    event_bus: IAsyncEventBus | None = None,
    exception_bus: IAsyncExceptionBus | None = None,
    event_handlers_registrar: EventBusRegistrar,
    exception_handlers_registrar: ExceptionBusRegistrar,
) -> tuple[IAsyncEventBus, IAsyncExceptionBus]:
    wired_exception_bus = exception_handlers_registrar(
        async_memory_bus=exception_bus,
    )
    wired_event_bus = event_handlers_registrar(
        async_memory_bus=event_bus,
    )

    return wired_event_bus, wired_exception_bus


def build_application_lifespan(
    *,
    event_bus_factory: EventBusFactory,
    exception_bus_factory: ExceptionBusFactory,
    event_handlers_registrar: EventBusRegistrar,
    exception_handlers_registrar: ExceptionBusRegistrar,
    extra_event_buses: Sequence[EventBusRegistration] = (),
) -> Callable[[Any], AsyncContextManager[None]]:
    @asynccontextmanager
    async def application_lifespan(app: Any) -> AsyncIterator[None]:
        event_bus, exception_bus = wire_application_buses(
            event_bus=event_bus_factory(),
            exception_bus=exception_bus_factory(),
            event_handlers_registrar=event_handlers_registrar,
            exception_handlers_registrar=exception_handlers_registrar,
        )
        extra_buses = [
            registrar(async_memory_bus=factory())
            for factory, registrar in extra_event_buses
        ]

        await exception_bus.start()
        await event_bus.start()
        for extra_bus in extra_buses:
            await extra_bus.start()

        try:
            yield
        finally:
            for extra_bus in reversed(extra_buses):
                await extra_bus.stop()
            await event_bus.stop()
            await exception_bus.stop()

    return application_lifespan
