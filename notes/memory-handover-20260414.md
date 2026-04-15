# Session Handover — 2026-04-14

## 1. Session scope

Two projects active: `mocho/` (middle ontology) and `goethe-faust/` (data pipeline POC). Work this session:

1. Built `htype → DoCO/RiC-O` mapping
2. Planned the EDM JSONL → mocho RDF transform script

---

## 2. Files created this session

| File | Description |
|---|---|
| `goethe-faust/output/lookup_htype_doco_rico.csv` | 44 htype codes → DoCO or RiC-O class; columns: `htype_code, label_de, label_en, domain, rdf_type, has_record_set_type, target_vocab, notes` |
| `goethe-faust/output/lookup_htype_doco_rico.json` | Same content as JSON array |
| `goethe-faust/notes/alignment-plan.md` | Approved plan for `transform_edm_to_mocho.py`; see §3–§8 |

---

## 3. htype mapping decisions

- 18 codes → DoCO (library structural types: Section, Chapter, Appendix, Part, Figure, Index, TableOfContents, TextChunk, Preface, Stanza)
- 14 codes → RiC-O (archival types: RecordSet + mocho:/ric-rst: named individuals; Record; RecordPart)
- 12 codes → `pending` (publication types — Monograph, Serial, Article — map to WEMI, not DoCO structural classes)
- All required DoCO classes already in `mocho-odk/imports/doco_terms.txt` — no additions needed
- mocho namespace for named individuals: `https://ise-fizkarlsruhe.github.io/ddbkg/mocho#` (replaces old `ddbo:`)

Key individual mappings (archival, from `miro-htype-rico.pdf`):

| htype | label | rdf_type | has_record_set_type |
|---|---|---|---|
| htype_048 | Tektonik | rico:RecordSet | mocho:Tektonik |
| htype_030 | Bestand | rico:RecordSet | mocho:Bestand, ric-rst:Fonds |
| htype_031 | Gliederung | rico:RecordSet | mocho:Gliederung, ric-rst:Series |
| htype_036 | Bestandsserie | rico:RecordSet | mocho:Bestandsserie, ric-rst:Collection |
| htype_037 | Bestandsklassifikation | rico:RecordSet | mocho:Bestandsklassifikation |
| htype_034 | Archivale | rico:Record | — |
| htype_035 | Teil | rico:RecordPart | — |

---

## 4. Transform script plan

**Script to write**: `goethe-faust/scripts/transform_edm_to_mocho.py`

**Key design decisions:**
- Input: `items-all-goethe-faust.json` (JSONL, not NT) — already per-object, streams with constant memory
- NT file (`ddbedm-goethe-faust.nt`) not used — generated from JSONL, adds no new information
- Alignment lookup key: `(entity_type, json_key)` → matches `alignment_ddbedm_mocho.csv` schema
- Filter: only rows where `in_mocho=True` and `rda_iri` non-empty
- Fan-out accepted: all RDA candidates emitted (dc:contributor → 360, dc:creator → 232); not filtered in POC
- Every ProvidedCHO gets `rdf:type mocho:Manifestation` unconditionally; where `hierarchyType` is present and mapped, also gets the DoCO/RiC-O class as an additional type; no `edm:ProvidedCHO` rdf:type emitted
- EDM-structural predicates skipped silently (per ADR Decision 4)
- stdlib only — no rdflib dependency

**Full plan**: `goethe-faust/notes/alignment-plan.md`

---

## 5. Pending tasks

- [ ] Write `goethe-faust/scripts/transform_edm_to_mocho.py` per `alignment-plan.md`
- [ ] Update `goethe-faust/scripts/README.md` with new script entry
- [ ] Verify output: 1 object per sector (`sec_01`–`sec_04`) × media type (`mediatype_002/003/007/009`)
- [ ] Resolve `lookup_htype_doco_rico.csv` pending entries (12 publication types mapped to WEMI — needs follow-up)

---

## 6. Key reference files

| File | Notes |
|---|---|
| `mocho/notes/alignment-ddbedm-mocho.md` | Entity type inventory; fanout figures; known issues (triple subject key deduplication) |
| `mocho/notes/alignment-ddbedm-mocho-adr.md` | Accepted decisions; D2 (DC→RDA route), D4 (EDM-structural out of scope) |
| `mocho/notes/alignment-ddbedm-mocho-spec.md` | Scope definition; in/out per entity type |
| `goethe-faust/output/alignment_ddbedm_mocho.csv` | 1,271 (entity_type, json_key) → rda_iri rows; primary alignment driver |
| `mocho/output/mapping_dct_to_rda.csv` | Upstream DC→RDA map (980 rows); do not re-derive |

---

## 7. Known issues flagged (for code comments in transform script)

