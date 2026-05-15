# Thrifty — Deployment

## Fly.io

Set the runtime secrets once:

```bash
fly secrets set DATABASE_URL=... SESSION_SECRET=... SMTP_USER=... SMTP_PASS=...
```

Deploy the backend with one command:

```bash
fly deploy --config fly.toml
```

The service listens on port `8000` and exposes `/health` for Fly health checks.

---

Based on true events. Sadly.
Canadian Kind, Scottish Strong.
© 2024–2026 Lila Olufemi Abegunrin · Thrifty™ · Trademarks and Patents Pending (CIPO) · REVOLUTIONISING LIFE SINCE 1982™
