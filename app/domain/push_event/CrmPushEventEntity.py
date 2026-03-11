from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmPushEventEntity:
    campaign_id: int
    token_id: int
    event_type: str
    event_time_utc: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    push_event_id: int | None = None
    created_at: datetime | None = None