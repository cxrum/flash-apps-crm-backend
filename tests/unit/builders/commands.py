from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, TypeVar

from app.application.admin.entities import (
    AppSecretValueCommand,
    CommandPreview,
    CreateAppCommand,
    CreateAppPlatformCommand,
    CreateConversionDefinitionCommand,
    CreateMetricDefinitionCommand,
    CreateParamDefinitionCommand,
    CreatePostbackRuleCommand,
    CreatePushCampaignCommand,
    CreateRoleCommand,
    CreateSecretTemplateCommand,
    GetAuditLogCommand,
    GetStatsCommand,
    ListAppPlatformsCommand,
    ListAppsCommand,
    ListAppSecretsCommand,
    ListClickLogsCommand,
    ListConversionDefinitionsCommand,
    ListEventLogsCommand,
    ListMetricDefinitionsCommand,
    ListParamDefinitionsCommand,
    ListPostbackRulesCommand,
    ListPushCampaignsCommand,
    ListRolesCommand,
    ListSecretTemplatesCommand,
    UpsertAppSecretsCommand,
)
from app.application.base import FlexibleCommand
from app.application.s2s.commands import S2SClickCommand
from app.application.sdk.entities import (
    GetSdkConfigCommand,
    SdkApplicationConfigurationCommand,
    SdkCreateAppCommand,
    SdkCreateAppPlatformCommand,
    SdkDeviceCommand,
    SdkEventCommand,
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
    SdkPushRegisterCommand,
)
from app.application.tracking.entities import TrackingRedirectCommand

CommandT = TypeVar("CommandT", bound=FlexibleCommand)

_FIXED_NOW = datetime(2026, 3, 12, 12, 0, tzinfo=UTC)
_FIXED_NOW_TEXT = _FIXED_NOW.isoformat().replace("+00:00", "Z")


def _merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    merged.update(overrides)
    return merged


def _build(
    command_type: type[CommandT],
    defaults: dict[str, Any],
    overrides: dict[str, Any],
) -> CommandT:
    return command_type.model_validate(_merge(defaults, overrides))


def _pagination_defaults() -> dict[str, Any]:
    return {
        "limit": 50,
        "offset": 0,
        "search": None,
    }


def build_sdk_device_command(**overrides: Any) -> SdkDeviceCommand:
    return _build(
        SdkDeviceCommand,
        {
            "os_name": "iOS",
            "os_version": "17.4",
            "device_brand": "Apple",
            "device_model": "iPhone 15",
            "app_version": "1.0.0",
            "sdk_version": "2.1.0",
        },
        overrides,
    )


def build_sdk_device(**overrides: Any) -> SdkDeviceCommand:
    return build_sdk_device_command(**overrides)


def build_sdk_install_command(**overrides: Any) -> SdkInstallCommand:
    return _build(
        SdkInstallCommand,
        {
            "install_key": "install-key-ios",
            "idempotency_key": "install-idempotency-1",
            "click_id": "click-1",
            "params": {"utm_source": "organic"},
            "device": build_sdk_device_command(),
        },
        overrides,
    )


def build_sdk_event_command(**overrides: Any) -> SdkEventCommand:
    return _build(
        SdkEventCommand,
        {
            "idempotency_key": "events-idempotency-1",
            "type": "metric",
            "key": "first_open",
            "event_time": _FIXED_NOW,
            "amount": None,
            "currency": None,
            "params": {"source": "sdk"},
        },
        overrides,
    )


def build_sdk_events_command(**overrides: Any) -> SdkEventsCommand:
    return _build(
        SdkEventsCommand,
        {
            "install_key": "install-key-ios",
            "click_id": "click-1",
            "idempotency_key": "events-idempotency-1",
            "events": [build_sdk_event_command()],
        },
        overrides,
    )


def build_sdk_params_update_command(**overrides: Any) -> SdkParamsUpdateCommand:
    return _build(
        SdkParamsUpdateCommand,
        {
            "click_id": "click-1",
            "idempotency_key": "params-idempotency-1",
            "params": {"campaign": "spring-launch"},
            "event_time": _FIXED_NOW,
        },
        overrides,
    )


def build_sdk_push_register_command(**overrides: Any) -> SdkPushRegisterCommand:
    return _build(
        SdkPushRegisterCommand,
        {
            "install_key": "install-key-ios",
            "token": "push-token-1",
            "provider": "apns",
            "click_id": "click-1",
            "crm_user_id": "crm-user-1",
            "idempotency_key": "push-register-1",
            "device": build_sdk_device_command(),
            "params": {"locale": "en"},
        },
        overrides,
    )


