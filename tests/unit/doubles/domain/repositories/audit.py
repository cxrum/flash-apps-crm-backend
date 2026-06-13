from __future__ import annotations

from app.modules.crm.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.modules.crm.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from tests.unit.doubles.base import (
    CallRecorderMixin,
    IntegerSequence,
    clone,
    comparable_datetime,
    evolve,
    utcnow,
)


class InMemoryCrmAuditLogRepository(CallRecorderMixin, CrmAuditLogRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmAuditLogEntity] = {}
        self._ids = IntegerSequence()

    def insert(self, entity: CrmAuditLogEntity) -> CrmAuditLogEntity:
        self._record("insert", clone(entity))
        changes: dict[str, object] = {}
        if entity.audit_log_id is None:
            changes["audit_log_id"] = self._ids.next()
        if entity.changed_at is None:
            changes["changed_at"] = utcnow()
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.audit_log_id is not None
        self._ids.observe(saved.audit_log_id)
        self._items[saved.audit_log_id] = clone(saved)
        return clone(saved)

    def insert_many(self, entities: list[CrmAuditLogEntity]) -> list[CrmAuditLogEntity]:
        self._record("insert_many", clone(entities))
        return [self.insert(entity) for entity in entities]

    def get_by_id(self, audit_log_id: int) -> CrmAuditLogEntity | None:
        self._record("get_by_id", audit_log_id)
        item = self._items.get(audit_log_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int, *, limit: int = 100) -> list[CrmAuditLogEntity]:
        self._record("list_by_app_id", app_id, limit=limit)
        items = [item for item in self._items.values() if item.app_id == app_id]
        items.sort(
            key=lambda item: (comparable_datetime(item.changed_at), item.audit_log_id or 0),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]

    def list_by_user_id(self, user_id: int, *, limit: int = 100) -> list[CrmAuditLogEntity]:
        self._record("list_by_user_id", user_id, limit=limit)
        items = [item for item in self._items.values() if item.user_id == user_id]
        items.sort(
            key=lambda item: (comparable_datetime(item.changed_at), item.audit_log_id or 0),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]
