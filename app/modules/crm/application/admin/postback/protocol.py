from typing import Protocol

from app.modules.crm.application.admin.postback.commands import (
    CreatePostbackRuleCommand,
    DeletePostbackRuleCommand,
    EvaluatePostbackRuleCommand,
    ExecutePostbackRuleCommand,
    GetPostbackRuleCommand,
    ListPostbackRulesCommand,
    UpdatePostbackRuleCommand,
)
from app.modules.crm.application.admin.postback.responses import (
    CreatePostbackResponse,
    DeletePostbackResponse,
    GetPostbackResponse,
    ListPostbackResponse,
)
from app.modules.crm.application.base import JsonDict
from app.modules.crm.domain.postback_rule import CrmPostbackRuleEntity
from app.modules.crm.domain.postback_rule.template import PostbackTemplateEntity
from app.modules.crm.domain.uow import UnitOfWorkProtocol


class PostbackServiceProtocol(Protocol):
    def create_postback(
        self,
        command: CreatePostbackRuleCommand,
    ) -> CreatePostbackResponse: ...

    def evaluate(
        self,
        command: EvaluatePostbackRuleCommand,
    ) -> list[CrmPostbackRuleEntity]: ...

    @staticmethod
    def build_params(
        uow: UnitOfWorkProtocol,
        template: PostbackTemplateEntity,
        event_id: str,
    ) -> JsonDict: ...

    @staticmethod
    def build_auth_params(
        uow: UnitOfWorkProtocol,
        auth_param: dict[str, str],
        *,
        platform_id: int,
    ) -> JsonDict: ...

    async def execute(self, command: ExecutePostbackRuleCommand) -> None: ...

    def get_list_postbacks(
        self,
        command: ListPostbackRulesCommand,
    ) -> ListPostbackResponse: ...

    def get_postback(self, command: GetPostbackRuleCommand) -> GetPostbackResponse: ...

    def update_postback(
        self,
        command: UpdatePostbackRuleCommand,
    ) -> CreatePostbackResponse: ...

    def delete_postback(
        self,
        command: DeletePostbackRuleCommand,
    ) -> DeletePostbackResponse: ...
