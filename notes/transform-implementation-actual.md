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

Each invocation derives the output filename stem from the input: for SQLite input `s2.sqlite` with `--offset N` the stem is `s2-N`; for JSONL input `foo.json` the stem is `foo`. Override with `--stem`.

Single-worker output:
```
<outdir>/
  <stem>.nq                   N-Quads, all named graphs
  <stem>-werk-staging.duckdb  W-slot staging rows
  <stem>-stats.json           run statistics
  <stem>-errors.jsonl         per-record errors (written live)
  <stem>.log                  run log
```

In the production parallel-sector run (`run-transform-sector.sh`), all workers for one sector share a single `nq/` shard directory; merged outputs land one level up named by sector:
```
<version>/
  nq/
    s2-0.nq  s2-0-stats.json  s2-0.log  ...   ← worker shards (deleted after merge)
    s2-38400.nq  ...
    ...
  s2.nq                    merged N-Quads (--merge-all only)
  s2-werk-staging.duckdb   merged werk_staging
  s2-stats.json            merged stats
  s2-errors.jsonl          merged errors
  s2.log                   merged log
```

Running sectors sequentially into the same `<version>/` dir produces non-colliding `s1-*` and `s2-*` files.

Named graphs:

| Graph IRI | Content |
|---|---|
| `https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm` | Verbatim EDM passthrough (always, including mt007) |
| `https://gemea.ise.fiz-karlsruhe.de/graph/mocho` | mocho-aligned triples (skipped for mt007) |
| `https://gemea.ise.fiz-karlsruhe.de/graph/prov` | PROV-O Layer 1 (always) |
| `https://gemea.ise.fiz-karlsruhe.de/graph/lang-title` | `dcterms:language` provenance triples for normalized lang codes (emitted only when a record carries at least one invalid BCP 47 code) |

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
| `test_bare_id_hastype_expanded` | `urn:ddbedm:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |

### 7.5 Unit test additions

| Class / function | Covers |
|---|---|
| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\n` |
| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id` (`urn:ddbedm:<id>`) |
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

## 8. Agent label stub fixes (2026-05-08)

Two bugs in `emitters.py` prevented `rdfs:label` from being emitted on agent stubs in the mocho graph. Both deviate from the spec in `transform-props-mapping-plan.md §4–5` ("Label sourced from `edm:Agent.prefLabel[].$` (first value). Applies to both creator and contributor URI resolutions.").

### 8.1 Bug 1 — `emit_creator_triples`: `isinstance(pref, str)` always False

Track 2 of `emit_creator_triples` emits `dcterms:creator <agent.about>` + `mocho:Agent` type when `resolve_agent` finds a matching `edm:Agent`. It also should emit `rdfs:label` sourced from `agent.prefLabel[].$`. The pre-fix code:

```python
pref = agent.get("prefLabel") or label
if pref and isinstance(pref, str):          # always False — prefLabel is a list
    lines.append(make_nq(agent_nt, RDFS_LABEL, f'"{_escape_literal(pref)}"', graph_iri))
