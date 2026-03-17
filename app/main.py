import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.core.config import settings
from app.di.dependencies import SHARED_ASYNC_MEMORY_BUS


@asynccontextmanager
async def lifespan(app: FastAPI):
    await SHARED_ASYNC_MEMORY_BUS.start()
    yield
    await SHARED_ASYNC_MEMORY_BUS.stop()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Base FastAPI project with API versioning and Docker support.",
    lifespan=lifespan
)

app.include_router(api_router)
