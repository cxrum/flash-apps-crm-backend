from fastapi import APIRouter


router = APIRouter()


@router.get("/", tags=["health"])
def health_check_v1() -> dict[str, str]:
    return {
        "status": "ok",
        "version": "v1",
        "service": "analytics-api",
    }
