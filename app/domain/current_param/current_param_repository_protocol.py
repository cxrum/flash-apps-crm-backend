from __future__ import annotations

from typing import Protocol

from app.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity

from app.domain.pagination import Pagination


class CrmCurrentParamRepositoryProtocol(Protocol):
    def save(self, entity: CrmCurrentParamEntity) -> CrmCurrentParamEntity: ...
    def save_many(self, entities: list[CrmCurrentParamEntity]) -> list[CrmCurrentParamEntity]: ...
    def create_or_update_many(self, entities: list[CrmCurrentParamEntity]) -> list[CrmCurrentParamEntity]: ...
    def get_by_click_and_key(self, click_id: str, param_key: str) -> CrmCurrentParamEntity | None: ...
    def list_by_click_id(
        self,
        click_id: str,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmCurrentParamEntity]: ...
