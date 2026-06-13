from __future__ import annotations

from typing import Protocol

from app.modules.crm.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.modules.crm.domain.pagination import Pagination


class CrmAuditLogRepositoryProtocol(Protocol):
    def insert(self, entity: CrmAuditLogEntity) -> CrmAuditLogEntity: ...
    def insert_many(self, entities: list[CrmAuditLogEntity]) -> list[CrmAuditLogEntity]: ...
    def get_by_id(self, audit_log_id: int) -> CrmAuditLogEntity | None: ...
    def delete(self, audit_log_id: int) -> CrmAuditLogEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        actor_id: int | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmAuditLogEntity]: ...
    def list_by_user_id(
        self,
        user_id: int,
        *,
        entity_type: str | None = None,
        entity_id: int | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmAuditLogEntity]: ...
