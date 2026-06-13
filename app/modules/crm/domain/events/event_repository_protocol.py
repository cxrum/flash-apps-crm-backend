from __future__ import annotations

from typing import Protocol

from app.modules.crm.domain.events.CrmEventEntity import EventEntity
from app.modules.crm.domain.pagination import Pagination


class CrmEventRepositoryProtocol(Protocol):
    def insert(self, entity: EventEntity) -> EventEntity: ...
    def insert_many(self, entities: list[EventEntity]) -> list[EventEntity]: ...
    def get_by_id(self, event_id: str) -> EventEntity | None: ...
    def delete(self, event_id: str) -> EventEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[EventEntity]: ...
    def list_by_click_id(
        self,
        click_id: str,
        *,
        app_id: int | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[EventEntity]: ...
