from __future__ import annotations

import pytest

from app.modules.analytics.domain.click.exception import AnalyticsClickPlatformMismatch, AnalyticsClickStatusInvalid
from app.modules.analytics.domain.current_param.exception import (
    AppendPolicyNotSupported,
    MergePolicyNotSupported,
    UnsupportedCurrentParamUpdatePolicy,
)
from app.modules.crm.domain.event_bus.events.exception import InvalidRawEventPayload
from app.modules.crm.domain.exceptions import DomainException
from app.modules.crm.domain.param_definition.exception import InvalidParamDataType, InvalidParamValue
from app.modules.crm.domain.postback_rule.exception import MissingSecretTemplate, PostbackUrlRequired
from app.modules.crm.domain.role.exceptions import AdminAccessRequired, ManagerAccessRequired


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        pytest.param(AnalyticsClickStatusInvalid(), "Click status is invalid", id="click-status"),
        pytest.param(AnalyticsClickPlatformMismatch(), "Click platform does not match", id="click-platform"),
        pytest.param(
            UnsupportedCurrentParamUpdatePolicy("prepend"),
            "Unsupported param update_policy: prepend",
            id="current-param-policy",
        ),
        pytest.param(
            AppendPolicyNotSupported(),
            "Append policy supports only string and list values",
            id="append-policy",
        ),
        pytest.param(
            MergePolicyNotSupported(),
            "Merge policy supports only dict and list values",
            id="merge-policy",
        ),
        pytest.param(AdminAccessRequired(), "Admin access is required", id="role-admin-required"),
        pytest.param(ManagerAccessRequired(), "Manager access is required", id="role-manager-required"),
        pytest.param(
            InvalidParamDataType("xml"),
            "Unsupported param data_type: xml",
            id="param-data-type",
        ),
        pytest.param(
            InvalidParamValue("attempt", "integer", "4.2"),
            "Param 'attempt' expected integer, got '4.2'",
            id="param-value",
        ),
        pytest.param(
            MissingSecretTemplate("missing-secret"),
            "Secret template: missing-secret doesn't exist",
            id="postback-secret-template",
        ),
        pytest.param(PostbackUrlRequired(), "Postback endpoint URL is required", id="postback-url-required"),
        pytest.param(
            InvalidRawEventPayload(),
            "RawEventMessage.payload['payload'] must be dict",
            id="raw-event-payload",
        ),
    ],
)
def test_domain_exceptions_resolve_messages(exc: Exception, expected: str) -> None:
    assert str(exc) == expected
