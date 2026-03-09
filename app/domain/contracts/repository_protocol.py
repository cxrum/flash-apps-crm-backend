from typing import Protocol

from sqlalchemy.orm import Session

from app.domain.app.app_repository_protocol import AppRepositoryProtocol
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol
from app.domain.events.events_repository_protocol import EventsRepositoryProtocol
from app.domain.identity.identity_repository_protocol import IdentityRepositoryProtocol
from app.domain.purchases.subscription_repository_protocol import SubscriptionRepositoryProtocol


class RepositoryFactoryProtocol(Protocol):
    def app_repo(self, session: Session) -> AppRepositoryProtocol: ...
    def user_repo(self, session: Session) -> UserRepositoryProtocol: ...
    def identity_repo(self, session: Session) -> IdentityRepositoryProtocol: ...
    def event_repo(self, session: Session) -> EventsRepositoryProtocol: ...
    def subscription_repo(self, session: Session) -> SubscriptionRepositoryProtocol: ...
