# Transform implementation — as-built

**Date**: 2026-05-06
**Status**: Implemented and verified on full goethe-faust corpus (115,432 records)
**Package**: `scripts/transform/` (invoked as `python -m transform` from `scripts/`)

Reference for the original design intent: `notes/transform-implementation-plan.md`.
Validation findings: `notes/transform-validation.md`.
Full-corpus run planning: `notes/transform-dryrun-plan.md`.

---

## 1. Package structure

The original plan targeted a monolithic rewrite of `scripts/transform_edm_to_mocho.py`. The actual implementation refactored into a Python package:

| Module | Contents |
|---|---|
| `constants.py` | IRIs, prefix table (`_PREFIXES`), dispatch tables, path defaults, type aliases |
| `utils.py` | N-Quads formatting, URI minting, IRI sanitisation, value normalisation |
| `loaders.py` | CSV/JSON config loaders |
| `emitters.py` | Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, werk_staging |
| `transform.py` | `transform_record` — per-record orchestration |
| `__main__.py` | CLI entry point |

---

## 2. Deviations from the plan

### 2.1 No in-process multiprocessing

The plan (§8) included `--workers N` and `--batch-size N` for a `ProcessPoolExecutor` approach. This was dropped in favour of **Option C parallel** (`transform-dryrun-plan.md §5.2`): export per-sector JSONL files from SQLite once, then run one `python -m transform` worker per sector as separate OS processes. No code changes required in the transform itself.

Rationale: per-UID SQLite random lookups are slower than sequential JSONL reads at 18.5M scale; sector split is the natural parallelism boundary; transform output is already sharded by sector. See `transform-dryrun-plan.md §5` for the full trade-off table.

### 2.2 CLI flags — additions and removals

**Planned but not implemented:**
- `--workers N`, `--batch-size N` — dropped (Option C)
- `--out` — output is always `<outdir>/goethe-faust.nq`; no free-choice path flag
- `--werk-staging` — DuckDB path is always `<outdir>/goethe-faust-werk-staging.duckdb`

**Added (not in plan):**
- `--total N` — expected total records; enables ETA in progress log
- `--log-interval N` — log a progress line every N records (default: 100,000)
- SIGINT/SIGTERM signal handler — graceful exit after current record; partial stats and errors written

**Output directory:** auto-timestamped `output/transform/YYYYMMDD_HHMMSS/` rather than fixed paths. Override with `--outdir`.

### 2.3 Stats expansion

The plan's `--stats` levels were implemented as designed. Additionally, during development the following were added at `dispatch` level (all from emitter Counters — no post-hoc N-Quad scanning):

- `records.by_mediatype` — mediatype distribution (short codes: `mt001`–`mt007`)
- `records.by_htype` — htype distribution (short codes: `ht021`, etc.)
- `records.uri_sanitized` — IRIs percent-encoded due to illegal characters (RFC 3987)
- `records.uri_split` — individual URIs extracted from multi-URI `resource` fields
- `records.uri_about_split` — extra `owl:sameAs` triples for multi-URI `about` fields
- `ddbedm_classes` — entity class instance counts in the ddbedm graph
- `ddbedm_vocab.properties_all` — predicate counts for the ddbedm stream
- `mocho_vocab.properties_all` / `properties_new` — predicate counts for the mocho stream

`full` level now aliases `dispatch` (reserved for future additions; the former regex-based predicate extraction was removed).

Schema and field rationale: `notes/transform-stats-plan.md`.

### 2.4 URI sanitisation and multi-URI data quality fixes

Not in the original plan. Added to `utils.py`:

**`_sanitize_iri(iri)`** — percent-encodes characters illegal in N-Triples IRI references (`[\x00-\x20<>"{}|\\^\x7f]`). Ported from `gemea/scripts/py/export_ddb.py`. Applied inside `value_to_nt_obj` for every `{"resource": ...}` value.

**Multi-URI `resource` fields** — 1,250 fields in the goethe-faust corpus contain multiple space-separated URIs in a single `resource` value (e.g. `"http://www.geonames.org/2856883 http://vocab.getty.edu/tgn/7005252"`). `value_to_nt_obj` splits on whitespace and emits each URI as a separate triple.

**Multi-URI `about` fields** — 1,178 entities (`Place`, `WebResource`, `Agent`) have multiple space-separated URIs in `about`. `emit_ddbedm_triples` uses the first URI as the RDF subject and emits `owl:sameAs` for each additional URI (+1,309 triples in the goethe-faust corpus).

---

## 3. Actual CLI

Run from `scripts/` directory:

```bash
python -m transform [OPTIONS]
```

### I/O

