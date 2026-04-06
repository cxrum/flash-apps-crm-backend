from __future__ import annotations

from typing import Any, ClassVar, Protocol

from app.application.admin.crm_authorization.service import CrmAuthorizationService
from app.application.admin.exception import ClickNotFound, EventNotFound
from app.application.admin.postback.exception import PostbackAppMismatch, PostbackNotFound, PostbackPlatformNotFound, RuleNotFound, SecretNotFound, TemplateNotFound
from app.application.admin.postback.mappers import PostbackCommandsMapper
from app.application.admin.postback.commands import (
    DeletePostbackRuleCommand,
    ExecutePostbackRuleCommand,
    GetPostbackRuleCommand,
    ListPostbackRulesCommand,
    UpdatePostbackRuleCommand,
)
from app.application.admin.postback.commands import CreatePostbackRuleCommand, EvaluatePostbackRuleCommand
from app.application.base import JsonDict
from app.application.contracts.requester import S2SRequesterProtocol
from app.application.admin.postback.responses import (
    CreatePostbackResponse,
    DeletePostbackResponse,
    GetPostbackResponse,
    ListPostbackResponse,
)
from app.application.mapper import PaginationMapper
from app.domain.pagination import Pagination
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.event_bus.service_protocol import IAsyncEventBus
from app.domain.postback_rule import CrmPostbackRuleEntity
from app.domain.postback_rule.template import PostbackTemplateEntity
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol


class TemplateParamResolverProtocol(Protocol):
    def resolve(self, uow: UnitOfWorkProtocol, key: str, event_id: str) -> Any | None: ...


class _CurrentTemplateParam(TemplateParamResolverProtocol):
    def resolve(self, uow: UnitOfWorkProtocol, key: str, event_id: str) -> Any | None:
        event = uow.event_repo.get_by_id(event_id)
        if event is None:
            return None

        current = uow.current_param_repo.get_by_click_and_key(event.click_id, key)
        if current is None:
            return None

        raw_value = current.current_value()

        click = uow.click_repo.get_by_id(event.click_id)
        if click is None:
            return raw_value

        platform = uow.app_platform_repo.get_by_id(click.app_platform_id)
        if platform is None:
            return raw_value

        definition = next(
            (
                item
                for item in uow.param_definition_repo.list_by_app_id(platform.app_id)
                if item.machine_key == key
            ),
            None,
        )
        if definition is None:
            return raw_value

        return definition.get_param_value({key: raw_value})


class _SnapshotTemplateParam(TemplateParamResolverProtocol):
    def resolve(self, uow: UnitOfWorkProtocol, key: str, event_id: str) -> Any | None:
        event = uow.event_repo.get_by_id(event_id)
        if event is None:
            return None

        return event.payload.get(key)


class _FallbackTemplateParam(TemplateParamResolverProtocol):
    def resolve(self, uow: UnitOfWorkProtocol, key: str, event_id: str) -> Any | None:
        event = uow.event_repo.get_by_id(event_id)
        if event is None:
            return None

        click = uow.click_repo.get_by_id(event.click_id)
        if click is None:
            return None

        platform = uow.app_platform_repo.get_by_id(click.app_platform_id)
        if platform is None:
            return None

        if key == "click_id":
            return event.click_id
        if key == "user_id":
            install = uow.install_repo.get_by_click_id(click.click_id)
            return None if install is None else install.app_user_id
        if key == "app_code":
            app = uow.app_repo.get_by_id(platform.app_id)
            return None if app is None else app.code_slug
        if key == "platform":
            return platform.platform
        if key == "timestamp":
            return event.event_time_utc
        if key == "amount_usd":
            return event.amount_usd
        if key == "raw_amount":
            return event.amount
        if key == "geo":
            return event.geo()
        if key == "ip":
            return event.ip()
        if key == "ua":
            return event.ua()
        return None


class TemplateResolverFactory:
    _strategies: ClassVar[dict[str, TemplateParamResolverProtocol]] = {
        "current": _CurrentTemplateParam(),
        "snapshot": _SnapshotTemplateParam(),
    }

    def from_value(self, value: str) -> tuple[TemplateParamResolverProtocol, str]:
        splitted = value.split(".", 1)
        if len(splitted) == 2 and splitted[0] in self._strategies:
            return self._strategies[splitted[0]], splitted[1]
        return _FallbackTemplateParam(), value


