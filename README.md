# Goethe-Faust — SPARQL Setup

DDB EDM dataset (8.6M triples) served via QLever, with SHMARQL as UI
and `mcp-server-qlever` for Claude Code access.

## Prerequisites

- Docker + Docker Compose plugin
- `output/ddbedm-goethe-faust.nt` (1.3 GB) — copy from source or
  re-run the pipeline to generate it

## Start

```bash
./setup.sh up
```

First run builds the QLever index (~few minutes). Subsequent runs
start in seconds — the index is persisted in `data/qlever-index/`.

## Services

| Service | URL | Description |
|---------|-----|-------------|
| SHMARQL | http://localhost:7032 | UI + SPARQL, backed by QLever |
| QLever  | http://localhost:7030 | Raw SPARQL endpoint |

Both are defined in `docker-compose.qlever.yml`.

## MCP (Claude Code)

Register once after `./setup.sh up`:

```bash
./setup.sh mcp-add
```

Then use QLever directly from Claude Code via the `goethe-faust` MCP
server.

## Other commands

```bash
./setup.sh down              # stop all services
./setup.sh status            # show container status
./setup.sh logs qlever       # tail QLever logs
./setup.sh logs shmarql      # tail SHMARQL logs
```

## Port overrides

```bash
QLEVER_PORT=7040 SHMARQL_PORT=7042 ./setup.sh up
```

## Transferring to another server

1. Copy this directory (including `output/ddbedm-goethe-faust.nt`)
2. Run `./setup.sh up`
