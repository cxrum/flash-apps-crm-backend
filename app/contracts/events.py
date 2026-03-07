from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EventRecordDTO:
    event_id: str
    app_id: int
    event_name: str
    event_time: datetime
    platform: str
    anonymous_id: str
    user_id: str | None
    source: str | None
    campaign: str | None
    medium: str | None
    params: dict

