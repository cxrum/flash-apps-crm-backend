from fastapi import APIRouter

from app.modules.analytics.api.v1.tracking.endpoints import router as tracking_router
from app.modules.crm.api.authentication.authentication import router as authentication_router
from app.modules.crm.api.health.health import router as health_router
from app.modules.crm.api.v1.router import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/api/v1")
api_router.include_router(tracking_router)
api_router.include_router(authentication_router)
api_router.include_router(health_router, prefix="/health")
