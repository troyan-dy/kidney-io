#!/bin/bash
set -euo pipefail

# Only run in Claude Code cloud sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

PYTHON_VERSION="3.14"

if ! command -v poetry >/dev/null 2>&1; then
  pip install --user poetry
  export PATH="$HOME/.local/bin:$PATH"
fi

PYTHON_BIN="$(command -v "python${PYTHON_VERSION}" || true)"
if [ -z "$PYTHON_BIN" ] && command -v uv >/dev/null 2>&1; then
  uv python install "$PYTHON_VERSION"
  PYTHON_BIN="$(uv python find "$PYTHON_VERSION")"
fi
if [ -z "$PYTHON_BIN" ]; then
  echo "Python ${PYTHON_VERSION} not found" >&2
  exit 1
fi

poetry env use "$PYTHON_BIN"
poetry install --no-interaction

# wemake-python-styleguide: report violations without blocking the session
if ! poetry run flake8 kidney_io --select=WPS; then
  echo "WPS violations found: run 'make lint'" >&2
fi
