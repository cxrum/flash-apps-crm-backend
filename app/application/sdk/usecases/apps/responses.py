
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateAppResponse:
    app_id: int

@dataclass(frozen=True)
class CreatePlatformResponse:
    platform_id: int

@dataclass(frozen=True)
class AppConfigQueryEntry:
    code: str
    display_name: str
    scope: str
    value_type: str
    value: object
    version: float
    is_masked: bool = True
    is_required: bool = False
    is_active: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

@dataclass(frozen=True)
class AppConfigQueryResponse:
    configurations: list[AppConfigQueryEntry]

