from app.domain.app.CrmAppEntity import CrmAppEntity
from app.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.domain.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.domain.click.CrmClickEntity import CrmClickEntity
from app.domain.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.domain.current_param.CrmCurrentParamEntity import CrmCurrentParamEntity
from app.domain.events.CrmEventEntity import EventEntity
from app.domain.install.CrmInstallEntity import CrmInstallEntity
from app.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.domain.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.domain.role.CrmRoleEntity import CrmRoleEntity
from app.domain.role_permission.CrmRolePermissionEntity import CrmRolePermissionEntity
from app.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.domain.user.CrmUserEntity import CrmUserEntity
from app.domain.user_role.CrmUserRoleEntity import CrmUserRoleEntity
from app.domain.audit_log.CrmAuditLogEntity import (
    CrmAuditLogEntity,
)
from app.domain.repositories import (
    CrmAppPlatformRepositoryProtocol,
    CrmAppRepositoryProtocol,
    CrmAppSecretRepositoryProtocol,
    CrmAppUserRepositoryProtocol,
    CrmAuditLogRepositoryProtocol,
    CrmClickRepositoryProtocol,
    CrmConversionDefinitionRepositoryProtocol,
    CrmCurrentParamRepositoryProtocol,
    CrmEventRepositoryProtocol,
    CrmInstallRepositoryProtocol,
    CrmMetricDefinitionRepositoryProtocol,
    CrmParamDefinitionRepositoryProtocol,
    CrmPermissionRepositoryProtocol,
    CrmPostbackRuleRepositoryProtocol,
    CrmPushCampaignRepositoryProtocol,
    CrmPushEventRepositoryProtocol,
    CrmPushTokenRepositoryProtocol,
    CrmRolePermissionRepositoryProtocol,
    CrmRoleRepositoryProtocol,
    CrmSecretTemplateRepositoryProtocol,
    CrmUserAppAccessRepositoryProtocol,
    CrmUserRepositoryProtocol,
    CrmUserRoleRepositoryProtocol,
)
from app.domain.uow import CrmUnitOfWorkProtocol

__all__ = [
    "CrmAppEntity",
    "CrmAppPlatformEntity",
    "CrmAppSecretEntity",
    "CrmAppUserEntity",
    "CrmAuditLogEntity",
    "CrmClickEntity",
    "CrmConversionDefinitionEntity",
    "CrmCurrentParamEntity",
    "EventEntity",
    "CrmInstallEntity",
    "CrmMetricDefinitionEntity",
    "CrmParamDefinitionEntity",
    "CrmPermissionEntity",
    "CrmPostbackRuleEntity",
    "CrmPushCampaignEntity",
    "CrmPushEventEntity",
    "CrmPushTokenEntity",
    "CrmRoleEntity",
    "CrmRolePermissionEntity",
    "CrmSecretTemplateEntity",
    "CrmUserAppAccessEntity",
    "CrmUserEntity",
    "CrmUserRoleEntity",
    "CrmAppPlatformRepositoryProtocol",
    "CrmAppRepositoryProtocol",
    "CrmAppSecretRepositoryProtocol",
    "CrmAppUserRepositoryProtocol",
    "CrmAuditLogRepositoryProtocol",
    "CrmClickRepositoryProtocol",
    "CrmConversionDefinitionRepositoryProtocol",
    "CrmCurrentParamRepositoryProtocol",
    "CrmEventRepositoryProtocol",
    "CrmInstallRepositoryProtocol",
    "CrmMetricDefinitionRepositoryProtocol",
    "CrmParamDefinitionRepositoryProtocol",
    "CrmPermissionRepositoryProtocol",
    "CrmPostbackRuleRepositoryProtocol",
    "CrmPushCampaignRepositoryProtocol",
    "CrmPushEventRepositoryProtocol",
    "CrmPushTokenRepositoryProtocol",
    "CrmRolePermissionRepositoryProtocol",
    "CrmRoleRepositoryProtocol",
    "CrmSecretTemplateRepositoryProtocol",
    "CrmUnitOfWorkProtocol",
    "CrmUserAppAccessRepositoryProtocol",
    "CrmUserRepositoryProtocol",
    "CrmUserRoleRepositoryProtocol",
]
