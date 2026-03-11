from dataclasses import dataclass, field
from datetime import datetime

@dataclass
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

    def activate(self) -> None:
        self.status = "active"
        self.updated_at = datetime.now()

    def draft(self) -> None:
        self.status = "draft"
        self.updated_at = datetime.now()
    
    def archive(self) -> None:
        self.status = "archived"
        self.updated_at = datetime.now()

    def add_screenshot(self, url: str) -> None:
        self.screenshots.append(url)
        self.updated_at = datetime.now()