| Flag | Default | Description |
|---|---|---|
| `--jsonl FILE` | `data/items-all-goethe-faust.json` | JSONL input (one DDB-EDM JSON object per line) |
| `--ids FILE\|-` | _(none)_ | ID allowlist file, or `-` for stdin; omit to process all |
| `--outdir DIR` | `output/transform/YYYYMMDD_HHMMSS` | Output directory; auto-timestamped if omitted |

### Config

| Flag | Default |
|---|---|
| `--alignment FILE` | `output/config/lookup_class_prop_alignment.csv` |
| `--lido FILE` | `output/config/lido_event_types.csv` |
| `--htype FILE` | `output/config/lookup_htype_doco_rico.csv` |
| `--mediatype FILE` | `output/config/lookup_mediatype_class.csv` |
| `--audio FILE` | `output/config/audio_type2class.json` |

### Run control

| Flag | Default | Description |
|---|---|---|
| `--stats none\|basic\|dispatch\|full` | `basic` | Stats verbosity in `transform_stats.json` |
| `--log-level DEBUG\|INFO\|WARNING\|ERROR` | `INFO` | Log verbosity |
| `--limit N` | _(none)_ | Stop after N records (smoke-testing) |
| `--total N` | _(none)_ | Expected total records — enables ETA in progress log |
| `--log-interval N` | `100000` | Progress log line every N records |
| `--debug` | — | Shorthand for `--log-level DEBUG` |

---

## 4. Output files

Each invocation creates a timestamped run directory. All output filenames are derived
from the input filename stem so that parallel sector runs in a shared directory are
unambiguous (e.g. `s2.jsonl` → `s2.nq`, `s2-stats.json`, …):

```
output/transform/YYYYMMDD_HHMMSS/
  <stem>.nq                   N-Quads, all named graphs
  <stem>-werk-staging.duckdb  W-slot staging rows
  <stem>-stats.json           run statistics
  <stem>-errors.jsonl         per-record errors (written live)
  <stem>.log                  run log
```

For the full GeMeA parallel run with `--outdir output/transform/gemea/s${n}`:
```
output/transform/gemea/
  s1/s1.nq  s1/s1-stats.json  s1/s1-errors.jsonl  s1/s1.log  ...
  s2/s2.nq  s2/s2-stats.json  s2/s2-errors.jsonl  s2/s2.log  ...
  ...
```

Named graphs:

| Graph IRI | Content |
|---|---|
| `https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm` | Verbatim EDM passthrough (always, including mt007) |
| `https://gemea.ise.fiz-karlsruhe.de/graph/mocho` | mocho-aligned triples (skipped for mt007) |
| `https://gemea.ise.fiz-karlsruhe.de/graph/prov` | PROV-O Layer 1 (always) |

---

## 5. POC run — goethe-faust reference corpus (2026-05-06)

| Metric | Value |
|---|---|
| Records processed | 115,432 |
| Triples total | 14,713,376 |
| ddbedm / mocho / prov | 8,957,262 / 1,898,754 / 3,857,360 |
| werk_staging rows | 15 (`rdac:C10001` only) |
| Errors (parse + transform) | 0 |
| fallback_d9 | 0 |
| uri_split | 4,188 |
| uri_about_split | 1,309 |
| uri_sanitized | 29 |

Dispatch sum check: 25,644 (htype) + 47,428 (mediatype) + 0 (fallback) + 42,360 (mt007) = 115,432 ✓

---

## 6. Open issues from validation

From `notes/transform-validation.md`:

### 6.1 `mocho:ImageWork` missing from werk_staging

`_W_SLOT_CLASSES` triggers on `rdac:C10001` and `mo:MusicalWork` only. `transform-revised-plan.md §1.1` marks `mocho:ImageWork` as a GND-Werk target (ht015 Illustration, ht019 Karte, sparte005 mt002). No `mocho:ImageWork` records in the goethe-faust corpus, so no current impact. **Fix before running on a broader corpus.**

### 6.2 `ec:EditorialWork` werk_staging scope

Adding `ec:EditorialWork` would produce 88 additional staging rows (mt005 Video). `transform-revised-plan.md §1.1` has no "GND Werk" column entry for mt005/EditorialWork. Video productions do not have GND Werk authority records. Left out intentionally; revisit when GND linking scope is finalised.

---

## 7. Full-corpus run plan

See `notes/transform-dryrun-plan.md §6` for the full pipeline:

1. **Export** — `python -m transform.sqlite_export` per sector (`s1.sqlite`…`s7.sqlite`) → per-sector JSONL
2. **Transform** — one `python -m transform` worker per sector, all in parallel
3. **Merge** — `cat` N-Quads shards; DuckDB `INSERT OR REPLACE` across staging files

Config files (`--alignment`, `--lido`, `--htype`, `--mediatype`, `--audio`) must be passed explicitly when running from outside the goethe-faust root. All live in `goethe-faust/output/config/`.

Estimated wall time at 18.5M records: ~1–1.5 h (7 parallel workers).
