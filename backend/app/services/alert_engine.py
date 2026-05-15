from __future__ import annotations

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Alert, Subscription


async def recompute_alerts(
    session: AsyncSession,
    subscription: Subscription,
) -> tuple[int, int]:
    await session.flush()
    return (0, 0)


async def cancel_pending_alerts(session: AsyncSession, subscription_id: str) -> int:
    result = await session.execute(
        update(Alert)
        .where(Alert.subscription_id == subscription_id, Alert.status == "scheduled")
        .values(status="cancelled")
    )
    return result.rowcount or 0
