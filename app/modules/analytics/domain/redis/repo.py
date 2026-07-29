from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from enum import StrEnum
from typing import Protocol


class RedisRepositoryProtocol(Protocol):
    """Small common interface for namespaced Redis key-value repositories."""

    async def get(self, key: str) -> str | None: ...

    async def set(
        self,
        key: str,
        value: str,
        *,
        ttl: int | timedelta | None = None,
        only_if_absent: bool = False,
    ) -> bool: ...

    async def exists(self, key: str) -> bool: ...

    async def delete(self, key: str) -> bool: ...


class IdempotencyKeyStatus(StrEnum):
    PROCESSING = "processing"
    COMPLETED = "completed"


@dataclass(frozen=True)
class IdempotencyKeyClaim:
    status: IdempotencyKeyStatus
    owner_token: str | None = None

    @property
    def is_owner(self) -> bool:
        return self.status is IdempotencyKeyStatus.PROCESSING and self.owner_token is not None


class IdempotencyKeyRepositoryProtocol(Protocol):
    """Coordinates a request key's processing and completed states."""

    async def acquire(self, key: str) -> IdempotencyKeyClaim: ...

    async def complete(self, key: str, owner_token: str) -> bool: ...

    async def release(self, key: str, owner_token: str) -> bool: ...
