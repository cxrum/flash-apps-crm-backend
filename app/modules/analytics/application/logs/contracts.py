from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class AnalyticsLogsPagination:
    start_at: datetime | None = None
    end_at: datetime | None = None
    limit: int | None = None
    offset: int | None = None


@dataclass(frozen=True)
class ListAnalyticsClickLogsQuery:
    app_id: int
    click_id: str | None = None
    pagination: AnalyticsLogsPagination = field(default_factory=AnalyticsLogsPagination)


@dataclass(frozen=True)
class ListAnalyticsEventLogsQuery:
    app_id: int
    click_id: str | None = None
    event_key: str | None = None
    pagination: AnalyticsLogsPagination = field(default_factory=AnalyticsLogsPagination)


@dataclass(frozen=True)
class AnalyticsClickLog:
    click_id: str
    app_platform_id: int
    status: str
    raw_query: dict[str, Any]
    ip_address: str | None
    user_agent: str | None
    referrer: str | None
    source: str | None
    redirect_target: str | None
    normalized_params: dict[str, Any]
    created_at: datetime | None


@dataclass(frozen=True)
class AnalyticsEventLog:
    event_id: str
    click_id: str
    event_type: str
    event_key: str
    event_time_utc: datetime
    app_user_id: int | None
    amount: float | None
    currency: str | None
    amount_usd: float | None
    payload: dict[str, Any]
    created_at: datetime | None
