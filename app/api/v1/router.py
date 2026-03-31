from fastapi import APIRouter
from app.api.v1.crm.router import router as admin_router
from app.api.v1.s2s.s2s import router as s2s_router
from app.api.v1.sdk.sdk import router as sdk_router

router = APIRouter()

router.include_router(router=sdk_router, prefix="/sdk")
router.include_router(router=s2s_router, prefix="/s2s")
router.include_router(router=admin_router, prefix="/admin")
