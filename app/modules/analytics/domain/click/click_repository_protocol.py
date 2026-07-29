from __future__ import annotations

from typing import Protocol

from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.crm.domain.pagination import Pagination


class AnalyticsClickRepositoryProtocol(Protocol):
    def insert(self, entity: AnalyticsClickEntity) -> AnalyticsClickEntity: ...
    def insert_many(self, entities: list[AnalyticsClickEntity]) -> list[AnalyticsClickEntity]: ...
    def get_by_id(self, click_id: str) -> AnalyticsClickEntity | None: ...
    def delete(self, click_id: str) -> AnalyticsClickEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsClickEntity]: ...
    def list_by_platform_id(
        self,
        app_platform_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsClickEntity]: ...
