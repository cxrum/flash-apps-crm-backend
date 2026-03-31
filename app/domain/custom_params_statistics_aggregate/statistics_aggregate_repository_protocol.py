from __future__ import annotations

from datetime import date, datetime
from typing import Protocol

from app.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import (
    CustomParamsStatisticsAggregateEntity,
)

from app.domain.pagination import Pagination


class CustomParamsStatisticsRepositoryProtocol(Protocol):
    def save(self, entity: CustomParamsStatisticsAggregateEntity) -> CustomParamsStatisticsAggregateEntity: ...
    def save_many(
        self,
        entities: list[CustomParamsStatisticsAggregateEntity],
    ) -> list[CustomParamsStatisticsAggregateEntity]: ...
    def get_by_id(self, aggregate_id: int) -> CustomParamsStatisticsAggregateEntity | None: ...
    def delete(self, aggregate_id: int) -> CustomParamsStatisticsAggregateEntity: ...
    def list_by_filters(
        self,
        *,
        aggregate_id: int | None = None,
        app_platform_id: int | None = None,
        geo: str | None = None,
        ddate: date | None = None,
        event_type: str | None = None,
        event_key: str | None = None,
        param_key: str | None = None,
        param_value: str | None = None,
        count: int | None = None,
        amount_usd: float | None = None,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
        pagination: Pagination | None = None,
    ) -> list[CustomParamsStatisticsAggregateEntity]: ...
    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CustomParamsStatisticsAggregateEntity]: ...


CustomParamsStatisticsRepositoryProtocol = CustomParamsStatisticsRepositoryProtocol
