from typing import Protocol

from app.modules.crm.application.attribution.contracts import CrmClickContext, CrmPostbackContext


class CrmAttributionGateway(Protocol):
    def get_click_context(self, click_id: str) -> CrmClickContext | None: ...
    def get_postback_context(self, event_id: str) -> CrmPostbackContext | None: ...
