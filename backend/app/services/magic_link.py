from __future__ import annotations

import hashlib
import secrets
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from email.message import EmailMessage

import aiosmtplib
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import AuthToken, User

LINK_TTL = timedelta(minutes=15)
SESSION_TTL = timedelta(days=30)
RATE_WINDOW = timedelta(hours=1)
RATE_LIMIT = 5

_requests: dict[str, list[datetime]] = defaultdict(list)
_issued_tokens: dict[str, str] = {}


def reset_auth_memory() -> None:
    _requests.clear()
    _issued_tokens.clear()


def last_issued_token(email: str) -> str:
    return _issued_tokens[email.lower()]


def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def utc_now() -> datetime:
    return datetime.now(UTC)


def as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def enforce_link_rate(email: str, now: datetime | None = None) -> None:
    stamp = now or utc_now()
    key = email.lower()
    recent = [entry for entry in _requests[key] if stamp - entry < RATE_WINDOW]
    if len(recent) >= RATE_LIMIT:
        raise TooManyLinksRequested
    recent.append(stamp)
    _requests[key] = recent


class TooManyLinksRequested(Exception):
    pass


async def find_or_create_user(session: AsyncSession, email: str) -> User:
    normalised = email.lower()
    result = await session.execute(select(User).where(User.email == normalised))
    user = result.scalar_one_or_none()
    if user is not None:
        return user

    user = User(email=normalised)
    session.add(user)
    await session.flush()
    return user


async def issue_magic_link(session: AsyncSession, settings: Settings, email: str) -> None:
    normalised = email.lower()
    enforce_link_rate(normalised)
    user = await find_or_create_user(session, normalised)
    token = secrets.token_urlsafe(32)
    auth_token = AuthToken(
        user_id=user.id,
        token_hash=token_digest(token),
        purpose="magic_link",
        expires_at=utc_now() + LINK_TTL,
    )
    session.add(auth_token)
    _issued_tokens[normalised] = token
    await session.commit()
    await send_magic_link(settings, normalised, token)


async def send_magic_link(settings: Settings, email: str, token: str) -> None:
    if not settings.smtp_user or not settings.smtp_pass:
        return

    message = EmailMessage()
    message["From"] = settings.smtp_from
    message["To"] = email
    message["Subject"] = "Sign in to Thrifty"
    message.set_content(f"Use this link to sign in: {settings.app_base_url}/auth?token={token}")

    smtp = aiosmtplib.SMTP(
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        start_tls=True,
    )
    await smtp.connect()
    await smtp.login(settings.smtp_user, settings.smtp_pass)
    await smtp.send_message(message)
    await smtp.quit()


def issue_session(settings: Settings, user: User) -> str:
    now = utc_now()
    payload = {
        "sub": user.id,
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int((now + SESSION_TTL).timestamp()),
    }
    return jwt.encode(payload, settings.session_secret, algorithm="HS256")


async def verify_magic_link(
    session: AsyncSession, settings: Settings, token: str
) -> tuple[str, User]:
    result = await session.execute(
        select(AuthToken).where(
            AuthToken.token_hash == token_digest(token),
            AuthToken.purpose == "magic_link",
        )
    )
    record = result.scalar_one_or_none()
    if record is None or as_utc(record.expires_at) <= utc_now():
        raise LinkInvalid
    if record.consumed_at is not None:
        raise LinkConsumed

    record.consumed_at = utc_now()
    user = await session.get(User, record.user_id)
    if user is None:
        raise LinkInvalid

    session_token = issue_session(settings, user)
    await session.commit()
    return session_token, user


class LinkInvalid(Exception):
    pass


class LinkConsumed(Exception):
    pass
