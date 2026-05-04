# Transform implementation tracking

**Date**: 2026-05-04
**Status**: In progress — notes audit phase complete; ADR entries and script-plan update pending before implementation

---

## 1. Context

Pre-implementation audit of `transform-script-plan.md` and `transform-script-adr.md` against the current authoritative spec (`transform-revised-plan.md` + `transform-props-mapping-adr.md`). Several stale sections and missing decisions were identified. New architectural decisions (N-Quads output, CHO URI minting) were added to `transform-adr.md D15` and `transform-revised-plan.md §0` during this session.

---

## 2. Audit results

### 2.1 transform-script-plan.md — section verdicts

| Section | Verdict |
|---|---|
| §0 Pipeline overview | **STALE** — single output file; four-stream N-Quads architecture not reflected |
| §0.1 Debug mode | Current (spec correct; not yet implemented) |
| §1 Input | Current |
| §2.1–2.5 Class dispatch | Current |
| §3.1 Property mapping | Current |
| §3.2.1 Subject handler | Current |
| §3.2.2 Creator fan-out | Current (IRI superseded: P30263 → P30329 in props-mapping-adr.md D2) |
| §3.2.3 Contributor handler | **STALE** — "keep dc:contributor"; now requires LIDO event dispatch (props-mapping-adr.md D3) |
| §3.3 Lookup tables | Current |
| §4 Output [A] CHO triples | **STALE** — references single `goethe-faust-mocho.nt`; should be four N-Quad streams |
| §5 Concurrent [B] Provenance | **STALE** — wrong output filename; `prov_edm_to_mocho.py` not created |
| §6 Concurrent [C] GND linking | **STALE** — references Phase 1b `link_gnd_agents.py`; now Phase 0 Work-level GND table (`link_gnd_works.py`) |
| §7 Class mapping detail | Current |
| §8 gen_dctype_class_mapping.py spec | Current |
| §9 Verification checklist | **STALE** — assumes single-file output; references Phase 1b agent linking |

### 2.2 transform-script-adr.md — decision verdicts

| Decision | Status | Notes |
|---|---|---|
| D1 JSONL input | ✅ Current | |
| D2 stdlib-only | ✅ Current | Scoped to POC; D18 overrides for full corpus |
| D3 Dispatch signal paths | ✅ Current | |
| D4 PhysicalThing deferred | → Moved | Correctly moved to transform-adr.md D14 |
| D5 N-Triples output | ✅ Current | Superseded by D22 |
| D6–D8 Subject/creator/contributor | → Moved | Now props-mapping-adr.md D1–D3; D7 IRI corrected P30263 → P30329 |
| D9 mocho:Manifestation fallback | ✅ Current | |
| D10 PhysicalThing htype-only | ✅ Current | |
| D11 mt002 dc:type dispatch | ✅ Current | |
| D12 mt002 WebResource ImageObject | ✅ Current | |
| D13 sparte002 htype Work dispatch | ✅ Current | |
| D14 Manual curation philosophy | ✅ Current | |
| D15 mt007 skip | ❌ Not implemented | Logic absent from script |
| D16 mt001 audio dispatch | ✅ Current | |
| D17 dc:date normalization | ❌ Not implemented | `normalize_date()` absent from script |
| D18 Two-stage full-corpus pipeline | ✅ Current | Scope correct |
| D19 sqlite/bufgz input | ✅ Current | Scope correct |
| D20 Named graph naming | 🔴 Stale | Single `.nt`; revised-plan requires four N-Quad streams |
| D21 Debug mode | ❌ Not implemented | Future feature; low priority |
| D22–D26 | ❌ Missing | See §3 below |

### 2.3 lookup_class_prop_alignment.csv — gaps

| Entity type | Status |
|---|---|
| edm:Aggregation (rows 572–575) | ✅ Already present |
| edm:Place label stub (row 576) | ✅ Added this session |
| edm:Agent (rows 549–571) | ✅ Already present |
| edm:WebResource | Not needed (no entity-level triples in Phase 0) |
| edm:TimeSpan | Not needed (dates emitted on CHO) |

---

## 3. New ADR entries (D22–D26) to write

Content to append to `transform-script-adr.md` after D21.

**D22 — N-Quads output + mocho-graph CHO URI minting**
Cross-reference to `transform-adr.md D15`. Key points:
- Output: N-Quads (`.nq`); each line `<s> <p> <o> <graph> .`
- mocho CHO subject: `https://gemea.ise.fiz-karlsruhe.de/mocho/<object_id>` via `get_object_id()`
- `owl:sameAs` triple: minted URI → original DDB URI; in mocho graph
- Agent/Place/WebResource: retain original URIs

