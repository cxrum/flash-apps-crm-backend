from __future__ import annotations

from collections.abc import Callable
from types import TracebackType

from sqlalchemy.orm import Session

from app.infra.uow_base import UnitOfWorkProtocol


class SqlAlchemyUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.session is not None:
                self.session.close()
                self.session = None

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW session is not started")
        self.session.commit()

    def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UoW session is not started")
        self.session.rollback()
