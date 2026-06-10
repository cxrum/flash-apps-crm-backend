from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import asdict, dataclass, is_dataclass
from datetime import UTC, datetime
from typing import Any, TypeVar

from app.application.events_bus.factories.value_update_event import (
    ValueChangedEventFactory,
    ValueChangedEventValue,
)
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.service_protocol import IAsyncEventBus
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol

T = TypeVar("T")


@dataclass(frozen=True)
class AuditSnapshot:
    value: dict[str, Any]
    updated_at: datetime | None


@dataclass(frozen=True)
class AuditConfig:
    ignore_fields: tuple[str, ...] = ("created_at", "updated_at")


class AuditedUtils:
    @classmethod
    def audit_value(cls, value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, dict):
            return {str(key): cls.audit_value(item) for key, item in value.items()}
        if isinstance(value, list):
            return [cls.audit_value(item) for item in value]
        if isinstance(value, tuple):
            return [cls.audit_value(item) for item in value]
        return value

    @classmethod
    def audit_entity_value(cls, entity: object) -> dict[str, Any]:
        if is_dataclass(entity):
            data = asdict(entity)
        else:
            data = dict(vars(entity))

        return cls.audit_value(data)

    @classmethod
    def load_snapshot(
        cls,
        uow_factory: UnitOfWorkFactoryProtocol,
        loader: Callable[[UnitOfWorkProtocol], object | None],
    ) -> AuditSnapshot | None:
        with uow_factory.create() as uow:
            entity = loader(uow)

        if entity is None:
            return None

        return AuditSnapshot(
            value=cls.audit_entity_value(entity),
            updated_at=getattr(entity, "updated_at", None),
        )

    @classmethod
    def dispatch_async_event(
        cls,
        async_event_bus: IAsyncEventBus,
        message: DomainEventMessage,
    ) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(async_event_bus.publish(message))
            return

        loop.create_task(async_event_bus.publish(message))

    @classmethod
    def publish_value_update_event(
        cls,
        async_event_bus: IAsyncEventBus,
        *,
        crm_user_id: int,
        app_id: int | None,
        entity_changed: str,
        entity_id: int | str | None,
        old_value: dict[str, Any],
        new_value: dict[str, Any],
        updated_at: datetime | None,
        ignore_fields: tuple[str, ...] | None = None,
    ) -> None:
        resolved_ignore_fields = () if ignore_fields is None else ignore_fields
        message = ValueChangedEventFactory.from_raw_payload(
            ValueChangedEventValue(
                crm_user_id=crm_user_id,
                app_id=app_id,
                entity_id=entity_id,
                old_value={entity_changed: old_value},
                new_value={entity_changed: new_value},
                updated_at=updated_at or datetime.now(UTC),
                ignore_fields=resolved_ignore_fields,
            )
        )
        cls.dispatch_async_event(async_event_bus, message)

    @classmethod
    def publish_entity_change(
        cls,
        async_event_bus: IAsyncEventBus,
        *,
        crm_user_id: int,
        app_id: int | None,
        entity_changed: str,
        entity_id: int | str | None,
        old_snapshot: AuditSnapshot | None,
        new_snapshot: AuditSnapshot | None,
        ignore_fields: tuple[str, ...] | None = None,
    ) -> None:
        if old_snapshot is None or new_snapshot is None:
            return

        cls.publish_value_update_event(
            async_event_bus,
            crm_user_id=crm_user_id,
            app_id=app_id,
            entity_changed=entity_changed,
            entity_id=entity_id,
            old_value=old_snapshot.value,
            new_value=new_snapshot.value,
            updated_at=new_snapshot.updated_at,
            ignore_fields=ignore_fields,
        )

    @classmethod
    def audit_entity_update(
        cls,
        uow_factory: UnitOfWorkFactoryProtocol,
        async_event_bus: IAsyncEventBus,
        *,
        crm_user_id: int,
        app_id: int,
        entity_changed: str,
        entity_id: int | str | None,
        loader: Callable[[UnitOfWorkProtocol], object | None],
        operation: Callable[[], T],
        ignore_fields: tuple[str, ...] | None = None,
    ) -> T:
        old_snapshot = cls.load_snapshot(uow_factory, loader)
        response = operation()
        new_snapshot = cls.load_snapshot(uow_factory, loader)

        cls.publish_entity_change(
            async_event_bus,
            crm_user_id=crm_user_id,
            app_id=app_id,
            entity_changed=entity_changed,
            entity_id=entity_id,
            old_snapshot=old_snapshot,
            new_snapshot=new_snapshot,
            ignore_fields=ignore_fields,
        )
        return response

    @classmethod
    def audit_entity_create(
        cls,
        uow_factory: UnitOfWorkFactoryProtocol,
        async_event_bus: IAsyncEventBus,
        *,
        crm_user_id: int,
        entity_changed: str,
        loader: Callable[[UnitOfWorkProtocol], object | None],
        create_operation: Callable[[], T],
        ignore_fields: tuple[str, ...] | None = None,
    ) -> T:
        old_snapshot = AuditSnapshot(value={}, updated_at=None)
        response = create_operation()
        new_snapshot = cls.load_snapshot(uow_factory, loader)

        cls.publish_entity_change(
            async_event_bus,
            crm_user_id=crm_user_id,
            entity_changed=entity_changed,
            old_snapshot=old_snapshot,
            new_snapshot=new_snapshot,
            ignore_fields=ignore_fields,
            app_id=None,
            entity_id=None,
        )
        return response
