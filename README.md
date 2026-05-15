# Thrifty — Claude Code Handoff Package

This package contains everything Claude Code needs to build Thrifty Phase 1 end-to-end in a single command, using parallel sub-agents.

## What's Inside

```
thrifty/
├── README.md                       # this file
├── docs/
│   ├── 01-PRD.md                   # locked product requirements
│   ├── 02-ARCHITECTURE.md          # locked system design
│   ├── 03-DATA-MODEL.md            # Postgres schema
│   ├── 04-API-CONTRACT.md          # full v1 API spec
│   └── 05-BACKLOG.md               # epics, stories, tasks
├── .claude/
│   └── commands/
│       └── goal.md                 # /goal slash command — orchestrates the build
└── agents/
    ├── backend-architect.md        # FastAPI + Postgres + alert engine
    ├── mobile-architect.md         # React Native + push + sign-in
    ├── devops-architect.md         # Docker + CI + Fly.io
    ├── qa-architect.md             # pytest suite
    └── content-architect.md        # British/Scottish copy
```

## Activation (in GitHub Codespaces)

1. Unzip into your Codespace repo root.
2. Move `agents/` contents to `.claude/agents/` (Claude Code's standard location):

```bash
mkdir -p .claude/agents
mv agents/*.md .claude/agents/
```

3. Open Claude Code in the Codespace terminal.
4. Run:

```
/goal
```

That's it. The build runs all five sub-agents in parallel, scaffolds backend + mobile + infra + tests + copy, runs the test suite, and prints the deploy command.

## What Gets Built

- Python 3.12 FastAPI backend with Postgres, magic-link auth, alert engine, APNs/FCM dispatcher
- React Native (Expo) mobile app for iOS + Android
- docker-compose for local dev
- GitHub Actions CI with banned-words and no-passwords linters
- Fly.io deploy config
- Full pytest suite with ≥ 85% coverage
- All copy in British/Scottish English

## Phase Override

```
/goal 2    # Phase 2: StoreKit + Play Billing ingestion
/goal 3    # Phase 3: Plaid + monetisation
/goal 4    # Phase 4: hardening
```

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
