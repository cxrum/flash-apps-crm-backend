from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CrmRoleEntity:
    code: str
    display_name: str
    role_id: int | None = None
    created_at: datetime | None = None
    
    def is_admin_role(self) -> bool:
        return self.code == "admin"
    
    def is_manager_role(self) -> bool:
        return self.code == "manager"