from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class NotificationTokenCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    platform: Literal["ios", "android"]
    token: str


class NotificationTokenResponse(BaseModel):
    id: str
    platform: str
    active: bool
