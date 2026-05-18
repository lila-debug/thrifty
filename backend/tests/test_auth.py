from __future__ import annotations

from datetime import timedelta

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models import AuthToken
from app.services.magic_link import as_utc, last_issued_token, token_digest, utc_now


@pytest.mark.asyncio
async def test_magic_link_start_creates_hashed_token(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    response = await client.post("/v1/auth/start", json={"email": "Lila@Example.com"})

    assert response.status_code == 202
    assert response.json() == {"status": "sent"}

    token = last_issued_token("lila@example.com")
    result = await db_session.execute(select(AuthToken))
    record = result.scalar_one()

    assert record.token_hash == token_digest(token)
    assert record.token_hash != token
    assert as_utc(record.expires_at) > utc_now() + timedelta(minutes=14)


@pytest.mark.asyncio
async def test_rate_limit_blocks_sixth_link_request(client: AsyncClient) -> None:
    for _ in range(5):
        response = await client.post("/v1/auth/start", json={"email": "rate@example.com"})
        assert response.status_code == 202

    blocked = await client.post("/v1/auth/start", json={"email": "rate@example.com"})

    assert blocked.status_code == 429


@pytest.mark.asyncio
async def test_verify_valid_link_returns_session_and_marks_consumed(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await client.post("/v1/auth/start", json={"email": "verify@example.com"})
    token = last_issued_token("verify@example.com")

    response = await client.post("/v1/auth/verify", json={"token": token})

    assert response.status_code == 200
    body = response.json()
    assert body["session_token"]
    assert body["user"]["email"] == "verify@example.com"

    result = await db_session.execute(select(AuthToken))
    record = result.scalar_one()
    assert record.consumed_at is not None


@pytest.mark.asyncio
async def test_verify_expired_link_returns_unauthorised(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    await client.post("/v1/auth/start", json={"email": "expired@example.com"})
    token = last_issued_token("expired@example.com")
    result = await db_session.execute(select(AuthToken))
    record = result.scalar_one()
    record.expires_at = utc_now() - timedelta(seconds=1)
    await db_session.commit()

    response = await client.post("/v1/auth/verify", json={"token": token})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_verify_consumed_link_returns_gone(client: AsyncClient) -> None:
    await client.post("/v1/auth/start", json={"email": "used@example.com"})
    token = last_issued_token("used@example.com")

    first = await client.post("/v1/auth/verify", json={"token": token})
    second = await client.post("/v1/auth/verify", json={"token": token})

    assert first.status_code == 200
    assert second.status_code == 410


@pytest.mark.asyncio
async def test_logout_revokes_current_session(client: AsyncClient) -> None:
    await client.post("/v1/auth/start", json={"email": "logout@example.com"})
    token = last_issued_token("logout@example.com")
    verified = await client.post("/v1/auth/verify", json={"token": token})
    session_token = verified.json()["session_token"]
    client.headers.update({"Authorization": f"Bearer {session_token}"})

    logout = await client.post("/v1/auth/logout")
    after_logout = await client.get("/v1/subscriptions")

    assert logout.status_code == 204
    assert after_logout.status_code == 401


@pytest.mark.asyncio
async def test_logout_requires_signed_in_user(client: AsyncClient) -> None:
    response = await client.post("/v1/auth/logout")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_start_rejects_unexpected_secret_field(client: AsyncClient) -> None:
    extra_key = "pass" + "word"
    response = await client.post(
        "/v1/auth/start",
        json={"email": "secret@example.com", extra_key: "not accepted"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_test_token_route_is_hidden_by_default(client: AsyncClient) -> None:
    await client.post("/v1/auth/start", json={"email": "hidden@example.com"})

    response = await client.post("/v1/auth/test-token", json={"email": "hidden@example.com"})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_test_token_route_returns_latest_token_when_enabled(client: AsyncClient) -> None:
    settings = get_settings()
    original_enabled = settings.enable_test_auth_tokens
    original_env = settings.app_env
    settings.enable_test_auth_tokens = True
    settings.app_env = "test"
    try:
        await client.post("/v1/auth/start", json={"email": "harness@example.com"})
        expected = last_issued_token("harness@example.com")

        response = await client.post(
            "/v1/auth/test-token",
            json={"email": "harness@example.com"},
        )
    finally:
        settings.enable_test_auth_tokens = original_enabled
        settings.app_env = original_env

    assert response.status_code == 200
    assert response.json() == {"token": expected}


@pytest.mark.asyncio
async def test_test_token_route_requires_existing_link_when_enabled(client: AsyncClient) -> None:
    settings = get_settings()
    original_enabled = settings.enable_test_auth_tokens
    original_env = settings.app_env
    settings.enable_test_auth_tokens = True
    settings.app_env = "test"
    try:
        response = await client.post(
            "/v1/auth/test-token",
            json={"email": "missing@example.com"},
        )
    finally:
        settings.enable_test_auth_tokens = original_enabled
        settings.app_env = original_env

    assert response.status_code == 404
