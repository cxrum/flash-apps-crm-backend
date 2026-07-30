from __future__ import annotations

from itertools import count

from app.modules.analytics.domain.redis.repo import (
    IdempotencyKeyClaim,
    IdempotencyKeyStatus,
)


class StubIdempotencyKeyRepository:
    def __init__(self) -> None:
        self._states: dict[str, tuple[IdempotencyKeyStatus, str | None]] = {}
        self._tokens = count(1)
        self._next_acquire_status: IdempotencyKeyStatus | None = None
        self._next_completion_result: bool | None = None

    def return_processing_for_next_request(self) -> None:
        self._next_acquire_status = IdempotencyKeyStatus.PROCESSING

    def fail_next_completion(self) -> None:
        self._next_completion_result = False

    async def acquire(self, key: str) -> IdempotencyKeyClaim:
        if self._next_acquire_status is not None:
            status = self._next_acquire_status
            self._next_acquire_status = None
            return IdempotencyKeyClaim(status=status)

        state = self._states.get(key)
        if state is not None:
            return IdempotencyKeyClaim(status=state[0])

        owner_token = f"owner-{next(self._tokens)}"
        self._states[key] = (IdempotencyKeyStatus.PROCESSING, owner_token)
        return IdempotencyKeyClaim(IdempotencyKeyStatus.PROCESSING, owner_token)

    async def complete(self, key: str, owner_token: str) -> bool:
        if self._next_completion_result is not None:
            result = self._next_completion_result
            self._next_completion_result = None
            return result

        if self._states.get(key) != (IdempotencyKeyStatus.PROCESSING, owner_token):
            return False

        self._states[key] = (IdempotencyKeyStatus.COMPLETED, None)
        return True

    async def release(self, key: str, owner_token: str) -> bool:
        if self._states.get(key) != (IdempotencyKeyStatus.PROCESSING, owner_token):
            return False

        del self._states[key]
        return True
