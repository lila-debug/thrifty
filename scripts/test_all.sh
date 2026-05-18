#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT/backend"
uv sync --extra dev
uv run --extra dev ruff format app alembic tests --check
uv run --extra dev ruff check app alembic tests
uv run python -m compileall app
uv run --extra dev python -m pytest -v
uv run python -m alembic upgrade head --sql >/tmp/thrifty-alembic.sql

cd "$ROOT"
python3 -m json.tool tutorial/remotion-context.json >/tmp/thrifty-remotion-context.json
python3 scripts/lint_copy.py

docker compose up -d --build
cleanup() {
  docker compose down
}
trap cleanup EXIT

for attempt in {1..30}; do
  if curl -fsS http://localhost:8000/health; then
    echo
    echo "All Thrifty checks passed."
    exit 0
  fi
  sleep 1
done

docker compose logs backend
echo "Backend health check did not pass within 30 seconds." >&2
exit 1
