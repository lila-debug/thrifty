# Thrifty — Build From The First Brick

## Decision

The clean path is to rebuild Thrifty contract-first:

1. Python FastAPI backend first.
2. Native iOS client after the API contract is proven.
3. Native Android client after iOS and backend flows are stable.
4. No package-manager app stack inside this repo.

The old mobile scaffold is legacy context only until it is removed in a dedicated cleanup slice.

## What You Need To Provide

| When | What | Why |
|---|---|---|
| Now | Confirm iOS first, Android second | Keeps the first native client focused. |
| Now | Three real subscriptions or trials for demo data | Makes the tutorial and launch video feel real. |
| Testing | TestSprite MCP server config and token | Lets an external tester walk the app as we build. |
| Auth | Email sender credentials | Required for live magic-link delivery. |
| iOS | Apple Developer account access | Required for signing, push, and StoreKit work. |
| Android | Google Play and Firebase access | Required for signing, push, and Play Billing work. |
| Launch | Domain and deployment account access | Required for public API and launch checks. |

## Build Order

| Step | Codex Builds | Proof |
|---|---|---|
| 0 | Reset rules and mark old mobile scaffold as legacy | Build guide says no package-manager app stack. |
| 1 | Founder-facing product rules | PRD, backlog, and agent guide agree. |
| 2 | Python API shell | `/health` returns ok. |
| 3 | Data model and migrations | Alembic SQL generation passes. |
| 4 | Passwordless auth | Auth tests pass. |
| 5 | Subscription CRUD and platform sync contract | Subscription tests pass. |
| 6 | Alert engine | Alert tests pass. |
| 7 | Notification token and delivery logging | Trial-conversion integration test passes. |
| 8 | Native iOS SwiftUI client | Xcode build and simulator flow pass. |
| 9 | Native Android Kotlin client | Gradle and emulator flow pass. |
| 10 | External regression with TestSprite | TestSprite report has no launch blockers. |
| 11 | Deploy and launch prep | Production `/health` and magic-link email pass. |

## Local Proof Command

```bash
./scripts/test_all.sh
```

Expected proof:

- backend format and lint pass;
- backend tests pass;
- migration SQL generation passes;
- tutorial context validates;
- copy guard passes;
- Docker starts API and database;
- `/health` returns `{"status":"ok","db":"ok","version":"1.0.0"}`.

## Walkthrough Artefact

Open `BUILD_FROM_START.html` for the interactive build walkthrough.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
