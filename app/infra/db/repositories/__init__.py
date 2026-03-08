"""Database repositories package."""

from app.infra.db.repositories.app_repository import AppRepository
from app.domain.app.app_repository_protocol import AppRepositoryProtocol
from app.infra.db.repositories.daily_aggregate_repository import DailyAggregateRepository
from app.domain.contracts.daily_aggregate_repository_protocol import DailyAggregateRepositoryProtocol
from app.infra.db.repositories.events_repository import EventsRepository
from app.domain.events.events_repository_protocol import EventsRepositoryProtocol
from app.infra.db.repositories.identity_repository import IdentityRepository
from app.domain.identity.identity_repository_protocol import IdentityRepositoryProtocol
from app.infra.db.repositories.subscription_repository import SubscriptionRepository
from app.domain.purchases.subscription_repository_protocol import SubscriptionRepositoryProtocol
from app.infra.db.repositories.user_repository import UserRepository
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol

__all__ = [
    "AppRepository",
    "AppRepositoryProtocol",
    "DailyAggregateRepository",
    "DailyAggregateRepositoryProtocol",
    "EventsRepository",
    "EventsRepositoryProtocol",
    "IdentityRepository",
    "IdentityRepositoryProtocol",
    "SubscriptionRepository",
    "SubscriptionRepositoryProtocol",
    "UserRepository",
    "UserRepositoryProtocol",
]
