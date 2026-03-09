from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.events.event_usecases import EventUseCases
from app.application.identity.identity_usecases import IdentityUseCases
from app.application.purchases.purchase_usecases import PurchasesUseCases
from app.domain.app.app_repository_protocol import AppRepositoryProtocol
from app.domain.contracts.repository_protocol import RepositoryFactoryProtocol
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol
from app.domain.events.registry import PurchasesEventsPlaceholder, PurchasesEventsPlaceholderProtocol
from app.domain.purchases.app_puchases_protocol import PurchasesClientProtocol
from app.domain.purchases.service import PurchasesDomainService
from app.domain.purchases.service_protocol import PurchasesServiceProtocol
from app.domain.purchases.subscription_repository_protocol import SubscriptionRepositoryProtocol
from app.infra.db.postgres_uow import SqlAlchemyUnitOfWork
from app.infra.db.repositories.factory import RepositoryFactory
from app.infra.db.session import SessionLocal, get_db
from app.infra.services.apple_purchases import ApplePurchasesService
from app.infra.uow_base import UnitOfWorkProtocol


def get_uow() -> UnitOfWorkProtocol:
    return SqlAlchemyUnitOfWork(SessionLocal)


def get_repository_factory() -> RepositoryFactoryProtocol:
    return RepositoryFactory()


def get_app_repository(
    db: Session = Depends(get_db),
    repo_factory: RepositoryFactoryProtocol = Depends(get_repository_factory),
) -> AppRepositoryProtocol:
    return repo_factory.app_repo(db)


def get_user_repository(
    db: Session = Depends(get_db),
    repo_factory: RepositoryFactoryProtocol = Depends(get_repository_factory),
) -> UserRepositoryProtocol:
    return repo_factory.user_repo(db)


def get_subscription_repository(
    db: Session = Depends(get_db),
    repo_factory: RepositoryFactoryProtocol = Depends(get_repository_factory),
) -> SubscriptionRepositoryProtocol:
    return repo_factory.subscription_repo(db)


def get_event_usecases(
    uow: UnitOfWorkProtocol = Depends(get_uow),
    repo_factory: RepositoryFactoryProtocol = Depends(get_repository_factory),
) -> EventUseCases:
    return EventUseCases(uow=uow, repository_factory=repo_factory)


def get_identity_usecases(
    uow: UnitOfWorkProtocol = Depends(get_uow),
    repo_factory: RepositoryFactoryProtocol = Depends(get_repository_factory),
) -> IdentityUseCases:
    return IdentityUseCases(uow=uow, repository_factory=repo_factory)


def get_purchases_events_placeholder() -> PurchasesEventsPlaceholderProtocol:
    return PurchasesEventsPlaceholder()


def get_apple_purchases_service() -> PurchasesClientProtocol:
    return ApplePurchasesService()


def get_purchases_service(
    app_repository: AppRepositoryProtocol = Depends(get_app_repository),
    user_repository: UserRepositoryProtocol = Depends(get_user_repository),
    subscription_repository: SubscriptionRepositoryProtocol = Depends(get_subscription_repository),
    events_placeholder: PurchasesEventsPlaceholderProtocol = Depends(get_purchases_events_placeholder),
    apple_purchases_service: PurchasesClientProtocol = Depends(get_apple_purchases_service),
) -> PurchasesServiceProtocol:
    return PurchasesDomainService(
        app_repository=app_repository,
        user_repository=user_repository,
        subscription_repository=subscription_repository,
        events_placeholder=events_placeholder,
        purchases_client=apple_purchases_service,
    )


def get_purchases_usecases(
    purchases_service: PurchasesServiceProtocol = Depends(get_purchases_service),
) -> PurchasesUseCases:
    return PurchasesUseCases(purchases_service)
