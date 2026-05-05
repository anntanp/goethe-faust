# Plan: Rewrite `transform_edm_to_mocho.py`

## §0 Context

The current script (~730 lines) emits a single N-Triples stream into one file with the wrong creator IRI (P30263 vs P30329), no mt007 guard, no date normalization, no LIDO contributor dispatch, no CHO URI minting, no PROV-O, no ddbedm passthrough, and no DuckDB work staging. All spec docs have been audited and are current. The rewrite encodes decisions D1–D27 from `transform-script-adr.md`, `transform-adr.md` D11/D15/D17, and the full property dispatch from `transform-props-mapping-plan.md`.

**Target output (POC mode):**
- `output/goethe-faust.nq` — combined N-Quads (all four named graphs)
- `output/goethe-faust-werk-staging.duckdb` — W-slot staging rows for `link_gnd_works.py`

---

## §1 Critical files

| File | Role |
|---|---|
| `scripts/transform_edm_to_mocho.py` | **Rewrite target** |
| `output/config/lookup_class_prop_alignment.csv` | `(target_class, edm_prop) → target_prop` — runtime dispatch |
| `output/config/lido_event_types.csv` | `lido_uri → {rdam_agent_prop, rdaw_agent_prop, …, dc_agent_fallback}` |
| `output/config/lookup_htype_doco_rico.csv` | htype_code → (rdf_type, rst_iris) — keep existing loader |
| `output/config/lookup_mediatype_class.csv` | (sparte, mediatype) → (use_htype, rdf_type_w, rdf_type_m) — new; drives fixed class layer in `retype_entities()` |
| `output/config/audio_type2class.json` | mt001 group dispatch |
| `output/alignment_ddbedm_mocho.csv` | general (entity_type, json_key) → rda_iri |
| `notes/transform-script-plan.md` | Full spec (§0–§10) |
| `notes/ddbedm-prov-o-plan.md` | PROV-O Layer 1 field mapping |

---

## §2 New constants

```python
GEMEA_BASE      = "https://gemea.ise.fiz-karlsruhe.de/mocho/"
# GEMEA_WORK_BASE: not defined here — Work URIs are minted by link_gnd_works.py only (D17)
GRAPH_DDBEDM    = "https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm"
GRAPH_MOCHO     = "https://gemea.ise.fiz-karlsruhe.de/graph/mocho"
GRAPH_PROV      = "https://gemea.ise.fiz-karlsruhe.de/graph/prov"
MT007_IRI       = "http://ddb.vocnet.org/medientyp/mt007"
DDB_ITEM_BASE   = "http://www.deutsche-digitale-bibliothek.de/item/"
DDB_BASE        = "http://www.deutsche-digitale-bibliothek.de"
DDB_API_BASE    = "https://api.deutsche-digitale-bibliothek.de/2/"
OWL_SAMEAS      = "http://www.w3.org/2002/07/owl#sameAs"
RDFS_LABEL      = "http://www.w3.org/2000/01/rdf-schema#label"
SKOS_PREF_LABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
SKOS_CONCEPT    = "http://www.w3.org/2004/02/skos/core#Concept"
FOAF_THUMBNAIL  = "http://xmlns.com/foaf/0.1/thumbnail"
EDM_DATA_PROVIDER = "http://www.europeana.eu/schemas/edm/dataProvider"
DCTERMS_SOURCE  = "http://purl.org/dc/terms/source"
# PROV-O
PROV_ENTITY     = "http://www.w3.org/ns/prov#Entity"
PROV_AGENT      = "http://www.w3.org/ns/prov#Agent"
PROV_SW_AGENT   = "http://www.w3.org/ns/prov#SoftwareAgent"
PROV_DERIVED    = "http://www.w3.org/ns/prov#wasDerivedFrom"
PROV_ATTRIBUTED = "http://www.w3.org/ns/prov#wasAttributedTo"
PROV_GEN_TIME   = "http://www.w3.org/ns/prov#generatedAtTime"
PROV_ON_BEHALF  = "http://www.w3.org/ns/prov#actedOnBehalfOf"
DCAT_DATASET    = "http://www.w3.org/ns/dcat#Dataset"
FOAF_ORG        = "http://xmlns.com/foaf/0.1/Organization"
FOAF_NAME       = "http://xmlns.com/foaf/0.1/name"
SCHEMA_URL      = "https://schema.org/url"
MOCHO_ISIL      = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#isil"
```

