# Plan: Complete the goethe-faust Transform Pipeline

## 0. Context

Note reorganisation (§2 of prior plan) is **complete**:
- ✅ `alignment-plan.md` → `transform-plan.md`
- ✅ `alignment-adr.md` → `transform-adr.md`
- ✅ `transform-pseudocode.md` deleted
- ✅ Cross-references updated in `goethe-faust/.claude/CLAUDE.md`, `mocho/notes/alignment-ddbedm-mocho-adr.md`, `image-type-class-mapping.md` §6, `babel-ddb/.claude/CLAUDE.md`
- ✅ `audio-type-class-mapping.md` written (MO/ACO class justification; GND URI future path)
- ✅ `image-type-class-mapping.md` written

**Current note inventory (goethe-faust/notes/)**:

| File | Role | Status |
|---|---|---|
| `transform-plan.md` | Transform implementation plan | Approved |
| `transform-adr.md` | Transform ADR (D1–D12) | Accepted |
| `transform-script-plan.md` | Dispatch table plan (Phase A done; B–D pending) | In progress |
| `audio-type-class-mapping.md` | AUDIO dispatch model (MO/ACO groups A–C) | Done |
| `image-type-class-mapping.md` | IMAGE dispatch model (D11–D12) | Done |
| `video-type-class-mapping.md` | VIDEO type class justification | Done |
| `inputs.md` | Input file descriptions | Done |

**Remaining work**: transform pipeline Phases B–D + `dnb_uri` additions.

---

## 3. What is unfinished in the goethe-faust transform

The goethe-faust POC transform (`transform_edm_to_mocho.py`) currently:
- ✅ D1–D10: JSONL streaming, alignment table, htype dispatch, mocho:Manifestation base type
- ✅ D11–D12 (config): `image_type2class.json` updated with new dispatch groups
- ✅ Phase B0: `count_dctype_gnd_coverage.py` written and run → see observations below
- ❌ Phase B: `gen_dctype_class_mapping.py` not written → `lookup_dctype_to_class.csv` does not exist
- ❌ Phase C: `sample_type_dispatch.py` not written
- ❌ Phase D: `transform_edm_to_mocho.py` not updated to use the lookup CSV or type WebResources

### 3.0 Phase B0 — `count_dctype_gnd_coverage.py` ✅

**Observations (run on 115,432 records, 2026-04-17)**:

92,853 records (80.4%) have a dc:type value. **98.8% of dc:type occurrences have a
GND URI** via Concept.prefLabel → Concept.about. 1,033 unique dc:type values;
959 with GND URI, 74 without. Lower coverage is concentrated in archive and library
sectors, where free-text catalogue entries appear without a corresponding
controlled-vocabulary Concept node.

| Mediatype | Sector | Total | GND | % |
|---|---|---|---|---|
| Audio | all | 476 | 476 | 100% |
| Photo | Archive | 5,129 | 5,099 | 99.4% |
| Photo | Library, Monument, Research, Media Library, Museum, Others | 14,867 | 14,867 | 100% |
| Text | Archive | 23,024 | 23,015 | 100% |
| Text | Library | 19,996 | 19,550 | 97.8% |
| Text | Research, Media Library, Museum, Others | 288 | 288 | 100% |
| Video | all | 96 | 96 | 100% |
| Not Digitized | Archive | 17,320 | 16,930 | 97.7% |
| Not Digitized | Library | 11,359 | 11,120 | 97.9% |
| Not Digitized | Monument, Research, Media Library, Museum | 279 | 279 | 100% |

Outputs: `output/dctype_gnd_coverage.csv` (per mediatype/sector/dc_type_de),
`output/dctype_to_gnd_uri.csv` (1,033 rows; source for `dnb_uri` column).

**Conclusion**: GND URI dispatch (Option 1) is viable for 98.8% of dc:type
occurrences. The `dnb_uri` column in `lookup_dctype_to_class.csv` can be populated
by joining `dctype_to_gnd_uri.csv` on `dc_type_de`.

### 3.1 Phase B — `gen_dctype_class_mapping.py`

Reads all four config JSONs (audio, image, video, general) and writes
`output/lookup_dctype_to_class.csv`. Schema (updated to include `dnb_uri`):

| Column | Description |
|---|---|
| `mediatype` | IRI or `any` |
| `sector` | IRI or `any` |
| `dc_type_de` | German dc:type literal (current lookup key) |
| `dc_type_en` | English translation |
| `dnb_uri` | GND concept URI from old-config `dnb` field (future lookup key — Option 1 path) |
| `rdf_type_w` | Work-level class IRI |
| `rdf_type_e` | Expression-level class IRI |
| `rdf_type_m` | Manifestation-level class IRI |
| `rdf_type_i` | Item-level class IRI |
| `source_vocab` | `mo`, `aco`, `vra`, `mocho`, `rico`, `ebucoreplus`, etc. |
| `notes` | from config `notes` field |

**`dnb_uri` rationale**: dc:type is a German free-text literal — fragile as a long-term
lookup key. The old-config `dnb` field already maps many dc:type strings to GND Sachbegriffe
URIs (e.g. `Schallplatte` → `https://d-nb.info/gnd/4052032-8`). Carrying this URI into
the CSV preserves the path to GND-URI-based dispatch (Option 1) without requiring it now.
Future work: resolve dc:type literals to GND URIs via lobid-gnd lookup; then key dispatch
on `dnb_uri` rather than `dc_type_de`. Document this path in `audio-type-class-mapping.md` §4.

**CLASS_MAP additions** for mt002 new classes (add to `gen_dctype_class_mapping.py`):
```python
"vra:Work":            "http://purl.org/vra/Work",
"mocho:ImageWork":     "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#ImageWork",
"mocho:ImmovableWork": "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#ImmovableWork",
"mocho:ImageObject":   "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#ImageObject",
"mocho:Manifestation": "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation",
```