**D23 — Aggregation traversal**
Source: `transform-revised-plan.md §7.2`; rows 572–575 of `lookup_class_prop_alignment.csv`.
- `isShownAt.resource` → `<cho> dcterms:source <wr-uri>`
- `dataProvider[].resource` (starts with `http://www.deutsche-digitale-bibliothek.de/organization/`) → `<cho> edm:dataProvider <uri>`
- `object[].resource` → `<cho> foaf:thumbnail <uri>`
- `aggregatedCHO.resource` → navigation only; no triple
- `about`, `isShownBy`, `edmRights`, `provider`, `aggregator`, `hasView`: not emitted

**D24 — edm:Place label stub**
Source: `transform-revised-plan.md §4.2`; `lookup_class_prop_alignment.csv` row 576.
- `<place-uri> rdfs:label "..."@lang` from `edm.RDF.Place[].prefLabel[].@value` + `.@language`
- No rdf:type; no other Place triples in Phase 0

**D25 — LIDO contributor predicate dispatch**
Supersedes D8. Full decision: `transform-props-mapping-adr.md D3`. Traversal chain: `transform-revised-plan.md §3.2`.
- `ProvidedCHO.hasMet[].resource → edm:Event.about → edm:Event.hasType.resource → LIDO type → target predicate`
- Lookup: `output/config/lido_event_types.csv`
- Fallback: `dc:contributor`

**D26 — Work-level GND Werk staging output**
Source: `transform-revised-plan.md §1.2`.
- Triggered when W-slot class = `rdac:C10001` or `mo:MusicalWork`
- Staging row fields: `dc:title`, `dc:alternative[]`, `dc:created`, `dc:creator[].resource` (GND URIs), `dc:creator[].$` (`last, first`)
- Separate from N-Quads stream; consumed by `link_gnd_works.py`

---

## 4. Engineering requirements

### 4.1 Modularity

Each entity type handler is a standalone function (`emit_cho_triples`, `emit_agent_triples`, `emit_aggregation_triples`, `emit_place_stubs`, etc.) with no side effects beyond returning a list of N-Quad lines. The main `transform_record()` orchestrates them. Lookup tables are loaded once and passed in — no global state inside handlers. Adding a new entity type means adding one function and one call site, nothing else.

### 4.2 Stats toggles

Stats collection is opt-in via `--stats LEVEL` (default `basic`):

| Level | What is collected | Cost |
|---|---|---|
| `none` | No stats file written | Zero overhead |
| `basic` | records_processed, error_count, triples_out, skipped_count | Negligible |
| `dispatch` | + W/M-slot class counts, htype match/miss, dctype fallback, LIDO event type counts | Low |
| `full` | + per-sector/mediatype/htype counts, EDM class instance counts, ignored properties, Agent type distribution, Place label coverage, creator/contributor URI match rates | Moderate — adds per-record dict lookups |

`full` is for paper reporting runs; `basic` or `none` for production 27M runs where throughput matters. Stats are accumulated in worker processes and merged after all batches complete (no locking overhead during transform).

### 4.3 Parallelism

The transform is embarrassingly parallel at the record level. Target design:

- **Worker pool** (`multiprocessing.Pool` or `concurrent.futures.ProcessPoolExecutor`): each worker receives a batch of JSONL records + pre-loaded lookup tables (shared via initializer, not re-loaded per record).
- **Batch size**: tunable via `--batch-size` (default 1,000 records). Each batch produces a temporary `.nq` chunk; chunks are concatenated to the final output streams at the end.
- **Output**: four output file handles (one per named graph) written in order after all batches complete, or streamed per-batch to avoid holding all output in memory at 27M scale.
- Lookup tables (CSV dicts) are read-only after load — safe to share across processes via initializer.

### 4.4 Documentation

- Every function has a header docstring: purpose, inputs/outputs, ADR cite (e.g. `# ADR D23`), relevant note reference.
- Non-obvious logic (URI filter, LIDO traversal, date normalization) gets an inline comment citing the ADR decision number.
- Script header block lists all lookup table dependencies, output files, and decision references.

### 4.5 Logging and error collection

For a 27M-record run:

