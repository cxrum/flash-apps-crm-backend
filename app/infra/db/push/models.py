from app.infra.db.base import Base


from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


from datetime import datetime


class PushEvent(Base):
    __tablename__ = "crm_push_events"
    #TODO() Before insert you need to validate campaign.app_id == token.install.app_user.app_id
    __table_args__ = (
        CheckConstraint(
            "event_type IN ('sent', 'delivered', 'opened', 'clicked', 'failed')",
            name="ck_crm_push_events_type",
        ),
    )

    push_event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    campaign_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_push_campaigns.campaign_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_push_tokens.token_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    event_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class PushCampaign(Base):
    __tablename__ = "crm_push_campaigns"
    __table_args__ = (
        CheckConstraint("status IN ('draft', 'scheduled', 'sent', 'cancelled')", name="ck_crm_push_campaigns_status"),
    )

    campaign_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    app_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_apps.app_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    target_link: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    geo_filter: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft", index=True)
    created_by_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("crm_users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
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


class PushToken(Base):
    __tablename__ = "crm_push_tokens"
    

    token_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    install_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("crm_installs.install_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    geo: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

