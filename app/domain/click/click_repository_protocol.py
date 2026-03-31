from __future__ import annotations

from typing import Protocol

from app.domain.click.CrmClickEntity import CrmClickEntity

from app.domain.pagination import Pagination


class CrmClickRepositoryProtocol(Protocol):
    def insert(self, entity: CrmClickEntity) -> CrmClickEntity: ...
    def insert_many(self, entities: list[CrmClickEntity]) -> list[CrmClickEntity]: ...
    def get_by_id(self, click_id: str) -> CrmClickEntity | None: ...
    def delete(self, click_id: str) -> CrmClickEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmClickEntity]: ...
    def list_by_platform_id(
        self,
        app_platform_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmClickEntity]: ...
