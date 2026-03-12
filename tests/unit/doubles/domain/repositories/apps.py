from __future__ import annotations

from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.domain.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.install.install_repository_protocol import CrmInstallRepositoryProtocol
from tests.unit.doubles.base import (
    CallRecorderMixin,
    IntegerSequence,
    clone,
    comparable_datetime,
    evolve,
    utcnow,
)


class InMemoryCrmAppRepository(CallRecorderMixin, CrmAppRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmAppEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmAppEntity) -> CrmAppEntity:
        self._record("save", clone(entity))
        existing = None
        if entity.app_id is not None:
            existing = self._items.get(entity.app_id)
        if existing is None:
            existing = next((item for item in self._items.values() if item.code_slug == entity.code_slug), None)

        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.app_id is None:
            changes["app_id"] = existing.app_id
        elif entity.app_id is None:
            changes["app_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now

        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.app_id is not None
        self._ids.observe(saved.app_id)
        self._items[saved.app_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmAppEntity]) -> list[CrmAppEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, app_id: int) -> CrmAppEntity | None:
        self._record("get_by_id", app_id)
        item = self._items.get(app_id)
        return clone(item) if item is not None else None

    def get_by_slug(self, code_slug: str) -> CrmAppEntity | None:
        self._record("get_by_slug", code_slug)
        item = next((entity for entity in self._items.values() if entity.code_slug == code_slug), None)
        return clone(item) if item is not None else None

    def list_all(self) -> list[CrmAppEntity]:
        self._record("list_all")
        return [clone(entity) for entity in sorted(self._items.values(), key=lambda item: item.app_id or 0)]


class InMemoryCrmAppPlatformRepository(CallRecorderMixin, CrmAppPlatformRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmAppPlatformEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmAppPlatformEntity) -> CrmAppPlatformEntity:
        self._record("save", clone(entity))
        existing = None
        if entity.platform_id is not None:
            existing = self._items.get(entity.platform_id)
        if existing is None:
            existing = next(
                (
                    item
                    for item in self._items.values()
                    if item.app_id == entity.app_id and item.platform == entity.platform
                ),
                None,
            )

        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.platform_id is None:
            changes["platform_id"] = existing.platform_id
        elif entity.platform_id is None:
            changes["platform_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now

        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.platform_id is not None
        self._ids.observe(saved.platform_id)
        self._items[saved.platform_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmAppPlatformEntity]) -> list[CrmAppPlatformEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, platform_id: int) -> CrmAppPlatformEntity | None:
        self._record("get_by_id", platform_id)
        item = self._items.get(platform_id)
        return clone(item) if item is not None else None

    def get_by_install_key(self, install_key: str) -> CrmAppPlatformEntity | None:
        self._record("get_by_install_key", install_key)
        item = next(
            (entity for entity in self._items.values() if entity.install_key == install_key),
            None,
        )
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int) -> list[CrmAppPlatformEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.platform_id or 0,
        )
        return [clone(item) for item in items]

    def list_by_platform(self, platform: str) -> list[CrmAppPlatformEntity]:
        self._record("list_by_platform", platform)
        items = sorted(
            (item for item in self._items.values() if item.platform == platform),
            key=lambda item: item.platform_id or 0,
        )
        return [clone(item) for item in items]


class InMemoryCrmAppUserRepository(CallRecorderMixin, CrmAppUserRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmAppUserEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmAppUserEntity) -> CrmAppUserEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.app_user_id) if entity.app_user_id is not None else None
        changes: dict[str, object] = {}
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = utcnow()
        if entity.app_user_id is None:
            changes["app_user_id"] = self._ids.next()

        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.app_user_id is not None
        self._ids.observe(saved.app_user_id)
        self._items[saved.app_user_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmAppUserEntity]) -> list[CrmAppUserEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, app_user_id: int) -> CrmAppUserEntity | None:
        self._record("get_by_id", app_user_id)
        item = self._items.get(app_user_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int) -> list[CrmAppUserEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.app_user_id or 0,
        )
        return [clone(item) for item in items]


class InMemoryCrmInstallRepository(CallRecorderMixin, CrmInstallRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmInstallEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmInstallEntity) -> CrmInstallEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.install_id) if entity.install_id is not None else None
        if existing is None and entity.app_user_id is not None:
            existing = next(
                (
                    item
                    for item in self._items.values()
                    if item.app_user_id == entity.app_user_id and item.app_platform_id == entity.app_platform_id
                ),
                None,
            )

        changes: dict[str, object] = {}
        if existing is not None and entity.install_id is None:
            changes["install_id"] = existing.install_id
        elif entity.install_id is None:
            changes["install_id"] = self._ids.next()
        if existing is not None and entity.installed_at is None:
            changes["installed_at"] = existing.installed_at
        elif entity.installed_at is None:
            changes["installed_at"] = utcnow()

        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.install_id is not None
        self._ids.observe(saved.install_id)
        self._items[saved.install_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmInstallEntity]) -> list[CrmInstallEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, install_id: int) -> CrmInstallEntity | None:
        self._record("get_by_id", install_id)
        item = self._items.get(install_id)
        return clone(item) if item is not None else None

    def get_by_app_user_id(self, app_user_id: int) -> CrmInstallEntity | None:
        self._record("get_by_app_user_id", app_user_id)
        items = [item for item in self._items.values() if item.app_user_id == app_user_id]
        if not items:
            return None
        latest = max(
            items,
            key=lambda item: (comparable_datetime(item.installed_at), item.install_id or 0),
        )
        return clone(latest)

    def get_by_click_id(self, click_id: str) -> CrmInstallEntity | None:
        self._record("get_by_click_id", click_id)
        items = [item for item in self._items.values() if item.click_id == click_id]
        if not items:
            return None
        latest = max(
            items,
            key=lambda item: (comparable_datetime(item.installed_at), item.install_id or 0),
        )
        return clone(latest)
