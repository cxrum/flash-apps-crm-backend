from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmUserAppAccessEntity:
    user_id: int
    app_id: int
    access_level: str = "manager"
    assigned_at: datetime | None = None