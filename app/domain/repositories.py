from __future__ import annotations

from typing import Protocol

from sqlalchemy.orm import Session

from app.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.domain.conversion_definition.conversion_definition_repository_protocol import CrmConversionDefinitionRepositoryProtocol
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
from app.domain.role_permission.role_permission_repository_protocol import CrmRolePermissionRepositoryProtocol
from app.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.domain.secret_template.secret_template_repository_protocol import CrmSecretTemplateRepositoryProtocol
from app.domain.user_app_access.user_app_access_repository_protocol import CrmUserAppAccessRepositoryProtocol
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_role.user_role_repository_protocol import CrmUserRoleRepositoryProtocol


class CrmRepositoryFactoryProtocol(Protocol):
    def app_repo(self, session: Session) -> CrmAppRepositoryProtocol: ...
    def app_platform_repo(self, session: Session) -> CrmAppPlatformRepositoryProtocol: ...
    def user_repo(self, session: Session) -> CrmUserRepositoryProtocol: ...
    def role_repo(self, session: Session) -> CrmRoleRepositoryProtocol: ...
    def permission_repo(self, session: Session) -> CrmPermissionRepositoryProtocol: ...
    def role_permission_repo(self, session: Session) -> CrmRolePermissionRepositoryProtocol: ...
    def user_role_repo(self, session: Session) -> CrmUserRoleRepositoryProtocol: ...
    def user_app_access_repo(self, session: Session) -> CrmUserAppAccessRepositoryProtocol: ...
    def click_repo(self, session: Session) -> CrmClickRepositoryProtocol: ...
    def app_user_repo(self, session: Session) -> CrmAppUserRepositoryProtocol: ...
    def install_repo(self, session: Session) -> CrmInstallRepositoryProtocol: ...
    def event_repo(self, session: Session) -> CrmEventRepositoryProtocol: ...
    def current_param_repo(self, session: Session) -> CrmCurrentParamRepositoryProtocol: ...
    def metric_definition_repo(self, session: Session) -> CrmMetricDefinitionRepositoryProtocol: ...
    def conversion_definition_repo(self, session: Session) -> CrmConversionDefinitionRepositoryProtocol: ...
    def secret_template_repo(self, session: Session) -> CrmSecretTemplateRepositoryProtocol: ...
    def app_secret_repo(self, session: Session) -> CrmAppSecretRepositoryProtocol: ...
    def param_definition_repo(self, session: Session) -> CrmParamDefinitionRepositoryProtocol: ...
    def postback_rule_repo(self, session: Session) -> CrmPostbackRuleRepositoryProtocol: ...
    def push_campaign_repo(self, session: Session) -> CrmPushCampaignRepositoryProtocol: ...
    def push_token_repo(self, session: Session) -> CrmPushTokenRepositoryProtocol: ...
    def push_event_repo(self, session: Session) -> CrmPushEventRepositoryProtocol: ...
    def audit_log_repo(self, session: Session) -> CrmAuditLogRepositoryProtocol: ...


__all__ = [
    "CrmAppRepositoryProtocol",
    "CrmAppPlatformRepositoryProtocol",
    "CrmUserRepositoryProtocol",
    "CrmRoleRepositoryProtocol",
    "CrmPermissionRepositoryProtocol",
    "CrmRolePermissionRepositoryProtocol",
    "CrmUserRoleRepositoryProtocol",
    "CrmUserAppAccessRepositoryProtocol",
    "CrmClickRepositoryProtocol",
    "CrmAppUserRepositoryProtocol",
    "CrmInstallRepositoryProtocol",
    "CrmEventRepositoryProtocol",
    "CrmCurrentParamRepositoryProtocol",
    "CrmMetricDefinitionRepositoryProtocol",
    "CrmConversionDefinitionRepositoryProtocol",
    "CrmSecretTemplateRepositoryProtocol",
    "CrmAppSecretRepositoryProtocol",
    "CrmParamDefinitionRepositoryProtocol",
    "CrmPostbackRuleRepositoryProtocol",
    "CrmPushCampaignRepositoryProtocol",
    "CrmPushTokenRepositoryProtocol",
    "CrmPushEventRepositoryProtocol",
    "CrmAuditLogRepositoryProtocol",
    "CrmRepositoryFactoryProtocol",
]