def build_get_sdk_config_command(**overrides: Any) -> GetSdkConfigCommand:
    return _build(
        GetSdkConfigCommand,
        {
            "install_key": "install-key-ios",
            "app_code": "test-app",
            "platform": "ios",
            "crm_user_id": "crm-user-1",
        },
        overrides,
    )


def build_sdk_create_app_command(**overrides: Any) -> SdkCreateAppCommand:
    return _build(
        SdkCreateAppCommand,
        {
            "id": 1,
            "name": "Test App",
            "code_slug": "test-app",
            "screanshots": {"0": "https://cdn.example.com/shot-1.png"},
            "logo_ur": "https://cdn.example.com/logo.png",
            "tech_description": "Technical description",
            "description": "Public description",
        },
        overrides,
    )


def build_sdk_create_app_platform_command(**overrides: Any) -> SdkCreateAppPlatformCommand:
    return _build(
        SdkCreateAppPlatformCommand,
        {
            "app_id": 1,
            "platform": "ios",
            "package_name": "com.example.test",
            "install_key": "install-key-ios",
            "store_url": "https://apps.example.com/test",
            "sdk_public_key": "sdk-public",
            "sdk_secret_hash": "sdk-secret-hash",
            "status": "active",
            "platform_id": 1,
            "created_at": _FIXED_NOW,
            "updated_at": _FIXED_NOW,
        },
        overrides,
    )


def build_sdk_application_configuration_command(
    **overrides: Any,
) -> SdkApplicationConfigurationCommand:
    return _build(
        SdkApplicationConfigurationCommand,
        {
            "app_id": 1,
            "platform": "ios",
        },
        overrides,
    )


def build_admin_list_apps_command(**overrides: Any) -> ListAppsCommand:
    return _build(ListAppsCommand, _pagination_defaults(), overrides)


def build_admin_create_app_command(**overrides: Any) -> CreateAppCommand:
    return _build(
        CreateAppCommand,
        {
            "code": "test-app",
            "name": "Test App",
            "description": "Admin managed application",
            "is_active": True,
        },
        overrides,
    )


def build_admin_list_app_platforms_command(**overrides: Any) -> ListAppPlatformsCommand:
    return _build(
        ListAppPlatformsCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
        },
        overrides,
    )


def build_admin_create_app_platform_command(**overrides: Any) -> CreateAppPlatformCommand:
    return _build(
        CreateAppPlatformCommand,
        {
            "app_id": 1,
            "platform": "ios",
            "install_key": "install-key-ios",
            "is_active": True,
        },
        overrides,
    )


def build_admin_list_metric_definitions_command(**overrides: Any) -> ListMetricDefinitionsCommand:
    return _build(ListMetricDefinitionsCommand, _pagination_defaults(), overrides)


def build_admin_create_metric_definition_command(
    **overrides: Any,
) -> CreateMetricDefinitionCommand:
    return _build(
        CreateMetricDefinitionCommand,
        {
            "key": "first_open",
            "name": "First Open",
            "description": "Application first open metric",
            "is_active": True,
        },
        overrides,
    )


def build_admin_list_conversion_definitions_command(
    **overrides: Any,
) -> ListConversionDefinitionsCommand:
    return _build(ListConversionDefinitionsCommand, _pagination_defaults(), overrides)


def build_admin_create_conversion_definition_command(
    **overrides: Any,
) -> CreateConversionDefinitionCommand:
    return _build(
        CreateConversionDefinitionCommand,
        {
            "key": "purchase",
            "name": "Purchase",
            "description": "In-app purchase conversion",
            "currency": "USD",
            "is_active": True,
        },
        overrides,
    )


def build_admin_list_param_definitions_command(**overrides: Any) -> ListParamDefinitionsCommand:
    return _build(ListParamDefinitionsCommand, _pagination_defaults(), overrides)


def build_admin_create_param_definition_command(
    **overrides: Any,
) -> CreateParamDefinitionCommand:
    return _build(
        CreateParamDefinitionCommand,
        {
            "key": "utm_source",
            "label": "UTM Source",
            "param_type": "string",
            "is_required": False,
        },
        overrides,
    )


def build_admin_list_secret_templates_command(
    **overrides: Any,
) -> ListSecretTemplatesCommand:
    return _build(ListSecretTemplatesCommand, _pagination_defaults(), overrides)


def build_admin_create_secret_template_command(
    **overrides: Any,
) -> CreateSecretTemplateCommand:
    return _build(
        CreateSecretTemplateCommand,
        {
            "key": "api_key",
            "name": "API Key",
            "secret_type": "text",
            "visibility": "global",
        },
        overrides,
    )


def build_admin_app_secret_value_command(**overrides: Any) -> AppSecretValueCommand:
    return _build(
        AppSecretValueCommand,
        {
            "key": "api_key",
            "value": "super-secret",
            "scope": "platform",
        },
        overrides,
    )


