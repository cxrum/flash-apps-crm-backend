from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class RecordedCall:
    method: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


def clone(value: T) -> T:
    return deepcopy(value)


def utcnow() -> datetime:
    return datetime.now(tz=UTC)


def comparable_datetime(value: date | None) -> date:
    return value or datetime.min.replace(tzinfo=UTC)


def evolve(entity: T, **changes: Any) -> T:
    return replace(entity, **changes) # type: ignore


class IntegerSequence:
    def __init__(self, *, start: int = 1) -> None:
        self._value = start

    def next(self) -> int:
        current = self._value
        self._value += 1
        return current

    def observe(self, value: int) -> None:
        if value >= self._value:
            self._value = value + 1


class CallRecorderMixin:
    def __init__(self) -> None:
        self.calls: list[RecordedCall] = []

    def _record(self, method: str, *args: Any, **kwargs: Any) -> None:
        self.calls.append(RecordedCall(method=method, args=args, kwargs=dict(kwargs))) # type: ignore

    def reset_calls(self) -> None:
        self.calls.clear()


class StubSession(CallRecorderMixin):
    def __init__(self) -> None:
        super().__init__()
        self.commit_calls = 0
        self.rollback_calls = 0
        self.close_calls = 0

    def commit(self) -> None:
        self.commit_calls += 1
        self._record("commit")

    def rollback(self) -> None:
        self.rollback_calls += 1
        self._record("rollback")

    def close(self) -> None:
        self.close_calls += 1
        self._record("close")
