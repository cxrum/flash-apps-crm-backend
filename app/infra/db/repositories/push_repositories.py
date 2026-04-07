from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.domain.pagination import Pagination
from app.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.push_campaign.push_campaign_repository_protocol import CrmPushCampaignRepositoryProtocol
from app.domain.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.push_event.push_event_repository_protocol import CrmPushEventRepositoryProtocol
from app.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.push_token.push_token_repository_protocol import CrmPushTokenRepositoryProtocol
from app.infra.db.apps.models import Install
from app.infra.db.push.models import PushCampaign, PushEvent, PushToken
from app.infra.exception import BaseInfraException


def _apply_pagination(stmt, pagination: Pagination | None):
    if pagination is not None and pagination.offset is not None:
        stmt = stmt.offset(pagination.offset)
    if pagination is not None and pagination.limit is not None:
        stmt = stmt.limit(pagination.limit)
    return stmt


class SqlAlchemyCrmPushCampaignRepository(CrmPushCampaignRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: PushCampaign) -> CrmPushCampaignEntity:
        return CrmPushCampaignEntity(
            campaign_id=row.campaign_id,
            app_id=row.app_id,
            title=row.title,
            body=row.body,
            image_url=row.image_url,
            target_link=row.target_link,
            geo_filter=dict(row.geo_filter),
            scheduled_at=row.scheduled_at,
            status=row.status,
            created_by_user_id=row.created_by_user_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def _to_row(self, entity: CrmPushCampaignEntity) -> PushCampaign:
        kwargs: dict[str, object] = {
            "app_id": entity.app_id,
            "title": entity.title,
            "body": entity.body,
            "image_url": entity.image_url,
            "target_link": entity.target_link,
            "geo_filter": dict(entity.geo_filter),
            "scheduled_at": entity.scheduled_at,
            "status": entity.status,
            "created_by_user_id": entity.created_by_user_id,
        }
        if entity.campaign_id is not None:
            kwargs["campaign_id"] = entity.campaign_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        if entity.updated_at is not None:
            kwargs["updated_at"] = entity.updated_at
        return PushCampaign(**kwargs)

    def save(self, entity: CrmPushCampaignEntity) -> CrmPushCampaignEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmPushCampaignEntity]) -> list[CrmPushCampaignEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, campaign_id: int) -> CrmPushCampaignEntity | None:
        row = self.session.get(PushCampaign, campaign_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, campaign_id: int) -> CrmPushCampaignEntity:
        row = self.session.get(PushCampaign, campaign_id)
        if row is None:
            raise BaseInfraException()

        campaign = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return campaign

    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPushCampaignEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(PushCampaign)
            .where(PushCampaign.app_id == app_id)
            .order_by(PushCampaign.campaign_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmPushTokenRepository(CrmPushTokenRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: PushToken) -> CrmPushTokenEntity:
        return CrmPushTokenEntity(
            token_id=row.token_id,
            install_id=row.install_id,
            push_token=row.push_token,
            country_code = row.country_code,
            lang = row.lang,
            geo = row.geo,
            is_active=row.is_active,
            last_seen_at=row.last_seen_at,
            created_at=row.created_at,
            app_user_id=row.app_user_id,
            click_id=row.click_id
        )

    def _to_row(self, entity: CrmPushTokenEntity) -> PushToken:
        kwargs: dict[str, object] = {
            "install_id": entity.install_id,
            "token": entity.push_token,
            "geo": entity.geo,
            "country_code": entity.country_code,
            "lang": entity.lang,
            "is_active": entity.is_active,
            "last_seen_at": entity.last_seen_at,
        }
        if entity.token_id is not None:
            kwargs["token_id"] = entity.token_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return PushToken(**kwargs)

    def save(self, entity: CrmPushTokenEntity) -> CrmPushTokenEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmPushTokenEntity]) -> list[CrmPushTokenEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, token_id: int) -> CrmPushTokenEntity | None:
        row = self.session.get(PushToken, token_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, token_id: int) -> CrmPushTokenEntity:
        row = self.session.get(PushToken, token_id)
        if row is None:
            raise BaseInfraException()

        token = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return token

    def get_by_token(self, token: str) -> CrmPushTokenEntity | None:
        row = self.session.scalars(
            select(PushToken).where(PushToken.push_token == token)
        ).first()
        return self._to_domain(row) if row is not None else None

    def list_by_app_user_id(
        self,
        app_user_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPushTokenEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(PushToken)
            .join(Install, PushToken.install_id == Install.install_id)
            .where(Install.app_user_id == app_user_id)
            .order_by(PushToken.token_id.asc()),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]


class SqlAlchemyCrmPushEventRepository(CrmPushEventRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: PushEvent) -> CrmPushEventEntity:
        return CrmPushEventEntity(
            push_event_id=row.push_event_id,
            campaign_id=row.campaign_id,
            token_id=row.token_id,
            event_type=row.event_type,
            event_time_utc=row.event_time_utc,
            payload=dict(row.payload),
            created_at=row.created_at,
        )

    def _to_row(self, entity: CrmPushEventEntity) -> PushEvent:
        kwargs: dict[str, object] = {
            "campaign_id": entity.campaign_id,
            "token_id": entity.token_id,
            "event_type": entity.event_type,
            "event_time_utc": entity.event_time_utc,
            "payload": dict(entity.payload),
        }
        if entity.push_event_id is not None:
            kwargs["push_event_id"] = entity.push_event_id
        if entity.created_at is not None:
            kwargs["created_at"] = entity.created_at
        return PushEvent(**kwargs)

    def insert(self, entity: CrmPushEventEntity) -> CrmPushEventEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[CrmPushEventEntity]) -> list[CrmPushEventEntity]:
        rows = [self._to_row(entity) for entity in entities]
        self.session.add_all(rows)
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, push_event_id: int) -> CrmPushEventEntity | None:
        row = self.session.get(PushEvent, push_event_id)
        return self._to_domain(row) if row is not None else None

    def delete(self, push_event_id: int) -> CrmPushEventEntity:
        row = self.session.get(PushEvent, push_event_id)
        if row is None:
            raise BaseInfraException()

        push_event = self._to_domain(row)
        self.session.delete(row)
        self.session.flush()
        return push_event

    def list_by_campaign_id(
        self,
        campaign_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPushEventEntity]:
        rows = self.session.scalars(_apply_pagination(
            select(PushEvent)
            .where(PushEvent.campaign_id == campaign_id)
            .order_by(desc(PushEvent.event_time_utc), desc(PushEvent.push_event_id)),
            pagination,
        )).all()
        return [self._to_domain(row) for row in rows]
