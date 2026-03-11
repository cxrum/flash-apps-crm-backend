from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmRolePermissionEntity:
    role_id: int
    permission_id: int
    created_at: datetime | None = None