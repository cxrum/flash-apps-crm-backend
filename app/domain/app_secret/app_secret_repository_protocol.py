from __future__ import annotations

from typing import Protocol

from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity

from app.domain.pagination import Pagination


class CrmAppSecretRepositoryProtocol(Protocol):
    def save(self, entity: CrmAppSecretEntity) -> CrmAppSecretEntity: ...
    def save_many(self, entities: list[CrmAppSecretEntity]) -> list[CrmAppSecretEntity]: ...
    def get_by_id(self, secret_id: int) -> CrmAppSecretEntity | None: ...
    def delete(self, secret_id: int) -> CrmAppSecretEntity: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        platform_id: int | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmAppSecretEntity]: ...
    def list_active_by_app(
        self,
        app_id: int,
        *,
        platform_id: int | None = None,
        pagination: Pagination | None = None,
    ) -> list[CrmAppSecretEntity]: ...
