#!/usr/bin/env bash
# macOS: pip may mark .pth files as hidden; Python 3.12+ then skips them.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE="${ROOT}/.venv/lib/python3.12/site-packages"
if [[ ! -d "$SITE" ]]; then
  echo "No .venv found. Run: python3 -m venv .venv && pip install -e \".[dev]\""
  exit 1
fi
for pth in "$SITE"/*.pth; do
  [[ -f "$pth" ]] || continue
  chflags nohidden "$pth" 2>/dev/null || true
done
echo "Fixed .pth visibility. Test with: python -c \"import expense_tracker; print('OK')\""
