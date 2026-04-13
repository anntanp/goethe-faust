# Plan: Configurable setup.sh

## Context
`setup.sh` and `docker-compose.qlever.yml` have hardcoded values (NT filename,
index directory, ports). This plan makes them configurable via a single
`config.env` file so the stack can be reused for different datasets and
deployed on other servers without editing source files.

## Config file: `config.env`

User-editable, gitignored. Sourced by `setup.sh` and passed to docker compose
via `--env-file`. Ship `config.env.example` as the committed template.

```bash
QLEVER_PORT=7030          # QLever raw SPARQL endpoint
SHMARQL_PORT=7032         # SHMARQL UI + SPARQL
NT_INPUT=output/ddbedm-goethe-faust.nt  # file or directory of .nt files
INDEX_DIR=data/qlever-index             # QLever binary index (persisted)
LOG_DIR=data/logs                       # log output directory
QLEVER_MEMORY=4GB         # memory cap for QLever server
INDEX_NAME=goethe-faust   # base name for QLever index files
```

## Changes: `setup.sh`

1. Source `config.env` if present; otherwise use inline defaults.
2. Compute `NT_INPUT_DIR` and `NT_INPUT_GLOB` from `NT_INPUT`:
   ```bash
   if [ -d "$NT_INPUT" ]; then
     NT_INPUT_DIR="$(realpath "$NT_INPUT")"
     NT_INPUT_GLOB="*.nt"
   else
     NT_INPUT_DIR="$(realpath "$(dirname "$NT_INPUT")")"
     NT_INPUT_GLOB="$(basename "$NT_INPUT")"
   fi
   export NT_INPUT_DIR NT_INPUT_GLOB INDEX_DIR INDEX_NAME
   ```
3. Pass `--env-file config.env` to all `docker compose` calls (when file exists).
4. `mkdir -p "$INDEX_DIR" "$LOG_DIR"` in `cmd_up`.
5. `cmd_logs`: tee docker compose logs to `$LOG_DIR/qlever.log` /
   `$LOG_DIR/shmarql.log`.
6. Remove dead references to pyoxigraph SHMARQL compose file and YASGUI.

## Changes: `docker-compose.qlever.yml`

- Volume mounts:
  - `${NT_INPUT_DIR}:/input:ro` (was `./output:/input:ro`)
  - `${INDEX_DIR}:/data` (was `./data/qlever-index:/data`)
- Pass env vars into container: `NT_INPUT_GLOB`, `INDEX_NAME`
- Container script:
  ```bash
  FILES=$(ls /input/$NT_INPUT_GLOB 2>/dev/null | tr '\n' ' ')
  /qlever/qlever-index -i /data/$INDEX_NAME -f $FILES -F nt -s /data/settings.json
  exec /qlever/qlever-server -i /data/$INDEX_NAME ...
  ```
- `index.ready` sentinel: `/data/$INDEX_NAME.ready`
  (keyed to index name so different datasets don't collide)
- Remove `yasgui` service.
- Update header comment.

## New file: `config.env.example`

Committed template; user copies to `config.env` and edits.

## `.gitignore`

Add `config.env` if not already present.

## Files

| Action | File |
|--------|------|
| Modify | `setup.sh` |
| Modify | `docker-compose.qlever.yml` |
| Create | `config.env.example` |
| Gitignore | `config.env` |

## Verification

1. No `config.env` → `./setup.sh up` uses defaults, works as before.
2. `SHMARQL_PORT=7099` in `config.env` → SHMARQL appears on 7099.
3. `NT_INPUT=output/` (directory) → QLever indexes all `.nt` files in dir.
4. `./setup.sh logs qlever` → output written to `data/logs/qlever.log`.
