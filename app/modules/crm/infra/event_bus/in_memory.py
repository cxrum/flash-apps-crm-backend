from collections.abc import Sequence

from app.core.bus.contract import EventMessageHandler, IEventBus, IMessageQueue
from app.core.bus.type import EventMessage
from app.core.exception import BusException


class InMemoryMessageQueue(IMessageQueue):
    def __init__(self, maxsize: int = 120) -> None:
        self._maxsize = maxsize
        self._messages: list[EventMessage] = []

    def enqueue(self, message: EventMessage) -> None:
        if len(self._messages) >= self._maxsize:
            raise BusException("Message queue is full")
        self._messages.append(message)

    def dequeue(self) -> EventMessage | None:
        if not self._messages:
            return None
        return self._messages.pop(0)

    def drain(self) -> list[EventMessage]:
        messages = list(self._messages)
        self._messages.clear()
        return messages

    def size(self) -> int:
        return len(self._messages)


class InMemoryEventBus(IEventBus):
    def __init__(self, message_queue: IMessageQueue | None = None) -> None:
        self._message_queue = message_queue or InMemoryMessageQueue()
        self._subscribers: dict[str, list[EventMessageHandler]] = {}

    def subscribe(self, event_name: str, handler: EventMessageHandler) -> None:
        normalized_event_name = self._normalize_event_name(event_name)
        handlers = self._subscribers.setdefault(normalized_event_name, [])
        if handler not in handlers:
            handlers.append(handler)

    def unsubscribe(self, event_name: str, handler: EventMessageHandler) -> None:
        normalized_event_name = self._normalize_event_name(event_name)
        handlers = self._subscribers.get(normalized_event_name)
        if handlers is None or handler not in handlers:
            raise BusException("Handler is not registered for this event")
        handlers.remove(handler)
        if not handlers:
            del self._subscribers[normalized_event_name]

    def publish(self, message: EventMessage) -> None:
        normalized_message = self._normalize_message(message)
        self._message_queue.enqueue(normalized_message)
        self._dispatch()

    def publish_many(self, messages: Sequence[EventMessage]) -> None:
        for message in messages:
            self.publish(message)

    def _dispatch(self) -> None:
        for event in self._message_queue.drain():
            for handler in tuple(self._subscribers.get(event.name, ())):
                handler.handle(event)

    @staticmethod
    def _normalize_event_name(event_name: str) -> str:
        normalized_event_name = event_name.strip()
        if not normalized_event_name:
            raise BusException("Event name is required")
        return normalized_event_name

    def _normalize_message(self, message: EventMessage) -> EventMessage:
        normalized_name = self._normalize_event_name(message.name)
        normalized_payload = dict(message.payload)
        normalized_metadata = dict(message.metadata)

        try:
            return type(message)(
                name=normalized_name,
                correlation_id=message.correlation_id,
                payload=normalized_payload,
                metadata=normalized_metadata,
                occurred_at=message.occurred_at,
            )
        except TypeError:
            return EventMessage(
                name=normalized_name,
                correlation_id=message.correlation_id,
                payload=normalized_payload,
                metadata=normalized_metadata,
                occurred_at=message.occurred_at,
            )
