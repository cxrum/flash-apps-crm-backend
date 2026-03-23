from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.di.dependencies import application_lifespan


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Base FastAPI project with API versioning and Docker support.",
    lifespan=application_lifespan,
)

app.include_router(api_router)