Remove: `CREATOR_IRI`, `CONTRIBUTOR_IRI` (D7/D8 fan-out whitelist — superseded by alignment CSV lookup and LIDO dispatch).

---

## §3 Prefix table for CURIE expansion

Used by `lido_event_types.csv` and `lookup_class_prop_alignment.csv`. Expand `_PREFIXES` dict (already partial in script):

```python
"rdam":     "http://rdaregistry.info/Elements/m/",
"rdaw":     "http://rdaregistry.info/Elements/w/",
"rdae":     "http://rdaregistry.info/Elements/e/",
"rdac":     "http://rdaregistry.info/Elements/c/",
"dc":       "http://purl.org/dc/elements/1.1/",
"dcterms":  "http://purl.org/dc/terms/",
"vra":      "http://purl.org/vra/",
"rico":     "http://www.ica.org/standards/RiC/ontology#",
"skos":     "http://www.w3.org/2004/02/skos/core#",
"owl":      "http://www.w3.org/2002/07/owl#",
"rdfs":     "http://www.w3.org/2000/01/rdf-schema#",
"foaf":     "http://xmlns.com/foaf/0.1/",
"edm":      "http://www.europeana.eu/schemas/edm/",
"mo":       "http://purl.org/ontology/mo/",
"aco":      "https://w3id.org/ac-ontology/aco#",
"ec":       "http://www.ebu.ch/metadata/ontologies/ebucoreplus#",
```

---

## §4 New loaders

### §4.1 `load_class_prop_alignment(path)` → `dict[(target_class_curie, edm_prop_curie), target_prop_iri]`
Reads `output/config/lookup_class_prop_alignment.csv` columns: `edm_class, target_class, wemi, edm_prop, target_prop`. Key: `(target_class_curie, edm_prop_curie)` — keep as CURIE. Value: `_expand_prefix(target_prop)`. Skip rows where `target_prop` is empty or `N/A`.

### §4.2 `load_lido_event_types(path)` → `dict[lido_uri_str, dict[col_name, expanded_iri]]`
Reads `output/config/lido_event_types.csv`. Key: `resource` column (full URI). Columns of interest: `rdam_agent_prop`, `rdaw_agent_prop`, `vra_image_agent_prop`, `vra_work_agent_prop`, `rico_agent_prop`, `dc_agent_fallback`. Expand CURIEs via `_expand_prefix()`.

### §4.3 `load_mediatype_class(path)` → `dict[(sparte_iri, mediatype_iri), row_dict]`
Reads `output/config/lookup_mediatype_class.csv`. Key: `(sparte, mediatype)` — full IRIs or `"any"`. Value: row dict with keys `use_htype` (bool), `rdf_type_w` (expanded IRI or `""`), `rdf_type_m` (expanded IRI or `""`). Expand CURIEs in `rdf_type_w`/`rdf_type_m` via `_expand_prefix()`. Lookup falls back to `("any", "any")` if exact key not found.

### §4.4 `load_audio_type2class(path)` → `dict[(sector_iri, dc_type_de), group_char]`
Reads `output/config/audio_type2class.json`. Maps `(sector, dc_type)` → group `"A"/"B"/"C"`. Group A → `mo:MusicalManifestation`, Groups B/C → `aco:AudioManifestation`.

---

## §5 New utility functions

### §5.1 `make_nq(s_nt, p_nt, o_nt, graph_iri)` → `str`
Returns one N-Quads line: `f"{s_nt} {p_nt} {o_nt} <{graph_iri}> ."`. Inputs are already N-T formatted strings (angle-bracketed IRIs or quoted literals).

### §5.2 `coerce_list(val)` → `list`
`None → []`, `dict → [dict]`, `list → list`.

### §5.3 `mint_cho_uri(obj_id)` → `str`
Returns `GEMEA_BASE + obj_id` (bare IRI, no angle brackets).

### §5.4 `mint_bare_id(entity_class, raw_id)` → `str`
D27: if `raw_id` starts with `http` or `urn`: return as-is. `ProvidedCHO` → `DDB_ITEM_BASE + raw_id`; others → `f"urn:ddbedm:{entity_class}:{raw_id}"`.

### §5.5 `normalize_date(s)` → `list[str]`
D17: 8-digit compact YYYYMMDD → `YYYY-MM-DD`; `begin/end` ISO interval → `[begin, end]`; else `[s]`.

### §5.6 `resolve_agent(label, resource, agents_index)` → `dict | None`
Agent index built once per record from `edm.RDF.Agent[]`: `{uri: agent_dict, prefLabel: agent_dict}`. URI match preferred; label match fallback.

