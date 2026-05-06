# Plan: `transform_edm_to_mocho.py` — Pipeline Sequence

**Date**: 2026-05-02
**Status**: In progress
**Related**: `transform-adr.md`, `transform-script-adr.md`, `transform-props-mapping-adr.md`, `transform-props-mapping-plan.md`, `transform-revised-plan.md`

---

## 0. Pipeline overview

Two input modes: POC uses `data/items-all-goethe-faust.json` (JSONL); full corpus reads `s2.sqlite` (`objs` table, `bufgz` column — gzip-compressed cortex JSON). In both cases the pipeline writes to four named-graph output streams.

```
s2.sqlite  (table: objs, columns: id, bufgz, …)        ← full corpus
      │  ← filter by list of DDB object IDs (optional)
      │
      ▼  decompress bufgz → cortex JSON
      │
      ├── [1] edm.RDF → raw EDM triples ────────────────────────→ <sector>-ddbedm.nq
      │       Priority #1. Faithfully round-trips the EDM payload.   graph/ddbedm
      │       Baseline for provenance and future re-alignment.
      │
      ├── [2] edm.RDF alignment → mocho triples ────────────────→ <sector>-mocho.nq
      │       Step 2a: class dispatch (§1.1 transform-revised-plan.md)  graph/mocho
      │       Step 2b: property mapping (transform-props-mapping-plan.md)
      │       CHO subject: https://gemea.ise.fiz-karlsruhe.de/mocho/<object_id> (script-adr D22)
      │
      ├── [3] Work-level GND staging ─────────────────────────────→ <sector>-werk-staging.duckdb
      │       W-slot records only; consumed by link_gnd_works.py      (Phase 0)
      │       Not an N-Quads stream; DuckDB table (§1.2, D26)
      │
      └── [4] Provenance triples ──────────────────────────────────→ <sector>-prov.nq
              PROV-O Layer 1 per ddbedm-prov-o-plan.md                  graph/prov
```

Named graph base: `https://gemea.ise.fiz-karlsruhe.de/`

Output filename conventions differ by run mode:
- **POC** (`items-all-goethe-faust.json`): all N-Quads streams combined into one file (`goethe-faust.nq`); graph IRI on every line distinguishes the streams. QLever loads the single file and handles multiple named graphs natively.
- **Full corpus** (`s2.sqlite`, per sector): one file per stream per sector — `<sector>-<stream>.nq` / `.duckdb` — so each sector can be loaded or re-run independently.

| Stream | Named graph IRI | POC output | Full corpus output | Script |
|---|---|---|---|---|
| [1] ddbedm | `…/graph/ddbedm` | `goethe-faust.nq` (combined) | `<sector>-ddbedm.nq` | `transform_edm_to_mocho.py` |
| [2] mocho | `…/graph/mocho` | `goethe-faust.nq` (combined) | `<sector>-mocho.nq` | `transform_edm_to_mocho.py` |
| [3] work (staging) | — (DuckDB) | `goethe-faust-werk-staging.duckdb` | `<sector>-werk-staging.duckdb` | `transform_edm_to_mocho.py` → `link_gnd_works.py` |
| [4] prov | `…/graph/prov` | `goethe-faust.nq` (combined) | `<sector>-prov.nq` | `transform_edm_to_mocho.py` |

Named graph IRIs use base `https://gemea.ise.fiz-karlsruhe.de/graph/<name>` (`transform-script-adr.md` D20). The `urn:ddbedm:` URN scheme is for bare-ID entity minting only (`transform-script-adr.md` D27).

mt007 (NOT DIGITIZED) records are **skipped** in streams [2] and [3] only — no mocho or work triples emitted (`transform-script-adr.md` D15). Streams [1] and [4] still process mt007 records: raw EDM triples (faithfulness) and provenance triples (pipeline audit trail).

**POC**: `data/items-all-goethe-faust.json` (JSONL, 115,432 records) for rapid iteration. JSONL and sqlite/bufgz carry identical cortex JSON structure; field paths in §1 apply to both. D1 governs the JSONL pass; D19 governs the `s2.sqlite` pass.