- **Triple subject keys**: ~~deduplication downstream~~ — **resolved**. `alignment_ddbedm_mocho.csv` fixed: `dcTermsSubject` `edm_prefix`/`edm_iri` corrected from `dc:subject` → `dcterms:subject` (42 rows). Transform uses `emit_subject_triples()`: collects unique values from all three keys; dispatches literals → dc:subject RDA candidates, IRIs → dcterms:subject RDA candidates; deduplicates `(pred, obj)` pairs per record.
- **`Event.occurredAt`**: ~~unmatched~~ — **resolved**. Typo `occuredAt` added to `OVERRIDES` in `align_ddbedm_to_mocho.py` → `edm:occurredAt`. `edm_field_profile.json` corrected. Picked up on next alignment re-run.
- **Fan-out**: ~~not filtered~~ — **resolved**. `creator` (464 Work-level candidates) → `rdam:P30263 has creator agent of manifestation` (Manifestation-level, consistent with D9). `contributor` (360 candidates, no generic RDA equivalent) → `dc:contributor` kept as-is. Both short-circuit the alignment table.
- **Alignment CSV error corrected**: `rdam:P30263` was erroneously mapped to `dc:format` with label "has reduction ratio designation" — removed from both `alignment_ddbedm_mocho.csv` and `mocho/output/mapping_dct_to_rda.csv`.

---

## 8. Verified data facts (session 2 — 2026-04-14 continuation)

### 8.1 `hierarchyType` value format

`hierarchyType` in the JSONL is an `owl:DatatypeProperty` literal. Values are **`htype_code` strings** (e.g., `"htype_030"`), not German/English labels.

Verified by: grep for `htype_0` in `items-all-goethe-faust.json` → 92,957 matches, exactly equal to `record_count` for `ProvidedCHO,hierarchyType` in the field profile.

**Plan correction required**: `alignment-plan.md §3.3` `load_htype_map` was drafted with `label_en (lowercased)` as key — **must use `htype_code` instead**. Already applied to `alignment-plan.md`.

### 8.2 Coverage stats

| Fact | Value |
|---|---|
| Total JSONL records | 115,432 |
| Records with `hierarchyType` (ProvidedCHO) | 92,957 (80.5%) |
| Records without `hierarchyType` → fallback `edm:ProvidedCHO` type | ~22,475 |
| PhysicalThing entities with `hierarchyType` | 55,771 (48.3%) |

### 8.3 PhysicalThing.hierarchyType

~~Skipped this pass.~~ **Resolved (ADR D10).** PhysicalThing entities are archival hierarchy ancestors (Bestand, Gliederung, etc.) stored inline in each record — the finding aid lineage. Each has its own `about` URI and `hierarchyType`. `retype_cho()` renamed to `retype_entities()`, extended to handle both entity types: ProvidedCHO gets `mocho:Manifestation` + DoCO/RiC-O (D9); PhysicalThing gets RiC-O only via htype lookup, no `mocho:Manifestation`, no fallback type if htype absent/pending.

### 8.4 Alignment CSV confirmed columns

```
entity_type, json_key, edm_prefix, edm_iri, record_count, coverage_pct,
rda_iri, rda_label, wemi_level, match_method, in_mocho
```

`in_mocho` is a string `"True"` / `"False"` (not a Python bool — compare as string).

### 8.5 Scripts directory (as of session 2)

`goethe-faust/scripts/` contains: `fetch-items.sh`, `fetch-progress.sh`, `summarise_results.py`, `match_objecttypes.py`, `translate_and_plot.py`, `plot_latex_figs.py`, `audit_timespan_coverage.py`, `analyse_years.py`, `build_dataframe.py`, `analyse_items.py`, `visualise_items.py`, `find_missing_items.py`, `analyse_bucket.py`, `extract_view_fields.py`, `extract_view_id_name.py`, `check_isbd_titles.py`, `gen_htype_doco_mapping.py`, `fetch-search-all.py`, `profile_edm_fields.py`, `align_ddbedm_to_mocho.py`, `open_diagram.py`, `README.md`

### 8.6 `ddbedm_1.0.ttl` confirms

`ddb:hierarchyType` is declared as `owl:DatatypeProperty` — values are literals, not IRIs.

### 8.7 Sectors and mediatypes (verified by grep)

**Sectors** — `http://ddb.vocnet.org/sparte/sparte00N` (all 7 present):

| Code | Label | Records |
|---|---|---|
| sparte001 | Archiv | 50,216 |
| sparte002 | Bibliothek | 50,198 |
| sparte003 | Denkmalfach | 111 |
| sparte004 | Mediathek | 1,283 |
| sparte005 | Museum | 4,288 |
| sparte006 | Sonstige | 9,215 |
| sparte007 | Wissenschaftliche Einrichtung | 85 |

**Mediatypes** — `http://ddb.vocnet.org/medientyp/mt00N` (mt004, mt006 absent):

| Code | Label | Records |
|---|---|---|
| mt001 | Audio | 476 |
| mt002 | Photo | 20,228 |
| mt003 | Text | 52,247 |
| mt005 | Video | 96 |
| mt007 | Not Digitized | 42,360 |

Note: old plan used `sec_01–sec_04` / `mediatype_002/003/007/009` notation — both corrected to actual IRI codes.
