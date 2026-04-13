# Goethe-Faust — SPARQL Setup

DDB EDM dataset (8.6M triples) served via QLever, with SHMARQL as UI
and `mcp-server-qlever` for Claude Code access.

## Prerequisites

- Docker + Docker Compose plugin
- `output/ddbedm-goethe-faust.nt` (1.3 GB) — copy from source or
  re-run the pipeline to generate it

## Configuration

Copy the example config and edit as needed:

```bash
cp config.env.example config.env
```

Key settings in `config.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `NT_INPUT` | `output/ddbedm-goethe-faust.nt` | Single `.nt` file or directory |
| `QLEVER_PORT` | `7030` | QLever SPARQL endpoint port |
| `SHMARQL_PORT` | `7032` | SHMARQL UI + SPARQL port |
| `INDEX_DIR` | `data/qlever-index` | Persisted QLever binary index |
| `LOG_DIR` | `data/logs` | Log output directory |
| `INDEX_NAME` | `goethe-faust` | Base name for index files |
| `QLEVER_MEMORY` | `4GB` | Memory cap for QLever server |

## Start

```bash
./setup.sh up
```

First run builds the QLever index (~few minutes). Subsequent runs
start in seconds — the index is persisted in `$INDEX_DIR`.

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

## Other commands

```bash
./setup.sh down              # stop all services
./setup.sh status            # show container status
./setup.sh logs qlever       # tail QLever logs (also writes to $LOG_DIR)
./setup.sh logs shmarql      # tail SHMARQL logs (also writes to $LOG_DIR)
```

## Transferring to another server

1. Copy this directory (including `output/ddbedm-goethe-faust.nt`)
2. Edit `config.env` if needed
3. Run `./setup.sh up`
