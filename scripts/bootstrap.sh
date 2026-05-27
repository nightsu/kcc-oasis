#!/usr/bin/env sh
set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"
KCC_REPO="${KCC_REPO:-https://github.com/ciromattia/kcc.git}"

if [ ! -d "$ROOT_DIR/vendor/kcc/.git" ] && [ ! -f "$ROOT_DIR/vendor/kcc/kcc-c2e.py" ]; then
  mkdir -p "$ROOT_DIR/vendor"
  git clone "$KCC_REPO" "$ROOT_DIR/vendor/kcc"
fi

if [ ! -x "$ROOT_DIR/.venv/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$ROOT_DIR/.venv"
fi

"$ROOT_DIR/.venv/bin/python" -m pip install -r "$ROOT_DIR/vendor/kcc/requirements.txt"
chmod +x "$ROOT_DIR/bin/kcc-oasis"

printf 'kcc-oasis is ready: %s\n' "$ROOT_DIR/bin/kcc-oasis"
