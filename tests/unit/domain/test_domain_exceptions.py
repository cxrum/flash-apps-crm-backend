from __future__ import annotations

import pytest

from app.modules.analytics.domain.click.exception import AnalyticsClickPlatformMismatch, AnalyticsClickStatusInvalid
from app.modules.analytics.domain.current_param.exception import (
    AppendPolicyNotSupported,
    MergePolicyNotSupported,
    UnsupportedCurrentParamUpdatePolicy,
)
from app.modules.crm.core.exception_resolver import MessageResolver
from app.modules.crm.domain.event_bus.events.exception import InvalidRawEventPayload
from app.modules.crm.domain.exceptions import DomainException
from app.modules.crm.domain.param_definition.exception import InvalidParamDataType, InvalidParamValue
from app.modules.crm.domain.postback_rule.exception import MissingSecretTemplate, PostbackUrlRequired
from app.modules.crm.domain.role.exceptions import AdminAccessRequired, ManagerAccessRequired


@pytest.mark.parametrize(
    ("exc", "message_key"),
    [
        pytest.param(AnalyticsClickStatusInvalid(), "domain.click.status.invalid", id="click-status"),
        pytest.param(AnalyticsClickPlatformMismatch(), "domain.click.platform.invalid", id="click-platform"),
        pytest.param(
            UnsupportedCurrentParamUpdatePolicy("prepend"),
            "domain.current_param.update_policy.unsupported",
            id="current-param-policy",
        ),
        pytest.param(
            AppendPolicyNotSupported(),
            "domain.current_param.append.unsupported",
            id="append-policy",
        ),
        pytest.param(
            MergePolicyNotSupported(),
            "domain.current_param.merge.unsupported",
            id="merge-policy",
        ),
        pytest.param(AdminAccessRequired(), "domain.role.access.admin_required", id="role-admin-required"),
        pytest.param(ManagerAccessRequired(), "domain.role.access.manager_required", id="role-manager-required"),
        pytest.param(
            InvalidParamDataType("xml"),
            "domain.param_definition.data_type.invalid",
            id="param-data-type",
        ),
        pytest.param(
            InvalidParamValue("attempt", "integer", "4.2"),
            "domain.param_definition.value.invalid",
            id="param-value",
        ),
        pytest.param(
            MissingSecretTemplate("missing-secret"),
            "domain.postback.secret_template.missing",
            id="postback-secret-template",
        ),
        pytest.param(PostbackUrlRequired(), "domain.postback.url.required", id="postback-url-required"),
        pytest.param(
            InvalidRawEventPayload(),
            "domain.event_bus.raw_event.payload.invalid",
            id="raw-event-payload",
        ),
    ],
)
def test_domain_exceptions_preserve_message_key(exc: Exception, message_key: str) -> None:
    assert getattr(exc, "message_key") == message_key
    assert MessageResolver().resolve(message_key, getattr(exc, "context"))