### §5.7 `is_ddb_or_gnd(uri)` → `bool`
True if starts with `http://www.deutsche-digitale-bibliothek.de/organization/` or `http://d-nb.info/gnd/`.

---

## §6 Handler functions

All handlers return `list[str]` of N-Quad lines. Graph IRI passed as parameter.

### §6.1 `emit_ddbedm_triples(rdf, record, graph_iri)` — stream [1], D20

Verbatim passthrough: iterate `rdf.items()` → each entity (coerce to list) → each `(json_key, raw_val)` → `value_to_nt_obj()` → emit using `edm_iri_map[(entity_type, json_key)]` as predicate IRI. Subject: original `entity["about"]` URI (not minted). Also emit `rdf:type` from a fixed entity_type → EDM class IRI table. All records including mt007.

### §6.2 `emit_prov_triples(record, ddb_cho_uri, graph_iri)` — stream [4], D11/D12

Layer 1 Without-Activity. Six node types per `ddbedm-prov-o-plan.md §2`:

| Node | URI pattern | Source fields |
|---|---|---|
| CHO | `ddb:item/<item-id>` | `properties.item-id` |
| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `provider-info.provider-ddb-id` |
| DDB | `http://www.deutsche-digitale-bibliothek.de` | fixed |
| SourceRecord | `ddb-api:items/<id>/source/record` | `binaries.binary[]` (one block per entry) |

### §6.3 `emit_mocho_triples(...)` — stream [2] orchestrator

Calls in order:
1. `retype_entities()` with minted `cho_uri`
2. `owl:sameAs` triple linking `cho_uri → ddb_uri`
3. Iterate `ProvidedCHO` properties → class dispatch via `class_prop_align`; skip `aggregationEntity`, `hierarchyPosition`; call special handlers for `creator`, `contributor`, subject keys, `dcType`
4. `emit_aggregation_triples()` for `Aggregation` block
5. `emit_place_stubs()` for `Place[]`

### §6.4 `retype_entities()` — refactor of existing

Changes from current:
- Accept minted `cho_uri` as subject for all mocho triples (not original DDB URI)
- Add edm:Agent class dispatch: `Agent[].type.resource` → `gndo:DifferentiatedPerson → mocho:Agent`, `gndo:CorporateBody → mocho:CorporateBody`, `gndo:ConferenceOrEvent → gndo:ConferenceOrEvent`, `gndo:Family → mocho:Family`; default `mocho:Agent`
- All emit calls use `make_nq(..., GRAPH_MOCHO)` instead of plain N-Triples strings
- Return `(nt_lines, target_class, wemi)` so orchestrator knows which dispatch column to use for creator/contributor

### §6.5 `emit_subject_triples()` — update (D1 amended)

IRI path: emit `dcterms:subject <uri>` + concept stub `<uri> rdfs:label "label"@lang` (from in-record `Concept[].prefLabel[]`). Literal path: keep `dc:subject "string"`. Dedup as before.

### §6.6 `emit_creator_triples(cho_nt, creator_values, agents_index, target_class, class_prop_align, graph_iri)` — D2 / props-mapping §4

Two independent tracks per creator value (both always run):
- **Track 1** — class-specific predicate: look up `(target_class, "dc:creator")` in `class_prop_align` → emit IRI or literal
- **Track 2** — Agent URI: `resolve_agent()` → if `is_ddb_or_gnd(uri)`: emit `<cho> dcterms:creator <uri>` + stub `<uri> rdf:type mocho:Agent ; rdfs:label "..."`. Silent if no URI.

### §6.7 `emit_contributor_triples(cho_nt, contributor_values, event_participant_index, lido_dispatch, target_class, wemi, graph_iri)` — D3/D25, props-mapping §5

Build `event_participant_index = {agent_uri: lido_hastype_resource}` once per record from `Event[].P11_had_participant` × `Event[].hasType.resource`.

Column selection:
```python
prop_col = {
    ("M", "rdac:C10007"):         "rdam_agent_prop",
    ("M", "mocho:Manifestation"): "rdam_agent_prop",
    ("W", "rdac:C10001"):         "rdaw_agent_prop",
    ("M", "vra:Image"):           "vra_image_agent_prop",
    ("W", "vra:Work"):            "vra_work_agent_prop",
    ("", "rico:RecordSet"):       "rico_agent_prop",
    ("", "rico:Record"):          "rico_agent_prop",
    ("", "rico:RecordPart"):      "rico_agent_prop",
}.get((wemi, target_class), "dc_agent_fallback")
```

