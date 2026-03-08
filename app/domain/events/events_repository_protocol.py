from __future__ import annotations

from typing import Protocol

from app.domain.events.entities import EventEntity


class EventsRepositoryProtocol(Protocol):
    def insert_events(self, events: list[EventEntity]) -> int: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

