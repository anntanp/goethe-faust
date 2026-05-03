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
      ├── [1] edm.RDF → raw EDM triples ────────────────────────→ <sector>-ddb-edm.nt
      │       Priority #1. Faithfully round-trips the EDM payload.   graph/ddb-edm
      │       Baseline for provenance and future re-alignment.
      │
      ├── [2] edm.RDF alignment → mocho triples ────────────────→ <sector>-mocho.nt
      │       Step 2a: class dispatch (§1.1 transform-revised-plan.md)  graph/mocho
      │       Step 2b: property mapping (transform-props-mapping-plan.md)
      │
      ├── [3] GND Work entity links ──────────────────────────────→ <sector>-work.nt
      │       W-level ProvidedCHOs → GND Werk via owl:sameAs           graph/work
      │       Phase 1b; depends on mocho graph IRIs
      │
      └── [4] Provenance triples ──────────────────────────────────→ <sector>-prov.nt
              Two-layer PROV-O per ddbedm-prov-o-plan.md               graph/prov
```

Named graph base: `http://gemea.ddb.de/`

| Stream | Named graph IRI | Output file | Script |
|---|---|---|---|
| [1] ddb-edm | `…/graph/ddb-edm` | `<sector>-ddb-edm.nt` | `transform_edm_to_mocho.py` |
| [2] mocho | `…/graph/mocho` | `<sector>-mocho.nt` | `transform_edm_to_mocho.py` |
| [3] work | `…/graph/work` | `<sector>-work.nt` | `link_gnd_works.py` |
| [4] prov | `…/graph/prov` | `<sector>-prov.nt` | `prov_edm_to_mocho.py` |

Named graph names follow kebab-case URL path conventions (D20).

mt007 (NOT DIGITIZED) records are **skipped** in streams [2] and [3] — no mocho or work triples emitted (D15). Stream [1] still emits raw EDM triples for mt007 records (faithfulness over filtering).

**POC**: `data/items-all-goethe-faust.json` (JSONL, 115,432 records) for rapid iteration. JSONL and sqlite/bufgz carry identical cortex JSON structure; field paths in §1 apply to both. D1 governs the JSONL pass; D19 governs the `s2.sqlite` pass.

### 0.1 Debug mode

When `--debug` is set, after the main run also produce:

1. **Parquet snapshot**: all cortex JSON fields (pre-transform) written to `debug/<sector>-raw.parquet` for DuckDB inspection.
2. **100-record sqlite sample**: 100 randomly sampled records extracted to `debug/<sector>-sample-100.sqlite` (same schema as source DB).
3. **Per-record named files** (for the 100 sampled records only):
   - `debug/<graphname>-<ddb-object-id>.nt` — N-Triples for each output stream
   - `debug/<graphname>-<ddb-object-id>.ttl` — Turtle (human-readable)
   - `debug/<ddb-object-id>.jsonld` — JSON-LD for the mocho graph only

`<ddb-object-id>`: the DDB item identifier (e.g. `224BB273RJDT6WN7GAIRV4AJ5ES5YPC5`). `<graphname>`: one of `ddb-edm`, `mocho`, `work`, `prov`. See D21.

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
| PhysicalThing array | `edm.RDF.PhysicalThing[]` | archival hierarchy retyping (D10) |
| WebResource | `edm.RDF.WebResource[0]` | mt002 ImageObject typing (D12) |
| provenance fields | `source.description.href`, `provider-info.*` | prov triples [B] |

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

- **PhysicalThing** entities: htype lookup only; no `mocho:Manifestation` (D10)
- **mt002 WebResources**: typed as `mocho:ImageObject` + `rdac:C10007` + `rdam:P30001 rdact:1018` + `vra:imageOf <cho-uri>` (D12)

### 2.5 Lookup tables

| Table | Keyed by | Used by |
|---|---|---|
| `output/config/lookup_htype_doco_rico.csv` | `htype_code` | htype-first strata (layer 1) |
| `output/config/audio_type2class.json` | `(dc_type_de, sector)` | dc:type only × AUDIO strata |

Note: `lookup_dctype_to_class.csv` (planned in §8) covers only the audio dc:type config path in the current dispatch model. IMAGE and VIDEO strata use fixed classes, not per-value dc:type lookup.

---

## 3. Step 2 — Property mapping (`emit_triples()`)

For each ProvidedCHO, iterate over EDM properties and emit target triples.

