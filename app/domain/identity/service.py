from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.domain.identity.service_protocol import IdentityLinkResult, IdentityServiceProtocol
from app.domain.contracts.identity_repository_protocol import IdentityRepositoryProtocol


class InvalidAnonymousIdError(Exception):
    pass


class IdentityDomainService(IdentityServiceProtocol):
    def __init__(self, repository: IdentityRepositoryProtocol) -> None:
        self.repository = repository

    def link_identity(self, *, anonymous_id: str, user_id: str, linked_at: datetime) -> IdentityLinkResult:
        self._validate_anonymous_id(anonymous_id)

        try:
            self.repository.upsert_user(user_id)
            self.repository.upsert_identity(
                anonymous_id=anonymous_id,
                user_id=user_id,
                linked_at=linked_at,
            )
            self.repository.commit()
        except Exception:
            self.repository.rollback()
            raise

        return IdentityLinkResult(
            status="linked",
            anonymous_id=anonymous_id,
            user_id=user_id,
            linked_at=linked_at,
        )

    def _validate_anonymous_id(self, anonymous_id: str) -> None:
        try:
            UUID(anonymous_id)
        except ValueError as exc:
            raise InvalidAnonymousIdError("anonymous_id must be a valid UUID") from exc