### 0.1 Debug mode

When `--debug` is set, after the main run also produce:

1. **Parquet snapshot**: all cortex JSON fields (pre-transform) written to `debug/<sector>-raw.parquet` for DuckDB inspection.
2. **100-record sqlite sample**: 100 randomly sampled records extracted to `debug/<sector>-sample-100.sqlite` (same schema as source DB).
3. **Per-record named files** (for the 100 sampled records only):
   - `debug/<graphname>-<ddb-object-id>.nt` — N-Triples for each output stream (per-graph, no graph column needed)
   - `debug/<graphname>-<ddb-object-id>.ttl` — Turtle (human-readable)
   - `debug/<ddb-object-id>.jsonld` — JSON-LD for the mocho graph only

`<ddb-object-id>`: the DDB item identifier (e.g. `224BB273RJDT6WN7GAIRV4AJ5ES5YPC5`). `<graphname>`: one of `ddbedm`, `mocho`, `prov`. (Debug output for the Werk staging / GND linking component is handled separately by `link_gnd_works.py`.) See D21.

### 0.2 Post-processing: NQ split → per-graph NT

After the transform, `scripts/split_nq.py` splits each `.nq` output into one `.nt` file per named graph. The `.nt` files are the working intermediates for sanitization, validation, and manual inspection. NQ wrapping (adding the graph IRI as the fourth element) is deferred to QLever load time.

| Transform output | Post-processing → | Working intermediates |
|---|---|---|
| `<sector>-ddbedm.nq` | `split_nq.py` | `ddbedm.nt` |
| `<sector>-mocho.nq` | `split_nq.py` | `mocho.nt` |
| `<sector>-prov.nq` | `split_nq.py` | `prov.nt` |

Graph IRI is derived mechanically from the slug at load time: `…/graph/<slug>`. Rationale: `transform-script-adr.md` D28.

---

## 1. Input

| Mode | File | Format | Records | Path |
|---|---|---|---|---|
| POC | `items-all-goethe-faust.json` | JSONL (one JSON object per line) | 115,432 | `data/items-all-goethe-faust.json` |
| Full corpus | `s2.sqlite` | sqlite (`objs` table; `bufgz` column = gzip-compressed cortex JSON) | ~27M | — |

In both modes the cortex JSON structure is identical. The sector is inferred from `provider-info.domains[0]` in JSONL mode and known from the DB at query time in sqlite mode. Key fields consumed:

| Field | JSONL path | Used by |
|---|---|---|
| item IRI | `edm.RDF.ProvidedCHO.about` | subject IRI of all CHO triples |
| sector | `provider-info.domains[0]` | class dispatch |
| mediatype | `edm.RDF.WebResource[0].type.resource` | class dispatch |
| htype | `edm.RDF.ProvidedCHO.hierarchyType` | class dispatch (Step 1a) |
| dc:type | `edm.RDF.ProvidedCHO.dcType.$` | class dispatch (Step 1b) |
| all ProvidedCHO properties | `edm.RDF.ProvidedCHO.*` | property mapping (Step 2) |
| PhysicalThing array | `edm.RDF.PhysicalThing[]` | archival hierarchy retyping (`transform-script-adr.md` D10) |
| WebResource | `edm.RDF.WebResource[0]` | mt002 ImageObject typing (`transform-script-adr.md` D12) |
| provenance fields | `properties.*`, `provider-info.*`, `source.*`, `binaries.binary[]` | prov triples [4] — see `ddbedm-prov-o-plan.md` for full field mapping |

**Bare-ID `about` values**: some `edm.RDF.*.about` fields and `.resource` references contain only the 32-char DDB internal ID instead of a full URI. Mint before emitting any triple (`transform-script-adr.md` D27):
- `ProvidedCHO` → `http://www.deutsche-digitale-bibliothek.de/item/<id>`
- All other entity types → `urn:ddbedm:<ClassName>:<id>`

---

## 2. Step 1 — Class dispatch (`retype_entities()`)

Dispatch is **not uniform**. Per sector × mediatype stratum, `transform-adr.md` §1.2 specifies one of two modes:

