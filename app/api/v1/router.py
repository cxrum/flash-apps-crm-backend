from fastapi import APIRouter

from app.api.v1.admin import router as admin_router
from app.api.v1.events import router as events_router
from app.api.v1.identity import router as identity_router
from app.api.v1.purchases import router as purchases_router

router = APIRouter()
router.include_router(admin_router, prefix="/admin")
router.include_router(events_router, prefix="/events")
router.include_router(identity_router, prefix="/identity")
router.include_router(purchases_router, prefix="/purchases")



@router.get("/health", tags=["v1"])
def health_check_v1() -> dict[str, str]:
    return {
        "status": "ok",
        "version": "v1",
        "service": "analytics-api",
    }


@router.get("/analytics/events", tags=["v1"])
def analytics_events_stub_v1() -> dict[str, object]:
    return {
        "version": "v1",
        "message": "Stub analytics events endpoint for v1",
        "items": [],
    }

