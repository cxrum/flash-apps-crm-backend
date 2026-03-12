from __future__ import annotations

import pytest

from app.infra.db.puow import SqlAlchemyUnitOfWork
from tests.unit.doubles import StubSession
from tests.unit.doubles.domain.uow import StubRepositoryFactory, StubUnitOfWork


def test_sqlalchemy_uow_commits_closes_and_populates_repositories() -> None:
    session = StubSession()
    backing_uow = StubUnitOfWork()
    repository_factory = StubRepositoryFactory(stub_uow=backing_uow)
    uow = SqlAlchemyUnitOfWork(lambda: session, repository_factory=repository_factory)  # type: ignore[arg-type]

    with uow as entered:
        assert entered.session is session
        assert entered.app_repo is backing_uow.app_repo
        assert entered.event_repo is backing_uow.event_repo

    assert session.commit_calls == 1
    assert session.rollback_calls == 0
    assert session.close_calls == 1
    assert uow.session is None


def test_sqlalchemy_uow_rolls_back_and_closes_on_error() -> None:
    session = StubSession()
    repository_factory = StubRepositoryFactory(stub_uow=StubUnitOfWork())
    uow = SqlAlchemyUnitOfWork(lambda: session, repository_factory=repository_factory)  # type: ignore[arg-type]

    with pytest.raises(RuntimeError, match="boom"):
        with uow:
            raise RuntimeError("boom")

    assert session.commit_calls == 0
    assert session.rollback_calls == 1
    assert session.close_calls == 1
    assert uow.session is None