| Mode | Logic |
|---|---|
| **htype first** | Apply htype lookup → DoCO/RiC-O class(es); then add the fixed mediatype class on top regardless of htype result |
| **dc:type only** | Assign fixed class(es) directly (no htype lookup); or apply `audio_type2class.json` for AUDIO strata |

### 2.1 Dispatch table

→ See **`transform-revised-plan.md` §1.1** for the canonical, up-to-date dispatch table (sparte × mediatype × htype → domain class). The table previously inlined here has been superseded by that version.

### 2.2 htype first — two-layer logic

For "htype first" strata, dispatch is two independent layers accumulated:
1. htype lookup in `lookup_htype_doco_rico.csv` → DoCO or RiC-O class(es) + `rico:hasRecordSetType` where applicable
2. Fixed mediatype class added on top unconditionally

If htype is absent or pending, layer 1 contributes nothing; layer 2 still fires.

For `rico:RecordSet` rows, `rico:hasRecordSetType` is asserted twice: `ric-rst:*` (coarse) + `vocnet-htype:htXXX` (fine-grained) per `has_record_set_type` column.

### 2.3 dc:type only — fixed and config variants

- **Fixed**: emit the listed class(es) directly; dc:type string value is not read for class dispatch
- **Config** (AUDIO only): look up dc:type string in `output/config/audio_type2class.json` → Group A → `mo:MusicalManifestation` (M); Groups B/C → `aco:AudioManifestation` (M). See D16 (`transform-script-adr.md`)

### 2.4 Additional typing

- **PhysicalThing** entities: htype lookup only; no `mocho:Manifestation` (`transform-script-adr.md` D10)
- **mt002 WebResources**: typed as `mocho:ImageObject` + `rdac:C10007` + `rdam:P30001 rdact:1018` + `vra:imageOf <cho-uri>` (`transform-script-adr.md` D12)

### 2.5 Lookup tables

| Table | Keyed by | Used by |
|---|---|---|
| `output/config/lookup_htype_doco_rico.csv` | `htype_code` | htype-first strata (layer 1) |
| `output/config/audio_type2class.json` | `(dc_type_de, sector)` | dc:type only × AUDIO strata |

---

## 3. Step 2 — Property mapping (`emit_triples()`)

For each ProvidedCHO, iterate over EDM properties and emit target triples.

### 3.1 General property dispatch

1. Look up `(target_class, edm_prop)` in `output/config/lookup_class_prop_alignment.csv`
   - If `target_prop != edm_prop` → emit both `edm_prop` and `target_prop` (dual-emit; `transform-props-mapping-adr.md` D4)
   - If `target_prop == edm_prop` → emit `edm_prop` only
2. Five predicates remapped to RDA Manifestation-level (`transform-props-mapping-adr.md` D5):

| edm_prop | target_prop |
|---|---|
| `dc:title` | `rdam:P30134` (+ dual-emit `dc:title`; `transform-props-mapping-adr.md` D4) |
| `dc:description` | `rdam:P30137` |
| `dc:date` | `rdam:P30278` |
| `dc:issued` | `rdam:P30278` |
| `dcterms:isPartOf` | `rdam:P30020` (object sanitised — see note) |

   **isPartOf sanitisation**: before emitting, normalise the resource value:
   - Full DDB URL (`http://www.deutsche-digitale-bibliothek.de/item/<UUID>`) → use as-is
   - Bare 32-char UUID → prepend `http://www.deutsche-digitale-bibliothek.de/item/`
   - Label-only (no resource) → skip; no triple emitted in graph/mocho

3. Two properties skipped in `graph/mocho` — no mocho triple emitted:
   - `ddb:aggregationEntity`
   - `ddb:hierarchyPosition`

   Both are DDB-internal structural fields with no mocho alignment equivalent. They are preserved verbatim in `graph/ddbedm` via the passthrough (stream [1]).

### 3.2 Special handlers

