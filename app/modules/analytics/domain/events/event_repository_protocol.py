from __future__ import annotations

from typing import Protocol

from app.modules.analytics.domain.events.AnalyticsEventEntity import AnalyticsEventEntity
from app.modules.crm.domain.pagination import Pagination


class AnalyticsEventRepositoryProtocol(Protocol):
    def insert(self, entity: AnalyticsEventEntity) -> AnalyticsEventEntity: ...
    def insert_many(self, entities: list[AnalyticsEventEntity]) -> list[AnalyticsEventEntity]: ...
    def get_by_id(self, event_id: str) -> AnalyticsEventEntity | None: ...
    def delete(self, event_id: str) -> AnalyticsEventEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsEventEntity]: ...
    def list_by_click_id(
        self,
        click_id: str,
        *,
        app_id: int | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsEventEntity]: ...
