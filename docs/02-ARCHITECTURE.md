# Thrifty — Architecture Document (v1.0, LOCKED)

## Purpose

Define the allowed system shape. Prevent tool sprawl. Enforce Python-only backend and proactive-alert philosophy.

## System Components

| Component | Technology | Notes |
|---|---|---|
| Mobile app | React Native (Expo bare workflow) | iOS + Android from one codebase; native modules for StoreKit/Play Billing |
| Backend API | Python 3.12 + FastAPI | Async, type-checked, OpenAPI auto-generated |
| Database | PostgreSQL 16 | Single instance; managed on PaaS |
| Scheduler | APScheduler (in-process) for Phase 1; migrate to Celery + Redis at Phase 2 if scale demands | Computes alert_at times, enqueues notification sends |
| Notifications | APNs (iOS) + FCM (Android) via single library (`pyfcm` + `aioapns`) | Hybrid model: backend push + on-device local fallback |
| Auth | Magic link via SMTP (Postmark/Resend) | Single-use JWT tokens, 15-min expiry |
| Hosting | Railway or Fly.io | One service + one Postgres + one Redis (Phase 2+) |
| Observability | Structured JSON logs to stdout; Sentry for errors | No external APM in v1 |

## Guardrails (Non-Negotiable)

1. No receipt-first UI. Primary view is **future events only**.
2. Never invent values. Unknown fields stored as NULL and rendered as "unknown" with reason.
3. All copy is British/Scottish English. Banned words enforced via CI lint.
4. Python only on backend. Any PR introducing Node.js fails CI.
5. No passwords. Any PR introducing a password field fails CI.

## Data Flow

```
[Mobile: StoreKit/Play Billing/Manual]
        ↓ (POST /v1/subscriptions/sync/platform)
[FastAPI: normalise → dedupe → persist]
        ↓
[Postgres: subscriptions table]
        ↓ (APScheduler nightly + on-write)
[Alert engine: compute next_event_at, alert_at × N]
        ↓
[Notification worker: APNs/FCM push]
        ↓
[Mobile: receive + display + log delivery]
```

## Minimum Data Model

See `03-DATA-MODEL.md` for schemas.

Tables: `users`, `auth_tokens`, `subscriptions`, `alerts`, `notification_tokens`, `subscription_sources`, `alert_delivery_log`.

## API Surface

See `04-API-CONTRACT.md` for full OpenAPI.

Endpoints:
- `POST /v1/auth/start`
- `POST /v1/auth/verify`
- `GET /v1/subscriptions`
- `POST /v1/subscriptions`
- `PATCH /v1/subscriptions/{id}`
- `DELETE /v1/subscriptions/{id}`
- `POST /v1/subscriptions/sync/platform`
- `GET /v1/alerts`
- `POST /v1/alerts/recompute`
- `POST /v1/notifications/token`
- `DELETE /v1/notifications/token/{id}`
- `GET /health`

## Failure Modes

| Code | Meaning |
|---|---|
| 401 | Auth required or invalid |
| 403 | Ownership violation |
| 404 | Resource not found |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Logged with Sentry; generic message returned |

## Stubbed for v1 (Implement Later)

- Plaid integration (Phase 3)
- Passkeys (Phase 4)
- History tab (Phase 4)
- Celery/Redis (only if APScheduler insufficient)

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
