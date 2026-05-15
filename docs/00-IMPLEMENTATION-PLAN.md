# Thrifty — Phase 1 Implementation Plan

This file turns the locked goal, PRD, architecture, data model, API contract, and backlog into the build order used for the Phase 1 MVP.

## Phase 1 Epics

| Epic | Outcome |
|---|---|
| THR-E1 | Python API, React Native shell, and passwordless sign-in exist as the foundation. |
| THR-E2 | Users can add subscriptions manually and see the same future-event list after signing in again. |
| THR-E3 | The backend computes proactive alerts and records delivery attempts before a charge or trial conversion. |

## Phase 1 Stories

| Story | Acceptance |
|---|---|
| THR-S1 | Magic-link sign-in issues a session without any secret field stored or requested from the user. |
| THR-S2 | Manual add captures known values, keeps unknown values null, and flags uncertainty honestly. |
| THR-S3 | A signed-in user can fetch the same subscription list from a new app session. |
| THR-S4 | Trial-conversion alerts are scheduled before the event and include known values only. |
| THR-S5 | Renewal alerts use the same proactive schedule as trial conversions. |
| THR-S6 | Unknown values render as "unknown" with a reason, never as invented facts. |

## Commit Slices

| Slice | Backlog Tasks | Verification Gate |
|---|---|---|
| 1 | THR-T1 | Backend imports, health route, and migration files exist. |
| 2 | THR-T2 | Auth tests prove link issue, rate limit, verification, expiry, and consumed-token handling. |
| 3 | THR-T4, THR-T6 | Subscription CRUD and platform sync tests pass. |
| 4 | THR-T7, THR-T8 | Alert engine, scheduler tick, and delivery log tests pass. |
| 5 | THR-T3, THR-T5, THR-T9 | Mobile TypeScript check passes with sign-in, future-event list, manual add, push, and local fallback modules. |
| 6 | THR-T10 | Copy pack compiles and banned-words lint passes. |
| 7 | THR-T11, THR-T12 | Docker, CI, structured logging, bootstrap script, and deployment doc are present. |

## Rules Applied During Build

- Backend remains Python 3.12 and FastAPI.
- Node.js files are limited to the React Native mobile app.
- The primary mobile view shows future events only.
- Nullable financial and timing fields stay unknown until a trusted source provides them.
- Generated Markdown keeps the required footer.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
