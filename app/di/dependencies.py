from collections.abc import Iterator

from fastapi import Depends

from app.application.sdk.usecases.apps.service import AppService
from app.domain.uow import CrmUnitOfWorkProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWork
from app.infra.db.session import SessionLocal


def get_uow() -> Iterator[CrmUnitOfWorkProtocol]:
    with SqlAlchemyUnitOfWork(SessionLocal) as uow:
        yield uow


def get_sdk_app_service(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
) -> AppService:
    return AppService(uow)