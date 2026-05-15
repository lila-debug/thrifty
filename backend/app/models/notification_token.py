from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GUID, Base, utc_now


class NotificationToken(Base):
    __tablename__ = "notification_tokens"
    __table_args__ = (
        CheckConstraint("platform IN ('ios','android')", name="ck_notification_tokens_platform"),
        UniqueConstraint("user_id", "token", name="uq_notification_tokens_user_token"),
    )

    id: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    platform: Mapped[str] = mapped_column(String(20))
    token: Mapped[str] = mapped_column(String(512))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="notification_tokens")
