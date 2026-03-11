from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmPermissionEntity:
    code: str
    description: str | None = None
    permission_id: int | None = None
    created_at: datetime | None = None