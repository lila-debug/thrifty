from __future__ import annotations

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.deps import CurrentUserDep, SessionDep
from app.models import Alert, Subscription
from app.schemas.alert import (
    AlertListResponse,
    AlertRecomputeRequest,
    AlertRecomputeResponse,
    AlertResponse,
)
from app.services.alert_engine import recompute_alerts

router = APIRouter(prefix="/v1/alerts", tags=["alerts"])
StatusQuery = Annotated[str | None, Query()]
FromQuery = Annotated[datetime | None, Query(alias="from")]


def to_response(alert: Alert) -> AlertResponse:
    return AlertResponse(
        id=alert.id,
        subscription_id=alert.subscription_id,
        alert_at=alert.alert_at,
        lead_label=alert.lead_label,
        status=alert.status,
    )


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    user: CurrentUserDep,
    session: SessionDep,
    status: StatusQuery = None,
    from_at: FromQuery = None,
) -> AlertListResponse:
    statement = select(Alert).where(Alert.user_id == user.id)
    if status is not None:
        statement = statement.where(Alert.status == status)
    if from_at is not None:
        statement = statement.where(Alert.alert_at >= from_at)
    statement = statement.order_by(Alert.alert_at)
    result = await session.execute(statement)
    return AlertListResponse(alerts=[to_response(alert) for alert in result.scalars()])


@router.post("/recompute", response_model=AlertRecomputeResponse)
async def recompute(
    payload: AlertRecomputeRequest,
    user: CurrentUserDep,
    session: SessionDep,
) -> AlertRecomputeResponse:
    statement = select(Subscription).where(
        Subscription.user_id == user.id,
        Subscription.deleted_at.is_(None),
    )
    if payload.subscription_id is not None:
        statement = statement.where(Subscription.id == payload.subscription_id)

    result = await session.execute(statement)
    created = cancelled = 0
    for subscription in result.scalars():
        made, stopped = await recompute_alerts(session, subscription)
        created += made
        cancelled += stopped

    await session.commit()
    return AlertRecomputeResponse(alerts_created=created, alerts_cancelled=cancelled)
