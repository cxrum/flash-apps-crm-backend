from __future__ import annotations

from datetime import UTC, datetime

from app.domain.purchases.entities import SubscriptionSnapshotEntity
from app.domain.events.registry import PurchasesEventsPlaceholderProtocol
from app.domain.platform import PlatformUseCases
from app.domain.purchases.service_protocol import PurchaseVerifyResult, PurchasesServiceProtocol
from app.domain.app.app_repository_protocol import AppRepositoryProtocol
from app.domain.purchases.subscription_repository_protocol import SubscriptionRepositoryProtocol
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol
from app.domain.purchases.app_puchases_protocol import PurchasesClientProtocol


class InvalidPlatformError(Exception):
    pass


class AppNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class PurchasesDomainService(PurchasesServiceProtocol):
    def __init__(
        self,
        app_repository: AppRepositoryProtocol,
        user_repository: UserRepositoryProtocol,
        subscription_repository: SubscriptionRepositoryProtocol,
        purchases_client: PurchasesClientProtocol,
        events_placeholder: PurchasesEventsPlaceholderProtocol,
    ) -> None:
        self.app_repository = app_repository
        self.user_repository = user_repository
        self.subscription_repository = subscription_repository
        self.events_placeholder = events_placeholder
        self.purchases_client = purchases_client

    def verify_purchase(
        self,
        *,
        app_id: int,
        platform: str,
        anonymous_id: str,
        user_id: str,
        linked_at: datetime,
    ) -> PurchaseVerifyResult:
        if not PlatformUseCases.is_supported_platform(platform):
            raise InvalidPlatformError("Unsupported platform")
        if not self.app_repository.exists(app_id):
            raise AppNotFoundError("Unknown app id")
        if not self.user_repository.exists(user_id):
            raise UserNotFoundError("Unknown user id")

        snapshot = self.subscription_repository.get_latest_subscription(
            app_id=app_id,
            user_id=user_id,
            platform=platform,
        )
        result = self._build_result(snapshot)

        if platform == "ios":
            status = self.purchases_client.verify("asd")
        else:
            status = "invalid"
                
        self.events_placeholder.emit_verify_purchase_event(
            app_id=app_id,
            platform=platform,
            user_id=user_id,
            anonymous_id=anonymous_id,
            status=result.status,
            linked_at=linked_at,
        )
        return result

    def _build_result(self, snapshot: SubscriptionSnapshotEntity | None) -> PurchaseVerifyResult:
        if snapshot is None:
            return PurchaseVerifyResult(
                status="invalid",
                expires_at=None,
                price=0.0,
                currency="",
                subscription_id=None,
            )

        normalized_status = snapshot.status.lower()
        if normalized_status == "cancelled":
            status = "canceled"
        elif snapshot.expires_at and snapshot.expires_at < datetime.now(UTC):
            status = "expired"
        elif normalized_status == "active":
            status = "active"
        else:
            status = "invalid"

        return PurchaseVerifyResult(
            status=status,
            expires_at=snapshot.expires_at,
            price=snapshot.price,
            currency=snapshot.currency,
            subscription_id=snapshot.subscription_id,
        )
