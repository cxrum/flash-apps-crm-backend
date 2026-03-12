
from dataclasses import dataclass


@dataclass(frozen=True)
class SdkInstallResponse:
    click_id: str
    app_user_id: int | None = None


@dataclass(frozen=True)
class SdkEventResponse:
    received: int
    inserted: int
    ignored_duplicates: int
    