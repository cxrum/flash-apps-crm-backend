from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.core.config import Settings
from app.modules.crm.infra.services import ip2location as ip2location_module


class _FakeDatabase:
    def __init__(self, path: str, *, calls: dict[str, object]) -> None:
        self._path = path
        self._calls = calls

    def get_all(self, ip: str) -> SimpleNamespace:
        self._calls["path"] = self._path
        self._calls["ip"] = ip
        return SimpleNamespace(
            city="Paris",
            country_long="France",
            country_short="FR",
        )


def test_resolve_reads_from_configured_database_and_maps_location_fields(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: dict[str, object] = {}

    monkeypatch.setattr(ip2location_module.IP2Location, "IP2Location", lambda path: _FakeDatabase(path, calls=calls))

    gateway = ip2location_module.IP2LocationGateway(settings.ip2location_bin_database_path)
    location = gateway.resolve("203.0.113.10")

    assert calls == {
        "path": settings.ip2location_bin_database_path,
        "ip": "203.0.113.10",
    }
    assert location.city == "Paris"
    assert location.country == "France"
    assert location.country_code == "FR"
