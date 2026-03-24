from __future__ import annotations

from sqlalchemy.orm import Session

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
from app.infra.db.repositories.push_repositories import (
    SqlAlchemyCrmPushCampaignRepository,
    SqlAlchemyCrmPushEventRepository,
    SqlAlchemyCrmPushTokenRepository,
)


class CrmSqlAlchemyRepositoryFactory:
    def app_repo(self, session: Session) -> SqlAlchemyCrmAppRepository:
        return SqlAlchemyCrmAppRepository(session)

    def app_platform_repo(self, session: Session) -> SqlAlchemyCrmAppPlatformRepository:
        return SqlAlchemyCrmAppPlatformRepository(session)

    def user_repo(self, session: Session) -> SqlAlchemyCrmUserRepository:
        return SqlAlchemyCrmUserRepository(session)

    def role_repo(self, session: Session) -> SqlAlchemyCrmRoleRepository:
        return SqlAlchemyCrmRoleRepository(session)

    def permission_repo(self, session: Session) -> SqlAlchemyCrmPermissionRepository:
        return SqlAlchemyCrmPermissionRepository(session)

    def user_permissions_repo(self, session: Session) -> SqlAlchemyCrmUserPermisionRepository:
        return SqlAlchemyCrmUserPermisionRepository(session)

    def user_app_access_repo(self, session: Session) -> SqlAlchemyCrmUserAppAccessRepository:
        return SqlAlchemyCrmUserAppAccessRepository(session)

    def click_repo(self, session: Session) -> SqlAlchemyCrmClickRepository:
        return SqlAlchemyCrmClickRepository(session)

    def app_user_repo(self, session: Session) -> SqlAlchemyCrmAppUserRepository:
        return SqlAlchemyCrmAppUserRepository(session)

    def install_repo(self, session: Session) -> SqlAlchemyCrmInstallRepository:
        return SqlAlchemyCrmInstallRepository(session)

    def event_repo(self, session: Session) -> SqlAlchemyCrmEventRepository:
        return SqlAlchemyCrmEventRepository(session)

    def current_param_repo(self, session: Session) -> SqlAlchemyCrmCurrentParamRepository:
        return SqlAlchemyCrmCurrentParamRepository(session)

    def statistics_repo(self, session: Session) -> SqlAlchemyStatisticsRepository:
        return SqlAlchemyStatisticsRepository(session)

    def custom_params_statistics_repo(self, session: Session) -> SqlAlchemyCustomParamsStatisticsRepository:
        return SqlAlchemyCustomParamsStatisticsRepository(session)

    def metric_definition_repo(self, session: Session) -> SqlAlchemyCrmMetricDefinitionRepository:
        return SqlAlchemyCrmMetricDefinitionRepository(session)

    def conversion_definition_repo(self, session: Session) -> SqlAlchemyCrmConversionDefinitionRepository:
        return SqlAlchemyCrmConversionDefinitionRepository(session)

    def secret_template_repo(self, session: Session) -> SqlAlchemyCrmSecretTemplateRepository:
        return SqlAlchemyCrmSecretTemplateRepository(session)

    def app_secret_repo(self, session: Session) -> SqlAlchemyCrmAppSecretRepository:
        return SqlAlchemyCrmAppSecretRepository(session)

    def param_definition_repo(self, session: Session) -> SqlAlchemyCrmParamDefinitionRepository:
        return SqlAlchemyCrmParamDefinitionRepository(session)

    def postback_rule_repo(self, session: Session) -> SqlAlchemyCrmPostbackRuleRepository:
        return SqlAlchemyCrmPostbackRuleRepository(session)

    def push_campaign_repo(self, session: Session) -> SqlAlchemyCrmPushCampaignRepository:
        return SqlAlchemyCrmPushCampaignRepository(session)

    def push_token_repo(self, session: Session) -> SqlAlchemyCrmPushTokenRepository:
        return SqlAlchemyCrmPushTokenRepository(session)

    def push_event_repo(self, session: Session) -> SqlAlchemyCrmPushEventRepository:
        return SqlAlchemyCrmPushEventRepository(session)

    def audit_log_repo(self, session: Session) -> SqlAlchemyCrmAuditLogRepository:
        return SqlAlchemyCrmAuditLogRepository(session)
