from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from typing import Any

from sqlalchemy import RowMapping, desc, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.modules.analytics.domain.click.AnalyticsClickEntity import AnalyticsClickEntity
from app.modules.analytics.domain.click.click_repository_protocol import AnalyticsClickRepositoryProtocol
from app.modules.analytics.domain.events.AnalyticsEventEntity import AnalyticsEventEntity
from app.modules.analytics.domain.events.event_repository_protocol import AnalyticsEventRepositoryProtocol
from app.modules.analytics.domain.install.AnalyticsInstallEntity import AnalyticsInstallEntity
from app.modules.analytics.domain.install.install_repository_protocol import AnalyticsInstallRepositoryProtocol
from app.modules.analytics.infra.db.models import (
    AnalyticsClick,
    AnalyticsCurrentParam,
    AnalyticsCustomParamsStatisticsAggregate,
    AnalyticsEvent,
    AnalyticsInstall,
    AnalyticsStatisticsAggregate,
)
from app.modules.analytics.infra.exception import AnalyticsInfraException
from app.modules.analytics.domain.current_param.AnalyticsCurrentParamEntity import AnalyticsCurrentParamEntity
from app.modules.analytics.domain.current_param.current_param_repository_protocol import AnalyticsCurrentParamRepositoryProtocol
from app.modules.analytics.domain.custom_params_statistics_aggregate.AnalyticsCustomParamsStatisticsAggregateEntity import AnalyticsCustomParamsStatisticsAggregateEntity
from app.modules.analytics.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import AnalyticsCustomParamsStatisticsRepositoryProtocol
from app.modules.crm.domain.pagination import Pagination
from app.modules.analytics.domain.statistics_aggregate.AnalyticsStatisticsAggregateEntity import AnalyticsStatisticsAggregateEntity
from app.modules.analytics.domain.statistics_aggregate.statistics_aggregate_repository_protocol import AnalyticsStatisticsRepositoryProtocol
from app.modules.crm.infra.db.apps.models import AppPlatform


def _apply_pagination(stmt, pagination: Pagination | None):
    if pagination is not None and pagination.offset is not None:
        stmt = stmt.offset(pagination.offset)
    if pagination is not None and pagination.limit is not None:
        stmt = stmt.limit(pagination.limit)
    return stmt


