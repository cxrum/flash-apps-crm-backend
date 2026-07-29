from app.modules.crm.application.contracts.encryption import EncryptionServiceProtocol
from app.modules.crm.application.contracts.ip2location import IP2LocationGatewayProtocol
from app.modules.crm.application.contracts.requester import S2SRequesterProtocol
from app.modules.crm.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.modules.crm.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.modules.crm.domain.app_secret.app_secret_repository_protocol import CrmAppSecretRepositoryProtocol
from app.modules.crm.domain.app_user.app_user_repository_protocol import CrmAppUserRepositoryProtocol
from app.modules.crm.domain.audit_log.audit_log_repository_protocol import CrmAuditLogRepositoryProtocol
from app.modules.crm.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.modules.crm.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.modules.crm.domain.current_param.current_param_repository_protocol import CrmCurrentParamRepositoryProtocol
from app.modules.crm.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
from app.modules.crm.domain.events.event_repository_protocol import CrmEventRepositoryProtocol
from app.modules.crm.domain.hash_protocol import HashProtocol
from app.modules.crm.domain.install.install_repository_protocol import CrmInstallRepositoryProtocol
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
from app.modules.crm.domain.statistics_aggregate.statistics_aggregate_repository_protocol import (
    StatisticsRepositoryProtocol,
)
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from app.modules.crm.domain.user.user_repository_protocol import CrmUserRepositoryProtocol
from app.modules.crm.domain.user_app_access.user_app_access_repository_protocol import (
    CrmUserAppAccessRepositoryProtocol,
)
from app.modules.crm.domain.user_permissions.user_permissions_repository_protocol import (
    CrmUserPermissionsRepositoryProtocol,
)
from tests.unit.doubles.application.currency import StubCurrencyConvertorClient
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.application.hash import StubHashService
from tests.unit.doubles.application.ip2location import StubIP2LocationGateway
from tests.unit.doubles.application.requester import StubS2SRequester
from tests.unit.doubles.application.signature import StubSignatureService
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
    InMemoryCrmRoleRepository,
    InMemoryCrmSecretTemplateRepository,
    InMemoryCrmUserAppAccessRepository,
    InMemoryCrmUserPermissionsRepository,
    InMemoryCrmUserRepository,
    InMemoryCustomParamsStatisticsRepository,
    InMemoryStatisticsRepository,
)
from tests.unit.doubles.domain.uow import StubUnitOfWork, StubUoWFactory

PROTOCOL_DOUBLE_REGISTRY = {
    EncryptionServiceProtocol: StubEncryptionService,
    IP2LocationGatewayProtocol: StubIP2LocationGateway,
    UnitOfWorkProtocol: StubUnitOfWork,
    UnitOfWorkFactoryProtocol: StubUoWFactory,
    HashProtocol: StubHashService,
    CrmAppRepositoryProtocol: InMemoryCrmAppRepository,
    CrmAppPlatformRepositoryProtocol: InMemoryCrmAppPlatformRepository,
    CrmAppSecretRepositoryProtocol: InMemoryCrmAppSecretRepository,
    CrmAppUserRepositoryProtocol: InMemoryCrmAppUserRepository,
    CrmAuditLogRepositoryProtocol: InMemoryCrmAuditLogRepository,
    CrmClickRepositoryProtocol: InMemoryCrmClickRepository,
    CrmConversionDefinitionRepositoryProtocol: InMemoryCrmConversionDefinitionRepository,
    CrmCurrentParamRepositoryProtocol: InMemoryCrmCurrentParamRepository,
    CustomParamsStatisticsRepositoryProtocol: InMemoryCustomParamsStatisticsRepository,
    CrmEventRepositoryProtocol: InMemoryCrmEventRepository,
    CrmInstallRepositoryProtocol: InMemoryCrmInstallRepository,
    CrmMetricDefinitionRepositoryProtocol: InMemoryCrmMetricDefinitionRepository,
    CrmParamDefinitionRepositoryProtocol: InMemoryCrmParamDefinitionRepository,
    CrmPermissionRepositoryProtocol: InMemoryCrmPermissionRepository,
    CrmPostbackRuleRepositoryProtocol: InMemoryCrmPostbackRuleRepository,
    CrmPushCampaignRepositoryProtocol: InMemoryCrmPushCampaignRepository,
    CrmPushEventRepositoryProtocol: InMemoryCrmPushEventRepository,
    CrmPushTokenRepositoryProtocol: InMemoryCrmPushTokenRepository,
    CrmRoleRepositoryProtocol: InMemoryCrmRoleRepository,
    CrmSecretTemplateRepositoryProtocol: InMemoryCrmSecretTemplateRepository,
    StatisticsRepositoryProtocol: InMemoryStatisticsRepository,
    CrmUserAppAccessRepositoryProtocol: InMemoryCrmUserAppAccessRepository,
    CrmUserRepositoryProtocol: InMemoryCrmUserRepository,
    CrmUserPermissionsRepositoryProtocol: InMemoryCrmUserPermissionsRepository,
    CurrencyConvertorClientProtocol: StubCurrencyConvertorClient,
    S2SRequesterProtocol: StubS2SRequester,
}
