
from dataclasses import dataclass


@dataclass(frozen=True)
class SdkInstallResponse:
    click_id: str
    app_user_id: int | None = None

