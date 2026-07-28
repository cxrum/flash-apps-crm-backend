from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.base import Base


class StatisticsAggregate(Base):
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


class CustomParamsStatisticsAggregate(Base):
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
