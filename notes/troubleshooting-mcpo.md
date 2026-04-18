# Troubleshooting: MCPO docker-in-docker failure

## Problem

MCPO (`ghcr.io/open-webui/mcpo:latest`) wraps stdio MCP servers as
HTTP endpoints for OpenWebUI. The original setup spawned
`mcp-server-qlever` by running `docker run ...` inside the MCPO
container, which failed because Docker is not installed in MCPO.

## Failed attempts

| Attempt | Error |
|---------|-------|
| `apk add docker-cli` in Dockerfile | MCPO is Debian, not Alpine — `apk` not found |
| Mount macOS docker binary | macOS binary can't run in Linux container |
| Multi-stage copy from `docker:cli` | Would work but still docker-in-docker |

## Root cause

`mcp-server-qlever` is an npm package. There is no need for Docker
inside MCPO. MCPO's base image (`python:3.12-slim-bookworm`) already
includes **Node.js 22.x and npx** (installed via NodeSource in the
upstream Dockerfile). Run `npx mcp-server-qlever` directly.

## Fix

**Delete** `mcpo/Dockerfile` — use the stock image.

**Change** the `mcpo` service in `docker-compose.qlever.yml`:

```yaml
# Before (broken)
mcpo:
  build: ./mcpo
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  extra_hosts:
    - "host.docker.internal:host-gateway"
  command: >
    --port 8001 --
    docker run --rm -i
    --add-host=host.docker.internal:host-gateway
    ghcr.io/xorwell/mcp-server-qlever:latest
    -e http://host.docker.internal:${QLEVER_PORT:-7030}

# After (working)
mcpo:
  image: ghcr.io/open-webui/mcpo:latest
  extra_hosts:
    - "host.docker.internal:host-gateway"
  command: >
    --port 8001 --
    npx -y mcp-server-qlever
    -e http://host.docker.internal:${QLEVER_PORT:-7030}
```

Key changes:
- `build: ./mcpo` → `image:` (stock image, no custom build)
- Remove `volumes` — no docker socket needed
- Keep `extra_hosts` — container must reach host QLever port
- Replace `docker run ...` with `npx -y mcp-server-qlever ...`
- `-y` auto-installs the npm package on first run

## Verification

```bash
# Start MCPO
docker compose -f docker-compose.qlever.yml \
  --env-file .env.runtime up -d mcpo

# Check container is running
docker ps | grep mcpo

# List tools exposed by mcp-server-qlever
curl -s http://localhost:8001/openapi.json \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for k in d['paths']:
    print(k)
"
```

Expected output — one path per tool, e.g.:

```
/sparql__query
/sparql__update
...
```

MCPO converts MCP tools to HTTP endpoints. Each path corresponds to
one tool from `mcp-server-qlever`. If the list is non-empty, MCPO
started the npm package successfully and is ready for OpenWebUI.

## Known limitation: MCPO tools not invoked by Ollama

Even with MCPO connected and green in OpenWebUI, Ollama models do
not call the tools. This is a known upstream bug — the `tools`
parameter is not propagated through OpenWebUI's Ollama proxy
(open-webui/open-webui #7597).

**Workaround**: use a native Python tool instead of MCPO.

See `openwebui-native-tool.md` and `openwebui-sparql-tool.py`
for a drop-in replacement that works reliably with Ollama.
