# Thrifty Decision Log

## 2026-05-18 — Native iOS First

Decision: build the first client as native iOS with SwiftUI.

Why: iOS is the best first launch path for subscription-app conversion, StoreKit testing is available in Xcode, and the backend contract is already proven with Python tests.

Execution:
- Build iOS first.
- Build Android second.
- Keep the app repo free of Node.js, npm, npx, pnpm, and yarn.

## 2026-05-18 — RevenueCat Later, Not First

Decision: use RevenueCat when Thrifty Plus billing enters scope, but do not add it to Sprint 1.

Why: RevenueCat provides a backend and wrapper around StoreKit and Google Play Billing for in-app purchases and subscriptions. That helps monetise Thrifty Plus across iOS and Android without building full purchase infrastructure ourselves.

Boundary: RevenueCat, StoreKit, and Google Play Billing are for Thrifty's own paid plan. They do not discover every third-party subscription a user has. Discovery still comes from manual add first, then bank/email/provider integrations later.

## 2026-05-18 — Render First For API Deployment

Decision: use Render as the first public API deployment target.

Why: Render has a direct FastAPI deployment path, GitHub integration, managed Postgres, and a simpler first deploy path than a lower-level container platform.

Later option: move to Fly.io if we need more control over regions, Docker runtime shape, or edge placement.

## 2026-05-18 — TestSprite As External QA

Decision: use TestSprite as an external regression checker, not as app infrastructure.

Why: TestSprite's MCP runner uses Node/npx. That is acceptable only outside the app repository. The required app build and QA path remains Python plus native iOS/Android tooling.

Implementation:
- `/v1/auth/test-token` exists only for local/test harnesses.
- The route is hidden unless `ENABLE_TEST_AUTH_TOKENS=true` and `APP_ENV` is `development`, `local`, or `test`.

## 2026-05-18 — App Intents Later

Decision: do not add App Intents before the core iOS app exists.

First App Intents after the app shell works:
- open upcoming charges;
- add a subscription;
- show the next trial conversion.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
