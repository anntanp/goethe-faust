# Transform dedup — `run_gemea_transform.sh` integration plan

**Date**: 2026-05-13
**Status**: Pending — context captured for a later session
**Relates to**: `scripts/run_gemea_transform.sh`, `scripts/transform/__main__.py`

## 1. Background

`__main__.py` gained an `--entities-db PATH` flag (2026-05-13, see `notes/transform-implementation-actual.md §11`) for cross-run shared-entity deduplication. It stores a `prov_entities` DuckDB table (`uri VARCHAR PRIMARY KEY, entity_type VARCHAR NOT NULL`) that prevents re-emitting identical descriptive triples for shared PROV-O nodes and `edm:Agent`/`Place`/`skos:Concept`/`edm:TimeSpan` entities across sector runs.

`run_gemea_transform.sh` does not yet pass `--entities-db` to any transform invocation.

## 2. Constraint: DuckDB single-writer

DuckDB allows only one writer at a time. The script runs all 7 sectors in parallel (background subshells, line 135) and within multi-worker sectors runs all chunk workers in parallel (line 129). A single shared `--entities-db` file cannot be written to concurrently — doing so will deadlock or raise "database is locked".

## 3. Plan

### 3.1 Add `ENTITIES_DB` path variable

Add near the other path variables (after line 41):

```bash
ENTITIES_DB=$OUT_BASE/entities.duckdb
```

### 3.2 Wipe entities DB on `--new`

Extend the `--new` wipe (line 55):

```bash
rm -rf "$OUT_BASE"/s{1..7} "$OUT_BASE/nt" \
       "$OUT_BASE/werk-staging-merged.duckdb" \
       "$OUT_BASE/entities.duckdb"
```

### 3.3 Single-worker sectors (s3, s7) — pass `--entities-db` directly

These sectors run one transform process (no concurrency). Add the flag to the single-worker invocation (lines 95–104):

```bash
"$PYTHON" -m transform \
  --jsonl      "$EXPORT_DIR/s${n}.jsonl" \
  --outdir     "$OUT_BASE/s${n}" \
  --stats      dispatch \
  --total      "$TOTAL" \
  --alignment  "$CFG/lookup_class_prop_alignment.csv" \
  --lido       "$CFG/lido_event_types.csv" \
  --htype      "$CFG/lookup_htype_doco_rico.csv" \
  --mediatype  "$CFG/lookup_mediatype_class.csv" \
  --audio      "$CFG/audio_type2class.json" \
  --entities-db "$ENTITIES_DB"
```

Safe because the single-worker sectors (s3 and s7) themselves still run in parallel with other sectors, but each only has one writer to `ENTITIES_DB` at a time. If s3 and s7 happen to write back simultaneously there is a race. To be safe, either:
- Accept the risk (both use `INSERT OR IGNORE`; worst case one write is retried or dropped — negligible for these small sectors), or
- Give each single-worker sector its own entities DB and merge them afterward (same pattern as `werk-staging-merged.duckdb`).

The simpler fix (accept the risk) is likely fine in practice given s3 and s7 are tiny sectors.

### 3.4 Multi-worker sectors (s1, s2, s4, s5, s6) — dedup at merge time with `sort -u`

Cannot share a DuckDB file across parallel chunk workers. Instead, replace the Phase 4 per-graph merge (lines 181–183) with a `sort -u` pipe:

```bash
for slug in "${!seen[@]}"; do
  find "$OUT_BASE" -name "*-${slug}.nt" ! -path "$NT_DIR/*" | sort | xargs cat \
    | sort -u > "$NT_DIR/${slug}.nt"
  echo "[$(date '+%F %T')] → $NT_DIR/${slug}.nt (deduped)"
done
```

`sort -u` on N-Triples is correct because each triple is a single line and identical triples are byte-identical. This achieves the same result as `--entities-db` for the multi-worker case with no concurrency constraint.

**Note on memory**: `sort -u` on `prov.nt` at 18M-record scale may be large. Use `LC_ALL=C sort -u` for speed; add `--buffer-size=2G` if needed on teach03.

### 3.5 Update script header comment

Update the `# Outputs:` line to document `entities.duckdb`:

```bash
# Outputs:   $OUT_BASE/s{1..7}/   (per-sector .nq, .duckdb, -stats.json, -errors.jsonl, .log)
#            $OUT_BASE/werk-staging-merged.duckdb
#            $OUT_BASE/entities.duckdb  (cross-run shared-entity dedup state; single-writer sectors only)
#            $OUT_BASE/nt/ddbedm.nt, mocho.nt, prov.nt  (deduped via sort -u)
```

## 4. Files to change

| File | Change |
|---|---|
| `scripts/run_gemea_transform.sh` | Add `ENTITIES_DB` var; extend `--new` wipe; add `--entities-db` to single-worker invocation; replace Phase 4 merge with `sort -u`; update header comment |

No changes needed to `scripts/transform/` — the `--entities-db` flag is already implemented.

## 5. Testing

After the change, run a two-sector subset and verify:
- `entities.duckdb` exists and contains rows after s3 or s7 completes
- `prov.nt` contains each PROV-O shared-node URI described exactly once (grep for `urn:ddbedm:dataset:`)
- Triple count in `prov.nt` is lower than without dedup (shared nodes not repeated per chunk)
