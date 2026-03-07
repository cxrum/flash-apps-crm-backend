from __future__ import annotations

from typing import Protocol


class SubscriptionRepositoryProtocol(Protocol):
    def upsert_subscription(self, subscription: dict) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

