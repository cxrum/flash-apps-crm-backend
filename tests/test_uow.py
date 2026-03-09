from __future__ import annotations

import pytest

from app.infra.db.postgres_uow import SqlAlchemyUnitOfWork
from tests.stubs import StubSession


def test_uow_commits_and_closes_session_on_success() -> None:
    session = StubSession()
    uow = SqlAlchemyUnitOfWork(lambda: session)  # type: ignore[arg-type]

    with uow:
        assert uow.session is session

    assert session.commit_calls == 1
    assert session.rollback_calls == 0
    assert session.close_calls == 1
    assert uow.session is None


def test_uow_rolls_back_and_closes_session_on_error() -> None:
    session = StubSession()
    uow = SqlAlchemyUnitOfWork(lambda: session)  # type: ignore[arg-type]

    with pytest.raises(RuntimeError, match="boom"):
        with uow:
            raise RuntimeError("boom")

    assert session.commit_calls == 0
    assert session.rollback_calls == 1
    assert session.close_calls == 1
    assert uow.session is None
