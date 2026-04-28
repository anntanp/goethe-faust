# Plan: EDM JSONL → mocho RDF Transformation (Reference Implementation)

**Date**: 2026-04-14
**Status**: Approved
**Related**: `goethe-faust/notes/alignment-adr.md`, `mocho/notes/alignment-ddbedm-mocho-adr.md`, `mocho/notes/alignment-ddbedm-mocho-spec.md`, `mocho/notes/alignment-ddbedm-mocho.md`

---

## 1. Context

The alignment table `alignment_ddbedm_mocho.csv` was built by walking `edm.RDF.*` JSON fields in the JSONL corpus, then resolving `json_key → edm_iri → rda_iri` via the DCT→RDA map. The table is keyed by `(entity_type, json_key)` — matching the JSON structure of the JSONL, not the NT file.

The JSONL (`items-all-goethe-faust.json`) is the right input: it is already per-object, streams with constant memory, and requires only stdlib JSON parsing. No NT indexing phase needed.

The NT file is not used — it was generated from this same JSONL and carries no additional information for this alignment pass.

---

## 2. Critical files

| File | Role |
|---|---|
| `goethe-faust/data/items-all-goethe-faust.json` | Source JSONL (115,432 records, one per line) |
| `goethe-faust/data/ids-all-goethe-faust.txt` | 115,437 object IDs (32-char each); filter set |
| `goethe-faust/output/alignment_ddbedm_mocho.csv` | Alignment table — keyed by `(entity_type, json_key)`; columns: `entity_type, json_key, edm_prefix, edm_iri, record_count, coverage_pct, rda_iri, rda_label, wemi_level, match_method, in_mocho` |
| `goethe-faust/output/lookup_htype_doco_rico.csv` | htype code → DoCO/RiC-O class lookup |
| `goethe-faust/scripts/README.md` | Must be updated after script is added |

**Reference notes:**
- `mocho/notes/alignment-ddbedm-mocho.md` — working note; entity type inventory, fanout figures, known issues
- `mocho/notes/alignment-ddbedm-mocho-spec.md` — scope definition; in/out of scope per entity type
- `mocho/notes/alignment-ddbedm-mocho-adr.md` — decisions; especially D2 (DC→RDA route), D4 (EDM-structural out of scope)

---

## 3. Script: `goethe-faust/scripts/transform_edm_to_mocho.py`

### 3.1 Header

```
Purpose:    Transform DDB-EDM JSONL records to mocho-aligned RDF triples (N-Triples)
Usage:      python transform_edm_to_mocho.py [--jsonl FILE] [--ids FILE] [--out FILE] [--limit N]
Inputs:     items-all-goethe-faust.json, ids-all-goethe-faust.txt,
            alignment_ddbedm_mocho.csv, lookup_htype_doco_rico.csv
Outputs:    mocho-goethe-faust.nt, transform_stats.json
Deps:       stdlib only (json, csv, re, collections, argparse, pathlib)
Assumes:    JSONL: one JSON object per line; edm.RDF.* structure per alignment-ddbedm-mocho.md
```

### 3.2 Constants

```python
CHO_BASE        = "http://www.deutsche-digitale-bibliothek.de/item/"
RDF_TYPE        = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
EDM_CHO              = "http://www.europeana.eu/schemas/edm/ProvidedCHO"
DDB_HTYPE            = "ddb:hierarchyType"          # json_key in alignment table
MOCHO_NS             = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#"
MOCHO_MANIFESTATION  = MOCHO_NS + "Manifestation"   # every ProvidedCHO is an instance of this
RICO_RST        = "http://www.ica.org/standards/RiC/ontology#hasRecordSetType"

# Fan-out whitelist (issue 2): bypass alignment table for creator/contributor
CREATOR_IRI     = "http://rdaregistry.info/Elements/m/P30263"   # rdam:P30263 has creator agent of manifestation
CONTRIBUTOR_IRI = "http://purl.org/dc/elements/1.1/contributor" # dc:contributor (kept as-is; no generic RDA equivalent in mocho)
```

### 3.3 Phase 1 — Load lookup tables

