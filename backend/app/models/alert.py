from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GUID, Base, utc_now


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled','sent','failed','cancelled')", name="ck_alerts_status"
        ),
    )

    id: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    subscription_id: Mapped[str] = mapped_column(
        GUID(), ForeignKey("subscriptions.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[str] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    alert_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    lead_label: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30), default="scheduled")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    subscription = relationship("Subscription", back_populates="alerts")
    user = relationship("User", back_populates="alerts")
    delivery_logs = relationship(
        "AlertDeliveryLog", back_populates="alert", cascade="all, delete-orphan"
    )
