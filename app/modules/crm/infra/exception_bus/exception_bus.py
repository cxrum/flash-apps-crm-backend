from __future__ import annotations

from collections.abc import Sequence

from app.core.bus.contract import AsyncEventMessageHandler, EventMessageHandler, IAsyncEventBus, IAsyncExceptionBus
from app.core.bus.exception.bus import AsyncExceptionBusAdapter as CoreAsyncExceptionBusAdapter
from app.core.bus.exception_event import ExceptionEvent
from app.core.exception import BusException
from app.modules.crm.infra.exception import BaseInfraException


class AsyncExceptionBusAdapter(IAsyncExceptionBus):
    def __init__(self, event_bus: IAsyncEventBus) -> None:
        self._core_adapter = CoreAsyncExceptionBusAdapter(event_bus)

    def subscribe(
        self,
        event_name: str,
        handler: AsyncEventMessageHandler | EventMessageHandler,
    ) -> None:
        try:
            self._core_adapter.subscribe(event_name, handler)
        except BusException as exc:
            raise BaseInfraException(str(exc)) from exc

    def unsubscribe(
        self,
        event_name: str,
        handler: AsyncEventMessageHandler | EventMessageHandler,
    ) -> None:
        try:
            self._core_adapter.unsubscribe(event_name, handler)
        except BusException as exc:
            raise BaseInfraException(str(exc)) from exc

    async def publish(self, message: ExceptionEvent) -> None:
        self._validate_message(message)
        try:
            await self._core_adapter.publish(message)
        except BusException as exc:
            raise BaseInfraException(str(exc)) from exc

    async def publish_many(self, messages: Sequence[ExceptionEvent]) -> None:
        validated_messages = tuple(messages)
        for message in validated_messages:
            self._validate_message(message)
        try:
            await self._core_adapter.publish_many(validated_messages)
        except BusException as exc:
            raise BaseInfraException(str(exc)) from exc

    async def start(self) -> None:
        await self._core_adapter.start()

    async def stop(self) -> None:
        await self._core_adapter.stop()

    @staticmethod
    def _validate_message(message: object) -> ExceptionEvent:
        if not isinstance(message, ExceptionEvent):
            raise BaseInfraException("AsyncExceptionBusAdapter expected ExceptionEvent message")
        return message