### 3.2 Phase C — `sample_type_dispatch.py`

Reads the JSONL and the lookup CSV; for a sample of records per (mediatype, sector)
cell, prints the dispatch result. Used to empirically validate the dispatch model
before modifying the transform.

### 3.3 Phase D — Update `transform_edm_to_mocho.py`

Two changes to `retype_entities()`:

**D.1 — dc:type dispatch for ProvidedCHO**

Load `lookup_dctype_to_class.csv` at startup (alongside htype CSV).
In `retype_entities()`, after the htype dispatch:
1. Extract mediatype + sector from the record's `edm.RDF.Concept` list
2. Extract dc:type from `ProvidedCHO.dcType`
3. Lookup (mediatype, sector, dc_type_de) → class row (three-level fallback: exact → any-sector → any-mediatype)
4. If W-slot class found: emit W-slot class **instead of** `mocho:Manifestation`
5. If M-slot class found: emit M-slot class **alongside** `mocho:Manifestation` (accumulation)
6. If no match: D9 fallback (`mocho:Manifestation` only)
7. Htype dispatch is independent — both layers can fire for the same record

**D.2 — WebResource typing for mt002**

After ProvidedCHO triples, for records where `mediatype = mt002`:
- Get WebResource URIs from `edm:isShownBy` and `edm:hasView`
- Emit for each WebResource URI:
```turtle
<wr-uri> a mocho:ImageObject ;
         a rdac:C10007 ;
         rdam:P30001 rdact:1018 ;
         vra:imageOf <cho-uri> .
```

---

## 3.4 Phase B0 — `count_dctype_gnd_coverage.py` (prerequisite for dnb_uri)

**Purpose**: measure what fraction of dc:type values in the corpus have a corresponding
GND URI via `edm.RDF.Concept`, and export the `dc_type_de → GND URI` mapping for use
as the `dnb_uri` column in `lookup_dctype_to_class.csv`.

**Lookup logic**: `ProvidedCHO.dcType` value → search `edm.RDF.Concept[]` for
case-insensitive `prefLabel` match → `Concept.about` is the GND URI.
Concept list also contains mediatype/sector IRIs (vocnet namespace) — skip those.

**Inputs**: `data/items-all-goethe-faust.json` (streaming)

**Outputs**:
1. `output/dctype_gnd_coverage.csv` — per (mediatype, sector, dc_type_de):
   `count`, `gnd_uri` (first GND match, empty if none), `has_gnd` (bool)
2. `output/dctype_to_gnd_uri.csv` — deduplicated `dc_type_de → gnd_uri` mapping
   (one row per unique dc_type_de; for populating `dnb_uri` in the lookup CSV)
3. Printed summary: per mediatype/sector — total dc:type occurrences, matched count, % coverage

**Implementation notes**:
- `dcType` may be a string or list → normalise to list
- `Concept.prefLabel` may be a string or list → normalise to list; match case-insensitively
- Skip Concepts with `about` in `ddb.vocnet.org/medientyp/` or `ddb.vocnet.org/sparte/`
- Prefer `d-nb.info/gnd/` URIs; if multiple Concepts match a dcType string, take first GND URI
- Mediatype and sector extracted from Concept list filtered by vocnet namespace IRIs
- stdlib only: `json`, `csv`, `pathlib`, `collections`

---

## 4. Files to modify

### Notes (pending)

| File | Action |
|---|---|
| `goethe-faust/notes/plan-goethe-faust-transform.md` | **New** — copy of this plan file (persistent note in the project) |
| `goethe-faust/notes/audio-type-class-mapping.md` | ✅ Added GND URI dispatch note to §3 open questions |
| `goethe-faust/notes/transform-script-plan.md` | Update §2 CSV schema to add `dnb_uri` column; mark phases B–D complete when done |

### Transform pipeline completion

| File | Action |
|---|---|
| `goethe-faust/scripts/count_dctype_gnd_coverage.py` | **New** — Phase B0 (GND URI coverage + mapping export) |
| `goethe-faust/output/dctype_gnd_coverage.csv` | **New** — generated by Phase B0 |
| `goethe-faust/output/dctype_to_gnd_uri.csv` | **New** — generated by Phase B0; source for `dnb_uri` column |
| `goethe-faust/scripts/gen_dctype_class_mapping.py` | **New** — Phase B |
| `goethe-faust/output/lookup_dctype_to_class.csv` | **New** — generated by Phase B |
| `goethe-faust/scripts/sample_type_dispatch.py` | **New** — Phase C |
| `goethe-faust/scripts/transform_edm_to_mocho.py` | **Update** — Phase D (load lookup, dc:type dispatch, WebResource typing) |
| `goethe-faust/scripts/README.md` | Update with new scripts and renames |

---

## 5. Verification

1. All four `*_type2class.json` configs exist and are non-empty
2. Run `gen_dctype_class_mapping.py` → `lookup_dctype_to_class.csv` exists, no TBD IRIs
3. Run `sample_type_dispatch.py` → spot-check: `Zeichnung/sparte006` → `vra:Work`; `Fotografie/sparte005` → `mocho:ImageWork`
4. Run `transform_edm_to_mocho.py` → check stats: `objects_missing_specific_type` reduced for mt002 records
5. Grep NT output: museum Zeichnung record has `vra:Work`, not `mocho:Manifestation`
6. Grep NT output: mt002 WebResource URI has `mocho:ImageObject` + `vra:imageOf`
7. No broken cross-references to old `alignment-plan.md` / `alignment-adr.md` filenames
