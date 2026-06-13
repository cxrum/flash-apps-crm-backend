from __future__ import annotations

import pytest

from app.modules.crm.domain.exceptions import DomainException
from app.modules.crm.domain.postback_rule.template import PostbackTemplateEntity


def test_postback_template_supports_dictionary_access() -> None:
    template = PostbackTemplateEntity({"click_id": "{click_id}"})

    template["event_key"] = "{event_key}"

    assert template["click_id"] == "{click_id}"
    assert template.get("event_key") == "{event_key}"
    assert "click_id" in template
    assert len(template) == 2
    assert list(template) == ["click_id", "event_key"]


def test_postback_template_supports_keys_values_items_and_update() -> None:
    template = PostbackTemplateEntity()

    template.update({"click_id": "{click_id}"}, event_key="{event_key}")

    assert list(template.keys()) == ["click_id", "event_key"]
    assert list(template.values()) == ["{click_id}", "{event_key}"]
    assert list(template.items()) == [
        ("click_id", "{click_id}"),
        ("event_key", "{event_key}"),
    ]


def test_postback_template_supports_pop_and_delete() -> None:
    template = PostbackTemplateEntity(
        {
            "click_id": "{click_id}",
            "event_key": "{event_key}",
        }
    )

    assert template.pop("event_key") == "{event_key}"
    del template["click_id"]

    assert len(template) == 0


def test_postback_template_clear_removes_all_values() -> None:
    template = PostbackTemplateEntity({"click_id": "{click_id}"})

    template.clear()

    assert template._template == {}


def test_postback_template_rejects_invalid_values_from_dictionary_methods() -> None:
    template = PostbackTemplateEntity()

    with pytest.raises(DomainException):
        template["click_id"] = "click_id"

    with pytest.raises(DomainException):
        template.update({"event_key": "event_key"})
