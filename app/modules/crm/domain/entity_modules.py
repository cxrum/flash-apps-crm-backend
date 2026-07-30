"""Compatibility module exporting one-module-per-entity CRM paths.

This keeps legacy-style module granularity while preserving the aggregated
``app.modules.crm.crm.entities`` contract.
"""

from app.modules.crm.domain.app.CrmAppEntity import CrmAppEntity
from app.modules.crm.domain.app_platform.CrmAppPlatformEntity import CrmAppPlatformEntity
from app.modules.crm.domain.app_secret.CrmAppSecretEntity import CrmAppSecretEntity
from app.modules.crm.domain.app_user.CrmAppUserEntity import CrmAppUserEntity
from app.modules.crm.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity
from app.modules.crm.domain.conversion_definition.CrmConversionDefinitionEntity import CrmConversionDefinitionEntity
from app.modules.crm.domain.metric_definition.CrmMetricDefinitionEntity import CrmMetricDefinitionEntity
from app.modules.crm.domain.param_definition.CrmParamDefinitionEntity import CrmParamDefinitionEntity
from app.modules.crm.domain.permission.CrmPermissionEntity import CrmPermissionEntity
from app.modules.crm.domain.postback_rule.CrmPostbackRuleEntity import CrmPostbackRuleEntity
from app.modules.crm.domain.push_campaign.CrmPushCampaignEntity import CrmPushCampaignEntity
from app.modules.crm.domain.push_event.CrmPushEventEntity import CrmPushEventEntity
from app.modules.crm.domain.push_token.CrmPushTokenEntity import CrmPushTokenEntity
from app.modules.crm.domain.role.CrmRoleEntity import CrmRoleEntity
from app.modules.crm.domain.secret_template.CrmSecretTemplateEntity import CrmSecretTemplateEntity
from app.modules.crm.domain.user.CrmUserEntity import CrmUserEntity
from app.modules.crm.domain.user_app_access.CrmUserAppAccessEntity import CrmUserAppAccessEntity
from app.modules.crm.domain.user_permissions.CrmUserPermissionEntity import CrmUserPermissionEntity

__all__ = [
    "CrmAppEntity",
    "CrmAppPlatformEntity",
    "CrmUserEntity",
    "CrmRoleEntity",
    "CrmPermissionEntity",
    "CrmUserPermissionEntity",
    "CrmUserAppAccessEntity",
    "CrmAppUserEntity",
    "CrmMetricDefinitionEntity",
    "CrmConversionDefinitionEntity",
    "CrmSecretTemplateEntity",
    "CrmAppSecretEntity",
    "CrmParamDefinitionEntity",
    "CrmPostbackRuleEntity",
    "CrmPushCampaignEntity",
    "CrmPushTokenEntity",
    "CrmPushEventEntity",
    "CrmAuditLogEntity",
]
