from __future__ import annotations

from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.permission.permission_repository_protocol import CrmPermissionRepositoryProtocol
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.domain.role_permission.CrmRolePermissionEntity import CrmRolePermissionEntity
from app.domain.role_permission.role_permission_repository_protocol import (
    CrmRolePermissionRepositoryProtocol,
)
from app.domain.user.CrmUserEntity import CrmUserEntity
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_role.CrmUserRoleEntity import CrmUserRoleEntity
from app.domain.user_role.user_role_repository_protocol import CrmUserRoleRepositoryProtocol
from tests.unit.doubles.base import CallRecorderMixin, IntegerSequence, clone, evolve, utcnow


class InMemoryCrmUserRepository(CallRecorderMixin, CrmUserRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmUserEntity] = {}
        self._ids = IntegerSequence()

    def insert(self, entity: CrmUserEntity) -> CrmUserEntity:
        self._record("insert", clone(entity))
        if any(item.email == entity.email for item in self._items.values()):
            raise ValueError(f"User with email {entity.email} already exists")
        now = utcnow()
        changes: dict[str, object] = {}
        if entity.user_id is None:
            changes["user_id"] = self._ids.next()
        if entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.user_id is not None
        self._ids.observe(saved.user_id)
        self._items[saved.user_id] = clone(saved)
        return clone(saved)

    def insert_many(self, entities: list[CrmUserEntity]) -> list[CrmUserEntity]:
        self._record("insert_many", clone(entities))
        return [self.insert(entity) for entity in entities]

    def get_by_id(self, user_id: int) -> CrmUserEntity | None:
        self._record("get_by_id", user_id)
        item = self._items.get(user_id)
        return clone(item) if item is not None else None

    def get_by_email(self, email: str) -> CrmUserEntity | None:
        self._record("get_by_email", email)
        item = next((entity for entity in self._items.values() if entity.email == email), None)
        return clone(item) if item is not None else None

    def list_all(self) -> list[CrmUserEntity]:
        self._record("list_all")
        return [clone(item) for item in sorted(self._items.values(), key=lambda item: item.user_id or 0)]


class InMemoryCrmRoleRepository(CallRecorderMixin, CrmRoleRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmRoleEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmRoleEntity) -> CrmRoleEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.role_id) if entity.role_id is not None else None
        if existing is None:
            existing = next((item for item in self._items.values() if item.code == entity.code), None)
        changes: dict[str, object] = {}
        if existing is not None and entity.role_id is None:
            changes["role_id"] = existing.role_id
        elif entity.role_id is None:
            changes["role_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = utcnow()
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.role_id is not None
        self._ids.observe(saved.role_id)
        self._items[saved.role_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmRoleEntity]) -> list[CrmRoleEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, role_id: int) -> CrmRoleEntity | None:
        self._record("get_by_id", role_id)
        item = self._items.get(role_id)
        return clone(item) if item is not None else None

    def get_by_code(self, code: str) -> CrmRoleEntity | None:
        self._record("get_by_code", code)
        item = next((entity for entity in self._items.values() if entity.code == code), None)
        return clone(item) if item is not None else None

    def list_all(self) -> list[CrmRoleEntity]:
        self._record("list_all")
        return [clone(item) for item in sorted(self._items.values(), key=lambda item: item.role_id or 0)]


class InMemoryCrmPermissionRepository(CallRecorderMixin, CrmPermissionRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmPermissionEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmPermissionEntity) -> CrmPermissionEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.permission_id) if entity.permission_id is not None else None
        if existing is None:
            existing = next((item for item in self._items.values() if item.code == entity.code), None)
        changes: dict[str, object] = {}
        if existing is not None and entity.permission_id is None:
            changes["permission_id"] = existing.permission_id
        elif entity.permission_id is None:
            changes["permission_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = utcnow()
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.permission_id is not None
        self._ids.observe(saved.permission_id)
        self._items[saved.permission_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmPermissionEntity]) -> list[CrmPermissionEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, permission_id: int) -> CrmPermissionEntity | None:
        self._record("get_by_id", permission_id)
        item = self._items.get(permission_id)
        return clone(item) if item is not None else None

    def get_by_code(self, code: str) -> CrmPermissionEntity | None:
        self._record("get_by_code", code)
        item = next((entity for entity in self._items.values() if entity.code == code), None)
        return clone(item) if item is not None else None

    def list_all(self) -> list[CrmPermissionEntity]:
        self._record("list_all")
        return [clone(item) for item in sorted(self._items.values(), key=lambda item: item.permission_id or 0)]


class InMemoryCrmRolePermissionRepository(CallRecorderMixin, CrmRolePermissionRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[tuple[int, int], CrmRolePermissionEntity] = {}

    def save(self, entity: CrmRolePermissionEntity) -> CrmRolePermissionEntity:
        self._record("save", clone(entity))
        self._items[(entity.role_id, entity.permission_id)] = clone(entity)
        return clone(entity)

    def save_many(self, entities: list[CrmRolePermissionEntity]) -> list[CrmRolePermissionEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def list_by_role_id(self, role_id: int) -> list[CrmRolePermissionEntity]:
        self._record("list_by_role_id", role_id)
        items = sorted(
            (item for item in self._items.values() if item.role_id == role_id),
            key=lambda item: item.permission_id,
        )
        return [clone(item) for item in items]

    def list_by_permission_id(self, permission_id: int) -> list[CrmRolePermissionEntity]:
        self._record("list_by_permission_id", permission_id)
        items = sorted(
            (item for item in self._items.values() if item.permission_id == permission_id),
            key=lambda item: item.role_id,
        )
        return [clone(item) for item in items]


class InMemoryCrmUserRoleRepository(CallRecorderMixin, CrmUserRoleRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[tuple[int, int], CrmUserRoleEntity] = {}

    def save(self, entity: CrmUserRoleEntity) -> CrmUserRoleEntity:
        self._record("save", clone(entity))
        self._items[(entity.user_id, entity.role_id)] = clone(entity)
        return clone(entity)

    def save_many(self, entities: list[CrmUserRoleEntity]) -> list[CrmUserRoleEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def list_by_user_id(self, user_id: int) -> list[CrmUserRoleEntity]:
        self._record("list_by_user_id", user_id)
        items = sorted(
            (item for item in self._items.values() if item.user_id == user_id),
            key=lambda item: item.role_id,
        )
        return [clone(item) for item in items]

    def list_by_role_id(self, role_id: int) -> list[CrmUserRoleEntity]:
        self._record("list_by_role_id", role_id)
        items = sorted(
            (item for item in self._items.values() if item.role_id == role_id),
            key=lambda item: item.user_id,
        )
        return [clone(item) for item in items]