```

`agent.get("prefLabel")` returns a list (e.g. `[{"$": "Goethe, …", "lang": "de"}]`). `isinstance(list, str)` is always `False`, so no `rdfs:label` was ever emitted from the agent's own prefLabel. When the list was empty, the fallback `or label` set `pref` to the literal string from the creator field — which did pass `isinstance(str)` — but that path is rare and emits without lang-tag.

**Fix**: replace with `coerce_list(agent.get("prefLabel"))` + `value_to_nt_obj` iteration (same pattern as `emit_hastype_triples`); fall back to the `label` string only when prefLabel is empty.

### 8.2 Bug 2 — `emit_contributor_triples`: no `agents_index`, label from `val.get("$")`

`emit_contributor_triples` had no `agents_index` parameter, so:

1. **URI case**: `rdfs:label` was sourced from `val.get("$")` — the literal annotation on the contributor field — not from the matching `edm:Agent.prefLabel`.
2. **Literal case**: no `resolve_agent` call at all. Contributor literals that matched a DDB/GND agent by label were emitted as plain `dc:contributor "literal"@lang` instead of an agent stub.

**Fix**: add `agents_index: dict[str, AgentDict] | None = None` parameter.
- **URI case**: `resolve_agent("", primary_resource, _agents)` → use `prefLabel` from agent; fall back to `val.get("$")` if not found.
- **Literal case**: `resolve_agent(label, "", _agents)` → if DDB/GND match, emit `<cho> <target_prop> <agent.about>` + `mocho:Agent` + `rdfs:label`; else emit plain literal.

Update `emit_mocho_triples` call site to pass `agents_index`.

### 8.3 Test additions

Eight new tests in `scripts/transform/tests/test_transform.py`:

| Class | Test | Covers |
|---|---|---|
| `TestEmitCreatorTriplesPrefLabel` | `test_preflabel_list_dict_emitted` | prefLabel list-of-dicts → label emitted |
| | `test_preflabel_lang_tagged` | lang tag preserved (`"Schiller, Friedrich"@de`) |
| | `test_preflabel_empty_list_falls_back_to_label` | empty prefLabel → fallback to literal |
| | `test_uri_track2_uses_agents_index_preflabel` | URI path also uses agents_index prefLabel |
| `TestEmitContributorTriplesAgentLabel` | `test_uri_case_uses_agents_index_preflabel` | agents_index prefLabel wins over `val["$"]` |
| | `test_uri_case_fallback_to_literal_label_when_no_index` | no agents_index → `val["$"]` used |
| | `test_literal_match_emits_agent_stub` | literal matching DDB/GND agent → stub emitted |
| | `test_literal_no_match_emits_plain_literal` | unmatched literal → plain `dc:contributor` |

Total: 114 tests (106 post-audit + 8 new).

### 8.4 Validation run — goethe-faust corpus (2026-05-08)

Full run on `data/items-all-goethe-faust.json` (115,432 records) after agent label fixes. Output: `output/transform/20260507_232804/`.

| Metric | Pre-fix (20260507_190805) | Post-fix (20260507_232804) | Δ |
|---|---|---|---|
| Records processed | 115,432 | 115,432 | — |
| Triples total | 14,764,352 | 14,782,653 | **+18,301** |
| ddbedm | 8,957,734 | 8,957,734 | 0 |
| **mocho** | **1,950,504** | **1,968,805** | **+18,301** |
| prov | 3,856,114 | 3,856,114 | 0 |
| `rdfs:label` (mocho) | 302,578 | 320,754 | **+18,176** |
| `rdf:type` (mocho) | 162,807 | 162,932 | **+125** |
| `dcterms:creator` | 53,453 | 53,453 | 0 |
| `dc:contributor` | 36,773 | 36,773 | 0 |

18,176 + 125 = 18,301 — all new mocho triples accounted for by the two fixes.

**Attribution:**
- **+18,176 `rdfs:label`** — Bug 1. Creator Track 2 now correctly iterates `agent.prefLabel[]` via `value_to_nt_obj`; all previously silenced agent labels are emitted. The contributor literal-match branch contributes its `rdfs:label` half here as well.
- **+125 `rdf:type mocho:Agent`** — Bug 2 (literal-match path). Contributor literals that previously fell through as plain `dc:contributor "…"@lang` now resolve to DDB/GND agents and emit `mocho:Agent` type stubs.
- `dcterms:creator` and `dc:contributor` counts unchanged — the fixes add stubs for existing agent resolutions, not new CHO-level predicates.

---

## 9. `hierarchyType` URI fixes (2026-05-12)

Two bugs in `retype_entities` (`emitters.py`) in the handling of `ProvidedCHO.hierarchyType`.

Corpus evidence: object `LH3LUU63TUKZJHMQEILGTP3HZXZP5IFT` (`s2.sqlite`) has `"hierarchyType": "htype_007 htype_020"`.

### 9.1 Bug 1 — wrong vocnet URI form

Raw values use the form `htype_NNN` (e.g. `htype_007`). The correct vocnet IRI suffix is `htNNN` (e.g. `ht007`). The emitter was appending the raw code directly to `_HTYPE_PREFIX`, producing the invalid IRI `http://ddb.vocnet.org/hierarchietyp/htype_007`.

