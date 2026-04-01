from app.infra.db.base import Base


from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, PrimaryKeyConstraint, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column


from datetime import datetime


class CrmUser(Base):
    __tablename__ = "crm_users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    time_zone: Mapped[str] = mapped_column(String(64), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
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


class CrmRole(Base):
    __tablename__ = "crm_roles"

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class CrmPermission(Base):
    __tablename__ = "crm_permissions"

    permission_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class CrmUserPermissions(Base):
    __tablename__ = "crm_user_permisions"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "permission_id", "app_id", name="pk_crm_user_permision"),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    permission_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_permissions.permission_id", ondelete="CASCADE"),
        nullable=False,
    )
    app_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
