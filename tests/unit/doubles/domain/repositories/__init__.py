from tests.unit.doubles.domain.repositories.aggregates import (
    InMemoryCustomParamsStatisticsRepository,
    InMemoryStatisticsRepository,
)
from tests.unit.doubles.domain.repositories.access import InMemoryCrmUserAppAccessRepository
from tests.unit.doubles.domain.repositories.apps import (
    InMemoryCrmAppPlatformRepository,
    InMemoryCrmAppRepository,
    InMemoryCrmAppUserRepository,
    InMemoryAnalyticsInstallRepository,
)
from tests.unit.doubles.domain.repositories.attribution import (
    InMemoryAnalyticsClickRepository,
    InMemoryAnalyticsCurrentParamRepository,
    InMemoryAnalyticsEventRepository,
)
from tests.unit.doubles.domain.repositories.audit import InMemoryCrmAuditLogRepository
from tests.unit.doubles.domain.repositories.config import (
    InMemoryCrmAppSecretRepository,
    InMemoryCrmConversionDefinitionRepository,
    InMemoryCrmMetricDefinitionRepository,
    InMemoryCrmParamDefinitionRepository,
    InMemoryCrmPostbackRuleRepository,
    InMemoryCrmSecretTemplateRepository,
)
from tests.unit.doubles.domain.repositories.crm import (
    InMemoryCrmPermissionRepository,
    InMemoryCrmRoleRepository,
    InMemoryCrmUserRepository,
    InMemoryCrmUserPermissionsRepository,
)
from tests.unit.doubles.domain.repositories.push import (
    InMemoryCrmPushCampaignRepository,
    InMemoryCrmPushEventRepository,
    InMemoryCrmPushTokenRepository,
)

__all__ = [
    "InMemoryCustomParamsStatisticsRepository",
    "InMemoryCrmAppPlatformRepository",
    "InMemoryCrmAppRepository",
    "InMemoryCrmAppSecretRepository",
    "InMemoryCrmAppUserRepository",
    "InMemoryCrmAuditLogRepository",
    "InMemoryAnalyticsClickRepository",
    "InMemoryCrmConversionDefinitionRepository",
    "InMemoryAnalyticsCurrentParamRepository",
    "InMemoryAnalyticsEventRepository",
    "InMemoryAnalyticsInstallRepository",
    "InMemoryCrmMetricDefinitionRepository",
    "InMemoryCrmParamDefinitionRepository",
    "InMemoryCrmPermissionRepository",
    "InMemoryCrmPostbackRuleRepository",
    "InMemoryCrmPushCampaignRepository",
    "InMemoryCrmPushEventRepository",
    "InMemoryCrmPushTokenRepository",
    "InMemoryCrmRoleRepository",
    "InMemoryCrmSecretTemplateRepository",
    "InMemoryCrmUserAppAccessRepository",
    "InMemoryCrmUserRepository",
    "InMemoryCrmUserPermissionsRepository",
    "InMemoryStatisticsRepository",
]
