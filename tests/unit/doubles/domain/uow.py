from __future__ import annotations

from types import TracebackType
from typing import Any

from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol, UnitOfWorkProtocol
from tests.unit.doubles.base import CallRecorderMixin
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


class StubUnitOfWork(CallRecorderMixin, UnitOfWorkProtocol):
    def __init__(self, **overrides: Any) -> None:
        super().__init__()
        self.enter_count = 0
        self.exit_count = 0
        self.commit_count = 0
        self.rollback_count = 0
        self.last_exception: BaseException | None = None

        self.app_repo = overrides.get("app_repo", InMemoryCrmAppRepository())
        self.app_platform_repo = overrides.get("app_platform_repo", InMemoryCrmAppPlatformRepository())
        self.user_repo = overrides.get("user_repo", InMemoryCrmUserRepository())
        self.role_repo = overrides.get("role_repo", InMemoryCrmRoleRepository())
        self.permission_repo = overrides.get("permission_repo", InMemoryCrmPermissionRepository())

        _crmUserPermissionsRepository = InMemoryCrmUserPermissionsRepository()
        _crmUserPermissionsRepository.set_permissions(self.permission_repo)

        self.user_permissions_repo = overrides.get("user_permissions_repo", _crmUserPermissionsRepository)
        self.user_app_access_repo = overrides.get(
            "user_app_access_repo",
            InMemoryCrmUserAppAccessRepository(),
        )
        self.click_repo = overrides.get("click_repo", InMemoryCrmClickRepository())
        self.app_user_repo = overrides.get("app_user_repo", InMemoryCrmAppUserRepository())
        self.install_repo = overrides.get("install_repo", InMemoryCrmInstallRepository())
        self.current_param_repo = overrides.get(
            "current_param_repo",
            InMemoryCrmCurrentParamRepository(),
        )
        self.statistics_repo = overrides.get(
            "statistics_repo",
            InMemoryStatisticsRepository(),
        )
        self.custom_params_statistics_repo = overrides.get(
            "custom_params_statistics_repo",
            InMemoryCustomParamsStatisticsRepository(),
        )
        self.metric_definition_repo = overrides.get(
            "metric_definition_repo",
            InMemoryCrmMetricDefinitionRepository(),
        )
        self.conversion_definition_repo = overrides.get(
            "conversion_definition_repo",
            InMemoryCrmConversionDefinitionRepository(),
        )
        self.secret_template_repo = overrides.get(
            "secret_template_repo",
            InMemoryCrmSecretTemplateRepository(),
        )
        self.param_definition_repo = overrides.get(
            "param_definition_repo",
            InMemoryCrmParamDefinitionRepository(),
        )
        self.push_campaign_repo = overrides.get(
            "push_campaign_repo",
            InMemoryCrmPushCampaignRepository(),
        )
        self.audit_log_repo = overrides.get("audit_log_repo", InMemoryCrmAuditLogRepository())

        self.event_repo = overrides.get(
            "event_repo",
            InMemoryCrmEventRepository(
                click_lookup=self.click_repo.get_by_id,
                platform_lookup=self.app_platform_repo.get_by_id,
            ),
        )
        self.app_secret_repo = overrides.get(
            "app_secret_repo",
            InMemoryCrmAppSecretRepository(
                platform_lookup=self.app_platform_repo.get_by_id,
            ),
        )
        self.postback_rule_repo = overrides.get(
            "postback_rule_repo",
            InMemoryCrmPostbackRuleRepository(
                platform_lookup=self.app_platform_repo.get_by_id,
            ),
        )
        self.push_token_repo = overrides.get(
            "push_token_repo",
            InMemoryCrmPushTokenRepository(
                install_lookup=self.install_repo.get_by_id,
            ),
        )
        self.push_event_repo = overrides.get("push_event_repo", InMemoryCrmPushEventRepository())

    def __enter__(self) -> "StubUnitOfWork":
        self.enter_count += 1
        self._record("__enter__")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.exit_count += 1
        self.last_exception = exc
        self._record("__exit__", exc_type, exc, tb)
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self) -> None:
        self.commit_count += 1
        self._record("commit")

    def rollback(self) -> None:
        self.rollback_count += 1
        self._record("rollback")


class StubRepositoryFactory(CallRecorderMixin):
    def __init__(self, *, stub_uow: StubUnitOfWork | None = None) -> None:
        super().__init__()
        self.stub_uow = stub_uow or StubUnitOfWork()

    def _repo(self, name: str, session: object) -> object:
        self._record(name, session)
        return getattr(self.stub_uow, name)

    def app_repo(self, session: object) -> object:
        return self._repo("app_repo", session)

    def app_platform_repo(self, session: object) -> object:
        return self._repo("app_platform_repo", session)

    def user_repo(self, session: object) -> object:
        return self._repo("user_repo", session)

    def role_repo(self, session: object) -> object:
        return self._repo("role_repo", session)

    def permission_repo(self, session: object) -> object:
        return self._repo("permission_repo", session)

    def user_permissions_repo(self, session: object) -> object:
        return self._repo("user_permissions_repo", session)

    def user_app_access_repo(self, session: object) -> object:
        return self._repo("user_app_access_repo", session)

    def click_repo(self, session: object) -> object:
        return self._repo("click_repo", session)

    def app_user_repo(self, session: object) -> object:
        return self._repo("app_user_repo", session)

    def install_repo(self, session: object) -> object:
        return self._repo("install_repo", session)

    def event_repo(self, session: object) -> object:
        return self._repo("event_repo", session)

    def current_param_repo(self, session: object) -> object:
        return self._repo("current_param_repo", session)

    def statistics_repo(self, session: object) -> object:
        return self._repo("statistics_repo", session)

    def custom_params_statistics_repo(self, session: object) -> object:
        return self._repo("custom_params_statistics_repo", session)

    def metric_definition_repo(self, session: object) -> object:
        return self._repo("metric_definition_repo", session)

    def conversion_definition_repo(self, session: object) -> object:
        return self._repo("conversion_definition_repo", session)

    def secret_template_repo(self, session: object) -> object:
        return self._repo("secret_template_repo", session)

    def app_secret_repo(self, session: object) -> object:
        return self._repo("app_secret_repo", session)

    def param_definition_repo(self, session: object) -> object:
        return self._repo("param_definition_repo", session)

    def postback_rule_repo(self, session: object) -> object:
        return self._repo("postback_rule_repo", session)

    def push_campaign_repo(self, session: object) -> object:
        return self._repo("push_campaign_repo", session)

    def push_token_repo(self, session: object) -> object:
        return self._repo("push_token_repo", session)

    def push_event_repo(self, session: object) -> object:
        return self._repo("push_event_repo", session)

    def audit_log_repo(self, session: object) -> object:
        return self._repo("audit_log_repo", session)


class StubUoWFactory(UnitOfWorkFactoryProtocol):
    def __init__(self, stub_uow: StubUnitOfWork | None = None) -> None:
        self.stub_uow = stub_uow or StubUnitOfWork()

    def create(self, *args: Any, **kwds: Any) -> StubUnitOfWork:
        return self.stub_uow
