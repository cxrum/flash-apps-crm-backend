from __future__ import annotations

import app.infra.db.models  # noqa: F401
from app.infra.db.base import Base


def test_crm_tables_are_registered_in_metadata() -> None:
    expected_tables = {
        "crm_apps",
        "crm_app_platforms",
        "crm_users",
        "crm_roles",
        "crm_permissions",
        "crm_role_permissions",
        "crm_user_roles",
        "crm_user_app_access",
        "crm_clicks",
        "crm_app_users",
        "crm_installs",
        "crm_events",
        "crm_current_params",
        "crm_metric_definitions",
        "crm_conversion_definitions",
        "crm_secret_templates",
        "crm_app_secrets",
        "crm_param_definitions",
        "crm_postback_rules",
        "crm_push_campaigns",
        "crm_push_tokens",
        "crm_push_events",
        "crm_audit_logs",
    }

    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(actual_tables)


def test_crm_foreign_key_graph_is_defined() -> None:
    expected_fk_graph = {
        "crm_app_platforms": {"crm_apps"},
        "crm_role_permissions": {"crm_roles", "crm_permissions"},
        "crm_user_roles": {"crm_users", "crm_roles"},
        "crm_user_app_access": {"crm_users", "crm_apps"},
        "crm_clicks": {"crm_app_platforms"},
        "crm_app_users": {"crm_apps"},
        "crm_installs": {"crm_app_users", "crm_clicks", "crm_app_platforms"},
        "crm_events": {"crm_installs"},
        "crm_current_params": {"crm_clicks"},
        "crm_metric_definitions": {"crm_apps"},
        "crm_conversion_definitions": {"crm_apps"},
        "crm_app_secrets": {"crm_app_platforms", "crm_secret_templates"},
        "crm_param_definitions": {"crm_apps"},
        "crm_postback_rules": {"crm_apps"},
        "crm_push_campaigns": {"crm_apps", "crm_users"},
        "crm_push_tokens": {"crm_installs"},
        "crm_push_events": {"crm_push_campaigns", "crm_push_tokens"},
        "crm_audit_logs": {"crm_users", "crm_apps"},
    }

    for table_name, expected_targets in expected_fk_graph.items():
        table = Base.metadata.tables[table_name]
        actual_targets = {fk.column.table.name for fk in table.foreign_keys}
        assert actual_targets == expected_targets
