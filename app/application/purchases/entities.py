from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class VerifyPurchaseCommand:
    app_id: int
    platform: str
    anonymous_id: str
    user_id: str
    linked_at: datetime

