---
description: Execute the full Thrifty Phase 1 MVP build end-to-end, spawning parallel sub-agents for backend, mobile, and infrastructure work
argument-hint: [phase number, e.g. "1" — defaults to 1]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
model: claude-opus-4-7
---

# /goal — Thrifty Phase 1 MVP Build

You are the lead engineer building **Thrifty**, the proactive subscription-interception app for Lila Olufemi Abegunrin. You have been handed a locked PRD, Architecture, Data Model, API Contract, and Backlog. Build Phase 1 to a deployable state.

## Non-Negotiable Rules

1. **Language:** British/Scottish English only in all code comments, UI copy, commit messages, error messages, and documentation. No Americanisms. Banned: "color" (use "colour"), "organize" (use "organise"), "favorite" (use "favourite"), "gonna", "wanna", "awesome", "totally", "absolutely", "no worries", "sounds good".
2. **Backend:** Python 3.12 + FastAPI only. **Node.js is banned** — any package.json must only exist inside the React Native mobile app.
3. **Auth:** Passwordless only. **No password fields anywhere.** Any password-related code fails the build.
4. **Philosophy:** Offensive, not defensive. **Never** build a primary UI that shows past charges. Primary view is future events only.
5. **Honesty:** Never invent amount, event time, or cancel-by. Unknown values must be stored as NULL and rendered as "unknown" with a reason.
6. **Cross-promotion:** Never reference FlatFinder, Prototype Cafe, MAAC, or any sibling brand in any file.
7. **Footer:** Every generated Markdown document ends with:
   ```
   Based on true events. Sadly.
   Canadian Kind, Scottish Strong.
   © 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
   ```

## Inputs

Read these before starting:
- `docs/01-PRD.md`
- `docs/02-ARCHITECTURE.md`
- `docs/03-DATA-MODEL.md`
- `docs/04-API-CONTRACT.md`
- `docs/05-BACKLOG.md`

## Execution Plan — Parallel Sub-Agents

Spawn the following sub-agents **in parallel** using the Task tool. Each agent has its own definition in `.claude/agents/`. Do not serialise these; launch all five concurrently:

1. **backend-architect** — scaffold FastAPI app, Postgres, Alembic, magic-link auth, subscriptions CRUD, alert engine, APScheduler worker, APNs/FCM dispatcher. Output: `backend/` directory.
2. **mobile-architect** — scaffold React Native (Expo bare) app, sign-in screen with deep-link handler, subscription list/add/edit screens, push registration, local-notification fallback, "unknown" UI states. Output: `mobile/` directory.
3. **devops-architect** — produce `docker-compose.yml` (Postgres + API), `Dockerfile` for backend, GitHub Actions CI (pytest + ruff + RN typecheck + banned-words lint), Railway/Fly.io deploy config. Output: `.github/`, `docker-compose.yml`, `fly.toml`.
4. **qa-architect** — write pytest suite covering auth flow, subscription CRUD, alert computation edge cases (timezone, unknown precision, multi-currency), and an integration test that simulates a trial-conversion alert firing. Output: `backend/tests/`.
5. **content-architect** — write all user-facing copy in British/Scottish English: onboarding screens, alert push payloads (4 lead-time variants), "unknown" reason strings, error messages, plain-English term-translation templates. Output: `mobile/src/copy/en-GB.ts`.

## After Sub-Agents Complete

1. Run `docker compose up -d` and verify `/health` returns 200.
2. Run `cd backend && pytest -v` and confirm all tests pass.
3. Run `cd mobile && npx tsc --noEmit` and confirm zero TypeScript errors.
4. Run the banned-words linter across the entire repo: `python scripts/lint_copy.py` — must exit 0.
5. Produce `docs/06-DEPLOYMENT.md` with the single command needed to deploy to Fly.io.
6. Print a final summary table: files created, tests passing, deployment command.

## Stop Conditions

- If any sub-agent reports an unrecoverable blocker, stop and report it as `STATUS: UNBUILDABLE. REASON: [one sentence]`.
- Do not ask for confirmation between steps. Do not produce partial outputs.
- The user will only see the final activation command.

## Phase Argument

If `$1` is provided and equals `2`, `3`, or `4`, build that phase instead. Default is `1`.

Begin.
