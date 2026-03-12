from app.application.contracts.encryption import EncryptionServiceProtocol
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
from app.domain.metric_definition.metric_definition_repository_protocol import (
    CrmMetricDefinitionRepositoryProtocol,
)
from app.domain.param_definition.param_definition_repository_protocol import CrmParamDefinitionRepositoryProtocol
from app.domain.permission.permission_repository_protocol import CrmPermissionRepositoryProtocol
from app.domain.postback_rule.postback_rule_repository_protocol import CrmPostbackRuleRepositoryProtocol
from app.domain.push_campaign.push_campaign_repository_protocol import CrmPushCampaignRepositoryProtocol
from app.domain.push_event.push_event_repository_protocol import CrmPushEventRepositoryProtocol
from app.domain.push_token.push_token_repository_protocol import CrmPushTokenRepositoryProtocol
from app.domain.role.role_repository_protocol import CrmRoleRepositoryProtocol
from app.domain.role_permission.role_permission_repository_protocol import (
    CrmRolePermissionRepositoryProtocol,
)
from app.domain.secret_template.secret_template_repository_protocol import (
    CrmSecretTemplateRepositoryProtocol,
)
from app.domain.uow import CrmUnitOfWorkProtocol
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_app_access.user_app_access_repository_protocol import (
    CrmUserAppAccessRepositoryProtocol,
)
from app.domain.user_role.user_role_repository_protocol import CrmUserRoleRepositoryProtocol
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.domain.repositories import (
    InMemoryCrmAppPlatformRepository,
    InMemoryCrmAppRepository,
    InMemoryCrmAppSecretRepository,
    InMemoryCrmAppUserRepository,
    InMemoryCrmAuditLogRepository,
    InMemoryCrmClickRepository,
    InMemoryCrmConversionDefinitionRepository,
    InMemoryCrmCurrentParamRepository,
    InMemoryCrmEventRepository,
    InMemoryCrmInstallRepository,
    InMemoryCrmMetricDefinitionRepository,
    InMemoryCrmParamDefinitionRepository,
    InMemoryCrmPermissionRepository,
    InMemoryCrmPostbackRuleRepository,
    InMemoryCrmPushCampaignRepository,
    InMemoryCrmPushEventRepository,
    InMemoryCrmPushTokenRepository,
    InMemoryCrmRolePermissionRepository,
    InMemoryCrmRoleRepository,
    InMemoryCrmSecretTemplateRepository,
    InMemoryCrmUserAppAccessRepository,
    InMemoryCrmUserRepository,
    InMemoryCrmUserRoleRepository,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork

PROTOCOL_DOUBLE_REGISTRY = {
    EncryptionServiceProtocol: StubEncryptionService,
    CrmUnitOfWorkProtocol: StubUnitOfWork,
    CrmAppRepositoryProtocol: InMemoryCrmAppRepository,
    CrmAppPlatformRepositoryProtocol: InMemoryCrmAppPlatformRepository,
    CrmAppSecretRepositoryProtocol: InMemoryCrmAppSecretRepository,
    CrmAppUserRepositoryProtocol: InMemoryCrmAppUserRepository,
    CrmAuditLogRepositoryProtocol: InMemoryCrmAuditLogRepository,
    CrmClickRepositoryProtocol: InMemoryCrmClickRepository,
    CrmConversionDefinitionRepositoryProtocol: InMemoryCrmConversionDefinitionRepository,
    CrmCurrentParamRepositoryProtocol: InMemoryCrmCurrentParamRepository,
    CrmEventRepositoryProtocol: InMemoryCrmEventRepository,
    CrmInstallRepositoryProtocol: InMemoryCrmInstallRepository,
    CrmMetricDefinitionRepositoryProtocol: InMemoryCrmMetricDefinitionRepository,
    CrmParamDefinitionRepositoryProtocol: InMemoryCrmParamDefinitionRepository,
    CrmPermissionRepositoryProtocol: InMemoryCrmPermissionRepository,
    CrmPostbackRuleRepositoryProtocol: InMemoryCrmPostbackRuleRepository,
    CrmPushCampaignRepositoryProtocol: InMemoryCrmPushCampaignRepository,
    CrmPushEventRepositoryProtocol: InMemoryCrmPushEventRepository,
    CrmPushTokenRepositoryProtocol: InMemoryCrmPushTokenRepository,
    CrmRolePermissionRepositoryProtocol: InMemoryCrmRolePermissionRepository,
    CrmRoleRepositoryProtocol: InMemoryCrmRoleRepository,
    CrmSecretTemplateRepositoryProtocol: InMemoryCrmSecretTemplateRepository,
    CrmUserAppAccessRepositoryProtocol: InMemoryCrmUserAppAccessRepository,
    CrmUserRepositoryProtocol: InMemoryCrmUserRepository,
    CrmUserRoleRepositoryProtocol: InMemoryCrmUserRoleRepository,
}
