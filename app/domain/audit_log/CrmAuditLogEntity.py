from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmAuditLogEntity:
    entity_changed: str
    user_id: int | None = None
    app_id: int | None = None
    entity_id: str | None = None
    old_value: dict[str, Any] | list[Any] | None = None
    new_value: dict[str, Any] | list[Any] | None = None
    changed_at: datetime | None = None
    audit_log_id: int | None = None