```python
def load_alignment(path) -> dict[tuple[str, str], list[dict]]:
    # Key: (entity_type, json_key)
    # Value: list of rows where rda_iri non-empty and in_mocho == 'True'
    # Each row: {rda_iri, rda_label, wemi_level, match_method}
    # Rows with in_mocho=False or rda_iri empty → excluded

def load_htype_map(path) -> dict[str, tuple[str, str | None]]:
    # Key: htype_code (e.g. "htype_030") — confirmed format in JSONL literals
    # Value: (rdf_type_iri, has_record_set_type_iri or None)
    # Skip rows where rdf_type == "pending"
    # Expand prefix to full IRI (doco:, rico:, ric-rst:, mocho:)
```

### 3.4 Phase 2 — Load IDs filter

```python
def load_ids(path) -> set[str]:
    # 32-char IDs, one per line; strip whitespace
```

### 3.5 Phase 3 — Stream JSONL and transform

#### 3.5.1 Record structure (per `alignment-ddbedm-mocho.md`)

```
record.edm.RDF = {
  "ProvidedCHO": {dict},          # single entity
  "Aggregation": {dict},          # single entity
  "Agent":       [{dict}, ...],   # array
  "Concept":     [{dict}, ...],   # array
  "WebResource": [{dict}, ...],   # array
  "Event":       [{dict}, ...],   # may be absent
  "Place":       [{dict}, ...],   # may be absent
  "TimeSpan":    [{dict}, ...],   # may be absent
  "PhysicalThing":[{dict}, ...],  # may be absent
}
each entity: {"about": "<subject_uri>", "<json_key>": <value>, ...}
value types: null | str | list | {"resource": str|null, "lang": str|null, "$": str}
```

#### 3.5.2 Object ID resolution

```python
def get_object_id(record) -> str | None:
    # Extract 32-char ID from ProvidedCHO.about URI
    # about = "http://www.deutsche-digitale-bibliothek.de/item/{id}"
    # Return id portion; None if not matching pattern
```

#### 3.5.3 Field value → NT object

```python
def value_to_nt_obj(val) -> list[str]:
    # Handles all value shapes:
    #   null → []
    #   str  → ['"str"']
    #   list → flatten recursively
    #   {"resource": IRI, ...}  → ["<IRI>"]  (if resource non-null)
    #   {"lang": L, "$": text}  → ['"text"@L'] (if lang non-null, text non-empty)
    #   {"lang": null, "$": text} → ['"text"']
    # Skips nulls and empty strings
    # Escapes backslash, double-quote in literals
```

#### 3.5.4 Core transform loop

