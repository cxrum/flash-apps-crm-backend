from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmAppUserEntity:
    app_id: int
    app_user_id: int | None = None
    created_at: datetime | None = None
