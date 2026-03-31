from pydantic import Field

from app.application.base import FlexibleCommand, JsonDict, PaginationCommand


class ListPostbackRulesCommand(PaginationCommand):
    crm_user_id: int
    app_id: int | None = None

class GetPostbackRuleCommand(FlexibleCommand):
    crm_user_id: int
    postback_id: int
    app_id: int | None = None

class CreatePostbackRuleCommand(FlexibleCommand):
    crm_user_id: int
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
    template: JsonDict = Field(default_factory=JsonDict)

class UpdatePostbackRuleCommand(FlexibleCommand):
    crm_user_id: int
    postback_id: int
    app_id: int | None = None
    platform_app_id: int | None = None
    name: str | None = None
    trigger_type: str | None = None
    event_key: str | None = None
    url: str | None = None
    http_method: str | None = None
    headers: JsonDict | None = None
    auth_params: JsonDict | None = None
    timeout: int | None = None
    retry_policy: JsonDict | None = None
    is_active: bool | None = None
    template: JsonDict | None = None

class DeletePostbackRuleCommand(FlexibleCommand):
    crm_user_id: int
    postback_id: int
    app_id: int | None = None

class EvaluatePostbackRuleCommand(FlexibleCommand):
    event_id: str
    trigger_type: str
    event_key: str | None = None

class ExecutePostbackRuleCommand(FlexibleCommand):
    postback_rule_id: int
    event_id: str
    install_id: int | None = None