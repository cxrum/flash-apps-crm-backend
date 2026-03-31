from __future__ import annotations

from typing import Protocol

from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity
from app.domain.pagination import Pagination


class CrmUserPermissionsRepositoryProtocol(Protocol):
    def save(self, entity: CrmUserPermissionEntity) -> CrmUserPermissionEntity: ...
    def save_many(self, entities: list[CrmUserPermissionEntity]) -> list[CrmUserPermissionEntity]: ...
    def list_by_user_id(
        self,
        user_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserPermissionEntity]: ...
    def delete(
        self,
        user_id: int,
        permission_id: int,
    ) ->CrmUserPermissionEntity: ...
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
