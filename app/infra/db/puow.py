from __future__ import annotations

from collections.abc import Callable, Generator
from types import TracebackType
from typing import Any

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
from app.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
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
from app.domain.secret_template.secret_template_repository_protocol import CrmSecretTemplateRepositoryProtocol
from app.domain.statistics_aggregate.statistics_aggregate_repository_protocol import StatisticsRepositoryProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_app_access.user_app_access_repository_protocol import CrmUserAppAccessRepositoryProtocol
from app.domain.user_permissions.user_permissions_repository_protocol import CrmUserPermissionsRepositoryProtocol
from app.infra.db.repositories.factory import CrmSqlAlchemyRepositoryFactory
from app.infra.db.session import SessionFactory

#FIXME: Temporary decision. Divide this class to smaller ones for each application service. 

class SqlAlchemyUnitOfWork(UnitOfWorkProtocol):
    app_repo: CrmAppRepositoryProtocol
    app_platform_repo: CrmAppPlatformRepositoryProtocol
    user_repo: CrmUserRepositoryProtocol
    role_repo: CrmRoleRepositoryProtocol
    permission_repo: CrmPermissionRepositoryProtocol
    user_permissions_repo: CrmUserPermissionsRepositoryProtocol
    user_app_access_repo: CrmUserAppAccessRepositoryProtocol
    click_repo: CrmClickRepositoryProtocol
    app_user_repo: CrmAppUserRepositoryProtocol
    install_repo: CrmInstallRepositoryProtocol
    event_repo: CrmEventRepositoryProtocol
    current_param_repo: CrmCurrentParamRepositoryProtocol
    statistics_repo: StatisticsRepositoryProtocol
    custom_params_statistics_repo: CustomParamsStatisticsRepositoryProtocol
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
        self.user_permissions_repo = self._repository_factory.user_permissions_repo(self.session)
        self.user_app_access_repo = self._repository_factory.user_app_access_repo(self.session)
        self.click_repo = self._repository_factory.click_repo(self.session)
        self.app_user_repo = self._repository_factory.app_user_repo(self.session)
        self.install_repo = self._repository_factory.install_repo(self.session)
        self.event_repo = self._repository_factory.event_repo(self.session)
        self.current_param_repo = self._repository_factory.current_param_repo(self.session)
        self.statistics_repo = self._repository_factory.statistics_repo(self.session)
        self.custom_params_statistics_repo = self._repository_factory.custom_params_statistics_repo(self.session)
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


class SqlAlchemyUnitOfWorkFactory(UnitOfWorkFactoryProtocol):
    
    def __init__(self, sesion_factory: Callable[[], Session]) -> None:
        self.__sesion_facoty = sesion_factory
    
    def create(self, *args: Any, **kwds: Any) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(self.__sesion_facoty)