class SqlAlchemyAnalyticsClickRepository(AnalyticsClickRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AnalyticsClick) -> AnalyticsClickEntity:
        return AnalyticsClickEntity(
            click_id=row.click_id,
            app_platform_id=row.app_platform_id,
            status=row.status,
            raw_query=dict(row.raw_query),
            ip_address=row.ip_address,
            user_agent=row.user_agent,
            city=row.city,
            country_code=row.country_code,
            region=row.region,
            language=row.language,
            referrer=row.referrer,
            source=row.source,
            redirect_target=row.redirect_target,
            normalized_params=dict(row.normalized_params),
            created_at=row.created_at,
        )

    def _to_row(self, entity: AnalyticsClickEntity) -> AnalyticsClick:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "app_platform_id": entity.app_platform_id,
            "status": entity.status,
            "raw_query": dict(entity.raw_query),
            "ip_address": entity.ip_address,
            "user_agent": entity.user_agent,
            "city": entity.city,
            "country_code": entity.country_code,
            "region": entity.region,
            "language": entity.language,
            "referrer": entity.referrer,
            "source": entity.source,
            "redirect_target": entity.redirect_target,
            "normalized_params": dict(entity.normalized_params),
        }
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return AnalyticsClick(**kwargs)

    def insert(self, entity: AnalyticsClickEntity) -> AnalyticsClickEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[AnalyticsClickEntity]) -> list[AnalyticsClickEntity]:
        rows = [self._to_row(entity) for entity in entities]
        self.session.add_all(rows)
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, click_id: str) -> AnalyticsClickEntity | None:
        row = self.session.get(AnalyticsClick, click_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, click_id: str) -> AnalyticsClickEntity:
        row = self.session.get(AnalyticsClick, click_id)
        if row is None:
            raise AnalyticsInfraException()

        click = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return click

    def _list_clicks(
        self,
        stmt,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsClickEntity]:
        start_at_value = None if pagination is None else pagination.start_at
        end_at_value = None if pagination is None else pagination.end_at

        if click_id is not None:
            stmt = stmt.where(AnalyticsClick.click_id == click_id)
        if start_at_value is not None:
            stmt = stmt.where(AnalyticsClick.created_at >= start_at_value)
        if end_at_value is not None:
            stmt = stmt.where(AnalyticsClick.created_at <= end_at_value)

        rows = self.session.scalars(
            _apply_pagination(
                stmt.order_by(desc(AnalyticsClick.created_at), desc(AnalyticsClick.click_id)),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsClickEntity]:
        stmt = (
            select(AnalyticsClick)
            .join(AppPlatform, AnalyticsClick.app_platform_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id)
        )
        return self._list_clicks(stmt, click_id=click_id, pagination=pagination)

    def list_by_platform_id(
        self,
        app_platform_id: int,
        *,
        click_id: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsClickEntity]:
        stmt = select(AnalyticsClick).where(AnalyticsClick.app_platform_id == app_platform_id)
        return self._list_clicks(stmt, click_id=click_id, pagination=pagination)


class SqlAlchemyAnalyticsInstallRepository(AnalyticsInstallRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AnalyticsInstall) -> AnalyticsInstallEntity:
        return AnalyticsInstallEntity(
            install_id=row.install_id,
            click_id=row.click_id,
            app_user_id=row.app_user_id,
            app_platform_id=row.app_platform_id,
            device_data=dict(row.device_data),
            installed_at=row.installed_at,
        )

    def _to_row(self, entity: AnalyticsInstallEntity) -> AnalyticsInstall:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "app_user_id": entity.app_user_id,
            "app_platform_id": entity.app_platform_id,
            "device_data": dict(entity.device_data),
        }
        if entity.install_id is not None:
            kwargs["install_id"] = entity.install_id
        if entity.installed_at is not None:
            kwargs["installed_at"] = entity.installed_at
        return AnalyticsInstall(**kwargs)

    def save(self, entity: AnalyticsInstallEntity) -> AnalyticsInstallEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[AnalyticsInstallEntity]) -> list[AnalyticsInstallEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, install_id: int) -> AnalyticsInstallEntity | None:
        row = self.session.get(AnalyticsInstall, install_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, install_id: int) -> AnalyticsInstallEntity:
        row = self.session.get(AnalyticsInstall, install_id)
        if row is None:
            raise AnalyticsInfraException()

        install = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return install

    def get_by_app_user_id(self, app_user_id: int) -> AnalyticsInstallEntity | None:
        row = self.session.scalars(
            select(AnalyticsInstall)
            .where(AnalyticsInstall.app_user_id == app_user_id)
            .order_by(desc(AnalyticsInstall.installed_at), desc(AnalyticsInstall.install_id))
        ).first()
        return self._to_domain(row) if row is not None else None

    def get_by_click_id(self, click_id: str) -> AnalyticsInstallEntity | None:
        row = self.session.scalars(
            select(AnalyticsInstall)
            .where(AnalyticsInstall.click_id == click_id)
            .order_by(desc(AnalyticsInstall.installed_at), desc(AnalyticsInstall.install_id))
        ).first()
        return self._to_domain(row) if row is not None else None


