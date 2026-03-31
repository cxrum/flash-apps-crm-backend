from __future__ import annotations

from typing import Protocol

from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.pagination import Pagination


class CrmMetricDefinitionRepositoryProtocol(Protocol):
    def save(self, entity: CrmMetricDefinitionEntity) -> CrmMetricDefinitionEntity: ...
    def save_many(self, entities: list[CrmMetricDefinitionEntity]) -> list[CrmMetricDefinitionEntity]: ...
    def get_by_id(self, metric_definition_id: int) -> CrmMetricDefinitionEntity | None: ...
    def delete(self, metric_definition_id: int) -> CrmMetricDefinitionEntity: ...
    def list_by_app_id(
        self,
        app_id: int | None,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmMetricDefinitionEntity]: ...
