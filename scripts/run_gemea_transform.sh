#!/usr/bin/env bash
# Purpose:   Full GeMeA corpus transform — 128 workers across 7 sectors in parallel (Option C, teach03)
# Usage:     bash scripts/run_gemea_transform.sh
#            Run from the goethe-faust project root, inside a tmux/screen session.
# Inputs:    /data/ddb/data/s{1..7}.sqlite
# Outputs:   $OUT_BASE/s{1..7}/   (per-sector .nq, .duckdb, -stats.json, -errors.jsonl, .log)
#            $OUT_BASE/merged.nq
#            $OUT_BASE/werk-staging-merged.duckdb
#            $OUT_BASE/nt/ddbedm.nt, mocho.nt, prov.nt
# Deps:      .venv/ created by scripts/setup_venv.sh (optional), duckdb via pip3 --user,
#            scripts/split_nq.py (stdlib only)
# Notes:     Sectors with >1 worker: export → split JSONL → N parallel transforms.
#            Sectors with 1 worker:  export → transform (no split).
#            cd into scripts/ before python3 -m transform so duckdb (user site-packages)
#            is visible without PYTHONPATH.

set -euo pipefail

# ── Paths ──────────────────────────────────────────────────────────────────────
GOETHE="$(cd "$(dirname "$0")/.." && pwd)"
SQLITE_DIR=/data/ddb/data
EXPORT_DIR=/data/ddb/gemea/json-export
SCRIPTS=$GOETHE/scripts
HASH=$(find "$SCRIPTS/transform" -name "*.py" | sort | xargs sha256sum | sha256sum | cut -c1-4)
VERSION="$(date '+%Y%m%d')-$(date '+%H')${HASH}"
OUT_BASE=/data/ddb/gemea/mocho-transform/$VERSION
# ──────────────────────────────────────────────────────────────────────────────

CFG=$GOETHE/output/config
PYTHON=$( [[ -x "$GOETHE/.venv/bin/python3" ]] && echo "$GOETHE/.venv/bin/python3" || echo python3 )

# Workers per sector — 128 total (50% of 256 cores on teach03)
# Distributed proportionally to record count so all sectors finish simultaneously.
declare -A WORKERS=([1]=17 [2]=86 [3]=1 [4]=6 [5]=8 [6]=9 [7]=1)

mkdir -p "$EXPORT_DIR" "$OUT_BASE"

echo "[$(date '+%F %T')] Starting GeMeA transform — 128 workers across 7 sectors"
echo "  GOETHE     = $GOETHE"
echo "  SQLITE_DIR = $SQLITE_DIR"
echo "  EXPORT_DIR = $EXPORT_DIR"
echo "  OUT_BASE   = $OUT_BASE"
echo "  Workers    = s1:${WORKERS[1]} s2:${WORKERS[2]} s3:${WORKERS[3]} s4:${WORKERS[4]}" \
     "s5:${WORKERS[5]} s6:${WORKERS[6]} s7:${WORKERS[7]}"

