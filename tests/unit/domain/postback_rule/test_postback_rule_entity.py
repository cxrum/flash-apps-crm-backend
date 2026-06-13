from __future__ import annotations

import pytest

from app.modules.crm.domain.exceptions import DomainException
from tests.unit.builders import build_postback_rule_entity


@pytest.mark.parametrize(
    "endpoint_url",
    [
        "https://example.com/postback",
        "http://example.com/postback?event=install",
        "https://api.example.com:8443/hooks/postback",
    ],
)
def test_validate_url_accepts_http_and_https_urls(endpoint_url: str) -> None:
    entity = build_postback_rule_entity(endpoint_url=endpoint_url)

    entity.validate_url()


@pytest.mark.parametrize(
    ("endpoint_url", "expected_match"),
    [
        ("", "required"),
        ("   ", "required"),
        ("ftp://example.com/postback", "http or https"),
        ("example.com/postback", "http or https"),
        ("https:///postback", "include a host"),
        ("https://", "include a host"),
        ("https://example.com/post back", "must not contain spaces"),
    ],
)
def test_validate_url_rejects_invalid_urls(
    endpoint_url: str,
    expected_match: str,
) -> None:
    entity = build_postback_rule_entity(endpoint_url=endpoint_url)

    with pytest.raises(DomainException, match=expected_match):
        entity.validate_url()