```python
def transform_record(record, alignment, htype_map, ids_filter) -> list[str]:
    # Returns list of NT lines for this record
    obj_id = get_object_id(record)
    if obj_id not in ids_filter:
        return []

    nt_lines = []
    rdf = record["edm"]["RDF"]

    for entity_type, entities in rdf.items():
        if entities is None:
            continue
        if isinstance(entities, dict):
            entities = [entities]
        for entity in entities:
            subject = entity.get("about")
            if not subject:
                continue
            subject_nt = f"<{subject}>"

            # Subject fields: value-type dispatch + cross-key deduplication
            # dcSubject / dcTermsSubject / dcTermSubject all carry subject data;
            # dcTermsSubject was incorrectly mapped to dc:subject — corrected in CSV.
            # After fix: dcSubject → dc:subject (literals); dcTermSubject/dcTermsSubject → dcterms:subject (IRIs).
            # Dispatch: collect unique values across all three keys; route by value type.
            if entity_type == "ProvidedCHO":
                nt_lines.extend(emit_subject_triples(entity, subject_nt, alignment))

            for json_key, raw_val in entity.items():
                if json_key == "about" or raw_val is None:
                    continue
                if entity_type == "ProvidedCHO" and json_key in SUBJECT_KEYS:
                    continue  # handled by emit_subject_triples

                # Fan-out whitelist (issue 2):
                #   creator    → single RDA property rdaw:P10065 (has creator agent of work)
                #   contributor → dc:contributor kept as-is; no generic RDA equivalent in mocho
                if entity_type == "ProvidedCHO" and json_key in ("creator", "contributor"):
                    pred_iri = CREATOR_IRI if json_key == "creator" else CONTRIBUTOR_IRI
                    pred_nt  = f"<{pred_iri}>"
                    for obj_nt in value_to_nt_obj(raw_val):
                        nt_lines.append(f"{subject_nt} {pred_nt} {obj_nt} .")
                    continue

                candidates = alignment.get((entity_type, json_key), [])
                for row in candidates:
                    pred_nt = f"<{row['rda_iri']}>"
                    for obj_nt in value_to_nt_obj(raw_val):
                        nt_lines.append(f"{subject_nt} {pred_nt} {obj_nt} .")

    # rdf:type for ProvidedCHO and PhysicalThing via ddb:hierarchyType
    nt_lines.extend(retype_entities(rdf, htype_map))
    return nt_lines

SUBJECT_KEYS = {"dcSubject", "dcTermsSubject", "dcTermSubject"}

def emit_subject_triples(entity, subject_nt, alignment) -> list[str]:
    # Collect all values from the three subject keys; deduplicate by (value_shape, content).
    # Dispatch each unique value:
    #   literal (str or lang-tagged text) → candidates for ("ProvidedCHO", "dcSubject")
    #   IRI (resource) → candidates for ("ProvidedCHO", "dcTermSubject")
    # Rationale: dc:subject is for uncontrolled literals; dcterms:subject for IRI references
    #            to controlled vocabulary terms (GND, LCSH, etc.).
    # dcTermsSubject IRI corrected in alignment CSV (was dc:subject, now dcterms:subject).
    lit_candidates = alignment.get(("ProvidedCHO", "dcSubject"), [])
    iri_candidates = alignment.get(("ProvidedCHO", "dcTermSubject"), [])

    seen_objs: set[tuple[str, str]] = set()  # (pred_nt, obj_nt) dedup
    nt_lines = []
    for key in SUBJECT_KEYS:
        raw_val = entity.get(key)
        if raw_val is None:
            continue
        for obj_nt in value_to_nt_obj(raw_val):
            is_iri = obj_nt.startswith("<")
            candidates = iri_candidates if is_iri else lit_candidates
            for row in candidates:
                pred_nt = f"<{row['rda_iri']}>"
                pair = (pred_nt, obj_nt)
                if pair not in seen_objs:
                    seen_objs.add(pair)
                    nt_lines.append(f"{subject_nt} {pred_nt} {obj_nt} .")
    return nt_lines

def retype_entities(rdf, htype_map) -> list[str]:
    # Handles rdf:type for ProvidedCHO and PhysicalThing — the two entity types
    # that carry hierarchyType.
    #
    # ProvidedCHO:
    #   - Always emit <cho_uri> rdf:type mocho:Manifestation (base type, D9).
    #   - If hierarchyType present and mapped: also emit DoCO or RiC-O class.
    #   - If has_record_set_type: emit <cho_uri> rico:hasRecordSetType <named_individual>.
    #   - No edm:ProvidedCHO fallback.
    #
    # PhysicalThing (archival hierarchy ancestors, each with own URI):
    #   - Each entity in the array carries its own hierarchyType → RiC-O class.
    #   - No mocho:Manifestation — these are archival aggregation nodes (RecordSet,
    #     Record, RecordPart), not carried objects.
    #   - Same htype lookup; if pending or absent: emit nothing (no fallback type).
    #   - If has_record_set_type: emit rico:hasRecordSetType as for ProvidedCHO.
```

### 3.6 Phase 4 — Output

```python
def main():
    alignment  = load_alignment(ALIGNMENT_CSV)
    htype_map  = load_htype_map(HTYPE_CSV)
    ids_filter = load_ids(args.ids)

    stats = defaultdict(int)
    unmatched_keys = Counter()

    with open(args.jsonl) as in_fh, open(args.out, "w") as out_fh:
        for lineno, line in enumerate(in_fh):
            if args.limit and lineno >= args.limit:
                break
            record = json.loads(line)
            nt_lines = transform_record(record, alignment, htype_map, ids_filter)
            for line in nt_lines:
                out_fh.write(line + "\n")
            stats["records_processed"] += 1
            stats["triples_out"] += len(nt_lines)

    write_stats(STATS_OUT, stats, unmatched_keys)
```

### 3.7 Stats output (`transform_stats.json`)

```json
{
  "records_processed": 115432,
  "records_skipped_not_in_ids": ...,
  "triples_out": ...,
  "triples_ignored": ...,
  "objects_missing_specific_type": ...,
  "whitelisted_keys": {"creator": "rdam:P30263", "contributor": "dc:contributor"},
  "ignored_properties": {
    "Aggregation.edmRights":  {"count": 115432, "edm_iri": "..."},
    "Aggregation.isShownAt":  {"count": 115432, "edm_iri": "..."},
    "...": "..."
  }
}
```

