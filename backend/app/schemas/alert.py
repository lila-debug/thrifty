from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    id: str
    subscription_id: str
    alert_at: datetime
    lead_label: str
    status: str


class AlertListResponse(BaseModel):
    alerts: list[AlertResponse]


class AlertRecomputeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subscription_id: str | None = None


class AlertRecomputeResponse(BaseModel):
    alerts_created: int
    alerts_cancelled: int
