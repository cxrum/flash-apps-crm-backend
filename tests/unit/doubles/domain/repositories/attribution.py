from __future__ import annotations

from collections.abc import Callable

from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.crm.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.modules.crm.domain.click.CrmClickEntity import CrmClickEntity
from app.modules.crm.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.modules.crm.domain.current_param.current_param_repository_protocol import CrmCurrentParamRepositoryProtocol
from app.modules.crm.domain.events.CrmEventEntity import EventEntity
from app.modules.crm.domain.events.event_repository_protocol import CrmEventRepositoryProtocol
from tests.unit.doubles.base import (
    CallRecorderMixin,
    IntegerSequence,
    clone,
    comparable_datetime,
    evolve,
    utcnow,
)


class InMemoryCrmClickRepository(CallRecorderMixin, CrmClickRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[str, CrmClickEntity] = {}
        self._inner_ids = IntegerSequence()

    def insert(self, entity: CrmClickEntity) -> CrmClickEntity:
        self._record("insert", clone(entity))
        saved = clone(entity)

        if entity.click_id in self._items:
            inner_id = self._inner_ids.next()

        if saved.created_at is None:
            saved = evolve(saved, created_at=utcnow())

        self._items[saved.click_id] = clone(saved)

        return clone(saved)

    def insert_many(self, entities: list[CrmClickEntity]) -> list[CrmClickEntity]:
        self._record("insert_many", clone(entities))
        return [self.insert(entity) for entity in entities]

    def get_by_id(self, click_id: str) -> CrmClickEntity | None:
        self._record("get_by_id", click_id)
        item = self._items.get(click_id)
        return clone(item) if item is not None else None

    def list_by_platform_id(self, app_platform_id: int, *, limit: int = 100) -> list[CrmClickEntity]:
        self._record("list_by_platform_id", app_platform_id, limit=limit)
        items = [item for item in self._items.values() if item.app_platform_id == app_platform_id]
        items.sort(
            key=lambda item: (comparable_datetime(item.created_at), item.click_id),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]


class InMemoryCrmCurrentParamRepository(CallRecorderMixin, CrmCurrentParamRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[tuple[str, str], CrmCurrentParamEntity] = {}

    def save(self, entity: CrmCurrentParamEntity) -> CrmCurrentParamEntity:
        self._record("save", clone(entity))
        key = (entity.click_id, entity.param_key)
        saved = clone(entity)
        if saved.updated_at is None:
            saved = evolve(saved, updated_at=utcnow())
        self._items[key] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmCurrentParamEntity]) -> list[CrmCurrentParamEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def create_or_update_many(self, entities: list[CrmCurrentParamEntity]) -> list[CrmCurrentParamEntity]:
        self._record("create_or_update_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_click_and_key(self, click_id: str, param_key: str) -> CrmCurrentParamEntity | None:
        self._record("get_by_click_and_key", click_id, param_key)
        item = self._items.get((click_id, param_key))
        return clone(item) if item is not None else None

    def list_by_click_id(self, click_id: str) -> list[CrmCurrentParamEntity]:
        self._record("list_by_click_id", click_id)
        items = sorted(
            (item for item in self._items.values() if item.click_id == click_id),
            key=lambda item: item.param_key,
        )
        return [clone(item) for item in items]


class InMemoryCrmEventRepository(CallRecorderMixin, CrmEventRepositoryProtocol):
    def __init__(
        self,
        *,
        click_lookup: Callable[[str], CrmClickEntity | None],
        platform_lookup: Callable[[int], CrmAppPlatformEntity | None],
    ) -> None:
        super().__init__()
        self._items: dict[str, EventEntity] = {}
        self._click_lookup = click_lookup
        self._platform_lookup = platform_lookup

    def insert(self, entity: EventEntity) -> EventEntity:
        self._record("insert", clone(entity))
        if entity.event_id in self._items:
            raise ValueError(f"Event {entity.event_id} already exists")
        saved = clone(entity)
        if saved.created_at is None:
            saved = evolve(saved, created_at=utcnow())
        self._items[saved.event_id] = clone(saved)
        return clone(saved)

    def insert_many(self, entities: list[EventEntity]) -> list[EventEntity]:
        self._record("insert_many", clone(entities))
        inserted: list[EventEntity] = []
        for entity in entities:
            if entity.event_id in self._items:
                continue
            inserted.append(self.insert(entity))
        return inserted

    def get_by_id(self, event_id: str) -> EventEntity | None:
        self._record("get_by_id", event_id)
        item = self._items.get(event_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int, *, limit: int = 100) -> list[EventEntity]:
        self._record("list_by_app_id", app_id, limit=limit)
        items: list[EventEntity] = []
        for event in self._items.values():
            click = self._click_lookup(event.click_id)
            if click is None:
                continue
            platform = self._platform_lookup(click.app_platform_id)
            if platform is None or platform.app_id != app_id:
                continue
            items.append(clone(event))
        items.sort(
            key=lambda item: (comparable_datetime(item.event_time_utc), item.event_id),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]

    def list_by_click_id(self, click_id: str, *, limit: int = 100) -> list[EventEntity]:
        self._record("list_by_click_id", click_id, limit=limit)
        items: list[EventEntity] = []
        for event in self._items.values():
            click = self._click_lookup(event.click_id)
            if click is None:
                continue
            items.append(clone(event))
        items.sort(
            key=lambda item: (comparable_datetime(item.event_time_utc), item.event_id),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]
