from __future__ import annotations

from typing import Protocol

from app.modules.crm.domain.pagination import Pagination
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity


class CrmUserPermissionsRepositoryProtocol(Protocol):
    def save(self, entity: CrmUserPermissionEntity) -> CrmUserPermissionEntity: ...
    def save_many(self, entities: list[CrmUserPermissionEntity]) -> list[CrmUserPermissionEntity]: ...
    def list_by_user_id(
        self,
        user_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserPermissionEntity]: ...
    def delete(self, user_id: int, permission_id: int, app_id: int) -> CrmUserPermissionEntity: ...
    def list_by_permission_id(
        self,
        permission_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserPermissionEntity]: ...
    def list_by_user_id_per_app(
        self,
        user_id: int,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPermissionEntity]: ...
