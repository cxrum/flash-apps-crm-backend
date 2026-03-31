from __future__ import annotations

from typing import Protocol

from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity

from app.domain.pagination import Pagination


class CrmAppPlatformRepositoryProtocol(Protocol):
    def save(self, entity: CrmAppPlatformEntity) -> CrmAppPlatformEntity: ...
    def delete(self, platform_id: int) -> CrmAppPlatformEntity: ...
    def save_many(self, entities: list[CrmAppPlatformEntity]) -> list[CrmAppPlatformEntity]: ...
    def get_by_id(self, platform_id: int) -> CrmAppPlatformEntity | None: ...
    def get_by_install_key(self, install_key: str) -> CrmAppPlatformEntity | None: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmAppPlatformEntity]: ...
    def list_by_platform(
        self,
        platform: str,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmAppPlatformEntity]: ...
