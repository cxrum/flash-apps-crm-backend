from __future__ import annotations

from tests.unit.builders import build_event_entity


def test_event_entity_exposes_common_payload_fields_via_methods() -> None:
    event = build_event_entity(
        payload={
            "geo": "US",
            "ip": "203.0.113.10",
            "ua": "PartnerBot/1.0",
        }
    )

    assert event.payload_value("geo") == "US"
    assert event.geo() == "US"
    assert event.ip() == "203.0.113.10"
    assert event.ua() == "PartnerBot/1.0"


def test_event_entity_payload_methods_return_none_for_missing_fields() -> None:
    event = build_event_entity(payload={})

    assert event.geo() is None
    assert event.ip() is None
    assert event.ua() is None
