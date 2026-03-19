from __future__ import annotations

from typing import Protocol

from app.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import (
    CustomParamsStatisticsAggregateEntity,
)


class CustomParamsStatisticsRepostitoryProtocol(Protocol):
    def save(self, entity: CustomParamsStatisticsAggregateEntity) -> CustomParamsStatisticsAggregateEntity: ...
    def save_many(
        self,
        entities: list[CustomParamsStatisticsAggregateEntity],
    ) -> list[CustomParamsStatisticsAggregateEntity]: ...
    def get_by_id(self, aggregate_id: int) -> CustomParamsStatisticsAggregateEntity | None: ...
    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        limit: int = 100,
    ) -> list[CustomParamsStatisticsAggregateEntity]: ...


CustomParamsStatisticsRepositoryProtocol = CustomParamsStatisticsRepostitoryProtocol
