from collections.abc import Sequence

from app.application.events_bus.handlers.conversion import AsyncConversionHandler
from app.application.events_bus.handlers.metric import AsyncMetricHandler
from app.application.events_bus.handlers.update_param import AsyncUpdateParamHandler
from app.di.exception_bus import AsyncHandlerSubscription
from app.di.infra import get_uow_factory
from app.domain.event_bus.events.crm_events import ConversionEventMessage, MetricEventMessage
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage


from functools import lru_cache

from app.domain.event_bus.service_protocol import AsyncEventMessageHandler, IAsyncEventBus
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus


SHARED_ASYNC_MEMORY_BUS = InMemoryAsyncEventBus()

def get_in_memory_event_bus() -> IAsyncEventBus:
    return SHARED_ASYNC_MEMORY_BUS


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