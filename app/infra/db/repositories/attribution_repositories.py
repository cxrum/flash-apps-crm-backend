from __future__ import annotations

from typing import Any, Mapping

from sqlalchemy import desc, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.current_param.current_param_repository_protocol import CrmCurrentParamRepositoryProtocol
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.events.event_repository_protocol import CrmEventRepositoryProtocol
from app.infra.db.apps.models import AppPlatform
from app.infra.db.attribution.models import Click, CurrentParam, Event


class SqlAlchemyCrmClickRepository(CrmClickRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: Click) -> CrmClickEntity:
        return CrmClickEntity(
            click_id=row.click_id,
            app_platform_id=row.app_platform_id,
            status=row.status,
            raw_query=dict(row.raw_query),
            ip_address=row.ip_address,
            user_agent=row.user_agent,
            geo=dict(row.geo),
            referrer=row.referrer,
            source=row.source,
            redirect_target=row.redirect_target,
            normalized_params=dict(row.normalized_params),
            created_at=row.created_at,
        )

    def _to_row(self, entity: CrmClickEntity) -> Click:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "app_platform_id": entity.app_platform_id,
            "status": entity.status,
            "raw_query": dict(entity.raw_query),
            "ip_address": entity.ip_address,
            "user_agent": entity.user_agent,
            "geo": dict(entity.geo),
            "referrer": entity.referrer,
            "source": entity.source,
            "redirect_target": entity.redirect_target,
            "normalized_params": dict(entity.normalized_params),
        }
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return Click(**kwargs)

    def insert(self, entity: CrmClickEntity) -> CrmClickEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[CrmClickEntity]) -> list[CrmClickEntity]:
        rows = [self._to_row(entity) for entity in entities]
        self.session.add_all(rows)
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, click_id: str) -> CrmClickEntity | None:
        row = self.session.get(Click, click_id)
        return self._to_domain(row) if row is not None else None

    def list_by_platform_id(self, app_platform_id: int, *, limit: int = 100) -> list[CrmClickEntity]:
        rows = self.session.scalars(
            select(Click)
            .where(Click.app_platform_id == app_platform_id)
            .order_by(desc(Click.created_at), desc(Click.click_id))
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmCurrentParamRepository(CrmCurrentParamRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CurrentParam) -> CrmCurrentParamEntity:
        return CrmCurrentParamEntity(
            click_id=row.click_id,
            param_key=row.param_key,
            value_string=row.value_string,
            value_number=row.value_number,
            value_bool=row.value_bool,
            value_json=row.value_json,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmCurrentParamEntity) -> CurrentParam:
        kwargs: dict[str, object] = {
            "click_id": entity.click_id,
            "param_key": entity.param_key,
            "value_string": entity.value_string,
            "value_number": entity.value_number,
            "value_bool": entity.value_bool,
            "value_json": entity.value_json,
        }
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return CurrentParam(**kwargs)

    def save(self, entity: CrmCurrentParamEntity) -> CrmCurrentParamEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmCurrentParamEntity]) -> list[CrmCurrentParamEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_click_and_key(self, click_id: str, param_key: str) -> CrmCurrentParamEntity | None:
        row = self.session.get(CurrentParam, {"click_id": click_id, "param_key": param_key})
        return self._to_domain(row) if row is not None else None

    def list_by_click_id(self, click_id: str) -> list[CrmCurrentParamEntity]:
        rows = self.session.scalars(
            select(CurrentParam)
            .where(CurrentParam.click_id == click_id)
            .order_by(CurrentParam.param_key.asc())
        ).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmEventRepository(CrmEventRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: Event) -> EventEntity:
        return EventEntity(
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

    def _mapping_to_domain(self, row: Mapping[str, Any]) -> EventEntity:
        return EventEntity(
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

    def _to_row(self, entity: EventEntity) -> Event:
        kwargs: dict[str, object] = {
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
            kwargs["created_at"] = entity.created_at
        return Event(**kwargs)

    def _to_values(self, entity: EventEntity) -> dict[str, object]:
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

    def insert(self, entity: EventEntity) -> EventEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[EventEntity]) -> list[EventEntity]:
        if not entities:
            return []

        stmt = (
            pg_insert(Event)
            .values([self._to_values(entity) for entity in entities])
            .on_conflict_do_nothing(index_elements=[Event.event_id])
            .returning(
                Event.event_id,
                Event.click_id,
                Event.app_user_id,
                Event.event_type,
                Event.event_key,
                Event.amount,
                Event.currency,
                Event.amount_usd,
                Event.event_time_utc,
                Event.payload,
                Event.created_at,
            )
        )
        rows = self.session.execute(stmt).mappings().all()
        self.session.flush()
        return [self._mapping_to_domain(row.__dict__) for row in rows]

    def get_by_id(self, event_id: str) -> EventEntity | None:
        row = self.session.get(Event, event_id)
        return self._to_domain(row) if row is not None else None

    def list_by_app_id(self, app_id: int, *, limit: int = 100) -> list[EventEntity]:
        rows = self.session.scalars(
            select(Event)
            .join(Click, Event.click_id == Click.click_id)
            .join(AppPlatform, Click.app_platform_id == AppPlatform.platform_id)
            .where(AppPlatform.app_id == app_id)
            .order_by(desc(Event.event_time_utc), desc(Event.event_id))
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_click_id(self, click_id: str, *, limit: int = 100) -> list[EventEntity]:
        rows = self.session.scalars(
            select(Event)
            .where(Event.click_id == click_id)
            .order_by(desc(Event.event_time_utc), desc(Event.event_id))
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]

    