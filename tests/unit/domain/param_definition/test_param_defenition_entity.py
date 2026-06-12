from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from app.domain.exceptions import DomainException
from tests.unit.builders import build_param_definition_entity


def test_get_param_value_returns_none_for_missing_or_null_param() -> None:
    definition = build_param_definition_entity(machine_key="utm_source")

    assert definition.get_param_value({}) is None
    assert definition.get_param_value({"utm_source": None}) is None


@pytest.mark.parametrize(
    ("data_type", "raw_value", "expected"),
    [
        ("string", 123, "123"),
        ("integer", "42", 42),
        ("float", "42.5", 42.5),
        ("boolean", "true", True),
        ("enum", "organic", "organic"),
    ],
)
def test_get_param_value_coerces_scalar_values(
    data_type: str,
    raw_value: object,
    expected: object,
) -> None:
    definition = build_param_definition_entity(data_type=data_type, machine_key="value")

    assert definition.get_param_value({"value": raw_value}) == expected


def test_get_param_value_coerces_date_and_datetime_values() -> None:
    date_definition = build_param_definition_entity(data_type="date", machine_key="sent_at")
    datetime_definition = build_param_definition_entity(data_type="datetime", machine_key="processed_at")

    assert date_definition.get_param_value({"sent_at": "2026-03-13"}) == date(2026, 3, 13)
    assert datetime_definition.get_param_value({"processed_at": "2026-03-13T10:30:00Z"}) == datetime(
        2026,
        3,
        13,
        10,
        30,
        tzinfo=UTC,
    )


def test_get_param_value_coerces_json_and_list_values() -> None:
    json_definition = build_param_definition_entity(data_type="json", machine_key="payload")
    list_definition = build_param_definition_entity(data_type="list", machine_key="channels")

    assert json_definition.get_param_value({"payload": '{"country":"US","active":true}'}) == {
        "country": "US",
        "active": True,
    }
    assert list_definition.get_param_value({"channels": "email, push , sms"}) == [
        "email",
        "push",
        "sms",
    ]


def test_get_param_value_raises_for_invalid_value() -> None:
    definition = build_param_definition_entity(data_type="integer", machine_key="attempts")

    with pytest.raises(DomainException, match="expected integer"):
        definition.get_param_value({"attempts": "4.2"})


def test_get_param_value_raises_for_unsupported_data_type() -> None:
    definition = build_param_definition_entity(data_type="xml", machine_key="payload")

    with pytest.raises(DomainException, match="Unsupported param data_type"):
        definition.get_param_value({"payload": "<tag />"})
