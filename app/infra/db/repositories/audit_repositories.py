from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.infra.db.audit.models import AuditLog


class SqlAlchemyCrmAuditLogRepository(CrmAuditLogRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _to_domain(self, row: AuditLog) -> CrmAuditLogEntity:
        return CrmAuditLogEntity(
            audit_log_id=row.audit_log_id,
            user_id=row.user_id,
            app_id=row.app_id,
            entity_changed=row.entity_changed,
            entity_id=row.entity_id,
            old_value=row.old_value,
            new_value=row.new_value,
            changed_at=row.changed_at,
        )

    def _to_row(self, entity: CrmAuditLogEntity) -> AuditLog:
        kwargs: dict[str, object] = {
            "user_id": entity.user_id,
            "app_id": entity.app_id,
            "entity_changed": entity.entity_changed,
            "entity_id": entity.entity_id,
            "old_value": entity.old_value,
            "new_value": entity.new_value,
        }
        if entity.audit_log_id is not None:
            kwargs["audit_log_id"] = entity.audit_log_id
        if entity.changed_at is not None:
            kwargs["changed_at"] = entity.changed_at
        return AuditLog(**kwargs)

    def insert(self, entity: CrmAuditLogEntity) -> CrmAuditLogEntity:
        row = self._to_row(entity)
        self.session.add(row)
        self.session.flush()
        return self._to_domain(row)

    def insert_many(self, entities: list[CrmAuditLogEntity]) -> list[CrmAuditLogEntity]:
        rows = [self._to_row(entity) for entity in entities]
        self.session.add_all(rows)
        self.session.flush()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, audit_log_id: int) -> CrmAuditLogEntity | None:
        row = self.session.get(AuditLog, audit_log_id)
        return self._to_domain(row) if row is not None else None

    def list_by_app_id(self, app_id: int, *, limit: int = 100) -> list[CrmAuditLogEntity]:
        rows = self.session.scalars(
            select(AuditLog)
            .where(AuditLog.app_id == app_id)
            .order_by(desc(AuditLog.changed_at), desc(AuditLog.audit_log_id))
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_by_user_id(self, user_id: int, *, limit: int = 100) -> list[CrmAuditLogEntity]:
        rows = self.session.scalars(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.changed_at), desc(AuditLog.audit_log_id))
            .limit(limit)
        ).all()
        return [self._to_domain(row) for row in rows]
