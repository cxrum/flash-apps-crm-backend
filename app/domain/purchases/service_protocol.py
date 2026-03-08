from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class PurchaseVerifyResult:
    status: str
    expires_at: datetime | None
    price: float
    currency: str
    subscription_id: int | None

    def as_dict(self) -> dict[str, str | int | float | None]:
        return {
            "status": self.status,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "price": self.price,
            "currency": self.currency,
            "subscription_id": self.subscription_id,
        }


class PurchasesServiceProtocol(Protocol):
    def verify_purchase(
        self,
        *,
        app_id: int,
        platform: str,
        anonymous_id: str,
        user_id: str,
        linked_at: datetime,
    ) -> PurchaseVerifyResult: ...
