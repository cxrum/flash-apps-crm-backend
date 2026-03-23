from __future__ import annotations

from pydantic import Field

from app.application.base import FlexibleCommand, JsonDict, PaginationCommand


class ListAppsCommand(PaginationCommand):
    pass


class CreateAppCommand(FlexibleCommand):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ListAppPlatformsCommand(PaginationCommand):
    app_id: int


class CreateAppPlatformCommand(FlexibleCommand):
    app_id: int
    platform: str | None = None
    install_key: str | None = None
    is_active: bool | None = None


class ListMetricDefinitionsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class CreateMetricDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    name: str
    description: str | None = None
    is_active: bool = True


class UpdateMetricDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    metric_definition_id: int
    key: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ListConversionDefinitionsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class CreateConversionDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    name: str
    description: str | None = None
    currency: str | None = None
    revenue_enabled: bool = True
    expects_amount: bool = True
    expects_currency: bool = True
    dedup_mode: str | None = None
    is_active: bool = True


class UpdateConversionDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    conversion_definition_id: int
    key: str | None = None
    name: str | None = None
    description: str | None = None
    revenue_enabled: bool | None = None
    expects_amount: bool | None = None
    expects_currency: bool | None = None
    dedup_mode: str | None = None


class ListParamDefinitionsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class CreateParamDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    label: str
    param_type: str
    description: str | None = None
    overwrite_policy: str | None = None
    is_active: bool | None = None
    visible_in_logs: bool | None = None
    visible_in_stats: bool | None = None
    filterable: bool | None = None
    groupable: bool | None = None
    is_required: bool | None = None


class UpdateParamDefinitionCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    param_definition_id: int
    key: str | None = None
    label: str | None = None
    param_type: str | None = None
    description: str | None = None
    overwrite_policy: str | None = None
    is_active: bool | None = None
    visible_in_logs: bool | None = None
    visible_in_stats: bool | None = None
    filterable: bool | None = None
    groupable: bool | None = None


class GetSecretTemplatesCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    template_id: int


class ListSecretTemplatesCommand(PaginationCommand):
    crm_user_id: int
    app_id: int


class CreateSecretTemplateCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    key: str
    name: str
    secret_type: str
    visibility: str

class UpdateSecretTemplateCommand(FlexibleCommand):
    crm_user_id: int
    template_id: int
    app_id: int
    key: str
    name: str
    secret_type: str
    visibility: str


class AppSecretValueCommand(FlexibleCommand):
    key: str | None = None
    value: str | None = None
    scope: str | None = None


class ListAppSecretsCommand(PaginationCommand):
    crm_user_id: int
    app_id: int
    platform_id: int | None = None


class CreateAppSecretCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    secret_template_id: int
    value: str
    platform_id: int | None = None
    active_flag: bool = True
    version: float = 1


class GetAppSecretValueCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    app_secret_id: int


class UpdateAppSecretCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    secret_id: int
    value: str | None = None
    platform_id: int | None = None
    active_flag: bool | None = None
    version: float | None = None


class UpsertAppSecretsCommand(FlexibleCommand):
    crm_user_id: int
    app_id: int
    platform_id: int | None = None
    secrets: list[AppSecretValueCommand] = Field(default_factory=list)


class ListPostbackRulesCommand(PaginationCommand):
    app_id: int | None = None


class CreatePostbackRuleCommand(FlexibleCommand):
    app_id: int 
    platform_app_id: int | None = None
    name: str
    trigger_type: str
    event_key: str | None = None
    url: str
    http_method: str
    headers: JsonDict
    auth_params: JsonDict
    timeout: int
    retry_policy: JsonDict
    is_active: bool = False
    tempalte: JsonDict = Field(default_factory=JsonDict)

class EvaluatePostbackRuleCommand(FlexibleCommand):
    event_id: str
    trigger_type: str
    event_key: str | None = None
    
class ExecutePostbackRuleCommand(FlexibleCommand):
    postback_rule_id: int
    event_id: str
    istall_id: int | None = None

class ListPushCampaignsCommand(PaginationCommand):
    app_id: int | None = None


class CreatePushCampaignCommand(FlexibleCommand):
    app_id: int | None = None
    name: str | None = None
    title: str | None = None
    body: str | None = None
    scheduled_at: str | None = None


class GetStatsCommand(PaginationCommand):
    app_id: int | None = None
    platform: str | None = None
    group_by: str | None = None
    start_at: str | None = None
    end_at: str | None = None


class ListClickLogsCommand(PaginationCommand):
    app_id: int | None = None
    click_id: str | None = None
    start_at: str | None = None
    end_at: str | None = None


class ListEventLogsCommand(PaginationCommand):
    app_id: int | None = None
    click_id: str | None = None
    event_key: str | None = None
    start_at: str | None = None
    end_at: str | None = None


class ListRolesCommand(PaginationCommand):
    app_id: int | None = None


class CreateRoleCommand(FlexibleCommand):
    name: str | None = None
    description: str | None = None
    permissions: list[str] = Field(default_factory=list)
    app_ids: list[int] = Field(default_factory=list)


class GetAuditLogCommand(PaginationCommand):
    actor_id: int | None = None
    entity_type: str | None = None
    entity_id: int | None = None
    start_at: str | None = None
    end_at: str | None = None


class CommandPreview(FlexibleCommand):
    resource: str
    payload: JsonDict = Field(default_factory=dict)
