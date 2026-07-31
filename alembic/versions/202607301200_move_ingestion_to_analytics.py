"""Move raw ingestion storage from CRM to Analytics ownership.

Revision ID: 202607301200
Revises: 0d9359a914ee
Create Date: 2026-07-30 12:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op


revision = "202607301200"
down_revision = "0d9359a914ee"
branch_labels = None
depends_on = None


_TABLE_RENAMES = (
    ("crm_clicks", "analytics_clicks"),
    ("crm_installs", "analytics_installs"),
    ("crm_events", "analytics_events"),
    ("crm_current_params", "analytics_current_params"),
    ("crm_statistics_aggregate", "analytics_statistics_aggregate"),
    ("crm_custom_params_statistics", "analytics_custom_params_statistics"),
)

_INDEX_RENAMES = (
    ("ix_crm_clicks_app_platform_id", "ix_analytics_clicks_app_platform_id"),
    ("ix_crm_clicks_status", "ix_analytics_clicks_status"),
    ("ix_crm_clicks_created_at", "ix_analytics_clicks_created_at"),
    ("ix_crm_installs_click_id", "ix_analytics_installs_click_id"),
    ("ix_crm_installs_app_user_id", "ix_analytics_installs_app_user_id"),
    ("ix_crm_installs_app_platform_id", "ix_analytics_installs_app_platform_id"),
    ("ix_crm_installs_installed_at", "ix_analytics_installs_installed_at"),
    ("ix_crm_events_app_user_id", "ix_analytics_events_app_user_id"),
    ("ix_crm_events_event_type", "ix_analytics_events_event_type"),
    ("ix_crm_events_event_key", "ix_analytics_events_event_key"),
    ("ix_crm_events_event_time_utc", "ix_analytics_events_event_time_utc"),
    ("ix_crm_statistics_aggregate_app_platform_id", "ix_analytics_statistics_aggregate_app_platform_id"),
    ("ix_crm_statistics_aggregate_geo", "ix_analytics_statistics_aggregate_geo"),
    ("ix_crm_statistics_aggregate_date", "ix_analytics_statistics_aggregate_date"),
    ("ix_crm_statistics_aggregate_event_type", "ix_analytics_statistics_aggregate_event_type"),
    ("ix_crm_statistics_aggregate_event_key", "ix_analytics_statistics_aggregate_event_key"),
    ("ix_crm_statistics_aggregate_updated_at", "ix_analytics_statistics_aggregate_updated_at"),
    ("ix_crm_custom_params_statistics_app_platform_id", "ix_analytics_custom_params_statistics_app_platform_id"),
    ("ix_crm_custom_params_statistics_geo", "ix_analytics_custom_params_statistics_geo"),
    ("ix_crm_custom_params_statistics_date", "ix_analytics_custom_params_statistics_date"),
    ("ix_crm_custom_params_statistics_event_type", "ix_analytics_custom_params_statistics_event_type"),
    ("ix_crm_custom_params_statistics_event_key", "ix_analytics_custom_params_statistics_event_key"),
    ("ix_crm_custom_params_statistics_param_key", "ix_analytics_custom_params_statistics_param_key"),
    ("ix_crm_custom_params_statistics_param_value", "ix_analytics_custom_params_statistics_param_value"),
)


def upgrade() -> None:
    # CRM may retain opaque click/install IDs in push tokens, but it must not
    # own ORM-level relationships to Analytics' raw ingestion records.
    op.execute("ALTER TABLE crm_push_tokens DROP CONSTRAINT IF EXISTS crm_push_tokens_install_id_fkey")
    op.execute("ALTER TABLE crm_push_tokens DROP CONSTRAINT IF EXISTS crm_push_tokens_click_id_fkey")

    for source, target in _TABLE_RENAMES:
        op.rename_table(source, target)
    for source, target in _INDEX_RENAMES:
        op.execute(f"ALTER INDEX {source} RENAME TO {target}")

    op.execute("ALTER TABLE analytics_clicks RENAME CONSTRAINT ck_crm_clicks_status TO ck_analytics_clicks_status")
    op.execute("ALTER TABLE analytics_installs RENAME CONSTRAINT uq_crm_installs_app_user TO uq_analytics_installs_app_user")
    op.execute("ALTER TABLE analytics_events RENAME CONSTRAINT ck_crm_events_type TO ck_analytics_events_type")
    op.execute("ALTER TABLE analytics_current_params RENAME CONSTRAINT pk_crm_current_params TO pk_analytics_current_params")
    op.execute(
        "ALTER TABLE analytics_statistics_aggregate RENAME CONSTRAINT "
        "ck_crm_statistics_aggregate_event_type TO ck_analytics_statistics_aggregate_event_type"
    )
    op.execute("ALTER TABLE analytics_custom_params_statistics RENAME CONSTRAINT ck_crm_params_agg_event_type TO ck_analytics_params_agg_event_type")


def downgrade() -> None:
    op.execute("ALTER TABLE analytics_clicks RENAME CONSTRAINT ck_analytics_clicks_status TO ck_crm_clicks_status")
    op.execute("ALTER TABLE analytics_installs RENAME CONSTRAINT uq_analytics_installs_app_user TO uq_crm_installs_app_user")
    op.execute("ALTER TABLE analytics_events RENAME CONSTRAINT ck_analytics_events_type TO ck_crm_events_type")
    op.execute("ALTER TABLE analytics_current_params RENAME CONSTRAINT pk_analytics_current_params TO pk_crm_current_params")
    op.execute(
        "ALTER TABLE analytics_statistics_aggregate RENAME CONSTRAINT "
        "ck_analytics_statistics_aggregate_event_type TO ck_crm_statistics_aggregate_event_type"
    )
    op.execute("ALTER TABLE analytics_custom_params_statistics RENAME CONSTRAINT ck_analytics_params_agg_event_type TO ck_crm_params_agg_event_type")

    for source, target in reversed(_INDEX_RENAMES):
        op.execute(f"ALTER INDEX {target} RENAME TO {source}")
    for source, target in reversed(_TABLE_RENAMES):
        op.rename_table(target, source)

    op.create_foreign_key(
        "fk_crm_push_tokens_install_id_crm_installs",
        "crm_push_tokens",
        "crm_installs",
        ["install_id"],
        ["install_id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_crm_push_tokens_click_id_crm_clicks",
        "crm_push_tokens",
        "crm_clicks",
        ["click_id"],
        ["click_id"],
        ondelete="RESTRICT",
    )
