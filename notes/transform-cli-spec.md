# transform_edm_to_mocho.py — CLI specification

**Script**: `scripts/transform/transform_edm_to_mocho.py`
**Usage**: `python scripts/transform/transform_edm_to_mocho.py [OPTIONS]`

---

## 1. Input / output

| Argument | Default | Description |
|---|---|---|
| `--jsonl FILE` | `data/items-all-goethe-faust.json` | JSONL input file — one DDB-EDM JSON object per line |
| `--ids FILE` | _(none — all records)_ | ID allowlist file (one 32-char DDB ID per line), or `-` to read from stdin; omit to process all records |
| `--outdir DIR` | `output/transform/YYYYMMDD_HHMMSS` | Output directory; auto-timestamped if omitted |

Each invocation writes a self-contained run directory:

```
output/transform/YYYYMMDD_HHMMSS/
    goethe-faust.nq                   N-Quads (ddbedm + mocho + prov named graphs)
    goethe-faust-werk-staging.duckdb  DuckDB werk_staging table (W-slot records only)
    transform_stats.json              Run statistics (see §4)
    transform_errors.jsonl            Per-record errors
    transform.log                     Full run log
```

---

## 2. Lookup tables (override defaults)

All lookup tables have sensible defaults pointing into `output/config/`. Override only when testing alternative dispatch configurations.

| Argument | Default | Content |
|---|---|---|
| `--alignment FILE` | `output/config/lookup_class_prop_alignment.csv` | `(target_class, edm_prop)` → mocho property alignment |
| `--lido FILE` | `output/config/lido_event_types.csv` | LIDO event URI → agent predicates per WEMI level |
| `--htype FILE` | `output/config/lookup_htype_doco_rico.csv` | `htype_code` → `rdf:type` IRIs for §1.1 htype-first dispatch |
| `--mediatype FILE` | `output/config/lookup_mediatype_class.csv` | `(sector, mediatype)` → WEMI class IRIs for §1.1 mediatype dispatch |
| `--audio FILE` | `output/config/audio_type2class.json` | `dc:type` value → audio group (A/B/C) for mt001 class dispatch |

---

## 3. Logging

| Argument | Default | Description |
|---|---|---|
| `--log-level LEVEL` | `INFO` | Console and file log verbosity: `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `--debug` | off | Enable DEBUG logging — shorthand for `--log-level DEBUG` |

Logs are written to `transform.log` in the run directory; console output mirrors the log.

---

## 4. Stats

| Argument | Default | Description |
|---|---|---|
| `--stats LEVEL` | `basic` | Stats verbosity written to `transform_stats.json` |

See [`notes/transform-stats-plan.md`](transform-stats-plan.md) for the full schema, field rationale, and resource paper guidance.

| Level | Sections written | Extra cost at 27 M records |
|---|---|---|
| `none` | nothing | 0 |
| `basic` | `run`, `records`, `triples`, `werk_staging` | ~0 |
| `dispatch` | basic + `dispatch` (WEMI class counts) | ~0 |
| `full` | dispatch + `mocho_vocab` (per-predicate counts) | minutes — use on samples only |

**Recommendation**: `--stats dispatch` for full-corpus runs; `--stats full --limit 50000` when vocabulary coverage data is needed.

The bottleneck at `full` is a per-triple predicate regex over the mocho stream. At 27 M records × ~50 mocho triples ≈ 1.35 B regex matches.

---

## 5. Development

| Argument | Default | Description |
|---|---|---|
| `--limit N` | _(none)_ | Stop after N records — for smoke-testing and sampling |

---

## 6. Examples

```bash
# full corpus, default stats (basic)
python scripts/transform/transform_edm_to_mocho.py

# full corpus, dispatch stats (recommended for production)
python scripts/transform/transform_edm_to_mocho.py --stats dispatch

# first 500 records, debug logging
python scripts/transform/transform_edm_to_mocho.py --limit 500 --debug

# vocabulary coverage sample (full stats on 50k records)
python scripts/transform/transform_edm_to_mocho.py --limit 50000 --stats full

# explicit output directory (no timestamp)
python scripts/transform/transform_edm_to_mocho.py --outdir output/transform/dev

# custom ID filter
python scripts/transform/transform_edm_to_mocho.py --ids data/ids-sample.txt

# pipe IDs from stdin
cat ids.txt | python scripts/transform/transform_edm_to_mocho.py --ids -
```

---

## 7. Cross-references

- `notes/transform-stats-plan.md` — stats schema, field rationale, resource paper guidance
- `notes/transform-adr.md` — transform decisions D1–D12
- `notes/transform-script-adr.md` — implementation decisions D13–D27
- `notes/transform-revised-plan.md` — §1.1 class dispatch table
- `scripts/transform/README.md` — pipeline overview and test instructions
