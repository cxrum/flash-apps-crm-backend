from __future__ import annotations

from app.application.purchases.entities import VerifyPurchaseCommand
from app.domain.purchases.service_protocol import PurchaseVerifyResult, PurchasesServiceProtocol


class PurchasesUseCases:
    def __init__(self, purchases_domain_service: PurchasesServiceProtocol) -> None:
        self.purchases_domain_service = purchases_domain_service

    def verify_purchase(self, command: VerifyPurchaseCommand) -> PurchaseVerifyResult:
        return self.purchases_domain_service.verify_purchase(
            app_id=command.app_id,
            platform=command.platform,
            anonymous_id=command.anonymous_id,
            user_id=command.user_id,
            linked_at=command.linked_at,
        )
