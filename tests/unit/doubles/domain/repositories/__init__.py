from tests.unit.doubles.domain.repositories.access import InMemoryCrmUserAppAccessRepository
from tests.unit.doubles.domain.repositories.apps import (
    InMemoryCrmAppPlatformRepository,
    InMemoryCrmAppRepository,
    InMemoryCrmAppUserRepository,
    InMemoryCrmInstallRepository,
)
from tests.unit.doubles.domain.repositories.attribution import (
    InMemoryCrmClickRepository,
    InMemoryCrmCurrentParamRepository,
    InMemoryCrmEventRepository,
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
    InMemoryCrmRolePermissionRepository,
    InMemoryCrmRoleRepository,
    InMemoryCrmUserRepository,
    InMemoryCrmUserRoleRepository,
)
from tests.unit.doubles.domain.repositories.push import (
    InMemoryCrmPushCampaignRepository,
    InMemoryCrmPushEventRepository,
    InMemoryCrmPushTokenRepository,
)

__all__ = [
    "InMemoryCrmAppPlatformRepository",
    "InMemoryCrmAppRepository",
    "InMemoryCrmAppSecretRepository",
    "InMemoryCrmAppUserRepository",
    "InMemoryCrmAuditLogRepository",
    "InMemoryCrmClickRepository",
    "InMemoryCrmConversionDefinitionRepository",
    "InMemoryCrmCurrentParamRepository",
    "InMemoryCrmEventRepository",
    "InMemoryCrmInstallRepository",
    "InMemoryCrmMetricDefinitionRepository",
    "InMemoryCrmParamDefinitionRepository",
    "InMemoryCrmPermissionRepository",
    "InMemoryCrmPostbackRuleRepository",
    "InMemoryCrmPushCampaignRepository",
    "InMemoryCrmPushEventRepository",
    "InMemoryCrmPushTokenRepository",
    "InMemoryCrmRolePermissionRepository",
    "InMemoryCrmRoleRepository",
    "InMemoryCrmSecretTemplateRepository",
    "InMemoryCrmUserAppAccessRepository",
    "InMemoryCrmUserRepository",
    "InMemoryCrmUserRoleRepository",
]
