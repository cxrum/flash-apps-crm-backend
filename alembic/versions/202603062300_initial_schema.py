"""initial schema

Revision ID: 202603062300
Revises:
Create Date: 2026-03-06 23:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "202603062300"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "apps",
        sa.Column("app_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_secret_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("app_id"),
    )
    op.create_table(
        "users",
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "identities",
        sa.Column("anonymous_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("anonymous_id"),
    )
    op.create_table(
        "events",
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("event_name", sa.String(length=120), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("platform", sa.String(length=16), nullable=False),
        sa.Column("anonymous_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("source", sa.String(length=120), nullable=True),
        sa.Column("campaign", sa.String(length=120), nullable=True),
        sa.Column("medium", sa.String(length=120), nullable=True),
        sa.Column("params", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.CheckConstraint("platform IN ('android', 'ios')", name="ck_events_platform"),
        sa.ForeignKeyConstraint(["anonymous_id"], ["identities.anonymous_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["app_id"], ["apps.app_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_index("ix_events_app_id", "events", ["app_id"])
    op.create_index("ix_events_event_time", "events", ["event_time"])
    op.create_index("ix_events_platform", "events", ["platform"])
    op.create_index("ix_events_user_id", "events", ["user_id"])

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("platform", sa.String(length=16), nullable=False),
        sa.Column("product_id", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("platform IN ('android', 'ios')", name="ck_subscriptions_platform"),
        sa.ForeignKeyConstraint(["app_id"], ["apps.app_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "app_id",
            "user_id",
            "platform",
            "product_id",
            name="uq_subscriptions_app_user_platform_product",
        ),
    )
    op.create_index("ix_subscriptions_app_id", "subscriptions", ["app_id"])
    op.create_index("ix_subscriptions_user_id", "subscriptions", ["user_id"])
    op.create_index("ix_subscriptions_platform", "subscriptions", ["platform"])
    op.create_index("ix_subscriptions_status", "subscriptions", ["status"])

    op.create_table(
        "daily_aggregates",
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("platform", sa.String(length=16), nullable=False),
        sa.Column("installs", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("signups", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("revenue", sa.Numeric(precision=14, scale=2), nullable=False, server_default="0"),
        sa.Column("active_subs", sa.Integer(), nullable=False, server_default="0"),
        sa.CheckConstraint("platform IN ('android', 'ios')", name="ck_daily_aggregates_platform"),
        sa.ForeignKeyConstraint(["app_id"], ["apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("app_id", "date", "platform", name="pk_daily_aggregates"),
    )


def downgrade() -> None:
    op.drop_table("daily_aggregates")
    op.drop_index("ix_subscriptions_status", table_name="subscriptions")
    op.drop_index("ix_subscriptions_platform", table_name="subscriptions")
    op.drop_index("ix_subscriptions_user_id", table_name="subscriptions")
    op.drop_index("ix_subscriptions_app_id", table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_index("ix_events_user_id", table_name="events")
    op.drop_index("ix_events_platform", table_name="events")
    op.drop_index("ix_events_event_time", table_name="events")
    op.drop_index("ix_events_app_id", table_name="events")
    op.drop_table("events")
    op.drop_table("identities")
    op.drop_table("users")
    op.drop_table("apps")
