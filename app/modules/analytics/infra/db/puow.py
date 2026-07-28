from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Any

from sqlalchemy.orm import Session
from typing_extensions import Self

from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol, AnalyticsUnitOfWorkProtocol
from app.modules.analytics.infra.db.factory import AnalyticsSqlAlchemyRepositoryFactory
from app.modules.crm.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.modules.crm.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.modules.crm.domain.click.click_repository_protocol import CrmClickRepositoryProtocol
from app.modules.crm.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.current_param.current_param_repository_protocol import CrmCurrentParamRepositoryProtocol
from app.modules.crm.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
from app.modules.crm.domain.events.event_repository_protocol import CrmEventRepositoryProtocol
from app.modules.crm.domain.install.install_repository_protocol import CrmInstallRepositoryProtocol
from app.modules.crm.domain.metric_definition.metric_definition_repository_protocol import (
    CrmMetricDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.param_definition.param_definition_repository_protocol import (
    CrmParamDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.statistics_aggregate.statistics_aggregate_repository_protocol import (
    StatisticsRepositoryProtocol,
)
from app.modules.crm.infra.db.repositories.factory import CrmSqlAlchemyRepositoryFactory

# FIXME: Temporary decision. Divide this class to smaller ones for each application service.


class SqlAlchemyUnitOfWork(AnalyticsUnitOfWorkProtocol):
    app_repo: CrmAppRepositoryProtocol
    app_platform_repo: CrmAppPlatformRepositoryProtocol
    click_repo: CrmClickRepositoryProtocol
    install_repo: CrmInstallRepositoryProtocol
    event_repo: CrmEventRepositoryProtocol
    current_param_repo: CrmCurrentParamRepositoryProtocol
    statistics_repo: StatisticsRepositoryProtocol
    custom_params_statistics_repo: CustomParamsStatisticsRepositoryProtocol
    metric_definition_repo: CrmMetricDefinitionRepositoryProtocol
    conversion_definition_repo: CrmConversionDefinitionRepositoryProtocol
    param_definition_repo: CrmParamDefinitionRepositoryProtocol

    def __init__(
        self,
        session_factory: Callable[[], Session],
        analytics_repository_factory: AnalyticsSqlAlchemyRepositoryFactory | None = None,
        crm_reference_repository_factory: CrmSqlAlchemyRepositoryFactory | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._analytics_repository_factory = analytics_repository_factory or AnalyticsSqlAlchemyRepositoryFactory()
        self._crm_reference_repository_factory = crm_reference_repository_factory or CrmSqlAlchemyRepositoryFactory()
        self.session: Session | None = None

    def __enter__(self) -> Self:
        self.session = self._session_factory()
        self.app_repo = self._crm_reference_repository_factory.app_repo(self.session)
        self.app_platform_repo = self._crm_reference_repository_factory.app_platform_repo(self.session)
        self.metric_definition_repo = self._crm_reference_repository_factory.metric_definition_repo(self.session)
        self.conversion_definition_repo = self._crm_reference_repository_factory.conversion_definition_repo(
            self.session
        )
        self.param_definition_repo = self._crm_reference_repository_factory.param_definition_repo(self.session)
        self.click_repo = self._analytics_repository_factory.click_repo(self.session)
        self.install_repo = self._analytics_repository_factory.install_repo(self.session)
        self.event_repo = self._analytics_repository_factory.event_repo(self.session)
        self.current_param_repo = self._analytics_repository_factory.current_param_repo(self.session)
        self.statistics_repo = self._analytics_repository_factory.statistics_repo(self.session)
        self.custom_params_statistics_repo = self._analytics_repository_factory.custom_params_statistics_repo(
            self.session
        )
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.session is not None:
                self.session.close()
                self.session = None

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW session is not started")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW session is not started")
        self.session.rollback()


class SqlAlchemyUnitOfWorkFactory(AnalyticsUnitOfWorkFactoryProtocol):
    def __init__(self, sesion_factory: Callable[[], Session]) -> None:
        self.__sesion_facoty = sesion_factory

    def create(self, *args: Any, **kwds: Any) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(self.__sesion_facoty)
