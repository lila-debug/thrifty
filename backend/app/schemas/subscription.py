from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Source = Literal["storekit", "play_billing", "plaid", "manual"]
Cadence = Literal["weekly", "monthly", "quarterly", "semi_annual", "annual", "custom"]
Status = Literal["trial", "active", "cancelled", "expired", "unknown"]
EventKind = Literal["renewal", "trial_conversion", "unknown"]
Precision = Literal["exact", "estimated", "unknown"]


class SubscriptionBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_name: str | None = None
    amount: Decimal | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    cadence: Cadence | None = None
    custom_period_days: int | None = Field(default=None, gt=0)
    status: Status | None = None
    trial_ends_at: datetime | None = None
    next_event_at: datetime | None = None
    next_event_kind: EventKind | None = None
    precision: Precision | None = None
    cancel_by_at: datetime | None = None
    cancel_url: str | None = None
    terms_raw: str | None = None
    terms_plain: str | None = None
    notes: str | None = None

    @field_validator("currency")
    @classmethod
    def normalise_currency(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.upper()


class SubscriptionCreate(SubscriptionBase):
    service_name: str


class SubscriptionPatch(SubscriptionBase):
    pass


class SubscriptionResponse(BaseModel):
    id: str
    service_name: str
    source: Source
    source_product_id: str | None
    amount: Decimal | None
    currency: str | None
    cadence: Cadence | None
    custom_period_days: int | None
    status: Status
    trial_ends_at: datetime | None
    next_event_at: datetime | None
    next_event_kind: EventKind | None
    precision: Precision
    cancel_by_at: datetime | None
    cancel_url: str | None
    terms_plain: str | None
    notes: str | None


class SubscriptionListResponse(BaseModel):
    subscriptions: list[SubscriptionResponse]


class PlatformSnapshot(SubscriptionCreate):
    source_product_id: str


class PlatformSyncRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    platform: Literal["storekit", "play_billing"]
    snapshots: list[PlatformSnapshot]


class PlatformSyncResponse(BaseModel):
    created: int
    updated: int
    unchanged: int
