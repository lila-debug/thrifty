#!/usr/bin/env bash
set -euo pipefail

docker compose up -d postgres
cd backend
uv sync --extra dev
uv run alembic upgrade head
cd ..
echo "Thrifty backend ready. Run: cd backend && uv run uvicorn app.main:app --reload"