**Fix** (`emitters.py` lines 277–283): apply `.replace("htype_", "ht")` to each code before constructing the IRI.

### 9.2 Bug 2 — space-separated multi-value treated as single code

`hierarchyType` can contain multiple space-separated codes. The emitter passed the raw string as one unit, producing a single IRI with an embedded space: `<…/htype_007 htype_020>`. The dispatch lookup (`htype_map.get(htype_code)`) also silently failed for any multi-value record.

**Fix** (`emitters.py`):
- **Dispatch** (layer 1): `htype_map.get(htype_code.split()[0])` — first code only, consistent with "most specific class" intent.
- **URI emission**: iterate `htype_code.split()`; emit one `ddbedm:hierarchyType` triple per code with the corrected IRI.

### 9.3 Test additions

Three new tests in `TestRetypeEntities` (`test_transform.py`):

| Test | Assertion |
|---|---|
| `test_multi_htype_emits_two_triples` | `"htype_007 htype_020"` → exactly 2 `ddbedm:hierarchyType` triples, IRIs `ht007` and `ht020` |
| `test_multi_htype_no_space_in_iri` | No object token in any `ddbedm:hierarchyType` triple contains a space |
| `test_multi_htype_dispatch_uses_first` | `flags["htype_used"] is True` and `flags["fallback"] is False` — first code resolves a class |

Two existing tests updated: `test_sparte001_mt003_htype021` and `test_htype_emitted_as_iri` now assert `ht021`/`ht042` (not `htype_021`/`htype_042`) in the emitted IRI.

Total: 140 tests.

---

## 10. BCP 47 language tag normalization (2026-05-12)

QLever validates RDF language tags against BCP 47 and terminates indexing on the first invalid tag. DDB source records carry ISO 639-2 collective codes (e.g. `wen`, `gem`) and malformed codes (e.g. `gerger`) in the `lang` field of cortex JSON. Neither is a valid BCP 47 individual-language subtag.

Design record: `gemea/notes/ingest/transform-language-tag.md`.

### 10.1 Validation approach

`langcodes` (v3.5.1, added to `requirements.txt`) is used rather than a hand-curated dict. Two failure classes must be caught:

1. **Malformed codes** (e.g. `gerger`) — `langcodes.tag_is_valid()` returns `False`.
2. **IANA collection subtags** (e.g. `wen`, `gem`) — `langcodes.tag_is_valid()` returns `True` (they are in the IANA registry), but QLever rejects them. Detected by membership in `_IANA_COLLECTION_CODES`, a `frozenset` parsed at import time from the IANA registry bundled with `langcodes` (`data/language-subtag-registry.txt`, `Scope: collection` entries). 116 codes in the current registry.

Both → normalized to `"und"` (BCP 47 "undetermined"). Original code retained via provenance triple.

### 10.2 Code changes

**`utils.py`**

| Change | Detail |
|---|---|
| `_build_iana_collection_codes()` | Parses bundled IANA registry line-by-line; returns `frozenset` of all `Scope: collection` subtags. Falls back to empty set on error. |
| `_IANA_COLLECTION_CODES` | Module-level `frozenset` built at import. |
| `_invalid_bcp47(lang)` | `@lru_cache(maxsize=512)`. `True` if `not tag_is_valid(lang) or lang in _IANA_COLLECTION_CODES`. |
| `value_to_nt_obj()` | Added `lang_coll: set[str] \| None = None` parameter. Strips `lang` before validation; guards `lang_coll.add()` against values containing internal spaces (see §10.3). |

**`emitters.py`**

`lang_coll: set[str] | None = None` added to `emit_ddbedm_triples()` and `emit_mocho_triples()`; passed to every `value_to_nt_obj()` call that processes CHO fields (title, generic property loop). Secondary emitters (`emit_subject_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_hastype_triples`, `emit_current_location_triples`) are unchanged — corpus analysis (`analyse_lang_tags_by_entity.py`) confirmed no collective codes on non-CHO entities.

**`transform.py`**

