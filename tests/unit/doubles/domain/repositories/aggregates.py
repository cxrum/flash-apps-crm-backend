from __future__ import annotations

from app.domain.custom_params_statistics_aggregate.CustomParamsStatisticsAggregateEntity import (
    CustomParamsStatisticsAggregateEntity,
)
from app.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
from app.domain.statistics_aggregate.StatisticsAggregateEntity import StatisticsAggregateEntity
from app.domain.statistics_aggregate.statistics_aggregate_repository_protocol import StatisticsRepositoryProtocol
from tests.unit.doubles.base import CallRecorderMixin, IntegerSequence, clone, comparable_datetime, evolve, utcnow


class InMemoryStatisticsRepository(CallRecorderMixin, StatisticsRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, StatisticsAggregateEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: StatisticsAggregateEntity) -> StatisticsAggregateEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.aggregate_id) if entity.aggregate_id is not None else None
        now = utcnow()
        changes: dict[str, object] = {}
        if entity.aggregate_id is None:
            changes["aggregate_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.aggregate_id is not None
        self._ids.observe(saved.aggregate_id)
        self._items[saved.aggregate_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[StatisticsAggregateEntity]) -> list[StatisticsAggregateEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, aggregate_id: int) -> StatisticsAggregateEntity | None:
        self._record("get_by_id", aggregate_id)
        item = self._items.get(aggregate_id)
        return clone(item) if item is not None else None

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        limit: int = 100,
    ) -> list[StatisticsAggregateEntity]:
        self._record("list_by_app_platform_id", app_platform_id, limit=limit)
        items = [
            item
            for item in self._items.values()
            if item.app_platform_id == app_platform_id
        ]
        items.sort(
            key=lambda item: (comparable_datetime(item.date), item.aggregate_id or 0),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]


class InMemoryCustomParamsStatisticsRepository(CallRecorderMixin, CustomParamsStatisticsRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CustomParamsStatisticsAggregateEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CustomParamsStatisticsAggregateEntity) -> CustomParamsStatisticsAggregateEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.aggregate_id) if entity.aggregate_id is not None else None
        now = utcnow()
        changes: dict[str, object] = {}
        if entity.aggregate_id is None:
            changes["aggregate_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.aggregate_id is not None
        self._ids.observe(saved.aggregate_id)
        self._items[saved.aggregate_id] = clone(saved)
        return clone(saved)

    def save_many(
        self,
        entities: list[CustomParamsStatisticsAggregateEntity],
    ) -> list[CustomParamsStatisticsAggregateEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, aggregate_id: int) -> CustomParamsStatisticsAggregateEntity | None:
        self._record("get_by_id", aggregate_id)
        item = self._items.get(aggregate_id)
        return clone(item) if item is not None else None

    def list_by_app_platform_id(
        self,
        app_platform_id: int,
        *,
        limit: int = 100,
    ) -> list[CustomParamsStatisticsAggregateEntity]:
        self._record("list_by_app_platform_id", app_platform_id, limit=limit)
        items = [
            item
            for item in self._items.values()
            if item.app_platform_id == app_platform_id
        ]
        items.sort(
            key=lambda item: (comparable_datetime(item.date), item.aggregate_id or 0),
            reverse=True,
        )
        return [clone(item) for item in items[:limit]]
