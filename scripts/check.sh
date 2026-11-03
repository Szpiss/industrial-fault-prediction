#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"
source scripts/node-env.sh
(cd backend && .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/pytest -q && .venv/bin/python -m pip check)
(cd frontend && npm run typecheck && npm run lint && npm run format:check && npm test && npm run build)