| Handler | Keys | Logic | ADR |
|---|---|---|---|
| `emit_subject_triples()` | `dcSubject`, `dcTermsSubject`, `dcTermSubject` | IRI value → `dcterms:subject <uri>` + `<uri> rdfs:label "label"@lang`; literal → `dc:subject "string"`; dedup per record | `transform-props-mapping-adr.md` D1 |
| `emit_creator_triples()` | `creator` | two-track dispatch (see §3.2.2) | `transform-props-mapping-adr.md` D2 |
| `emit_contributor_triples()` | `contributor` | LIDO event type dispatch via edm:Agent + edm:Event (see §3.2.3) | `transform-props-mapping-adr.md` D3 |
| `emit_aggregation_triples()` | `Aggregation.*` | `dcterms:source` (isShownAt), `edm:dataProvider` (org URI filter), `foaf:thumbnail` (object) | `transform-script-adr.md` D23 |
| `emit_place_stubs()` | `Place[].prefLabel` | `<place-uri> rdfs:label "..."@lang` for each Place referenced by CHO | `transform-script-adr.md` D24 |

#### 3.2.1 `dc:title` — dual-emit

```python
# lookup_class_prop_alignment indexed as {(target_class, edm_prop): target_prop}
target_prop = alignment.get((target_class, "dc:title"))

if target_prop and target_prop != "dc:title":
    emit(cho_iri, DC.title, value)          # cross-WEMI handle
    emit(cho_iri, target_prop, value)       # class-specific (e.g. rdam:P30134)
else:
    emit(cho_iri, DC.title, value)          # dc:title only
```

#### 3.2.2 `dc:creator` — two-track dispatch

Both tracks run independently for every creator value (`transform-props-mapping-plan.md §4`).

```python
def emit_creator_triples(cho_iri, creator_values, agents, target_class, alignment):
    # Track 1 — class-specific predicate (always runs)
    target_prop = alignment.get((target_class, "dc:creator"))
    # target_prop: rdam:P30329 (M), rdaw:P10065 (W), rdae:P20053 (E)

    for cv in creator_values:
        label    = (cv.get("$") or "").strip()
        resource = (cv.get("resource") or "").strip()

        # Track 1: emit class-specific predicate (IRI if available, else literal)
        if target_prop and target_prop != "TBD":
            if resource:
                emit(cho_iri, target_prop, URIRef(resource))
            elif label:
                emit(cho_iri, target_prop, Literal(label))

        # Track 2: resolve Agent URI → dcterms:creator + agent stub (independent of Track 1)
        agent = resolve_agent(label, resource, agents)  # URI match, then label match
        if agent and is_ddb_or_gnd(agent["about"]):
            agent_uri = URIRef(agent["about"])
            emit(cho_iri, DCTERMS.creator, agent_uri)   # generic cross-WEMI handle
            emit(agent_uri, RDF.type, MOCHO.Agent)
            emit(agent_uri, RDFS.label, Literal(agent["prefLabel"]))
        # if no URI resolved: Track 2 silent (no literal fallback on dcterms:creator)
```

When a URI resolves, a creator gets two predicate triples — one class-specific (`rdam:P30329 <uri>`) and one generic (`dcterms:creator <uri>`) — consistent with the dual-emit pattern (`transform-props-mapping-adr.md` D4). Source: `transform-props-mapping-adr.md` D2, `transform-props-mapping-plan.md §4`.

#### 3.2.3 `dc:contributor` — LIDO event type dispatch

The predicate emitted for each contributor value is determined by the LIDO event type of the `edm:Event` in which the contributor's Agent URI participates. Resolution requires two indexes built once per record:

**Index 1 — Event participant index** (`event_participant_index`):
```python
# {agent_uri: lido_hastype_resource}
event_participant_index = {}
for event in coerce_list(rdf.get("Event")):
    hastype = (event.get("hasType") or {}).get("resource", "").strip()
    for p in coerce_list(event.get("P11_had_participant")):
        puri = (p.get("resource") or "").strip()
        if puri and hastype:
            event_participant_index[puri] = hastype
```

