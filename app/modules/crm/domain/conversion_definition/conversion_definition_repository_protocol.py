from __future__ import annotations

from typing import Protocol

from app.modules.crm.domain.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.modules.crm.domain.pagination import Pagination


class CrmConversionDefinitionRepositoryProtocol(Protocol):
    def save(self, entity: CrmConversionDefinitionEntity) -> CrmConversionDefinitionEntity: ...
    def save_many(self, entities: list[CrmConversionDefinitionEntity]) -> list[CrmConversionDefinitionEntity]: ...
    def get_by_id(self, conversion_definition_id: int) -> CrmConversionDefinitionEntity | None: ...
    def delete(self, conversion_definition_id: int) -> CrmConversionDefinitionEntity: ...
    def list_by_app_id(
        self,
        app_id: int | None,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmConversionDefinitionEntity]: ...
