from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from app.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.pagination import Pagination


class CrmPostbackRuleRepositoryProtocol(Protocol):
    def save(self, entity: CrmPostbackRuleEntity) -> CrmPostbackRuleEntity: ...
    def save_many(self, entities: list[CrmPostbackRuleEntity]) -> list[CrmPostbackRuleEntity]: ...
    def get_by_id(self, rule_id: int) -> CrmPostbackRuleEntity | None: ...
    def delete(self, rule_id: int) -> CrmPostbackRuleEntity: ...
    def list_by_filters(
        self,
        *,
        rule_id: int | None = None,
        platform_app_id: int | None = None,
        name: str | None = None,
        endpoint_url: str | None = None,
        trigger_type: str | None = None,
        http_method: str | None = None,
        headers: dict[str, Any] | None = None,
        auth_params: dict[str, str] | None = None,
        timeout: int | None = None,
        event_key: str | None = None,
        template: dict[str, Any] | None = None,
        retry_policy: dict[str, Any] | None = None,
        is_active: bool | None = None,
        updated_at: datetime | None = None,
        created_at: datetime | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmPostbackRuleEntity]: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPostbackRuleEntity]: ...
    def list_active_by_app(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPostbackRuleEntity]: ...
