from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class EventEntity:
    event_id: str
    click_id: str
    event_type: str
    event_key: str
    event_time_utc: datetime
    app_user_id: int | None = None
    amount: float | None = None
    currency: str | None = None
    amount_usd: float | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
