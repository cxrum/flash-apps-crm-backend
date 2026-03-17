from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Any, Sequence

from fastapi import Depends

from app.application.contracts.encryption import EncryptionServiceProtocol
from app.application.events_bus.handlers.update_param import AsyncUpdateParamHandler
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.domain.event_bus.events.crm_update_params import UpdateCurrentParamMessage
from app.domain.event_bus.service_protocol import AsyncEventMessageHandler, IAsyncEventBus
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


def get_uow_factory() -> UnitOfWorkFacotyProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)

def get_app_seacrets_encryptor() -> EncryptionServiceProtocol:
    return EncryptionService()

def get_currecncy_client() -> CurrencyConvertorClientProtocol:
    return CurrencyConvertorClient()

def get_in_memory_event_bus() -> IAsyncEventBus:
    return SHARED_ASYNC_MEMORY_BUS

def build_update_param_handler(
        uow_factory: UnitOfWorkFacotyProtocol
    ) -> AsyncEventMessageHandler:
    return AsyncUpdateParamHandler(uow_factory)

def get_event_subscribers() -> list[tuple[str, AsyncEventMessageHandler]]:
    uow_factory = get_uow_factory()
    
    return [
        (UpdateCurrentParamMessage.EVENT_NAME, build_update_param_handler(uow_factory)),
    ]

def register_event_handlers(
        async_handlers: list[tuple[str, AsyncEventMessageHandler]] = get_event_subscribers(),
        async_memory_bus: IAsyncEventBus = get_in_memory_event_bus(), 
    ):
    
    for (event_name, handler) in async_handlers:
        async_memory_bus.subscribe(event_name, handler) 

def get_sdk_app_service(
    uow_factory: UnitOfWorkFacotyProtocol = Depends(get_uow_factory),
    encryption_service: EncryptionServiceProtocol = Depends(get_app_seacrets_encryptor),
) -> AppService:
    return AppService(uow_factory, encryption_service)

def get_sdk_ingestion_service(
    uow_factory: UnitOfWorkFacotyProtocol = Depends(get_uow_factory),
    event_bus: IAsyncEventBus = Depends(get_in_memory_event_bus),
    currency_service = Depends(get_currecncy_client)
) -> IngestionService:
    return IngestionService(uow_factory, event_bus, currency_service)

def get_s2s_service(
    uow_factory: UnitOfWorkFacotyProtocol = Depends(get_uow_factory),
) -> S2SService:
    return S2SService(uow_factory)
