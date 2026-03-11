from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CrmAppEntity:
    name: str
    code_slug: str
    description: str | None = None
    tech_description: str | None = None
    status: str = "active"
    logo_url: str | None = None
    screenshots: list[str] = field(default_factory=list)
    app_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None