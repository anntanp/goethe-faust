#!/usr/bin/env bash
# Purpose:   Full GeMeA corpus transform — 7 sectors in parallel (Option C)
# Usage:     bash scripts/run_gemea_transform.sh
#            Run from the goethe-faust project root, inside a tmux/screen session.
# Inputs:    /data/ddb/data/s{1..7}.sqlite
# Outputs:   $OUT_BASE/s{1..7}/   (per-sector .nq, .duckdb, -stats.json, -errors.jsonl, .log)
#            $OUT_BASE/merged.nq
#            $OUT_BASE/werk-staging-merged.duckdb
#            $OUT_BASE/nt/ddbedm.nt, mocho.nt, prov.nt
# Deps:      python3 -m transform (PYTHONPATH=scripts/), duckdb Python package,
#            scripts/split_nq.py (stdlib only)
# Notes:     EXPORT_DIR needs ~400 GB free for uncompressed JSONL.
#            Each sector runs export then transform back-to-back in its own subshell.
#            All 7 subshells are launched in parallel; script waits for all to finish.

set -euo pipefail

# ── Paths (set before running) ─────────────────────────────────────────────────
GOETHE="$(cd "$(dirname "$0")/.." && pwd)"   # goethe-faust project root (auto-detected)
SQLITE_DIR=/data/ddb/data                    # s1.sqlite … s7.sqlite
EXPORT_DIR=/data/ddb/export                  # per-sector JSONL; needs ~400 GB free
OUT_BASE=/data/ddb/gemea      # s1/ … s7/ land here
# ──────────────────────────────────────────────────────────────────────────────

CFG=$GOETHE/output/config
SCRIPTS=$GOETHE/scripts

mkdir -p "$EXPORT_DIR" "$OUT_BASE"

echo "[$(date '+%F %T')] Starting full GeMeA transform — 7 sectors in parallel"
echo "  GOETHE     = $GOETHE"
echo "  SQLITE_DIR = $SQLITE_DIR"
echo "  EXPORT_DIR = $EXPORT_DIR"
echo "  OUT_BASE   = $OUT_BASE"

# ── Phase 1+2: export then transform, pipelined per sector ────────────────────
for n in 1 2 3 4 5 6 7; do
  (
    echo "[$(date '+%F %T')] [s${n}] export starting"
    PYTHONPATH="$SCRIPTS" python3 -m transform.sqlite_export \
      --db  "$SQLITE_DIR/s${n}.sqlite" \
      --out "$EXPORT_DIR/s${n}.jsonl"

    TOTAL=$(wc -l < "$EXPORT_DIR/s${n}.jsonl")
    echo "[$(date '+%F %T')] [s${n}] export done (${TOTAL} records) — transform starting"

    PYTHONPATH="$SCRIPTS" python3 -m transform \
      --jsonl      "$EXPORT_DIR/s${n}.jsonl" \
      --outdir     "$OUT_BASE/s${n}" \
      --stats      dispatch \
      --total      "$TOTAL" \
      --alignment  "$CFG/lookup_class_prop_alignment.csv" \
      --lido       "$CFG/lido_event_types.csv" \
      --htype      "$CFG/lookup_htype_doco_rico.csv" \
      --mediatype  "$CFG/lookup_mediatype_class.csv" \
      --audio      "$CFG/audio_type2class.json"

    echo "[$(date '+%F %T')] [s${n}] transform done"
  ) &
done

echo "[$(date '+%F %T')] All 7 sector workers launched — waiting for completion..."
wait
echo "[$(date '+%F %T')] All sectors complete — merging"

# ── Phase 3: merge N-Quads ────────────────────────────────────────────────────
MERGED_NQ=$OUT_BASE/merged.nq
cat "$OUT_BASE"/s*/*.nq > "$MERGED_NQ"
NQ_LINES=$(wc -l < "$MERGED_NQ")
echo "[$(date '+%F %T')] N-Quads merged (${NQ_LINES} quads) → $MERGED_NQ"

# ── Phase 3: merge DuckDB werk_staging ───────────────────────────────────────
OUT_BASE="$OUT_BASE" python33 <<'PYEOF'
import duckdb, glob, os, sys
out_base = os.environ["OUT_BASE"]
shards = sorted(glob.glob(f"{out_base}/s*/*-werk-staging.duckdb"))
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
python3 "$SCRIPTS/split_nq.py" "$MERGED_NQ" --out-dir "$NT_DIR"
echo "[$(date '+%F %T')] Split complete"

echo "[$(date '+%F %T')] Done. All output in: $OUT_BASE"
