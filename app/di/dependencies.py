from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.events.registry import PurchasesEventsPlaceholder, PurchasesEventsPlaceholderProtocol
from app.domain.events.service import EventsDomainService
from app.domain.identity.service import IdentityDomainService
from app.domain.identity.service_protocol import IdentityServiceProtocol
from app.domain.purchases.service import PurchasesDomainService
from app.domain.purchases.service_protocol import PurchasesServiceProtocol
from app.infra.db.repositories.app_repository import AppRepository
from app.domain.contracts.app_repository_protocol import AppRepositoryProtocol
from app.infra.db.repositories.events_repository import EventsRepository
from app.domain.contracts.events_repository_protocol import EventsRepositoryProtocol
from app.infra.db.repositories.identity_repository import IdentityRepository
from app.domain.contracts.identity_repository_protocol import IdentityRepositoryProtocol
from app.infra.db.repositories.subscription_repository import SubscriptionRepository
from app.domain.contracts.subscription_repository_protocol import SubscriptionRepositoryProtocol
from app.infra.db.repositories.user_repository import UserRepository
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol
from app.infra.db.session import get_db
from app.infra.services.apple_purchases import ApplePurchasesService


def get_events_repository(db: Session = Depends(get_db)) -> EventsRepositoryProtocol:
    return EventsRepository(db)


def get_app_repository(db: Session = Depends(get_db)) -> AppRepositoryProtocol:
    return AppRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryProtocol:
    return UserRepository(db)


def get_identity_repository(db: Session = Depends(get_db)) -> IdentityRepositoryProtocol:
    return IdentityRepository(db)

def get_subscription_repository(db: Session = Depends(get_db)) -> SubscriptionRepositoryProtocol:
    return SubscriptionRepository(db)


def get_purchases_events_placeholder() -> PurchasesEventsPlaceholderProtocol:
    return PurchasesEventsPlaceholder()


def get_apple_purchases_service () -> PurchasesServiceProtocol:
    return ApplePurchasesService() # type: ignore


def get_events_domain_service(
    event_repository: EventsRepositoryProtocol = Depends(get_events_repository),
    app_repository: AppRepositoryProtocol = Depends(get_app_repository),
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
    identity_repository: IdentityRepositoryProtocol = Depends(get_identity_repository),
) -> EventsDomainService:
    return EventsDomainService(
        event_repo=event_repository,
        app_repo=app_repository,
        user_repo=user_repository,
        identity_repo=identity_repository,
    )

def get_purchases_service(
    app_repository: AppRepositoryProtocol = Depends(get_app_repository),
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
    subscription_repository: SubscriptionRepositoryProtocol = Depends(get_subscription_repository),
    events_placeholder: PurchasesEventsPlaceholderProtocol = Depends(get_purchases_events_placeholder),
    apple_purchases_service: ApplePurchasesService = Depends(get_apple_purchases_service)
) -> PurchasesServiceProtocol:
    return PurchasesDomainService(
        app_repository=app_repository,
        user_repository=user_repository,
        subscription_repository=subscription_repository,
        events_placeholder=events_placeholder,
        purchases_client=apple_purchases_service
    )
    
def get_identity_service(
    repository: IdentityRepositoryProtocol = Depends(get_identity_repository),
) -> IdentityServiceProtocol:
    return IdentityDomainService(repository)

