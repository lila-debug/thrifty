from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GUID, Base, TimestampMixin


class Subscription(TimestampMixin, Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint(
            "source IN ('storekit','play_billing','plaid','manual')", name="ck_subscriptions_source"
        ),
        CheckConstraint(
            "cadence IN ('weekly','monthly','quarterly','semi_annual','annual','custom')",
            name="ck_subscriptions_cadence",
        ),
        CheckConstraint(
            "status IN ('trial','active','cancelled','expired','unknown')",
            name="ck_subscriptions_status",
        ),
        CheckConstraint(
            "next_event_kind IN ('renewal','trial_conversion','unknown')",
            name="ck_subscriptions_event_kind",
        ),
        CheckConstraint(
            "precision IN ('exact','estimated','unknown')",
            name="ck_subscriptions_precision",
        ),
        UniqueConstraint(
            "user_id", "source", "source_product_id", name="uq_subscriptions_source_product"
        ),
    )

    id: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    source: Mapped[str] = mapped_column(String(30))
    source_product_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    service_name: Mapped[str] = mapped_column(String(255))
    amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(CHAR(3), nullable=True)
    cadence: Mapped[str | None] = mapped_column(String(30), nullable=True)
    custom_period_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="unknown")
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_event_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_event_kind: Mapped[str | None] = mapped_column(String(30), nullable=True)
    precision: Mapped[str] = mapped_column(String(30), default="unknown")
    cancel_by_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancel_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    terms_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    terms_plain: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="subscriptions")
    alerts = relationship("Alert", back_populates="subscription", cascade="all, delete-orphan")
