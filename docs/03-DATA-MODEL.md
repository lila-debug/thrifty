# Thrifty — Data Model (v1.0, LOCKED)

## Conventions

- All IDs: UUID v7 (sortable)
- All timestamps: `TIMESTAMPTZ`, UTC stored, IANA timezone in user record
- Currency: ISO 4217 three-letter codes
- Amounts: `NUMERIC(12,2)` — never floats
- Soft delete: `deleted_at` column where applicable

## Schema

```sql
CREATE TABLE users (
  id              UUID PRIMARY KEY,
  email           CITEXT NOT NULL UNIQUE,
  timezone        TEXT NOT NULL DEFAULT 'Europe/London',
  locale          TEXT NOT NULL DEFAULT 'en-GB',
  default_currency CHAR(3) NOT NULL DEFAULT 'GBP',
  tier            TEXT NOT NULL DEFAULT 'free' CHECK (tier IN ('free','plus')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at      TIMESTAMPTZ
);

CREATE TABLE auth_tokens (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash      TEXT NOT NULL UNIQUE,
  purpose         TEXT NOT NULL CHECK (purpose IN ('magic_link','session')),
  expires_at      TIMESTAMPTZ NOT NULL,
  consumed_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_auth_tokens_user ON auth_tokens(user_id);
CREATE INDEX idx_auth_tokens_expires ON auth_tokens(expires_at);

CREATE TABLE subscriptions (
  id                  UUID PRIMARY KEY,
  user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  source              TEXT NOT NULL CHECK (source IN ('storekit','play_billing','plaid','manual')),
  source_product_id   TEXT,
  service_name        TEXT NOT NULL,
  amount              NUMERIC(12,2),
  currency            CHAR(3),
  cadence             TEXT CHECK (cadence IN ('weekly','monthly','quarterly','semi_annual','annual','custom')),
  custom_period_days  INTEGER,
  status              TEXT NOT NULL CHECK (status IN ('trial','active','cancelled','expired','unknown')),
  trial_ends_at       TIMESTAMPTZ,
  next_event_at       TIMESTAMPTZ,
  next_event_kind     TEXT CHECK (next_event_kind IN ('renewal','trial_conversion','unknown')),
  precision           TEXT NOT NULL DEFAULT 'unknown' CHECK (precision IN ('exact','estimated','unknown')),
  cancel_by_at        TIMESTAMPTZ,
  cancel_url          TEXT,
  terms_raw           TEXT,
  terms_english         TEXT,
  notes               TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at          TIMESTAMPTZ,
  UNIQUE (user_id, source, source_product_id)
);
CREATE INDEX idx_subs_user ON subscriptions(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_subs_next_event ON subscriptions(next_event_at) WHERE next_event_at IS NOT NULL;

CREATE TABLE alerts (
  id              UUID PRIMARY KEY,
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  alert_at        TIMESTAMPTZ NOT NULL,
  lead_label      TEXT NOT NULL,
  status          TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled','sent','failed','cancelled')),
  attempts        INTEGER NOT NULL DEFAULT 0,
  last_error      TEXT,
  sent_at         TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_alerts_due ON alerts(alert_at) WHERE status = 'scheduled';
CREATE INDEX idx_alerts_user ON alerts(user_id);

CREATE TABLE notification_tokens (
  id              UUID PRIMARY KEY,
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  platform        TEXT NOT NULL CHECK (platform IN ('ios','android')),
  token           TEXT NOT NULL,
  active          BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, token)
);

CREATE TABLE alert_delivery_log (
  id              UUID PRIMARY KEY,
  alert_id        UUID NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
  attempted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  outcome         TEXT NOT NULL CHECK (outcome IN ('delivered','failed_token_invalid','failed_provider','failed_network','skipped_no_token')),
  reason          TEXT
);
```

## Retention

- `auth_tokens`: hard-deleted 7 days after `expires_at`
- `alert_delivery_log`: 180 days then archive
- `subscriptions`: soft-deleted; purged 365 days after `deleted_at`

## Multi-Device

`users` is canonical. `notification_tokens` supports many per user. Mobile fetches `/v1/subscriptions` on every cold start to reconcile.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
