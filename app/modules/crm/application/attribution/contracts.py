from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmClickContext:
    """CRM's narrow, non-persistent view of an Analytics click."""

    click_id: str
    app_platform_id: int
    install_id: int | None
    app_user_id: int | None


@dataclass(frozen=True)
class CrmPostbackContext:
    event_id: str
    click: CrmClickContext
    event_type: str
    event_key: str
    event_time_utc: datetime
    amount: float | None
    amount_usd: float | None
    payload: dict[str, Any]
    current_params: dict[str, Any]
