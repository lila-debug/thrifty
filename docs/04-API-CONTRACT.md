# Thrifty — API Contract (v1.0, LOCKED)

Base URL: `/v1`
Auth: Bearer JWT (session token returned by `/auth/verify`)
Content-Type: `application/json`
All timestamps: ISO 8601 with timezone.

## Auth

### `POST /v1/auth/start`
**Body:** `{ "email": "user@example.com" }`
**Response 202:** `{ "status": "sent" }`
**Rate limit:** 5/hour per email.
**Effect:** generates single-use magic-link token, emails it.

### `POST /v1/auth/verify`
**Body:** `{ "token": "..." }`
**Response 200:** `{ "session_token": "...", "user": { "id": "...", "email": "...", "tier": "free" } }`
**Errors:** 401 invalid/expired, 410 already consumed.

### `POST /v1/auth/logout`
**Auth:** required.
**Response 204.**
**Effect:** revokes the current session token server-side; the client must discard the token.

### `POST /v1/auth/test-token`
**Local/test only. Hidden unless `ENABLE_TEST_AUTH_TOKENS=true` and `APP_ENV` is `development`, `local`, or `test`.**
**Body:** `{ "email": "user@example.com" }`
**Response 200:** `{ "token": "single-use-magic-link-token" }`
**Errors:** 404 when disabled or when no link has been issued.
**Effect:** lets external harnesses and simulators complete passwordless sign-in without weakening production auth.

## Subscriptions

### `GET /v1/subscriptions`
**Query:** `?include_deleted=false`
**Response 200:**
```json
{
  "subscriptions": [
    {
      "id": "uuid",
      "service_name": "Netflix",
      "source": "manual",
      "amount": "10.99",
      "currency": "GBP",
      "cadence": "monthly",
      "status": "active",
      "next_event_at": "2026-06-01T00:00:00Z",
      "next_event_kind": "renewal",
      "precision": "exact",
      "cancel_by_at": null,
      "cancel_url": "https://netflix.com/cancel",
      "terms_plain": "Renews monthly at £10.99. Cancel any time from Netflix account settings.",
      "notes": null
    }
  ]
}
```

### `POST /v1/subscriptions`
**Body:** (manual add)
```json
{
  "service_name": "Spotify Family",
  "amount": "17.99",
  "currency": "GBP",
  "cadence": "monthly",
  "next_event_at": "2026-06-15T09:00:00Z",
  "next_event_kind": "renewal",
  "precision": "exact",
  "notes": "Shared with family"
}
```
**Response 201:** the created subscription.
**Validation:** `service_name` required; everything else optional but flagged `precision: unknown` if missing.

### `PATCH /v1/subscriptions/{id}`
**Body:** any subset of fields. Triggers alert recompute.

### `DELETE /v1/subscriptions/{id}`
**Response 204.** Soft delete. Cancels pending alerts.

### `POST /v1/subscriptions/sync/platform`
**Body:**
```json
{
  "platform": "storekit",
  "snapshots": [
    {
      "source_product_id": "com.netflix.premium",
      "service_name": "Netflix Premium",
      "amount": "17.99",
      "currency": "GBP",
      "cadence": "monthly",
      "status": "active",
      "trial_ends_at": null,
      "next_event_at": "2026-06-01T00:00:00Z",
      "precision": "exact"
    }
  ]
}
```
**Response 200:** `{ "created": 1, "updated": 0, "unchanged": 0 }`
**Effect:** upserts on `(user_id, source, source_product_id)`; recomputes alerts.

## Alerts

### `GET /v1/alerts`
**Query:** `?status=scheduled&from=2026-05-15T00:00:00Z`
**Response 200:**
```json
{
  "alerts": [
    {
      "id": "uuid",
      "subscription_id": "uuid",
      "alert_at": "2026-05-29T00:00:00Z",
      "lead_label": "T-3 days",
      "status": "scheduled"
    }
  ]
}
```

### `POST /v1/alerts/recompute`
**Body:** `{ "subscription_id": "uuid" }` (omit to recompute all for user)
**Response 200:** `{ "alerts_created": 4, "alerts_cancelled": 2 }`

## Notifications

### `POST /v1/notifications/token`
**Body:** `{ "platform": "ios", "token": "apns-token-string" }`
**Response 201.**

### `DELETE /v1/notifications/token/{id}`
**Response 204.**

## Health

### `GET /health`
**Response 200:** `{ "status": "ok", "db": "ok", "version": "1.0.0" }`

## Error Envelope (All Errors)

```json
{
  "error": {
    "code": "validation_error",
    "message": "amount must be positive",
    "field": "amount"
  }
}
```

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
