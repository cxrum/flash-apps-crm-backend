from __future__ import annotations

from typing import Protocol

from app.contracts.subscription import SubscriptionSnapshotDTO


class SubscriptionRepositoryProtocol(Protocol):
    def get_latest_subscription(
        self,
        *,
        app_id: int,
        user_id: str,
        platform: str,
    ) -> SubscriptionSnapshotDTO | None: ...
    def upsert_subscription(self, subscription: dict) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
