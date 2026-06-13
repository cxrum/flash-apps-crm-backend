from typing import Protocol

from app.modules.crm.application.sdk.s2s.commands import S2SClickCommand
from app.modules.crm.application.sdk.s2s.responses import S2SClickResponse
from app.modules.crm.application.tracking.entities import TrackingRedirectCommand
from app.modules.crm.application.tracking.responses import TrackingRedirectResponse


class ClickServiceProtocol(Protocol):
    def process_s2s_click(self, command: S2SClickCommand) -> S2SClickResponse: ...

    def process_redirect_click(
        self,
        command: TrackingRedirectCommand,
    ) -> TrackingRedirectResponse: ...
