from collections.abc import Sequence

from app.application.events_bus.events import DomainEventMessage
from app.application.events_bus.service import EventMessageHandlerProtocol, IEventBus, IMessageQueue


from collections import deque

from app.application.exceptions import ApplicationError


class InMemoryMessageQueue(IMessageQueue):
    def __init__(self) -> None:
        self._messages: deque[DomainEventMessage] = deque()

    def enqueue(self, message: DomainEventMessage) -> None:
        self._messages.append(message)

    def dequeue(self) -> DomainEventMessage | None:
        if not self._messages:
            return None
        return self._messages.popleft()

    def drain(self) -> list[DomainEventMessage]:
        drained = list(self._messages)
        self._messages.clear()
        return drained

    def size(self) -> int:
        return len(self._messages)


class InMemoryEventBus(IEventBus):
    def __init__(self, message_queue: IMessageQueue | None = None) -> None:
        self._message_queue = message_queue or InMemoryMessageQueue()
        self._subscribers: dict[str, list[EventMessageHandlerProtocol]] = {}

    def subscribe(self, event_name: str, handler: EventMessageHandlerProtocol) -> None:
        normalized_event_name = self._normalize_event_name(event_name)
        handlers = self._subscribers.setdefault(normalized_event_name, [])
        if handler not in handlers:
            handlers.append(handler)

    def unsubscribe(self, event_name: str, handler: EventMessageHandlerProtocol) -> None:
        normalized_event_name = self._normalize_event_name(event_name)
        handlers = self._subscribers.get(normalized_event_name)
        if handlers is None or handler not in handlers:
            raise ApplicationError("Handler is not registered for this event")
        handlers.remove(handler)
        if not handlers:
            del self._subscribers[normalized_event_name]

    def publish(self, message: DomainEventMessage) -> None:
        normalized_message = self._normalize_message(message)
        self._message_queue.enqueue(normalized_message)
        for handler in tuple(self._subscribers.get(normalized_message.name, ())):
            handler.handle(normalized_message)

    def publish_many(self, messages: Sequence[DomainEventMessage]) -> None:
        for message in messages:
            self.publish(message)

    @staticmethod
    def _normalize_event_name(event_name: str) -> str:
        normalized_event_name = event_name.strip()
        if not normalized_event_name:
            raise ApplicationError("Event name is required")
        return normalized_event_name

    def _normalize_message(self, message: DomainEventMessage) -> DomainEventMessage:
        return DomainEventMessage(
            name=self._normalize_event_name(message.name),
            payload=dict(message.payload),
            metadata=dict(message.metadata),
            occurred_at=message.occurred_at,
        )