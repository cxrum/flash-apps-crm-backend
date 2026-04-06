import asyncio
import inspect
import logging
from collections.abc import Sequence

from app.application.exception import GeneralException
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.service_protocol import (
    AsyncEventMessageHandler,
    EventMessageHandler,
    IAsyncEventBus,
    IAsyncMessageQueue,
)
from app.infra.event_bus.async_bus.worker import AsyncWorkerProtocol


logger = logging.getLogger(__name__)
EventHandler = AsyncEventMessageHandler | EventMessageHandler


class InMemoryAsyncMessageQueue(IAsyncMessageQueue):
    def __init__(self, maxsize: int = 120) -> None:
        self._messages: asyncio.Queue[DomainEventMessage] = asyncio.Queue(maxsize)

    async def enqueue(self, message: DomainEventMessage) -> None:
        await self._messages.put(message)

    async def dequeue(self) -> DomainEventMessage:
        return await self._messages.get()

    def size(self) -> int:
        return self._messages.qsize()


class AsyncWorker(AsyncWorkerProtocol):
    def __init__(self, queue: IAsyncMessageQueue, handlers: dict[str, list[EventHandler]], *, id: int) -> None:
        self._queue = queue
        self._handlers = handlers
        self.__is_active = False
        self.__id = id
        self.__task: asyncio.Task[None] | None = None

    @property
    def id(self) -> int:
        return self.__id

    @property
    def is_active(self) -> bool:
        return self.__is_active

    async def start(self) -> None:
        if self.__task is not None and not self.__task.done():
            return
        self.__is_active = True
        self.__task = asyncio.create_task(
            self.execute(),
            name=f"in-memory-event-bus-worker-{self.__id}",
        )

    async def stop(self) -> None:
        self.__is_active = False
        if self.__task is None:
            return

        self.__task.cancel("Worker stopped")
        try:
            await self.__task
        except asyncio.CancelledError:
            pass
        finally:
            self.__task = None

    async def execute(self) -> None:
        while self.__is_active:
            try:
                event = await self._queue.dequeue()
            except asyncio.CancelledError:
                break

            for handler in tuple(self._handlers.get(event.name, ())):
                try:
                    await self._dispatch(handler, event)
                except Exception:
                    logger.exception(
                        "Async event handler failed",
                        extra={"event_name": event.name, "worker_id": self.__id},
                    )

    @staticmethod
    async def _dispatch(handler: EventHandler, event: DomainEventMessage) -> None:
        result = handler.handle(event)
        if inspect.isawaitable(result):
            await result

class InMemoryAsyncEventBus(IAsyncEventBus):
    def __init__(self, workers_count: int = 1, message_queue: IAsyncMessageQueue | None = None) -> None:
        self._message_queue = message_queue or InMemoryAsyncMessageQueue()
        self._subscribers: dict[str, list[EventHandler]] = {}
        if workers_count < 1:
            raise RuntimeError("Workers count cant be less than 1")

        self._workers: list[AsyncWorkerProtocol] = []

        for id in range(workers_count):
            worker = AsyncWorker(
                self._message_queue,
                self._subscribers,
                id=id
            )
            self._workers.append(worker)

    async def start(self) -> None:
        for worker in self._workers:
            await worker.start()

    async def stop(self) -> None:
        for worker in self._workers:
            await worker.stop()

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        normalized_event_name = self._normalize_event_name(event_name)
        handlers = self._subscribers.setdefault(normalized_event_name, [])
        if handler not in handlers:
            handlers.append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        normalized_event_name = self._normalize_event_name(event_name)
        handlers = self._subscribers.get(normalized_event_name)
        if handlers is None or handler not in handlers:
            raise GeneralException("Handler is not registered for this event")
        handlers.remove(handler)
        if not handlers:
            del self._subscribers[normalized_event_name]

    async def publish(self, message: DomainEventMessage) -> None:
        normalized_message = self._normalize_message(message)
        await self._message_queue.enqueue(normalized_message)

    async def publish_many(self, messages: Sequence[DomainEventMessage]) -> None:
        for message in messages:
           await self.publish(message)

    @staticmethod
    def _normalize_event_name(event_name: str) -> str:
        normalized_event_name = event_name.strip()
        if not normalized_event_name:
            raise GeneralException("Event name is required")
        return normalized_event_name

    def _normalize_message(self, message: DomainEventMessage) -> DomainEventMessage:
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
            return DomainEventMessage(
                name=normalized_name,
                correlation_id=message.correlation_id,
                payload=normalized_payload,
                metadata=normalized_metadata,
                occurred_at=message.occurred_at,
            )
