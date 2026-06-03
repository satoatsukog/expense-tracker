#!/usr/bin/env bash
# Run the API server (works even if editable install is broken).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
exec python -m uvicorn expense_tracker.main:app --reload --host 127.0.0.1 --port 8000
