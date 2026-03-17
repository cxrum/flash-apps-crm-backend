import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.core.config import settings
from app.di.dependencies import SHARED_ASYNC_MEMORY_BUS, get_event_subscribers, get_in_memory_event_bus, register_event_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    bus = get_in_memory_event_bus()
    register_event_handlers(get_event_subscribers(), bus)
    
    await bus.start()
    try:
        yield
    finally:
        await bus.stop()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Base FastAPI project with API versioning and Docker support.",
    lifespan=lifespan
)

app.include_router(api_router)
