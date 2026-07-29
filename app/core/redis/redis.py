from __future__ import annotations

from app.core.config import settings


def create_redis_client():
    from redis.asyncio import Redis

    return Redis.from_url(settings.redis_uri, decode_responses=True)
