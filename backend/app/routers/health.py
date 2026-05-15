from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import __version__
from app.db import get_session

router = APIRouter(tags=["health"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/health")
async def health(session: SessionDep) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ok", "db": "ok", "version": __version__}
