from __future__ import annotations

from collections.abc import Callable

from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)
from app.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.metric_definition.metric_definition_repository_protocol import (
    CrmMetricDefinitionRepositoryProtocol,
)
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.param_definition.param_definition_repository_protocol import (
    CrmParamDefinitionRepositoryProtocol,
)
from app.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.postback_rule.postback_rule_repository_protocol import CrmPostbackRuleRepositoryProtocol
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.secret_template.secret_template_repository_protocol import (
    CrmSecretTemplateRepositoryProtocol,
)
from tests.unit.doubles.base import CallRecorderMixin, IntegerSequence, clone, evolve, utcnow


class InMemoryCrmMetricDefinitionRepository(CallRecorderMixin, CrmMetricDefinitionRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmMetricDefinitionEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmMetricDefinitionEntity) -> CrmMetricDefinitionEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.metric_definition_id) if entity.metric_definition_id is not None else None
        if existing is None:
            existing = next(
                (
                    item
                    for item in self._items.values()
                    if item.app_id == entity.app_id and item.machine_key == entity.machine_key
                ),
                None,
            )
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.metric_definition_id is None:
            changes["metric_definition_id"] = existing.metric_definition_id
        elif entity.metric_definition_id is None:
            changes["metric_definition_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.metric_definition_id is not None
        self._ids.observe(saved.metric_definition_id)
        self._items[saved.metric_definition_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmMetricDefinitionEntity]) -> list[CrmMetricDefinitionEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, metric_definition_id: int) -> CrmMetricDefinitionEntity | None:
        self._record("get_by_id", metric_definition_id)
        item = self._items.get(metric_definition_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int | None) -> list[CrmMetricDefinitionEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.metric_definition_id or 0,
        )
        return [clone(item) for item in items]


class InMemoryCrmConversionDefinitionRepository(CallRecorderMixin, CrmConversionDefinitionRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmConversionDefinitionEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmConversionDefinitionEntity) -> CrmConversionDefinitionEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.conversion_definition_id) if entity.conversion_definition_id is not None else None
        if existing is None:
            existing = next(
                (
                    item
                    for item in self._items.values()
                    if item.app_id == entity.app_id and item.machine_key == entity.machine_key
                ),
                None,
            )
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.conversion_definition_id is None:
            changes["conversion_definition_id"] = existing.conversion_definition_id
        elif entity.conversion_definition_id is None:
            changes["conversion_definition_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.conversion_definition_id is not None
        self._ids.observe(saved.conversion_definition_id)
        self._items[saved.conversion_definition_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmConversionDefinitionEntity]) -> list[CrmConversionDefinitionEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, conversion_definition_id: int) -> CrmConversionDefinitionEntity | None:
        self._record("get_by_id", conversion_definition_id)
        item = self._items.get(conversion_definition_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int | None) -> list[CrmConversionDefinitionEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.conversion_definition_id or 0,
        )
        return [clone(item) for item in items]


class InMemoryCrmParamDefinitionRepository(CallRecorderMixin, CrmParamDefinitionRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmParamDefinitionEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmParamDefinitionEntity) -> CrmParamDefinitionEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.param_definition_id) if entity.param_definition_id is not None else None
        if existing is None:
            existing = next(
                (
                    item
                    for item in self._items.values()
                    if item.app_id == entity.app_id and item.machine_key == entity.machine_key
                ),
                None,
            )
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.param_definition_id is None:
            changes["param_definition_id"] = existing.param_definition_id
        elif entity.param_definition_id is None:
            changes["param_definition_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.param_definition_id is not None
        self._ids.observe(saved.param_definition_id)
        self._items[saved.param_definition_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmParamDefinitionEntity]) -> list[CrmParamDefinitionEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, param_definition_id: int) -> CrmParamDefinitionEntity | None:
        self._record("get_by_id", param_definition_id)
        item = self._items.get(param_definition_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int | None) -> list[CrmParamDefinitionEntity]:
        self._record("list_by_app_id", app_id)
        items = sorted(
            (item for item in self._items.values() if item.app_id == app_id),
            key=lambda item: item.param_definition_id or 0,
        )
        return [clone(item) for item in items]


class InMemoryCrmSecretTemplateRepository(CallRecorderMixin, CrmSecretTemplateRepositoryProtocol):
    def __init__(self) -> None:
        super().__init__()
        self._items: dict[int, CrmSecretTemplateEntity] = {}
        self._ids = IntegerSequence()

    def save(self, entity: CrmSecretTemplateEntity) -> CrmSecretTemplateEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.template_id) if entity.template_id is not None else None
        if existing is None:
            existing = next((item for item in self._items.values() if item.code == entity.code), None)
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.template_id is None:
            changes["template_id"] = existing.template_id
        elif entity.template_id is None:
            changes["template_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.template_id is not None
        self._ids.observe(saved.template_id)
        self._items[saved.template_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmSecretTemplateEntity]) -> list[CrmSecretTemplateEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, template_id: int) -> CrmSecretTemplateEntity | None:
        self._record("get_by_id", template_id)
        item = self._items.get(template_id)
        return clone(item) if item is not None else None

    def get_by_code(self, code: str) -> CrmSecretTemplateEntity | None:
        self._record("get_by_code", code)
        item = next((entity for entity in self._items.values() if entity.code == code), None)
        return clone(item) if item is not None else None

    def list_all(self) -> list[CrmSecretTemplateEntity]:
        self._record("list_all")
        return [clone(item) for item in sorted(self._items.values(), key=lambda item: item.template_id or 0)]


