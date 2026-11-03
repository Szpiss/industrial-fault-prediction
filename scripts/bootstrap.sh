#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
source scripts/node-env.sh
PYTHON_BIN="${PYTHON_BIN:-python3.12}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3.12 missing. Set PYTHON_BIN to a compatible Python executable." >&2
  exit 1
fi
"$PYTHON_BIN" -c 'import sys; assert (3,12) <= sys.version_info < (3,15), "Python 3.12-3.14 required; 3.12 recommended"'
if [ ! -d backend/.venv ]; then
  "$PYTHON_BIN" -m venv backend/.venv
fi
if [ ! -f .env ]; then
  (umask 077; cp .env.example .env)
fi
backend/.venv/bin/python -m pip install -r backend/requirements-dev.lock
backend/.venv/bin/python -m pip install --no-deps --no-build-isolation -e backend
(cd backend && .venv/bin/alembic upgrade head)
(cd frontend && npm ci)
echo "Setup complete. Start ./scripts/backend.sh and ./scripts/frontend.sh in separate terminals."
