from collections.abc import Iterator

from fastapi import Depends

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.s2s.servicie import S2SService
from app.application.sdk.usecases.apps.service import AppService
from app.domain.uow import CrmUnitOfWorkProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWork
from app.infra.db.session import SessionFactory
from app.infra.services.encription import EncryptionService


def get_uow() -> Iterator[CrmUnitOfWorkProtocol]:
    with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        yield uow

def get_app_seacrets_encryptor() -> EncryptionServiceProtocol:
    return EncryptionService()

def get_sdk_app_service(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_seacrets_encryptor),
) -> AppService:
    return AppService(uow, encryption_service)

def get_s2s_service(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
) -> S2SService:
    return S2SService(uow)