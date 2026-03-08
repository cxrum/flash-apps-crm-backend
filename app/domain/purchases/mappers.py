
from __future__ import annotations

from app.domain.purchases.entities import SubscriptionSnapshotEntity


class SubscriptionSnapshotMappers:
    @staticmethod
    def to_dict(subscription: SubscriptionSnapshotEntity) -> dict[str, object]:
        return {
            "id": subscription.subscription_id,
            "status": subscription.status,
            "expires_at": subscription.expires_at,
            "price": subscription.price,
            "currency": subscription.currency,
        }
