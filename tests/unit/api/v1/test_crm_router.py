from __future__ import annotations

from fastapi.routing import APIRoute

from app.modules.crm.api.v1.crm.router import router as crm_router


def _route_counts() -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}

    for route in crm_router.routes:
        if not isinstance(route, APIRoute):
            continue

        for method in route.methods:
            if method in {"HEAD", "OPTIONS"}:
                continue

            key = (route.path, method)
            counts[key] = counts.get(key, 0) + 1

    return counts


def test_crm_router_registers_cleaned_routes_once() -> None:
    route_counts = _route_counts()

    assert all(count == 1 for count in route_counts.values())

    expected_routes = {
        ("/app/", "GET"),
        ("/app/{app_id}", "GET"),
        ("/app/{app_id}/platform/{platform_id}", "PATCH"),
        ("/audit/", "GET"),
        ("/conversion/{conversion_definition_id}", "DELETE"),
        ("/metric/{metric_definition_id}", "PATCH"),
        ("/param/{param_definition_id}", "DELETE"),
        ("/postback/{postback_id}", "GET"),
        ("/postback/{postback_id}", "PATCH"),
        ("/push/{push_id}/start", "POST"),
        ("/role/share", "POST"),
        ("/role/share/{role_code}", "GET"),
        ("/secret/template", "GET"),
        ("/secret/template/{template_id}", "PATCH"),
        ("/secret/{secret_id}", "DELETE"),
        ("/stats/logs/events", "GET"),
    }

    for route_key in expected_routes:
        assert route_counts.get(route_key) == 1
