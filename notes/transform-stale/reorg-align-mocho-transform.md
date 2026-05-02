# Plan: Organise Alignment + Transformation Notes and Complete the goethe-faust Transform Pipeline

## 0. Context and terminology

**Problem**: Notes on mapping DDB-EDM objects to mocho are spread across two projects
with inconsistent naming. The goethe-faust transform pipeline is also incomplete.

**Terminology decision**:

| Term | Meaning | Where |
|---|---|---|
| **Alignment** | Ontology-level mapping: DDB-EDM property X → mocho/RDA property Y. Corpus-independent, reusable across all DDB corpora. | `mocho/notes/` |
| **Transformation** | ETL pipeline that *applies* the alignment to actual records (DDB-EDM JSONL → mocho RDF). Corpus-specific. | `goethe-faust/notes/` |

The correct framing: *"transform DDB objects from DDB-EDM to mocho, using the alignment rules."*

---

## 1. Current note inventory

### 1.1 mocho/notes/ — Alignment layer (corpus-independent)

| File | Lines | Role | Status |
|---|---|---|---|
| `alignment-ddbedm-mocho.md` | 127 | Working note — POC alignment analysis | Superseded by spec/ADR |
| `alignment-ddbedm-mocho-spec.md` | 140 | POC alignment spec (property → property) | Draft |
| `alignment-ddbedm-mocho-adr.md` | 162 | POC alignment ADR (D1–D5) | Accepted |
| `alignment-ddbsearch-mocho-spec.md` | 323 | Production alignment spec (GeMeA pipeline) | Draft |
| `alignment-ddbsearch-mocho-adr.md` | 234 | Production alignment ADR | Draft |

### 1.2 goethe-faust/notes/ — Transformation layer (POC corpus)

| File | Lines | Role | Status |
|---|---|---|---|
| `alignment-plan.md` | 365 | **Misnamed** — is the transform implementation plan | Approved |
| `alignment-adr.md` | 405 | **Misnamed** — is the transform ADR (D1–D12) | Accepted |
| `transform-pseudocode.md` | 11 | Brief pseudocode sketch | Thin; absorb |
| `transform-script-plan.md` | 430 | Dispatch table plan (Phase A done; B–D pending) | In progress |
| `image-type-class-mapping.md` | 492 | IMAGE dispatch model (D11–D12) | Done |
| `video-type-class-mapping.md` | 105 | VIDEO type class justification | Done |
| `inputs.md` | 60 | Input file descriptions | Done |

---

## 2. Note reorganisation

### 2.1 Renames (goethe-faust/notes/)

| From | To | Reason |
|---|---|---|
| `alignment-plan.md` | `transform-plan.md` | It is a transformation plan, not an alignment plan |
| `alignment-adr.md` | `transform-adr.md` | It is the transform ADR (D1–D12), not an alignment ADR |

Update cross-references in:
- `goethe-faust/.claude/CLAUDE.md`
- `goethe-faust/scripts/README.md` (any references)
- `mocho/notes/alignment-ddbedm-mocho-adr.md` (references goethe-faust alignment-adr)
- `image-type-class-mapping.md` §6 (references alignment-adr.md)

### 2.2 Absorb transform-pseudocode.md

Content (11 lines) is already superseded by `transform-plan.md` and `transform-script-plan.md`.
Delete the file; the pseudocode logic is captured in detail in those two documents.

### 2.3 mocho/notes/ — no renames needed

The `alignment-ddbedm-mocho*` naming is correct: these are ontology alignment notes.
`alignment-ddbedm-mocho.md` (working note) is superseded by the spec and ADR — can be
archived or deleted at the author's discretion. Leave for now.

---

## 3. What is unfinished in the goethe-faust transform

The goethe-faust POC transform (`transform_edm_to_mocho.py`) currently:
- ✅ D1–D10: JSONL streaming, alignment table, htype dispatch, mocho:Manifestation base type
- ✅ D11–D12 (config): `image_type2class.json` updated with new dispatch groups
- ❌ Phase B: `gen_dctype_class_mapping.py` not written → `lookup_dctype_to_class.csv` does not exist
- ❌ Phase C: `sample_type_dispatch.py` not written
- ❌ Phase D: `transform_edm_to_mocho.py` not updated to use the lookup CSV or type WebResources

### 3.1 Phase B — `gen_dctype_class_mapping.py`

Reads all four config JSONs (audio, image, video, general) and writes
`output/config/lookup_dctype_to_class.csv`. Schema from `transform-script-plan.md` §2:

| Column | Description |
|---|---|
| `mediatype` | IRI or `any` |
| `sector` | IRI or `any` |
| `dc_type_de` | German dc:type literal |
| `dc_type_en` | English translation |
| `rdf_type_w` | Work-level class IRI |
| `rdf_type_e` | Expression-level class IRI |
| `rdf_type_m` | Manifestation-level class IRI |
| `rdf_type_i` | Item-level class IRI |
| `source_vocab` | `mo`, `aco`, `vra`, `mocho`, `rico`, `ebucoreplus`, etc. |
| `notes` | from config `notes` field |

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

## 4. Files to modify

### Reorganisation

| File | Action |
|---|---|
| `goethe-faust/notes/alignment-plan.md` | Rename → `transform-plan.md` |
| `goethe-faust/notes/alignment-adr.md` | Rename → `transform-adr.md` |
| `goethe-faust/notes/transform-pseudocode.md` | Delete (absorbed) |
| `goethe-faust/.claude/CLAUDE.md` | Update references |
| `image-type-class-mapping.md` §6 | Update `alignment-adr.md` ref → `transform-adr.md` |
| `mocho/notes/alignment-ddbedm-mocho-adr.md` | Update cross-ref to goethe-faust transform-adr.md |

### Transform pipeline completion

| File | Action |
|---|---|
| `goethe-faust/scripts/gen_dctype_class_mapping.py` | **New** — Phase B |
| `goethe-faust/output/config/lookup_dctype_to_class.csv` | **New** — generated by Phase B |
| `goethe-faust/scripts/sample_type_dispatch.py` | **New** — Phase C |
| `goethe-faust/scripts/transform_edm_to_mocho.py` | **Update** — Phase D (load lookup, dc:type dispatch, WebResource typing) |
| `goethe-faust/scripts/README.md` | Update with new scripts and renames |
| `goethe-faust/notes/transform-script-plan.md` | Mark phases B–D as complete when done |

---

## 5. Verification

1. All four `*_type2class.json` configs exist and are non-empty
2. Run `gen_dctype_class_mapping.py` → `lookup_dctype_to_class.csv` exists, no TBD IRIs
3. Run `sample_type_dispatch.py` → spot-check: `Zeichnung/sparte006` → `vra:Work`; `Fotografie/sparte005` → `mocho:ImageWork`
4. Run `transform_edm_to_mocho.py` → check stats: `objects_missing_specific_type` reduced for mt002 records
5. Grep NT output: museum Zeichnung record has `vra:Work`, not `mocho:Manifestation`
6. Grep NT output: mt002 WebResource URI has `mocho:ImageObject` + `vra:imageOf`
7. No broken cross-references to old `alignment-plan.md` / `alignment-adr.md` filenames
