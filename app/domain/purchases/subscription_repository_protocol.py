from __future__ import annotations

from typing import Protocol

from app.domain.purchases.entities import SubscriptionSnapshotEntity


class SubscriptionRepositoryProtocol(Protocol):
    def get_latest_subscription(
        self,
        *,
        app_id: int,
        user_id: str,
        platform: str,
    ) -> SubscriptionSnapshotEntity | None: ...
    def upsert_subscription(self, subscription: SubscriptionSnapshotEntity) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
