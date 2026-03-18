from __future__ import annotations

import asyncio

import pytest

from app.infra.exception_bus.exception_bus import AsyncExceptionBusAdapter
from app.application.exceptions import ApplicationError
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.exception_event import ExceptionEvent


class RecordingHandler:
    def handle(self, message: DomainEventMessage) -> None:
        return None


class RecordingAsyncEventBus:
    def __init__(self) -> None:
        self.subscriptions: list[tuple[str, object]] = []
        self.unsubscriptions: list[tuple[str, object]] = []
        self.published_messages: list[DomainEventMessage] = []
        self.published_batches: list[tuple[DomainEventMessage, ...]] = []
        self.start_calls = 0
        self.stop_calls = 0

    def subscribe(self, event_name: str, handler: object) -> None:
        self.subscriptions.append((event_name, handler))

    def unsubscribe(self, event_name: str, handler: object) -> None:
        self.unsubscriptions.append((event_name, handler))

    async def publish(self, message: DomainEventMessage) -> None:
        self.published_messages.append(message)

    async def publish_many(self, messages: tuple[DomainEventMessage, ...]) -> None:
        self.published_batches.append(messages)

    async def start(self) -> None:
        self.start_calls += 1

    async def stop(self) -> None:
        self.stop_calls += 1


def build_exception_event(**payload_overrides: object) -> ExceptionEvent:
    payload = {
        "exception_type": "RuntimeError",
        "exception_message": "failed",
        "context": {"source": "worker"},
    }
    payload.update(payload_overrides)
    return ExceptionEvent(name=ExceptionEvent.EVENT_NAME, payload=payload)


def test_async_exception_bus_adapter_delegates_lifecycle_and_subscription_methods() -> None:
    async def scenario() -> None:
        event_bus = RecordingAsyncEventBus()
        adapter = AsyncExceptionBusAdapter(event_bus)
        handler = RecordingHandler()

        adapter.subscribe(ExceptionEvent.EVENT_NAME, handler)
        adapter.unsubscribe(ExceptionEvent.EVENT_NAME, handler)
        await adapter.start()
        await adapter.stop()

        assert event_bus.subscriptions == [(ExceptionEvent.EVENT_NAME, handler)]
        assert event_bus.unsubscriptions == [(ExceptionEvent.EVENT_NAME, handler)]
        assert event_bus.start_calls == 1
        assert event_bus.stop_calls == 1

    asyncio.run(scenario())


def test_async_exception_bus_adapter_forwards_exception_events() -> None:
    async def scenario() -> None:
        event_bus = RecordingAsyncEventBus()
        adapter = AsyncExceptionBusAdapter(event_bus)
        message = build_exception_event(context={"source": "sdk", "event_id": "evt-1"})

        await adapter.publish(message)
        await adapter.publish_many([message])

        assert event_bus.published_messages == [message]
        assert event_bus.published_batches == [(message,)]

    asyncio.run(scenario())


def test_async_exception_bus_adapter_rejects_non_exception_message() -> None:
    async def scenario() -> None:
        event_bus = RecordingAsyncEventBus()
        adapter = AsyncExceptionBusAdapter(event_bus)
        message = DomainEventMessage(name="crm.events.saved", payload={"event_id": "evt-1"})

        with pytest.raises(
            ApplicationError,
            match="AsyncExceptionBusAdapter expected ExceptionEvent message",
        ):
            await adapter.publish(message)

        assert event_bus.published_messages == []
        assert event_bus.published_batches == []

    asyncio.run(scenario())


def test_async_exception_bus_adapter_rejects_mixed_batches_before_forwarding() -> None:
    async def scenario() -> None:
        event_bus = RecordingAsyncEventBus()
        adapter = AsyncExceptionBusAdapter(event_bus)
        valid_message = build_exception_event()
        invalid_message = DomainEventMessage(
            name="crm.events.saved",
            payload={"event_id": "evt-1"},
        )

        with pytest.raises(
            ApplicationError,
            match="AsyncExceptionBusAdapter expected ExceptionEvent message",
        ):
            await adapter.publish_many([valid_message, invalid_message])

        assert event_bus.published_messages == []
        assert event_bus.published_batches == []

    asyncio.run(scenario())
