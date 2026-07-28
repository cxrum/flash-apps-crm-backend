from fastapi import APIRouter

from app.modules.analytics.api.v1.ingestion.endpoints import router as ingestion_router
from app.modules.analytics.api.v1.s2s.endpoints import router as s2s_router

router = APIRouter()

router.include_router(ingestion_router)
router.include_router(s2s_router)