**Index 2 — LIDO → target predicate** (loaded once from `output/config/lido_event_types.csv`):
```python
# {lido_uri: {col: target_prop, ...}}
# columns: rdam_prop, rdaw_prop, vra_image_prop, vra_work_prop, rico_prop, dc_fallback
lido_dispatch = load_lido_event_types("output/config/lido_event_types.csv")
```

**Dispatch per contributor value**:
```python
def emit_contributor_triples(cho_iri, contributor_values, event_participant_index,
                              lido_dispatch, target_class, wemi):
    prop_col = {
        # wemi × target_class → column name in lido_event_types.csv
        ("M", "rdac:C10007"):          "rdam_prop",
        ("M", "mocho:Manifestation"):  "rdam_prop",
        ("W", "rdac:C10001"):          "rdaw_prop",
        ("M", "vra:Image"):            "vra_image_prop",
        ("W", "vra:Work"):             "vra_work_prop",
        ("", "rico:RecordSet"):        "rico_prop",
        ("", "rico:Record"):           "rico_prop",
        ("", "rico:RecordPart"):       "rico_prop",
    }.get((wemi, target_class), "dc_fallback")

    for cv in coerce_list(contributor_values):
        resource = (cv.get("resource") or "").strip()
        label    = (cv.get("$") or "").strip()

        # Step 1: resolve LIDO event type via participant index
        lido_type = event_participant_index.get(resource) if resource else None
        row = lido_dispatch.get(lido_type) if lido_type else None
        target_prop = row[prop_col] if row else "dc:contributor"

        # Step 2: emit IRI or literal + agent stub
        if resource:
            agent_uri = URIRef(resource)
            emit(cho_iri, target_prop, agent_uri)
            emit(agent_uri, RDF.type, MOCHO.Agent)
            emit(agent_uri, RDFS.label, Literal(label))
        elif label:
            emit(cho_iri, target_prop, Literal(label))
        # if neither: skip
```

**Fallback rules** (all cases → `dc:contributor`):
- No matching Event found for contributor URI
- Contributor is label-only (no `resource`)
- LIDO event type not in `lido_event_types.csv`

Definitive spec: `transform-props-mapping-plan.md §5`. Config source: `output/config/lido_event_types.csv`. Full dispatch table and property rationale: `transform-props-mapping-adr.md D3`.

### 3.3 Lookup table

| Table | Keyed by | Output | ADR |
|---|---|---|---|
| `output/config/lookup_class_prop_alignment.csv` | `(target_class, edm_prop)` | `target_prop` | `transform-props-mapping-adr.md` D4 |
| `output/config/lido_event_types.csv` | `lido_hastype_resource` | `{rdam_prop, rdaw_prop, vra_image_prop, vra_work_prop, rico_prop, dc_fallback}` | `transform-props-mapping-adr.md` D3 |

`lookup_class_prop_alignment.csv` fully populated — all CHO properties from `transform-props-mapping-plan.md §0.1` plus Agent, Aggregation, and gndo properties.

---

## 4. Output — four streams

All N-Quads output uses `.nq` format; each line includes the named graph IRI as the fourth element (`transform-script-adr.md` D22). See §0 for filename conventions per run mode.

**POC** (`output/goethe-faust.nq` — all streams combined; `output/goethe-faust-werk-staging.duckdb`):

| Named graph | Content | Records |
|---|---|---|
| `…/graph/ddbedm` | Verbatim EDM passthrough — all `edm.RDF.*` fields; all records including mt007 | All |
| `…/graph/mocho` | Aligned mocho triples — CHO subject minted as `https://gemea.ise.fiz-karlsruhe.de/mocho/<object_id>` (`transform-script-adr.md` D22); `owl:sameAs` to original DDB URI; Agent/Place/WebResource retain original URIs | All except mt007 |
| `…/graph/prov` | PROV-O — Layer 1 per-item (`transform-adr.md` D11) | All |
| — (DuckDB) | W-slot staging rows: dc:title, dc:alternative[], dc:created, creator URIs, creator literals (`last, first`) | W-slot records only (`transform-script-adr.md` D26) |

`link_gnd_works.py` (Phase 0) consumes the DuckDB staging table and writes a separate file:

