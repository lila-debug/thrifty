from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CHAR, CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GUID, Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("tier IN ('free','plus')", name="ck_users_tier"),)

    id: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    timezone: Mapped[str] = mapped_column(String(80), default="Europe/London")
    locale: Mapped[str] = mapped_column(String(20), default="en-GB")
    default_currency: Mapped[str] = mapped_column(CHAR(3), default="GBP")
    tier: Mapped[str] = mapped_column(String(20), default="free")
    session_revoked_after: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    auth_tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship(
        "Subscription", back_populates="user", cascade="all, delete-orphan"
    )
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    notification_tokens = relationship(
        "NotificationToken", back_populates="user", cascade="all, delete-orphan"
    )
