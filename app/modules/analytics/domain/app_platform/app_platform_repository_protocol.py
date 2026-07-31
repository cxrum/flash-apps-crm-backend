from __future__ import annotations

from typing import Protocol

from app.modules.analytics.domain.app_platform.AnalyticsAppPlatformEntity import AnalyticsAppPlatformEntity
from app.modules.crm.domain.pagination import Pagination


class AnalyticsAppPlatformRepositoryProtocol(Protocol):
    def save(self, entity: AnalyticsAppPlatformEntity) -> AnalyticsAppPlatformEntity: ...
    def save_many(self, entities: list[AnalyticsAppPlatformEntity]) -> list[AnalyticsAppPlatformEntity]: ...
    def delete(self, platform_id: int) -> AnalyticsAppPlatformEntity: ...
    def get_by_id(self, platform_id: int) -> AnalyticsAppPlatformEntity | None: ...
    def get_by_install_key(self, install_key: str) -> AnalyticsAppPlatformEntity | None: ...
    def list_by_app_id(
        self,
        app_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsAppPlatformEntity]: ...
    def list_by_platform(
        self,
        platform: str,
        *,
        pagination: Pagination | None = None,
    ) -> list[AnalyticsAppPlatformEntity]: ...