class InMemoryCrmPostbackRuleRepository(CallRecorderMixin, CrmPostbackRuleRepositoryProtocol):
    def __init__(
        self,
        *,
        platform_lookup: Callable[[int], CrmAppPlatformEntity | None],
    ) -> None:
        super().__init__()
        self._items: dict[int, CrmPostbackRuleEntity] = {}
        self._ids = IntegerSequence()
        self._platform_lookup = platform_lookup

    def save(self, entity: CrmPostbackRuleEntity) -> CrmPostbackRuleEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.rule_id) if entity.rule_id is not None else None
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.rule_id is None:
            changes["rule_id"] = existing.rule_id
        elif entity.rule_id is None:
            changes["rule_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.rule_id is not None
        self._ids.observe(saved.rule_id)
        self._items[saved.rule_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmPostbackRuleEntity]) -> list[CrmPostbackRuleEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, rule_id: int) -> CrmPostbackRuleEntity | None:
        self._record("get_by_id", rule_id)
        item = self._items.get(rule_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int) -> list[CrmPostbackRuleEntity]:
        self._record("list_by_app_id", app_id)
        items = [
            item
            for item in self._items.values()
            if (platform := self._platform_lookup(item.platfrom_app_id)) is not None and platform.app_id == app_id
        ]
        items.sort(key=lambda item: item.rule_id or 0)
        return [clone(item) for item in items]

    def list_active_by_app(self, app_id: int) -> list[CrmPostbackRuleEntity]:
        self._record("list_active_by_app", app_id)
        items = [item for item in self.list_by_app_id(app_id) if item.is_active]
        return [clone(item) for item in items]


class InMemoryCrmAppSecretRepository(CallRecorderMixin, CrmAppSecretRepositoryProtocol):
    def __init__(
        self,
        *,
        platform_lookup: Callable[[int], CrmAppPlatformEntity | None],
    ) -> None:
        super().__init__()
        self._items: dict[int, CrmAppSecretEntity] = {}
        self._ids = IntegerSequence()
        self._platform_lookup = platform_lookup

    def save(self, entity: CrmAppSecretEntity) -> CrmAppSecretEntity:
        self._record("save", clone(entity))
        existing = self._items.get(entity.secret_id) if entity.secret_id is not None else None
        if existing is None:
            existing = next(
                (
                    item
                    for item in self._items.values()
                    if item.platform_id == entity.platform_id
                    and item.template_id == entity.template_id
                    and item.version == entity.version
                ),
                None,
            )
        now = utcnow()
        changes: dict[str, object] = {}
        if existing is not None and entity.secret_id is None:
            changes["secret_id"] = existing.secret_id
        elif entity.secret_id is None:
            changes["secret_id"] = self._ids.next()
        if existing is not None and entity.created_at is None:
            changes["created_at"] = existing.created_at
        elif entity.created_at is None:
            changes["created_at"] = now
        if entity.updated_at is None:
            changes["updated_at"] = now
        saved = evolve(entity, **changes) if changes else clone(entity)
        assert saved.secret_id is not None
        self._ids.observe(saved.secret_id)
        self._items[saved.secret_id] = clone(saved)
        return clone(saved)

    def save_many(self, entities: list[CrmAppSecretEntity]) -> list[CrmAppSecretEntity]:
        self._record("save_many", clone(entities))
        return [self.save(entity) for entity in entities]

    def get_by_id(self, secret_id: int) -> CrmAppSecretEntity | None:
        self._record("get_by_id", secret_id)
        item = self._items.get(secret_id)
        return clone(item) if item is not None else None

    def list_by_app_id(self, app_id: int, *, platform_id: int | None = None) -> list[CrmAppSecretEntity]:
        self._record("list_by_app_id", app_id, platform_id=platform_id)
        items: list[CrmAppSecretEntity] = []
        for item in self._items.values():
            if item.platform_id is None:
                continue
            platform = self._platform_lookup(item.platform_id)
            if platform is None or platform.app_id != app_id:
                continue
            if platform_id is not None and item.platform_id != platform_id:
                continue
            items.append(clone(item))
        items.sort(key=lambda item: item.secret_id or 0)
        return [clone(item) for item in items]

    def list_active_by_app(
        self,
        app_id: int,
        *,
        platform_id: int | None = None,
    ) -> list[CrmAppSecretEntity]:
        self._record("list_active_by_app", app_id, platform_id=platform_id)
        return [
            clone(item)
            for item in self.list_by_app_id(app_id, platform_id=platform_id)
            if item.active_flag
        ]