class PostbackService:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactoryProtocol,
        async_event_bus: IAsyncEventBus,
        s2s_requester: S2SRequesterProtocol,
        authorization_service: CrmAuthorizationService | None = None,
    ) -> None:
        self._uow_factory = uow_factory
        self._async_event_bus = async_event_bus
        self._s2s_requester = s2s_requester
        self._authorization_service = authorization_service

    def _check_user_app_access(
        self,
        *,
        crm_user_id: int,
        app_id: int | None,
    ) -> None:
        if self._authorization_service is None or app_id is None:
            return

        self._authorization_service.has_user_app_access(
            crm_user_id=crm_user_id,
            app_id=app_id,
        )

    @staticmethod
    def _get_postback_rule(
        uow: UnitOfWorkProtocol,
        *,
        postback_id: int,
        app_id: int | None = None,
    ) -> CrmPostbackRuleEntity:
        postback = uow.postback_rule_repo.get_by_id(postback_id)
        if postback is None:
            raise PostbackNotFound(postback_id)

        if app_id is not None:
            platform = uow.app_platform_repo.get_by_id(postback.platform_app_id)
            if platform is None or platform.app_id != app_id:
                raise PostbackAppMismatch(app_id)

        return postback


    @staticmethod
    def _latest_secrets_by_template(
        secrets: list[CrmAppSecretEntity],
    ) -> dict[int, CrmAppSecretEntity]:
        latest_by_template: dict[int, CrmAppSecretEntity] = {}
        for secret in secrets:
            current = latest_by_template.get(secret.template_id)
            if current is None or secret.version > current.version:
                latest_by_template[secret.template_id] = secret
        return latest_by_template

    def create_postback(self, command: CreatePostbackRuleCommand) -> CreatePostbackResponse:
        self._check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            if command.platform_app_id is None:
                platforms = uow.app_platform_repo.list_by_app_id(command.app_id)
            else:
                platforms = [uow.app_platform_repo.get_by_id(command.platform_app_id)]

            if len(platforms) == 0:
                raise PostbackPlatformNotFound()

            secrets = uow.secret_template_repo.list_all()
            secret_codes = [i.code for i in secrets]

            postback_rules: list[CrmPostbackRuleEntity] = []
            for platform in platforms:
                if platform is None or platform.platform_id is None:
                    raise PostbackPlatformNotFound()

                postback_rule = CrmPostbackRuleEntity(
                    platform_app_id=platform.platform_id,
                    name=command.name,
                    endpoint_url=command.url,
                    trigger_type=command.trigger_type,
                    http_method=command.http_method,
                    headers=command.headers,
                    event_key=command.event_key,
                    auth_params=command.auth_params,
                    timeout=command.timeout,
                    retry_policy=command.retry_policy,
                    is_active=command.is_active,
                )

                postback_rule.template.set_payload(command.template)
                postback_rule.validate_url()
                postback_rule.validate_http_method()
                postback_rule.validate_secrets(secret_codes)
                postback_rules.append(postback_rule)

            saved_rules = uow.postback_rule_repo.save_many(postback_rules)

        return CreatePostbackResponse(
            postback=PostbackCommandsMapper.postback_domain_to_value(saved_rules[0])
        )

    def evaluate(self, command: EvaluatePostbackRuleCommand) -> list[CrmPostbackRuleEntity]:
        with self._uow_factory.create() as uow:
            event = uow.event_repo.get_by_id(command.event_id)
            if event is None:
                raise EventNotFound(command.event_id)

            click = uow.click_repo.get_by_id(event.click_id)
            
            if click is None:
                raise ClickNotFound(event.click_id)

            postback_rules = uow.postback_rule_repo.list_by_filters(
                platform_app_id=click.app_platform_id,
                trigger_type=command.trigger_type,
                event_key=command.event_key,
            )

        return postback_rules

    @staticmethod
    def build_params(
        uow: UnitOfWorkProtocol,
        template: PostbackTemplateEntity,
        event_id: str,
    ) -> JsonDict:
        params: JsonDict = {}

        for key, value in template.normalized().items():
            resolver, resolved_key = TemplateResolverFactory().from_value(value)
            params[key] = resolver.resolve(uow, resolved_key, event_id)

        return params

    @staticmethod
    def build_auth_params(
        uow: UnitOfWorkProtocol,
        auth_param: dict[str, str],
        *,
        platform_id: int,
    ) -> JsonDict:
        platform = uow.app_platform_repo.get_by_id(platform_id)
        if platform is None:
            raise PostbackPlatformNotFound()

        latest_secrets = PostbackService._latest_secrets_by_template(
            uow.app_secret_repo.list_active_by_app(platform.app_id, platform_id=platform_id)
        )

        unmasked_auth_params: JsonDict = {}
        for key, value in auth_param.items():
            template = uow.secret_template_repo.get_by_code(value)
            
            if template is None or template.template_id is None:
                raise TemplateNotFound(value)

            secret = latest_secrets.get(template.template_id)
            if secret is None:
                raise SecretNotFound(value)

            unmasked_auth_params[key] = secret.encrypted_value

        return unmasked_auth_params

    async def execute(self, command: ExecutePostbackRuleCommand) -> None:
        with self._uow_factory.create() as uow:
            rule = uow.postback_rule_repo.get_by_id(command.postback_rule_id)
            if rule is None:
                raise RuleNotFound(command.postback_rule_id)

            unmasked_auth_params = self.build_auth_params(
                uow,
                rule.auth_params,
                platform_id=rule.platform_app_id,
            )
            params = self.build_params(uow, rule.template, command.event_id)

            await self._s2s_requester.postback(
                url=rule.endpoint_url,
                http_method=rule.http_method,
                header=rule.headers,
                params=params,
                auth=unmasked_auth_params,
            )

    def get_list_postbacks(
        self,
        command: ListPostbackRulesCommand
    ) -> ListPostbackResponse:
        self._check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            if command.app_id is None:
                postbacks = uow.postback_rule_repo.list_by_filters(
                    pagination=PaginationMapper.pagination_from_command(command),
                )
            else:
                postbacks = uow.postback_rule_repo.list_by_app_id(
                    command.app_id,
                    pagination=PaginationMapper.pagination_from_command(command),
                )

        return ListPostbackResponse(
            postbacks=[PostbackCommandsMapper.postback_domain_to_value(it) for it in postbacks]
        )
    
    def get_postback(
        self,
        command: GetPostbackRuleCommand
    ) -> GetPostbackResponse:
        self._check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            postback = self._get_postback_rule(
                uow,
                postback_id=command.postback_id,
                app_id=command.app_id,
            )

        return GetPostbackResponse(
            postback=PostbackCommandsMapper.postback_domain_to_value(postback)
        )
    
    def update_postback(
        self,
        command: UpdatePostbackRuleCommand
    ) -> CreatePostbackResponse:
        self._check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            postback = self._get_postback_rule(
                uow,
                postback_id=command.postback_id,
                app_id=command.app_id,
            )

            platform_app_id: int | None = None
            
            if command.platform_app_id is not None:
                platform = uow.app_platform_repo.get_by_id(command.platform_app_id)
                
                if platform is None or platform.platform_id is None:
                    raise PostbackPlatformNotFound()
                
                if command.app_id is not None and platform.app_id != command.app_id:
                    raise PostbackAppMismatch(command.app_id)
                
                platform_app_id = platform.platform_id

            template: PostbackTemplateEntity | None = None
            
            if command.template is not None:
                template = PostbackTemplateEntity.from_dict(command.template)

            postback.update(
                platform_app_id=platform_app_id,
                name=command.name,
                endpoint_url=command.url,
                trigger_type=command.trigger_type,
                http_method=command.http_method,
                headers=command.headers,
                auth_params=command.auth_params,
                timeout=command.timeout,
                template=template,
                retry_policy=command.retry_policy,
                is_active=command.is_active,
            )
            
            secrets = uow.secret_template_repo.list_all()
            secret_codes = [item.code for item in secrets]

            postback.validate_url()
            postback.validate_http_method()
            postback.validate_secrets(secret_codes)
            postback.validate_event_key()

            saved_postback = uow.postback_rule_repo.save(postback)

        return CreatePostbackResponse(
            postback=PostbackCommandsMapper.postback_domain_to_value(saved_postback)
        )
    
    def delete_postback(
        self,
        command: DeletePostbackRuleCommand
    ) -> DeletePostbackResponse:
        self._check_user_app_access(crm_user_id=command.crm_user_id, app_id=command.app_id)

        with self._uow_factory.create() as uow:
            postback = self._get_postback_rule(
                uow,
                postback_id=command.postback_id,
                app_id=command.app_id,
            )
            
            if postback.rule_id is None:
                raise PostbackNotFound()
            
            deleted_postback = uow.postback_rule_repo.delete(postback.rule_id)

        return DeletePostbackResponse(
            postback=PostbackCommandsMapper.postback_domain_to_value(deleted_postback)
        )
