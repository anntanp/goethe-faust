# Implementation Plan: `transform_edm_to_mocho.py`

## Context

All design decisions are finalised in `goethe-faust/notes/alignment-plan.md` (approved)
and `goethe-faust/notes/alignment-adr.md` (D1–D10). This is the reference implementation
of the mocho ingest transformation — validated on the goethe-faust corpus (115,432 records)
and intended as the canonical basis for all subsequent mocho corpus transforms.
The script streams with constant memory, stdlib only.

---

## Critical files

| Path | Role |
|---|---|
| `goethe-faust/scripts/transform_edm_to_mocho.py` | **New script** |
| `goethe-faust/data/items-all-goethe-faust.json` | Source JSONL |
| `goethe-faust/data/ids-all-goethe-faust.txt` | ID filter set |
| `goethe-faust/output/alignment_ddbedm_mocho.csv` | Alignment table |
| `goethe-faust/output/lookup_htype_doco_rico.csv` | htype → DoCO/RiC-O |
| `goethe-faust/output/mocho-goethe-faust.nt` | **New output** — N-Triples pipeline intermediate |
| `goethe-faust/output/mocho-goethe-faust.jsonld` | **New output** — JSON-LD for inspection/tooling |
| `goethe-faust/output/transform_stats.json` | **New output** — run stats + ignored triples inventory |
| `goethe-faust/scripts/README.md` | Must be updated |

---

## Implementation

### 1. Header block

```
Purpose:    Transform DDB-EDM JSONL records to mocho-aligned RDF triples (N-Triples + JSON-LD)
Usage:      python transform_edm_to_mocho.py [--jsonl FILE] [--ids FILE] [--out-nt FILE]
            [--out-jsonld FILE] [--stats FILE] [--limit N]
Inputs:     items-all-goethe-faust.json, ids-all-goethe-faust.txt,
            alignment_ddbedm_mocho.csv, lookup_htype_doco_rico.csv
Outputs:    mocho-goethe-faust.nt, mocho-goethe-faust.jsonld, transform_stats.json
Deps:       stdlib only (json, csv, re, collections, argparse, pathlib)
Assumes:    JSONL one JSON object per line; edm.RDF.* structure per alignment-ddbedm-mocho.md
```

### 2. Constants

```python
CHO_BASE             = "http://www.deutsche-digitale-bibliothek.de/item/"
RDF_TYPE             = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
MOCHO_NS             = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#"
MOCHO_MANIFESTATION  = MOCHO_NS + "Manifestation"
RICO_RST             = "http://www.ica.org/standards/RiC/ontology#hasRecordSetType"
CREATOR_IRI          = "http://rdaregistry.info/Elements/m/P30263"   # has creator agent of manifestation
CONTRIBUTOR_IRI      = "http://purl.org/dc/elements/1.1/contributor" # kept as-is; no generic RDA equiv in mocho
SUBJECT_KEYS         = {"dcSubject", "dcTermsSubject", "dcTermSubject"}

# Prefix expansion for load_htype_map
PREFIXES = {
    "doco":    "http://purl.org/spar/doco/",
    "rico":    "http://www.ica.org/standards/RiC/ontology#",
    "ric-rst": "http://www.ica.org/standards/RiC/vocabularies/recordSetTypes#",
    "mocho":   MOCHO_NS,
}
```

### 3. `load_alignment(path)` → `dict[tuple[str,str], list[dict]]`

- Read `alignment_ddbedm_mocho.csv` with `csv.DictReader`
- Include row iff `row['in_mocho'] == 'True'` and `row['rda_iri']` non-empty
  (string comparison — `in_mocho` is not a Python bool)
- Key: `(row['entity_type'], row['json_key'])`
- Value: list of `{'rda_iri': ..., 'rda_label': ..., 'wemi_level': ..., 'match_method': ...}`

### 4. `load_htype_map(path)` → `dict[str, tuple[str, list[str]]]`

