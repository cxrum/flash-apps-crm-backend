from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Any

from fastapi import Depends

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.event_bus.service_protocol import IAsyncEventBus
from app.application.s2s.servicie import S2SService
from app.application.sdk.usecases.apps.service import AppService
from app.application.sdk.usecases.ingestion.service import IngestionService
from app.domain.uow import UnitOfWorkFacotyProtocol, UnitOfWorkProtocol
from app.infra.db.puow import SqlAlchemyUnitOfWork, SqlAlchemyUnitOfWorkFactory
from app.infra.db.session import SessionFactory
from app.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus
from app.infra.services.currency import CurrencyConvertorClient
from app.infra.services.encription import EncryptionService

SHARED_ASYNC_MEMORY_BUS = InMemoryAsyncEventBus()


def uow_factory() -> UnitOfWorkFacotyProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)

def get_app_seacrets_encryptor() -> EncryptionServiceProtocol:
    return EncryptionService()

def get_currecncy_client() -> CurrencyConvertorClientProtocol:
    return CurrencyConvertorClient()

def get_in_memory_event_bus() -> IAsyncEventBus:
    return SHARED_ASYNC_MEMORY_BUS

def get_sdk_app_service(
    uow_factory: UnitOfWorkFacotyProtocol = Depends(uow_factory),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_seacrets_encryptor),
) -> AppService:
    return AppService(uow_factory, encryption_service)

def get_sdk_ingestion_service(
    uow_factory: UnitOfWorkFacotyProtocol = Depends(uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    currency_service = Depends(get_currecncy_client)
) -> IngestionService:
    return IngestionService(uow_factory, event_bus, currency_service)

def get_s2s_service(
    uow_factory: UnitOfWorkFacotyProtocol = Depends(uow_factory),
) -> S2SService:
    return S2SService(uow_factory)
