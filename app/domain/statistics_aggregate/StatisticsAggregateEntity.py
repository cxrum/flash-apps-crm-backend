from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StatisticsAggregateEntity:
    app_platform_id: int
    geo: str
    date: datetime
    event_type: str
    event_key: str
    count: int
    aggregate_id: int | None = None
    amount_usd: float | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None
