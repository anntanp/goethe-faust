#!/usr/bin/env bash
# Purpose:    Start/stop QLever + SHMARQL for an RDF dataset.
# Usage:      ./setup.sh <command>
#             Commands: up | down | status | logs | mcp-add
# Inputs:     config.env (optional, copy from config.env.example)
#             NT_INPUT: .nt file or directory of .nt files
# Outputs:    $INDEX_DIR — QLever binary index (persisted)
#             $LOG_DIR   — log files from docker compose
# Dependencies: docker, docker compose
# Assumptions: Run from the goethe-faust/ directory.
#              On a new server, copy the directory and run ./setup.sh up.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- Defaults (overridden by config.env) ---
QLEVER_PORT=7030
SHMARQL_PORT=7032
NT_INPUT=output/ddbedm-goethe-faust.nt
INDEX_DIR=data/qlever-index
LOG_DIR=data/logs
QLEVER_MEMORY=4GB
INDEX_NAME=goethe-faust

# Load config.env if present
if [ -f config.env ]; then
  # shellcheck disable=SC1091
  set -a; source config.env; set +a
fi

# Resolve NT_INPUT to absolute path
NT_INPUT="$(realpath "$NT_INPUT" 2>/dev/null || echo "$NT_INPUT")"

# Derive NT_INPUT_DIR and NT_INPUT_GLOB for docker compose
if [ -d "$NT_INPUT" ]; then
  NT_INPUT_DIR="$NT_INPUT"
  NT_INPUT_GLOB="*.nt"
else
  NT_INPUT_DIR="$(dirname "$NT_INPUT")"
  NT_INPUT_GLOB="$(basename "$NT_INPUT")"
fi

# INDEX_DIR must be absolute for docker compose to treat it as a bind mount
mkdir -p "$INDEX_DIR"
INDEX_DIR="$(realpath "$INDEX_DIR")"

# Write all computed vars to a runtime env file for docker compose.
# This is more reliable than relying on shell export inheritance.
cat > .env.runtime << EOF
NT_INPUT_DIR=${NT_INPUT_DIR}
NT_INPUT_GLOB=${NT_INPUT_GLOB}
INDEX_DIR=${INDEX_DIR}
INDEX_NAME=${INDEX_NAME}
QLEVER_PORT=${QLEVER_PORT}
SHMARQL_PORT=${SHMARQL_PORT}
QLEVER_MEMORY=${QLEVER_MEMORY}
EOF

compose() {
  docker compose -f docker-compose.qlever.yml --env-file .env.runtime "$@"
}

check_prereqs() {
  if ! command -v docker &>/dev/null; then
    echo "ERROR: docker not found." >&2
    exit 1
  fi
  if ! docker compose version &>/dev/null 2>&1; then
    echo "ERROR: 'docker compose' plugin not found." >&2
    exit 1
  fi
  if [ -d "$NT_INPUT" ]; then
    if ! ls "$NT_INPUT"/*.nt &>/dev/null; then
      echo "ERROR: no .nt files found in $NT_INPUT" >&2
      exit 1
    fi
  elif [ ! -f "$NT_INPUT" ]; then
    echo "ERROR: $NT_INPUT not found." >&2
    echo "  Set NT_INPUT in config.env or copy the file." >&2
    exit 1
  fi
}

cmd_up() {
  check_prereqs
  mkdir -p "$LOG_DIR"

  echo "=== Starting QLever + SHMARQL ==="
  echo "  Input:    $NT_INPUT_DIR/$NT_INPUT_GLOB"
  echo "  Index:    $INDEX_DIR"
  compose up -d --wait --wait-timeout 600
  echo ""
  echo "  SHMARQL UI:      http://localhost:$SHMARQL_PORT"
  echo "  SPARQL endpoint: http://localhost:$QLEVER_PORT"
  echo ""
  echo "  MCP: run './setup.sh mcp-add' to register with Claude Code"
}

cmd_down() {
  compose down
}

cmd_status() {
  compose ps
}

cmd_logs() {
  local service="${1:-}"
  case "$service" in
    qlever)
      compose logs -f qlever-goethe-faust \
        | tee "$LOG_DIR/qlever.log"
      ;;
    shmarql)
      compose logs -f shmarql \
        | tee "$LOG_DIR/shmarql.log"
      ;;
    *)
      echo "Usage: ./setup.sh logs <qlever|shmarql>"
      exit 1
      ;;
  esac
}

cmd_mcp_add() {
  echo "Registering MCP server with Claude Code..."
  claude mcp add "$INDEX_NAME" -- \
    docker run --rm -i --network=host \
    ghcr.io/xorwell/mcp-server-qlever:latest \
    -e "http://localhost:$QLEVER_PORT"
  echo "Done. Test with: claude mcp list"
}

case "${1:-}" in
  up)      cmd_up ;;
  down)    cmd_down ;;
  status)  cmd_status ;;
  logs)    cmd_logs "${2:-}" ;;
  mcp-add) cmd_mcp_add ;;
  *)
    echo "Usage: ./setup.sh <command>"
    echo "  up        Start QLever + SHMARQL (builds index on first run)"
    echo "  down      Stop all services"
    echo "  status    Show container status"
    echo "  logs      ./setup.sh logs <qlever|shmarql>"
    echo "  mcp-add   Register QLever as Claude Code MCP server"
    echo ""
    echo "Config: copy config.env.example to config.env and edit."
    echo "Active settings:"
    echo "  NT_INPUT=$NT_INPUT"
    echo "  INDEX_DIR=$INDEX_DIR"
    echo "  LOG_DIR=$LOG_DIR"
    echo "  QLEVER_PORT=$QLEVER_PORT"
    echo "  SHMARQL_PORT=$SHMARQL_PORT"
    echo "  INDEX_NAME=$INDEX_NAME"
    exit 1
    ;;
esac
