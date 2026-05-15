from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GUID, Base, utc_now


class AlertDeliveryLog(Base):
    __tablename__ = "alert_delivery_log"
    __table_args__ = (
        CheckConstraint(
            "outcome IN ("
            "'delivered','failed_token_invalid','failed_provider',"
            "'failed_network','skipped_no_token'"
            ")",
            name="ck_alert_delivery_log_outcome",
        ),
    )

    id: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    alert_id: Mapped[str] = mapped_column(
        GUID(), ForeignKey("alerts.id", ondelete="CASCADE"), index=True
    )
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    outcome: Mapped[str] = mapped_column(String(40))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    alert = relationship("Alert", back_populates="delivery_logs")
