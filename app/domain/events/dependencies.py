from sqlalchemy.orm import Session

from app.domain.events.service import EventsDomainService
from app.infra.db.repositories.events_repository import EventsRepository
from app.infra.db.repositories.events_repository_protocol import EventsRepositoryProtocol


from fastapi import Depends

from app.infra.db.session import get_db


def get_events_repository(db: Session = Depends(get_db)) -> EventsRepositoryProtocol:
    return EventsRepository(db)


def get_events_domain_service(
    repository: EventsRepositoryProtocol = Depends(get_events_repository),
) -> EventsDomainService:
    return EventsDomainService(repository)