from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmUserAppAccessEntity:
    user_id: int
    app_id: int
    role_id: int
    assigned_at: datetime | None = None