from __future__ import annotations

from typing import Protocol

from app.domain.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.pagination import Pagination


class CrmPushEventRepositoryProtocol(Protocol):
    def insert(self, entity: CrmPushEventEntity) -> CrmPushEventEntity: ...
    def insert_many(self, entities: list[CrmPushEventEntity]) -> list[CrmPushEventEntity]: ...
    def get_by_id(self, push_event_id: int) -> CrmPushEventEntity | None: ...
    def delete(self, push_event_id: int) -> CrmPushEventEntity: ...
    def list_by_campaign_id(
        self,
        campaign_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPushEventEntity]: ...
