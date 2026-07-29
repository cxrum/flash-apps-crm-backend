from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class AnalyticsInstallEntity:
    click_id: str
    app_platform_id: int
    app_user_id: int | None = None
    device_data: dict[str, Any] = field(default_factory=dict)
    install_id: int | None = None
    installed_at: datetime | None = None
