from fastapi import APIRouter

from app.modules.analytics.api.v1.ingestion.endpoints import router as ingestion_router
from app.modules.analytics.api.v1.s2s.endpoints import router as s2s_router
from app.modules.analytics.api.v1.tracking.endpoints import router as tracking_router

api_router = APIRouter()
api_router.include_router(ingestion_router, prefix="/ingestion/v1")
api_router.include_router(s2s_router, prefix="/ingestion/v1")
api_router.include_router(tracking_router)