class SqlAlchemyAnalyticsEventRepository(AnalyticsEventRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AnalyticsEvent) -> AnalyticsEventEntity:
        return AnalyticsEventEntity(
            event_id=row.event_id,
            click_id=row.click_id,
            app_user_id=row.app_user_id,
            event_type=row.event_type,
            event_key=row.event_key,
            amount=row.amount,
            currency=row.currency,
            amount_usd=row.amount_usd,
            event_time_utc=row.event_time_utc,
            payload=dict(row.payload),
            created_at=row.created_at,
        )

    def _mapping_to_domain(self, row: Mapping[str, Any]) -> AnalyticsEventEntity:
        return AnalyticsEventEntity(
            event_id=row["event_id"],
            click_id=row["click_id"],
            app_user_id=row["app_user_id"],
            event_type=row["event_type"],
            event_key=row["event_key"],
            amount=row["amount"],
            currency=row["currency"],
            amount_usd=row["amount_usd"],
            event_time_utc=row["event_time_utc"],
            payload=dict(row["payload"]),
            created_at=row["created_at"],
        )

    def _to_row(self, entity: AnalyticsEventEntity) -> AnalyticsEvent:
        return AnalyticsEvent(**self._to_values(entity))

    def _to_values(self, entity: AnalyticsEventEntity) -> dict[str, object]:
        values: dict[str, object] = {
            "event_id": entity.event_id,
            "click_id": entity.click_id,
            "app_user_id": entity.app_user_id,
            "event_type": entity.event_type,
            "event_key": entity.event_key,
            "amount": entity.amount,
            "currency": entity.currency,
            "amount_usd": entity.amount_usd,
            "event_time_utc": entity.event_time_utc,
            "payload": dict(entity.payload),
        }
        if entity.created_at is not None:
            values["created_at"] = entity.created_at
        return values

    def insert(self, entity: AnalyticsEventEntity) -> AnalyticsEventEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[AnalyticsEventEntity]) -> list[AnalyticsEventEntity]:
        if not entities:
            return []

        stmt = (
            pg_insert(AnalyticsEvent)
            .values([self._to_values(entity) for entity in entities])
            .on_conflict_do_nothing(index_elements=[AnalyticsEvent.event_id])
            .returning(
                AnalyticsEvent.event_id,
                AnalyticsEvent.click_id,
                AnalyticsEvent.app_user_id,
                AnalyticsEvent.event_type,
                AnalyticsEvent.event_key,
                AnalyticsEvent.amount,
                AnalyticsEvent.currency,
                AnalyticsEvent.amount_usd,
                AnalyticsEvent.event_time_utc,
                AnalyticsEvent.payload,
                AnalyticsEvent.created_at,
            )
        )
        rows = self.session.execute(stmt).mappings().all()
        self.session.flush()
        return [self._mapping_to_domain(row) for row in rows]

    def get_by_id(self, event_id: str) -> AnalyticsEventEntity | None:
        row = self.session.get(AnalyticsEvent, event_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, event_id: str) -> AnalyticsEventEntity:
        row = self.session.get(AnalyticsEvent, event_id)
        if row is None:
            raise AnalyticsInfraException()

        event = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return event

    def _list_events(
        self,
        stmt,
        *,
        click_id: str | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsEventEntity]:
        start_at_value = None if pagination is None else pagination.start_at
        end_at_value = None if pagination is None else pagination.end_at

        if click_id is not None:
            stmt = stmt.where(AnalyticsEvent.click_id == click_id)
        if event_key is not None:
            stmt = stmt.where(AnalyticsEvent.event_key == event_key)
        if start_at_value is not None:
            stmt = stmt.where(AnalyticsEvent.event_time_utc >= start_at_value)
        if end_at_value is not None:
            stmt = stmt.where(AnalyticsEvent.event_time_utc <= end_at_value)

        rows = self.session.scalars(
            _apply_pagination(
                stmt.order_by(desc(AnalyticsEvent.event_time_utc), desc(AnalyticsEvent.event_id)),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_id(
        self,
        app_id: int,
        *,
        click_id: str | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsEventEntity]:
        stmt = (
            select(AnalyticsEvent)
            .join(AnalyticsClick, AnalyticsEvent.click_id == AnalyticsClick.click_id)
            .join(AppPlatform, AnalyticsClick.app_platform_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id)
        )
        return self._list_events(stmt, click_id=click_id, event_key=event_key, pagination=pagination)

    def list_by_click_id(
        self,
        click_id: str,
        *,
        app_id: int | None = None,
        event_key: str | None = None,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsEventEntity]:
        stmt = select(AnalyticsEvent)
        if app_id is not None:
            stmt = (
                stmt.join(AnalyticsClick, AnalyticsEvent.click_id == AnalyticsClick.click_id)
                .join(AppPlatform, AnalyticsClick.app_platform_id == AppPlatform.platform_id)
                .where(AppPlatform.app_id == app_id)
            )
        return self._list_events(stmt, click_id=click_id, event_key=event_key, pagination=pagination)


class SqlAlchemyAnalyticsCurrentParamRepository(AnalyticsCurrentParamRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AnalyticsCurrentParam) -> AnalyticsCurrentParamEntity:
        return AnalyticsCurrentParamEntity(
            click_id=row.click_id,
            param_key=row.param_key,
            value_string=row.value_string,
            value_number=row.value_number,
            value_bool=row.value_bool,
            value_json=row.value_json,
            updated_at=row.updated_at,
        )

    def _mapping_to_domain(self, row: RowMapping) -> AnalyticsCurrentParamEntity:
        return AnalyticsCurrentParamEntity(
            click_id=row["click_id"],
            param_key=row["param_key"],
            value_string=row["value_string"],
            value_number=row["value_number"],
            value_bool=row["value_bool"],
            value_json=row["value_json"],
            updated_at=row["updated_at"],
        )

    def _to_values(self, entity: AnalyticsCurrentParamEntity) -> dict[str, object]:
        values: dict[str, object] = {
            "click_id": entity.click_id,
            "param_key": entity.param_key,
            "value_string": entity.value_string,
            "value_number": entity.value_number,
            "value_bool": entity.value_bool,
            "value_json": entity.value_json,
        }
        if entity.updated_at is not None:
            values["updated_at"] = entity.updated_at
        return values

    def save(self, entity: AnalyticsCurrentParamEntity) -> AnalyticsCurrentParamEntity:
        rows = self.create_or_update_many([entity])
        return rows[0]

    def save_many(self, entities: list[AnalyticsCurrentParamEntity]) -> list[AnalyticsCurrentParamEntity]:
        return self.create_or_update_many(entities)

    def create_or_update_many(self, entities: list[AnalyticsCurrentParamEntity]) -> list[AnalyticsCurrentParamEntity]:
        if not entities:
            return []

        insert_stmt = pg_insert(AnalyticsCurrentParam)
        stmt = (
            insert_stmt.values([self._to_values(entity) for entity in entities])
            .on_conflict_do_update(
                index_elements=[AnalyticsCurrentParam.click_id, AnalyticsCurrentParam.param_key],
                set_={
                    "value_string": insert_stmt.excluded.value_string,
                    "value_number": insert_stmt.excluded.value_number,
                    "value_bool": insert_stmt.excluded.value_bool,
                    "value_json": insert_stmt.excluded.value_json,
                    "updated_at": insert_stmt.excluded.updated_at,
                },
            )
            .returning(
                AnalyticsCurrentParam.click_id,
                AnalyticsCurrentParam.param_key,
                AnalyticsCurrentParam.value_string,
                AnalyticsCurrentParam.value_number,
                AnalyticsCurrentParam.value_bool,
                AnalyticsCurrentParam.value_json,
                AnalyticsCurrentParam.updated_at,
            )
        )
        rows = self.session.execute(stmt).mappings().all()
        self.session.flush()
        return [self._mapping_to_domain(row) for row in rows]

    def get_by_click_and_key(self, click_id: str, param_key: str) -> AnalyticsCurrentParamEntity | None:
        row = self.session.get(AnalyticsCurrentParam, {"click_id": click_id, "param_key": param_key})
        return self._to_domain(row) if row is not None else None

    def list_by_click_id(
        self,
        click_id: str,
        *,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsCurrentParamEntity]:
        rows = self.session.scalars(
            _apply_pagination(
                select(AnalyticsCurrentParam)
                .where(AnalyticsCurrentParam.click_id == click_id)
                .order_by(AnalyticsCurrentParam.param_key.asc()),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyAnalyticsStatisticsRepository(AnalyticsStatisticsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AnalyticsStatisticsAggregate) -> AnalyticsStatisticsAggregateEntity:
        return AnalyticsStatisticsAggregateEntity(
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

    def _to_row(self, entity: AnalyticsStatisticsAggregateEntity) -> AnalyticsStatisticsAggregate:
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
        return AnalyticsStatisticsAggregate(**kwargs)

    def save(self, entity: AnalyticsStatisticsAggregateEntity) -> AnalyticsStatisticsAggregateEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[AnalyticsStatisticsAggregateEntity]) -> list[AnalyticsStatisticsAggregateEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, aggregate_id: int) -> AnalyticsStatisticsAggregateEntity | None:
        row = self.session.get(AnalyticsStatisticsAggregate, aggregate_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, aggregate_id: int) -> AnalyticsStatisticsAggregateEntity:
        row = self.session.get(AnalyticsStatisticsAggregate, aggregate_id)
        if row is None:
            raise AnalyticsInfraException()
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
    ) -> list[AnalyticsStatisticsAggregateEntity]:
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

        stmt = select(AnalyticsStatisticsAggregate)
        for field_name, value in filter_values.items():
            if value is not None:
                stmt = stmt.where(getattr(AnalyticsStatisticsAggregate, field_name) == value)

        rows = self.session.scalars(
            _apply_pagination(
                stmt.order_by(desc(AnalyticsStatisticsAggregate.date), desc(AnalyticsStatisticsAggregate.aggregate_id)),
                pagination,
            )
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsStatisticsAggregateEntity]:
        return self.list_by_filters(app_platform_id=app_platform_id, pagination=pagination)


class SqlAlchemyAnalyticsCustomParamsStatisticsRepository(AnalyticsCustomParamsStatisticsRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AnalyticsCustomParamsStatisticsAggregate) -> AnalyticsCustomParamsStatisticsAggregateEntity:
        return AnalyticsCustomParamsStatisticsAggregateEntity(
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

    def _to_row(self, entity: AnalyticsCustomParamsStatisticsAggregateEntity) -> AnalyticsCustomParamsStatisticsAggregate:
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
        return AnalyticsCustomParamsStatisticsAggregate(**kwargs)

    def save(self, entity: AnalyticsCustomParamsStatisticsAggregateEntity) -> AnalyticsCustomParamsStatisticsAggregateEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(
        self,
        entities: list[AnalyticsCustomParamsStatisticsAggregateEntity],
    ) -> list[AnalyticsCustomParamsStatisticsAggregateEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, aggregate_id: int) -> AnalyticsCustomParamsStatisticsAggregateEntity | None:
        row = self.session.get(AnalyticsCustomParamsStatisticsAggregate, aggregate_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, aggregate_id: int) -> AnalyticsCustomParamsStatisticsAggregateEntity:
        row = self.session.get(AnalyticsCustomParamsStatisticsAggregate, aggregate_id)
        if row is None:
            raise AnalyticsInfraException()
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
    ) -> list[AnalyticsCustomParamsStatisticsAggregateEntity]:
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

        stmt = select(AnalyticsCustomParamsStatisticsAggregate)
        for field_name, value in filter_values.items():
            if value is not None:
                stmt = stmt.where(getattr(AnalyticsCustomParamsStatisticsAggregate, field_name) == value)

        rows = self.session.scalars(
            _apply_pagination(
                stmt.order_by(
                    desc(AnalyticsCustomParamsStatisticsAggregate.date),
                    desc(AnalyticsCustomParamsStatisticsAggregate.aggregate_id),
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
    ) -> list[AnalyticsCustomParamsStatisticsAggregateEntity]:
        return self.list_by_filters(app_platform_id=app_platform_id, pagination=pagination)
