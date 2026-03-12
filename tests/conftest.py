from __future__ import annotations

import pytest

from tests.unit.base import UnitTestContext
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.domain.uow import StubRepositoryFactory, StubUnitOfWork


@pytest.fixture
def stub_uow() -> StubUnitOfWork:
    return StubUnitOfWork()


@pytest.fixture
def stub_repository_factory(stub_uow: StubUnitOfWork) -> StubRepositoryFactory:
    return StubRepositoryFactory(stub_uow=stub_uow)


@pytest.fixture
def stub_encryption_service() -> StubEncryptionService:
    return StubEncryptionService()


@pytest.fixture
def unit_test_context(
    stub_uow: StubUnitOfWork,
    stub_encryption_service: StubEncryptionService,
) -> UnitTestContext:
    return UnitTestContext(
        uow=stub_uow,
        encryption_service=stub_encryption_service,
    )
