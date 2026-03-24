from __future__ import annotations

from app.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.domain.conversion_definition.conversion_definition_repository_protocol import CrmConversionDefinitionRepositoryProtocol
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
from app.domain.user_app_access.user_app_access_repository_protocol import CrmUserAppAccessRepositoryProtocol
from app.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.domain.user_permissions.CrmUserPermisionEntity import CrmUserPermisionEntity


__all__ = [
    "CrmAppRepositoryProtocol",
    "CrmAppPlatformRepositoryProtocol",
    "CrmUserRepositoryProtocol",
    "CrmRoleRepositoryProtocol",
    "CrmPermissionRepositoryProtocol",
    "CrmUserPermisionEntity",
    "CrmUserAppAccessRepositoryProtocol",
    "CrmClickRepositoryProtocol",
    "CrmAppUserRepositoryProtocol",
    "CrmInstallRepositoryProtocol",
    "CrmEventRepositoryProtocol",
    "CrmCurrentParamRepositoryProtocol",
    "CustomParamsStatisticsRepositoryProtocol",
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
    "StatisticsRepositoryProtocol",
]
