from __future__ import annotations

import pytest

from app.domain.event_bus.events.exception_event import ExceptionEvent
from app.domain.exceptions import DomainError


def build_exception_event(**payload_overrides: object) -> ExceptionEvent:
    payload = {
        "exception_type": "ValueError",
        "exception_message": "boom",
        "context": {"source": "sdk"},
    }
    payload.update(payload_overrides)
    return ExceptionEvent(
        name=ExceptionEvent.EVENT_NAME,
        payload=payload,
    )


def test_exception_event_exposes_structured_payload_fields() -> None:
    event = build_exception_event(context={"source": "sdk", "event_id": "evt-1"})

    assert event.name == ExceptionEvent.EVENT_NAME
    assert event.exception_type == "ValueError"
    assert event.exception_message == "boom"
    assert event.context == {"source": "sdk", "event_id": "evt-1"}


def test_exception_event_context_returns_copy() -> None:
    event = build_exception_event(context={"source": "sdk"})

    context = event.context
    context["source"] = "mutated"

    assert event.context == {"source": "sdk"}


@pytest.mark.parametrize(
    ("payload_overrides", "property_name", "message"),
    [
        ({"exception_type": 123}, "exception_type", "ExceptionEvent.exception_type must be str"),
        (
            {"exception_message": ["boom"]},
            "exception_message",
            "ExceptionEvent.exception_message must be str",
        ),
        ({"context": ["sdk"]}, "context", "ExceptionEvent.context must be dict"),
    ],
)
def test_exception_event_validates_payload_types(
    payload_overrides: dict[str, object],
    property_name: str,
    message: str,
) -> None:
    event = build_exception_event(**payload_overrides)

    with pytest.raises(DomainError, match=message):
        getattr(event, property_name)
