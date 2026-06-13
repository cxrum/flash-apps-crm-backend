from __future__ import annotations

import pytest

from app.modules.crm.domain.uow import UnitOfWorkProtocol
from app.modules.crm.infra.db.puow import SqlAlchemyUnitOfWork
from tests.unit.doubles import StubSession
from tests.unit.doubles.domain.uow import StubRepositoryFactory, StubUnitOfWork


def test_sqlalchemy_uow_commits_closes_and_populates_repositories() -> None:
    session = StubSession()
    backing_uow = StubUnitOfWork()
    repository_factory = StubRepositoryFactory(stub_uow=backing_uow)
    uow = SqlAlchemyUnitOfWork(lambda: session, repository_factory=repository_factory)  # type: ignore[arg-type]
    repository_names = list(UnitOfWorkProtocol.__annotations__)

    with uow as entered:
        assert entered.session is session
        for repository_name in repository_names:
            assert getattr(entered, repository_name) is getattr(backing_uow, repository_name)

    assert session.commit_calls == 1
    assert session.rollback_calls == 0
    assert session.close_calls == 1
    assert uow.session is None
    assert [call.method for call in repository_factory.calls] == repository_names
    assert [call.args for call in repository_factory.calls] == [(session,)] * len(repository_names)


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
