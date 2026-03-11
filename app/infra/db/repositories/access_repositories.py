from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.user_app_access.user_app_access_repository_protocol import (
    CrmUserAppAccessRepositoryProtocol,
)
from app.infra.db.access.models import CrmUserAppAccess


class SqlAlchemyCrmUserAppAccessRepository(CrmUserAppAccessRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: CrmUserAppAccess) -> CrmUserAppAccessEntity:
        return CrmUserAppAccessEntity(
            user_id=row.user_id,
            app_id=row.app_id,
            access_level=row.access_level,
            assigned_at=row.assigned_at,
        )

    def _to_row(self, entity: CrmUserAppAccessEntity) -> CrmUserAppAccess:
        kwargs: dict[str, object] = {
            "user_id": entity.user_id,
            "app_id": entity.app_id,
            "access_level": entity.access_level,
        }
        if entity.assigned_at is not None:
            kwargs["assigned_at"] = entity.assigned_at
        return CrmUserAppAccess(**kwargs)

    def save(self, entity: CrmUserAppAccessEntity) -> CrmUserAppAccessEntity:
        row = self.session.merge(self._to_row(entity))
        self.session.flush()
        return self._to_domain(row)

    def save_many(self, entities: list[CrmUserAppAccessEntity]) -> list[CrmUserAppAccessEntity]:
        rows = [self.session.merge(self._to_row(entity)) for entity in entities]
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_user_and_app(self, user_id: int, app_id: int) -> CrmUserAppAccessEntity | None:
        row = self.session.get(CrmUserAppAccess, {"user_id": user_id, "app_id": app_id})
        return self._to_domain(row) if row is not None else None

    def list_by_user_id(self, user_id: int) -> list[CrmUserAppAccessEntity]:
        rows = self.session.scalars(
            select(CrmUserAppAccess)
            .where(CrmUserAppAccess.user_id == user_id)
            .order_by(CrmUserAppAccess.app_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_app_id(self, app_id: int) -> list[CrmUserAppAccessEntity]:
        rows = self.session.scalars(
            select(CrmUserAppAccess)
            .where(CrmUserAppAccess.app_id == app_id)
            .order_by(CrmUserAppAccess.user_id.asc())
        ).all()
        return [self._to_domain(row) for row in rows]
