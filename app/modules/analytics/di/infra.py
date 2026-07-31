from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from app.core.config import Settings, settings
from app.core.db.session import SessionFactory
from app.core.redis.redis import create_redis_client
from app.modules.analytics.domain.redis.repo import IdempotencyKeyRepositoryProtocol
from app.modules.analytics.domain.uow import AnalyticsUnitOfWorkFactoryProtocol
from app.modules.analytics.infra.db.puow import SqlAlchemyUnitOfWorkFactory
from app.modules.analytics.infra.redis.idempotency_repo import RedisIdempotencyKeyRepository


def get_analytics_uow_factory() -> AnalyticsUnitOfWorkFactoryProtocol:
    return SqlAlchemyUnitOfWorkFactory(SessionFactory)


@lru_cache(1)
def async_redis_client():
    return create_redis_client()


def get_config() -> Settings:
    return settings


def get_idempotency_repository(
    client: Annotated[Redis, Depends(async_redis_client)],
    config: Annotated[Settings, Depends(get_config)],
) -> IdempotencyKeyRepositoryProtocol:
    return RedisIdempotencyKeyRepository(client, config)
