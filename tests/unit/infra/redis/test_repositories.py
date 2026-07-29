from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace

import pytest

from app.modules.analytics.domain.redis.repo import IdempotencyKeyClaim, IdempotencyKeyStatus
from app.modules.analytics.infra.redis.idempotency_repo import RedisIdempotencyKeyRepository
from app.modules.analytics.infra.redis.repo import BaseRedisRepository


class FakeAsyncRedisClient:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.set_calls: list[dict[str, object]] = []

    async def get(self, name: str) -> str | None:
        return self.values.get(name)

    async def set(self, name: str, value: str, *, ex: int | None = None, nx: bool = False) -> bool:
        self.set_calls.append({"name": name, "value": value, "ex": ex, "nx": nx})
        if nx and name in self.values:
            return False

        self.values[name] = value
        return True

    async def exists(self, name: str) -> int:
        return int(name in self.values)

    async def delete(self, *names: str) -> int:
        deleted = 0
        for name in names:
            if name in self.values:
                del self.values[name]
                deleted += 1
        return deleted

    async def eval(self, script: str, numkeys: int, name: str, *args: object) -> int:
        assert numkeys == 1
        value = self.values.get(name)
        if value is None:
            return 0

        state = json.loads(value)
        expected_status, owner_token = args[:2]
        if state.get("status") != expected_status or state.get("owner_token") != owner_token:
            return 0

        if "DEL" in script:
            del self.values[name]
            return 1

        completed_value, ttl = args[2:]
        self.values[name] = str(completed_value)
        self.set_calls.append({"name": name, "value": completed_value, "ex": ttl, "nx": False})
        return 1


def test_base_repository_namespaces_basic_key_value_operations() -> None:
    async def scenario() -> None:
        client = FakeAsyncRedisClient()
        repository = BaseRedisRepository(client, namespace="analytics:cache")

        assert await repository.set("item-1", "value", ttl=30)
        assert client.set_calls == [{"name": "analytics:cache:item-1", "value": "value", "ex": 30, "nx": False}]
        assert await repository.get("item-1") == "value"
        assert await repository.exists("item-1")
        assert await repository.delete("item-1")
        assert not await repository.exists("item-1")

    asyncio.run(scenario())


def test_idempotency_repository_transitions_from_processing_to_completed() -> None:
    async def scenario() -> None:
        client = FakeAsyncRedisClient()
        repository = RedisIdempotencyKeyRepository(
            client,
            SimpleNamespace(redis_idempotency_key_ttl_seconds=12 * 60 * 60),
        )

        claimed = await repository.acquire("request-123")
        duplicate = await repository.acquire("request-123")

        assert claimed.status is IdempotencyKeyStatus.PROCESSING
        assert claimed.owner_token is not None
        assert duplicate == IdempotencyKeyClaim(IdempotencyKeyStatus.PROCESSING)
        assert await repository.complete("request-123", claimed.owner_token)
        assert (await repository.acquire("request-123")).status is IdempotencyKeyStatus.COMPLETED
        assert client.set_calls[0]["ex"] == 12 * 60 * 60
        assert client.set_calls[-1]["ex"] == 12 * 60 * 60

    asyncio.run(scenario())


def test_idempotency_repository_only_allows_the_owner_to_release_or_complete() -> None:
    async def scenario() -> None:
        client = FakeAsyncRedisClient()
        repository = RedisIdempotencyKeyRepository(client, SimpleNamespace(redis_idempotency_key_ttl_seconds=60))
        claimed = await repository.acquire("request-123")

        assert claimed.owner_token is not None
        assert not await repository.complete("request-123", "stale-owner")
        assert not await repository.release("request-123", "stale-owner")
        assert await repository.release("request-123", claimed.owner_token)
        assert (await repository.acquire("request-123")).is_owner

    asyncio.run(scenario())


@pytest.mark.parametrize("ttl", [0, -1])
def test_base_repository_rejects_non_positive_ttl(ttl: int) -> None:
    async def scenario() -> None:
        repository = BaseRedisRepository(FakeAsyncRedisClient(), namespace="analytics:cache")

        with pytest.raises(ValueError, match="TTL"):
            await repository.set("item-1", "value", ttl=ttl)

    asyncio.run(scenario())
