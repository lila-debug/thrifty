from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import GUID, Base, utc_now


class AuthToken(Base):
    __tablename__ = "auth_tokens"
    __table_args__ = (
        CheckConstraint("purpose IN ('magic_link','session')", name="ck_auth_tokens_purpose"),
    )

    id: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(String(128), unique=True)
    purpose: Mapped[str] = mapped_column(String(30))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="auth_tokens")
