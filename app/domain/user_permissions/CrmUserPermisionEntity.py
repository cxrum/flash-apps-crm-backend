from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmUserPermisionEntity:
    user_id: int
    app_id: int
    permission_id: int
    assigned_at: datetime | None = None