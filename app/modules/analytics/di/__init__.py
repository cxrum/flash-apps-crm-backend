from app.modules.analytics.di.event_bus import get_analytics_event_bus, register_analytics_event_handlers

get_in_memory_event_bus = get_analytics_event_bus
register_event_handlers = register_analytics_event_handlers

__all__ = [
    "get_analytics_event_bus",
    "get_in_memory_event_bus",
    "register_analytics_event_handlers",
    "register_event_handlers",
]
