from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.base import Base


class AppUser(Base):
    __tablename__ = "crm_app_users"
    __table_args__ = (UniqueConstraint("app_user_id", "app_id", name="uq_crm_app_users_platform_external_user"),)
    app_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )


class App(Base):
    __tablename__ = "crm_apps"
    __table_args__ = (CheckConstraint("status IN ('draft', 'active', 'archived')", name="ck_crm_apps_status"),)

    app_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code_slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tech_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active", index=True)
    logo_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    screenshots: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
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


class AppPlatform(Base):
    __tablename__ = "crm_app_platforms"
    __table_args__ = (
        CheckConstraint("platform IN ('android', 'ios')", name="ck_crm_app_platforms_platform"),
        CheckConstraint("status IN ('active', 'inactive')", name="ck_crm_app_platforms_status"),
        UniqueConstraint("app_id", "platform", name="uq_crm_app_platforms_app_platform"),
    )

    platform_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    platform: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    package_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    store_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    install_key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    sdk_public_key: Mapped[str] = mapped_column(String(255), nullable=False)
    sdk_secret_encrypted: Mapped[str] = mapped_column(String(255), nullable=False)
    sdk_secret_fallback_encrypted: Mapped[str] = mapped_column(String(255), nullable=True)
    version_policy: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    current_version: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="active", index=True)
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


class Install(Base):
    __tablename__ = "crm_installs"
    __table_args__ = (UniqueConstraint("app_platform_id", "app_user_id", name="uq_crm_installs_app_user"),)

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
