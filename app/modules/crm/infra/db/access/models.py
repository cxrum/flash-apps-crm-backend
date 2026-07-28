from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, PrimaryKeyConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base


class CrmUserAppAccess(Base):
    __tablename__ = "crm_user_app_access"
    __table_args__ = (PrimaryKeyConstraint("user_id", "app_id", "role_id", name="pk_crm_user_app_access"),)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    app_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_roles.role_id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