# ── Phase 1+2: export then transform (chunked where W>1) ──────────────────────
for n in 1 2 3 4 5 6 7; do
  W=${WORKERS[$n]}
  (
    mkdir -p "$OUT_BASE/s${n}"

    # Export full sector JSONL
    echo "[$(date '+%F %T')] [s${n}] export starting"
    cd "$SCRIPTS"
    "$PYTHON" -m transform.sqlite_export \
      --db  "$SQLITE_DIR/s${n}.sqlite" \
      --out "$EXPORT_DIR/s${n}.jsonl" \
      2>> "$OUT_BASE/s${n}/export.log"
    echo "[$(date '+%F %T')] [s${n}] export done"

    if [[ $W -eq 1 ]]; then
      # Single worker — transform directly
      TOTAL=$(wc -l < "$EXPORT_DIR/s${n}.jsonl")
      echo "[$(date '+%F %T')] [s${n}] transform starting (1 worker, ${TOTAL} records)"
      cd "$SCRIPTS"
      "$PYTHON" -m transform \
        --jsonl      "$EXPORT_DIR/s${n}.jsonl" \
        --outdir     "$OUT_BASE/s${n}" \
        --stats      dispatch \
        --total      "$TOTAL" \
        --alignment  "$CFG/lookup_class_prop_alignment.csv" \
        --lido       "$CFG/lido_event_types.csv" \
        --htype      "$CFG/lookup_htype_doco_rico.csv" \
        --mediatype  "$CFG/lookup_mediatype_class.csv" \
        --audio      "$CFG/audio_type2class.json"
    else
      # Multiple workers — split JSONL into W chunks then transform in parallel
      CHUNK_DIR="$EXPORT_DIR/s${n}_chunks"
      mkdir -p "$CHUNK_DIR"
      echo "[$(date '+%F %T')] [s${n}] splitting into ${W} chunks"
      split -n l/$W "$EXPORT_DIR/s${n}.jsonl" "$CHUNK_DIR/chunk_"

      echo "[$(date '+%F %T')] [s${n}] launching ${W} transform workers"
      for chunk in "$CHUNK_DIR"/chunk_*; do
        stem=$(basename "$chunk")
        TOTAL=$(wc -l < "$chunk")
        mkdir -p "$OUT_BASE/s${n}/$stem"
        (
          cd "$SCRIPTS"
          "$PYTHON" -m transform \
            --jsonl      "$chunk" \
            --outdir     "$OUT_BASE/s${n}/$stem" \
            --stats      dispatch \
            --total      "$TOTAL" \
            --alignment  "$CFG/lookup_class_prop_alignment.csv" \
            --lido       "$CFG/lido_event_types.csv" \
            --htype      "$CFG/lookup_htype_doco_rico.csv" \
            --mediatype  "$CFG/lookup_mediatype_class.csv" \
            --audio      "$CFG/audio_type2class.json"
        ) &
      done
      wait  # wait for all chunk workers of this sector
    fi

    echo "[$(date '+%F %T')] [s${n}] done"
  ) &
done

echo "[$(date '+%F %T')] All sector workers launched — waiting for completion..."
wait
echo "[$(date '+%F %T')] All sectors complete — merging"

# ── Phase 3: merge N-Quads ────────────────────────────────────────────────────
MERGED_NQ=$OUT_BASE/merged.nq
find "$OUT_BASE" -name "*.nq" | sort | xargs cat > "$MERGED_NQ"
NQ_LINES=$(wc -l < "$MERGED_NQ")
echo "[$(date '+%F %T')] N-Quads merged (${NQ_LINES} quads) → $MERGED_NQ"

# ── Phase 3: merge DuckDB werk_staging ───────────────────────────────────────
OUT_BASE="$OUT_BASE" "$PYTHON" <<'PYEOF'
import glob, os, sys
try:
    import duckdb
except ImportError:
    print("duckdb not available — skipping werk_staging merge")
    sys.exit(0)
out_base = os.environ["OUT_BASE"]
shards = sorted(glob.glob(f"{out_base}/**/*-werk-staging.duckdb", recursive=True))
if not shards:
    print("No werk_staging shards found — skipping DuckDB merge")
    sys.exit(0)
out = f"{out_base}/werk-staging-merged.duckdb"
conn = duckdb.connect(out)
conn.execute(f"CREATE TABLE werk_staging AS SELECT * FROM '{shards[0]}'")
for p in shards[1:]:
    conn.execute(f"INSERT OR REPLACE INTO werk_staging SELECT * FROM '{p}'")
rows = conn.execute("SELECT COUNT(*) FROM werk_staging").fetchone()[0]
conn.close()
print(f"werk_staging merged ({len(shards)} shards, {rows} rows) → {out}")
PYEOF

# ── Phase 4: split merged N-Quads into per-graph N-Triples ───────────────────
NT_DIR=$OUT_BASE/nt
echo "[$(date '+%F %T')] Splitting N-Quads into per-graph .nt files → $NT_DIR"
"$PYTHON" "$SCRIPTS/split_nq.py" "$MERGED_NQ" --out-dir "$NT_DIR"
echo "[$(date '+%F %T')] Split complete"

echo "[$(date '+%F %T')] Done. Output: $OUT_BASE"
