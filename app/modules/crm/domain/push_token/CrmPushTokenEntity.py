from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmPushTokenEntity:
    install_id: int
    click_id: str
    push_token: str
    app_user_id: int | None = None
    
    country_code: str | None = None
    lang: str | None = None
    geo: str | None = None
    
    is_active: bool = True
    last_seen_at: datetime | None = None
    token_id: int | None = None
    created_at: datetime | None = None
