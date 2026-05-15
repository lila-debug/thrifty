from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import get_settings
from app.models import Subscription, User
from app.services.magic_link import issue_session


@pytest.mark.asyncio
async def test_create_subscription_with_full_fields(authed_client: AsyncClient) -> None:
    next_event = (datetime.now(UTC) + timedelta(days=10)).isoformat()
    response = await authed_client.post(
        "/v1/subscriptions",
        json={
            "service_name": "Spotify Family",
            "amount": "17.99",
            "currency": "gbp",
            "cadence": "monthly",
            "status": "active",
            "next_event_at": next_event,
            "next_event_kind": "renewal",
            "precision": "exact",
            "notes": "Shared with family",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["service_name"] == "Spotify Family"
    assert body["amount"] == "17.99"
    assert body["currency"] == "GBP"
    assert body["precision"] == "exact"


@pytest.mark.asyncio
async def test_create_subscription_with_only_service_name_marks_unknown(
    authed_client: AsyncClient,
) -> None:
    response = await authed_client.post("/v1/subscriptions", json={"service_name": "Netflix"})

    assert response.status_code == 201
    body = response.json()
    assert body["service_name"] == "Netflix"
    assert body["amount"] is None
    assert body["next_event_at"] is None
    assert body["precision"] == "unknown"
    assert body["status"] == "unknown"


@pytest.mark.asyncio
async def test_list_returns_only_signed_in_users_subscriptions(
    authed_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    other = User(email="other@example.com")
    db_session.add(other)
    await db_session.flush()
    db_session.add(
        Subscription(
            user_id=other.id,
            source="manual",
            service_name="Other Service",
            status="active",
            precision="exact",
        )
    )
    await db_session.commit()

    await authed_client.post("/v1/subscriptions", json={"service_name": "Mine"})
    response = await authed_client.get("/v1/subscriptions")

    assert response.status_code == 200
    names = [item["service_name"] for item in response.json()["subscriptions"]]
    assert names == ["Mine"]


@pytest.mark.asyncio
async def test_patch_updates_subscription_without_overwriting_unknown_defaults(
    authed_client: AsyncClient,
) -> None:
    created = await authed_client.post("/v1/subscriptions", json={"service_name": "Disney+"})
    subscription_id = created.json()["id"]

    response = await authed_client.patch(
        f"/v1/subscriptions/{subscription_id}",
        json={"amount": "8.99", "currency": "CAD", "notes": "Annual offer checked"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["amount"] == "8.99"
    assert body["currency"] == "CAD"
    assert body["precision"] == "unknown"


@pytest.mark.asyncio
async def test_delete_soft_deletes_subscription(
    authed_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    created = await authed_client.post("/v1/subscriptions", json={"service_name": "Canva"})
    subscription_id = created.json()["id"]

    response = await authed_client.delete(f"/v1/subscriptions/{subscription_id}")
    visible = await authed_client.get("/v1/subscriptions")
    result = await db_session.execute(
        select(Subscription).where(Subscription.id == subscription_id)
    )
    record = result.scalar_one()

    assert response.status_code == 204
    assert visible.json()["subscriptions"] == []
    assert record.deleted_at is not None


@pytest.mark.asyncio
async def test_platform_sync_upserts_by_source_product(authed_client: AsyncClient) -> None:
    payload = {
        "platform": "storekit",
        "snapshots": [
            {
                "source_product_id": "app.service.monthly",
                "service_name": "Service",
                "amount": "4.99",
                "currency": "GBP",
                "cadence": "monthly",
                "status": "active",
                "precision": "exact",
            }
        ],
    }
    created = await authed_client.post("/v1/subscriptions/sync/platform", json=payload)
    updated_payload = payload | {
        "snapshots": [payload["snapshots"][0] | {"service_name": "Service Plus", "amount": "5.99"}]
    }
    updated = await authed_client.post("/v1/subscriptions/sync/platform", json=updated_payload)
    unchanged = await authed_client.post("/v1/subscriptions/sync/platform", json=updated_payload)

    assert created.json() == {"created": 1, "updated": 0, "unchanged": 0}
    assert updated.json() == {"created": 0, "updated": 1, "unchanged": 0}
    assert unchanged.json() == {"created": 0, "updated": 0, "unchanged": 1}


@pytest.mark.asyncio
async def test_cross_session_fetches_existing_subscriptions(
    authed_client: AsyncClient,
    client: AsyncClient,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    await authed_client.post("/v1/subscriptions", json={"service_name": "Readly"})

    async with session_factory() as session:
        result = await session.execute(select(User).where(User.email == "lila@example.com"))
        user = result.scalar_one()
        second_token = issue_session(get_settings(), user)

    client.headers.update({"Authorization": f"Bearer {second_token}"})
    response = await client.get("/v1/subscriptions")

    assert response.status_code == 200
    assert response.json()["subscriptions"][0]["service_name"] == "Readly"
