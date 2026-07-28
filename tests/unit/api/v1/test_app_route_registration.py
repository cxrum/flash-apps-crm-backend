from __future__ import annotations

from fastapi.routing import APIRoute

from app.main import app


def _route_counts() -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue

        for method in route.methods:
            if method in {"HEAD", "OPTIONS"}:
                continue
            key = (route.path, method)
            counts[key] = counts.get(key, 0) + 1

    return counts


def test_app_registers_analytics_public_routes_once() -> None:
    route_counts = _route_counts()

    expected_routes = {
        ("/ingestion/v1/install", "POST"),
        ("/ingestion/v1/events", "POST"),
        ("/ingestion/v1/params/update", "POST"),
        ("/ingestion/v1/config", "GET"),
        ("/ingestion/v1/click", "POST"),
        ("/r/{app_code}/{platform}", "GET"),
    }

    for route_key in expected_routes:
        assert route_counts.get(route_key) == 1


def test_app_preserves_crm_admin_prefix() -> None:
    route_counts = _route_counts()

    assert route_counts.get(("/api/v1/admin/app/", "GET")) == 1
    assert route_counts.get(("/api/v1/admin/stats/logs/events", "GET")) == 1
