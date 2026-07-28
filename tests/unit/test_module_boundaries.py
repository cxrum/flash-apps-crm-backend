from __future__ import annotations

from pathlib import Path


def test_crm_module_does_not_import_analytics_module() -> None:
    crm_root = Path("app/modules/crm")
    offenders: list[str] = []

    for path in crm_root.rglob("*.py"):
        text = path.read_text()
        if "app.modules.analytics" in text:
            offenders.append(str(path))

    assert offenders == []
