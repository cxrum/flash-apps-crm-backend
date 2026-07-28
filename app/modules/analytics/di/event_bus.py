from collections.abc import Sequence
from functools import lru_cache

from app.core.bus.contract import AsyncEventMessageHandler, IAsyncEventBus
from app.core.bus.di import AsyncHandlerSubscription
from app.core.bus.event.bus import InMemoryAsyncEventBus
from app.modules.analytics.di.infra import get_analytics_uow_factory
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.analytics.handlers.event.conversion import AsyncConversionHandler
from app.modules.analytics.handlers.event.event import ConversionEventMessage, MetricEventMessage
from app.modules.analytics.handlers.event.metric import AsyncMetricHandler
from app.modules.analytics.handlers.update_param.event import UpdateCurrentParamMessage
from app.modules.analytics.handlers.update_param.update_param import AsyncUpdateParamHandler

SHARED_ANALYTICS_MEMORY_BUS = InMemoryAsyncEventBus()


def get_analytics_event_bus() -> IAsyncEventBus:
    return SHARED_ANALYTICS_MEMORY_BUS


def build_update_param_handler(
    uow_factory: AnalyticsUnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncUpdateParamHandler(uow_factory)


def build_metric_handler(
    uow_factory: AnalyticsUnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncMetricHandler(uow_factory)


def build_conversion_handler(
    uow_factory: AnalyticsUnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncConversionHandler(uow_factory)


@lru_cache
def get_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    uow_factory = get_analytics_uow_factory()

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


def register_analytics_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncEventBus | None = None,
) -> IAsyncEventBus:
    handlers = get_event_subscribers() if async_handlers is None else tuple(async_handlers)
    event_bus = get_analytics_event_bus() if async_memory_bus is None else async_memory_bus

    for event_name, handler in handlers:
        event_bus.subscribe(event_name, handler)

    return event_bus
