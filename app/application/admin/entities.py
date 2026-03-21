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
    pass


class CreateMetricDefinitionCommand(FlexibleCommand):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ListConversionDefinitionsCommand(PaginationCommand):
    pass


class CreateConversionDefinitionCommand(FlexibleCommand):
    key: str | None = None
    name: str | None = None
    description: str | None = None
    currency: str | None = None
    is_active: bool | None = None


class ListParamDefinitionsCommand(PaginationCommand):
    pass


class CreateParamDefinitionCommand(FlexibleCommand):
    key: str | None = None
    label: str | None = None
    param_type: str | None = None
    is_required: bool | None = None


class ListSecretTemplatesCommand(PaginationCommand):
    pass


class CreateSecretTemplateCommand(FlexibleCommand):
    key: str | None = None
    name: str | None = None
    secret_type: str | None = None
    visibility: str | None = None


class AppSecretValueCommand(FlexibleCommand):
    key: str | None = None
    value: str | None = None
    scope: str | None = None


class ListAppSecretsCommand(PaginationCommand):
    app_id: int


class UpsertAppSecretsCommand(FlexibleCommand):
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