- **Structured logging** (`logging` module, configurable level via `--log-level`): one line per batch at INFO; per-record errors at WARNING/ERROR.
- **Exception log**: records that raise an exception are caught, logged with object ID + exception type + message, and written to `output/transform_errors.jsonl` (one JSON object per line: `{id, exception, message, traceback}`). Processing continues.
- **Stats file** (`output/transform_stats.json`): existing pattern extended with per-entity-type counts, error count, skipped count, batch count, elapsed time.
- **Progress**: `tqdm` or plain `print` to stderr every N batches (configurable).

### 4.6 Reprocessing specific IDs

- `--ids FILE` already exists in the current script (filters to a set of 32-char object IDs).
- Extend: `--ids` can also be a plain list of IDs on stdin (piped from error log). Example:
  ```
  jq -r '.id' output/transform_errors.jsonl | python transform_edm_to_mocho.py --ids -
  ```
- Reprocess writes to separate output files (e.g. `goethe-faust-mocho-reprocess.nq`) to avoid overwriting the main run; a `--merge` flag merges them into the primary output (replacing triples for those IDs by subject).
- Open question: deduplication on merge — see §6 Q6.

---

## 5. Task checklist

### 5.1 Notes / ADR updates (before implementation)

- [x] **`transform-script-adr.md`** — append D22–D26 (§3 above)
- [x] **`transform-script-plan.md §0`** — update pipeline overview: four N-Quad streams, named graph IRIs, ddbedm passthrough spec
- [x] **`transform-script-plan.md §3.2.3`** — LIDO event dispatch spec already present (was already current)
- [x] **`transform-script-plan.md §4`** — update output section: four-stream `.nq` files, minted CHO URI
- [x] **`transform-script-plan.md §5`** — update provenance section: cite `ddbedm-prov-o-plan.md`, Layer 1 + Layer 2
- [x] **`transform-script-plan.md §6`** — replace Phase 1b agent linking with Phase 0 Work-level GND table / `link_gnd_works.py`
- [x] **`transform-script-plan.md §9`** — rewrite verification checklist for four-stream output

### 5.2 Script implementation

**Output + architecture:**
- [ ] **`transform_edm_to_mocho.py`** — N-Quads: add graph IRI fourth element to every emit call; four output file handles (`mocho`, `ddbedm`, `work`, `prov`)
- [ ] **`transform_edm_to_mocho.py`** — CHO URI minting: `GEMEA_BASE = "https://gemea.ise.fiz-karlsruhe.de/mocho/"` + `get_object_id()`; emit `owl:sameAs` to original DDB URI in mocho graph
- [ ] **`transform_edm_to_mocho.py`** — multiprocessing: `ProcessPoolExecutor` with `--workers N` (default cpu_count); lookup tables shared via initializer; `--batch-size` tunable
- [ ] **`transform_edm_to_mocho.py`** — `--stats LEVEL` flag (`none`/`basic`/`dispatch`/`full`); per-worker accumulators merged post-batch
- [ ] **`transform_edm_to_mocho.py`** — structured logging + `transform_errors.jsonl` (one `{id, exception, message, traceback}` per caught exception)
- [ ] **`transform_edm_to_mocho.py`** — `--ids -` stdin support for reprocessing from error log

**ddbedm stream:**
- [ ] **`transform_edm_to_mocho.py`** — `emit_ddbedm_triples()`: verbatim passthrough of all `edm.RDF.*` fields as N-Quads into `graph/ddbedm`; all records including mt007; no predicate mapping — use raw EDM IRIs via `value_to_nt_obj()`

**mocho stream — new/corrected handlers:**
- [ ] **`transform_edm_to_mocho.py`** — remove `CREATOR_IRI` fan-out whitelist; route `dc:creator` through alignment CSV (Q4)
- [ ] **`transform_edm_to_mocho.py`** — mt007 guard: skip mocho/work emit only; still calls `emit_ddbedm_triples()` and `emit_prov_triples()` (Q3)
- [ ] **`transform_edm_to_mocho.py`** — edm:Agent class dispatch via `edm:Agent.type.resource` (Q7)
- [ ] **`transform_edm_to_mocho.py`** — Aggregation traversal: `emit_aggregation_triples()` — `dcterms:source`, `edm:dataProvider` (org URI filter), `foaf:thumbnail`
- [ ] **`transform_edm_to_mocho.py`** — Place label stubs: `emit_place_stubs()` — `rdfs:label` from `Place[].prefLabel`
- [ ] **`transform_edm_to_mocho.py`** — LIDO contributor dispatch: Event index + `lido_event_types.csv` lookup; replace hardcoded `CONTRIBUTOR_IRI`
- [ ] **`transform_edm_to_mocho.py`** — date normalization: `normalize_date()` per D17 (compact YYYYMMDD → ISO; range split on `/`)
- [ ] **`transform_edm_to_mocho.py`** — `emit_subject_triples()`: IRI path now emits concept stub `<uri> rdfs:label "label"@lang` in addition to `dcterms:subject <uri>`; literal path keeps `dc:subject "string"` (props-mapping-adr.md D1 amended)
- [ ] **`transform_edm_to_mocho.py`** — Concept stub for dcType URI path (§15): `<concept-uri> a skos:Concept ; skos:prefLabel "..."@lang`

