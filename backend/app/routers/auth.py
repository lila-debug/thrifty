from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db import get_session
from app.schemas.auth import (
    AuthStartRequest,
    AuthStartResponse,
    AuthUser,
    AuthVerifyRequest,
    AuthVerifyResponse,
)
from app.services.magic_link import (
    LinkConsumed,
    LinkInvalid,
    TooManyLinksRequested,
    issue_magic_link,
    verify_magic_link,
)

router = APIRouter(prefix="/v1/auth", tags=["auth"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.post("/start", response_model=AuthStartResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_auth(
    payload: AuthStartRequest,
    session: SessionDep,
    settings: SettingsDep,
) -> AuthStartResponse:
    try:
        await issue_magic_link(session, settings, payload.email)
    except TooManyLinksRequested as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many links requested. Try again in an hour.",
        ) from exc
    return AuthStartResponse(status="sent")


@router.post("/verify", response_model=AuthVerifyResponse)
async def verify_auth(
    payload: AuthVerifyRequest,
    session: SessionDep,
    settings: SettingsDep,
) -> AuthVerifyResponse:
    try:
        session_token, user = await verify_magic_link(session, settings, payload.token)
    except LinkConsumed as exc:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Link already used.") from exc
    except LinkInvalid as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Link invalid or expired.",
        ) from exc

    return AuthVerifyResponse(
        session_token=session_token,
        user=AuthUser(id=user.id, email=user.email, tier=user.tier),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
