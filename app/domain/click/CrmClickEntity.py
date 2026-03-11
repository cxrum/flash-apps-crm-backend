from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmClickEntity:
    click_id: str
    app_platform_id: int
    status: str = "accepted"
    raw_query: dict[str, Any] = field(default_factory=dict)
    ip_address: str | None = None
    user_agent: str | None = None
    geo: dict[str, Any] = field(default_factory=dict)
    referrer: str | None = None
    source: str | None = None
    redirect_target: str | None = None
    normalized_params: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
