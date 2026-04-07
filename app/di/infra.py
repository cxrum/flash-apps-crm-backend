from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWorkFactory
from app.infra.db.session import SessionFactory


def get_uow_factory() -> UnitOfWorkFactoryProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)