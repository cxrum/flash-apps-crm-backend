from typing import Protocol

from app.modules.crm.application.sdk.ingestion.commands import (
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
)
from app.modules.crm.application.sdk.ingestion.responses import SdkInstallResponse


class IngestionServiceProtocol(Protocol):
    async def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse: ...
    async def process_batch_events(self, command: SdkEventsCommand) -> None: ...
    async def update_params(self, command: SdkParamsUpdateCommand) -> None: ...