Fallback (no event, label-only, unknown LIDO type): `dc:contributor`.

### §6.8 `emit_aggregation_triples(agg, cho_nt, graph_iri)` — D23

From `edm.RDF.Aggregation`:
- `isShownAt.resource` → `<cho> dcterms:source <uri>`
- `dataProvider[].resource` (filter: starts with `…/organization/`) → `<cho> edm:dataProvider <uri>`
- `object[].resource` → `<cho> foaf:thumbnail <uri>`
- `aggregatedCHO.resource` → navigation only; no triple

### §6.9 `emit_place_stubs(places, graph_iri)` — D24

For each `Place[]`: emit `<place-uri> rdfs:label "..."@lang` from `prefLabel[]`.

### §6.10 `werk_staging_row(cho_uri, cho_entity, target_class)` → `dict | None` — D26

When W-slot class ∈ {`rdac:C10001`, `mo:MusicalWork`}: return staging dict with keys `ddb_obj_id`, `cho_uri`, `target_class`, `dc_title`, `dc_alternative`, `dc_created`, `creator_uris`, `creator_literals`. Else None.

---

## §7 Core transform restructure

### §7.1 `transform_record(record, ...)` → `tuple[dict[str, list[str]], dict|None]`

Returns `(streams, werk_row)` where `streams = {"ddbedm": [...], "mocho": [...], "prov": [...]}`.

```python
obj_id  = get_object_id(record)
# IDs filter check
rdf     = record["edm"]["RDF"]
cho     = rdf.get("ProvidedCHO") or {}
ddb_uri = mint_bare_id("ProvidedCHO", cho.get("about", ""))
cho_uri = mint_cho_uri(obj_id)

mediatype, sector = _extract_mediatype_sector(rdf.get("Concept"))
is_mt007 = (mediatype == MT007_IRI)

streams["ddbedm"] = emit_ddbedm_triples(rdf, record, GRAPH_DDBEDM)   # always
streams["prov"]   = emit_prov_triples(record, ddb_uri, GRAPH_PROV)    # always

if not is_mt007:
    streams["mocho"] = emit_mocho_triples(...)
    werk_row = werk_staging_row(cho_uri, cho, target_class)
```

---

## §8 CLI changes

**New flags:**
- `--out` — combined `.nq` output (default `output/goethe-faust.nq`); replaces `--out-nt` and `--out-jsonld`
- `--werk-staging` — DuckDB path (default `output/goethe-faust-werk-staging.duckdb`)
- `--stats LEVEL` — `none|basic|dispatch|full` (default `basic`)
- `--log-level` — `DEBUG|INFO|WARNING|ERROR` (default `INFO`)
- `--workers N` — process pool size (default `cpu_count()`)
- `--batch-size N` — records per batch (default `1000`)
- `--ids -` — read IDs from stdin

**Remove:** `--out-nt`, `--out-jsonld`; drop `nt_lines_to_jsonld_nodes()` and JSON-LD writer.

---

## §9 Output file structure (POC)

```
output/
  goethe-faust.nq                   ← all named graphs combined; graph IRI on every line
  goethe-faust-werk-staging.duckdb  ← work-level GND staging
  transform_stats.json
  transform_errors.jsonl            ← {id, exception, message, traceback} per caught error
  transform.log
```

## §9.1 DuckDB werk_staging table schema

```sql
CREATE TABLE werk_staging (
    ddb_obj_id       VARCHAR PRIMARY KEY,
    cho_uri          VARCHAR,
    target_class     VARCHAR,
    dc_title         VARCHAR,
    dc_alternative   VARCHAR[],
    dc_created       VARCHAR,
    creator_uris     VARCHAR[],
    creator_literals VARCHAR[]
);
```

Requires `pip install duckdb`; add to script deps header.

---

## §10 Implementation order

1. **Constants + prefix table** — §2 + §3
2. **Utilities** — §5: `make_nq`, `coerce_list`, `mint_cho_uri`, `mint_bare_id`, `normalize_date`, `resolve_agent`, `is_ddb_or_gnd`
3. **New loaders** — §4: `load_class_prop_alignment`, `load_lido_event_types`, `load_audio_type2class`
4. **ddbedm stream** — §6.1: `emit_ddbedm_triples`
5. **PROV-O stream** — §6.2: `emit_prov_triples`
6. **mocho stream handlers** — §6.4–§6.9: `retype_entities` refactor, updated `emit_subject_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs`
7. **mocho orchestrator** — §6.3: `emit_mocho_triples`
8. **`transform_record`** — §7.1: restructure to return `(streams, werk_row)`
9. **`main`** — §8: new flags, single `.nq` output, DuckDB insert, stats, error log
10. **Multiprocessing** — `ProcessPoolExecutor` + batch chunking + stats merge (last; single-process first)

