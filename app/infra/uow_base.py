from __future__ import annotations

from types import TracebackType
from typing import Protocol

from sqlalchemy.orm import Session


class UnitOfWorkProtocol(Protocol):
    session: Session | None

    def __enter__(self) -> "UnitOfWorkProtocol": ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

