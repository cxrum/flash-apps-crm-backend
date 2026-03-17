from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from app.application.exceptions import ApplicationError
from app.domain.event_bus.base_event import DomainEventMessage
from app.infra.event_bus.async_bus.in_memory import (
    InMemoryAsyncEventBus,
    InMemoryAsyncMessageQueue,
)


class RecordingHandler:
    def __init__(self) -> None:
        self.messages: list[DomainEventMessage] = []
        self.called = asyncio.Event()

    def handle(self, message: DomainEventMessage) -> None:
        self.messages.append(message)
        self.called.set()


class AsyncRecordingHandler:
    def __init__(self) -> None:
        self.messages: list[DomainEventMessage] = []
        self.called = asyncio.Event()

    async def handle(self, message: DomainEventMessage) -> None:
        self.messages.append(message)
        self.called.set()


def test_async_message_queue_supports_enqueue_dequeue_and_size() -> None:
    async def scenario() -> None:
        queue = InMemoryAsyncMessageQueue()
        first = DomainEventMessage(name="event.first", payload={"value": 1})
        second = DomainEventMessage(name="event.second", payload={"value": 2})

        await queue.enqueue(first)
        await queue.enqueue(second)

        assert queue.size() == 2
        assert await queue.dequeue() == first
        assert await queue.dequeue() == second
        assert queue.size() == 0

    asyncio.run(scenario())


def test_async_event_bus_publish_enqueues_normalized_copy_without_inline_dispatch() -> None:
    async def scenario() -> None:
        queue = InMemoryAsyncMessageQueue()
        bus = InMemoryAsyncEventBus(message_queue=queue)
        handler = RecordingHandler()
        message = DomainEventMessage(
            name="  crm.events.saved  ",
            payload={"event_id": "evt-1"},
            metadata={"source": "sdk"},
            occurred_at=datetime(2026, 3, 13, 12, 0, tzinfo=UTC),
        )

        bus.subscribe("crm.events.saved", handler)
        await bus.publish(message)
        message.payload["event_id"] = "mutated"
        message.metadata["source"] = "changed"

        assert handler.messages == []
        assert queue.size() == 1
        queued = await queue.dequeue()
        assert queued.name == "crm.events.saved"
        assert queued.payload == {"event_id": "evt-1"}
        assert queued.metadata == {"source": "sdk"}
        assert queued.occurred_at == datetime(2026, 3, 13, 12, 0, tzinfo=UTC)

    asyncio.run(scenario())


def test_async_event_bus_publish_many_preserves_order() -> None:
    async def scenario() -> None:
        queue = InMemoryAsyncMessageQueue()
        bus = InMemoryAsyncEventBus(message_queue=queue)
        messages = [
            DomainEventMessage(name="crm.events.metric.saved", payload={"event_id": "evt-1"}),
            DomainEventMessage(name="crm.events.conversion.saved", payload={"event_id": "evt-2"}),
        ]

        await bus.publish_many(messages)

        dequeued = [await queue.dequeue(), await queue.dequeue()]
        assert [message.name for message in dequeued] == [
            "crm.events.metric.saved",
            "crm.events.conversion.saved",
        ]

    asyncio.run(scenario())


def test_async_event_bus_rejects_blank_event_names() -> None:
    bus = InMemoryAsyncEventBus()
    handler = RecordingHandler()

    with pytest.raises(ApplicationError, match="Event name is required"):
        bus.subscribe("   ", handler)

    async def scenario() -> None:
        with pytest.raises(ApplicationError, match="Event name is required"):
            await bus.publish(DomainEventMessage(name="   "))

    asyncio.run(scenario())


def test_async_event_bus_unsubscribe_validates_registered_handler() -> None:
    bus = InMemoryAsyncEventBus()

    with pytest.raises(ApplicationError, match="Handler is not registered"):
        bus.unsubscribe("crm.events.saved", RecordingHandler())


def test_async_event_bus_rejects_non_positive_worker_counts() -> None:
    with pytest.raises(RuntimeError, match="Workers count cant be less than 1"):
        InMemoryAsyncEventBus(workers_count=0)


def test_async_event_bus_dispatches_async_handlers_once_even_with_duplicate_subscription() -> None:
    async def scenario() -> None:
        bus = InMemoryAsyncEventBus()
        handler = AsyncRecordingHandler()

        bus.subscribe("crm.events.saved", handler)
        bus.subscribe("crm.events.saved", handler)

        await bus.start()
        try:
            await bus.publish(DomainEventMessage(name="crm.events.saved", payload={"event_id": "evt-1"}))
            await asyncio.wait_for(handler.called.wait(), timeout=1)
        finally:
            await bus.stop()

        assert [message.payload["event_id"] for message in handler.messages] == ["evt-1"]

    asyncio.run(scenario())


def test_async_event_bus_dispatches_sync_handlers_and_ignores_unknown_events_or_unsubscribed_handlers() -> None:
    async def scenario() -> None:
        bus = InMemoryAsyncEventBus()
        matching_handler = RecordingHandler()
        removed_handler = RecordingHandler()

        bus.subscribe("crm.events.saved", matching_handler)
        bus.subscribe("crm.events.saved", removed_handler)
        bus.unsubscribe("crm.events.saved", removed_handler)

        await bus.start()
        try:
            await bus.publish(DomainEventMessage(name="crm.events.unknown", payload={"event_id": "evt-0"}))
            await bus.publish(DomainEventMessage(name="crm.events.saved", payload={"event_id": "evt-1"}))
            await asyncio.wait_for(matching_handler.called.wait(), timeout=1)
        finally:
            await bus.stop()

        assert removed_handler.messages == []
        assert [message.payload["event_id"] for message in matching_handler.messages] == ["evt-1"]

    asyncio.run(scenario())
