from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.conversion_definition.CrmConversionDefinitionEntity import (
    CrmConversionDefinitionEntity,
)
from app.domain.currency.entity import CurrencyEntity
from app.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.role_permission.CrmRolePermissionEntity import CrmRolePermissionEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.user.CrmUserEntity import CrmUserEntity
from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.user_role.CrmUserRoleEntity import CrmUserRoleEntity


def _merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    merged.update(overrides)
    return merged


def _now() -> datetime:
    return datetime(2026, 3, 12, 12, 0, tzinfo=UTC)


def build_app_entity(**overrides: Any) -> CrmAppEntity:
    return CrmAppEntity(**_merge({"name": "Test App", "code_slug": "test-app"}, overrides))


def build_app_platform_entity(**overrides: Any) -> CrmAppPlatformEntity:
    return CrmAppPlatformEntity(
        **_merge(
            {
                "app_id": 1,
                "platform": "ios",
                "package_name": "com.example.test",
                "install_key": "install-key-ios",
            },
            overrides,
        )
    )


def build_app_secret_entity(**overrides: Any) -> CrmAppSecretEntity:
    return CrmAppSecretEntity(
        **_merge(
            {
                "template_id": 1,
                "encrypted_value": "enc::secret",
                "platform_id": 1,
                "active_flag": True,
                "version": 1,
            },
            overrides,
        )
    )


def build_app_user_entity(**overrides: Any) -> CrmAppUserEntity:
    return CrmAppUserEntity(**_merge({"app_id": 1}, overrides))


def build_audit_log_entity(**overrides: Any) -> CrmAuditLogEntity:
    return CrmAuditLogEntity(
        **_merge(
            {
                "entity_changed": "crm_apps",
                "app_id": 1,
                "changed_at": _now(),
            },
            overrides,
        )
    )


def build_click_entity(**overrides: Any) -> CrmClickEntity:
    return CrmClickEntity(
        **_merge(
            {
                "click_id": "click-1",
                "app_platform_id": 1,
                "created_at": _now(),
            },
            overrides,
        )
    )


def build_conversion_definition_entity(
    **overrides: Any,
) -> CrmConversionDefinitionEntity:
    return CrmConversionDefinitionEntity(
        **_merge(
            {
                "machine_key": "purchase",
                "display_name": "Purchase",
                "app_id": 1,
            },
            overrides,
        )
    )


def build_current_param_entity(**overrides: Any) -> CrmCurrentParamEntity:
    return CrmCurrentParamEntity(
        **_merge(
            {
                "click_id": "click-1",
                "param_key": "utm_source",
                "value_string": "organic",
                "updated_at": _now(),
            },
            overrides,
        )
    )


def build_event_entity(**overrides: Any) -> EventEntity:
    return EventEntity(
        **_merge(
            {
                "event_id": "evt-1",
                "click_id": "click-1",
                "event_type": "metric",
                "event_key": "first_open",
                "event_time_utc": _now(),
            },
            overrides,
        )
    )


def build_install_entity(**overrides: Any) -> CrmInstallEntity:
    return CrmInstallEntity(
        **_merge(
            {
                "click_id": "click-1",
                "app_platform_id": 1,
            },
            overrides,
        )
    )


def build_metric_definition_entity(**overrides: Any) -> CrmMetricDefinitionEntity:
    return CrmMetricDefinitionEntity(
        **_merge(
            {
                "machine_key": "first_open",
                "display_name": "First Open",
                "app_id": 1,
            },
            overrides,
        )
    )


def build_param_definition_entity(**overrides: Any) -> CrmParamDefinitionEntity:
    return CrmParamDefinitionEntity(
        **_merge(
            {
                "display_name": "UTM Source",
                "machine_key": "utm_source",
                "data_type": "string",
                "app_id": 1,
            },
            overrides,
        )
    )


def build_permission_entity(**overrides: Any) -> CrmPermissionEntity:
    return CrmPermissionEntity(**_merge({"code": "apps.view"}, overrides))


def build_postback_rule_entity(**overrides: Any) -> CrmPostbackRuleEntity:
    return CrmPostbackRuleEntity(
        **_merge(
            {
                "platfrom_app_id": 1,
                "name": "Install postback",
                "endpoint_url": "https://example.com/postback",
                "trigger_type": "install",
            },
            overrides,
        )
    )


def build_push_campaign_entity(**overrides: Any) -> CrmPushCampaignEntity:
    return CrmPushCampaignEntity(
        **_merge(
            {
                "app_id": 1,
                "title": "Hello",
                "body": "World",
            },
            overrides,
        )
    )


def build_push_event_entity(**overrides: Any) -> CrmPushEventEntity:
    return CrmPushEventEntity(
        **_merge(
            {
                "campaign_id": 1,
                "token_id": 1,
                "event_type": "sent",
                "event_time_utc": _now(),
            },
            overrides,
        )
    )


def build_push_token_entity(**overrides: Any) -> CrmPushTokenEntity:
    return CrmPushTokenEntity(
        **_merge(
            {
                "install_id": 1,
                "token": "push-token-1",
            },
            overrides,
        )
    )


def build_role_entity(**overrides: Any) -> CrmRoleEntity:
    return CrmRoleEntity(**_merge({"code": "manager", "display_name": "Manager"}, overrides))


def build_role_permission_entity(**overrides: Any) -> CrmRolePermissionEntity:
    return CrmRolePermissionEntity(
        **_merge({"role_id": 1, "permission_id": 1}, overrides)
    )


def build_secret_template_entity(**overrides: Any) -> CrmSecretTemplateEntity:
    return CrmSecretTemplateEntity(
        **_merge(
            {
                "code": "api_key",
                "display_name": "API Key",
                "scope": "client_public",
                "value_type": "text",
            },
            overrides,
        )
    )


def build_user_entity(**overrides: Any) -> CrmUserEntity:
    return CrmUserEntity(
        **_merge(
            {
                "full_name": "Manager User",
                "email": "manager@example.com",
                "password_hash": "hashed-password",
            },
            overrides,
        )
    )


def build_user_app_access_entity(**overrides: Any) -> CrmUserAppAccessEntity:
    return CrmUserAppAccessEntity(**_merge({"user_id": 1, "app_id": 1}, overrides))


def build_user_role_entity(**overrides: Any) -> CrmUserRoleEntity:
    return CrmUserRoleEntity(**_merge({"user_id": 1, "role_id": 1}, overrides))

def build_currency_entity(**overrides: Any) -> CurrencyEntity:
    return CurrencyEntity(
        **_merge(
            {
                "base": "USD",
                "value": 1,
            },
            overrides,
        )
    )