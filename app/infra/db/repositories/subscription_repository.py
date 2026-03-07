from __future__ import annotations

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.infra.db.models import Subscription
from app.infra.db.repositories.subscription_repository_protocol import SubscriptionRepositoryProtocol


class SubscriptionRepository(SubscriptionRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

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

