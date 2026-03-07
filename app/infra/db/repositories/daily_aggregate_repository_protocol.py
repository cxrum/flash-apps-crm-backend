from __future__ import annotations

from typing import Protocol


class DailyAggregateRepositoryProtocol(Protocol):
    def upsert_daily_aggregate(self, aggregate: dict) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

