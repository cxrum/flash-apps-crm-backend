from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.domain.event_bus.service_protocol import IAsyncEventBus
from app.application.sdk.usecases.apps.service import AppService
from app.application.sdk.usecases.ingestion.service import IngestionService
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.domain.uow import StubUnitOfWork


@dataclass(slots=True)
class UnitTestContext:
    uow: StubUnitOfWork
    uow_factory: Callable[[], StubUnitOfWork] 
    encryption_service: StubEncryptionService
    currency_service: CurrencyConvertorClientProtocol
    async_event_bus: IAsyncEventBus

    def build_app_service(self) -> AppService:
        return AppService(
            uow_factory=self.uow_factory,
            encryption_service=self.encryption_service,
        )
        
    def build_ingestion_service(self) -> IngestionService:
        return IngestionService(
            uow_factory=self.uow_factory,
            async_event_bus=self.async_event_bus,
            currency_service=self.currency_service
        )