`triples_ignored` = total values skipped across all unmatched keys.
`ignored_properties` = full inventory of every `EntityType.json_key` with values
but no alignment candidates, sorted by count descending, with `edm_iri` for
cross-reference.

---

## 4. Alignment scope (per ADR + spec)

### 4.1 Per-entity-type treatment

All nine entity types present in `edm.RDF` are enumerated below. The general transform loop iterates every entity type; an entity's properties are emitted if and only if `alignment[(entity_type, json_key)]` returns at least one `in_mocho=True` row. Entity types with zero such rows produce no property triples.

| Entity type | Records (% of corpus) | in_mocho rows | Property triples | rdf:type | Notes |
|---|---|---|---|---|---|
| **ProvidedCHO** | 115,432 (100%) | 894 | ✅ emitted | `mocho:Manifestation` + dc:type dispatch (D11) + optional htype class (D9/D10) | Main cultural object; creator/contributor whitelisted (D7–D8); subject keys deduplicated (D6) |
| **WebResource** | 312,538 (270%) | 247 | ✅ emitted via general loop | mt002 only: `mocho:ImageObject`, `rdac:C10007`, `rdam:P30001 rdact:1018`, `vra:imageOf` (D12) | 247 mapped rows cover `type`, `edmRights`, `dcTermsRights`, `creator` |
| **Agent** | 422,026 (365%) | 22 | ✅ emitted via general loop | ❌ none | 22 rows for biographical properties (dates, labels, identifiers); GND sameAs links |
| **PhysicalThing** | 55,771 (48%) | 31 | ✅ emitted via general loop | htype lookup → DoCO/RiC-O class + optional `rico:hasRecordSetType` | `hierarchyType` key skipped in loop; handled by `retype_entities()` |
| **Place** | 118,088 (102%) | 17 | ✅ emitted via general loop | ❌ none | 17 rows; geo coords (lat/long), prefLabel, sameAs |
| **Aggregation** | 115,432 (100%) | 4 | ✅ emitted via general loop | ❌ none | 4 rows mapped; `isShownAt`, `aggregatedCHO`, `provider`, `dataProvider` are EDM-structural (D4) and skipped |
| **Event** | 158,407 (137%) | 0 | ❌ no triples | ❌ none | `hasType`, `happenedAt`, `occuredAt`, `P11_had_participant` — no mocho mapping; deferred |
| **Concept** | 717,638 (621%) | 0 | ❌ no triples | ❌ none | Read-only: used to extract mediatype + sector IRI for dc:type dispatch; `prefLabel`/`notation` not emitted |
| **TimeSpan** | 99,930 (86%) | 0 | ❌ no triples | ❌ none | `begin`/`end` — no mocho mapping yet; deferred |

### 4.2 General rules

- **Mapped**: `alignment[(entity_type, json_key)]` rows where `in_mocho=True` and `rda_iri` non-empty
- **EDM-structural skipped**: `edm:isShownAt`, `edm:aggregatedCHO`, `edm:provider`, `edm:dataProvider` — per ADR D4
- **Unmatched keys**: counted in `transform_stats.json → ignored_properties` with EDM IRI for cross-reference
- **Fan-out**: `dc:creator` → `rdam:P30263`; `dc:contributor` → `dc:contributor` (see ADR D7–D8)
- **rdf:type**: ProvidedCHO and PhysicalThing only; all other entity types get no `rdf:type` triple

---

## 5. Outputs

| File | Description |
|---|---|
| `goethe-faust/output/mocho-goethe-faust.nt` | mocho-aligned NT triples (pipeline intermediate) |
| `goethe-faust/output/mocho-goethe-faust.jsonld` | same triples in JSON-LD (inspection/tooling) |
| `goethe-faust/output/transform_stats.json` | records processed, triples out/ignored, full ignored-properties inventory |

---

## 6. Verification

Select one object per sector × mediatype combination for spot-checking. Coverage confirmed by grep on `items-all-goethe-faust.json`.

**Sectors** — IRI base `http://ddb.vocnet.org/sparte/sparte00N`:

