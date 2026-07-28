from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.analytics.infra.db.repositories import (
    SqlAlchemyAnalyticsClickRepository,
    SqlAlchemyAnalyticsCurrentParamRepository,
    SqlAlchemyAnalyticsCustomParamsStatisticsRepository,
    SqlAlchemyAnalyticsEventRepository,
    SqlAlchemyAnalyticsInstallRepository,
    SqlAlchemyAnalyticsStatisticsRepository,
)


class AnalyticsSqlAlchemyRepositoryFactory:
    def click_repo(self, session: Session) -> SqlAlchemyAnalyticsClickRepository:
        return SqlAlchemyAnalyticsClickRepository(session)

    def install_repo(self, session: Session) -> SqlAlchemyAnalyticsInstallRepository:
        return SqlAlchemyAnalyticsInstallRepository(session)

    def event_repo(self, session: Session) -> SqlAlchemyAnalyticsEventRepository:
        return SqlAlchemyAnalyticsEventRepository(session)

    def current_param_repo(self, session: Session) -> SqlAlchemyAnalyticsCurrentParamRepository:
        return SqlAlchemyAnalyticsCurrentParamRepository(session)

    def statistics_repo(self, session: Session) -> SqlAlchemyAnalyticsStatisticsRepository:
        return SqlAlchemyAnalyticsStatisticsRepository(session)

    def custom_params_statistics_repo(self, session: Session) -> SqlAlchemyAnalyticsCustomParamsStatisticsRepository:
        return SqlAlchemyAnalyticsCustomParamsStatisticsRepository(session)
