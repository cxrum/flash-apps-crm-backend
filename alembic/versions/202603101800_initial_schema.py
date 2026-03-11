"""crm schema

Revision ID: 202603101800
Revises: None
Create Date: 2026-03-10 18:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "202603101800"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "crm_apps",
        sa.Column("app_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("code_slug", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tech_description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("logo_url", sa.String(length=1024), nullable=True),
        sa.Column("screenshots", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("status IN ('draft', 'active', 'archived')", name="ck_crm_apps_status"),
        sa.PrimaryKeyConstraint("app_id"),
    )
    op.create_index("ix_crm_apps_code_slug", "crm_apps", ["code_slug"], unique=True)
    op.create_index("ix_crm_apps_status", "crm_apps", ["status"])

    op.create_table(
        "crm_users",
        sa.Column("user_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index("ix_crm_users_email", "crm_users", ["email"], unique=True)
    op.create_index("ix_crm_users_is_active", "crm_users", ["is_active"])

    op.create_table(
        "crm_roles",
        sa.Column("role_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("role_id"),
    )
    op.create_index("ix_crm_roles_code", "crm_roles", ["code"], unique=True)

    op.create_table(
        "crm_permissions",
        sa.Column("permission_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("permission_id"),
    )
    op.create_index("ix_crm_permissions_code", "crm_permissions", ["code"], unique=True)

    op.create_table(
        "crm_app_platforms",
        sa.Column("platform_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("platform", sa.String(length=16), nullable=False),
        sa.Column("package_name", sa.String(length=255), nullable=False),
        sa.Column("store_url", sa.String(length=1024), nullable=True),
        sa.Column("install_key", sa.String(length=128), nullable=False),
        sa.Column("sdk_public_key", sa.String(length=255), nullable=True),
        sa.Column("sdk_secret_hash", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("platform IN ('android', 'ios')", name="ck_crm_app_platforms_platform"),
        sa.CheckConstraint("status IN ('active', 'inactive')", name="ck_crm_app_platforms_status"),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("platform_id"),
        sa.UniqueConstraint("app_id", "platform", name="uq_crm_app_platforms_app_platform"),
    )
    op.create_index("ix_crm_app_platforms_app_id", "crm_app_platforms", ["app_id"])
    op.create_index("ix_crm_app_platforms_platform", "crm_app_platforms", ["platform"])
    op.create_index("ix_crm_app_platforms_package_name", "crm_app_platforms", ["package_name"])
    op.create_index("ix_crm_app_platforms_status", "crm_app_platforms", ["status"])
    op.create_index("ix_crm_app_platforms_install_key", "crm_app_platforms", ["install_key"], unique=True)

    op.create_table(
        "crm_role_permissions",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["crm_permissions.permission_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["crm_roles.role_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("role_id", "permission_id", name="pk_crm_role_permissions"),
    )

    op.create_table(
        "crm_user_roles",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["crm_roles.role_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role_id", name="pk_crm_user_roles"),
    )

    op.create_table(
        "crm_user_app_access",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("access_level", sa.String(length=32), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("access_level IN ('viewer', 'manager', 'owner')", name="ck_crm_user_app_access_level"),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "app_id", name="pk_crm_user_app_access"),
    )

    op.create_table(
        "crm_app_users",
        sa.Column("app_user_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("app_user_id"),
        sa.UniqueConstraint("app_user_id", "app_id", name="uq_crm_app_users_platform_external_user"),
    )
    op.create_index("ix_crm_app_users_app_id", "crm_app_users", ["app_id"])
    op.create_index("ix_crm_app_users_created_at", "crm_app_users", ["created_at"])

    op.create_table(
        "crm_clicks",
        sa.Column("click_id", sa.String(length=64), nullable=False),
        sa.Column("app_platform_id", sa.BigInteger(), nullable=False),
        sa.Column("raw_query", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("geo", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("referrer", sa.String(length=1024), nullable=True),
        sa.Column("source", sa.String(length=256), nullable=True),
        sa.Column("redirect_target", sa.Text(), nullable=True),
        sa.Column("normalized_params", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "status IN ('accepted', 'redirected', 'duplicate', 'rejected', 'test')",
            name="ck_crm_clicks_status",
        ),
        sa.ForeignKeyConstraint(["app_platform_id"], ["crm_app_platforms.platform_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("click_id"),
    )
    op.create_index("ix_crm_clicks_app_platform_id", "crm_clicks", ["app_platform_id"])
    op.create_index("ix_crm_clicks_status", "crm_clicks", ["status"])
    op.create_index("ix_crm_clicks_created_at", "crm_clicks", ["created_at"])

    op.create_table(
        "crm_installs",
        sa.Column("install_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("click_id", sa.String(length=64), nullable=False),
        sa.Column("app_user_id", sa.BigInteger(), nullable=True),
        sa.Column("app_platform_id", sa.BigInteger(), nullable=False),
        sa.Column("device_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("installed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["app_platform_id"], ["crm_app_platforms.platform_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["app_user_id"], ["crm_app_users.app_user_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["click_id"], ["crm_clicks.click_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("install_id"),
        sa.UniqueConstraint("app_platform_id", "app_user_id", name="uq_crm_installs_app_user"),
    )
    op.create_index("ix_crm_installs_click_id", "crm_installs", ["click_id"])
    op.create_index("ix_crm_installs_app_user_id", "crm_installs", ["app_user_id"])
    op.create_index("ix_crm_installs_app_platform_id", "crm_installs", ["app_platform_id"])
    op.create_index("ix_crm_installs_installed_at", "crm_installs", ["installed_at"])

    op.create_table(
        "crm_events",
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("click_id", sa.String(length=64), nullable=False),
        sa.Column("app_user_id", sa.BigInteger(), nullable=True),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("event_key", sa.String(length=120), nullable=False),
        sa.Column("amount", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.Column("amount_usd", sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column("event_time_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('metric', 'conversion', 'param_update', 'system')",
            name="ck_crm_events_type",
        ),
        sa.ForeignKeyConstraint(["app_user_id"], ["crm_app_users.app_user_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["click_id"], ["crm_clicks.click_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("event_id"),
    )
    op.create_index("ix_crm_events_app_user_id", "crm_events", ["app_user_id"])
    op.create_index("ix_crm_events_event_type", "crm_events", ["event_type"])
    op.create_index("ix_crm_events_event_key", "crm_events", ["event_key"])
    op.create_index("ix_crm_events_event_time_utc", "crm_events", ["event_time_utc"])

    op.create_table(
        "crm_current_params",
        sa.Column("click_id", sa.String(length=64), nullable=False),
        sa.Column("param_key", sa.String(length=120), nullable=False),
        sa.Column("value_string", sa.Text(), nullable=True),
        sa.Column("value_number", sa.Numeric(precision=18, scale=6), nullable=True),
        sa.Column("value_bool", sa.Boolean(), nullable=True),
        sa.Column("value_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["click_id"], ["crm_clicks.click_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("click_id", "param_key", name="pk_crm_current_params"),
    )

    op.create_table(
        "crm_metric_definitions",
        sa.Column("metric_definition_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=True),
        sa.Column("machine_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("visible_in_stats", sa.Boolean(), nullable=False),
        sa.Column("visible_in_logs", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("metric_definition_id"),
        sa.UniqueConstraint("app_id", "machine_key", name="uq_crm_metric_definitions_app_machine_key"),
    )
    op.create_index("ix_crm_metric_definitions_app_id", "crm_metric_definitions", ["app_id"])
    op.create_index("ix_crm_metric_definitions_machine_key", "crm_metric_definitions", ["machine_key"])

    op.create_table(
        "crm_conversion_definitions",
        sa.Column("conversion_definition_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=True),
        sa.Column("machine_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("revenue_enabled", sa.Boolean(), nullable=False),
        sa.Column("expects_amount", sa.Boolean(), nullable=False),
        sa.Column("expects_currency", sa.Boolean(), nullable=False),
        sa.Column("dedup_mode", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "dedup_mode IN ('none', 'click', 'user', 'day')",
            name="ck_crm_conversion_definitions_dedup_mode",
        ),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("conversion_definition_id"),
        sa.UniqueConstraint("app_id", "machine_key", name="uq_crm_conversion_definitions_app_machine_key"),
    )
    op.create_index("ix_crm_conversion_definitions_app_id", "crm_conversion_definitions", ["app_id"])
    op.create_index("ix_crm_conversion_definitions_machine_key", "crm_conversion_definitions", ["machine_key"])

    op.create_table(
        "crm_secret_templates",
        sa.Column("template_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("scope", sa.String(length=32), nullable=False),
        sa.Column("value_type", sa.String(length=32), nullable=False),
        sa.Column("is_masked", sa.Boolean(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "scope IN ('client_public', 'server_private')",
            name="ck_crm_secret_templates_scope",
        ),
        sa.CheckConstraint(
            "value_type IN ('text', 'json', 'file')",
            name="ck_crm_secret_templates_value_type",
        ),
        sa.PrimaryKeyConstraint("template_id"),
    )
    op.create_index("ix_crm_secret_templates_code", "crm_secret_templates", ["code"], unique=True)

    op.create_table(
        "crm_app_secrets",
        sa.Column("secret_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("platform_id", sa.BigInteger(), nullable=True),
        sa.Column("template_id", sa.BigInteger(), nullable=False),
        sa.Column("encrypted_value", sa.Text(), nullable=False),
        sa.Column("active_flag", sa.Boolean(), nullable=False),
        sa.Column("version", sa.Numeric(precision=10, scale=0), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["platform_id"], ["crm_app_platforms.platform_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["template_id"], ["crm_secret_templates.template_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("secret_id"),
        sa.UniqueConstraint(
            "platform_id",
            "template_id",
            "version",
            name="uq_crm_app_secrets_app_platform_template_version",
        ),
    )
    op.create_index("ix_crm_app_secrets_platform_id", "crm_app_secrets", ["platform_id"])
    op.create_index("ix_crm_app_secrets_template_id", "crm_app_secrets", ["template_id"])
    op.create_index("ix_crm_app_secrets_active_flag", "crm_app_secrets", ["active_flag"])

    op.create_table(
        "crm_param_definitions",
        sa.Column("param_definition_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=True),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("machine_key", sa.String(length=120), nullable=False),
        sa.Column("data_type", sa.String(length=32), nullable=False),
        sa.Column("overwrite_policy", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("visible_in_logs", sa.Boolean(), nullable=False),
        sa.Column("visible_in_stats", sa.Boolean(), nullable=False),
        sa.Column("filterable", sa.Boolean(), nullable=False),
        sa.Column("groupable", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "data_type IN ('string', 'integer', 'float', 'boolean', 'date', 'datetime', 'enum', 'json', 'list')",
            name="ck_crm_param_definitions_data_type",
        ),
        sa.CheckConstraint(
            "overwrite_policy IN ('replace', 'append', 'merge')",
            name="ck_crm_param_definitions_overwrite_policy",
        ),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("param_definition_id"),
        sa.UniqueConstraint("app_id", "machine_key", name="uq_crm_param_definitions_app_machine_key"),
    )
    op.create_index("ix_crm_param_definitions_app_id", "crm_param_definitions", ["app_id"])
    op.create_index("ix_crm_param_definitions_machine_key", "crm_param_definitions", ["machine_key"])

    op.create_table(
        "crm_postback_rules",
        sa.Column("rule_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("platfrom_app_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("endpoint_url", sa.String(length=1024), nullable=False),
        sa.Column("http_method", sa.String(length=8), nullable=False),
        sa.Column("headers", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("auth_params", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("timeout", sa.BigInteger(), nullable=False),
        sa.Column("event_key", sa.String(length=120), nullable=True),
        sa.Column("trigger_type", sa.String(length=64), nullable=False),
        sa.Column("template", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("retry_policy", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("http_method IN ('GET', 'POST')", name="ck_crm_postback_rules_http_method"),
        sa.CheckConstraint(
            "trigger_type IN ('install', 'metric', 'conversion', 'param_update')",
            name="ck_crm_postback_rules_trigger_type",
        ),
        sa.ForeignKeyConstraint(["platfrom_app_id"], ["crm_app_platforms.platform_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("rule_id"),
    )
    op.create_index("ix_crm_postback_rules_platfrom_app_id", "crm_postback_rules", ["platfrom_app_id"])
    op.create_index("ix_crm_postback_rules_timeout", "crm_postback_rules", ["timeout"])
    op.create_index("ix_crm_postback_rules_event_key", "crm_postback_rules", ["event_key"])
    op.create_index("ix_crm_postback_rules_trigger_type", "crm_postback_rules", ["trigger_type"])
    op.create_index("ix_crm_postback_rules_is_active", "crm_postback_rules", ["is_active"])

    op.create_table(
        "crm_push_campaigns",
        sa.Column("campaign_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("app_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("image_url", sa.String(length=1024), nullable=True),
        sa.Column("target_link", sa.String(length=1024), nullable=True),
        sa.Column("geo_filter", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_user_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("status IN ('draft', 'scheduled', 'sent', 'cancelled')", name="ck_crm_push_campaigns_status"),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["crm_users.user_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("campaign_id"),
    )
    op.create_index("ix_crm_push_campaigns_app_id", "crm_push_campaigns", ["app_id"])
    op.create_index("ix_crm_push_campaigns_scheduled_at", "crm_push_campaigns", ["scheduled_at"])
    op.create_index("ix_crm_push_campaigns_status", "crm_push_campaigns", ["status"])
    op.create_index("ix_crm_push_campaigns_created_by_user_id", "crm_push_campaigns", ["created_by_user_id"])

    op.create_table(
        "crm_push_tokens",
        sa.Column("token_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("install_id", sa.BigInteger(), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("geo", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["install_id"], ["crm_installs.install_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("token_id"),
    )
    op.create_index("ix_crm_push_tokens_install_id", "crm_push_tokens", ["install_id"])
    op.create_index("ix_crm_push_tokens_token", "crm_push_tokens", ["token"], unique=True)
    op.create_index("ix_crm_push_tokens_is_active", "crm_push_tokens", ["is_active"])

    op.create_table(
        "crm_push_events",
        sa.Column("push_event_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("campaign_id", sa.BigInteger(), nullable=False),
        sa.Column("token_id", sa.BigInteger(), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("event_time_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('sent', 'delivered', 'opened', 'clicked', 'failed')",
            name="ck_crm_push_events_type",
        ),
        sa.ForeignKeyConstraint(["campaign_id"], ["crm_push_campaigns.campaign_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["token_id"], ["crm_push_tokens.token_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("push_event_id"),
    )
    op.create_index("ix_crm_push_events_campaign_id", "crm_push_events", ["campaign_id"])
    op.create_index("ix_crm_push_events_token_id", "crm_push_events", ["token_id"])
    op.create_index("ix_crm_push_events_event_type", "crm_push_events", ["event_type"])
    op.create_index("ix_crm_push_events_event_time_utc", "crm_push_events", ["event_time_utc"])

    op.create_table(
        "crm_audit_logs",
        sa.Column("audit_log_id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("app_id", sa.BigInteger(), nullable=True),
        sa.Column("entity_changed", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.String(length=128), nullable=True),
        sa.Column("old_value", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("new_value", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["app_id"], ["crm_apps.app_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["crm_users.user_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("audit_log_id"),
    )
    op.create_index("ix_crm_audit_logs_user_id", "crm_audit_logs", ["user_id"])
    op.create_index("ix_crm_audit_logs_app_id", "crm_audit_logs", ["app_id"])
    op.create_index("ix_crm_audit_logs_entity_changed", "crm_audit_logs", ["entity_changed"])
    op.create_index("ix_crm_audit_logs_changed_at", "crm_audit_logs", ["changed_at"])


def downgrade() -> None:
    op.drop_index("ix_crm_audit_logs_changed_at", table_name="crm_audit_logs")
    op.drop_index("ix_crm_audit_logs_entity_changed", table_name="crm_audit_logs")
    op.drop_index("ix_crm_audit_logs_app_id", table_name="crm_audit_logs")
    op.drop_index("ix_crm_audit_logs_user_id", table_name="crm_audit_logs")
    op.drop_table("crm_audit_logs")

    op.drop_index("ix_crm_push_events_event_time_utc", table_name="crm_push_events")
    op.drop_index("ix_crm_push_events_event_type", table_name="crm_push_events")
    op.drop_index("ix_crm_push_events_token_id", table_name="crm_push_events")
    op.drop_index("ix_crm_push_events_campaign_id", table_name="crm_push_events")
    op.drop_table("crm_push_events")

    op.drop_index("ix_crm_push_tokens_is_active", table_name="crm_push_tokens")
    op.drop_index("ix_crm_push_tokens_token", table_name="crm_push_tokens")
    op.drop_index("ix_crm_push_tokens_install_id", table_name="crm_push_tokens")
    op.drop_table("crm_push_tokens")

    op.drop_index("ix_crm_push_campaigns_created_by_user_id", table_name="crm_push_campaigns")
    op.drop_index("ix_crm_push_campaigns_status", table_name="crm_push_campaigns")
    op.drop_index("ix_crm_push_campaigns_scheduled_at", table_name="crm_push_campaigns")
    op.drop_index("ix_crm_push_campaigns_app_id", table_name="crm_push_campaigns")
    op.drop_table("crm_push_campaigns")

    op.drop_index("ix_crm_postback_rules_is_active", table_name="crm_postback_rules")
    op.drop_index("ix_crm_postback_rules_trigger_type", table_name="crm_postback_rules")
    op.drop_index("ix_crm_postback_rules_event_key", table_name="crm_postback_rules")
    op.drop_index("ix_crm_postback_rules_timeout", table_name="crm_postback_rules")
    op.drop_index("ix_crm_postback_rules_platfrom_app_id", table_name="crm_postback_rules")
    op.drop_table("crm_postback_rules")

    op.drop_index("ix_crm_param_definitions_machine_key", table_name="crm_param_definitions")
    op.drop_index("ix_crm_param_definitions_app_id", table_name="crm_param_definitions")
    op.drop_table("crm_param_definitions")

    op.drop_index("ix_crm_app_secrets_active_flag", table_name="crm_app_secrets")
    op.drop_index("ix_crm_app_secrets_template_id", table_name="crm_app_secrets")
    op.drop_index("ix_crm_app_secrets_platform_id", table_name="crm_app_secrets")
    op.drop_table("crm_app_secrets")

    op.drop_index("ix_crm_secret_templates_code", table_name="crm_secret_templates")
    op.drop_table("crm_secret_templates")

    op.drop_index("ix_crm_conversion_definitions_machine_key", table_name="crm_conversion_definitions")
    op.drop_index("ix_crm_conversion_definitions_app_id", table_name="crm_conversion_definitions")
    op.drop_table("crm_conversion_definitions")

    op.drop_index("ix_crm_metric_definitions_machine_key", table_name="crm_metric_definitions")
    op.drop_index("ix_crm_metric_definitions_app_id", table_name="crm_metric_definitions")
    op.drop_table("crm_metric_definitions")

    op.drop_table("crm_current_params")

    op.drop_index("ix_crm_events_event_time_utc", table_name="crm_events")
    op.drop_index("ix_crm_events_event_key", table_name="crm_events")
    op.drop_index("ix_crm_events_event_type", table_name="crm_events")
    op.drop_index("ix_crm_events_app_user_id", table_name="crm_events")
    op.drop_table("crm_events")

    op.drop_index("ix_crm_installs_installed_at", table_name="crm_installs")
    op.drop_index("ix_crm_installs_app_platform_id", table_name="crm_installs")
    op.drop_index("ix_crm_installs_app_user_id", table_name="crm_installs")
    op.drop_index("ix_crm_installs_click_id", table_name="crm_installs")
    op.drop_table("crm_installs")

    op.drop_index("ix_crm_clicks_created_at", table_name="crm_clicks")
    op.drop_index("ix_crm_clicks_status", table_name="crm_clicks")
    op.drop_index("ix_crm_clicks_app_platform_id", table_name="crm_clicks")
    op.drop_table("crm_clicks")

    op.drop_index("ix_crm_app_users_created_at", table_name="crm_app_users")
    op.drop_index("ix_crm_app_users_app_id", table_name="crm_app_users")
    op.drop_table("crm_app_users")

    op.drop_table("crm_user_app_access")
    op.drop_table("crm_user_roles")
    op.drop_table("crm_role_permissions")

    op.drop_index("ix_crm_app_platforms_install_key", table_name="crm_app_platforms")
    op.drop_index("ix_crm_app_platforms_status", table_name="crm_app_platforms")
    op.drop_index("ix_crm_app_platforms_package_name", table_name="crm_app_platforms")
    op.drop_index("ix_crm_app_platforms_platform", table_name="crm_app_platforms")
    op.drop_index("ix_crm_app_platforms_app_id", table_name="crm_app_platforms")
    op.drop_table("crm_app_platforms")

    op.drop_index("ix_crm_permissions_code", table_name="crm_permissions")
    op.drop_table("crm_permissions")

    op.drop_index("ix_crm_roles_code", table_name="crm_roles")
    op.drop_table("crm_roles")

    op.drop_index("ix_crm_users_is_active", table_name="crm_users")
    op.drop_index("ix_crm_users_email", table_name="crm_users")
    op.drop_table("crm_users")

    op.drop_index("ix_crm_apps_status", table_name="crm_apps")
    op.drop_index("ix_crm_apps_code_slug", table_name="crm_apps")
    op.drop_table("crm_apps")
