# Thrifty No-Node QA Plan

## Decision

TestSprite MCP is not part of the required Thrifty build path because its official MCP server runs through `npx`. The application remains Python plus native mobile clients.

## Standard Gates

| Layer | Tooling | Proof |
|---|---|---|
| Backend API | Python, pytest, httpx, Ruff | Auth, subscription, alert, and integration tests pass. |
| Database | Alembic, Postgres in Docker | Migration SQL generates and `/health` reports database ok. |
| Tutorial files | Python stdlib HTML parser, JSON validation | Interactive controls, animation hooks, and launch-video context validate. |
| Copy safety | Python copy lint | Password drift and banned brand references fail the build. |
| External backend harness | TestSprite MCP, kept outside the app repo | Local/test-only token hook lets authenticated flows run without exposing production tokens. |
| iOS client | Xcode, XCTest, XCUITest | Native sign-in, add subscription, list refresh, and alert-permission flows pass. |
| Android client | Gradle, emulator-native tests | Native Android flows pass after Android enters scope. |

## External Services

External testing services are optional. They may inspect a deployed app or simulator output, but they must not add Node.js, npm, npx, pnpm, yarn, or a JavaScript build workflow to this repository.

For local authenticated API checks, the backend can expose `/v1/auth/test-token` only when both conditions are true:

- `APP_ENV` is `development`, `local`, or `test`;
- `ENABLE_TEST_AUTH_TOKENS=true`.

The endpoint is hidden in all other environments.

## One Command

```bash
./scripts/test_all.sh
```

That command is the local proof gate before a build slice is called complete.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
