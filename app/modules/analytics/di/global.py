from app.modules.analytics.controller.ingestion import IngestionController
from app.modules.analytics.controller.s2s import S2SController
from app.modules.analytics.controller.tracking import TrackingController
from app.modules.analytics.di.event_bus import get_analytics_event_bus, register_analytics_event_handlers
from app.modules.analytics.session import SessionFactory

get_in_memory_event_bus = get_analytics_event_bus
register_event_handlers = register_analytics_event_handlers


def get_ingestion_controller() -> IngestionController:
    return IngestionController(SessionFactory)


def get_s2s_controller() -> S2SController:
    return S2SController(SessionFactory)


def get_tracking_controller() -> TrackingController:
    return TrackingController(SessionFactory)
