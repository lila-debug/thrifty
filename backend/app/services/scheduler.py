from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.services.notifier import send_due_alerts


def build_scheduler(session_factory: async_sessionmaker) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    async def tick() -> None:
        async with session_factory() as session:
            await send_due_alerts(session)

    scheduler.add_job(tick, "interval", seconds=60, id="send_due_alerts", replace_existing=True)
    return scheduler
