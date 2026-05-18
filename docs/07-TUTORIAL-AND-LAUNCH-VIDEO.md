# Thrifty — Interactive Tutorial And Launch Video Brief

## Walkthrough Artefacts

| File | Use |
|---|---|
| `OPEN_TUTORIAL.html` | Open locally for the animated interactive walkthrough, product demo flow, operator notes, and narration copy. No install or server required. |
| `tutorial/remotion-context.json` | Use as context for a future video composition: scene structure, timing, proof points, and narration. |
| `scripts/test_all.sh` | Run the full local proof path before recording or rendering launch material. |

## Walkthrough Goal

The tutorial should make Thrifty feel immediately understandable to a non-technical viewer:

1. Sign in without a password.
2. See future charges first.
3. Add a subscription without inventing unknown facts.
4. Keep the list across sessions and devices.
5. Schedule alerts before the charge.
6. Log notification outcomes honestly.
7. Prove the build with tests and health checks.
8. Reuse the story as the launch video spine.

## Launch Video Direction

Recommended launch format: vertical `1080x1350`, 30 fps, roughly 90 seconds.

Use `tutorial/remotion-context.json` as the canonical scene source. Each scene includes:

- `durationSeconds`
- `title`
- `narration`
- `visuals`
- `proof`

Keep the video light-mode, practical, and evidence-led. Avoid purple, pink, receipt-first framing, fake certainty, and password language.

Do not add a video build system inside this application repo. If a Remotion render is used later, run it in a separate video workspace so the application stays clean.

## Recording Checklist

Before recording or rendering:

```bash
./scripts/test_all.sh
```

Expected proof:

- backend format and lint pass;
- backend tests pass;
- tutorial context validates;
- copy guard passes;
- Docker starts the API and database;
- `/health` returns `{"status":"ok","db":"ok","version":"1.0.0"}`.

## Vercel Fit

The current Thrifty app is a Dockerised FastAPI backend plus mobile shell, so Fly.io remains the better fit for the API. Vercel is useful only if the walkthrough becomes a public tutorial page or if a future web dashboard is added.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
