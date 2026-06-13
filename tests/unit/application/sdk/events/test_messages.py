from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.modules.crm.application.events_bus.factories.raw_event import RawEventMessage, RawEventMessageFactory
from app.modules.crm.application.exception import GeneralException
from tests.unit.builders import build_event_entity


def test_raw_event_message_factory_maps_domain_event_into_message() -> None:
    event = build_event_entity(
        event_id="evt-1",
        click_id="click-1",
        event_type="metric",
        event_key="install",
        event_time_utc=datetime(2026, 3, 13, 10, 0, tzinfo=UTC),
        payload={"install_key": "ios-install-key"},
    )

    message = RawEventMessageFactory.from_event(event, metadata={"tenant": "crm"})

    assert isinstance(message, RawEventMessage)
    assert message.name == RawEventMessage.EVENT_NAME
    assert message.event_id == "evt-1"
    assert message.click_id == "click-1"
    assert message.event_type == "metric"
    assert message.event_key == "install"
    assert message.raw_payload == {"install_key": "ios-install-key"}
    assert message.metadata == {"source": "sdk", "tenant": "crm"}
    assert message.occurred_at == event.event_time_utc


def test_raw_event_message_factory_uses_created_at_when_present() -> None:
    created_at = datetime(2026, 3, 13, 10, 30, tzinfo=UTC)
    event = build_event_entity(created_at=created_at)

    message = RawEventMessageFactory.from_event(event)

    assert message.occurred_at == created_at


def test_raw_event_message_factory_builds_many_messages() -> None:
    events = [
        build_event_entity(event_id="evt-1"),
        build_event_entity(event_id="evt-2", click_id="click-2"),
    ]

    messages = RawEventMessageFactory.from_events(events)

    assert [message.event_id for message in messages] == ["evt-1", "evt-2"]


def test_raw_event_message_factory_requires_event_id() -> None:
    event = build_event_entity(event_id="")

    with pytest.raises(GeneralException, match="Event id is required"):
        RawEventMessageFactory.from_event(event)
