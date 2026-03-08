from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.domain.purchases.entities import SubscriptionSnapshotEntity
from app.domain.purchases.mappers import SubscriptionSnapshotMappers
from app.infra.db.models import Subscription
from app.domain.purchases.subscription_repository_protocol import SubscriptionRepositoryProtocol


class SubscriptionRepository(SubscriptionRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_latest_subscription(
        self,
        *,
        app_id: int,
        user_id: str,
        platform: str,
    ) -> SubscriptionSnapshotEntity | None:
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
        return SubscriptionSnapshotEntity(
            subscription_id=subscription.id,
            status=subscription.status,
            expires_at=subscription.expires_at,
            price=price,
            currency=subscription.currency,
        )

    def upsert_subscription(self, subscription: SubscriptionSnapshotEntity) -> None:
        stmt = pg_insert(Subscription).values([SubscriptionSnapshotMappers.to_dict(subscription)])
        self.db.execute(
            stmt.on_conflict_do_update(
                index_elements=[
                    Subscription.id,
                ],
                set_={
                    "status": stmt.excluded.status,
                    "expires_at": stmt.excluded.expires_at,
                    "price": stmt.excluded.price,
                    "currency": stmt.excluded.currency,
                },
            )
        )
    
    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
