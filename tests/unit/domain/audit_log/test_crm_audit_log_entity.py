from datetime import UTC, datetime

import pytest

from app.domain.audit_log.CrmAuditLogEntity import CrmAuditLogEntity


def test_create_from_diff_builds_audit_logs_for_changed_top_level_entities() -> None:
    changed_at = datetime(2026, 6, 9, tzinfo=UTC)

    audit_logs = CrmAuditLogEntity.create_from_diff(
        {
            "crm_apps": {
                "name": "old",
                "settings": {"enabled": True, "limit": 10},
                "removed": "value",
            },
            "crm_users": {"email": "same@example.com"},
        },
        {
            "crm_apps": {
                "name": "new",
                "settings": {"enabled": True, "limit": 20},
                "added": "value",
            },
            "crm_users": {"email": "same@example.com"},
        },
        user_id=1,
        app_id=2,
        entity_id=3,
        changed_at=changed_at,
    )

    assert audit_logs == [
        CrmAuditLogEntity(
            entity_changed="crm_apps",
            user_id=1,
            app_id=2,
            entity_id="3",
            old_value={
                "name": "old",
                "settings": {"limit": 10},
                "removed": "value",
                "added": None,
            },
            new_value={
                "name": "new",
                "settings": {"limit": 20},
                "removed": None,
                "added": "value",
            },
            changed_at=changed_at,
        )
    ]


def test_create_from_diff_builds_single_audit_log_for_explicit_entity() -> None:
    audit_logs = CrmAuditLogEntity.create_from_diff(
        {"name": "old", "settings": {"enabled": False}},
        {"name": "new", "settings": {"enabled": True}},
        entity_changed="crm_apps",
        entity_id="app-1",
    )

    assert audit_logs == [
        CrmAuditLogEntity(
            entity_changed="crm_apps",
            entity_id="app-1",
            old_value={"name": "old", "settings": {"enabled": False}},
            new_value={"name": "new", "settings": {"enabled": True}},
        )
    ]


def test_create_from_diff_returns_empty_list_without_changes() -> None:
    assert (
        CrmAuditLogEntity.create_from_diff(
            {"crm_apps": {"name": "same"}},
            {"crm_apps": {"name": "same"}},
        )
        == []
    )


def test_create_from_diff_requires_entity_name_for_non_dict_values() -> None:
    with pytest.raises(ValueError, match="entity_changed is required"):
        CrmAuditLogEntity.create_from_diff(["old"], ["new"])


def test_create_from_diff_ignores_configured_fields_recursively() -> None:
    assert (
        CrmAuditLogEntity.create_from_diff(
            {
                "crm_apps": {
                    "name": "same",
                    "updated_at": "2026-06-10T10:00:00+00:00",
                    "settings": {"updated_at": "old"},
                }
            },
            {
                "crm_apps": {
                    "name": "same",
                    "updated_at": "2026-06-10T11:00:00+00:00",
                    "settings": {"updated_at": "new"},
                }
            },
            ignore_fields=("updated_at",),
        )
        == []
    )
