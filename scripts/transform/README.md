# scripts/transform/

Reference transform for the mocho ingest pipeline, using the goethe-faust corpus
(115,432 DDB records). Converts DDB-EDM JSONL to mocho-aligned N-Quads and a
DuckDB werk_staging table for GND Werk linking.

---

## transform_edm_to_mocho.py

### Pipeline

```
data/items-all-goethe-faust.json      JSONL input
data/ids-all-goethe-faust.txt         ID allowlist (optional)
output/config/*.csv / *.json          dispatch + alignment tables
          │
          ▼
  transform_edm_to_mocho.py
          │
          └── output/transform/YYYYMMDD_HHMMSS/
                  goethe-faust.nq                  N-Quads (all named graphs)
                  goethe-faust-werk-staging.duckdb  DuckDB werk_staging table
                  transform_stats.json              run statistics
                  transform_errors.jsonl            per-record errors
                  transform.log                     run log
```

Each invocation creates a new timestamped run directory. Use `--outdir` to set
an explicit path instead.

### Named graphs

| Graph IRI | Content |
|---|---|
| `https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm` | Verbatim EDM passthrough |
| `https://gemea.ise.fiz-karlsruhe.de/graph/mocho` | mocho-aligned triples (class dispatch, property alignment, agents, places) |
| `https://gemea.ise.fiz-karlsruhe.de/graph/prov` | PROV-O Layer 1 provenance chain |

`werk_staging` rows are written to DuckDB, not to the N-Quads file.

### Inputs

| File | Description |
|---|---|
| `data/items-all-goethe-faust.json` | DDB-EDM JSONL; one JSON object per line |
| `data/ids-all-goethe-faust.txt` | 32-char DDB object IDs; passed via `--ids` to filter JSONL |
| `output/config/lookup_mediatype_class.csv` | `(sector, mediatype)` → class dispatch |
| `output/config/lookup_htype_doco_rico.csv` | `htype_code` → rdf:type IRIs (§1.1) |
| `output/config/lookup_class_prop_alignment.csv` | `(target_class, edm_prop)` → mocho property |
| `output/config/lido_event_types.csv` | LIDO event URI → agent predicates per WEMI level |
| `output/config/audio_type2class.json` | `dc:type` → audio group (A/B/C) for mt001 dispatch |

### CLI arguments

Run `python scripts/transform/transform_edm_to_mocho.py --help` for the full argument list.
Full descriptions, defaults, and examples: [`notes/transform-cli-spec.md`](../../notes/transform-cli-spec.md).

Quick reference:

| Group | Key arguments |
|---|---|
| Input / output | `--jsonl`, `--ids`, `--outdir` |
| Lookup tables | `--alignment`, `--lido`, `--htype`, `--mediatype`, `--audio` |
| Stats | `--stats none\|basic\|dispatch\|full` (default: `basic`) |
| Logging | `--log-level`, `--debug` |
| Development | `--limit N` |

**Stats recommendation**: `--stats dispatch` for full-corpus runs; `--stats full --limit 50000`
when vocabulary coverage data is needed. See [`notes/transform-stats-plan.md`](../../notes/transform-stats-plan.md)
for the schema and performance trade-offs.

### Usage

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
```

### Tests

```bash
python -m pytest scripts/transform/tests/ -q
```

42 unit tests covering loaders, class dispatch (§1.1), N-Quad formatting, PROV node
construction, creator/contributor dispatch, and the D9 fallback. Uses actual config
CSVs — no mocking.

---

**Key references**:
- `notes/transform-adr.md` — transform decisions D1–D12
- `notes/transform-script-adr.md` — implementation decisions D13–D27
- `notes/transform-revised-plan.md` — §1.1 class dispatch table
- `notes/transform-stats-plan.md` — stats schema and resource paper guidance
