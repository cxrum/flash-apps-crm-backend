from __future__ import annotations

from app.application.identity.entities import LinkIdentityCommand
from app.domain.contracts.repository_protocol import RepositoryFactoryProtocol
from app.domain.identity.service import IdentityDomainService
from app.domain.identity.service_protocol import IdentityLinkResult
from app.infra.uow_base import UnitOfWorkProtocol


class IdentityUseCases:
    def __init__(self, uow: UnitOfWorkProtocol, repository_factory: RepositoryFactoryProtocol) -> None:
        self.uow = uow
        self.repository_factory = repository_factory

    def link_identity(self, command: LinkIdentityCommand) -> IdentityLinkResult:
        with self.uow as uow:
            if uow.session is None:
                raise RuntimeError("UoW session is not started")

            identity_domain_service = IdentityDomainService(
                self.repository_factory.identity_repo(uow.session)
            )
            
            return identity_domain_service.link_identity(
                anonymous_id=command.anonymous_id,
                user_id=command.user_id,
                linked_at=command.linked_at,
            )
