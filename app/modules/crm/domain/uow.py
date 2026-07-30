from __future__ import annotations

from types import TracebackType
from typing import Any, Protocol

from app.modules.crm.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.modules.crm.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.modules.crm.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.modules.crm.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.modules.crm.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.modules.crm.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.metric_definition.metric_definition_repository_protocol import (
    CrmMetricDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.param_definition.param_definition_repository_protocol import (
    CrmParamDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.permission.permission_repository_protocol import CrmPermissionRepositoryProtocol
from app.modules.crm.domain.postback_rule.postback_rule_repository_protocol import CrmPostbackRuleRepositoryProtocol
from app.modules.crm.domain.push_campaign.push_campaign_repository_protocol import CrmPushCampaignRepositoryProtocol
from app.modules.crm.domain.push_event.push_event_repository_protocol import CrmPushEventRepositoryProtocol
from app.modules.crm.domain.push_token.push_token_repository_protocol import CrmPushTokenRepositoryProtocol
from app.modules.crm.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.modules.crm.domain.secret_template.secret_template_repository_protocol import (
    CrmSecretTemplateRepositoryProtocol,
)
from app.modules.crm.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.modules.crm.domain.user_app_access.user_app_access_repository_protocol import (
    CrmUserAppAccessRepositoryProtocol,
)
from app.modules.crm.domain.user_permissions.user_permissions_repository_protocol import (
    CrmUserPermissionsRepositoryProtocol,
)


class UnitOfWorkProtocol(Protocol):
    app_repo: CrmAppRepositoryProtocol
    app_platform_repo: CrmAppPlatformRepositoryProtocol
    user_repo: CrmUserRepositoryProtocol
    role_repo: CrmRoleRepositoryProtocol
    permission_repo: CrmPermissionRepositoryProtocol
    user_permissions_repo: CrmUserPermissionsRepositoryProtocol
    user_app_access_repo: CrmUserAppAccessRepositoryProtocol
    app_user_repo: CrmAppUserRepositoryProtocol
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

    def __enter__(self) -> "UnitOfWorkProtocol": ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class UnitOfWorkFactoryProtocol(Protocol):
    def create(self, *args: Any, **kwds: Any) -> UnitOfWorkProtocol: ...
