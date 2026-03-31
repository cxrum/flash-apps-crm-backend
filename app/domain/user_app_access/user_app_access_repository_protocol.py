from __future__ import annotations

from typing import Protocol

from app.domain.user import CrmUserEntity
from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.pagination import Pagination


class CrmUserAppAccessRepositoryProtocol(Protocol):
    def save(self, entity: CrmUserAppAccessEntity) -> CrmUserAppAccessEntity: ...
    def save_many(self, entities: list[CrmUserAppAccessEntity]) -> list[CrmUserAppAccessEntity]: ...
    def get_by_user_and_app(self, user_id: int, app_id: int) -> CrmUserAppAccessEntity | None: ...
    def list_by_user_id(
        self,
        user_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserAppAccessEntity]: ...
    def delete(
        self,
        user_id: int,
        app_id: int
    ) -> CrmUserAppAccessEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmUserAppAccessEntity]: ...