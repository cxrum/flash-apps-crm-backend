from __future__ import annotations

import json
from uuid import uuid4

from redis.asyncio import Redis

from app.core.config import Settings
from app.modules.analytics.domain.redis.repo import (
    IdempotencyKeyClaim,
    IdempotencyKeyRepositoryProtocol,
    IdempotencyKeyStatus,
)
from app.modules.analytics.infra.redis.repo import BaseRedisRepository


class RedisIdempotencyKeyRepository(BaseRedisRepository, IdempotencyKeyRepositoryProtocol):
    """Owner-safe Redis state machine for idempotency keys."""

    _COMPLETE_SCRIPT = """
local value = redis.call('GET', KEYS[1])
if not value then return 0 end
local state = cjson.decode(value)
if state.status ~= ARGV[1] or state.owner_token ~= ARGV[2] then return 0 end
redis.call('SET', KEYS[1], ARGV[3], 'EX', ARGV[4])
return 1
"""
    _RELEASE_SCRIPT = """
local value = redis.call('GET', KEYS[1])
if not value then return 0 end
local state = cjson.decode(value)
if state.status ~= ARGV[1] or state.owner_token ~= ARGV[2] then return 0 end
return redis.call('DEL', KEYS[1])
"""

    def __init__(
        self,
        client: Redis,
        settings: Settings,
        *,
        namespace: str = "analytics:idempotency",
    ) -> None:
        self.settings = settings
        super().__init__(client, namespace=namespace)

    def _encode(self, status: IdempotencyKeyStatus, owner_token: str | None = None) -> str:
        value: dict[str, str] = {"status": status.value}
        if owner_token is not None:
            value["owner_token"] = owner_token
        return json.dumps(value, separators=(",", ":"), sort_keys=True)

    @staticmethod
    def _decode(value: str | None) -> IdempotencyKeyStatus:
        if value is None:
            return IdempotencyKeyStatus.PROCESSING

        try:
            return IdempotencyKeyStatus(json.loads(value)["status"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            # Existing pre-state-machine keys are conservatively treated as in-flight.
            return IdempotencyKeyStatus.PROCESSING

    async def acquire(self, key: str) -> IdempotencyKeyClaim:
        owner_token = uuid4().hex
        acquired = await self.set(
            key,
            self._encode(IdempotencyKeyStatus.PROCESSING, owner_token),
            ttl=self.settings.redis_idempotency_key_ttl_seconds,
            only_if_absent=True,
        )
        if acquired:
            return IdempotencyKeyClaim(IdempotencyKeyStatus.PROCESSING, owner_token)

        return IdempotencyKeyClaim(self._decode(await self.get(key)))

    async def complete(self, key: str, owner_token: str) -> bool:
        result = await self._client.eval(
            self._COMPLETE_SCRIPT,
            1,
            self._key(key),
            IdempotencyKeyStatus.PROCESSING.value,
            owner_token,
            self._encode(IdempotencyKeyStatus.COMPLETED),
            self.settings.redis_idempotency_key_ttl_seconds,
        )
        return bool(result)

    async def release(self, key: str, owner_token: str) -> bool:
        result = await self._client.eval(
            self._RELEASE_SCRIPT,
            1,
            self._key(key),
            IdempotencyKeyStatus.PROCESSING.value,
            owner_token,
        )
        return bool(result)
