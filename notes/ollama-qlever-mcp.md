# Ollama + QLever MCP: Feasibility & Setup (Distributed)

## Context
Ollama runs on Server A; QLever + SHMARQL run on Server B.
Ollama doesn't support MCP natively — a bridge is required.
mcp-server-qlever uses **stdio** transport (subprocess), so it always
runs locally alongside the bridge. The connection to QLever is plain
HTTP, so it can point to any host.

## Key insight
The stdio transport is only between the bridge and the MCP subprocess
(both local). The QLever URL is just an HTTP endpoint — it can be on
any reachable host. So distributed setup only requires:
- Server B's QLever port (7030) reachable from Server A
- The bridge config points to `http://SERVER_B:7030` instead of localhost

## Option A — ollama-mcp-bridge (API/script use, no UI)

Everything runs on Server A. The MCP subprocess connects to Server B
over HTTP.

```
Server A                              Server B
────────────────────────────          ──────────────────
Ollama client                         QLever :7030
  → ollama-mcp-bridge :11435          SHMARQL :7032
    → Ollama :11434
    → mcp-server-qlever (stdio)
        → http://SERVER_B:7030
```

**Config on Server A** (`ollama-mcp/config.json`):
```json
{
  "mcpServers": {
    "goethe-faust": {
      "command": "docker",
      "args": [
        "run","--rm","-i",
        "ghcr.io/xorwell/mcp-server-qlever:latest",
        "-e","http://SERVER_B:7030"
      ]
    }
  },
  "ollamaHost": "http://localhost:11434",
  "model": "llama3.1"
}
```

**Requirement**: Server B must expose port 7030 to Server A (firewall).

## Option B — OpenWebUI + MCPO (browser chat UI)

MCPO runs on Server B (alongside QLever). OpenWebUI runs on Server A
(alongside Ollama) and connects to both.

```
Server A                              Server B
────────────────────────────          ──────────────────
Browser                               QLever :7030
  → OpenWebUI :3000                   SHMARQL :7032
    → Ollama :11434 (local)           MCPO :8001
    → MCPO http://SERVER_B:8001         → mcp-server-qlever (stdio)
                                            → localhost:7030
```

MCPO wraps the stdio MCP server as an OpenAPI HTTP service, making it
network-accessible. OpenWebUI v0.6.31+ calls it as a native tool.

**Server B** (`docker-compose.qlever.yml` addition):
```yaml
  mcpo:
    image: ghcr.io/open-webui/mcpo:latest
    ports:
      - "8001:8001"
    command: ["--port","8001","--",
              "docker","run","--rm","-i","--network=host",
              "ghcr.io/xorwell/mcp-server-qlever:latest",
              "-e","http://localhost:7030"]
```

**Server A**: OpenWebUI configured with:
- Ollama URL: `http://localhost:11434`
- Tools URL: `http://SERVER_B:8001`

**Requirement**: Server B must expose port 8001 to Server A.

## Recommendation
- **Option A** if querying via scripts or API — simpler, fewer services
- **Option B** if a browser chat interface is the goal

## Files to create (Option A)
- `goethe-faust/ollama-mcp/config.json` — bridge config (Server A)
- `goethe-faust/ollama-mcp/README.md` — setup steps for Server A

## Files to modify (Option B)
- `goethe-faust/docker-compose.qlever.yml` — add `mcpo` service (Server B)
- `goethe-faust/README.md` — document OpenWebUI setup for Server A

## Networking requirement (both options)
Server B must allow inbound TCP on the relevant port from Server A:
- Option A: port 7030 (QLever)
- Option B: port 8001 (MCPO)
