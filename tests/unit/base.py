from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.core.config import Settings
from app.modules.analytics.application.ingestion.service import IngestionService
from app.modules.crm.application.admin.crm_authorization.service import CrmAuthorizationService
from app.modules.crm.application.sdk.apps.service import AppService
from app.modules.crm.domain.currency.currency_convertor_protocol import CurrencyConvertorClientProtocol
from app.modules.crm.domain.event_bus.service_protocol import IAsyncEventBus
from app.modules.crm.domain.uow import UnitOfWorkFactoryProtocol
from tests.unit.doubles.application.currency import StubCurrencyConvertorClient
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.application.hash import StubHashService
from tests.unit.doubles.domain.uow import StubUnitOfWork


@dataclass(slots=True)
class UnitTestContext:
    uow: StubUnitOfWork
    uow_factory: UnitOfWorkFactoryProtocol
    encryption_service: StubEncryptionService
    hash_service: StubHashService
    currency_service: StubCurrencyConvertorClient
    async_event_bus: IAsyncEventBus
    settings: Settings

    def build_app_service(self) -> AppService:
        return AppService(
            uow_factory=self.uow_factory,
            authorization_service=CrmAuthorizationService(self.uow_factory),
            encryption_service=self.encryption_service,
            hash_service=self.hash_service,
            async_event_bus=self.async_event_bus,
        )

    def build_ingestion_service(self) -> IngestionService:
        return IngestionService(
            uow_factory=self.uow_factory, async_event_bus=self.async_event_bus, currency_service=self.currency_service
        )
