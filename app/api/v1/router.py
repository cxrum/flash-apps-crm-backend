from fastapi import APIRouter
from app.api.v1.crm.router import router as admin_router

router = APIRouter()

router.include_router(router=admin_router, prefix="/admin")
