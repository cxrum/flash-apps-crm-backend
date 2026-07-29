from typing import Protocol

from app.modules.analytics.application.ingestion.commands import (
    SdkEventsCommand,
    SdkInstallCommand,
    SdkParamsUpdateCommand,
)
from app.modules.analytics.application.ingestion.responses import SdkInstallResponse


class IngestionServiceProtocol(Protocol):
    async def process_install(self, command: SdkInstallCommand) -> SdkInstallResponse | None: ...
    async def process_batch_events(self, command: SdkEventsCommand) -> bool: ...
    async def update_params(self, command: SdkParamsUpdateCommand) -> bool: ...
