from collections.abc import Iterator
from functools import lru_cache

from fastapi import Depends

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.infra.event_bus.in_memory import InMemoryEventBus, InMemoryMessageQueue
from app.application.events_bus.service import IEventBus, IMessageQueue
from app.application.s2s.servicie import S2SService
from app.application.sdk.usecases.apps.service import AppService
from app.application.sdk.usecases.ingestion.service import IngestionService
from app.domain.uow import CrmUnitOfWorkProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWork
from app.infra.db.session import SessionFactory
from app.infra.services.currency import CurrencyConvertorClient
from app.infra.services.encription import EncryptionService


def get_uow() -> Iterator[CrmUnitOfWorkProtocol]:
    with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        yield uow

def get_app_seacrets_encryptor() -> EncryptionServiceProtocol:
    return EncryptionService()


def get_currecncy_client() -> CurrencyConvertorClientProtocol:
    return CurrencyConvertorClient()


@lru_cache(maxsize=1)
def get_in_memory_event_bus() -> IEventBus:
    return InMemoryEventBus()

def get_sdk_app_service(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_seacrets_encryptor),
) -> AppService:
    return AppService(uow, encryption_service)

def get_sdk_ingestion_service(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
    event_bus: IEventBus = Depends(get_in_memory_event_bus),
    currency_service = Depends(get_currecncy_client)
) -> IngestionService:
    return IngestionService(uow, event_bus, currency_service)

def get_s2s_service(
    uow: CrmUnitOfWorkProtocol = Depends(get_uow),
) -> S2SService:
    return S2SService(uow)
