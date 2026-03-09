
from datetime import datetime

from app.application.events.entities import EventItemCommand, IngestEventsBatchCommand
from app.domain.contracts.repository_protocol import RepositoryFactoryProtocol
from app.application.events.mappers import EventEntityMapper
from app.domain.events.service import EventsDomainService
from app.infra.uow_base import UnitOfWorkProtocol


class EventUseCases:
    def __init__(
        self,
        uow: UnitOfWorkProtocol,
        repository_factory: RepositoryFactoryProtocol,
    ) -> None:
        self.uow = uow
        self.repository_factory = repository_factory

    def process_batch(self, command: IngestEventsBatchCommand):
        events_data: list[EventItemCommand] = command.payload.events
        received = len(events_data)
        sdk_version: str = command.payload.sdk_version
        sent_at: datetime = command.payload.sent_at

        events = [
            EventEntityMapper.from_payload(
                event_data,
                app_id=command.app_id,
                environment=command.env,
                sdk_version=sdk_version,
                sent_at=sent_at,
            )
            for event_data in events_data
        ]

        with self.uow as uow:
            if uow.session is None:
                raise RuntimeError("UoW session is not started")

            event_domain_service = EventsDomainService(
                event_repo=self.repository_factory.event_repo(uow.session),
                app_repo=self.repository_factory.app_repo(uow.session),
                user_repo=self.repository_factory.user_repo(uow.session),
                identity_repo=self.repository_factory.identity_repo(uow.session),
            )

            return event_domain_service.process_batch(
                app_id=command.app_id,
                events=events,
                received=received,
            )