def build_admin_list_app_secrets_command(**overrides: Any) -> ListAppSecretsCommand:
    return _build(
        ListAppSecretsCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
        },
        overrides,
    )


def build_admin_upsert_app_secrets_command(**overrides: Any) -> UpsertAppSecretsCommand:
    return _build(
        UpsertAppSecretsCommand,
        {
            "app_id": 1,
            "platform_id": 1,
            "secrets": [build_admin_app_secret_value_command()],
        },
        overrides,
    )


def build_admin_list_postback_rules_command(
    **overrides: Any,
) -> ListPostbackRulesCommand:
    return _build(
        ListPostbackRulesCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
        },
        overrides,
    )


def build_admin_create_postback_rule_command(
    **overrides: Any,
) -> CreatePostbackRuleCommand:
    return _build(
        CreatePostbackRuleCommand,
        {
            "app_id": 1,
            "name": "Install Rule",
            "event_key": "install",
            "url": "https://example.com/postback",
            "is_active": True,
        },
        overrides,
    )


def build_admin_list_push_campaigns_command(
    **overrides: Any,
) -> ListPushCampaignsCommand:
    return _build(
        ListPushCampaignsCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
        },
        overrides,
    )


def build_admin_create_push_campaign_command(
    **overrides: Any,
) -> CreatePushCampaignCommand:
    return _build(
        CreatePushCampaignCommand,
        {
            "app_id": 1,
            "name": "Welcome Campaign",
            "title": "Hello",
            "body": "Welcome aboard",
            "scheduled_at": _FIXED_NOW_TEXT,
        },
        overrides,
    )


def build_admin_get_stats_command(**overrides: Any) -> GetStatsCommand:
    return _build(
        GetStatsCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
            "platform": "ios",
            "group_by": "day",
            "start_at": "2026-03-01T00:00:00Z",
            "end_at": "2026-03-12T00:00:00Z",
        },
        overrides,
    )


def build_admin_list_click_logs_command(**overrides: Any) -> ListClickLogsCommand:
    return _build(
        ListClickLogsCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
            "click_id": "click-1",
            "start_at": "2026-03-01T00:00:00Z",
            "end_at": "2026-03-12T00:00:00Z",
        },
        overrides,
    )


def build_admin_list_event_logs_command(**overrides: Any) -> ListEventLogsCommand:
    return _build(
        ListEventLogsCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
            "click_id": "click-1",
            "event_key": "first_open",
            "start_at": "2026-03-01T00:00:00Z",
            "end_at": "2026-03-12T00:00:00Z",
        },
        overrides,
    )


def build_admin_list_roles_command(**overrides: Any) -> ListRolesCommand:
    return _build(
        ListRolesCommand,
        {
            **_pagination_defaults(),
            "app_id": 1,
        },
        overrides,
    )


def build_admin_create_role_command(**overrides: Any) -> CreateRoleCommand:
    return _build(
        CreateRoleCommand,
        {
            "name": "manager",
            "description": "Manager role",
            "permissions": ["apps.view"],
            "app_ids": [1],
        },
        overrides,
    )


def build_admin_get_audit_log_command(**overrides: Any) -> GetAuditLogCommand:
    return _build(
        GetAuditLogCommand,
        {
            **_pagination_defaults(),
            "actor_id": 1,
            "entity_type": "app",
            "entity_id": 1,
            "start_at": "2026-03-01T00:00:00Z",
            "end_at": "2026-03-12T00:00:00Z",
        },
        overrides,
    )


def build_admin_command_preview(**overrides: Any) -> CommandPreview:
    return _build(
        CommandPreview,
        {
            "resource": "apps.create",
            "payload": {"name": "Test App"},
        },
        overrides,
    )


def build_s2s_click_command(**overrides: Any) -> S2SClickCommand:
    return _build(
        S2SClickCommand,
        {
            "app_code": "test-app",
            "platform": "ios",
            "idempotency_key": "s2s-click-1",
            "click_id": "click-1",
            "redirect_url": "https://example.com/landing",
            "ip": "203.0.113.10",
            "user_agent": "Mozilla/5.0",
            "params": {"campaign": "spring"},
        },
        overrides,
    )


def build_tracking_redirect_command(**overrides: Any) -> TrackingRedirectCommand:
    return _build(
        TrackingRedirectCommand,
        {
            "app_code": "test-app",
            "platform": "ios",
            "redirect_url": "https://example.com/landing",
            "idempotency_key": "tracking-redirect-1",
            "ip": "203.0.113.10",
            "user_agent": "Mozilla/5.0",
            "params": {"campaign": "spring"},
        },
        overrides,
    )
