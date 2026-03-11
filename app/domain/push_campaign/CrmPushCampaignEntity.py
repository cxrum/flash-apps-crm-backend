from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CrmPushCampaignEntity:
    app_id: int
    title: str
    body: str
    image_url: str | None = None
    target_link: str | None = None
    geo_filter: dict[str, Any] = field(default_factory=dict)
    scheduled_at: datetime | None = None
    status: str = "draft"
    created_by_user_id: int | None = None
    campaign_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None