from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.domain.exceptions import DomainException
from tests.unit.builders import build_current_param_entity


def test_update_param_replace_overwrites_scalar_slot() -> None:
    entity = build_current_param_entity(value_string="organic")

    entity.update_param("replace", "paid")

    assert entity.value_string == "paid"
    assert entity.value_number is None
    assert entity.value_bool is None
    assert entity.value_json is None
    assert entity.updated_at is not None


def test_update_param_append_supports_uniq_lists() -> None:
    entity = build_current_param_entity(value_string=None, value_json=["email"])

    entity.update_param("append", ["push", "sms", "sms"])

    assert entity.value_json == ["email", "push", "sms"]


def test_update_param_merge_supports_dicts() -> None:
    entity = build_current_param_entity(
        value_string=None,
        value_json={"utm_source": "organic", "campaign": "spring"},
    )

    entity.update_param("merge", {"campaign": "summer", "channel": "push"})

    assert entity.value_json == {
        "utm_source": "organic",
        "campaign": "summer",
        "channel": "push",
    }


def test_update_param_merge_supports_unique_list_union() -> None:
    entity = build_current_param_entity(value_string=None, value_json=["email", "push"])

    entity.update_param("merge", ["push", "sms"])

    assert entity.value_json == ["email", "push", "sms"]


def test_update_param_stores_boolean_and_datetime_values_in_supported_slots() -> None:
    bool_entity = build_current_param_entity(value_string="old")
    datetime_entity = build_current_param_entity(value_string="old")

    bool_entity.update_param("replace", True)
    datetime_entity.update_param("replace", datetime(2026, 3, 13, 15, 0, tzinfo=UTC))

    assert bool_entity.value_bool is True
    assert bool_entity.value_string is None
    assert datetime_entity.value_string == "2026-03-13T15:00:00+00:00"


def test_update_param_rejects_unsupported_policy() -> None:
    entity = build_current_param_entity()

    with pytest.raises(DomainException, match="Unsupported param update_policy"):
        entity.update_param("prepend", "paid")


def test_update_param_rejects_append_for_non_string_or_list_values() -> None:
    entity = build_current_param_entity(value_string=None, value_json={"source": "organic"})

    with pytest.raises(DomainException, match="Append policy supports only string and list values"):
        entity.update_param("append", {"source": "paid"})


def test_update_param_rejects_merge_for_scalar_values() -> None:
    entity = build_current_param_entity(value_string="organic")

    with pytest.raises(DomainException, match="Merge policy supports only dict and list values"):
        entity.update_param("merge", "paid")