| Named graph | Content | Output file |
|---|---|---|
| `…/graph/work` | WEMI link triples: `rdac:C10001`, `mocho:hasManifestation`, `mocho:isManifestationOf`, `skos:exactMatch` (`transform-adr.md` D17, `transform-script-adr.md` D26) | POC: `goethe-faust-work.nq`; full corpus: `<sector>-work.nq` |

**Full corpus**: `transform_edm_to_mocho.py` outputs split into `<sector>-ddbedm.nq`, `<sector>-mocho.nq`, `<sector>-prov.nq`, `<sector>-werk-staging.duckdb` per sector DB.

---

## 5. Provenance triples — PROV-O

Fully specified in `notes/ddbedm-prov-o-plan.md`. Implemented inside `transform_edm_to_mocho.py` (not a separate script). Source: `transform-adr.md` D11 (per-item pattern).

**Layer 1 — per item** (Without-Activity pattern; 6 node types per record: 5-node base + SourceRecord from `binaries.binary[]`):

| Node | rdf:type | Source fields |
|---|---|---|
| CHO entity | `prov:Entity` | `edm.RDF.ProvidedCHO.about` |
| Dataset | `dcat:Dataset`, `prov:Entity` | `source.description.record.*` |
| XSLT pipeline | `prov:SoftwareAgent` | fixed IRI |
| Provider | `prov:Agent`, `foaf:Organization` | `provider-info.*` |
| DDB (fixed) | `prov:Agent`, `foaf:Organization` | fixed |
| SourceRecord | `prov:Entity` | `binaries.binary[]` |

**Layer 2 — per run** (Full Activity pattern): **Future work. Not implemented by `transform_edm_to_mocho.py`.** Intended to extend PROV-O coverage to LM-assisted enrichments and inter-script lineage. Specified in `ddbedm-prov-o-plan.md §3`.

---

## 6. Work-level GND staging (Phase 0)

Script: `scripts/link_gnd_works.py` (Phase 0; reads DuckDB staging table produced by `transform_edm_to_mocho.py`)

When class dispatch assigns a W-slot class (`rdac:C10001` or `mo:MusicalWork`), `transform_edm_to_mocho.py` inserts a staging row into `output/goethe-faust-werk-staging.duckdb`. Fields: `dc_title`, `dc_alternative[]`, `dc_created`, `creator_uris[]`, `creator_literals` (`last, first`). See `transform-script-adr.md` D26 and `transform-revised-plan.md §1.2`.

`link_gnd_works.py` consumes the staging table, performs ISBD title extraction + NER fallback + lobid-gnd Werk lookup, mints `<gemea-work-uri>` (`https://gemea.ise.fiz-karlsruhe.de/work/<id>`), and writes Work entity triples + WEMI links into `graph/work`:

```turtle
<gemea-work-uri>  a rdac:C10001 .
<gemea-work-uri>  mocho:hasManifestation  <gemea-cho-uri> .
<gemea-work-uri>  skos:exactMatch         <gnd-uri> .       # when GND lookup succeeds
<gemea-cho-uri>   mocho:isManifestationOf <gemea-work-uri> .
```

`transform_edm_to_mocho.py` does not emit `mocho:isManifestationOf` — that link is written by `link_gnd_works.py` only. See `transform-adr.md D17` for full rationale (Work URI minting, `skos:exactMatch` vs `owl:sameAs`, GND URI as Work node rejected).

---

## 7. Class mapping detail: old-config → mocho-aligned

*(Retained from original plan — inputs to `gen_dctype_class_mapping.py`)*

### 7.1 Audio (mt001)

| Old M-slot class | New `rdf_type_m` | Group |
|---|---|---|
| `mo:MusicalManifestation` | `mo:MusicalManifestation` | A — Musical |
| `mo:Record`, `aco:AudioClip` | `aco:AudioManifestation` | B/C — Non-musical |
| `fabio:AudioDocument` at E | `aco:AudioManifestation` | B — Produced audio |

`mo:MusicalWork` [W] populated in config for Group A but not emitted for ProvidedCHO — reserved for future Work-entity generation.

### 7.2 Text (mt003)

