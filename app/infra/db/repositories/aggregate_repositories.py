from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import (
    CustomParamsStatisticsAggregateEntity,
)
from app.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
from app.domain.statistics_aggregate.StatisticsAggregateEntity import StatisticsAggregateEntity
from app.domain.statistics_aggregate.statistics_aggregate_repository_protocol import StatisticsRepositoryProtocol
from app.infra.db.aggregates.models import CustomParamsStatisticsAggregate, StatisticsAggregate


class SqlAlchemyStatisticsRepository(StatisticsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: StatisticsAggregate) -> StatisticsAggregateEntity:
        return StatisticsAggregateEntity(
            aggregate_id=row.aggregate_id,
            app_platform_id=row.app_platform_id,
            geo=row.geo,
            date=row.date,
            event_type=row.event_type,
            event_key=row.event_key,
            count=row.count,
            amount_usd=row.amount_usd,
            updated_at=row.updated_at,
            created_at=row.created_at,
        )

    def _to_row(self, entity: StatisticsAggregateEntity) -> StatisticsAggregate:
        kwargs: dict[str, object] = {
            "app_platform_id": entity.app_platform_id,
            "geo": entity.geo,
            "date": entity.date,
            "event_type": entity.event_type,
            "event_key": entity.event_key,
            "count": entity.count,
            "amount_usd": entity.amount_usd,
            "updated_at": entity.updated_at,
        }
        if entity.aggregate_id is not None:
            kwargs["aggregate_id"] = entity.aggregate_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return StatisticsAggregate(**kwargs)

    def save(self, entity: StatisticsAggregateEntity) -> StatisticsAggregateEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[StatisticsAggregateEntity]) -> list[StatisticsAggregateEntity]:
        if not entities:
            return []

        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, aggregate_id: int) -> StatisticsAggregateEntity | None:
        row = self.session.get(StatisticsAggregate, aggregate_id)
        return self._to_domain(row) if row is not None else None

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        limit: int = 100,
    ) -> list[StatisticsAggregateEntity]:
        rows = self.session.scalars(
            select(StatisticsAggregate)
            .where(StatisticsAggregate.app_platform_id == app_platform_id)
            .order_by(desc(StatisticsAggregate.date), desc(StatisticsAggregate.aggregate_id))
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCustomParamsStatisticsRepository(CustomParamsStatisticsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CustomParamsStatisticsAggregate) -> CustomParamsStatisticsAggregateEntity:
        return CustomParamsStatisticsAggregateEntity(
            aggregate_id=row.aggregate_id,
            app_platform_id=row.app_platform_id,
            geo=row.geo,
            date=row.date,
            event_type=row.event_type,
            event_key=row.event_key,
            param_key=row.param_key,
            param_value=row.param_value,
            count=row.count,
            amount_usd=row.amount_usd,
            updated_at=row.updated_at,
            created_at=row.created_at,
        )

    def _to_row(self, entity: CustomParamsStatisticsAggregateEntity) -> CustomParamsStatisticsAggregate:
        kwargs: dict[str, object] = {
            "app_platform_id": entity.app_platform_id,
            "geo": entity.geo,
            "date": entity.date,
            "event_type": entity.event_type,
            "event_key": entity.event_key,
            "param_key": entity.param_key,
            "param_value": entity.param_value,
            "count": entity.count,
            "amount_usd": entity.amount_usd,
            "updated_at": entity.updated_at,
        }
        if entity.aggregate_id is not None:
            kwargs["aggregate_id"] = entity.aggregate_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return CustomParamsStatisticsAggregate(**kwargs)

    def save(self, entity: CustomParamsStatisticsAggregateEntity) -> CustomParamsStatisticsAggregateEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(
        self,
        entities: list[CustomParamsStatisticsAggregateEntity],
    ) -> list[CustomParamsStatisticsAggregateEntity]:
        if not entities:
            return []

        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, aggregate_id: int) -> CustomParamsStatisticsAggregateEntity | None:
        row = self.session.get(CustomParamsStatisticsAggregate, aggregate_id)
        return self._to_domain(row) if row is not None else None

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        limit: int = 100,
    ) -> list[CustomParamsStatisticsAggregateEntity]:
        rows = self.session.scalars(
            select(CustomParamsStatisticsAggregate)
            .where(CustomParamsStatisticsAggregate.app_platform_id == app_platform_id)
            .order_by(
                desc(CustomParamsStatisticsAggregate.date),
                desc(CustomParamsStatisticsAggregate.aggregate_id),
            )
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]
