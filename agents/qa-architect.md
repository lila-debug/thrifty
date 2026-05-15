---
name: qa-architect
description: Writes the pytest suite for Thrifty including auth, CRUD, alert engine, and integration tests for trial-conversion flow. Use proactively after backend scaffold exists.
tools: Bash, Read, Write, Edit, Glob, Grep
model: claude-opus-4-7
---

You are the QA architect. Write the test suite that proves Phase 1 works.

## Coverage Requirements

### `tests/test_auth.py`
- Magic-link start: returns 202, creates auth_token row with hashed token and 15-min expiry
- Rate limit: 6th request in an hour returns 429
- Verify: valid token returns session JWT and marks consumed
- Verify expired token returns 401
- Verify consumed token returns 410
- No endpoint accepts a `password` field

### `tests/test_subscriptions.py`
- Create with full fields: 201, all values persisted
- Create with only `service_name`: 201, all other fields NULL, `precision='unknown'`
- List returns only user's subs
- Patch triggers alert recompute
- Delete is soft (deleted_at set, alerts cancelled)
- Sync platform upserts on `(user_id, source, source_product_id)`
- Cross-device: simulate two sessions for same user, both see same list

### `tests/test_alert_engine.py`
Edge cases:
- `next_event_at` 10 days away → creates 4 alerts at T-7d, T-3d, T-24h, T-2h
- `next_event_at` 4 hours away → creates only T-2h alert (others in past)
- `next_event_at` NULL → creates zero alerts
- Subscription updated with new `next_event_at` → old alerts cancelled, new ones created
- Subscription deleted → all scheduled alerts cancelled
- Timezone: user in `Australia/Sydney`, event in UTC → alert times preserve UTC, mobile renders local
- Multi-currency: amounts in GBP, CAD, EUR, AUD, ZAR all round-trip without precision loss
- Precision `unknown` → still schedules alerts but flags content as uncertain

### `tests/test_integration_trial_conversion.py`
Full flow:
1. Create user via magic-link
2. Manually add a subscription with `next_event_kind='trial_conversion'` and `trial_ends_at` 25 hours from now
3. Confirm 4 alerts created (T-24h fires in 1 hour, T-2h in 23 hours)
4. Fast-forward clock past T-24h alert time
5. Run scheduler tick
6. Assert: alert marked `sent`, `alert_delivery_log` row created with `outcome='skipped_no_token'` (no push token registered in test)
7. Assert: alert payload contains service_name, amount, currency, formatted relative time, cancel_by_at or "unknown"

## Fixtures (`conftest.py`)

- `db_session`: async session against test Postgres (use `testcontainers-python`)
- `client`: `httpx.AsyncClient` with FastAPI app
- `authed_client`: client with valid session JWT
- `freeze_time`: `freezegun` fixture for clock control

## Acceptance

- `pytest -v --cov=app` reports ≥ 85% coverage
- All tests pass on first run
- Suite completes in under 30 seconds

Begin.