---

## §11 Verification

```bash
# Run POC
python scripts/transform_edm_to_mocho.py \
  --jsonl data/items-all-goethe-faust.json \
  --ids data/ids-all-goethe-faust.txt \
  --out output/goethe-faust.nq \
  --werk-staging output/goethe-faust-werk-staging.duckdb \
  --stats full 2>output/transform.log

# Named graph distribution (expect 3+ graph IRIs)
awk '{print $4}' output/goethe-faust.nq | sort | uniq -c

# CHO URI minting + owl:sameAs (counts should match records_processed)
grep -c 'gemea.ise.fiz-karlsruhe.de/mocho/' output/goethe-faust.nq
grep -c 'owl#sameAs' output/goethe-faust.nq

# mt007: present in ddbedm, absent from mocho
OBJ=<a known mt007 obj_id>
grep -c "$OBJ.*graph/ddbedm" output/goethe-faust.nq   # > 0
grep -c "$OBJ.*graph/mocho"  output/goethe-faust.nq   # 0

# LIDO contributor dispatch (typed predicates present)
grep -c 'P30083\|P30081' output/goethe-faust.nq   # > 0

# Wrong creator IRI absent
grep -c 'P30263' output/goethe-faust.nq   # 0

# DuckDB staging row count
python -c "import duckdb; c=duckdb.connect('output/goethe-faust-werk-staging.duckdb'); print(c.execute('SELECT count(*) FROM werk_staging').fetchone())"

# Error log
wc -l output/transform_errors.jsonl
```

---

## §12 Testing and validation style

Three levels, each with a distinct role:

### §12.1 Unit tests — `scripts/tests/test_transform.py`

Test each handler function in isolation with a fixture JSON snippet → expected N-Quad lines. Use `pytest`. Cover happy path + key edge cases per function.

Priority targets:
- `retype_entities()` — one test per sector × mediatype stratum; mt007 guard; htype absent
- `emit_creator_triples()` — Track 1 and Track 2 run independently; URI present; label-only; no match
- `emit_contributor_triples()` — LIDO type matched; no event; label-only fallback → `dc:contributor`
- `normalize_date()` — compact YYYYMMDD, ISO interval split, passthrough
- `mint_bare_id()` — bare 32-char ID for ProvidedCHO; bare ID for other entity types; full URI passthrough

```python
def test_retype_sparte002_ht021():
    lines = retype_entities("sparte002", "mt003", "htype_021", None, cho_nt="<...>", graph_iri=GRAPH_MOCHO)
    classes = extract_rdf_types(lines)
    assert "rdac:C10001" in classes
    assert "rdac:C10007" in classes
```

### §12.2 Collect-don't-crash — in `transform_record()`

Never `assert` or `raise` mid-pipeline. Wrap each record in `try/except`; append to `transform_errors.jsonl` and continue. Check total count in `transform_stats.json` at the end.

```python
try:
    streams, werk_row = transform_record(record, ...)
except Exception as exc:
    errors.append({"id": obj_id, "issue": str(exc), "traceback": ...})
    continue
```

### §12.3 Output validation — `scripts/validate_output.py`

Separate read-only script. Runs after the transform; never imported by the transform. Checks `§11` items mechanically against the output `.nq` file:

- Every line is valid N-Quads (4 terms + ` .`)
- Named graph IRIs are in `{graph/ddbedm, graph/mocho, graph/prov}`
- mocho-graph CHO subjects match `https://gemea.ise.fiz-karlsruhe.de/mocho/<32-char-id>`
- `owl:sameAs` count == `records_processed` (from `transform_stats.json`)
- No `P30263` (wrong creator IRI)
- mt007 spot-check: given a known mt007 ID, confirm present in ddbedm, absent from mocho

Keep transformation fast and dumb; validate the output file after.

---

## §13 Design patterns

### §13.1 Table-driven dispatch

The lookup CSVs are the dispatch tables — logic lives in data, not code. Applies to both class dispatch (`sector × mediatype × htype → class`) and property mapping (`target_class × edm_prop → target_prop`). Adding or correcting a mapping means editing a CSV, not touching the script.

