from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.application.crm_authentication.protocol import CrmAuthenticationProtocol
from app.application.crm_authentication.responses import ResolvedCrmUserResponse
from app.application.crm_authentication.service import CrmAuthentication
from app.di.event_bus import get_in_memory_event_bus, register_event_handlers
from app.di.exception_bus import get_in_memory_exception_event_bus, register_exception_event_handlers
from app.di.infra import get_uow_factory
from app.di.services import get_hash_service
from app.domain.event_bus.service_protocol import (
    IAsyncEventBus,
    IAsyncExceptionBus,
)
from app.domain.hash_protocol import HashProtocol
from app.domain.uow import UnitOfWorkFactoryProtocol


def wire_application_buses(
    event_bus: IAsyncEventBus | None = None,
    exception_bus: IAsyncExceptionBus | None = None,
) -> tuple[IAsyncEventBus, IAsyncExceptionBus]:
    wired_exception_bus = register_exception_event_handlers(
        async_memory_bus=exception_bus,
    )
    wired_event_bus = register_event_handlers(
        async_memory_bus=event_bus,
    )
    
    return wired_event_bus, wired_exception_bus


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncIterator[None]:
    event_bus, exception_bus = wire_application_buses(
        event_bus=get_in_memory_event_bus(),
        exception_bus=get_in_memory_exception_event_bus(),
    )

    await exception_bus.start()
    await event_bus.start()
    
    try:
        yield
    finally:
        await event_bus.stop()
        await exception_bus.stop()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache
def stub_user_resolver(
    uow_factory: UnitOfWorkFactoryProtocol = Depends(get_uow_factory),
    hash_service: HashProtocol = Depends(get_hash_service)
) -> CrmAuthenticationProtocol:
    return CrmAuthentication(
        uow_factory,
        hash_service
    )

def verify_token(token: str = Depends(oauth2_scheme), user_resolver: CrmAuthenticationProtocol = Depends(stub_user_resolver)) -> str:
    return user_resolver.verify_token(token)

def resolve_user(token: str = Depends(oauth2_scheme), user_resolver: CrmAuthenticationProtocol = Depends(stub_user_resolver)) -> ResolvedCrmUserResponse:
    return user_resolver.resolve_user(token)

