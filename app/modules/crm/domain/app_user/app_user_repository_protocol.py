from __future__ import annotations

from typing import Protocol

from app.modules.crm.domain.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.modules.crm.domain.pagination import Pagination


class CrmAppUserRepositoryProtocol(Protocol):
    def save(self, entity: CrmAppUserEntity) -> CrmAppUserEntity: ...
    def save_many(self, entities: list[CrmAppUserEntity]) -> list[CrmAppUserEntity]: ...
    def get_by_id(self, app_user_id: int) -> CrmAppUserEntity | None: ...
    def delete(self, app_user_id: int) -> CrmAppUserEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmAppUserEntity]: ...