**PROV-O stream** (spec: `ddbedm-prov-o-plan.md`):
- [ ] **`transform_edm_to_mocho.py`** — Layer 1 `emit_prov_triples()`: reads `properties.*`, `provider-info.*`, `source.*`, `binaries.binary[]`; emits CHO + Dataset + XSLT + Provider + DDB + SourceRecord nodes into `graph/prov` (transform-adr.md D11)
- **Layer 2** — **Future work; not implemented here.** Will extend PROV-O to LM-assisted enrichments and inter-script lineage. Spec: `ddbedm-prov-o-plan.md §3`.

**Work stream + staging:**
- [ ] **`transform_edm_to_mocho.py`** — Work-level DuckDB staging: insert row when W-slot class dispatched; fields per §3 D26
- [ ] **`scripts/README.md`** — update script header: new flags, outputs, decision references

---

## 6. Verification

### 6.0 Stats for ISWC 2026 paper

`transform_stats.json` must include the following counts. They directly feed paper TODOs in `30-resource.tex` and `40-quality.tex`.

**30-resource.tex — Scale paragraph** (currently `\todo{…}`):
- Total quad count (all four named graphs combined)
- ProvidedCHO count
- Named graph count (= 1 for POC single-file)
- Triples per named graph (mocho / ddbedm / work / prov breakdown)

**30-resource.tex — Object types and sectors table** (currently `\todo{…}`):
- Records per sector (`sparte001`–`sparte007`)
- Records per mediatype (`mt001`–`mt007`)
- Records per htype code (top-N htypes)
- EDM class instance counts: ProvidedCHO, Agent, Event, Place, TimeSpan, WebResource, Concept, Aggregation, PhysicalThing — sourced from iterating `edm.RDF.*` keys

**30-resource.tex — Mocho alignment PoC** (currently `\todo{…}`):
- W-slot class assigned count + breakdown by class
- M-slot class accumulated count + breakdown by class
- dc:type fallback count (no match → `mocho:Manifestation`)
- htype matched count vs. missing count
- Work-level staging rows written (W-slot records for GND Werk linking)

**40-quality.tex — Mapping quality**:
- `in_mocho=True` row count vs. `in_mocho=False` (direct vs. approximate match rate per entity type)
- Ignored properties count per entity type (properties with no alignment candidate — feeds "known limitations")
- Creator URI match rate (contributor URI resolved vs. label-only)
- LIDO contributor dispatch: count per event type (creation / publication / production / photography / designing / commissioning / fallback)
- Agent type distribution: `gndo:DifferentiatedPerson` / `gndo:CorporateBody` / `gndo:ConferenceOrEvent` / `gndo:Family` / unknown
- Place label stub coverage: Place URIs with at least one `rdfs:label` vs. total

**40-quality.tex — Completeness**:
- mt007 records: EDM triples emitted (ddbedm stream) vs. mocho triples skipped
- Error count + breakdown by exception type (from `transform_errors.jsonl`)

Stats collection is controlled by `--stats LEVEL` (§4.2). Paper reporting runs use `--stats full`; production runs use `--stats basic` or `--stats none`. All counts are accumulated per-worker and merged after all batches complete.

---

### 6.1 Run

```bash
python scripts/transform_edm_to_mocho.py \
  --jsonl data/items-all-goethe-faust.json \
  --ids data/ids-all-goethe-faust.txt \
  --out output/goethe-faust-mocho.nq \
  --werk-staging output/goethe-faust-werk-staging.duckdb \
  --log-level INFO 2>output/transform.log
```

Check `output/transform_errors.jsonl` is empty or review exceptions before proceeding.

### 6.2 Stats sanity

```bash
python -c "import json; s=json.load(open('output/transform_stats.json')); print(s)"
```

