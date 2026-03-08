from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.contracts.subscription import SubscriptionSnapshotDTO
from app.infra.db.models import Subscription
from app.domain.contracts.subscription_repository_protocol import SubscriptionRepositoryProtocol


class SubscriptionRepository(SubscriptionRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_latest_subscription(
        self,
        *,
        app_id: int,
        user_id: str,
        platform: str,
    ) -> SubscriptionSnapshotDTO | None:
        stmt = (
            select(Subscription)
            .where(
                Subscription.app_id == app_id,
                Subscription.user_id == user_id,
                Subscription.platform == platform,
            )
            .order_by(Subscription.last_verified_at.desc().nullslast(), Subscription.started_at.desc())
        )
        subscription = self.db.execute(stmt).scalars().first()
        if subscription is None:
            return None

        raw_price = subscription.price
        price = float(raw_price) if isinstance(raw_price, Decimal) else float(raw_price or 0)
        return SubscriptionSnapshotDTO(
            subscription_id=subscription.id,
            status=subscription.status,
            expires_at=subscription.expires_at,
            price=price,
            currency=subscription.currency,
        )

    def upsert_subscription(self, subscription: dict) -> None:
        stmt = pg_insert(Subscription).values([subscription])
        self.db.execute(
            stmt.on_conflict_do_update(
                index_elements=[
                    Subscription.app_id,
                    Subscription.user_id,
                    Subscription.platform,
                    Subscription.product_id,
                ],
                set_={
                    "status": stmt.excluded.status,
                    "started_at": stmt.excluded.started_at,
                    "expires_at": stmt.excluded.expires_at,
                    "price": stmt.excluded.price,
                    "currency": stmt.excluded.currency,
                    "last_verified_at": stmt.excluded.last_verified_at,
                },
            )
        )
    
    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
