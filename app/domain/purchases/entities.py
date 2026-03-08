from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SubscriptionSnapshotEntity:
    subscription_id: int
    status: str
    expires_at: datetime | None
    price: float
    currency: str