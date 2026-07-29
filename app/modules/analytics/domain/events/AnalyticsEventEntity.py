from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AnalyticsEventEntity:
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

    def payload_value(self, key: str, default: Any = None) -> Any:
        return self.payload.get(key, default)

    def geo(self) -> Any | None:
        return self.payload_value("geo")

    def ip(self) -> Any | None:
        return self.payload_value("ip")

    def ua(self) -> Any | None:
        return self.payload_value("ua")
