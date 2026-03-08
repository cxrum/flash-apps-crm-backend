from __future__ import annotations

from datetime import datetime
from typing import Protocol


class PurchasesEventsPlaceholderProtocol(Protocol):
    def emit_verify_purchase_event(
        self,
        *,
        app_id: int,
        platform: str,
        user_id: str,
        anonymous_id: str,
        status: str,
        linked_at: datetime,
    ) -> None: ...


class PurchasesEventsPlaceholder(PurchasesEventsPlaceholderProtocol):
    def emit_verify_purchase_event(
        self,
        *,
        app_id: int,
        platform: str,
        user_id: str,
        anonymous_id: str,
        status: str,
        linked_at: datetime,
    ) -> None:
        # Placeholder: later this will write domain events into DB.
        pass

