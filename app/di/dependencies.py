from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.postgres_uow import SqlAlchemyUnitOfWork
from app.infra.db.session import SessionLocal, get_db
from app.infra.uow_base import UnitOfWorkProtocol


def get_uow() -> UnitOfWorkProtocol:
    return SqlAlchemyUnitOfWork(SessionLocal)

