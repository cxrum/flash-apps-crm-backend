from __future__ import annotations

from datetime import timedelta

from redis.asyncio import Redis

from app.modules.analytics.domain.redis.repo import (
    RedisRepositoryProtocol,
)


class BaseRedisRepository(RedisRepositoryProtocol):
    """Reusable namespaced Redis key-value repository.

    Subclasses only choose a namespace and expose their domain-specific
    operations. Keeping the basic Redis operations here prevents key collisions
    and makes adding another small Redis-backed repository inexpensive.
    """

    def __init__(self, client: Redis, *, namespace: str) -> None:
        if not namespace.strip(":"):
            raise ValueError("Redis namespace cannot be empty")

        self._client = client
        self._namespace = namespace.strip(":")

    @property
    def namespace(self) -> str:
        return self._namespace

    def _key(self, key: str) -> str:
        if not key:
            raise ValueError("Redis key cannot be empty")

        return f"{self._namespace}:{key}"

    @staticmethod
    def _ttl_seconds(ttl: int | timedelta | None) -> int | None:
        if ttl is None:
            return None

        seconds = int(ttl.total_seconds()) if isinstance(ttl, timedelta) else ttl
        if seconds <= 0:
            raise ValueError("Redis TTL must be greater than zero")

        return seconds

    async def get(self, key: str) -> str | None:
        value = await self._client.get(self._key(key))
        if isinstance(value, bytes):
            return value.decode()
        return value

    async def set(
        self,
        key: str,
        value: str,
        *,
        ttl: int | timedelta | None = None,
        only_if_absent: bool = False,
    ) -> bool:
        was_set = await self._client.set(
            self._key(key),
            value,
            ex=self._ttl_seconds(ttl),
            nx=only_if_absent,
        )
        return bool(was_set)

    async def exists(self, key: str) -> bool:
        return bool(await self._client.exists(self._key(key)))

    async def delete(self, key: str) -> bool:
        return bool(await self._client.delete(self._key(key)))
