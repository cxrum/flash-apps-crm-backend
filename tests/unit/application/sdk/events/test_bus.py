from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.exception import GeneralException
from app.domain.event_bus.entity import DomainEventMessage
from app.infra.event_bus.in_memory import (
    InMemoryEventBus,
    InMemoryMessageQueue,
)
from app.infra.exception import BaseInfraException


class RecordingHandler:
    def __init__(self) -> None:
        self.messages: list[DomainEventMessage] = []

    def handle(self, message: DomainEventMessage) -> None:
        self.messages.append(message)


def test_message_queue_supports_enqueue_dequeue_and_drain() -> None:
    queue = InMemoryMessageQueue()
    first = DomainEventMessage(name="event.first", payload={"value": 1})
    second = DomainEventMessage(name="event.second", payload={"value": 2})

    queue.enqueue(first)
    queue.enqueue(second)

    assert queue.size() == 2
    assert queue.dequeue() == first
    assert queue.drain() == [second]
    assert queue.size() == 0


def test_event_bus_publishes_to_matching_handlers_and_enqueues_normalized_copies() -> None:
    queue = InMemoryMessageQueue()
    bus = InMemoryEventBus(queue)
    handler = RecordingHandler()
    message = DomainEventMessage(
        name="  crm.events.saved  ",
        payload={"event_id": "evt-1"},
        metadata={"source": "sdk"},
        occurred_at=datetime(2026, 3, 13, 12, 0, tzinfo=UTC),
    )

    bus.subscribe("crm.events.saved", handler)
    bus.subscribe("crm.events.saved", handler)
    bus.publish(message)
    message.payload["event_id"] = "mutated"
    message.metadata["source"] = "changed"

    assert [item.name for item in handler.messages] == ["crm.events.saved"]
    assert handler.messages[0].payload == {"event_id": "evt-1"}
    assert handler.messages[0].metadata == {"source": "sdk"}
    assert queue.size() == 1
    queued = queue.dequeue()
    assert queued is not None
    assert queued.name == "crm.events.saved"
    assert queued.payload == {"event_id": "evt-1"}
    assert queued.metadata == {"source": "sdk"}
    assert queued.occurred_at == datetime(2026, 3, 13, 12, 0, tzinfo=UTC)


def test_event_bus_publish_many_preserves_order_and_dispatches_per_event_name() -> None:
    queue = InMemoryMessageQueue()
    bus = InMemoryEventBus(queue)
    metric_handler = RecordingHandler()
    conversion_handler = RecordingHandler()
    messages = [
        DomainEventMessage(name="crm.events.metric.saved", payload={"event_id": "evt-1"}),
        DomainEventMessage(name="crm.events.conversion.saved", payload={"event_id": "evt-2"}),
    ]

    bus.subscribe("crm.events.metric.saved", metric_handler)
    bus.subscribe("crm.events.conversion.saved", conversion_handler)

    bus.publish_many(messages)

    assert [message.payload["event_id"] for message in metric_handler.messages] == ["evt-1"]
    assert [message.payload["event_id"] for message in conversion_handler.messages] == ["evt-2"]
    assert [message.name for message in queue.drain()] == [
        "crm.events.metric.saved",
        "crm.events.conversion.saved",
    ]


def test_event_bus_rejects_blank_event_names() -> None:
    bus = InMemoryEventBus()
    handler = RecordingHandler()

    with pytest.raises(BaseInfraException, match="Event name is required"):
        bus.subscribe("   ", handler)

    with pytest.raises(BaseInfraException, match="Event name is required"):
        bus.publish(DomainEventMessage(name="   "))


def test_event_bus_unsubscribe_validates_registered_handler() -> None:
    bus = InMemoryEventBus()

    with pytest.raises(BaseInfraException, match="Handler is not registered"):
        bus.unsubscribe("crm.events.saved", RecordingHandler())


def test_event_bus_unsubscribe_removes_handler_from_future_notifications() -> None:
    bus = InMemoryEventBus()
    handler = RecordingHandler()

    bus.subscribe("crm.events.saved", handler)
    bus.unsubscribe("crm.events.saved", handler)
    bus.publish(DomainEventMessage(name="crm.events.saved", payload={"event_id": "evt-1"}))

    assert handler.messages == []
