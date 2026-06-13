from __future__ import annotations

from app.modules.crm.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.modules.crm.domain.user_app_access.user_app_access_repository_protocol import (
    CrmUserAppAccessRepositoryProtocol,
)
from tests.unit.doubles.base import CallRecorderMixin, clone


class InMemoryCrmUserAppAccessRepository(CallRecorderMixin, CrmUserAppAccessRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[tuple[int, int], CrmUserAppAccessEntity] = {}

    def save(self, entity: CrmUserAppAccessEntity) -> CrmUserAppAccessEntity:
        self._record("save", clone(entity))
        key = (entity.user_id, entity.app_id)
        self._items[key] = clone(entity)
        return clone(entity)

    def save_many(self, entities: list[CrmUserAppAccessEntity]) -> list[CrmUserAppAccessEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_user_and_app(self, user_id: int, app_id: int) -> CrmUserAppAccessEntity | None:
        self._record("get_by_user_and_app", user_id, app_id)
        item = self._items.get((user_id, app_id))
        return clone(item) if item is not None else None

    def list_by_user_id(self, user_id: int) -> list[CrmUserAppAccessEntity]:
        self._record("list_by_user_id", user_id)
        items = sorted(
            (item for item in self._items.values() if item.user_id == user_id),
            key=lambda item: item.app_id,
        )
        return [clone(item) for item in items]

    def list_by_app_id(self, app_id: int) -> list[CrmUserAppAccessEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.user_id,
        )
        return [clone(item) for item in items]
