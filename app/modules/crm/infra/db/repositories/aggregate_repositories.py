from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.modules.crm.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import (
    CustomParamsStatisticsAggregateEntity,
)
from app.modules.crm.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
from app.modules.crm.domain.pagination import Pagination
from app.modules.crm.domain.statistics_aggregate.statistics_aggregate_repository_protocol import (
    StatisticsRepositoryProtocol,
)
from app.modules.crm.domain.statistics_aggregate.StatisticsAggregateEntity import StatisticsAggregateEntity
from app.modules.crm.infra.db.aggregates.models import CustomParamsStatisticsAggregate, StatisticsAggregate
from app.modules.crm.infra.exception import BaseInfraException


def _apply_pagination(stmt, pagination: Pagination | None):
    if pagination is not None and pagination.offset is not None:
        stmt = stmt.offset(pagination.offset)
    if pagination is not None and pagination.limit is not None:
        stmt = stmt.limit(pagination.limit)
    return stmt


class SqlAlchemyStatisticsRepository(StatisticsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: StatisticsAggregate) -> StatisticsAggregateEntity:
        return StatisticsAggregateEntity(
            aggregate_id=row.aggregate_id,
            app_platform_id=row.app_platform_id,
            geo=row.geo,
            ddate=row.date,
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
            "date": entity.ddate,
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

    def delete(self, aggregate_id: int) -> StatisticsAggregateEntity:
        row = self.session.get(StatisticsAggregate, aggregate_id)
        if row is None:
            raise BaseInfraException()

        aggregate = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return aggregate

    def list_by_filters(
        self,
        *,
        aggregate_id: int | None = None,
        app_platform_id: int | None = None,
        geo: str | None = None,
        ddate: date | None = None,
        event_type: str | None = None,
        event_key: str | None = None,
        count: int | None = None,
        amount_usd: float | None = None,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
        pagination: Pagination | None = None,
    ) -> list[StatisticsAggregateEntity]:
        filter_values = {
            "aggregate_id": aggregate_id,
            "app_platform_id": app_platform_id,
            "geo": geo,
            "date": ddate,
            "event_type": event_type,
            "event_key": event_key,
            "count": count,
            "amount_usd": amount_usd,
            "updated_at": updated_at,
            "created_at": created_at,
        }

        stmt = select(StatisticsAggregate)
        for field_name, value in filter_values.items():
            if value is not None:
                stmt = stmt.where(getattr(StatisticsAggregate, field_name) == value)

        rows = self.session.scalars(
            _apply_pagination(
                stmt.order_by(desc(StatisticsAggregate.date), desc(StatisticsAggregate.aggregate_id)),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[StatisticsAggregateEntity]:
        return self.list_by_filters(app_platform_id=app_platform_id, pagination=pagination)


class SqlAlchemyCustomParamsStatisticsRepository(CustomParamsStatisticsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CustomParamsStatisticsAggregate) -> CustomParamsStatisticsAggregateEntity:
        return CustomParamsStatisticsAggregateEntity(
            aggregate_id=row.aggregate_id,
            app_platform_id=row.app_platform_id,
            geo=row.geo,
            ddate=row.date,
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
            "date": entity.ddate,
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

    def delete(self, aggregate_id: int) -> CustomParamsStatisticsAggregateEntity:
        row = self.session.get(CustomParamsStatisticsAggregate, aggregate_id)
        if row is None:
            raise BaseInfraException()

        aggregate = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return aggregate

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
    ) -> list[CustomParamsStatisticsAggregateEntity]:
        filter_values = {
            "aggregate_id": aggregate_id,
            "app_platform_id": app_platform_id,
            "geo": geo,
            "date": ddate,
            "event_type": event_type,
            "event_key": event_key,
            "param_key": param_key,
            "param_value": param_value,
            "count": count,
            "amount_usd": amount_usd,
            "updated_at": updated_at,
            "created_at": created_at,
        }

        stmt = select(CustomParamsStatisticsAggregate)
        for field_name, value in filter_values.items():
            if value is not None:
                stmt = stmt.where(getattr(CustomParamsStatisticsAggregate, field_name) == value)

        rows = self.session.scalars(
            _apply_pagination(
                stmt.order_by(
                    desc(CustomParamsStatisticsAggregate.date),
                    desc(CustomParamsStatisticsAggregate.aggregate_id),
                ),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CustomParamsStatisticsAggregateEntity]:
        return self.list_by_filters(app_platform_id=app_platform_id, pagination=pagination)
