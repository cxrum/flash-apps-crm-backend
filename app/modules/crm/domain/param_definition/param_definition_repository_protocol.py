from __future__ import annotations

from typing import Protocol

from app.modules.crm.domain.pagination import Pagination
from app.modules.crm.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity


class CrmParamDefinitionRepositoryProtocol(Protocol):
    def save(self, entity: CrmParamDefinitionEntity) -> CrmParamDefinitionEntity: ...
    def save_many(self, entities: list[CrmParamDefinitionEntity]) -> list[CrmParamDefinitionEntity]: ...
    def get_by_id(self, param_definition_id: int) -> CrmParamDefinitionEntity | None: ...
    def delete(self, param_definition_id: int) -> CrmParamDefinitionEntity: ...
    def list_by_app_id(
        self,
        app_id: int | None,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmParamDefinitionEntity]: ...
