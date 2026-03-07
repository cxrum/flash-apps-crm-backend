from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.identity.service import IdentityDomainService
from app.domain.identity.service_protocol import IdentityServiceProtocol
from app.infra.db.repositories.identity_repository import IdentityRepository
from app.infra.db.repositories.identity_repository_protocol import IdentityRepositoryProtocol
from app.infra.db.session import get_db


def get_identity_repository(db: Session = Depends(get_db)) -> IdentityRepositoryProtocol:
    return IdentityRepository(db)


def get_identity_service(
    repository: IdentityRepositoryProtocol = Depends(get_identity_repository),
) -> IdentityServiceProtocol:
    return IdentityDomainService(repository)

