from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import CHAR, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TypeDecorator


class GUID(TypeDecorator[str]):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=False))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value: str | None, dialect) -> str | None:
        if value is None:
            return None
        return str(uuid.UUID(str(value)))

    def process_result_value(self, value: str | None, dialect) -> str | None:
        if value is None:
            return None
        return str(value)


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    type_annotation_map = {str: CHAR}


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
