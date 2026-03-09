

from sqlalchemy.orm import Session

from app.domain.app.app_repository_protocol import AppRepositoryProtocol
from app.domain.contracts.repository_protocol import RepositoryFactoryProtocol
from app.domain.contracts.user_repository_protocol import UserRepositoryProtocol
from app.domain.events.events_repository_protocol import EventsRepositoryProtocol
from app.domain.identity.identity_repository_protocol import IdentityRepositoryProtocol
from app.domain.purchases.subscription_repository_protocol import SubscriptionRepositoryProtocol
from app.infra.db.repositories.app_repository import AppRepository
from app.infra.db.repositories.events_repository import EventsRepository
from app.infra.db.repositories.identity_repository import IdentityRepository
from app.infra.db.repositories.subscription_repository import SubscriptionRepository
from app.infra.db.repositories.user_repository import UserRepository


class RepositoryFactory(RepositoryFactoryProtocol):
    def app_repo(self, session: Session) -> AppRepositoryProtocol:
        return AppRepository(session)
        
    def user_repo(self, session: Session) -> UserRepositoryProtocol:
        return UserRepository(session)
    
    def identity_repo(self, session: Session) -> IdentityRepositoryProtocol:
        return IdentityRepository(session)
        
    def event_repo(self, session: Session) -> EventsRepositoryProtocol: 
        return EventsRepository(session)    
    
    def subscription_repo(self, session: Session) -> SubscriptionRepositoryProtocol: 
        return SubscriptionRepository(session)