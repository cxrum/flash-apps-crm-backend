from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from app.domain.crm.app.CrmAppEntity import CrmAppEntity
from app.domain.crm.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.crm.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.crm.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.domain.crm.click.CrmClickEntity import CrmClickEntity
from app.domain.crm.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.domain.crm.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.crm.event.CrmEventEntity import CrmEventEntity
from app.domain.crm.install.CrmInstallEntity import CrmInstallEntity
from app.domain.crm.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.crm.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.crm.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.crm.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.crm.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.crm.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.crm.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.crm.role.CrmRoleEntity import CrmRoleEntity
from app.domain.crm.role_permission.CrmRolePermissionEntity import CrmRolePermissionEntity
from app.domain.crm.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.crm.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.crm.CrmUserEntity import CrmUserEntity
from app.domain.crm.user_role.CrmUserRoleEntity import CrmUserRoleEntity
from app.domain.crm.audit_log.CrmAuditLogEntity import (
    CrmAuditLogEntity,
)


def test_crm_entities_support_minimal_construction() -> None:
    now = datetime(2026, 3, 9, 12, 0, tzinfo=UTC)
    entities = [
        CrmAppEntity(name="Test app", code_slug="test-app"),
        CrmAppPlatformEntity(app_id=1, platform="ios", package_name="com.example.app", install_key="inst-key"),
        CrmUserEntity(full_name="Manager", email="manager@example.com", password_hash="hash"),
        CrmRoleEntity(code="manager", display_name="Manager"),
        CrmPermissionEntity(code="view_stats"),
        CrmRolePermissionEntity(role_id=1, permission_id=1),
        CrmUserRoleEntity(user_id=1, role_id=1),
        CrmUserAppAccessEntity(user_id=1, app_id=1),
        CrmClickEntity(click_id="click-1", app_platform_id=1),
        CrmAppUserEntity(app_platform_id=1, crm_user_id="crm-user-1"),
        CrmInstallEntity(app_user_id=1),
        CrmEventEntity(
            event_id="event-1",
            app_id=1,
            event_type="metric",
            event_key="first_open",
            event_time_utc=now,
        ),
        CrmCurrentParamEntity(click_id="click-1", param_key="utm_source", value_string="organic"),
        CrmMetricDefinitionEntity(machine_key="first_open", display_name="First Open"),
        CrmConversionDefinitionEntity(machine_key="trial_start", display_name="Trial Start"),
        CrmSecretTemplateEntity(
            code="openai_api_key",
            display_name="OpenAI API key",
            scope="server_private",
            value_type="string",
        ),
        CrmAppSecretEntity(app_id=1, template_id=1, encrypted_value="enc-value"),
        CrmParamDefinitionEntity(machine_key="utm_source", data_type="string"),
        CrmPostbackRuleEntity(app_id=1, endpoint_url="https://example.com/postback", trigger_type="conversion"),
        CrmPushCampaignEntity(app_id=1, title="Hello", body="Body"),
        CrmPushTokenEntity(app_user_id=1, app_platform_id=1, token="token", platform="ios"),
        CrmPushEventEntity(campaign_id=1, token_id=1, event_type="sent", event_time_utc=now),
        CrmAuditLogEntity(entity_changed="crm_apps", app_id=1),
    ]

    assert len(entities) == 23


def test_crm_entities_defaults_are_safe_and_predictable() -> None:
    first_app = CrmAppEntity(name="A", code_slug="a")
    second_app = CrmAppEntity(name="B", code_slug="b")
    click = CrmClickEntity(click_id="click-2", app_platform_id=1)
    postback = CrmPostbackRuleEntity(
        app_id=1,
        endpoint_url="https://example.com/rule",
        trigger_type="metric",
    )

    assert first_app.screenshots == []
    assert first_app.screenshots is not second_app.screenshots
    assert click.raw_query == {}
    assert click.geo == {}
    assert postback.template == {}
    assert postback.retry_policy == {}


def test_crm_entities_keep_decimal_and_datetime_values() -> None:
    now = datetime(2026, 3, 9, 12, 0, tzinfo=UTC)
    event = CrmEventEntity(
        event_id="event-2",
        app_id=1,
        event_type="conversion",
        event_key="purchase",
        event_time_utc=now,
        amount=Decimal("12.50"),
        amount_usd=Decimal("12.50"),
    )
    secret = CrmAppSecretEntity(app_id=1, template_id=1, encrypted_value="enc")
    param = CrmCurrentParamEntity(click_id="click-3", param_key="amount", value_number=Decimal("12.5"))

    assert event.event_time_utc == now
    assert event.amount == Decimal("12.50")
    assert event.amount_usd == Decimal("12.50")
    assert secret.version == Decimal("1")
    assert param.value_number == Decimal("12.5")
