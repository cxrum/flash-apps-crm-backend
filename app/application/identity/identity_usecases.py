from __future__ import annotations

from app.application.identity.entities import LinkIdentityCommand
from app.domain.identity.service_protocol import IdentityServiceProtocol, IdentityLinkResult


class IdentityUseCases:
    def __init__(self, identity_domain_service: IdentityServiceProtocol) -> None:
        self.identity_domain_service = identity_domain_service

    def link_identity(self, command: LinkIdentityCommand) -> IdentityLinkResult:
        return self.identity_domain_service.link_identity(
            anonymous_id=command.anonymous_id,
            user_id=command.user_id,
            linked_at=command.linked_at,
        )