- Read `lookup_htype_doco_rico.csv`
- Skip rows where `rdf_type == 'pending'` or `rdf_type` empty
- Key: `row['htype_code']` (e.g. `"htype_030"`)
- Value: `(rdf_type_iri, [rst_iri, ...])` where:
  - `rdf_type_iri` = expand prefix → full IRI using PREFIXES dict
  - `[rst_iri, ...]` = split `row['has_record_set_type']` on `', '`, expand each
    prefix → full IRI; empty list if column is blank
  - **Multi-value**: `has_record_set_type` can be comma-separated
    (e.g. `"mocho:Bestand, ric-rst:Fonds"`) → emit one `rico:hasRecordSetType`
    triple per individual

### 5. `load_ids(path)` → `set[str]`

- One 32-char ID per line; strip whitespace

### 6. `get_object_id(record)` → `str | None`

- `record['edm']['RDF']['ProvidedCHO']['about']`
- Split on `/`, return last segment (32-char ID)
- Return `None` if path missing or pattern mismatch

### 7. `value_to_nt_obj(val)` → `list[str]`

Handle all value shapes, returning valid NT object strings:

| Input shape | Output |
|---|---|
| `None` | `[]` |
| `""` (empty string) | `[]` |
| `str s` (non-empty) | `['"s"']` with `\` and `"` escaped |
| `list` | recurse on each element, flatten |
| `{"resource": IRI, ...}` where IRI non-null/non-empty | `["<IRI>"]` |
| `{"resource": null/empty, "lang": L, "$": text}` where L non-null, text non-empty | `['"text"@L']` with escaping |
| `{"resource": null/empty, "lang": null, "$": text}` where text non-empty | `['"text"']` with escaping |
| `{"resource": null/empty, "$": ""}` | `[]` |

Escaping: replace `\` → `\\`, then `"` → `\"` in literal strings.

### 8. `emit_subject_triples(entity, subject_nt, alignment)` → `list[str]`

- `lit_candidates = alignment.get(("ProvidedCHO", "dcSubject"), [])`
- `iri_candidates = alignment.get(("ProvidedCHO", "dcTermSubject"), [])`
- `seen: set[tuple[str,str]]` for per-entity dedup
- For each key in `SUBJECT_KEYS`: get raw val, call `value_to_nt_obj`
- For each obj_nt: if `obj_nt.startswith("<")` → use `iri_candidates`, else `lit_candidates`
- Only append `(pred_nt, obj_nt)` if not in `seen`

### 9. `retype_entities(rdf, htype_map)` → `list[str]`

**ProvidedCHO** (single dict):
1. Always emit `<cho_uri> <rdf:type> <mocho:Manifestation> .`
2. Get `htype_code = entity.get('hierarchyType')`; look up in `htype_map`
3. If found: emit `<cho_uri> <rdf:type> <rdf_type_iri> .`
4. For each rst_iri in list: emit `<cho_uri> <rico:hasRecordSetType> <rst_iri> .`

**PhysicalThing** (array, may be absent/None):
1. For each entity in array: get `htype_code`, look up in `htype_map`
2. If found: emit `<uri> <rdf:type> <rdf_type_iri> .`
3. For each rst_iri: emit `<uri> <rico:hasRecordSetType> <rst_iri> .`
4. If not found (absent or pending): emit nothing (no fallback type)

### 10. `transform_record(record, alignment, htype_map, ids_filter)` → `list[str]`

