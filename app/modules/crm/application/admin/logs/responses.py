from datetime import datetime
from typing import Any

from app.modules.crm.application.base import BaseResponse


class AuditLogResponseEntry(BaseResponse):
    entity_changed: str
    user_id: int | None = None
    app_id: int | None = None
    entity_id: str | None = None
    old_value: dict[str, Any] | list[Any] | None = None
    new_value: dict[str, Any] | list[Any] | None = None
    changed_at: datetime | None = None
    audit_log_id: int | None = None


class ListAuditLogsResponse(BaseResponse):
    audit_logs: list[AuditLogResponseEntry]


class RawEventLogResponseEntry(BaseResponse):
    event_id: str
    click_id: str
    event_type: str
    event_key: str
    event_time_utc: datetime
    app_user_id: int | None = None
    amount: float | None = None
    currency: str | None = None
    amount_usd: float | None = None
    payload: dict[str, Any] | None = None
    created_at: datetime | None = None


class ListRawEventsResponse(BaseResponse):
    events: list[RawEventLogResponseEntry]


class ClickLogResponseEntry(BaseResponse):
    click_id: str
    app_platform_id: int
    status: str = "accepted"
    raw_query: dict[str, Any] | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    geo: dict[str, Any] | None = None
    referrer: str | None = None
    source: str | None = None
    redirect_target: str | None = None
    normalized_params: dict[str, Any] | None = None
    created_at: datetime | None = None


class ListClickLogsResponse(BaseResponse):
    clicks: list[ClickLogResponseEntry]
