"""add statistics aggregates

Revision ID: 202603191320
Revises: 202603101800
Create Date: 2026-03-19 13:20:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "202603191320"
down_revision = "202603101800"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "crm_statistics_aggregate",
        sa.Column("aggregate_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_platform_id", sa.BigInteger(), nullable=False),
        sa.Column("geo", sa.String(length=32), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("event_key", sa.String(length=120), nullable=False),
        sa.Column("count", sa.BigInteger(), nullable=False),
        sa.Column("amount_usd", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('metric', 'conversion')",
            name="ck_crm_statistics_aggregate_event_type",
        ),
        sa.ForeignKeyConstraint(["app_platform_id"], ["crm_app_platforms.platform_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("aggregate_id"),
    )
    op.create_index("ix_crm_statistics_aggregate_app_platform_id", "crm_statistics_aggregate", ["app_platform_id"])
    op.create_index("ix_crm_statistics_aggregate_geo", "crm_statistics_aggregate", ["geo"])
    op.create_index("ix_crm_statistics_aggregate_date", "crm_statistics_aggregate", ["date"])
    op.create_index("ix_crm_statistics_aggregate_event_type", "crm_statistics_aggregate", ["event_type"])
    op.create_index("ix_crm_statistics_aggregate_event_key", "crm_statistics_aggregate", ["event_key"])
    op.create_index("ix_crm_statistics_aggregate_updated_at", "crm_statistics_aggregate", ["updated_at"])

    op.create_table(
        "crm_custom_params_statistics",
        sa.Column("aggregate_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_platform_id", sa.BigInteger(), nullable=False),
        sa.Column("geo", sa.String(length=32), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("event_key", sa.String(length=120), nullable=False),
        sa.Column("param_key", sa.String(length=120), nullable=False),
        sa.Column("param_value", sa.Text(), nullable=False),
        sa.Column("count", sa.BigInteger(), nullable=False),
        sa.Column("amount_usd", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('metric', 'conversion')",
            name="ck_crm_params_agg_event_type",
        ),
        sa.ForeignKeyConstraint(["app_platform_id"], ["crm_app_platforms.platform_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("aggregate_id"),
    )
    op.create_index(
        "ix_crm_custom_params_statistics_app_platform_id",
        "crm_custom_params_statistics",
        ["app_platform_id"],
    )
    op.create_index("ix_crm_custom_params_statistics_geo", "crm_custom_params_statistics", ["geo"])
    op.create_index("ix_crm_custom_params_statistics_date", "crm_custom_params_statistics", ["date"])
    op.create_index("ix_crm_custom_params_statistics_event_type", "crm_custom_params_statistics", ["event_type"])
    op.create_index("ix_crm_custom_params_statistics_event_key", "crm_custom_params_statistics", ["event_key"])
    op.create_index("ix_crm_custom_params_statistics_param_key", "crm_custom_params_statistics", ["param_key"])
    op.create_index("ix_crm_custom_params_statistics_param_value", "crm_custom_params_statistics", ["param_value"])


def downgrade() -> None:
    op.drop_index("ix_crm_custom_params_statistics_param_value", table_name="crm_custom_params_statistics")
    op.drop_index("ix_crm_custom_params_statistics_param_key", table_name="crm_custom_params_statistics")
    op.drop_index("ix_crm_custom_params_statistics_event_key", table_name="crm_custom_params_statistics")
    op.drop_index("ix_crm_custom_params_statistics_event_type", table_name="crm_custom_params_statistics")
    op.drop_index("ix_crm_custom_params_statistics_date", table_name="crm_custom_params_statistics")
    op.drop_index("ix_crm_custom_params_statistics_geo", table_name="crm_custom_params_statistics")
    op.drop_index("ix_crm_custom_params_statistics_app_platform_id", table_name="crm_custom_params_statistics")
    op.drop_table("crm_custom_params_statistics")

    op.drop_index("ix_crm_statistics_aggregate_updated_at", table_name="crm_statistics_aggregate")
    op.drop_index("ix_crm_statistics_aggregate_event_key", table_name="crm_statistics_aggregate")
    op.drop_index("ix_crm_statistics_aggregate_event_type", table_name="crm_statistics_aggregate")
    op.drop_index("ix_crm_statistics_aggregate_date", table_name="crm_statistics_aggregate")
    op.drop_index("ix_crm_statistics_aggregate_geo", table_name="crm_statistics_aggregate")
    op.drop_index("ix_crm_statistics_aggregate_app_platform_id", table_name="crm_statistics_aggregate")
    op.drop_table("crm_statistics_aggregate")
