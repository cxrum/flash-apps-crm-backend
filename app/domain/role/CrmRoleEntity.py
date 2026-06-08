from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import ClassVar

from app.domain.role.exceptions import AdminAccessRequired, ManagerAccessRequired, RoleAccessException


class Roles(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    



@dataclass(frozen=True)
class CrmRoleEntity:
    code: str
    display_name: str
    role_id: int | None = None
    created_at: datetime | None = None

    roles_structure: ClassVar[tuple[Roles, ...]] = (Roles.MANAGER, Roles.ADMIN)
    
    @classmethod
    def normalize_role(cls, role: Roles | str) -> Roles | None:
        if isinstance(role, Roles):
            return role
        try:
            return Roles(role)
        except ValueError:
            return None
        
    @classmethod
    def _role_level(cls, role: Roles | str) -> int | None:
        normalized_role = cls.normalize_role(role)
        if normalized_role is None:
            return None

        try:
            return cls.roles_structure.index(normalized_role)
        except ValueError:
            return None

    def compare(self, role: Roles | str) -> bool:
        current_role_level = self._role_level(self.code)
        required_role_level = self._role_level(role)

        if current_role_level is None or required_role_level is None:
            return False

        return current_role_level >= required_role_level
        
    def required(self, role: Roles | str) -> None:
        is_same = self.compare(role)
        if not is_same:
            if self.normalize_role(self.code) is Roles.ADMIN:
                raise AdminAccessRequired()
            elif self.normalize_role(self.code) is Roles.MANAGER:
                raise ManagerAccessRequired()
            else:
                raise RoleAccessException()

    def can_share_app_access(self) -> bool:
        return self.compare(Roles.ADMIN)

    def required_share_app_access(self) -> None:
        self.required(Roles.ADMIN)
    
    def is_admin_role(self) -> bool:
        return self.normalize_role(self.code) is Roles.ADMIN

    def is_manager_role(self) -> bool:
        return self.normalize_role(self.code) is Roles.MANAGER
