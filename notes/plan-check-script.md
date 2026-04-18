# Plan: check.sh — Status check + guided setup

## Context
A single script that inspects the current machine for running QLever,
SHMARQL, and MCP-to-Claude containers, then offers to continue with
whichever setup step is missing: MCP registration with Claude Code, or
Ollama + OpenWebUI browser chat.

## Script: `check.sh`

### Step 1 — Check running containers

```bash
docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}' \
  | grep -E 'qlever|shmarql|mcpo'
```

Report each service as UP / DOWN:

| Check | Command |
|-------|---------|
| QLever | `curl -sf http://localhost:7030/?cmd=stats` |
| SHMARQL | `curl -sf http://localhost:7032/` |
| MCPO | `curl -sf http://localhost:8001/openapi.json` |
| MCP→Claude | `claude mcp list 2>/dev/null \| grep goethe-faust` |

### Step 2 — Conditional next steps

```
if QLever is DOWN:
    print "Run ./setup.sh up first"
    exit

if QLever is UP and MCP→Claude not registered:
    prompt: "Register MCP server with Claude Code? [y/N]"
    if yes: ./setup.sh mcp-add

if QLever is UP and MCPO is DOWN:
    prompt: "Start MCPO for OpenWebUI? [y/N]"
    if yes: docker compose -f docker-compose.qlever.yml up -d mcpo

if QLever is UP and MCPO is UP:
    print "OpenWebUI tools URL: http://$(hostname -I | awk '{print $1}'):8001"
    print "Add this in OpenWebUI → Admin → Settings → Tools"
```

## File to create
- `goethe-faust/check.sh` (executable)

## Key shell commands used
- `docker ps --format` — list containers with name/status/ports
- `curl -sf` — silent health checks (exit 0 = up, non-zero = down)
- `claude mcp list` — check MCP registrations
- `hostname -I` — get local IP for cross-server URLs
- `docker compose ... up -d mcpo` — start individual service
