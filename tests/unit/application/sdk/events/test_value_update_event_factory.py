from datetime import UTC, datetime

from app.modules.crm.application.events_bus.factories.value_update_event import (
    AuditEventValue,
    ValueChangedEventFactory,
)
from app.modules.crm.domain.event_bus.events.crm_value_update_event import ValueChangedEvent


def test_value_changed_event_factory_builds_typed_message() -> None:
    updated_at = datetime(2026, 6, 10, tzinfo=UTC)

    message = ValueChangedEventFactory.from_raw_payload(
        AuditEventValue(
            crm_user_id=1,
            app_id=2,
            entity_id=3,
            old_value={"crm_apps": {"name": "old"}},
            new_value={"crm_apps": {"name": "new"}},
            updated_at=updated_at,
            ignore_fields=("created_at", "updated_at"),
        ),
        metadata={"request_id": "req-1"},
    )

    assert isinstance(message, ValueChangedEvent)
    assert message.name == ValueChangedEvent.EVENT_NAME
    assert message.crm_user_id == 1
    assert message.app_id == 2
    assert message.entity_id == "3"
    assert message.old_value == {"crm_apps": {"name": "old"}}
    assert message.new_value == {"crm_apps": {"name": "new"}}
    assert message.ignore_fields == ("created_at", "updated_at")
    assert message.updated_at == updated_at
    assert message.occurred_at == updated_at
    assert message.metadata == {"source": "crm", "request_id": "req-1"}


def test_value_changed_event_factory_builds_batch() -> None:
    updated_at = datetime(2026, 6, 10, tzinfo=UTC)
    value = AuditEventValue(
        crm_user_id=1,
        old_value={"crm_apps": {"name": "old"}},
        new_value={"crm_apps": {"name": "new"}},
        updated_at=updated_at,
    )

    messages = ValueChangedEventFactory.from_raw_payloads([value])

    assert len(messages) == 1
    assert isinstance(messages[0], ValueChangedEvent)
    assert messages[0].metadata == {"source": "crm"}
