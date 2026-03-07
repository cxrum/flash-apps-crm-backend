from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.base import Base


class App(Base):
    __tablename__ = "apps"

    app_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Identity(Base):
    __tablename__ = "identities"

    anonymous_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(
        String(128),
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
    )
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("platform IN ('android', 'ios')", name="ck_events_platform"),
    )

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    app_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("apps.app_id", ondelete="CASCADE"), nullable=False)
    event_name: Mapped[str] = mapped_column(String(120), nullable=False)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    platform: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    anonymous_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("identities.anonymous_id", ondelete="RESTRICT"), nullable=False
    )
    user_id: Mapped[str | None] = mapped_column(
        String(128),
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source: Mapped[str | None] = mapped_column(String(120), nullable=True)
    campaign: Mapped[str | None] = mapped_column(String(120), nullable=True)
    medium: Mapped[str | None] = mapped_column(String(120), nullable=True)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint("platform IN ('android', 'ios')", name="ck_subscriptions_platform"),
        UniqueConstraint("app_id", "user_id", "platform", "product_id", name="uq_subscriptions_app_user_platform_product"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("apps.app_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(128), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    platform: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    product_id: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class DailyAggregate(Base):
    __tablename__ = "daily_aggregates"
    __table_args__ = (
        CheckConstraint("platform IN ('android', 'ios')", name="ck_daily_aggregates_platform"),
        PrimaryKeyConstraint("app_id", "date", "platform", name="pk_daily_aggregates"),
    )

    app_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("apps.app_id", ondelete="CASCADE"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    platform: Mapped[str] = mapped_column(String(16), nullable=False)
    installs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    signups: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    revenue: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    active_subs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
