# Thrifty — Product Requirements Document (v1.0, LOCKED)

**Tagline:** I may be thrifty, but I'm not frugal.
**Founder:** Lila Olufemi Abegunrin
**Markets:** UK, Canada, Australia, Europe, Africa (NOT US-centric)
**Platforms:** iOS native (SwiftUI) + Android native (Kotlin/Compose)
**Backend:** Python (FastAPI). Node.js banned.
**Auth:** Passwordless only.
**Language:** British/Scottish English throughout. Zero Americanisms.

---

## 1. Summary

Thrifty is a mobile application that proactively warns users **before** a free trial converts or a subscription renews, so charges can be cancelled in time. It is offensive, not defensive — it intercepts charges before they happen. It is not a receipt app.

## 2. Problem

The founder lost between £1,500 and £2,000 (CAD equivalent) since Boxing Day to subscriptions accumulated without conscious sign-up, forgotten trials, offloaded apps removing the only reminder, and deliberately convoluted terms.

## 3. Goal

Intercept subscription costs **before** money leaves the account by detecting upcoming renewal and trial-conversion events, then alerting the user with: what will charge, when, how much, cancellation window, and cancel-by time — or an explicit "unknown" where any field cannot be honestly determined.

## 4. Target Users

People in the UK, Canada, Australia, Europe, and Africa who accidentally enter free trials, forget cancellations, or lose visibility because of app deletion or offloading.

## 5. Core Workflow

1. Install Thrifty (iOS or Android).
2. Sign in passwordlessly.
3. Connect available sources: StoreKit, Google Play Billing, Plaid (optional), or manual add.
4. Thrifty normalises all subscriptions into one persistent list, independent of device app state.
5. Backend computes next event time and alert times.
6. Proactive alerts fire **before** the event.
7. Subscription terms are translated into plain British/Scottish English.

## 6. In Scope (v1)

- iOS + Android native clients
- Python backend (FastAPI)
- Passwordless authentication (magic link via email — see §13 Decisions)
- Proactive alerts before renewals and trial-to-paid conversions
- StoreKit billing for Thrifty Plus (iOS)
- Play Billing for Thrifty Plus (Android)
- Manual add (always available)
- Persistence across app deletion, offload, and device change
- Plain-English translation of known subscription fields

## 7. Out of Scope (v1)

- Receipt-first experience or any "charges already happened" feed as primary view
- US-centric assumptions (currency defaults, region defaults, copy)
- Plaid integration (deferred to Phase 3)
- Any reference to FlatFinder Inc., Prototype Cafe™, or MAAC™
- Node.js anywhere in the stack
- Any password storage

## 8. Functional Requirements

| ID | Requirement |
|---|---|
| FR1 | Manual add: capture known subscriptions and trials without inventing unknown values |
| FR2 | Thrifty Plus billing: use StoreKit on iOS and Play Billing on Android for Thrifty's own paid plan |
| FR3 | Plaid ingestion (Phase 3): detect subscription-like merchants not visible via store billing; label uncertainty |
| FR4 | Manual add: user can add any subscription or trial with amount, currency, cadence, next event datetime, notes |
| FR5 | Normalisation: unify all sources into one canonical Subscription model; dedupe on (provider, product_id, user_id) |
| FR6 | Proactive scheduling: compute next_event_at and one or more alert_at times strictly before next_event_at |
| FR7 | Alert content: every alert includes (as available) what, when, how much, cancellation window, cancel-by time, or explicit "unknown" with reason |
| FR8 | Persistence: subscription records persist server-side independent of app install or offload state |
| FR9 | Plain-language translation: explain subscription and trial terms in plain British/Scottish English; no jargon |
| FR10 | Uncertainty honesty: never invent amount, event time, or cancellation deadline |

## 9. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR1 | Backend is Python only (FastAPI). Native mobile clients only. Node.js banned. |
| NFR2 | Passwordless only. No password storage anywhere. |
| NFR3 | Alert delivery SLO: 99% of scheduled alerts delivered within ±60 seconds of scheduled time, no later than 1 hour before event |
| NFR4 | Multi-currency (ISO 4217), multi-region (IANA timezones) |
| NFR5 | Low ops burden: deployable to a single managed PaaS (Railway/Fly.io/Render) with one Postgres instance |
| NFR6 | Observability: structured JSON logs; every alert delivery logged with reason |

## 10. Data Requirements

Canonical entities: `users`, `auth_identities`, `subscriptions`, `alerts`, `notification_tokens`, `subscription_sources`. Amounts stored with ISO 4217 currency code. User timezones stored as IANA strings. Event precision flagged as `exact`, `estimated`, or `unknown`.

## 11. Security, Privacy, Safety

- Magic-link auth with single-use tokens, 15-minute expiry, rate-limited to 5 requests per email per hour.
- Plaid tokens (Phase 3) encrypted at rest using AES-256-GCM with keys from environment-managed KMS.
- Data minimisation: no transaction storage beyond what is needed to identify a recurring subscription.
- Honest uncertainty: never display a "cancel by" deadline that was not directly provided by the source.

## 12. Success Criteria

| Metric | Target |
|---|---|
| Alerts delivered before event time | ≥ 99% |
| User-reported prevented charges (first 90 days) | ≥ 60% of detected subscriptions surfaced at least one alert acted upon |
| Subscription detection coverage (auto vs manual) | ≥ 70% auto by end of Phase 2 |
| Comprehension (plain-English survey) | ≥ 90% rate explanations as "clear" |

## 13. Decisions (Open Questions Resolved)

| Q | Decision |
|---|---|
| Q1 Passwordless method | **Magic link** via email. Single-use, 15-min expiry, rate-limited. Passkeys deferred to Phase 4. |
| Q2 Alert lead times | Default schedule: **T-7 days, T-3 days, T-24 hours, T-2 hours**. User-configurable per subscription. |
| Q3 Notification model | **Hybrid**: backend schedules push (APNs/FCM); mobile sets local notifications as fallback for offline state. |
| Q4 Plaid in MVP | **No.** Phase 3. |
| Q5 Translation source | Template-based from canonical fields. **No LLM at runtime in v1.** Terms text ingested as-is from platform APIs; no invention. |
| Q6 Monetisation | **Freemium**: free tier covers manual add and core reminders; paid tier (Thrifty Plus) uses app-store billing. RevenueCat is the preferred cross-platform entitlement layer when monetisation enters scope. No ads. |
| Q7 Historical charges | **Disallowed in primary view.** Secondary "History" tab in Phase 4, read-only, clearly labelled past events. |

## 14. Risks

- Platform API limitations on exact conversion times → mitigation: explicit uncertainty flags
- Notification permissions denied → mitigation: in-app banner on launch; local fallback
- Multi-market cancellation law differences → mitigation: never give legal advice; link to provider's own cancellation page
- Product drift into receipt territory → mitigation: hard rule in PRD §7
- Monetisation trust risk → mitigation: own subscription must be trivially cancellable inside Thrifty

## 15. Assumptions

- Users grant notification permissions or accept degraded experience
- Sufficient metadata exists to compute next event; otherwise uncertainty is shown

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
