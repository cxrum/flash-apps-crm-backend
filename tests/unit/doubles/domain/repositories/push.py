from __future__ import annotations

from collections.abc import Callable

from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.push_campaign.push_campaign_repository_protocol import CrmPushCampaignRepositoryProtocol
from app.domain.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.push_event.push_event_repository_protocol import CrmPushEventRepositoryProtocol
from app.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.push_token.push_token_repository_protocol import CrmPushTokenRepositoryProtocol
from tests.unit.doubles.base import (
    CallRecorderMixin,
    IntegerSequence,
    clone,
    comparable_datetime,
    evolve,
    utcnow,
)


class InMemoryCrmPushCampaignRepository(CallRecorderMixin, CrmPushCampaignRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmPushCampaignEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmPushCampaignEntity) -> CrmPushCampaignEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.campaign_id) if entity.campaign_id is not None else None
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.campaign_id is None:
            changes["campaign_id"] = existing.campaign_id
        elif entity.campaign_id is None:
            changes["campaign_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.campaign_id is not None
        self._ids.observe(saved.campaign_id)
        self._items[saved.campaign_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmPushCampaignEntity]) -> list[CrmPushCampaignEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, campaign_id: int) -> CrmPushCampaignEntity | None:
        self._record("get_by_id", campaign_id)
        item = self._items.get(campaign_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int) -> list[CrmPushCampaignEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.campaign_id or 0,
        )
        return [clone(item) for item in items]


class InMemoryCrmPushTokenRepository(CallRecorderMixin, CrmPushTokenRepositoryProtocol):
    def __init__(
        self,
        *,
        install_lookup: Callable[[int], CrmInstallEntity | None],
    ) -> None:
        super().__init__()
        self._items: dict[int, CrmPushTokenEntity] = {}
        self._ids = IntegerSequence()
        self._install_lookup = install_lookup

    def save(self, entity: CrmPushTokenEntity) -> CrmPushTokenEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.token_id) if entity.token_id is not None else None
        if existing is None:
            existing = next((item for item in self._items.values() if item.token == entity.token), None)
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.token_id is None:
            changes["token_id"] = existing.token_id
        elif entity.token_id is None:
            changes["token_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.last_seen_at is None:
            changes["last_seen_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.token_id is not None
        self._ids.observe(saved.token_id)
        self._items[saved.token_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmPushTokenEntity]) -> list[CrmPushTokenEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, token_id: int) -> CrmPushTokenEntity | None:
        self._record("get_by_id", token_id)
        item = self._items.get(token_id)
        return clone(item) if item is not None else None

    def get_by_token(self, token: str) -> CrmPushTokenEntity | None:
        self._record("get_by_token", token)
        item = next((entity for entity in self._items.values() if entity.token == token), None)
        return clone(item) if item is not None else None

    def list_by_app_user_id(self, app_user_id: int) -> list[CrmPushTokenEntity]:
        self._record("list_by_app_user_id", app_user_id)
        items = []
        for item in self._items.values():
            install = self._install_lookup(item.install_id)
            if install is None or install.app_user_id != app_user_id:
                continue
            items.append(clone(item))
        items.sort(key=lambda item: item.token_id or 0)
        return [clone(item) for item in items]


class InMemoryCrmPushEventRepository(CallRecorderMixin, CrmPushEventRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmPushEventEntity] = {}
        self._ids = IntegerSequence()

    def insert(self, entity: CrmPushEventEntity) -> CrmPushEventEntity:
        self._record("insert", clone(entity))
        now = utcnow()
        changes: dict[str, object] = {}
        if entity.push_event_id is None:
            changes["push_event_id"] = self._ids.next()
        if entity.created_at is None:
            changes["created_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.push_event_id is not None
        self._ids.observe(saved.push_event_id)
        self._items[saved.push_event_id] = clone(saved)
        return clone(saved)

    def insert_many(self, entities: list[CrmPushEventEntity]) -> list[CrmPushEventEntity]:
        self._record("insert_many", clone(entities))
        return [self.insert(entity) for entity in entities]

    def get_by_id(self, push_event_id: int) -> CrmPushEventEntity | None:
        self._record("get_by_id", push_event_id)
        item = self._items.get(push_event_id)
        return clone(item) if item is not None else None

    def list_by_campaign_id(self, campaign_id: int) -> list[CrmPushEventEntity]:
        self._record("list_by_campaign_id", campaign_id)
        items = [item for item in self._items.values() if item.campaign_id == campaign_id]
        items.sort(
            key=lambda item: (comparable_datetime(item.event_time_utc), item.push_event_id or 0),
            reverse=True,
        )
        return [clone(item) for item in items]