Already the core design: `lookup_htype_doco_rico.csv`, `lookup_class_prop_alignment.csv`, `lido_event_types.csv` are all instances of this pattern.

---

## §14 Coding style

Target audience: mid-level to senior programmers reading the script cold. Optimize for clarity first; micro-optimizations only where profiling shows a bottleneck.

### §14.1 Type hints — everywhere

All function signatures carry type hints. Use `type aliases` for recurring types:

```python
NQuad     = str          # one N-Quads line
NQList    = list[NQuad]  # return type of all emit_* handlers
AgentDict = dict[str, Any]
PropAlign = dict[tuple[str, str], str]  # (target_class, edm_prop) → target_prop_iri
```

```python
def emit_creator_triples(
    cho_nt: str,
    creator_values: list[dict],
    agents_index: dict[str, AgentDict],
    target_class: str,
    class_prop_align: PropAlign,
    graph_iri: str,
) -> NQList:
```

Return types make the pipeline contract explicit without reading the body.

### §14.2 Docstrings — one line on public functions

One sentence stating what the function returns or does, not how. Skip for private helpers (`_`-prefixed) where the name is self-explanatory.

```python
def emit_creator_triples(...) -> NQList:
    """Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2)."""
```

No parameter lists in docstrings — type hints already carry that. No multi-line blocks.

### §14.3 Guard clauses over nesting

Reject bad input at the top; keep the happy path unindented.

```python
# prefer
def mint_bare_id(entity_class: str, raw_id: str) -> str:
    if raw_id.startswith(("http", "urn")):
        return raw_id
    if entity_class == "ProvidedCHO":
        return DDB_ITEM_BASE + raw_id
    return f"urn:ddbedm:{entity_class}:{raw_id}"

# avoid
def mint_bare_id(entity_class: str, raw_id: str) -> str:
    if not raw_id.startswith(("http", "urn")):
        if entity_class == "ProvidedCHO":
            return DDB_ITEM_BASE + raw_id
        else:
            return f"urn:ddbedm:{entity_class}:{raw_id}"
    return raw_id
```

### §14.4 Named constants, not magic strings

All IRI strings, graph names, and controlled-vocab values live in `§2` constants. No bare strings inside handlers.

```python
# prefer
emit(cho_nt, OWL_SAMEAS, f"<{ddb_uri}>", GRAPH_MOCHO)

# avoid
emit(cho_nt, "http://www.w3.org/2002/07/owl#sameAs", f"<{ddb_uri}>", "https://gemea.ise.fiz-karlsruhe.de/graph/mocho")
```

### §14.5 Function size — one responsibility

Each `emit_*` handler does one thing. If a handler needs a sub-step with non-obvious logic, extract it into a `_`-prefixed helper rather than adding inline comments. Aim for functions readable in one screen (~40 lines).

### §14.6 Comments — only for non-obvious WHY

No comments explaining what the code does. Only add one when there is a hidden constraint, a surprising invariant, or a workaround for a known data quirk. Reference the ADR decision when the reason lives there.

```python
# Track 1 and Track 2 are independent — both run even when URI resolves (D2)
# 99.5% of dc:spatial URIs duplicate Event.happenedAt — no event traversal needed
```

### §13.2 Registry (dict of callables)

The main property loop in `emit_mocho_triples()` must branch for ~6 properties with special handling. An if/elif chain grows brittle as properties are added. Use a registry instead:

```python
SPECIAL_HANDLERS = {
    "creator":        emit_creator_triples,
    "contributor":    emit_contributor_triples,
    "dcSubject":      emit_subject_triples,
    "dcTermsSubject": emit_subject_triples,
    "dcTermSubject":  emit_subject_triples,
    "dcType":         emit_dctype_triples,
}

for prop, val in cho.items():
    handler = SPECIAL_HANDLERS.get(prop)
    if handler:
        lines += handler(cho_nt, val, ...)
    else:
        lines += emit_generic_triple(cho_nt, prop, val, class_prop_align, ...)
```

Adding a new special case = one entry in the registry + one new function. The generic path handles all remaining properties via `class_prop_align` lookup.

### §13.3 Pipeline

`transform_record()` calls independent stream emitters in sequence — `emit_ddbedm_triples`, `emit_mocho_triples`, `emit_prov_triples` — each returning a list of N-Quad lines. The four output streams are fully decoupled: mt007 guard applies only to mocho and werk_staging; ddbedm and prov always run. See `§7.1`.
