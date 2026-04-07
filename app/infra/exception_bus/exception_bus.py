from __future__ import annotations

from collections.abc import Sequence

from app.domain.event_bus.events.exception_event import ExceptionEvent
from app.domain.event_bus.service_protocol import (
    AsyncEventMessageHandler,
    EventMessageHandler,
    IAsyncEventBus,
    IAsyncExceptionBus,
)
from app.infra.exception import BaseInfraException


class AsyncExceptionBusAdapter(IAsyncExceptionBus):
    def __init__(self, event_bus: IAsyncEventBus) -> None:
        self._event_bus = event_bus

    def subscribe(
        self,
        event_name: str,
        handler: AsyncEventMessageHandler | EventMessageHandler,
    ) -> None:
        self._event_bus.subscribe(event_name, handler)

    def unsubscribe(
        self,
        event_name: str,
        handler: AsyncEventMessageHandler | EventMessageHandler,
    ) -> None:
        self._event_bus.unsubscribe(event_name, handler)

    async def publish(self, message: ExceptionEvent) -> None:
        self._validate_message(message)
        await self._event_bus.publish(message)

    async def publish_many(self, messages: Sequence[ExceptionEvent]) -> None:
        validated_messages = tuple(messages)
        for message in validated_messages:
            self._validate_message(message)
        await self._event_bus.publish_many(validated_messages)

    async def start(self) -> None:
        await self._event_bus.start()

    async def stop(self) -> None:
        await self._event_bus.stop()

    @staticmethod
    def _validate_message(message: object) -> ExceptionEvent:
        if not isinstance(message, ExceptionEvent):
            raise BaseInfraException(
                "AsyncExceptionBusAdapter expected ExceptionEvent message"
            )
        return message
