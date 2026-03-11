from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.application.identity.entities import LinkIdentityCommand
from app.application.identity.identity_usecases import IdentityUseCases
from app.di.dependencies import get_identity_usecases
from app.domain.identity.service import InvalidAnonymousIdError
from app.domain.identity.service_protocol import IdentityLinkResult
from app.infra.db.puow import SqlAlchemyUnitOfWork
from app.main import app
from tests.stubs import IdentityOnlyRepositoryFactory, StubSession


@dataclass
class StubIdentityUseCases:
    result: IdentityLinkResult | None = None
    error: Exception | None = None

    def link_identity(self, command: LinkIdentityCommand) -> IdentityLinkResult:
        if self.error is not None:
            raise self.error
        if self.result is None:
            raise RuntimeError("Stub result was not provided")
        return self.result


def test_identity_api_success() -> None:
    linked_at = datetime(2026, 3, 8, 12, 0, 0, tzinfo=UTC)
    use_case_stub = StubIdentityUseCases(
        result=IdentityLinkResult(
            status="linked",
            anonymous_id="4f2f5f49-9f58-4274-bf5f-0e0b0895a44e",
            user_id="user-1",
            linked_at=linked_at,
        )
    )
    app.dependency_overrides[get_identity_usecases] = lambda: use_case_stub

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/identity",
                json={
                    "anonymous_id": "4f2f5f49-9f58-4274-bf5f-0e0b0895a44e",
                    "user_id": "user-1",
                    "linked_at": linked_at.isoformat(),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["status"] == "linked"


def test_identity_api_returns_400_on_invalid_anonymous_id() -> None:
    use_case_stub = StubIdentityUseCases(
        error=InvalidAnonymousIdError("anonymous_id must be a valid UUID")
    )
    app.dependency_overrides[get_identity_usecases] = lambda: use_case_stub

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/identity",
                json={
                    "anonymous_id": "not-a-uuid",
                    "user_id": "user-1",
                    "linked_at": datetime(2026, 3, 8, 12, 0, 0, tzinfo=UTC).isoformat(),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "anonymous_id must be a valid UUID"


def test_identity_use_case_rolls_back_transaction_on_repository_error() -> None:
    session = StubSession()
    uow = SqlAlchemyUnitOfWork(lambda: session)  # type: ignore[arg-type]
    use_cases = IdentityUseCases(uow=uow, repository_factory=IdentityOnlyRepositoryFactory()) # type: ignore
    command = LinkIdentityCommand(
        anonymous_id="4f2f5f49-9f58-4274-bf5f-0e0b0895a44e",
        user_id="user-1",
        linked_at=datetime(2026, 3, 8, 12, 0, 0, tzinfo=UTC),
    )

    with pytest.raises(RuntimeError, match="identity upsert failed"):
        use_cases.link_identity(command)

    assert session.commit_calls == 0
    assert session.rollback_calls == 1
    assert session.close_calls == 1
