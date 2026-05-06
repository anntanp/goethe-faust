#!/usr/bin/env bash
# Purpose:   Create a Python venv with all dependencies for the GeMeA transform pipeline.
# Usage:     bash scripts/setup_venv.sh
#            Run from the goethe-faust project root.
# Outputs:   .venv/ in the project root
# Deps:      python3, pip

set -euo pipefail

GOETHE="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$GOETHE/.venv"

python3 -m venv "$VENV"
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install -r "$GOETHE/requirements.txt"

echo "Venv ready: $VENV"
echo "Python: $("$VENV/bin/python3" --version)"
echo "duckdb: $("$VENV/bin/python3" -c 'import duckdb; print(duckdb.__version__)')"
