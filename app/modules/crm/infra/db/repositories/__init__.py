"""Database repositories package."""

from app.modules.crm.infra.db.repositories.access_repositories import SqlAlchemyCrmUserAppAccessRepository
from app.modules.crm.infra.db.repositories.aggregate_repositories import (
    SqlAlchemyCustomParamsStatisticsRepository,
    SqlAlchemyStatisticsRepository,
)
from app.modules.crm.infra.db.repositories.apps_repositories import (
    SqlAlchemyCrmAppPlatformRepository,
    SqlAlchemyCrmAppRepository,
    SqlAlchemyCrmAppUserRepository,
    SqlAlchemyCrmInstallRepository,
)
from app.modules.crm.infra.db.repositories.attribution_repositories import (
    SqlAlchemyCrmClickRepository,
    SqlAlchemyCrmCurrentParamRepository,
    SqlAlchemyCrmEventRepository,
)
from app.modules.crm.infra.db.repositories.audit_repositories import SqlAlchemyCrmAuditLogRepository
from app.modules.crm.infra.db.repositories.config_repositories import (
    SqlAlchemyCrmAppSecretRepository,
    SqlAlchemyCrmConversionDefinitionRepository,
    SqlAlchemyCrmMetricDefinitionRepository,
    SqlAlchemyCrmParamDefinitionRepository,
    SqlAlchemyCrmPostbackRuleRepository,
    SqlAlchemyCrmSecretTemplateRepository,
)
from app.modules.crm.infra.db.repositories.crm_repositories import (
    SqlAlchemyCrmPermissionRepository,
    SqlAlchemyCrmRoleRepository,
    SqlAlchemyCrmUserPermissionRepository,
    SqlAlchemyCrmUserRepository,
)
from app.modules.crm.infra.db.repositories.factory import CrmSqlAlchemyRepositoryFactory
from app.modules.crm.infra.db.repositories.push_repositories import (
    SqlAlchemyCrmPushCampaignRepository,
    SqlAlchemyCrmPushEventRepository,
    SqlAlchemyCrmPushTokenRepository,
)

__all__ = [
    "CrmSqlAlchemyRepositoryFactory",
    "SqlAlchemyCustomParamsStatisticsRepository",
    "SqlAlchemyCrmAppPlatformRepository",
    "SqlAlchemyCrmAppRepository",
    "SqlAlchemyCrmAppSecretRepository",
    "SqlAlchemyCrmAppUserRepository",
    "SqlAlchemyCrmAuditLogRepository",
    "SqlAlchemyCrmClickRepository",
    "SqlAlchemyCrmConversionDefinitionRepository",
    "SqlAlchemyCrmCurrentParamRepository",
    "SqlAlchemyCrmEventRepository",
    "SqlAlchemyCrmInstallRepository",
    "SqlAlchemyCrmMetricDefinitionRepository",
    "SqlAlchemyCrmParamDefinitionRepository",
    "SqlAlchemyCrmPermissionRepository",
    "SqlAlchemyCrmPostbackRuleRepository",
    "SqlAlchemyCrmPushCampaignRepository",
    "SqlAlchemyCrmPushEventRepository",
    "SqlAlchemyCrmPushTokenRepository",
    "SqlAlchemyCrmRoleRepository",
    "SqlAlchemyCrmSecretTemplateRepository",
    "SqlAlchemyCrmUserAppAccessRepository",
    "SqlAlchemyCrmUserRepository",
    "SqlAlchemyCrmUserPermissionRepository",
    "SqlAlchemyStatisticsRepository",
]
