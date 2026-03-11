from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmPushTokenEntity:
    install_id: int
    token: str
    geo: dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    last_seen_at: datetime | None = None
    token_id: int | None = None
    created_at: datetime | None = None
