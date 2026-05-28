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

FULL_MODE=0
if [ "${KCC_OASIS_FULL:-0}" = "1" ]; then
  FULL_MODE=1
fi

REQUIREMENTS_FILE="$(PYTHONPATH="$ROOT_DIR/src:$ROOT_DIR/vendor/kcc${PYTHONPATH+:$PYTHONPATH}" "$ROOT_DIR/.venv/bin/python" -c 'from pathlib import Path; import sys; from kcc_oasis.bootstrap import requirements_file; print(requirements_file(Path(sys.argv[1]), full_mode=sys.argv[2] == "1"))' "$ROOT_DIR" "$FULL_MODE")"
printf 'Installing dependencies from: %s\n' "$REQUIREMENTS_FILE"
"$ROOT_DIR/.venv/bin/python" -m pip install -r "$REQUIREMENTS_FILE"
chmod +x "$ROOT_DIR/bin/kcc-oasis"

printf 'kcc-oasis is ready: %s\n' "$ROOT_DIR/bin/kcc-oasis"
