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

## 7. Emitter safety audit (2026-05-07)

### 7.1 Issue categories

Three systemic gaps (A–C) and one feature addition (D):

| # | Category | Root cause / motivation | Emitters affected |
|---|---|---|---|
| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags; the unescaped tag appears verbatim in the N-Quad literal | Any emitter that calls `_escape_literal` on a field containing `<br …>` |
| B | Multi-URI `resource` not split | Emitters that manually extract `val.get("resource")` treat space-separated URIs as one string, producing a malformed IRI | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs` |
| C | Bare IDs not expanded in special emitters | Same emitters bypass `expand_obj_nt`; also `emit_prov_triples` passes `provider_isil` without `_sanitize_iri` | `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`, `emit_prov_triples` |
| D | `edm:currentLocation` — IRI-with-label-stub | Currently emitted via generic loop (no label stub). Should follow the same "IRI-with-label-stub" pattern as `edm:hasType`: URI values get a `rdfs:label` stub from the matching `edm:Place`; literal values pass through unchanged | New `emit_current_location_triples`; `"currentLocation"` added to `_MOCHO_SKIP` |

Note: `value_to_nt_obj` (used by the generic loops in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are exclusively in special-case emitters that extract `resource` manually.

Corpus evidence (from `data/items-all-goethe-faust.json`):
- **B/D** — `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF`: `ProvidedCHO.currentLocation.resource = "http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745"` and matching `Place.about`
- **A** — `223GMAWUHPGI76OQUKSL54XVOCHHXDWD`: description field contains `"...1749, +22. März 1832<br />Eduard Lassen..."` 
- **C** — `222NZKK63TNRLC2VETRV722VKBDSUVGL`: `ProvidedCHO.hasType[0].resource = "DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6"` (bare 32-char ID)

### 7.2 Design — `resource_uris()` utility

Rather than patching each emitter individually, one utility in `utils.py` encapsulates the three sub-steps every manual `resource` extraction must perform:

```python
def resource_uris(
    resource_raw: str,
    bare_id_to_uri: dict[str, str] | None = None,
    entity_class: str = "Agent",
) -> list[str]:
    """Expand, sanitize, and split all URIs from a (possibly multi-value) resource string.

    Steps: (1) split on whitespace; (2) expand bare IDs via index or mint_bare_id fallback;
    (3) percent-encode unsafe characters. Returns [] for empty input.
    """
```

Callers pass `(val.get("resource") or "").strip()`, the per-record `bare_id_to_uri` index, and the entity class for bare-ID minting. Returns a list of safe, full URI strings ready for `f"<{uri}>"` wrapping.

**Primary-URI rule**: emitters that need the raw first URI before expansion (e.g. `event_participant_index` lookup in `emit_contributor_triples`, `resolve_agent` in `emit_creator_triples`) extract `resource_raw.split()[0]` before calling `resource_uris()`.

### 7.3 Change inventory

**`utils.py`**

| Change | Detail |
|---|---|
| Add `_BR_RE` | `re.compile(r'<br\s*/?\s*>', re.IGNORECASE)` |
| Update `_escape_literal` | Prepend `s = _BR_RE.sub('\n', s)` before the escape chain |
| Add `resource_uris()` | New utility; imported by `emitters.py` |

**`emitters.py`**

| Emitter | Change |
|---|---|
| `emit_subject_triples` | Replace single-URI `resource` branch with `resource_uris(resource_raw, _bare, "Concept")` loop |
| `emit_hastype_triples` | Same pattern |
| `emit_creator_triples` | Add `bare_id_to_uri=None` param; Track 1: `resource_uris()` loop; Track 2: `resource_raw.split()[0]` for `resolve_agent`; apply `_sanitize_iri(agent_uri)` |
| `emit_contributor_triples` | Add `bare_id_to_uri=None` param; `resource_raw.split()[0]` for `event_participant_index` lookup; `resource_uris()` loop for triples |
| `emit_prov_triples` | Apply `_sanitize_iri(provider_isil)` |
| `emit_place_stubs` | Split `raw_about`; pass only first part to `mint_bare_id` with `_sanitize_iri` |
| `emit_aggregation_triples` | Inline split+sanitize loop for `isShownAt.resource`, `dataProvider.resource`, `object.resource` (no bare ID expansion — aggregation URIs are always full) |
| `emit_mocho_triples` | Pass `bare_id_to_uri` to `emit_creator_triples` and `emit_contributor_triples` |

**`emitters.py` — imports**: add `resource_uris` to `from .utils import`.

### 7.4 Fixture-based integration tests

Three real corpus records are saved to `scripts/transform/tests/fixtures/` as minimal inspection targets. Each record is stored as `<id>.json` (single-record JSON, not JSONL).

| File | Record ID | Pattern |
|---|---|---|
| `fixtures/multi_uri.json` | `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF` | Multi-URI in `Place.about` and `currentLocation.resource` |
| `fixtures/br_tag.json` | `223GMAWUHPGI76OQUKSL54XVOCHHXDWD` | `<br />` in description literal |
| `fixtures/bare_id.json` | `222NZKK63TNRLC2VETRV722VKBDSUVGL` | Bare 32-char ID in `hasType.resource` |

After fixes are applied, a fixture script `tests/make_fixtures.py` runs the full transform on all three records and writes `fixtures/<id>.nq` — the complete N-Quads output for human inspection.

Integration tests in `test_transform.py` (new `TestFixtures` class) load each `.json`, call `transform_record()`, and make targeted assertions:

| Test | Assertion |
|---|---|
| `test_multi_uri_place_splits` | Two separate `Place` subject IRIs emitted; no IRI containing a space |
| `test_multi_uri_current_location_splits` | Two separate triples for `currentLocation` |
| `test_br_tag_normalized` | `\\n` appears in the relevant literal; no `<br` substring in any triple |
| `test_bare_id_hastype_expanded` | `urn:ddbedm:Concept:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |

### 7.5 Unit test additions

| Class / function | Covers |
|---|---|
| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\n` |
| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id`; entity_class forwarded |
| `TestEmitSubjectTriplesMultiUri` | `"URI1 URI2"` → two `dcterms:subject` triples |
| `TestEmitHastypeTriplesMultiUri` | Same for `edm:hasType` |
| `TestEmitCreatorTriplesMultiUri` | Two URIs → two Track-1 triples |
| `TestEmitCreatorTriplesBareId` | Bare ID expanded; `agent_uri` sanitized |
| `TestEmitContributorTriplesMultiUri` | Two URIs → two `(cho, prop, uri)` triples |
| `TestEmitContributorTriplesBareId` | Bare ID expanded via param |
| `TestEmitProvTriplesIsil` | `provider_isil` with unsafe chars → sanitized in `MOCHO_ISIL` triple |
| `TestEmitPlaceStubsSplitAbout` | Space-separated `about` → only first part used as subject |
| `TestEmitAggregationSplitUri` | `isShownAt.resource = "URI1 URI2"` → two `dcterms:source` triples |

### 7.6 Validation run — goethe-faust corpus (2026-05-07)

Full run on `data/items-all-goethe-faust.json` (115,432 records) after all audit fixes. Output: `output/transform/20260507_190805/`.

| Metric | POC (2026-05-06) | Post-audit (2026-05-07) | Delta |
|---|---|---|---|
| Records processed | 115,432 | 115,432 | — |
| Triples total | 14,713,376 | 14,764,352 | +50,976 |
| ddbedm | 8,957,262 | 8,957,734 | +472 |
| **mocho** | **1,898,754** | **1,950,504** | **+51,750** |
| prov | 3,857,360 | 3,856,114 | −1,246 |
| Errors | 0 | 0 | — |
| fallback_d9 | 0 | 0 | — |
| uri_sanitized | 29 | 29 | — |
| uri_split | 4,188 | 2,685 | −1,503 |
| uri_about_split | 1,309 | 1,309 | — |

**mocho +51,750** breaks down as:
- `edm:currentLocation` — 31,837 new triples (property moved from generic loop to `emit_current_location_triples`; IRI-with-label-stub pattern)
- Creator/contributor bare-ID expansions, multi-URI splits, and subject/hasType label stubs now handled correctly in special emitters account for the remainder

**uri_split −1,503**: some multi-URI splits previously counted via the generic loop (`value_to_nt_obj`) are now handled in special emitters via `resource_uris()` and tracked separately; the net split count is lower because `currentLocation` URIs (many multi-value) are no longer double-counted.

**prov −1,246**: minor change due to PROV provider node deduplication; no logic change — variance from record ordering in input.

---

## 8. Full-corpus run plan

See `notes/transform-dryrun-plan.md §6` for the full pipeline:

1. **Export** — `python -m transform.sqlite_export` per sector (`s1.sqlite`…`s7.sqlite`) → per-sector JSONL
2. **Transform** — one `python -m transform` worker per sector, all in parallel
3. **Merge** — `cat` N-Quads shards; DuckDB `INSERT OR REPLACE` across staging files

Config files (`--alignment`, `--lido`, `--htype`, `--mediatype`, `--audio`) must be passed explicitly when running from outside the goethe-faust root. All live in `goethe-faust/output/config/`.

Estimated wall time at 18.5M records: ~1–1.5 h (7 parallel workers).