```
get_object_id → filter against ids_filter (skip if not in set)
rdf = record['edm']['RDF']
for entity_type, entities in rdf.items():
    normalise to list (ProvidedCHO/Aggregation are dicts, not arrays)
    for entity in entities:
        subject = entity.get('about') — skip if None
        if entity_type == 'ProvidedCHO':
            emit_subject_triples(...)
        for json_key, raw_val in entity.items():
            skip 'about', None values
            skip SUBJECT_KEYS for ProvidedCHO (handled above)
            if ProvidedCHO and json_key in ('creator','contributor'):
                emit single triple with CREATOR_IRI / CONTRIBUTOR_IRI; continue
            candidates = alignment.get((entity_type, json_key), [])
            for row in candidates:
                emit triples via value_to_nt_obj
retype_entities(rdf, htype_map)  # appended after entity loop
```

Track per-record stats: `records_processed`, `triples_out`, `unmatched_keys` Counter
(key = `"EntityType.json_key"` for any key with no alignment candidates and not
explicitly whitelisted/skipped).

### 11. JSON-LD output

JSON-LD is written as a streaming array — one object per ProvidedCHO subject.
Built per-record from the same `nt_lines` output using a helper:

```python
def nt_lines_to_jsonld_node(nt_lines: list[str]) -> dict:
    # Group triples by subject → {subject: {predicate: [objects]}}
    # For each subject, produce a JSON-LD node dict:
    #   "@id": subject_iri
    #   predicate_iri: [{"@id": obj} or {"@value": lit, "@language": lang}]
    # Return list of node dicts (one per subject in this record's triples)
```

Write strategy: open JSON-LD file at start, write `[\n`; after each record
write the node object(s) as `  {...},\n`; strip trailing comma and write `]\n`
at end. No full in-memory accumulation.

JSON-LD context is minimal — no prefix compaction in this pass (full IRIs).
A separate `@context` block with prefix declarations is prepended.

### 12. `main()`

- `argparse`: `--jsonl`, `--ids`, `--out-nt`, `--out-jsonld`, `--stats`, `--limit`
- Default paths relative to script location
- Stream: `for lineno, line in enumerate(in_fh)`
- Write both `.nt` and `.jsonld` simultaneously per record
- Write stats to JSON on completion

### 13. Stats output (`transform_stats.json`)

```json
{
  "records_processed": 115432,
  "records_skipped_not_in_ids": ...,
  "triples_out": ...,
  "triples_ignored": ...,
  "objects_missing_specific_type": ...,
  "whitelisted_keys": {"creator": "rdam:P30263", "contributor": "dc:contributor"},
  "ignored_properties": {
    "Aggregation.edmRights":         {"count": 115432, "edm_iri": "..."},
    "Aggregation.isShownAt":         {"count": 115432, "edm_iri": "..."},
    "ProvidedCHO.hasType":           {"count": 97272,  "edm_iri": "..."},
    "...": "..."
  }
}
```

`triples_ignored` = total value-level triple candidates skipped (sum of `count`
across `ignored_properties`). `ignored_properties` is a full inventory — every
`EntityType.json_key` that had at least one value in the corpus but zero
alignment candidates — including EDM-structural fields (D4), SKOS labels, geo
coords, etc. Sorted by count descending. Each entry records `edm_iri` from the
alignment table where available (for cross-reference), else `null`.

---

## One stale comment to fix in alignment-plan.md §3.5.4

The inline comment in the creator/contributor block still says
`rdaw:P10065 (has creator agent of work)` — should read
`rdam:P30263 (has creator agent of manifestation)`. Fix while writing the script.

---

## Verification (per alignment-plan.md §6)

1. Run full pass; check `triples_out / records_processed` ≈ 20–80
2. Spot-check one object per sector × mediatype — every ProvidedCHO has
   `mocho:Manifestation` rdf:type; mapped htype adds DoCO/RiC-O type
3. Grep NT for `europeana.eu` predicates — expect zero
4. Grep NT for `edm:ProvidedCHO` as rdf:type object — expect zero
5. Check PhysicalThing URIs in NT have RiC-O types (e.g. `rico:RecordSet`)
6. Confirm `dc:contributor` appears as predicate; `rdam:P30263` appears as predicate
7. Update `goethe-faust/scripts/README.md`