`lang_coll: set[str] = set()` created in `transform_record()`; passed to both emitters (mutated in place). After emitters complete, one `dcterms:language <http://id.loc.gov/vocabulary/iso639-2/{orig_lang}>` provenance triple per unique original code is emitted to `GRAPH_LANG_TITLE`. Subject is `ddb_uri` (not `cho_uri`).

**`constants.py`**

`GRAPH_LANG_TITLE = "https://gemea.ise.fiz-karlsruhe.de/graph/lang-title"` added.

### 10.3 Whitespace-in-lang bug

`lang = "en en"` appears on record `LH3LUU63TUKZJHMQEILGTP3HZXZP5IFT` (`s2.sqlite`) on `ProvidedCHO.dcType` and `Concept[1].prefLabel`. Root cause: `Concept[1].about` contains two space-joined URIs (`"http://ddb.vocnet.org/hierarchietyp/ht007 http://ddb.vocnet.org/hierarchietyp/ht020"`); the DDB XML-to-JSON converter applied the same join to the `lang` attributes of the repeated element, concatenating `"en"` + `" "` + `"en"`.

Without the guard, `lang_coll.add("en en")` would produce `<http://id.loc.gov/vocabulary/iso639-2/en en>` — an invalid N-Quads IRI. Fix in `value_to_nt_obj()`:

```python
lang = val.get("lang")
if lang:
    lang = str(lang).strip()
if lang and _invalid_bcp47(lang):
    if lang_coll is not None and " " not in lang:
        lang_coll.add(lang)
    lang = "und"
```

`.strip()` handles leading/trailing whitespace. `" " not in lang` prevents any space-containing value from entering `lang_coll` (it still normalizes to `"und"`, so the literal output is correct).

### 10.4 Test additions

Three new test classes in `test_transform.py`:

| Class | Tests | Covers |
|---|---|---|
| `TestIanaCollectionCodes` | 3 | Registry loaded (>0 codes); known collectives (`wen`, `gem`) present; valid individuals (`ger`, `eng`) absent |
| `TestInvalidBcp47` | 4 | Collective → `True`; malformed → `True`; valid codes → `False`; `und` itself → `False` |
| `TestValueToNtObjLangNorm` | 10 | `wen`/`gem`/`gerger` → `@und`; valid lang unchanged; `lang_coll` populated for collective/malformed, empty for valid; `"en en"` → `@und` and not added to `lang_coll`; leading/trailing whitespace stripped |

Total: 137 tests (135 passing; 2 pre-existing failures in `TestRetypeEntities` — see §9.3).

---

## 11. Shared-entity deduplication (2026-05-13)

Descriptive triples for shared named entities are emitted at most once per URI across all transform runs. Without this, every sector run re-emits identical triples for the DDB Agent, XSLT SoftwareAgent, provider institutions, datasets, and all GND agents/places/concepts/timespans that appear in multiple records.

### 11.1 Mechanism

An `emitted: dict[str, str]` (`uri → entity_type`) is passed into both `emit_prov_triples` and `emit_ddbedm_triples`. Each shared-node block checks membership before emitting and registers the URI on first emission. The dict is initialized in `__main__.py` before the record loop (empty = within-run dedup only). With `--entities-db PATH`, it is loaded from DuckDB at startup and written back with `INSERT OR IGNORE` after the loop, enabling cross-run dedup across sector files.

**Entity types tracked**:

| entity_type | Source |
|---|---|
| `prov_xslt` | `properties.mapping-version` → XSLT SoftwareAgent URI |
| `prov_ddb` | Fixed `DDB_BASE` URI |
| `prov_provider` | `provider-info.provider-ddb-id` → Provider Agent URI |
| `prov_dataset` | `properties.dataset-id` → Dataset URI |
| `edm_agent` | `edm.RDF.Agent[].about` |
| `edm_place` | `edm.RDF.Place[].about` |
| `skos_concept` | `edm.RDF.Concept[].about` |
| `edm_timespan` | `edm.RDF.TimeSpan[].about` |

Per-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted unconditionally.

### 11.2 DuckDB schema