RDA Manifestation-level via `rdac:C10007`. Document categories (Dissertation, Lehrbuch) preserved as literals via property alignment — not promoted to rdf:type (no RDA rdf:type class for bibliographic genre). DoCO structural classes via htype dispatch only.

### 7.3 Photo (mt002)

Sector × dc:type dispatch from `image_type2class.json` (851 entries). W-slot class replaces `mocho:Manifestation` (`transform-script-adr.md` D11). See `image-type-class-mapping.md` §3.1.

### 7.4 Video (mt005)

dc:type dispatch from `video_type2class.json`. `ec:EditorialWork` [W] + `ec:MediaResource` [M] for editorial types; `ec:MediaResource` [M] default.

### 7.5 Not Digitized (mt007)

**ddbedm stream**: verbatim EDM triples emitted (faithfulness baseline).
**prov stream**: provenance triples emitted (pipeline audit trail — the record was seen and processed).
**mocho, work streams**: skipped — no triples emitted (`transform-script-adr.md` D15).

Detection: `_extract_mediatype_sector()` returns `mt007`; mt007 guard applied before mocho/work handlers fire only.

---

## 8. Verification checklist

**Config tables:**
- [x] `lookup_class_prop_alignment.csv` fully populated for all EDM properties in `transform-props-mapping-plan.md`
- [x] `lido_event_types.csv` present at `output/config/`

**Class dispatch spot-checks:**
- [ ] `Schallplatte` → `mo:MusicalManifestation`; `Zeichnung` (sparte006) → `vra:Work`; `htype_021` → `rdac:C10001 + rdac:C10007`
- [ ] mt007 record → ddbedm + prov quads present; mocho/work output empty for that ID
- [ ] edm:Agent with `gndo:DifferentiatedPerson` type → `mocho:Agent`

**Output streams:**
- [ ] POC: `goethe-faust.nq` (combined) + `goethe-faust-werk-staging.duckdb` present; full corpus: `<sector>-ddbedm.nq`, `<sector>-mocho.nq`, `<sector>-prov.nq`, `<sector>-werk-staging.duckdb` per sector
- [ ] All `.nq` lines have exactly four space-separated terms + ` .` (N-Quads format)
- [ ] Named graph IRIs ∈ `{graph/ddbedm, graph/mocho, graph/prov}` — no `.nt` graph names
- [ ] mocho graph CHO subjects use `https://gemea.ise.fiz-karlsruhe.de/mocho/<32-char-id>`
- [ ] `owl:sameAs` count in mocho graph == records_processed (minus mt007 count)

**Stats and logs:**
- [ ] `output/transform_errors.jsonl` is empty or exceptions reviewed
- [ ] `output/transform_stats.json` contains `records_processed`, `error_count`, sector/mediatype breakdowns
- [ ] `--stats full` run produces LIDO event type counts, Agent type distribution, Place label coverage (feeds 30-resource.tex and 40-quality.tex TODOs)

**ADR cross-references confirmed:**
- [ ] D22 (N-Quads + CHO URI minting), D23 (Aggregation), D24 (Place stubs), D25 (LIDO contributor), D26 (Werk staging)
- [ ] `transform-adr.md` D11 (PROV-O per-item), D15 (N-Quads architecture), D17 (Work URI minting + WEMI link pattern)
- [ ] `transform-props-mapping-adr.md` D1–D3 (subject/creator/contributor)
- [ ] `scripts/README.md` updated: new flags (`--werk-staging`, `--stats`, `--workers`, `--batch-size`, `--ids -`), all four output files

---

## 10. Open review issues

Issues identified during 2026-05-04 review. Work through one by one before implementation.

- [x] **R1 — §0.1 debug `<graphname>` list includes `work`** — resolved: `work` removed from list; Werk staging debug handled separately by `link_gnd_works.py`.

- [x] **R2 — §1 provenance fields row too narrow** — resolved: row updated to `properties.*`, `provider-info.*`, `source.*`, `binaries.binary[]` with pointer to `ddbedm-prov-o-plan.md` as definitive reference.

