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


def test_analytics_raw_ingestion_does_not_depend_on_removed_crm_domain_models() -> None:
    analytics_root = Path("app/modules/analytics")
    forbidden_imports = (
        "app.modules.crm.domain.click",
        "app.modules.crm.domain.events",
        "app.modules.crm.domain.install",
        "app.modules.crm.domain.current_param",
        "app.modules.crm.domain.statistics_aggregate",
        "app.modules.crm.domain.custom_params_statistics_aggregate",
    )

    offenders = [
        str(path)
        for path in analytics_root.rglob("*.py")
        if any(import_path in path.read_text() for import_path in forbidden_imports)
    ]

    assert offenders == []