| Code | Label | Records |
|---|---|---|
| sparte001 | Archiv | 50,216 |
| sparte002 | Bibliothek | 50,198 |
| sparte003 | Denkmalfach | 111 |
| sparte004 | Mediathek | 1,283 |
| sparte005 | Museum | 4,288 |
| sparte006 | Sonstige | 9,215 |
| sparte007 | Wissenschaftliche Einrichtung | 85 |

**Mediatypes** — IRI base `http://ddb.vocnet.org/medientyp/mt00N` (mt004, mt006 absent):

| Code | Label | Records |
|---|---|---|
| mt001 | Audio | 476 |
| mt002 | Photo | 20,228 |
| mt003 | Text | 52,247 |
| mt005 | Video | 96 |
| mt007 | Not Digitized | 42,360 |

Note: not all 35 sector × mediatype combinations are populated. Small sectors (sparte003 = 111, sparte007 = 85) and small mediatypes (mt001 = 476, mt005 = 96) may lack certain intersections — document missing combinations in `transform_stats.json`.

Steps:
1. Run `--limit N` covering the full corpus (or run full pass); inspect NT output per spot-check object
2. For each sector, select one object from each mediatype present in that sector; confirm every ProvidedCHO has a `mocho:Manifestation` rdf:type triple; where `hierarchyType` is present and mapped, confirm an additional DoCO or RiC-O rdf:type triple also appears; confirm no `edm:ProvidedCHO` rdf:type triples in output
3. Confirm at least one RDA property triple is emitted for `dc:title`, `dc:creator`, or `dc:description`
4. `transform_stats.json`: `triples_out / records_processed` ≈ 20–80 (reasonable range); `objects_missing_htype` documented
5. Grep output NT for `europeana.eu` predicates — should be zero (all EDM predicates replaced or skipped)
6. Update `goethe-faust/scripts/README.md`

---

## 7. RDF serialization choice

| Format | Process | Size | Read |
|---|---|---|---|
| **N-Triples** (`.nt`) | Best — one triple/line, no parser context, grep/awk/stream-friendly | Worst — full URIs repeated every line | Poor |
| **Turtle** (`.ttl`) | Good — most parsers support it | Best among text formats — prefix compression | Best |
| **JSON-LD** (`.jsonld`) | Moderate — needs JSON + context handling | Moderate | Moderate (if you know JSON) |
| RDF/XML | Worst | Worst | Worst |

**Decision**: N-Triples for pipeline intermediate files (transform output, QLever ingest, sort/dedup); Turtle for hand-authored files (ontology, SPARQL update templates). N-Quads (`.nq`) if named graph identity is required alongside the same processing advantages.

---

## 8. Known issues to flag in code comments (per `alignment-ddbedm-mocho.md`)

- **Triple subject keys**: ~~deduplication downstream~~ — **resolved**. `dcTermsSubject` IRI corrected in CSV (`dc:subject` → `dcterms:subject`). Transform uses `emit_subject_triples()`: value-type dispatch (literal → dc:subject candidates, IRI → dcterms:subject candidates) + per-record `(pred, obj)` deduplication across all three keys.
- **Fan-out**: ~~not filtered in POC~~ — **resolved**. `creator` (464 Work-level candidates) → whitelisted to `rdaw:P10065 has creator agent of work`. `contributor` (360 candidates, no generic RDA equivalent in mocho) → kept as `dc:contributor` directly. Both bypass the alignment table via early `continue` in the transform loop.
- **`Event.occurredAt`**: ~~no IRI resolved~~ — **resolved**. DDB API typo (`occuredAt`, one 'r') added to `OVERRIDES` in `align_ddbedm_to_mocho.py` → resolves to `edm:occurredAt`. `edm_field_profile.json` corrected to `occurredAt`. Will be picked up on next alignment re-run.
- **`in_mocho` column type**: string `"True"` / `"False"`, not a Python bool — compare as `row['in_mocho'] == 'True'`
- **`PhysicalThing.hierarchyType`**: ~~skipped~~ — **resolved**. `retype_entities()` handles both `ProvidedCHO` and `PhysicalThing`. PhysicalThing entities are archival hierarchy ancestors (Bestand, Gliederung, etc.) → typed via htype lookup to RiC-O classes only; no `mocho:Manifestation` (they are aggregation nodes, not carried objects). No fallback type if htype absent or pending.
