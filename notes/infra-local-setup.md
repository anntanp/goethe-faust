# Local Infrastructure Setup

All services run on this Mac. Ollama runs natively (GPU/Metal); everything else runs in Docker.

## Services

| Service | Port | Compose file | Purpose |
|---|---|---|---|
| QLever | 7030 | `docker-compose.qlever.yml` | SPARQL endpoint |
| SHMARQL | 7032 | `docker-compose.qlever.yml` | SPARQL UI (QLever-backed) |
| MCPO | 8001 | `docker-compose.qlever.yml` | MCP→HTTP bridge (exposes QLever to OpenWebUI) |
| YASGUI | 7031 | `docker-compose.qlever.yml` | YASGUI query UI |
| SHMARQL (pyoxigraph) | 8030 | `docker-compose.shmarql.yml` | Standalone SHMARQL with own store |
| OpenWebUI | 3000 | `docker-compose.openwebui.yml` | Chat UI (connects to Ollama + MCPO) |
| Ollama | 11434 | native (not Docker) | LLM inference (Apple Silicon GPU) |

## Prerequisites

- Docker Desktop running
- Ollama installed and running natively: `ollama serve` (or launched via the app)
- Model pulled: `ollama pull gemma4:e4b` (or whichever model `DEFAULT_MODELS` is set to)

## Config

Copy once, edit to taste:

```bash
cp config.env.example config.env
```

Key variables in `config.env`:

```
NT_INPUT_DIR=<absolute path to directory containing .nq file>
NT_INPUT_GLOB=*.nq
NT_FORMAT=nq
INDEX_DIR=/absolute/path/to/goethe-faust/data/qlever-index
INDEX_NAME=goethe-faust
QLEVER_PORT=7030
SHMARQL_PORT=7032
MCPO_PORT=8001
```

## First-time startup

All `docker compose` commands must be run from `goethe-faust/`.

```bash
cd /Users/mta/Documents/claude/goethe-faust

# QLever stack (builds index on first run — ~10–20 min for 2.9 GB nq)
docker compose --env-file config.env -f docker-compose.qlever.yml up -d --wait

# OpenWebUI (connects to native Ollama + MCPO on qlever stack)
docker compose -f docker-compose.openwebui.yml up -d

# Optional: standalone SHMARQL with pyoxigraph store
docker compose -f docker-compose.shmarql.yml up -d
```

## Reload with new transform output

Run after the transform produces a new `output/transform/YYYYMMDD_HHMMSS/goethe-faust.nq`.

```bash
# 1. Re-run transform (from scripts/)
cd /Users/mta/Documents/claude/goethe-faust/scripts
/Users/mta/Documents/claude/goethe-faust/.venv/bin/python -m transform --stats dispatch

# 2. Update config.env with new input path
#    NT_INPUT_DIR=/Users/mta/Documents/claude/goethe-faust/output/transform/YYYYMMDD_HHMMSS

# 2. Stop qlever stack
docker compose -f docker-compose.qlever.yml down

# 3. Clear old index (force rebuild)
rm -f data/qlever-index/goethe-faust.ready \
       data/qlever-index/goethe-faust.index.* \
       data/qlever-index/goethe-faust.internal.* \
       data/qlever-index/goethe-faust.meta-data.json \
       data/qlever-index/goethe-faust.vocabulary.* \
       data/qlever-index/goethe-faust.text.*

# 4. Rebuild and start
docker compose --env-file config.env -f docker-compose.qlever.yml up -d --wait
```

OpenWebUI and standalone SHMARQL don't need to be restarted.

## QLever index flags

The compose file passes these flags to `qlever-index`:
- `-F nq` — N-Quads format (named graphs)
- `-W` — full-text search index from literals (`--text-words-from-literals`)

## Logs

```bash
docker compose -f docker-compose.qlever.yml logs -f qlever-goethe-faust
docker compose -f docker-compose.qlever.yml logs -f mcpo
```

## MCP (Claude Code)

MCPO exposes QLever as an OpenAPI tool server at `http://localhost:8001`.
OpenWebUI connects to it via Admin → Settings → Tools → `http://localhost:8001`.

To register directly with Claude Code (bypassing OpenWebUI):

```bash
./setup.sh mcp-add
```
