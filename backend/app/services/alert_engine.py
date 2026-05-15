from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Alert, Subscription
from app.services.magic_link import as_utc

LEAD_TIMES = (
    ("T-7 days", timedelta(days=7)),
    ("T-3 days", timedelta(days=3)),
    ("T-24 hours", timedelta(hours=24)),
    ("T-2 hours", timedelta(hours=2)),
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def desired_alert_times(
    subscription: Subscription,
    *,
    now: datetime | None = None,
) -> dict[str, datetime]:
    if subscription.next_event_at is None:
        return {}

    current_time = now or utc_now()
    event_at = as_utc(subscription.next_event_at)
    desired: dict[str, datetime] = {}
    for label, delta in LEAD_TIMES:
        alert_at = event_at - delta
        if alert_at > current_time:
            desired[label] = alert_at
    return desired


async def recompute_alerts(
    session: AsyncSession,
    subscription: Subscription,
    *,
    now: datetime | None = None,
) -> tuple[int, int]:
    await session.flush()
    result = await session.execute(
        select(Alert).where(
            Alert.subscription_id == subscription.id,
            Alert.status == "scheduled",
        )
    )
    existing = list(result.scalars())
    desired = desired_alert_times(subscription, now=now)

    created = 0
    cancelled = 0
    kept: set[str] = set()

    for alert in existing:
        desired_time = desired.get(alert.lead_label)
        if desired_time is not None and as_utc(alert.alert_at) == desired_time:
            kept.add(alert.lead_label)
            continue
        alert.status = "cancelled"
        cancelled += 1

    for label, alert_at in desired.items():
        if label in kept:
            continue
        session.add(
            Alert(
                subscription_id=subscription.id,
                user_id=subscription.user_id,
                alert_at=alert_at,
                lead_label=label,
            )
        )
        created += 1

    await session.flush()
    return created, cancelled


async def cancel_pending_alerts(session: AsyncSession, subscription_id: str) -> int:
    result = await session.execute(
        update(Alert)
        .where(Alert.subscription_id == subscription_id, Alert.status == "scheduled")
        .values(status="cancelled")
    )
    return result.rowcount or 0
