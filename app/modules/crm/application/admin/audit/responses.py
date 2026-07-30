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
