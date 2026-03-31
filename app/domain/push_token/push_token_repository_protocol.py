from __future__ import annotations

from typing import  Protocol

from app.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.pagination import Pagination


class CrmPushTokenRepositoryProtocol(Protocol):
    def save(self, entity: CrmPushTokenEntity) -> CrmPushTokenEntity: ...
    def save_many(self, entities: list[CrmPushTokenEntity]) -> list[CrmPushTokenEntity]: ...
    def get_by_id(self, token_id: int) -> CrmPushTokenEntity | None: ...
    def delete(self, token_id: int) -> CrmPushTokenEntity: ...
    def get_by_token(self, token: str) -> CrmPushTokenEntity | None: ...
    def list_by_app_user_id(
        self,
        app_user_id: int,
        *,
        pagination: Pagination | None = None,
    ) -> list[CrmPushTokenEntity]: ...
