"""Add Analytics-owned application reference tables.

Revision ID: 202607311200
Revises: 202607301200
Create Date: 2026-07-31 12:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op


revision = "202607311200"
down_revision = "202607301200"
branch_labels = None
depends_on = None


_OLD_PLATFORM_FOREIGN_KEYS = (
    ("analytics_clicks", "crm_clicks_app_platform_id_fkey"),
    ("analytics_installs", "crm_installs_app_platform_id_fkey"),
    ("analytics_statistics_aggregate", "crm_statistics_aggregate_app_platform_id_fkey"),
    ("analytics_custom_params_statistics", "crm_custom_params_statistics_app_platform_id_fkey"),
)

_NEW_PLATFORM_FOREIGN_KEYS = (
    ("fk_analytics_clicks_app_platform", "analytics_clicks"),
    ("fk_analytics_installs_app_platform", "analytics_installs"),
    ("fk_analytics_statistics_aggregate_app_platform", "analytics_statistics_aggregate"),
    ("fk_analytics_custom_params_statistics_app_platform", "analytics_custom_params_statistics"),
)


def upgrade() -> None:
    op.create_table(
        "analytics_apps",
        sa.Column("app_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code_slug", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("app_id"),
        sa.UniqueConstraint("code_slug"),
    )
    op.create_index("ix_analytics_apps_code_slug", "analytics_apps", ["code_slug"])

    op.create_table(
        "analytics_app_platforms",
        sa.Column("platform_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("platform", sa.String(length=16), nullable=False),
        sa.Column("install_key", sa.String(length=128), nullable=False),
        sa.Column("sdk_secret_encrypted", sa.String(length=255), nullable=False),
        sa.CheckConstraint("platform IN ('android', 'ios')", name="ck_analytics_app_platforms_platform"),
        sa.ForeignKeyConstraint(["app_id"], ["analytics_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("platform_id"),
        sa.UniqueConstraint("app_id", "platform", name="uq_analytics_app_platforms_app_platform"),
        sa.UniqueConstraint("install_key"),
    )
    op.create_index("ix_analytics_app_platforms_app_id", "analytics_app_platforms", ["app_id"])
    op.create_index("ix_analytics_app_platforms_platform", "analytics_app_platforms", ["platform"])

    op.execute("INSERT INTO analytics_apps (app_id, code_slug) SELECT app_id, code_slug FROM crm_apps")
    op.execute(
        "INSERT INTO analytics_app_platforms "
        "(platform_id, app_id, platform, install_key, sdk_secret_encrypted) "
        "SELECT platform_id, app_id, platform, install_key, sdk_secret_encrypted FROM crm_app_platforms"
    )
    op.execute(
        "SELECT setval(pg_get_serial_sequence('analytics_apps', 'app_id'), "
        "COALESCE((SELECT MAX(app_id) FROM analytics_apps), 1), true)"
    )
    op.execute(
        "SELECT setval(pg_get_serial_sequence('analytics_app_platforms', 'platform_id'), "
        "COALESCE((SELECT MAX(platform_id) FROM analytics_app_platforms), 1), true)"
    )

    for table_name, constraint_name in _OLD_PLATFORM_FOREIGN_KEYS:
        op.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint_name}")

    for constraint_name, table_name in _NEW_PLATFORM_FOREIGN_KEYS:
        op.create_foreign_key(
            constraint_name,
            table_name,
            "analytics_app_platforms",
            ["app_platform_id"],
            ["platform_id"],
            ondelete="RESTRICT",
        )


def downgrade() -> None:
    for constraint_name, table_name in _NEW_PLATFORM_FOREIGN_KEYS:
        op.drop_constraint(constraint_name, table_name, type_="foreignkey")

    for table_name, constraint_name in _OLD_PLATFORM_FOREIGN_KEYS:
        op.create_foreign_key(
            constraint_name,
            table_name,
            "crm_app_platforms",
            ["app_platform_id"],
            ["platform_id"],
            ondelete="RESTRICT",
        )

    op.drop_index("ix_analytics_app_platforms_platform", table_name="analytics_app_platforms")
    op.drop_index("ix_analytics_app_platforms_app_id", table_name="analytics_app_platforms")
    op.drop_table("analytics_app_platforms")
    op.drop_index("ix_analytics_apps_code_slug", table_name="analytics_apps")
    op.drop_table("analytics_apps")
