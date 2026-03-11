from app.infra.db.base import Base


from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, PrimaryKeyConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column


from datetime import datetime


class CrmUserAppAccess(Base):
    __tablename__ = "crm_user_app_access"
    __table_args__ = (
        CheckConstraint("access_level IN ('viewer', 'manager', 'owner')", name="ck_crm_user_app_access_level"),
        PrimaryKeyConstraint("user_id", "app_id", name="pk_crm_user_app_access"),
    )

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
    access_level: Mapped[str] = mapped_column(String(32), nullable=False, default="manager")
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )