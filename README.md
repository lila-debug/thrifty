# Thrifty — Build Handoff

Thrifty is being rebuilt contract-first:

- Python 3.12 FastAPI backend first.
- Native iOS client after the API contract is proven.
- Native Android client after iOS and backend flows are stable.
- No package-manager app stack inside this repo.

## Start Here

Open:

```text
BUILD_FROM_START.html
```

That walkthrough explains the build order, what Codex does, what you provide, and what proof shows each step worked.

For the product demo and launch story, open:

```text
OPEN_TUTORIAL.html
```

## Current Proof Command

```bash
./scripts/test_all.sh
```

This checks backend formatting, backend tests, migration SQL generation, tutorial context, copy lint, Docker startup, and `/health`.

## Useful Files

| File | Purpose |
|---|---|
| `AGENTS.md` | Active agent rules, sprint map, and verification gates. |
| `BUILD_FROM_START.html` | Interactive build walkthrough from the first brick. |
| `OPEN_TUTORIAL.html` | Interactive product and launch walkthrough. |
| `docs/08-BUILD-FROM-START.md` | Text version of the build path. |
| `docs/09-COPY-DECK.md` | Preserved product copy. |
| `backend/` | FastAPI backend. |

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