### 3.1 General property dispatch

1. Look up `(target_class, edm_prop)` in `output/config/lookup_class_prop_alignment.csv`
   - If `target_prop != edm_prop` → emit both `edm_prop` and `target_prop` (dual-emit; D4, `transform-props-mapping-adr.md`)
   - If `target_prop == edm_prop` → emit `edm_prop` only
2. Five predicates remapped to RDA Manifestation-level (D5):

| edm_prop | target_prop |
|---|---|
| `dc:title` | `rdam:P30134` (+ dual-emit `dc:title`; D4) |
| `dc:description` | `rdam:P30137` |
| `dc:date` | `rdam:P30278` |
| `dc:issued` | `rdam:P30278` |
| `dcterms:isPartOf` | `rdam:P30020` |

3. Two properties skipped — no triple emitted (D6):
   - `ddb:aggregationEntity`
   - `ddb:hierarchyPosition`

### 3.2 Special handlers

| Handler | Keys | Logic | ADR |
|---|---|---|---|
| `emit_subject_triples()` | `dcSubject`, `dcTermsSubject`, `dcTermSubject` | IRI value → `dcterms:subject`; literal → `dc:subject`; dedup per record | D1 |
| `emit_creator_triples()` | `creator` | two-track dispatch (see §3.2.2) | D2, D7 |
| `emit_contributor_triples()` | `contributor` | LIDO event type dispatch via edm:Agent + edm:Event (see §3.2.3) | D3 |

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

```python
def emit_creator_triples(cho_iri, creator_values, agents, target_class, alignment):
    # Track 1 — class dispatch
    target_prop = alignment.get((target_class, "dc:creator"))
    # target_prop is rdam:P30329, rdaw:P10065, dcterms:creator, or TBD

    for cv in creator_values:
        label = cv.get("$", "")
        resource = cv.get("resource", "")

        # Track 2 — Agent URI resolution
        agent = resolve_agent(label, resource, agents)  # URI match, then label match
        if agent and is_ddb_or_gnd(agent["about"]):
            agent_uri = URIRef(agent["about"])
            emit(cho_iri, DCTERMS.creator, agent_uri)
            emit(agent_uri, RDF.type, MOCHO.Agent)
            emit(agent_uri, RDFS.label, Literal(agent["prefLabel"]))
            # Track 1 not emitted when Track 2 resolves (dcterms:creator covers it)
            continue

        # Track 1 only — no URI resolved
        if target_prop and target_prop not in ("TBD", "dcterms:creator"):
            emit(cho_iri, target_prop, Literal(label))
```

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

**Fallback rules**:
- No matching Event for contributor URI → `dc:contributor`
- Contributor is label-only (no `resource`) → look up event by label match against Agent prefLabel (same normalization as `emit_creator_triples()`); if unresolved, `dc:contributor`
- LIDO event type not in `lido_event_types.csv` → `dc:contributor`

**Config source**: `output/config/lido_event_types.csv` — columns: `resource, label, rdam_prop, rdaw_prop, vra_image_prop, vra_work_prop, rico_prop, dc_fallback`. See ADR D3 for full dispatch table and property rationale.

### 3.3 Lookup table

| Table | Keyed by | Output | ADR |
|---|---|---|---|
| `output/config/lookup_class_prop_alignment.csv` | `(target_class, edm_prop)` | `target_prop` | D4 |
| `output/config/lido_event_types.csv` | `lido_hastype_resource` | `{rdam_prop, rdaw_prop, vra_image_prop, vra_work_prop, rico_prop, dc_fallback}` | D3 |

`lookup_class_prop_alignment.csv` populated for `dc:title`, `dc:creator`, `dcterms:alternative`, `dc:date`, `dc:issued`, `dc:description`. Expanded as property decisions are made in `transform-props-mapping-plan.md`.

---

## 4. Output [A] — CHO triples

| File | Content | Named graph |
|---|---|---|
| `output/goethe-faust-mocho.nt` | All CHO, PhysicalThing, WebResource triples | `http://gemea.ddb.de/graph/mocho` |

---

## 5. Concurrent [B] — Provenance triples

Script: `scripts/prov_edm_to_mocho.py` (pending)

Emits PROV-O triples per record: source entity → DDB item derivation chain, `prov:Agent` for institution and pipeline, `prov:generatedAtTime`. Pattern from `transform-adr.md` D11 (PROV-O).

