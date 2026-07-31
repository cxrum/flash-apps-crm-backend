from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyticsAppEntity:
    """Analytics' read-only reference to an application configuration."""

    code_slug: str
    app_id: int | None = None
