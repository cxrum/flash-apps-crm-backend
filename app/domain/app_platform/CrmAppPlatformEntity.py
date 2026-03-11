from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmAppPlatformEntity:
    app_id: int
    platform: str
    package_name: str
    install_key: str
    store_url: str | None = None
    sdk_public_key: str | None = None
    sdk_secret_hash: str | None = None
    status: str = "active"
    platform_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None