- [x] **R3 — §3.2 handler table ADR references are ambiguous** — resolved: all three cite `transform-props-mapping-adr.md D1/D2/D3`. D1 also amended: IRI path now emits concept stub `<uri> rdfs:label "label"@lang` in addition to `dcterms:subject <uri>`; literal path keeps `dc:subject "string"`.

- [x] **R4 — §3.2.2 `emit_creator_triples()` Track 2 hardcodes `DCTERMS.creator`** — resolved: `DCTERMS.creator` is correct (generic cross-WEMI handle per `transform-props-mapping-plan.md §4`). Bug was the `continue` making tracks mutually exclusive; fixed to run both independently. Also led to D16 in `transform-adr.md` (Work URI minting + WEMI link pattern).

- [x] **R4b — §3.2.2 `emit_creator_triples()` Track 1: code to be updated** — resolved: code already corrected when R4 was fixed; both tracks run independently, `continue` removed.

- [x] **R5 — §5 Layer 1 node count says 5, table has 6** — resolved: heading updated to "6 node types (5-node base + SourceRecord from `binaries.binary[]`)".

- [x] **R6 — §5 two prov-related named graph URIs are unexplained** — resolved: named graph base updated to `https://gemea.ise.fiz-karlsruhe.de/` throughout; §5 Layer 2 marked as future work (not implemented by `transform_edm_to_mocho.py`); D12 reference removed from §5 source line.

---

- [x] **I1 — §2.3: D16 numbering collision** — resolved: Work URI minting decision renumbered to `transform-adr.md D17`; all references updated in `transform-script-plan.md` and `transform-revised-plan.md`.

- [x] **I2 — §3.1: "(D6)" source unknown** — resolved: skip is intentional; `ddb:aggregationEntity` and `ddb:hierarchyPosition` are DDB-internal structural fields with no mocho alignment equivalent. They are preserved in `graph/ddbedm` via verbatim passthrough. No ADR entry needed; stale "(D6)" reference removed from §3.1.

- [x] **I3 — §3.3 lookup table: bare ADR references** — resolved: both now cite `transform-props-mapping-adr.md D4` and `D3`.

- [x] **I4 — §3.2.3 contributor: label-only fallback logic is unspecified** — resolved: `transform-props-mapping-plan.md §5` is the definitive spec; fallback for all non-matched cases (URI absent, label-only, unknown LIDO type) is simply `dc:contributor`. Erroneous label-match logic removed from §3.2.3.

- [x] **I5 — §3.2.3: bare "ADR D3" reference** — resolved as part of I4; §3.2.3 now cites `transform-props-mapping-adr.md D3`.

- [x] **I6 — §4: `link_gnd_works.py` N-Quads output absent** — resolved: §4 now includes a separate table for `link_gnd_works.py` output (`graph/work`, WEMI link triples, POC filename `goethe-faust-work.nq`).

- [x] **I7 — §8: audio config path inconsistency** — resolved: `output/config/audio_type2class.json` is canonical and must not be overwritten by any script. §8 input list updated accordingly.

- [x] **I8 — §9 verification: two gaps** — resolved: (a) withdrawn — Layer 2 is future work, not implemented by `transform_edm_to_mocho.py`; §9 named-graph list is correct as-is. (b) `transform-adr.md D17` added to ADR cross-reference checklist; D12 removed (Layer 2 out of scope).

- [x] **I9 — §10 R4b: stale text after resolution note** — resolved: stale problem description removed from R4b entry.

- [x] **I10 — §0 / §4: output filename prefix inconsistency** — resolved: POC outputs all N-Quads streams into one combined `goethe-faust.nq`; full corpus uses `<sector>-<stream>.nq` per sector DB. Both §0 stream table and §4 updated to reflect the two conventions.

- [x] **I11 — §1: bare-ID `about` values undocumented** — resolved: §1 note and D27 added. `ProvidedCHO` bare IDs → `http://www.deutsche-digitale-bibliothek.de/item/<id>`; all other entity types → `urn:ddbedm:<ClassName>:<id>`. Consistent with `export-s2-plan.md §4.3` and `export_ddb.py`.
