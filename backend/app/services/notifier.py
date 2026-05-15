from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Alert, AlertDeliveryLog, NotificationToken, Subscription


def format_amount(subscription: Subscription) -> str:
    if subscription.amount is None or subscription.currency is None:
        return "unknown amount"
    return f"{subscription.amount:.2f} {subscription.currency}"


def build_alert_payload(subscription: Subscription, alert: Alert) -> dict[str, str | None]:
    return {
        "service_name": subscription.service_name,
        "amount": format_amount(subscription),
        "next_event_kind": subscription.next_event_kind or "unknown",
        "next_event_at": subscription.next_event_at.isoformat()
        if subscription.next_event_at is not None
        else None,
        "cancel_by_at": subscription.cancel_by_at.isoformat()
        if subscription.cancel_by_at is not None
        else "unknown",
        "lead_label": alert.lead_label,
        "precision": subscription.precision,
    }


async def send_due_alerts(session: AsyncSession, *, now: datetime | None = None) -> int:
    current_time = now or datetime.now(UTC)
    result = await session.execute(
        select(Alert).where(Alert.status == "scheduled", Alert.alert_at <= current_time)
    )
    sent_count = 0
    for alert in result.scalars():
        subscription = await session.get(Subscription, alert.subscription_id)
        if subscription is None or subscription.deleted_at is not None:
            alert.status = "cancelled"
            continue

        token_result = await session.execute(
            select(NotificationToken).where(
                NotificationToken.user_id == alert.user_id,
                NotificationToken.active.is_(True),
            )
        )
        tokens = list(token_result.scalars())
        if not tokens:
            alert.status = "sent"
            alert.attempts += 1
            alert.sent_at = current_time
            alert.last_error = "No active notification token."
            session.add(
                AlertDeliveryLog(
                    alert_id=alert.id,
                    outcome="skipped_no_token",
                    reason="No active notification token.",
                )
            )
            sent_count += 1
            continue

        alert.status = "sent"
        alert.attempts += 1
        alert.sent_at = current_time
        session.add(
            AlertDeliveryLog(
                alert_id=alert.id,
                outcome="delivered",
                reason=f"Queued {len(tokens)} provider notification.",
            )
        )
        sent_count += 1

    await session.commit()
    return sent_count