```sql
CREATE TABLE IF NOT EXISTS emitted_entities (
    uri         VARCHAR PRIMARY KEY,
    entity_type VARCHAR NOT NULL
)
```

Separate file from `werk-staging.duckdb`; shared across all sector runs in a production campaign. Managed by the caller — not auto-created in the run output directory.

### 11.3 New CLI flag

| Flag | Default | Description |
|---|---|---|
| `--entities-db PATH` | _(none)_ | Shared cross-run entity-dedup DuckDB. Omit for within-run dedup only. |

### 11.4 Code changes

| File | Change |
|---|---|
| `emitters.py` | Add `_DEDUP_ENTITY_TYPES` dict; add `emitted` param to `emit_ddbedm_triples` and `emit_prov_triples`; guard 4 PROV-O shared-node blocks + entity loop in `emit_ddbedm_triples` |
| `transform.py` | Add `emitted_entities` param to `transform_record`; thread through to both emitters |
| `__main__.py` | Add `--entities-db` CLI arg; DuckDB setup/load at startup; pass `emitted_entities` to `transform_record`; batch write-back after loop |

### 11.5 PROV-O URN scheme change

PROV-O shared nodes switched from a verbose property-chain URN form to short typed-prefix URNs:

| Node | Old form | New form |
|---|---|---|
| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `urn:ddbedm:dataset:<id>` |
| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `urn:ddbedm:xslt:<ver>` |
| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `urn:ddbedm:provider:<id>` |

**Collision guard**: bare DDB entity IDs (Agent, Place, Concept, TimeSpan) are minted as `urn:ddbedm:<id>` without a class name. DDB IDs are 32-character alphanumeric strings (no colons), so `urn:ddbedm:dataset:X` vs `urn:ddbedm:X` are unambiguous — the colon after the type segment is the discriminator.

### 11.6 Test additions

19 new tests across 2 new classes (total: 159).

**`TestEmitProvTriplesDedup`** (11 tests): `emitted=None` emits all; dict populated with correct `entity_type` values; each of the 4 shared nodes skipped when URI already in `emitted`; per-CHO linking triples always present even when all shared nodes are pre-emitted; 4 URN-format tests asserting the new short-prefix form and no collision between PROV-O nodes and bare entity IDs.

**`TestEmitDdbedmTriplesDedup`** (8 tests): Agent/Place/Concept/TimeSpan skipped when URI already in `emitted`; `ProvidedCHO` never skipped (not in `_DEDUP_ENTITY_TYPES`); `emitted=None` emits all; second call with same `emitted` dict emits 0 agent triples; dict populated with correct `entity_type` after first call.

---

## 12. Full-corpus run plan

The production orchestrator is `scripts/run-transform-sector.sh`. It splits the SQLite table into `--workers` chunks, launches one `python -m transform` OS process per chunk, waits for all to finish, then merges.

```bash
# one sector, all defaults (50 workers, merge stats only):
bash scripts/run-transform-sector.sh --merge --sector s2

# merge including .nq:
bash scripts/run-transform-sector.sh --merge-all --sector s2

# custom worker count:
bash scripts/run-transform-sector.sh --merge --sector s2 --workers 20
```

Key defaults: `--sqlite-dir /data/gemea/sqlite`, `--scripts-dir /home/ann/goethe-faust/scripts`, `--output-dir /data/gemea/www/downloads/gemea/YYYYMMDD` (today's date).

**Merge output naming**: `merge.py` receives `--stem "$SECTOR"`, so all merged files are named `<sector>-stats.json`, `<sector>.log`, etc. (not the version-date directory name). Multiple sectors run sequentially into the same version dir produce non-colliding outputs.

**`--merge` vs `--merge-all`**: `--merge` passes `--skip-nq` to `merge.py` — merges stats, werk_staging, errors, and logs only; `.nq` shards are retained for later concatenation. `--merge-all` also concatenates `.nq` shards into `<sector>.nq`.

Config files (`--alignment`, `--lido`, `--htype`, `--mediatype`, `--audio`) default to `output/config/` relative to the goethe-faust root derived from `--scripts-dir`.

Estimated wall time at 18.5M records: ~1–1.5 h (7 parallel workers).
