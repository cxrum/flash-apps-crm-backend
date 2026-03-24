"""Database repositories package."""

from app.infra.db.repositories.aggregate_repositories import (
    SqlAlchemyCustomParamsStatisticsRepository,
    SqlAlchemyStatisticsRepository,
)
from app.infra.db.repositories.access_repositories import SqlAlchemyCrmUserAppAccessRepository
from app.infra.db.repositories.apps_repositories import (
    SqlAlchemyCrmAppPlatformRepository,
    SqlAlchemyCrmAppRepository,
    SqlAlchemyCrmAppUserRepository,
    SqlAlchemyCrmInstallRepository,
)
from app.infra.db.repositories.attribution_repositories import (
    SqlAlchemyCrmClickRepository,
    SqlAlchemyCrmCurrentParamRepository,
    SqlAlchemyCrmEventRepository,
)
from app.infra.db.repositories.audit_repositories import SqlAlchemyCrmAuditLogRepository
from app.infra.db.repositories.config_repositories import (
    SqlAlchemyCrmAppSecretRepository,
    SqlAlchemyCrmConversionDefinitionRepository,
    SqlAlchemyCrmMetricDefinitionRepository,
    SqlAlchemyCrmParamDefinitionRepository,
    SqlAlchemyCrmPostbackRuleRepository,
    SqlAlchemyCrmSecretTemplateRepository,
)
from app.infra.db.repositories.crm_repositories import (
    SqlAlchemyCrmPermissionRepository,
    SqlAlchemyCrmRoleRepository,
    SqlAlchemyCrmUserRepository,
    SqlAlchemyCrmUserPermisionRepository,
)
from app.infra.db.repositories.factory import CrmSqlAlchemyRepositoryFactory
from app.infra.db.repositories.push_repositories import (
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
    "SqlAlchemyCrmUserPermisionRepository",
    "SqlAlchemyStatisticsRepository",
]
