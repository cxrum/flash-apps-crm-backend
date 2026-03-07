from __future__ import annotations

from typing import Protocol

from app.contracts.events import EventRecordDTO


class EventsRepositoryProtocol(Protocol):
    def insert_events(self, events: list[EventRecordDTO]) -> int: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

