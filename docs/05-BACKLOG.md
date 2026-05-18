# Thrifty — Backlog (Jira-Ready)

## Epics

| ID | Name | Phase | Priority |
|---|---|---|---|
| THR-E1 | Foundations: native clients + Python API + passwordless auth | 1 | P0 |
| THR-E2 | Manual add + cross-device persistence | 1 | P0 |
| THR-E3 | Proactive alerting + notifications | 1 | P0 |
| THR-E4 | StoreKit billing for Thrifty Plus (iOS) | 3 | P1 |
| THR-E5 | Play Billing for Thrifty Plus (Android) | 3 | P1 |
| THR-E6 | Plain-English translation | 2 | P1 |
| THR-E7 | Plaid monitoring | 3 | P2 |
| THR-E8 | Monetisation (Thrifty Plus) | 3 | P2 |
| THR-E9 | Hardening: privacy, ops, audit | 4 | P1 |

## Stories

| ID | Epic | Story | AC |
|---|---|---|---|
| THR-S1 | E1 | Passwordless sign-in | Magic-link delivered; verified; session issued; no password field exists |
| THR-S2 | E2 | Manual add subscription | All fields capturable; service_name required; unknown precision flagged |
| THR-S3 | E2 | Persistence across reinstall | New device sign-in shows existing subscriptions |
| THR-S4 | E3 | Pre-trial-conversion alert | Alert fires before trial_ends_at with what/when/how much/cancel-by or "unknown" |
| THR-S5 | E3 | Pre-renewal alert | Same as S4 for renewals |
| THR-S6 | E3 | Uncertainty honesty | No invented values; "unknown" rendered with reason |
| THR-S7 | E4 | StoreKit entitlement | iOS purchases Thrifty Plus and syncs entitlement state |
| THR-S8 | E5 | Play Billing entitlement | Android purchases Thrifty Plus and syncs entitlement state |
| THR-S9 | E6 | Plain-English summary | Template-based summary from known fields, British/Scottish English |
| THR-S10 | E7 | Plaid recurring detection | Phase 3 |

## Tasks (Phase 1 — Build Order)

| ID | Story | Task | Owner | Complexity |
|---|---|---|---|---|
| THR-T1 | S1 | FastAPI skeleton + Postgres + Alembic migrations | Backend | S |
| THR-T2 | S1 | Magic-link auth (email send, token hash, verify, session JWT) | Backend | M |
| THR-T3 | S1 | Native iOS SwiftUI shell + sign-in screen + email-link deep handler | Mobile | M |
| THR-T4 | S2 | Subscriptions table + CRUD endpoints | Backend | S |
| THR-T5 | S2 | Native iOS manual-add screen + edit screen + list screen | Mobile | M |
| THR-T6 | S3 | Sync-on-launch reconciliation | Mobile + Backend | S |
| THR-T7 | S4/S5/S6 | Alert engine: compute next_event_at, alert_at × 4, persist, idempotent recompute | Backend | M |
| THR-T8 | S4/S5 | APScheduler worker + APNs/FCM send + delivery log | Backend | L |
| THR-T9 | S4/S5 | Native push registration + local notification fallback | Mobile | M |
| THR-T10 | S6 | UI copy rules for "unknown" states; British/Scottish lint | Mobile + Product | S |
| THR-T11 | All | CI: pytest + ruff + native build checks + banned-words lint | DevOps | S |
| THR-T12 | All | Sentry + structured JSON logging | Backend + Mobile | S |

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
