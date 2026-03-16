from __future__ import annotations

from dataclasses import dataclass

from app.domain.event_bus.service_protocol import IEventBus
from app.application.sdk.usecases.apps.service import AppService
from app.application.sdk.usecases.ingestion.service import IngestionService
from app.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.domain.uow import StubUnitOfWork


@dataclass(slots=True)
class UnitTestContext:
    uow: StubUnitOfWork
    encryption_service: StubEncryptionService
    currency_service: CurrencyConvertorClientProtocol
    event_bus: IEventBus

    def build_app_service(self) -> AppService:
        return AppService(
            uow=self.uow,
            encryption_service=self.encryption_service,
        )
        
    def build_ingestion_service(self) -> IngestionService:
        return IngestionService(
            uow=self.uow,
            event_bus=self.event_bus,
            currency_service=self.currency_service
        )
