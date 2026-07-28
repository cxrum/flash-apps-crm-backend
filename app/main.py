from fastapi import FastAPI

from app.core.bus.di import (
    build_application_lifespan,
    get_in_memory_event_bus,
    get_in_memory_exception_event_bus,
    register_exception_event_handlers,
)
from app.core.config import settings
from app.modules.analytics.api.router import api_router as analytics_api_router
from app.modules.analytics.api.v1.admin.stats import router as analytics_stats_router
from app.modules.analytics.di.event_bus import get_analytics_event_bus, register_analytics_event_handlers
from app.modules.crm.api.router import api_router
from app.modules.crm.di.event_bus import register_event_handlers
from app.modules.crm.di.exception_bus import (
    register_fastapi_exception_handlers,
)

application_lifespan = build_application_lifespan(
    event_bus_factory=get_in_memory_event_bus,
    exception_bus_factory=get_in_memory_exception_event_bus,
    event_handlers_registrar=register_event_handlers,
    exception_handlers_registrar=register_exception_event_handlers,
    extra_event_buses=((get_analytics_event_bus, register_analytics_event_handlers),),
)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Base FastAPI project with API versioning and Docker support.",
    lifespan=application_lifespan,
)

app.include_router(api_router)
app.include_router(analytics_stats_router, prefix="/api/v1/admin/stats")
app.include_router(analytics_api_router)

register_fastapi_exception_handlers(app)
