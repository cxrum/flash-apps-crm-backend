from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
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

    def update(
        self,
        *,
        app_id: int | None = None,
        title: str | None = None,
        body: str | None = None,
        image_url: str | None = None,
        target_link: str | None = None,
        geo_filter: dict[str, Any] | None = None,
        scheduled_at: datetime | None = None,
        status: str | None = None,
        created_by_user_id: int | None = None,
    ) -> None:
        self.app_id = app_id if app_id is not None else self.app_id
        self.title = title if title is not None else self.title
        self.body = body if body is not None else self.body
        self.image_url = image_url if image_url is not None else self.image_url
        self.target_link = target_link if target_link is not None else self.target_link
        self.geo_filter = geo_filter if geo_filter is not None else self.geo_filter
        self.scheduled_at = scheduled_at if scheduled_at is not None else self.scheduled_at
        self.status = status if status is not None else self.status
        self.created_by_user_id = (
            created_by_user_id if created_by_user_id is not None else self.created_by_user_id
        )

        self.updated_at = datetime.now(UTC)
