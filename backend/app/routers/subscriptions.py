from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import select

from app.deps import CurrentUserDep, SessionDep
from app.models import Subscription
from app.schemas.subscription import (
    PlatformSnapshot,
    PlatformSyncRequest,
    PlatformSyncResponse,
    SubscriptionCreate,
    SubscriptionListResponse,
    SubscriptionPatch,
    SubscriptionResponse,
)
from app.services.alert_engine import cancel_pending_alerts, recompute_alerts

router = APIRouter(prefix="/v1/subscriptions", tags=["subscriptions"])


def to_response(subscription: Subscription) -> SubscriptionResponse:
    return SubscriptionResponse(
        id=subscription.id,
        service_name=subscription.service_name,
        source=subscription.source,
        source_product_id=subscription.source_product_id,
        amount=subscription.amount,
        currency=subscription.currency,
        cadence=subscription.cadence,
        custom_period_days=subscription.custom_period_days,
        status=subscription.status,
        trial_ends_at=subscription.trial_ends_at,
        next_event_at=subscription.next_event_at,
        next_event_kind=subscription.next_event_kind,
        precision=subscription.precision,
        cancel_by_at=subscription.cancel_by_at,
        cancel_url=subscription.cancel_url,
        terms_english=subscription.terms_english,
        notes=subscription.notes,
    )


def payload_values(
    payload: SubscriptionCreate | SubscriptionPatch | PlatformSnapshot,
    *,
    with_defaults: bool,
) -> dict[str, object]:
    values = payload.model_dump(exclude_unset=True)
    if with_defaults and values.get("precision") is None:
        values["precision"] = "unknown"
    if with_defaults and values.get("status") is None:
        values["status"] = "unknown"
    return values


async def get_owned_subscription(
    session: SessionDep,
    user_id: str,
    subscription_id: str,
) -> Subscription:
    subscription = await session.get(Subscription, subscription_id)
    if (
        subscription is None
        or subscription.user_id != user_id
        or subscription.deleted_at is not None
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found.")
    return subscription


@router.get("", response_model=SubscriptionListResponse)
async def list_subscriptions(
    user: CurrentUserDep,
    session: SessionDep,
    include_deleted: bool = Query(default=False),
) -> SubscriptionListResponse:
    statement = select(Subscription).where(Subscription.user_id == user.id)
    if not include_deleted:
        statement = statement.where(Subscription.deleted_at.is_(None))
    statement = statement.order_by(Subscription.next_event_at.is_(None), Subscription.next_event_at)
    result = await session.execute(statement)
    return SubscriptionListResponse(
        subscriptions=[to_response(subscription) for subscription in result.scalars()]
    )


@router.post("", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    payload: SubscriptionCreate,
    user: CurrentUserDep,
    session: SessionDep,
) -> SubscriptionResponse:
    subscription = Subscription(
        user_id=user.id,
        source="manual",
        **payload_values(payload, with_defaults=True),
    )
    session.add(subscription)
    await recompute_alerts(session, subscription)
    await session.commit()
    await session.refresh(subscription)
    return to_response(subscription)


@router.patch("/{subscription_id}", response_model=SubscriptionResponse)
async def patch_subscription(
    subscription_id: str,
    payload: SubscriptionPatch,
    user: CurrentUserDep,
    session: SessionDep,
) -> SubscriptionResponse:
    subscription = await get_owned_subscription(session, user.id, subscription_id)
    for key, value in payload_values(payload, with_defaults=False).items():
        setattr(subscription, key, value)
    subscription.updated_at = datetime.now(UTC)
    await recompute_alerts(session, subscription)
    await session.commit()
    await session.refresh(subscription)
    return to_response(subscription)


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subscription(
    subscription_id: str,
    user: CurrentUserDep,
    session: SessionDep,
) -> Response:
    subscription = await get_owned_subscription(session, user.id, subscription_id)
    subscription.deleted_at = datetime.now(UTC)
    await cancel_pending_alerts(session, subscription.id)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def subscription_changed(subscription: Subscription, values: dict[str, object]) -> bool:
    for key, value in values.items():
        current = getattr(subscription, key)
        if isinstance(current, Decimal) and value is not None:
            value = Decimal(str(value))
        if current != value:
            return True
    return False


@router.post("/sync/platform", response_model=PlatformSyncResponse)
async def sync_platform(
    payload: PlatformSyncRequest,
    user: CurrentUserDep,
    session: SessionDep,
) -> PlatformSyncResponse:
    created = updated = unchanged = 0

    for snapshot in payload.snapshots:
        statement = select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.source == payload.platform,
            Subscription.source_product_id == snapshot.source_product_id,
        )
        result = await session.execute(statement)
        subscription = result.scalar_one_or_none()
        values = payload_values(snapshot, with_defaults=True)
        values["source"] = payload.platform

        if subscription is None:
            subscription = Subscription(user_id=user.id, **values)
            session.add(subscription)
            await recompute_alerts(session, subscription)
            created += 1
            continue

        if subscription_changed(subscription, values):
            for key, value in values.items():
                setattr(subscription, key, value)
            subscription.deleted_at = None
            subscription.updated_at = datetime.now(UTC)
            await recompute_alerts(session, subscription)
            updated += 1
        else:
            unchanged += 1

    await session.commit()
    return PlatformSyncResponse(created=created, updated=updated, unchanged=unchanged)
