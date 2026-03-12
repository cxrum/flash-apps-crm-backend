from __future__ import annotations

from dataclasses import dataclass

from app.application.sdk.usecases.apps.service import AppService
from app.application.sdk.usecases.ingestion.service import InsegisntionService
from tests.unit.doubles.application.encryption import StubEncryptionService
from tests.unit.doubles.domain.uow import StubUnitOfWork


@dataclass(slots=True)
class UnitTestContext:
    uow: StubUnitOfWork
    encryption_service: StubEncryptionService

    def build_app_service(self) -> AppService:
        return AppService(
            uow=self.uow,
            encryption_service=self.encryption_service,
        )
        
    def build_ingestion_service(self) -> InsegisntionService:
        return InsegisntionService(
            uow=self.uow,
        )
