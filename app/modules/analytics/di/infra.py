from app.core.db.session import SessionFactory
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.analytics.infra.db.puow import SqlAlchemyUnitOfWorkFactory


def get_analytics_uow_factory() -> AnalyticsUnitOfWorkFactoryProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)
