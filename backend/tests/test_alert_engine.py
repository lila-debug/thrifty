from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Alert, Subscription, User
from app.services.alert_engine import cancel_pending_alerts, recompute_alerts
from app.services.magic_link import as_utc


async def make_subscription(
    session: AsyncSession,
    *,
    next_event_at: datetime | None,
    precision: str = "exact",
    currency: str = "GBP",
) -> Subscription:
    user = User(email=f"user-{datetime.now(UTC).timestamp()}@example.com")
    session.add(user)
    await session.flush()
    subscription = Subscription(
        user_id=user.id,
        source="manual",
        service_name="Test Service",
        amount="10.99",
        currency=currency,
        cadence="monthly",
        status="active",
        next_event_at=next_event_at,
        next_event_kind="renewal" if next_event_at else None,
        precision=precision,
    )
    session.add(subscription)
    await session.flush()
    return subscription


async def alerts_for(session: AsyncSession, subscription: Subscription) -> list[Alert]:
    result = await session.execute(
        select(Alert)
        .where(Alert.subscription_id == subscription.id)
        .order_by(Alert.alert_at, Alert.lead_label)
    )
    return list(result.scalars())


@pytest.mark.asyncio
async def test_alert_engine_creates_four_lead_times(db_session: AsyncSession) -> None:
    now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    subscription = await make_subscription(db_session, next_event_at=now + timedelta(days=10))

    created, cancelled = await recompute_alerts(db_session, subscription, now=now)
    alerts = await alerts_for(db_session, subscription)

    assert (created, cancelled) == (4, 0)
    assert [alert.lead_label for alert in alerts] == [
        "T-7 days",
        "T-3 days",
        "T-24 hours",
        "T-2 hours",
    ]


@pytest.mark.asyncio
async def test_alert_engine_skips_lead_times_already_in_past(db_session: AsyncSession) -> None:
    now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    subscription = await make_subscription(db_session, next_event_at=now + timedelta(hours=4))

    created, cancelled = await recompute_alerts(db_session, subscription, now=now)
    alerts = await alerts_for(db_session, subscription)

    assert (created, cancelled) == (1, 0)
    assert [alert.lead_label for alert in alerts] == ["T-2 hours"]


@pytest.mark.asyncio
async def test_alert_engine_schedules_no_alerts_without_event_time(
    db_session: AsyncSession,
) -> None:
    subscription = await make_subscription(db_session, next_event_at=None)

    created, cancelled = await recompute_alerts(db_session, subscription)

    assert (created, cancelled) == (0, 0)
    assert await alerts_for(db_session, subscription) == []


@pytest.mark.asyncio
async def test_alert_engine_cancels_superseded_alerts(db_session: AsyncSession) -> None:
    now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    subscription = await make_subscription(db_session, next_event_at=now + timedelta(days=10))
    await recompute_alerts(db_session, subscription, now=now)

    subscription.next_event_at = now + timedelta(days=12)
    created, cancelled = await recompute_alerts(db_session, subscription, now=now)
    alerts = await alerts_for(db_session, subscription)

    assert (created, cancelled) == (4, 4)
    assert len([alert for alert in alerts if alert.status == "scheduled"]) == 4
    assert len([alert for alert in alerts if alert.status == "cancelled"]) == 4


@pytest.mark.asyncio
async def test_deleted_subscription_cancels_pending_alerts(db_session: AsyncSession) -> None:
    now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    subscription = await make_subscription(db_session, next_event_at=now + timedelta(days=10))
    await recompute_alerts(db_session, subscription, now=now)

    stopped = await cancel_pending_alerts(db_session, subscription.id)
    alerts = await alerts_for(db_session, subscription)

    assert stopped == 4
    assert {alert.status for alert in alerts} == {"cancelled"}


@pytest.mark.asyncio
async def test_timezone_event_keeps_utc_alert_times(db_session: AsyncSession) -> None:
    now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    user = User(email="sydney@example.com", timezone="Australia/Sydney")
    db_session.add(user)
    await db_session.flush()
    subscription = Subscription(
        user_id=user.id,
        source="manual",
        service_name="Sydney Service",
        status="active",
        precision="exact",
        next_event_at=now + timedelta(days=10),
        next_event_kind="renewal",
    )
    db_session.add(subscription)
    await db_session.flush()

    await recompute_alerts(db_session, subscription, now=now)
    alerts = await alerts_for(db_session, subscription)

    assert as_utc(alerts[0].alert_at).tzinfo == UTC
    assert as_utc(alerts[0].alert_at) == now + timedelta(days=3)


@pytest.mark.asyncio
@pytest.mark.parametrize("currency", ["GBP", "CAD", "EUR", "AUD", "ZAR"])
async def test_multi_currency_amounts_round_trip(
    authed_client: AsyncClient,
    currency: str,
) -> None:
    response = await authed_client.post(
        "/v1/subscriptions",
        json={
            "service_name": f"{currency} Service",
            "amount": "12.34",
            "currency": currency,
        },
    )

    assert response.status_code == 201
    assert response.json()["amount"] == "12.34"
    assert response.json()["currency"] == currency


@pytest.mark.asyncio
async def test_unknown_precision_still_schedules_alerts(db_session: AsyncSession) -> None:
    now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    subscription = await make_subscription(
        db_session,
        next_event_at=now + timedelta(days=10),
        precision="unknown",
    )

    created, _ = await recompute_alerts(db_session, subscription, now=now)

    assert created == 4
