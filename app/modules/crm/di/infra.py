from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol
from app.modules.crm.infra.db.puow import SqlAlchemyUnitOfWorkFactory
from app.core.db.session import SessionFactory


def get_uow_factory() -> UnitOfWorkFactoryProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)
