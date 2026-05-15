from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Alert, AlertDeliveryLog, Subscription
from app.services.magic_link import last_issued_token
from app.services.notifier import build_alert_payload, send_due_alerts


@pytest.mark.asyncio
async def test_trial_conversion_alert_flow(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await client.post("/v1/auth/start", json={"email": "trial@example.com"})
    token = last_issued_token("trial@example.com")
    verified = await client.post("/v1/auth/verify", json={"token": token})
    session_token = verified.json()["session_token"]
    client.headers.update({"Authorization": f"Bearer {session_token}"})

    event_at = datetime.now(UTC) + timedelta(hours=25)
    created = await client.post(
        "/v1/subscriptions",
        json={
            "service_name": "Trial Box",
            "amount": "19.99",
            "currency": "CAD",
            "status": "trial",
            "trial_ends_at": event_at.isoformat(),
            "next_event_at": event_at.isoformat(),
            "next_event_kind": "trial_conversion",
            "precision": "exact",
        },
    )
    assert created.status_code == 201

    alert_result = await db_session.execute(
        select(Alert).order_by(Alert.alert_at, Alert.lead_label)
    )
    alerts = list(alert_result.scalars())
    assert [alert.lead_label for alert in alerts] == ["T-24 hours", "T-2 hours"]

    subscription = await db_session.get(Subscription, alerts[0].subscription_id)
    assert subscription is not None
    payload = build_alert_payload(subscription, alerts[0])
    assert payload["service_name"] == "Trial Box"
    assert payload["amount"] == "19.99 CAD"
    assert payload["next_event_kind"] == "trial_conversion"
    assert payload["cancel_by_at"] == "unknown"

    sent = await send_due_alerts(db_session, now=alerts[0].alert_at + timedelta(seconds=1))
    log_result = await db_session.execute(select(AlertDeliveryLog))
    log = log_result.scalar_one()
    refreshed = await db_session.get(Alert, alerts[0].id)

    assert sent == 1
    assert refreshed is not None
    assert refreshed.status == "sent"
    assert log.outcome == "skipped_no_token"
