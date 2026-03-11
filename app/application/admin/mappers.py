from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel

from app.application.admin.entities import (
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

TCommand = TypeVar("TCommand", bound=BaseModel)


class AdminCommandMapper:
    @staticmethod
    def _to_command(command_type: type[TCommand], payload: Mapping[str, object]) -> TCommand:
        return command_type.model_validate(dict(payload))

    @classmethod
    def list_apps_from_transport(cls, payload: Mapping[str, object]) -> ListAppsCommand:
        return cls._to_command(ListAppsCommand, payload)

    @classmethod
    def create_app_from_transport(cls, payload: Mapping[str, object]) -> CreateAppCommand:
        return cls._to_command(CreateAppCommand, payload)

    @classmethod
    def list_app_platforms_from_transport(cls, payload: Mapping[str, object]) -> ListAppPlatformsCommand:
        return cls._to_command(ListAppPlatformsCommand, payload)

    @classmethod
    def create_app_platform_from_transport(cls, payload: Mapping[str, object]) -> CreateAppPlatformCommand:
        return cls._to_command(CreateAppPlatformCommand, payload)

    @classmethod
    def list_metrics_from_transport(cls, payload: Mapping[str, object]) -> ListMetricDefinitionsCommand:
        return cls._to_command(ListMetricDefinitionsCommand, payload)

    @classmethod
    def create_metric_from_transport(cls, payload: Mapping[str, object]) -> CreateMetricDefinitionCommand:
        return cls._to_command(CreateMetricDefinitionCommand, payload)

    @classmethod
    def list_conversions_from_transport(cls, payload: Mapping[str, object]) -> ListConversionDefinitionsCommand:
        return cls._to_command(ListConversionDefinitionsCommand, payload)

    @classmethod
    def create_conversion_from_transport(cls, payload: Mapping[str, object]) -> CreateConversionDefinitionCommand:
        return cls._to_command(CreateConversionDefinitionCommand, payload)

    @classmethod
    def list_params_from_transport(cls, payload: Mapping[str, object]) -> ListParamDefinitionsCommand:
        return cls._to_command(ListParamDefinitionsCommand, payload)

    @classmethod
    def create_param_from_transport(cls, payload: Mapping[str, object]) -> CreateParamDefinitionCommand:
        return cls._to_command(CreateParamDefinitionCommand, payload)

    @classmethod
    def list_secret_templates_from_transport(cls, payload: Mapping[str, object]) -> ListSecretTemplatesCommand:
        return cls._to_command(ListSecretTemplatesCommand, payload)

    @classmethod
    def create_secret_template_from_transport(cls, payload: Mapping[str, object]) -> CreateSecretTemplateCommand:
        return cls._to_command(CreateSecretTemplateCommand, payload)

    @classmethod
    def list_app_secrets_from_transport(cls, payload: Mapping[str, object]) -> ListAppSecretsCommand:
        return cls._to_command(ListAppSecretsCommand, payload)

    @classmethod
    def upsert_app_secrets_from_transport(cls, payload: Mapping[str, object]) -> UpsertAppSecretsCommand:
        return cls._to_command(UpsertAppSecretsCommand, payload)

    @classmethod
    def list_postbacks_from_transport(cls, payload: Mapping[str, object]) -> ListPostbackRulesCommand:
        return cls._to_command(ListPostbackRulesCommand, payload)

    @classmethod
    def create_postback_from_transport(cls, payload: Mapping[str, object]) -> CreatePostbackRuleCommand:
        return cls._to_command(CreatePostbackRuleCommand, payload)

    @classmethod
    def list_push_campaigns_from_transport(cls, payload: Mapping[str, object]) -> ListPushCampaignsCommand:
        return cls._to_command(ListPushCampaignsCommand, payload)

    @classmethod
    def create_push_campaign_from_transport(cls, payload: Mapping[str, object]) -> CreatePushCampaignCommand:
        return cls._to_command(CreatePushCampaignCommand, payload)

    @classmethod
    def stats_from_transport(cls, payload: Mapping[str, object]) -> GetStatsCommand:
        return cls._to_command(GetStatsCommand, payload)

    @classmethod
    def click_logs_from_transport(cls, payload: Mapping[str, object]) -> ListClickLogsCommand:
        return cls._to_command(ListClickLogsCommand, payload)

    @classmethod
    def event_logs_from_transport(cls, payload: Mapping[str, object]) -> ListEventLogsCommand:
        return cls._to_command(ListEventLogsCommand, payload)

    @classmethod
    def list_roles_from_transport(cls, payload: Mapping[str, object]) -> ListRolesCommand:
        return cls._to_command(ListRolesCommand, payload)

    @classmethod
    def create_role_from_transport(cls, payload: Mapping[str, object]) -> CreateRoleCommand:
        return cls._to_command(CreateRoleCommand, payload)

    @classmethod
    def audit_log_from_transport(cls, payload: Mapping[str, object]) -> GetAuditLogCommand:
        return cls._to_command(GetAuditLogCommand, payload)
