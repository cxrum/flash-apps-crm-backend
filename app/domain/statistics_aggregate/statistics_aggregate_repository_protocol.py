from __future__ import annotations

from typing import Protocol

from app.domain.statistics_aggregate.StatisticsAggregateEntity import StatisticsAggregateEntity


class StatisticsRepositoryProtocol(Protocol):
    def save(self, entity: StatisticsAggregateEntity) -> StatisticsAggregateEntity: ...
    def save_many(self, entities: list[StatisticsAggregateEntity]) -> list[StatisticsAggregateEntity]: ...
    def get_by_id(self, aggregate_id: int) -> StatisticsAggregateEntity | None: ...
    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        limit: int = 100,
    ) -> list[StatisticsAggregateEntity]: ...
