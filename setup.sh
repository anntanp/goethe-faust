#!/usr/bin/env bash
# Purpose:    Start/stop QLever and SHMARQL for the goethe-faust DDB EDM
#             dataset.
# Usage:      ./setup.sh <command>
#             Commands: up | down | status | logs | mcp-add
# Inputs:     output/ddbedm-goethe-faust.nt (1.3 GB, 8.6M triples)
# Outputs:    data/qlever-index/  — QLever binary index (persisted)
#             data/shmarql-store/ — pyoxigraph store (persisted)
# Dependencies: docker, docker compose
# Assumptions: Run from the goethe-faust/ directory.
#              On a new server, copy the full directory (including output/*.nt)
#              then run this script.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

NT_FILE="output/ddbedm-goethe-faust.nt"
QLEVER_PORT="${QLEVER_PORT:-7030}"
YASGUI_PORT="${YASGUI_PORT:-7031}"
SHMARQL_QLEVER_PORT="${SHMARQL_PORT:-7032}"
SHMARQL_PORT="${SHMARQL_PORT:-8030}"

check_prereqs() {
  if ! command -v docker &>/dev/null; then
    echo "ERROR: docker not found. Install Docker Desktop or Docker Engine." >&2
    exit 1
  fi
  if ! docker compose version &>/dev/null 2>&1; then
    echo "ERROR: 'docker compose' plugin not found." >&2
    exit 1
  fi
  if [ ! -f "$NT_FILE" ]; then
    echo "ERROR: $NT_FILE not found." >&2
    echo "  Copy it from the source server or re-run the pipeline." >&2
    exit 1
  fi
}

cmd_up() {
  check_prereqs
  mkdir -p data/qlever-index data/shmarql-store

  echo "=== Starting QLever + YASGUI + SHMARQL ==="
  docker compose -f docker-compose.qlever.yml up -d --wait \
    --wait-timeout 600
  echo "  SPARQL UI (YASGUI):   http://localhost:$YASGUI_PORT"
  echo "  SPARQL UI (SHMARQL):  http://localhost:$SHMARQL_QLEVER_PORT"
  echo "  SPARQL endpoint:      http://localhost:$QLEVER_PORT"
  echo ""

  echo "=== Starting SHMARQL (port $SHMARQL_PORT) ==="
  docker compose -f docker-compose.shmarql.yml up -d
  echo "  SPARQL endpoint: http://localhost:$SHMARQL_PORT/sparql"
  echo "  UI:              http://localhost:$SHMARQL_PORT/"
  echo ""

  echo "=== MCP server (Claude Code) ==="
  echo "  Run once to register:"
  echo "  claude mcp add goethe-faust -- docker run --rm -i --network=host \\"
  echo "    ghcr.io/xorwell/mcp-server-qlever:latest \\"
  echo "    -e http://localhost:$QLEVER_PORT"
}

cmd_down() {
  echo "Stopping QLever..."
  docker compose -f docker-compose.qlever.yml down
  echo "Stopping SHMARQL..."
  docker compose -f docker-compose.shmarql.yml down
}

cmd_status() {
  echo "=== QLever ==="
  docker compose -f docker-compose.qlever.yml ps
  echo ""
  echo "=== SHMARQL ==="
  docker compose -f docker-compose.shmarql.yml ps
}

cmd_logs() {
  local service="${1:-}"
  if [ "$service" = "qlever" ]; then
    docker compose -f docker-compose.qlever.yml logs -f
  elif [ "$service" = "shmarql" ]; then
    docker compose -f docker-compose.shmarql.yml logs -f
  else
    echo "Usage: ./setup.sh logs <qlever|shmarql>"
    exit 1
  fi
}

cmd_mcp_add() {
  echo "Registering MCP server with Claude Code..."
  claude mcp add goethe-faust -- docker run --rm -i --network=host \
    ghcr.io/xorwell/mcp-server-qlever:latest -e "http://localhost:$QLEVER_PORT"
  echo "Done. Test with: claude mcp list"
}

case "${1:-}" in
  up)       cmd_up ;;
  down)     cmd_down ;;
  status)   cmd_status ;;
  logs)     cmd_logs "${2:-}" ;;
  mcp-add)  cmd_mcp_add ;;
  *)
    echo "Usage: ./setup.sh <command>"
    echo "  up        Start QLever + SHMARQL (builds index on first run)"
    echo "  down      Stop both services"
    echo "  status    Show container status"
    echo "  logs      ./setup.sh logs <qlever|shmarql>"
    echo "  mcp-add   Register QLever as Claude Code MCP server"
    echo ""
    echo "Ports (override via env vars):"
    echo "  QLEVER_PORT=$QLEVER_PORT  (QLever SPARQL)"
    echo "  SHMARQL_PORT=$SHMARQL_PORT  (SHMARQL UI + SPARQL)"
    exit 1
    ;;
esac
