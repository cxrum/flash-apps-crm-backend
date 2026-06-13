from __future__ import annotations

import pytest

from app.modules.crm.application.admin.crm_authorization.exceptions import AdminAccessRequired
from app.modules.crm.application.admin.definitions.exceptions import MetricDefinitionNotFound
from app.modules.crm.application.admin.exception import ClickNotFound, EventNotFound, InstallNotFound
from app.modules.crm.application.admin.postback.exception import PostbackPlatformNotFound
from app.modules.crm.application.admin.push.exception import InvalidScheduledAt
from app.modules.crm.application.admin.secrets.exception import AppSecretNotFound, SecretTemplateNotFound
from app.modules.crm.application.exception import GeneralException


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        pytest.param(ClickNotFound("click-1"), "Click 'click-1' doesn't exist", id="click-not-found"),
        pytest.param(EventNotFound("evt-1"), "Event 'evt-1' doesn't exist", id="event-not-found"),
        pytest.param(InstallNotFound("click-1"), "Install doesn't exist", id="install-not-found"),
        pytest.param(AdminAccessRequired(), "Admin access is required", id="admin-access-required"),
        pytest.param(
            MetricDefinitionNotFound(7), "Metric definition with id 7 doesn't exist", id="metric-definition-not-found"
        ),
        pytest.param(PostbackPlatformNotFound(), "Platform doesn't exist", id="postback-platform-not-found"),
        pytest.param(
            InvalidScheduledAt("not-a-date"), "Invalid scheduled_at value: not-a-date", id="invalid-scheduled-at"
        ),
        pytest.param(SecretTemplateNotFound(3), "Secret template doesn't exist", id="secret-template-not-found"),
        pytest.param(AppSecretNotFound(9), "App secret doesn't exist", id="app-secret-not-found"),
    ],
)
def test_admin_exceptions_resolve_messages(exc: GeneralException, expected: str) -> None:
    assert isinstance(exc, GeneralException)
    assert str(exc) == expected
