from sqlalchemy.dialects.postgresql import JSONB

from app.infra.db.base import Base


from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


from datetime import datetime


class MetricDefinition(Base):
    __tablename__ = "crm_metric_definitions"
    __table_args__ = (
        UniqueConstraint("app_id", "machine_key", name="uq_crm_metric_definitions_app_machine_key"),
    )

    metric_definition_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    machine_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    visible_in_stats: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    visible_in_logs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class ConversionDefinition(Base):
    __tablename__ = "crm_conversion_definitions"
    __table_args__ = (
        CheckConstraint(
            "dedup_mode IN ('none', 'click', 'user', 'day')",
            name="ck_crm_conversion_definitions_dedup_mode",
        ),
        UniqueConstraint("app_id", "machine_key", name="uq_crm_conversion_definitions_app_machine_key"),
    )

    conversion_definition_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    machine_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    revenue_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expects_amount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expects_currency: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    dedup_mode: Mapped[str] = mapped_column(String(32), nullable=False, default="none")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class ParamDefinition(Base):
    __tablename__ = "crm_param_definitions"
    __table_args__ = (
        CheckConstraint(
            "data_type IN ('string', 'integer', 'float', 'boolean', 'date', 'datetime', 'enum', 'json', 'list')",
            name="ck_crm_param_definitions_data_type",
        ),
        CheckConstraint(
            "overwrite_policy IN ('replace', 'append', 'merge')",
            name="ck_crm_param_definitions_overwrite_policy",
        ),
        UniqueConstraint("app_id", "machine_key", name="uq_crm_param_definitions_app_machine_key"),
    )

    param_definition_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    machine_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    data_type: Mapped[str] = mapped_column(String(32), nullable=False)
    overwrite_policy: Mapped[str] = mapped_column(String(32), nullable=False, default="replace")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    visible_in_logs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    visible_in_stats: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    filterable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    groupable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

class SecretTemplate(Base):
    __tablename__ = "crm_secret_templates"
    __table_args__ = (
        CheckConstraint(
            "scope IN ('client_public', 'server_private')",
            name="ck_crm_secret_templates_scope",
        ),
        CheckConstraint(
            "value_type IN ('text', 'json','file')",
            name="ck_crm_secret_templates_value_type",
        ),
    )

    template_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    scope: Mapped[str] = mapped_column(String(32), nullable=False)
    value_type: Mapped[str] = mapped_column(String(32), nullable=False)
    is_masked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class PostbackRule(Base):
    __tablename__ = "crm_postback_rules"
    __table_args__ = (
        CheckConstraint("http_method IN ('GET', 'POST')", name="ck_crm_postback_rules_http_method"),
        CheckConstraint("trigger_type IN ('install', 'metric', 'conversion', 'param_update')", name="ck_crm_postback_rules_trigger_type"),
    )

    rule_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    platfrom_app_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_platforms.platform_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False) 
    
    endpoint_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    http_method: Mapped[str] = mapped_column(String(8), nullable=False, default="POST")
    
    headers: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    auth_params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    timeout: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0, index=True)
    
    # Field when Event.event_key == PostbackRule.event_key then posback rule will be launched 
    event_key: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)

    # Field when Event.event_type == PostbackRule.triger_event_type then posback rule will be launched 
    trigger_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    
    template: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    retry_policy: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class AppSecret(Base):
    __tablename__ = "crm_app_secrets"
    __table_args__ = (
        UniqueConstraint(
            "platform_id",
            "template_id",
            "version",
            name="uq_crm_app_secrets_app_platform_template_version",
        ),
    )

    secret_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    platform_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_platforms.platform_id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    template_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_secret_templates.template_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    encrypted_value: Mapped[str] = mapped_column(Text, nullable=False)
    active_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    version: Mapped[float] = mapped_column(Numeric(10, 0), nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