| Stat | Expected |
|---|---|
| `records_processed` | 115,432 (minus mt007 count for mocho stream) |
| `records_skipped_not_in_ids` | 0 (all IDs present) |
| `error_count` | 0 (or investigate) |
| `dctype_fallback` | Low — most records should match |

### 6.3 Named graph distribution

```bash
# Count quads per named graph
awk '{print $4}' output/goethe-faust-mocho.nq | sort | uniq -c
```

Expect four graph IRIs; `graph/mocho` should be the largest.

### 6.4 CHO URI minting + owl:sameAs

```bash
# Minted URIs present in mocho graph
grep 'gemea.ise.fiz-karlsruhe.de/mocho/' output/goethe-faust-mocho.nq | head -3

# owl:sameAs links to original DDB URIs
grep 'owl#sameAs' output/goethe-faust-mocho.nq | head -3
```

Count of `owl:sameAs` triples should equal `records_processed`.

### 6.5 Entity-type spot checks

```bash
# Aggregation: dcterms:source present
grep 'dcterms/terms/source' output/goethe-faust-mocho.nq | wc -l   # expect ~115K

# Aggregation: foaf:thumbnail present
grep 'foaf.*thumbnail\|thumbnail' output/goethe-faust-mocho.nq | wc -l

# Aggregation: edm:dataProvider (DDB org URIs only)
grep 'dataProvider' output/goethe-faust-mocho.nq | grep -v 'deutsche-digitale-bibliothek' | wc -l  # expect 0

# Place: rdfs:label stubs
grep 'rdf-schema#label' output/goethe-faust-mocho.nq | grep 'Place\|place' | head -3

# Agent: typed classes (not all mocho:Agent)
grep 'CorporateBody\|gndo.*ConferenceOrEvent\|mocho.*Family' output/goethe-faust-mocho.nq | wc -l

# Creator: rdam:P30329 present, P30263 absent
grep 'P30329' output/goethe-faust-mocho.nq | wc -l   # expect > 0
grep 'P30263' output/goethe-faust-mocho.nq | wc -l   # expect 0

# LIDO contributor dispatch: typed predicates present
grep 'P30083\|P30081\|P10051\|P10287' output/goethe-faust-mocho.nq | wc -l
```

### 6.6 mt007 handling

```bash
# mt007 records emit ddbedm triples but no mocho triples
# Pick a known mt007 object ID and check:
OBJ=<mt007-object-id>
grep "$OBJ" output/goethe-faust-mocho.nq | grep 'graph/ddbedm' | wc -l   # expect > 0
grep "$OBJ" output/goethe-faust-mocho.nq | grep 'graph/mocho' | wc -l     # expect 0
```

### 6.7 Work staging table

```python
import duckdb
con = duckdb.connect('output/goethe-faust-werk-staging.duckdb')
print(con.execute('SELECT count(*) FROM werk_staging').fetchone())  # expect ~W-slot record count
print(con.execute('SELECT * FROM werk_staging LIMIT 3').fetchdf())
```

---

## 7. Open questions

1. ✅ **D26 staging output format**: DuckDB table. `link_gnd_works.py` joins against it directly.

2. ✅ **Four-stream file naming**: Single `.nq` file for POC (`goethe-faust-mocho.nq`). Sector-aware filenames deferred to full-corpus stage.

3. ✅ **mt007 skip scope**: mt007 records **do** emit `edm.RDF.*` triples to the `ddbedm` named graph. No mocho/work/prov triples emitted for mt007.

4. ✅ **Creator IRI correction**: `lookup_class_prop_alignment.csv` row 28 already has `rdac:C10007 → rdam:P30329`; all other classes have class-specific predicates (`dcterms:creator`, `rdaw:P10065`, etc.). The script's hardcoded `CREATOR_IRI = rdam:P30263` (line 81, `transform_edm_to_mocho.py`) bypasses the CSV via fan-out whitelist and is **wrong**. Fix: remove the creator fan-out whitelist entry; route `dc:creator` through the alignment CSV like all other properties.

6. ⏸ **Reprocess merge deduplication**: deferred. `--ids` reprocessing writes to a separate output file; `--merge` not implemented in this pass.

7. ✅ **edm:Agent class dispatch**: implement now. Read `edm:Agent.type.resource` and emit type-specific `rdf:type` per revised-plan §2.1 dispatch table (`gndo:DifferentiatedPerson → mocho:Agent`, `gndo:CorporateBody → mocho:CorporateBody`, `gndo:ConferenceOrEvent → gndo:ConferenceOrEvent`, `gndo:Family → mocho:Family`). Default `mocho:Agent` when field absent.
