# Thrifty Agent Guide

This file is the working guide for any agent building or reviewing Thrifty. It keeps the product rules, sprint map, task ownership, and verification gates in one visible place.

## Product Rules

- Build for proactive interception: the primary experience shows future renewal and trial-conversion events only.
- Keep the backend Python 3.12 and FastAPI. Do not add Node.js, npm, npx, pnpm, yarn, a JavaScript server, or a JavaScript application build workflow.
- Keep auth passwordless. Do not add password fields, password storage, or password reset flows.
- Never invent subscription facts. Unknown amount, event time, cancel-by time, or terms stay null server-side and render as "unknown" with a reason.
- Use British/Scottish English in comments, copy, docs, errors, and commit messages.
- Do not reference sibling brands anywhere in the repo.

## Sprint 1 Goal

Ship the Phase 1 MVP as a usable local application:

- a FastAPI backend with magic-link auth, subscription CRUD, platform sync, alert computation, notification token storage, and health checks;
- native mobile clients after the API contract is proven;
- Docker, CI, deployment notes, and test coverage for the main behaviours.

## Epics

| Epic | Outcome | Status |
|---|---|---|
| THR-E1 Foundations | Python API, Postgres schema, passwordless auth | Built |
| THR-E2 Manual Add And Persistence | Manual subscription CRUD, sync contract, cross-device persistence | Built |
| THR-E3 Proactive Alerts | T-7d, T-3d, T-24h, T-2h alerts, notification logs, unknown handling | Built |
| THR-E4 StoreKit Ingestion | Native iOS billing ingestion | Stubbed for Phase 2 |
| THR-E5 Play Billing Ingestion | Native Android billing ingestion | Stubbed for Phase 2 |
| THR-E6 Plain-English Translation | Template-based explanations from known fields | Started |
| THR-E7 Plaid Monitoring | Bank-side recurring detection | Deferred to Phase 3 |
| THR-E8 Monetisation | Thrifty Plus and app-store billing | Deferred to Phase 3 |
| THR-E9 Hardening | Privacy, audit, passkeys, history, scale work | Deferred to Phase 4 |

## Sprint 1 Stories And Tasks

| Story | Task | Files |
|---|---|---|
| THR-S1 Passwordless sign-in | Magic-link issue, verify, logout, single-use token handling | `backend/app/routers/auth.py`, `backend/app/services/magic_link.py`, future native sign-in screens |
| THR-S2 Manual add subscription | Create, list, update, delete subscriptions | `backend/app/routers/subscriptions.py`, future native subscription screens |
| THR-S3 Persistence across reinstall | Server-side records and token-backed mobile refresh | `backend/app/models/subscription.py`, future native session storage |
| THR-S4 Pre-trial-conversion alert | Compute trial-conversion alert schedule | `backend/app/services/alert_engine.py`, `backend/tests/test_alert_engine.py` |
| THR-S5 Pre-renewal alert | Compute renewal alert schedule | `backend/app/services/alert_engine.py`, `backend/app/routers/alerts.py` |
| THR-S6 Uncertainty honesty | Null unknown values and render explicit unknown reasons | `backend/app/schemas/subscription.py`, `docs/09-COPY-DECK.md`, future native unknown states |
| THR-S10 Copy guard | Block banned wording and password drift | `scripts/lint_copy.py`, `docs/09-COPY-DECK.md` |
| THR-S11 CI and deployment | Run lint, tests, deployment checks, and deploy config | `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `docker-compose.yml`, `fly.toml` |
| THR-S12 Walkthrough and launch context | Keep an animated interactive product tutorial and launch-video outline | `OPEN_TUTORIAL.html`, `tutorial/remotion-context.json`, `docs/07-TUTORIAL-AND-LAUNCH-VIDEO.md` |
| THR-S13 Build from start guide | Keep a no-package-manager rebuild walkthrough and exact handoff checklist | `BUILD_FROM_START.html`, `docs/08-BUILD-FROM-START.md` |
| THR-S14 Copy deck | Preserve product copy while removing legacy mobile scaffolding | `docs/09-COPY-DECK.md` |

## Verification Gates

Run these from the repo root before marking work complete:

```bash
./scripts/test_all.sh
```

The script expands to:

```bash
cd backend && uv run --extra dev ruff format app alembic tests --check
cd backend && uv run --extra dev ruff check app alembic tests
cd backend && uv run python -m compileall app
cd backend && uv run --extra dev python -m pytest -v
cd backend && uv run python -m alembic upgrade head --sql
python3 -m json.tool tutorial/remotion-context.json >/tmp/thrifty-remotion-context.json
python3 scripts/test_tutorial_html.py
python scripts/lint_copy.py
docker compose up -d --build
curl -fsS http://localhost:8000/health
docker compose down
```

## No-Node QA Harness

The application and its standard test path do not depend on TestSprite, npm, npx, or Node.js.

- Backend/API proof: `pytest`, `httpx`, Ruff, `compileall`, Alembic SQL generation, Docker health smoke test.
- Tutorial proof: `scripts/test_tutorial_html.py`, `json.tool`, and copy lint.
- iOS proof when the native client exists: Xcode build plus XCTest/XCUITest simulator flows.
- Android proof when the native client exists: Gradle build plus native emulator tests.
- External hosted test services are optional only and must not add a Node.js runtime to the app repository.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
