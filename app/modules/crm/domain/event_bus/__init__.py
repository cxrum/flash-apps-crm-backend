from app.core.bus.contract import AsyncEventMessageHandler, EventMessageHandler, IAsyncEventBus, IEventBus
from app.core.bus.type import EventMessage


class DomainEventMessage(EventMessage):
    pass

__all__ = [
    "AsyncEventMessageHandler",
    "DomainEventMessage",
    "EventMessageHandler",
    "IAsyncEventBus",
    "IEventBus",
]
