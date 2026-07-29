from __future__ import annotations

from types import TracebackType
from typing import Any, Protocol

from app.modules.crm.domain.app.app_repository_protocol import CrmAppRepositoryProtocol
from app.modules.crm.domain.app_platform.app_platform_repository_protocol import CrmAppPlatformRepositoryProtocol
from app.modules.analytics.domain.click.click_repository_protocol import AnalyticsClickRepositoryProtocol
from app.modules.crm.domain.conversion_definition.conversion_definition_repository_protocol import (
    CrmConversionDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.current_param.current_param_repository_protocol import CrmCurrentParamRepositoryProtocol
from app.modules.crm.domain.custom_params_statistics_aggregate.statistics_aggregate_repository_protocol import (
    CustomParamsStatisticsRepositoryProtocol,
)
from app.modules.analytics.domain.events.event_repository_protocol import AnalyticsEventRepositoryProtocol
from app.modules.analytics.domain.install.install_repository_protocol import AnalyticsInstallRepositoryProtocol
from app.modules.crm.domain.metric_definition.metric_definition_repository_protocol import (
    CrmMetricDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.param_definition.param_definition_repository_protocol import (
    CrmParamDefinitionRepositoryProtocol,
)
from app.modules.crm.domain.statistics_aggregate.statistics_aggregate_repository_protocol import (
    StatisticsRepositoryProtocol,
)


class AnalyticsUnitOfWorkProtocol(Protocol):
    app_repo: CrmAppRepositoryProtocol
    app_platform_repo: CrmAppPlatformRepositoryProtocol
    click_repo: AnalyticsClickRepositoryProtocol
    install_repo: AnalyticsInstallRepositoryProtocol
    event_repo: AnalyticsEventRepositoryProtocol
    current_param_repo: CrmCurrentParamRepositoryProtocol
    statistics_repo: StatisticsRepositoryProtocol
    custom_params_statistics_repo: CustomParamsStatisticsRepositoryProtocol
    metric_definition_repo: CrmMetricDefinitionRepositoryProtocol
    conversion_definition_repo: CrmConversionDefinitionRepositoryProtocol
    param_definition_repo: CrmParamDefinitionRepositoryProtocol

    def __enter__(self) -> "AnalyticsUnitOfWorkProtocol": ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class AnalyticsUnitOfWorkFactoryProtocol(Protocol):
    def create(self, *args: Any, **kwds: Any) -> AnalyticsUnitOfWorkProtocol: ...
