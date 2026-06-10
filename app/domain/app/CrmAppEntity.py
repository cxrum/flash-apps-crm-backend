from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.exceptions import AppStatusDoestExist


@dataclass
class CrmAppEntity:
    name: str
    code_slug: str
    status: str
    description: str | None = None
    tech_description: str | None = None
    logo_url: str | None = None
    screenshots: list[str] = field(default_factory=list)
    app_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def __available_statuses() -> list[str]:
        return ["active", "draft", "archive"]

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

    @staticmethod
    def create(
        *,
        code_slug: str,
        name: str,
        status: str = "draft",
        description: str | None = None,
        tech_description: str | None = None,
        logo_url: str | None = None,
        screenshots: list[str] = [],
    ) -> "CrmAppEntity":
        if status not in CrmAppEntity.__available_statuses():
            raise AppStatusDoestExist(status)

        return CrmAppEntity(
            code_slug=code_slug,
            name=name,
            status=status,
            description=description,
            tech_description=tech_description,
            logo_url=logo_url,
            screenshots=screenshots,
        )

    def update(
        self,
        *,
        code_slug: str | None = None,
        name: str | None = None,
        description: str | None = None,
        tech_description: str | None = None,
        status: str | None = None,
        logo_url: str | None = None,
        screenshots: list[str] | None = None,
    ) -> None:
        self.code_slug = code_slug if code_slug is not None else self.code_slug
        self.name = name if name is not None else self.name
        self.description = description if description is not None else self.description
        self.tech_description = tech_description if tech_description is not None else self.tech_description
        self.status = status if status is not None and status in CrmAppEntity.__available_statuses() else self.status
        self.logo_url = logo_url if logo_url is not None else self.logo_url
        self.screenshots = screenshots if screenshots is not None else self.screenshots
        self.updated_at = datetime.now(UTC)