| File | Content | Named graph |
|---|---|---|
| `output/goethe-faust-mocho-prov.nt` | PROV-O provenance triples | `http://gemea.ddb.de/graph/prov` |

Runs over the same JSONL input as [A]; does not depend on [A]'s output.

---

## 6. Concurrent [C] — GND linking triples (Phase 1b)

Script: `scripts/link_gnd_agents.py` (Phase 1b)

Enriches `edm:Agent` nodes created in [A] with GND authority data. Depends on [A] output (needs minted Agent IRIs) or runs as a second pass over the JSONL with the same IRI minting logic.

| File | Content | Named graph |
|---|---|---|
| `output/goethe-faust-mocho-gnd.nt` | GND enrichment triples for agents | `http://gemea.ddb.de/graph/gnd-enrichment` |

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

Sector × dc:type dispatch from `image_type2class.json` (851 entries). W-slot class replaces `mocho:Manifestation` (D11). See `image-type-class-mapping.md` §3.1.

### 7.4 Video (mt005)

dc:type dispatch from `video_type2class.json`. `ec:EditorialWork` [W] + `ec:MediaResource` [M] for editorial types; `ec:MediaResource` [M] default.

### 7.5 Not Digitized (mt007)

**Skip record — no triples emitted.** SOLR false-positive. Detected at record ingestion time.

---

## 8. `gen_dctype_class_mapping.py` spec

```
Purpose:    Generate lookup_dctype_to_class.csv — type dispatch table mapping
            (mediatype, sector, dc_type_de) to mocho-aligned rdf:type class IRIs.
Usage:      python gen_dctype_class_mapping.py
Inputs:     scripts/old-config/type2class.json
            scripts/old-config/audio_type2class.json
            output/config/image_type2class.json
            output/config/video_type2class.json
Outputs:    output/config/lookup_dctype_to_class.csv
Deps:       stdlib only (json, csv, pathlib)
```

`CLASS_MAP` (old FRBR/FaBiO → mocho-aligned IRIs):
```python
CLASS_MAP = {
    "mo:MusicalWork":           "http://purl.org/ontology/mo/MusicalWork",
    "mo:MusicalManifestation":  "http://purl.org/ontology/mo/MusicalManifestation",
    "mo:MusicalExpression":     "http://purl.org/ontology/mo/MusicalExpression",
    "mo:Record":                "http://purl.org/ontology/mo/Record",
    "aco:AudioManifestation":   "https://w3id.org/ac-ontology/aco#AudioManifestation",
    "aco:AudioClip":            "https://w3id.org/ac-ontology/aco#AudioClip",
    "aco:AudioFile":            "https://w3id.org/ac-ontology/aco#AudioFile",
    "vra:Work":                 "http://purl.org/vra/Work",
    "vra:Image":                "http://purl.org/vra/Image",
    "ec:EditorialWork":         "http://www.ebu.ch/metadata/ontologies/ebucoreplus#EditorialWork",
    "ec:MediaResource":         "http://www.ebu.ch/metadata/ontologies/ebucoreplus#MediaResource",
    "rico:Record":              "https://www.ica.org/standards/RiC/ontology#Record",
    "mocho:ImmovableWork":      "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#ImmovableWork",
    "mocho:ImageWork":          "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#ImageWork",
    # Deprecated FaBiO → omit (empty string = skip)
    "fabio:PrintObject":        "",
    "fabio:AnalogItem":         "",
    "fabio:DigitalItem":        "",
    "frbr:Work":                "",
    "frbr:Manifestation":       "",
    "frbr:Item":                "",
}
```

---

## 9. Verification checklist

- [ ] `lookup_dctype_to_class.csv` generated; TBD count = 0
- [ ] `lookup_class_prop_alignment.csv` fully populated for all EDM properties in `transform-props-mapping-plan.md`
- [ ] Spot-check dispatch: `Schallplatte` → `mo:MusicalManifestation`; `Zeichnung` (sparte006) → `vra:Work`; `htype_021` → `rdac:C10001 + rdac:C10007`
- [ ] Named graph IRIs confirmed and consistent across [A]/[B]/[C]
- [ ] `scripts/README.md` updated for all new/modified scripts
- [ ] ADR decisions cross-referenced: `transform-adr.md` D11, `transform-script-adr.md` D9–D16, `transform-props-mapping-adr.md` D1–D6
