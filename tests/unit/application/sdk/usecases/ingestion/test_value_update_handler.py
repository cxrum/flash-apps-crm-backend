from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from app.application.events_bus.factories.value_update_event import (
    ValueChangedEventFactory,
    ValueChangedEventValue,
)
from app.application.events_bus.handlers.value_update import AsyncAuditValueHandler
from app.application.exception import GeneralException
from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.domain.event_bus.entity import DomainEventMessage
from app.domain.event_bus.events.crm_value_update_event import ValueChangedEvent
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory


def _build_value_changed_message() -> ValueChangedEvent:
    updated_at = datetime(2026, 6, 10, 12, 30, tzinfo=UTC)
    message = ValueChangedEventFactory.from_raw_payload(
        ValueChangedEventValue(
            crm_user_id=1,
            app_id=2,
            entity_id=3,
            old_value={
                "crm_apps": {
                    "name": "old app",
                    "settings": {"enabled": True, "limit": 10},
                    "removed": "value",
                },
                "crm_users": {"email": "same@example.com"},
            },
            new_value={
                "crm_apps": {
                    "name": "new app",
                    "settings": {"enabled": True, "limit": 20},
                    "added": "value",
                    "updated_at": "ignored-new",
                },
                "crm_users": {"email": "same@example.com"},
            },
            updated_at=updated_at,
            ignore_fields=("updated_at",),
        )
    )

    assert isinstance(message, ValueChangedEvent)
    return message


def test_async_audit_value_handler_persists_audit_logs_from_diff() -> None:
    async def scenario() -> None:
        uow = StubUnitOfWork()
        handler = AsyncAuditValueHandler(StubUoWFactory(uow))
        message = _build_value_changed_message()

        await handler.handle(message)

        saved_logs = uow.audit_log_repo.list_by_app_id(2)
        assert saved_logs == [
            CrmAuditLogEntity(
                audit_log_id=1,
                entity_changed="crm_apps",
                user_id=1,
                app_id=2,
                entity_id="3",
                old_value={
                    "name": "old app",
                    "settings": {"limit": 10},
                    "removed": "value",
                    "added": None,
                },
                new_value={
                    "name": "new app",
                    "settings": {"limit": 20},
                    "removed": None,
                    "added": "value",
                },
                changed_at=message.updated_at,
            )
        ]
        assert [call.method for call in uow.audit_log_repo.calls] == [
            "insert_many",
            "insert",
            "list_by_app_id",
        ]
        assert uow.enter_count == 1
        assert uow.commit_count == 1
        assert uow.rollback_count == 0

    asyncio.run(scenario())


def test_async_audit_value_handler_rejects_wrong_message_type() -> None:
    async def scenario() -> None:
        handler = AsyncAuditValueHandler(StubUoWFactory(StubUnitOfWork()))

        with pytest.raises(
            GeneralException,
            match="expected ValueChangedEvent, got DomainEventMessage",
        ):
            await handler.handle(DomainEventMessage(name=ValueChangedEvent.EVENT_NAME))

    asyncio.run(scenario())
