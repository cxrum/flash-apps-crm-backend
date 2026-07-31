from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyticsAppPlatformEntity:
    """Analytics' read-only reference to a platform's ingestion configuration."""

    app_id: int
    platform: str
    install_key: str
    sdk_secret_encrypted: str
    platform_id: int | None = None
