from typing import Protocol

from app.application.sdk.s2s.commands import S2SClickCommand
from app.application.sdk.s2s.responses import S2SClickResponse
from app.application.tracking.entities import TrackingRedirectCommand
from app.application.tracking.responses import TrackingRedirectResponse


class ClickServiceProtocol(Protocol):
    def process_s2s_click(self, command: S2SClickCommand) -> S2SClickResponse: ...

    def process_redirect_click(
        self,
        command: TrackingRedirectCommand,
    ) -> TrackingRedirectResponse: ...
