from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy import select

from app.deps import CurrentUserDep, SessionDep
from app.models import NotificationToken
from app.schemas.notification import NotificationTokenCreate, NotificationTokenResponse

router = APIRouter(prefix="/v1/notifications", tags=["notifications"])


@router.post(
    "/token", response_model=NotificationTokenResponse, status_code=status.HTTP_201_CREATED
)
async def register_token(
    payload: NotificationTokenCreate,
    user: CurrentUserDep,
    session: SessionDep,
) -> NotificationTokenResponse:
    result = await session.execute(
        select(NotificationToken).where(
            NotificationToken.user_id == user.id,
            NotificationToken.token == payload.token,
        )
    )
    token = result.scalar_one_or_none()
    if token is None:
        token = NotificationToken(user_id=user.id, platform=payload.platform, token=payload.token)
        session.add(token)
    else:
        token.platform = payload.platform
        token.active = True

    await session.commit()
    await session.refresh(token)
    return NotificationTokenResponse(id=token.id, platform=token.platform, active=token.active)


@router.delete("/token/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token(
    token_id: str,
    user: CurrentUserDep,
    session: SessionDep,
) -> Response:
    token = await session.get(NotificationToken, token_id)
    if token is None or token.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found.")
    token.active = False
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
