from collections.abc import Sequence
from functools import lru_cache

from app.core.bus.contract import AsyncEventMessageHandler, IAsyncEventBus
from app.core.bus.di import AsyncHandlerSubscription, get_in_memory_event_bus
from app.core.bus.event.events.audit_event import CrmAuditEvent
from app.modules.crm.application.events_bus.handlers.audit import AsyncAuditValueHandler
from app.modules.crm.di.dependencies import get_uow_factory
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol


def build_audit_value_handler(
    uow_factory: UnitOfWorkFactoryProtocol,
) -> AsyncEventMessageHandler:
    return AsyncAuditValueHandler(uow_factory)


@lru_cache
def get_event_subscribers() -> tuple[AsyncHandlerSubscription, ...]:
    uow_factory = get_uow_factory()

    return (
        (
            CrmAuditEvent.EVENT_NAME,
            build_audit_value_handler(uow_factory),
        ),
    )


def register_event_handlers(
    async_handlers: Sequence[AsyncHandlerSubscription] | None = None,
    async_memory_bus: IAsyncEventBus | None = None,
) -> IAsyncEventBus:
    handlers = get_event_subscribers() if async_handlers is None else tuple(async_handlers)
    event_bus = get_in_memory_event_bus() if async_memory_bus is None else async_memory_bus

    for event_name, handler in handlers:
        event_bus.subscribe(event_name, handler)

    return event_bus
