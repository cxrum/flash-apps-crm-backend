from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base


class AuditLog(Base):
    __tablename__ = "crm_audit_logs"

    audit_log_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    app_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    entity_changed: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    entity_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    old_value: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
