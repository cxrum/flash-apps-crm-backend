from __future__ import annotations

from collections.abc import Callable
from types import TracebackType

from sqlalchemy.orm import Session

from app.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.domain.current_param.current_param_repository_protocol import CrmCurrentParamRepositoryProtocol
from app.domain.events.event_repository_protocol import CrmEventRepositoryProtocol
from app.domain.install.install_repository_protocol import CrmInstallRepositoryProtocol
from app.domain.metric_definition.metric_definition_repository_protocol import CrmMetricDefinitionRepositoryProtocol
from app.domain.param_definition.param_definition_repository_protocol import CrmParamDefinitionRepositoryProtocol
from app.domain.permission.permission_repository_protocol import CrmPermissionRepositoryProtocol
from app.domain.postback_rule.postback_rule_repository_protocol import CrmPostbackRuleRepositoryProtocol
from app.domain.push_campaign.push_campaign_repository_protocol import CrmPushCampaignRepositoryProtocol
from app.domain.push_event.push_event_repository_protocol import CrmPushEventRepositoryProtocol
from app.domain.push_token.push_token_repository_protocol import CrmPushTokenRepositoryProtocol
from app.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.domain.role_permission.role_permission_repository_protocol import CrmRolePermissionRepositoryProtocol
from app.domain.secret_template.secret_template_repository_protocol import CrmSecretTemplateRepositoryProtocol
from app.domain.uow import CrmUnitOfWorkProtocol
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_app_access.user_app_access_repository_protocol import CrmUserAppAccessRepositoryProtocol
from app.domain.user_role.user_role_repository_protocol import CrmUserRoleRepositoryProtocol
from app.infra.db.repositories.factory import CrmSqlAlchemyRepositoryFactory


class SqlAlchemyUnitOfWork(CrmUnitOfWorkProtocol):
    app_repo: CrmAppRepositoryProtocol
    app_platform_repo: CrmAppPlatformRepositoryProtocol
    user_repo: CrmUserRepositoryProtocol
    role_repo: CrmRoleRepositoryProtocol
    permission_repo: CrmPermissionRepositoryProtocol
    role_permission_repo: CrmRolePermissionRepositoryProtocol
    user_role_repo: CrmUserRoleRepositoryProtocol
    user_app_access_repo: CrmUserAppAccessRepositoryProtocol
    click_repo: CrmClickRepositoryProtocol
    app_user_repo: CrmAppUserRepositoryProtocol
    install_repo: CrmInstallRepositoryProtocol
    event_repo: CrmEventRepositoryProtocol
    current_param_repo: CrmCurrentParamRepositoryProtocol
    metric_definition_repo: CrmMetricDefinitionRepositoryProtocol
    conversion_definition_repo: CrmConversionDefinitionRepositoryProtocol
    secret_template_repo: CrmSecretTemplateRepositoryProtocol
    app_secret_repo: CrmAppSecretRepositoryProtocol
    param_definition_repo: CrmParamDefinitionRepositoryProtocol
    postback_rule_repo: CrmPostbackRuleRepositoryProtocol
    push_campaign_repo: CrmPushCampaignRepositoryProtocol
    push_token_repo: CrmPushTokenRepositoryProtocol
    push_event_repo: CrmPushEventRepositoryProtocol
    audit_log_repo: CrmAuditLogRepositoryProtocol

    def __init__(
        self,
        session_factory: Callable[[], Session],
        repository_factory: CrmSqlAlchemyRepositoryFactory | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._repository_factory = repository_factory or CrmSqlAlchemyRepositoryFactory()
        self.session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.app_repo = self._repository_factory.app_repo(self.session)
        self.app_platform_repo = self._repository_factory.app_platform_repo(self.session)
        self.user_repo = self._repository_factory.user_repo(self.session)
        self.role_repo = self._repository_factory.role_repo(self.session)
        self.permission_repo = self._repository_factory.permission_repo(self.session)
        self.role_permission_repo = self._repository_factory.role_permission_repo(self.session)
        self.user_role_repo = self._repository_factory.user_role_repo(self.session)
        self.user_app_access_repo = self._repository_factory.user_app_access_repo(self.session)
        self.click_repo = self._repository_factory.click_repo(self.session)
        self.app_user_repo = self._repository_factory.app_user_repo(self.session)
        self.install_repo = self._repository_factory.install_repo(self.session)
        self.event_repo = self._repository_factory.event_repo(self.session)
        self.current_param_repo = self._repository_factory.current_param_repo(self.session)
        self.metric_definition_repo = self._repository_factory.metric_definition_repo(self.session)
        self.conversion_definition_repo = self._repository_factory.conversion_definition_repo(self.session)
        self.secret_template_repo = self._repository_factory.secret_template_repo(self.session)
        self.app_secret_repo = self._repository_factory.app_secret_repo(self.session)
        self.param_definition_repo = self._repository_factory.param_definition_repo(self.session)
        self.postback_rule_repo = self._repository_factory.postback_rule_repo(self.session)
        self.push_campaign_repo = self._repository_factory.push_campaign_repo(self.session)
        self.push_token_repo = self._repository_factory.push_token_repo(self.session)
        self.push_event_repo = self._repository_factory.push_event_repo(self.session)
        self.audit_log_repo = self._repository_factory.audit_log_repo(self.session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.session is not None:
                self.session.close()
                self.session = None

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW session is not started")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW session is not started")
        self.session.rollback()
