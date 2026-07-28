from __future__ import annotations

from collections.abc import Sequence

from app.core.bus.contract import AsyncEventMessageHandler, EventMessageHandler, IAsyncMessageQueue
from app.core.bus.event.bus import InMemoryAsyncEventBus as CoreInMemoryAsyncEventBus
from app.core.bus.event.bus import InMemoryAsyncMessageQueue
from app.core.bus.type import EventMessage
from app.core.exception import BusException
from app.modules.crm.application.exception import GeneralException


class InMemoryAsyncEventBus(CoreInMemoryAsyncEventBus):
    def __init__(self, workers_count: int = 1, message_queue: IAsyncMessageQueue | None = None) -> None:
        super().__init__(workers_count=workers_count, message_queue=message_queue)

    def subscribe(
        self,
        event_name: str,
        handler: AsyncEventMessageHandler | EventMessageHandler,
    ) -> None:
        try:
            super().subscribe(event_name, handler)
        except BusException as exc:
            raise GeneralException(str(exc)) from exc

    def unsubscribe(
        self,
        event_name: str,
        handler: AsyncEventMessageHandler | EventMessageHandler,
    ) -> None:
        try:
            super().unsubscribe(event_name, handler)
        except BusException as exc:
            raise GeneralException(str(exc)) from exc

    async def publish(self, message: EventMessage) -> None:
        try:
            await super().publish(message)
        except BusException as exc:
            raise GeneralException(str(exc)) from exc

    async def publish_many(self, messages: Sequence[EventMessage]) -> None:
        try:
            await super().publish_many(messages)
        except BusException as exc:
            raise GeneralException(str(exc)) from exc

__all__ = ["InMemoryAsyncEventBus", "InMemoryAsyncMessageQueue"]
