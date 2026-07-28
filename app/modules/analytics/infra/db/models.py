from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Numeric, PrimaryKeyConstraint, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base
from app.modules.crm.infra.db.apps.models import AppPlatform, AppUser  # noqa: F401


class AnalyticsClick(Base):
    __tablename__ = "crm_clicks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('accepted', 'redirected', 'duplicate', 'rejected', 'test')",
            name="ck_crm_clicks_status",
        ),
        {"extend_existing": True},
    )

    click_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    app_platform_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_platforms.platform_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    raw_query: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(64), nullable=False)
    region: Mapped[str] = mapped_column(String(64), nullable=False)
    language: Mapped[str] = mapped_column(String(64), nullable=False)
    country_code: Mapped[str] = mapped_column(String(3), nullable=False)
    referrer: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    source: Mapped[str | None] = mapped_column(String(256), nullable=True)
    redirect_target: Mapped[str | None] = mapped_column(Text, nullable=True)
    normalized_params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="accepted", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )


class AnalyticsInstall(Base):
    __tablename__ = "crm_installs"
    __table_args__ = (
        {"extend_existing": True},
    )

    install_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    click_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("crm_clicks.click_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    app_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_users.app_user_id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    app_platform_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_platforms.platform_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    device_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )


class AnalyticsEvent(Base):
    __tablename__ = "crm_events"
    __table_args__ = (
        CheckConstraint(
            "event_type IN ('metric', 'conversion', 'param_update', 'system')",
            name="ck_crm_events_type",
        ),
        {"extend_existing": True},
    )

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    click_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("crm_clicks.click_id", ondelete="RESTRICT"),
        nullable=False,
    )
    app_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_users.app_user_id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    event_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    amount: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    amount_usd: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    event_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class AnalyticsCurrentParam(Base):
    __tablename__ = "crm_current_params"
    __table_args__ = (
        PrimaryKeyConstraint("click_id", "param_key", name="pk_crm_current_params"),
        {"extend_existing": True},
    )

    click_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("crm_clicks.click_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    param_key: Mapped[str] = mapped_column(String(120), primary_key=True, nullable=False)
    value_string: Mapped[str | None] = mapped_column(Text, nullable=True)
    value_number: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    value_bool: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    value_json: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class AnalyticsStatisticsAggregate(Base):
    __tablename__ = "crm_statistics_aggregate"
    __table_args__ = (
        CheckConstraint(
            "event_type IN ('metric', 'conversion')",
            name="ck_crm_statistics_aggregate_event_type",
        ),
        {"extend_existing": True},
    )

    aggregate_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    app_platform_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_platforms.platform_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    geo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    event_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount_usd: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class AnalyticsCustomParamsStatisticsAggregate(Base):
    __tablename__ = "crm_custom_params_statistics"
    __table_args__ = (
        CheckConstraint(
            "event_type IN ('metric', 'conversion')",
            name="ck_crm_params_agg_event_type",
        ),
        {"extend_existing": True},
    )

    aggregate_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    app_platform_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_app_platforms.platform_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    geo: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    event_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    param_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    param_value: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount_usd: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
