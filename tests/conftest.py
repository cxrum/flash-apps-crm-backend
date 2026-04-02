from __future__ import annotations

import pytest

from app.core.config import Settings, settings as app_settings
from app.domain.event_bus.service_protocol import IAsyncEventBus, IEventBus
from app.domain.uow import UnitOfWorkFactoryProtocol
from app.infra.event_bus.in_memory import InMemoryEventBus
from app.infra.event_bus.async_bus.in_memory import InMemoryAsyncEventBus
from tests.unit.base import UnitTestContext
from tests.unit.doubles.application.currency import StubCurrencyConvertorClient
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.application.hash import StubHashService
from tests.unit.doubles.domain.uow import StubRepositoryFactory, StubUnitOfWork, StubUoWFactory


@pytest.fixture
def stub_uow() -> StubUnitOfWork:
    return StubUnitOfWork()

@pytest.fixture
def stub_uow_factory(stub_uow: StubUnitOfWork) -> StubUoWFactory:
    return StubUoWFactory(stub_uow)

@pytest.fixture
def stub_repository_factory(stub_uow: StubUnitOfWork) -> StubRepositoryFactory:
    return StubRepositoryFactory(stub_uow=stub_uow)

@pytest.fixture
def stub_encryption_service() -> StubEncryptionService:
    return StubEncryptionService()

@pytest.fixture
def stub_hash_service() -> StubHashService:
    return StubHashService()

@pytest.fixture
def event_bus() -> IEventBus:
    return InMemoryEventBus()

@pytest.fixture
def async_event_bus() -> IAsyncEventBus:
    return InMemoryAsyncEventBus(1)

@pytest.fixture
def currency_service() -> StubCurrencyConvertorClient:
    return StubCurrencyConvertorClient()

@pytest.fixture
def settings() -> Settings:
    return app_settings

@pytest.fixture
def unit_test_context(
    stub_uow: StubUnitOfWork,
    stub_uow_factory: UnitOfWorkFactoryProtocol,
    stub_encryption_service: StubEncryptionService,
    stub_hash_service: StubHashService,
    async_event_bus: IAsyncEventBus,
    currency_service: StubCurrencyConvertorClient,
    settings: Settings,
) -> UnitTestContext:
    return UnitTestContext(
        uow=stub_uow,
        uow_factory=stub_uow_factory,
        encryption_service=stub_encryption_service,
        hash_service=stub_hash_service,
        async_event_bus=async_event_bus,
        currency_service=currency_service,
        settings=settings,
    )
