# ADR: transform_edm_to_mocho.py — Implementation Decisions

**Date**: 2026-04-14  
**Status**: Accepted  
**Related**: `transform-adr.md` (D0 — design), `transform-props-mapping-adr.md` (property decisions — D6/D7/D8 moved there), `mocho/notes/alignment-ddbedm-mocho-adr.md`

---

## Context

This document records implementation decisions for `transform_edm_to_mocho.py`,
the reference DDB-EDM JSONL → mocho RDF transform. Dispatch architecture and
signal priority are decided in `transform-adr.md` (D0); the decisions here
govern how those design choices are realised in code.

---

## Decision 1: Use JSONL as input, not the NT file

**Decision**: Stream `items-all-goethe-faust.json` (JSONL, one JSON object per
line). The NT file `ddbedm-goethe-faust.nt` is not used.

**Alternatives considered**:
- *NT file*: Load triples from the pre-generated NT and align by predicate IRI.
  Rejected because: (a) the NT was generated from the same JSONL and carries no
  additional information; (b) the alignment table is keyed by `(entity_type,
  json_key)` matching the JSON structure, not by IRI, so NT input would require
  a reverse IRI→json_key lookup that is neither defined nor stable.

**Rationale**: JSONL streams with constant memory, preserves the `(entity_type,
json_key)` lookup key structure, and requires only stdlib `json`. No NT indexing
phase needed.

---

## Decision 2: stdlib only — no rdflib in the transform script

**Decision**: The transform script uses only Python stdlib (`json`, `csv`, `re`,
`collections`, `argparse`, `pathlib`). rdflib is not imported.

**Rationale**: The transform is a data pipeline step, not an ontology processing
step. N-Triples output can be constructed by string formatting. rdflib adds a
non-stdlib dependency and significant startup overhead for a script that runs
over 115k records.

**Scope**: This applies only to `transform_edm_to_mocho.py`. Upstream scripts
that parse OWL or Turtle (`align_ddbedm_to_mocho.py`, `gen_htype_doco_mapping.py`)
continue to use rdflib.

---

## Decision 3: Dispatch signal field paths and htype lookup key

**Decision**: The four dispatch signals are read from the following JSONL paths:

| Signal | JSONL path | Value example | Notes |
|---|---|---|---|
| sector | `provider-info.domains[0]` | `http://ddb.vocnet.org/sparte/sparte001` | Vocnet sparte IRI; `domains[0]` is always the primary sector |
| mediatype | `edm.RDF.WebResource[0].type.resource` | `http://ddb.vocnet.org/medientyp/mt002` | Vocnet medientyp IRI; taken from first WebResource |
| htype | `edm.RDF.ProvidedCHO.hierarchyType` | `"htype_030"` | Literal `htype_code` string; absent if record has no hierarchy type |
| dc_type | `edm.RDF.ProvidedCHO.dcType.$` | `"Fotografie"` | German label; `dcType` is a dict with `$` as text field and `resource` (may be null) |

The EDM path `edm.RDF.Concept[].about` also carries sector and mediatype IRIs but
requires iterating and filtering by prefix — `provider-info.domains[0]` and
`WebResource[0].type.resource` are direct lookups and preferred for performance.

`load_htype_map()` uses the `htype_code` column (e.g. `"htype_030"`) as the lookup
key. Rows where `rdf_type == "pending"` are excluded.

**Rationale**: Corpus inspection confirmed that `ddb:hierarchyType` is an
`owl:DatatypeProperty` whose literal values are `htype_code` strings. Grepping
`items-all-goethe-faust.json` for `"htype_0"` yields exactly 92,957 matches —
equal to the `record_count` for `ProvidedCHO,hierarchyType` in the field
profile. The original draft keyed by `label_en (lowercased)`; this was corrected
when the literal format was confirmed.

`provider-info.domains[0]` and `WebResource[0].type.resource` were confirmed
against `data/items-excerpt-1000.json`: sector returns vocnet sparte IRIs directly;
mediatype returns the medientyp IRI from the `resource` subfield of the `type` dict.
`dcType.$` is the German label text; the `resource` subfield is null for dc:type values.

**Validation script**: `scripts/validate_dispatch.py` reads these four paths per
record, applies the §1.2 dispatch table, and writes `output/dispatch_validation.csv`
with columns `(item_id, sector, mediatype, htype, dc_type, W_class, M_class,
dispatch_rule)`. Intended as Option B (spot-check) before encoding the dispatch
logic in `transform_edm_to_mocho.py` (Option A).

**Pending rows** (16 codes — Monograph, Serial, Article, Annotation, Charter,
Dedication, etc.) have no DoCO or RiC-O class assigned. They fall through the
htype lookup without emitting an additional rdf:type. All ProvidedCHOs still
receive `mocho:Manifestation` as their base type regardless (see D9); pending
htype codes are counted in `objects_missing_specific_type` in stats output.

---

## Decision 4: PhysicalThing.hierarchyType skipped this pass

→ Moved to **`transform-adr.md` D14**.

---

## Decision 5: RDF output format — N-Triples for pipeline, Turtle for hand-authored

**Decision**: Transform output (`mocho-goethe-faust.nt`) and all pipeline
intermediate files use N-Triples (`.nt`). Hand-authored files (ontology,
SPARQL update templates) use Turtle (`.ttl`). N-Quads (`.nq`) if named graph
identity is required.

**Rationale**: N-Triples are one triple per line — grep/awk/stream-friendly,
no parser context, trivial to sort and dedup with Unix tools. The verbosity
(full URIs repeated) is acceptable for machine-processed intermediates.
Turtle prefix compression is valuable for human-readable hand-authored files.

---

## Decision 6: Triple subject keys — IRI correction + value-type dispatch

→ **Moved to `transform-props-mapping-adr.md` D1.**

---

## Decision 7: Creator fan-out — whitelist to Manifestation-level creator property

→ **Moved to `transform-props-mapping-adr.md` D2.** Note: IRI corrected from `rdam:P30263` to `rdam:P30329` "has creator agent of manifestation".

---

## Decision 8: Contributor fan-out — keep dc:contributor as-is

→ **Moved to `transform-props-mapping-adr.md` D3.**

---

## Consequences

- `alignment_ddbedm_mocho.csv` was patched: `dcTermsSubject` `edm_iri` corrected
  from `dc:subject` to `dcterms:subject` (42 rows). If the alignment script is
  re-run, this correction must be reapplied or the `OVERRIDES` dict in
  `align_ddbedm_to_mocho.py` must be extended to handle `dcTermsSubject`
  explicitly.
- Two fields (`creator`, `contributor`) bypass the alignment table entirely.
  Their alignment table rows remain but are unused by the transform script; they
  are still valid for downstream consumers (ISWC paper appendix, second-pass
  scripts).
- `dc:contributor` in the output is not mocho-RDA aligned. A Phase 1b script
  (`link_gnd_agents.py`) will emit typed contributor triples via GND role lookup.
- The transform stats (`transform_stats.json`) will show `contributor` and
  `creator` with zero unmatched-key entries since they are handled before the
  alignment lookup. Stats should record them under a separate `whitelisted_keys`
  counter.
- Every ProvidedCHO gets at least one rdf:type triple (`mocho:Manifestation`).
  Objects with a mapped htype get two rdf:type triples. Objects with a pending
  or absent htype get one. No `edm:ProvidedCHO` rdf:type triples appear in the
  output; verification step 2 should grep for its absence.

---

## Decision 9: mocho:Manifestation as fallback type for ProvidedCHO

**Decision**: `mocho:Manifestation` is the fallback `rdf:type` for any ProvidedCHO not matched by the sector × mediatype dispatch table (`transform-adr.md §1.2`). The `edm:ProvidedCHO` type is not emitted. Where a `hierarchyType` code maps to a DoCO or RiC-O class, that class is accumulated alongside the mediatype class (see D10).

*Note*: the earlier formulation ("unconditionally emitted for every ProvidedCHO") is superseded by `transform-adr.md §1.2`, which assigns domain-specific classes (e.g. `rdac:C10007`, `aco:AudioManifestation`, `vra:Image`, `rico:RecordSet`) per sector × mediatype stratum. `mocho:Manifestation` is emitted only when no stratum matches (~42 records, 0.04% of corpus).

**Rationale**: `edm:ProvidedCHO` is an EDM modelling artefact, not an ontological type. DDB items map to the Manifestation level of the WEMI hierarchy — the carrier as held and provided by an institution. `mocho:Manifestation` is therefore the correct base/fallback type. Domain-specific subclasses (D11, D12) refine this where sector and mediatype allow.

**Alternatives considered**:
- *Keep `edm:ProvidedCHO` as fallback*: Mixes EDM and mocho semantics. Rejected.
- *Omit rdf:type when no stratum matches*: Leaves fallback records untyped. Rejected.
- *Type as mocho:Work instead*: ProvidedCHO represents the carrier level, not the abstract Work. Rejected.

---

## Decision 10: PhysicalThing entities typed via htype lookup, no mocho:Manifestation

**Decision**: `PhysicalThing` entities in the JSONL are archival hierarchy
ancestors of the ProvidedCHO — the finding aid lineage (Tektonik, Bestand,
Gliederung, etc.) stored inline in each record. Each has its own `about` URI
and `hierarchyType`. They are typed via the same htype lookup as ProvidedCHO
but receive **no** `mocho:Manifestation` base type. If `hierarchyType` is
absent or pending, no rdf:type triple is emitted for that entity.

**Background**: Corpus inspection of record `224BB273RJDT6WN7GAIRV4AJ5ES5YPC5`
confirmed the structure. The PhysicalThing array carries the object's ancestor
nodes (e.g. two `htype_031 Gliederung` nodes). These are archival aggregation
containers — `rico:RecordSet` with named individuals — not carried objects.
The DDB UI renders them as the "Verbundene Objekte" hierarchy tree.

**Rationale**: `mocho:Manifestation` is the base type for carried objects
(ProvidedCHO, D9). Archival hierarchy nodes are `rico:RecordSet` / `rico:Record`
/ `rico:RecordPart` depending on htype — a different branch of the mocho type
system. Applying `mocho:Manifestation` to them would conflate the carried object
with its archival containers and produce incorrect SPARQL results.

**Implementation**: `retype_cho()` is renamed to `retype_entities()` and
extended to iterate over both `ProvidedCHO` (single dict) and `PhysicalThing`
(array). ProvidedCHO logic unchanged (D9). PhysicalThing loop: htype lookup →
emit RiC-O class and `rico:hasRecordSetType` where applicable; no Manifestation
assertion; no fallback.

---

## Decision 11: mt002 ProvidedCHO typing — domain-specific dispatch replaces mocho:Manifestation

**Decision**: For mt002 (Photo/Image) records, `retype_entities()` applies a
dc:type × sector dispatch table (`lookup_dctype_to_class.csv`) that assigns
domain-specific classes **instead of** (not in addition to) `mocho:Manifestation`.
The dispatch groups and their target classes are:

| Group | dc:types | Sector | ProvidedCHO rdf:type |
|---|---|---|---|
| A — 2D Artworks | ARTWORK_2D (Zeichnung, Gemälde, Druckgraphik, …) | sparte005, sparte006 | `vra:Work` |
| B — 3D Objects | OBJECTS_3D (Skulptur, Büste, Medaille, …) | any | `vra:Work` |
| C — Photo Works | PHOTO_TYPES (Fotografie, Standfoto, Postkarte, …) | sparte005, sparte006 | `mocho:ImageWork` |
| D — Architecture | ARCHITECTURE (Baudenkmal, Denkmal, Wohnhaus, …) | any | `mocho:ImmovableWork` |
| E — Archive photo | PHOTO_TYPES in sparte001 | sparte001 | *(skip — rico:Record via htype)* |
| Defaults | unmatched | sparte006 | `vra:Work` |
| Defaults | unmatched | sparte003 | `mocho:ImmovableWork` [W] + `mocho:ImageManifestation` [M] |
| Defaults | unmatched | sparte005 | `mocho:ImageWork` |
| F — Default | all remaining | any | `mocho:Manifestation` (D9) |

**WEMI semantics**: Groups A–D assign Work-level classes (`vra:Work`,
`mocho:ImageWork`, `mocho:ImmovableWork`), all encoded in the W slot of
`image_type2class.json`. When a W-slot class is present, `mocho:Manifestation`
is **not** emitted for that ProvidedCHO. The ProvidedCHO is a Work, not a
Manifestation; the Manifestation role is fulfilled by the WebResource
(`mocho:ImageObject`, see D12). Group F retains `mocho:Manifestation` (D9).

**New mocho classes** (manual edit required in `mocho-edit.owl`):
- `mocho:ImageWork rdfs:subClassOf mocho:Work` — photographic artifact as Work
- `mocho:ImmovableWork rdfs:subClassOf mocho:Work` — built heritage fixed in environment
- `mocho:ImageObject rdfs:subClassOf mocho:Manifestation` — digital image carrier (see D12)
- `mocho:ImageManifestation rdfs:subClassOf mocho:Manifestation` — photographic reproduction of an immovable work (sparte003 sector default)

**Rationale**: D9 applied `mocho:Manifestation` uniformly to all ProvidedCHOs,
treating them as carriers. This is correct for library/archival records (text,
audio, video) where the ProvidedCHO is the collected copy. It is incorrect for
museum visual objects: a `Zeichnung` (drawing), `Gemälde` (painting), or
`Fotografie` (photograph) in sparte006 (Museum) or sparte005 (Media Library) is
the creative/physical artifact itself — a Work-level entity in WEMI. The D9
rationale ("the ProvidedCHO represents the object as held and provided — the
carrier level") does not apply when the object held and provided is the original
Work. Sector is a required dimension of the lookup — not just dc:type alone — because
the same dc:type string maps to different classes depending on provenance: `Druck`
in sparte006 (Museum) is a printed artwork (`vra:Work`), but in sparte005 (Media
Library) it is a photographic print (`mocho:ImageWork`); `Fotografie` in
sparte001 (Archive) suppresses the image WEMI class entirely (handled via htype
→ `rico:Record`). Sector defaults handle dc:types that match no named group, with
sparte006 → `vra:Work`, sparte005 → `mocho:ImageWork`, sparte003 → `mocho:ImmovableWork` +
`mocho:ImageManifestation`, others → `mocho:Manifestation`.
Dispatch was derived from `output/config/image_type2class.json` (851
entries, 696 unique dc:types × sector), generated by `gen_image_type2class.py`.

**Implementation**: `retype_entities()` in `transform_edm_to_mocho.py` is
extended with a second dispatch step after htype lookup, gated on `mediatype =
mt002`. Reads `output/config/lookup_dctype_to_class.csv` (generated by
`gen_dctype_class_mapping.py`). W-slot class present → emit W-slot class, skip
`mocho:Manifestation`. M-slot class present → emit M-slot class alongside
`mocho:Manifestation` (accumulation rule, same as D9+D10). No match → D9 fallback.

**Reference**: `notes/image-type-class-mapping.md` §3.1, §3.4.

---

## Decision 12: mt002 WebResources typed as mocho:ImageObject

**Decision**: For mt002 (Photo/Image) records, the target URIs of
`edm:isShownBy` and `edm:hasView` (WebResources) are typed as:

```turtle
<webresource-uri>
    a mocho:ImageObject ;    # digital image carrier (subClassOf mocho:Manifestation)
    a rdac:C10007 ;          # RDA Manifestation class
    rdam:P30001 rdact:1018 ; # has carrier type: online resource
    vra:imageOf <cho-uri> .  # interim link; Phase B: replace with mocho:facsimile
```

- `mocho:ImageObject rdfs:subClassOf mocho:Manifestation` — the digital image file
  is the Manifestation-level carrier of the Work-level ProvidedCHO.
- `rdac:C10007` = `http://rdaregistry.info/Elements/c/C10007` — RDA Manifestation.
- `rdam:P30001 rdact:1018` — has carrier type: online resource
  (`http://rdaregistry.info/termList/RDAct/1018`).
- `vra:imageOf` (`owl:inverseOf vra:hasImage`) — interim WebResource → CHO link.
  Replaced by `mocho:facsimile` in Phase B (follow-up ADR). `mocho:facsimile`
  is defined after Hayes & Warren 2010 `mw:facsimileOf` (p. 74): "The subject is
  a more or less precise re-rendering, reproduction or visual representation of
  the object"; domain `mocho:ImageObject`, range `mocho:ImageWork` / `vra:Work`.

**Rationale**: D11 moves ProvidedCHOs to Work level for mt002. The Manifestation
level must then be represented by the digital carrier. `mocho:ImageObject` fills
this role explicitly, making the WEMI chain complete: `vra:Work` /
`mocho:ImageWork` (Work) ← `vra:imageOf` ← `mocho:ImageObject` (Manifestation).
`vra:Image` was considered but is unreliable for explicit Manifestation dispatch
because its OWL superclass is `schema:CreativeWork` — WEMI-neutral by design but
Work-level by naming convention. A reasoner mapping `schema:CreativeWork →
mocho:Work` would pull `vra:Image` to Work, contradicting the Manifestation
intent. `mocho:ImageObject` has a clean `rdfs:subClassOf mocho:Manifestation`
chain with no ambiguity.

**Property rejected**: `rdam:P30139` ("has expression manifested") was considered
as a Manifestation → Work link. Confirmed wrong: it is Manifestation → Expression.
DDB does not model Expression-level entities. Dropped.

**Scope**: WebResource typing applies to mt002 records only in this phase. Audio,
video, and text WebResources are handled separately (Phase B).

**Reference**: `notes/image-type-class-mapping.md` §3.3.

---

## Decision 13: sparte002 Library htype Work-level dispatch — three htypes resolved

**Decision**: For sparte002 (Library) records, three htype codes receive dual `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" assertions, in addition to any DoCO structural class already assigned:

| htype | DE label | Rationale |
|---|---|---|
| ht003 | Beigefügtes Werk | "Accompanying work" — a separately authored intellectual creation bound with or appended to a main work; independently identifiable in GND |
| ht006 | Aufsatz | Essay or journal article — an independently authored text with its own bibliographic identity; routinely assigned a GND Werk record |
| ht025 | Rezension | Review — an independently authored critical text; has its own GND authority record distinct from the reviewed work |

All three require GND entity linking (`Entity linking: GND Werk`) to connect the ProvidedCHO to its GND Work record via `owl:sameAs` or a mocho link property.

**Pending**: ht008 Beilage (supplement) and ht024 Privilegie (charter/privilege) remain unresolved. Beilage may be independently authored (→ W+M) or a physical insert (→ M only); Privilegie is typically a primary-source legal document whose WEMI level in a library context has not been settled.

**Rationale**: The criterion for Work-level assertion is independent intellectual authorship — whether the entity has its own bibliographic identity and could in principle be assigned a GND Werk record. Structural parts of a containing work (chapter, section, verse, preface, index) do not meet this criterion; they are assigned `rdac:C10007` "Manifestation" only. The dual W+M assertion follows the same pattern as D11 (image domain) but applied to the library/text domain: the DDB ProvidedCHO represents both the intellectual entity (Work) and the carrier held by the institution (Manifestation).

**Reference**: `notes/transform-revised-plan.md` §1.1 (sparte002 Library rows).

---

## Decision 15: mt007 records skipped — no mocho triples emitted

**Decision**: Records where mediatype is `http://ddb.vocnet.org/medientyp/mt007`
(NOT DIGITIZED) are skipped at record ingestion time. No RDF triples are emitted
for these records.

**Rationale**: mt007 records carry no `binaries.binary.@href` — there is no digital
surrogate to describe. They appear in the corpus because the SOLR query filter
`digitalisat=TRUE` does not exclude mt007. Emitting a `mocho:Manifestation` triple
for a physically-only object would misrepresent it as a digital resource in the
knowledge graph. Skipping is the correct response to a known data quality issue at
the extraction boundary.

**Implementation**: Check the mediatype IRI (or code) before entering the main
transform loop; `continue` (skip) if mt007 is detected. Log skipped record count.

**Source**: Confirmed by inspecting `data/items-excerpt-1000.json` — all 356 mt007
records in the sample have no `binaries.binary.@href`. See `transform-adr.md` D1.

---

## Decision 16: mt001 ProvidedCHO typing — three-group dc:type dispatch

**Decision**: For mt001 (Audio) records, `retype_entities()` applies a dc:type
dispatch table (`output/config/audio_type2class.json`) that assigns Manifestation-level
classes to the ProvidedCHO. Unlike mt002 (D11), audio ProvidedCHOs remain at
**Manifestation level** — no W-slot class replaces `mocho:Manifestation` in the
current phase. The dispatch uses a three-group classification:

| Group | Semantics | ProvidedCHO class [M slot] | W slot |
|---|---|---|---|
| A — Musical carriers | dc:type unambiguously names a musical carrier format | `mo:MusicalManifestation` | `mo:MusicalWork` (future) |
| B — Produced audio | dc:type names an authored non-musical audio document | `aco:AudioManifestation` | — |
| C — Generic / speech | dc:type is generic or names spoken-word content | `aco:AudioManifestation` | — |

**Group determination**: Groups are curator-assigned, not derived from a data field.
The group for each dc:type entry is a manual annotation in `audio_type2class.json`
based on the semantics of the dc:type string. The `topic` field in the config
provides secondary context for ambiguous entries (e.g. `Schallfolie` is Group A
because its documented topics are all musical; `Sprechplatte` handles the
non-musical remainder of similar carrier types). Sector is an additional dimension
for entries whose meaning drifts by provenance (e.g. `Magnettonband` → Group B in
sparte004 Research; `Ton` → Group A in sparte006 Museum).

**Vocabulary split**:
- **MO** (Music Ontology) — Group A only. `mo:MusicalManifestation` at [M],
  `mo:MusicalWork` at [W] for future Work-entity generation. MO is music-specific
  and must not be applied to radio broadcasts, lectures, or speech recordings.
- **ACO** (Audio Commons Ontology) — Groups B and C. `aco:AudioManifestation` at [M].
  `aco:AudioExpression` at [E] is noted for Group B (authored audio documents) as a
  future addition when expression-level modelling is in scope; not emitted currently.

**W-slot status**: `mo:MusicalWork` [W] is populated in the config for Group A but
is **not emitted** for the ProvidedCHO by the current transform. It is reserved for
when Work-entity generation is implemented (a separate Work node typed `mo:MusicalWork`
linked to the ProvidedCHO `mo:MusicalManifestation`).

**B vs. C distinction**: Both groups map to `aco:AudioManifestation` in the current
transform. The distinction is semantic, not functional: Group B (produced, authored
audio) is flagged for future `aco:AudioExpression` [E] addition; Group C (generic /
speech) has no anticipated expression-level class.

**Config source**: `output/config/audio_type2class.json` — 24 dc:type entries,
manually annotated. Derived from `scripts/old-config/audio_type2class.json` and
updated with group classifications and WEMI-slot class assignments per
`notes/audio-type-class-mapping.md`.

**Reference**: `notes/audio-type-class-mapping.md` §1–2.

---

## Decision 17: dc:date normalization — compact date expansion and range split

**Decision**: Before emitting `rdam:P30278`, apply two normalizations to each `dc:date` value:

1. **Compact date expansion**: YYYYMMDD strings (8 digits, no separators) are reformatted to ISO 8601: `"18300213"` → `"1830-02-13"`.
2. **Range split**: ISO interval strings of the form `"begin/end"` are split on `/`; two `rdam:P30278` triples are emitted, one per part. Example: `"1915-01-01/1920-12-31"` → `rdam:P30278 "1915-01-01"` + `rdam:P30278 "1920-12-31"`.

Both normalizations apply equally to `dc:issued` values.

**Not in scope**: Role-annotated dates (`"2018 (Fotografische Aufnahme)"`) are emitted as-is. The role string is deferred — it may link to `edm:Event.hasType` but requires a separate decision.

**Corpus basis** (`notes/corpus-analysis.md §2`, 115,432 records): compact dates and range splits together account for ~17% of records with dates. `edm:TimeSpan.begin/.end` (98.2% match rate against `dc:date`) are the structured source of truth; these normalizations align `dc:date` literals to the same form.

**Implementation**: `normalize_date(s)` — detect 8-digit string → reformat; detect `/` → split and return list. Called in `emit_date_triples()` before writing.

---

## Decision 18: Two-stage pipeline for full-corpus scale (27M records)

**Decision**: For the full DDB corpus (27M records), replace the single Python
streaming script with a two-stage pipeline:

1. **Flatten pass** (Python, stdlib): one streaming pass over the JSONL, fan-out
   nested entity arrays into per-entity-type flat JSONL files (`cho.jsonl`,
   `agent.jsonl`, `webresource.jsonl`, `place.jsonl`, `physicalthing.jsonl`,
   `concept.jsonl`, `timespan.jsonl`). No dispatch logic in this pass.

2. **Dispatch + map pass** (DuckDB): for each flat JSONL file, join against the
   lookup CSVs and alignment table using SQL. Assemble N-Triple strings as SQL
   expressions; write directly to `.nt` via `COPY ... TO`. DuckDB reads JSONL and
   CSV natively; joins are vectorized and process 27M rows in minutes on a single
   machine (`pip install duckdb`, no server).

Special-case handlers that require conditional logic (IRI vs. literal dispatch,
GND resolution, dual-emit with class-specific predicates) are implemented as
DuckDB Python UDFs or a thin post-processing pass — not embedded in the SQL.

**Supersedes D2** (stdlib-only) for the full-corpus pipeline. D2 remains in
effect for `transform_edm_to_mocho.py` (reference corpus, rapid iteration).

**Alternatives rejected**:
- *Python multiprocessing*: linear speedup with cores but still slow per-record;
  output merging adds complexity; I/O-bound above ~10 cores.
- *SPARQL CONSTRUCT*: requires loading all data into a triplestore first; SPARQL
  conditional logic is clunky; known to be slow at this scale.
- *Polars/pandas vectorized*: per-record fan-out (one record → many triples of
  variable structure) doesn't fit the DataFrame model naturally; verbose for
  nested arrays.

**Rationale**: Class dispatch and property mapping are joins. DuckDB is a
columnar query engine designed for exactly this workload — large-file joins
against lookup tables — with no server overhead. The flatten pass keeps Stage 2
simple (no `UNNEST` chains on deeply nested structures). The lookup tables already
exist as CSVs; no data migration is needed.

---

## Decision 19: Full-corpus input — sqlite/bufgz sector database

**Decision**: Two input modes exist:
- **POC**: `data/items-all-goethe-faust.json` (JSONL, 115,432 records). Governed by D1.
- **Full corpus**: `s2.sqlite` (`objs` table, `bufgz` column — gzip-compressed cortex JSON, ~27M records). Sector is known from the DB at query time; no per-record sector detection is needed.

**Supersedes D1** for the full-corpus (`s2.sqlite`) path. D1 remains in effect for the POC JSONL path.

**Rationale**: `s2.sqlite` is the production storage format used by `gemea/scripts/py/export_ddb.py`. Reading it directly avoids a JSONL export step. The cortex JSON structure inside `bufgz` is identical to the JSONL records, so all downstream field paths (D3, §1 of `transform-script-plan.md`) apply unchanged.

---

## Decision 20: Named graph naming convention — kebab-case URL paths

**Decision**: Named graph local names follow kebab-case URL path conventions: `ddb-edm`, `mocho`, `work`, `prov`. Full IRIs: `http://gemea.ddb.de/graph/<name>`.

| Graph | IRI | Content |
|---|---|---|
| `ddb-edm` | `…/graph/ddb-edm` | Raw EDM triples — faithful round-trip of the cortex JSON `edm.RDF` payload |
| `mocho` | `…/graph/mocho` | mocho-aligned triples — class dispatch + property mapping |
| `work` | `…/graph/work` | GND Work entity links for W-level ProvidedCHOs (Phase 1b) |
| `prov` | `…/graph/prov` | Two-layer PROV-O provenance per `ddbedm-prov-o-plan.md` |

**Rationale**: Kebab-case is consistent with OpenAPI path conventions and existing GeMeA graph names (e.g. `gnd-enrichment`). The `ddb-edm` graph is emitted as priority #1 — a faithful baseline from which `mocho` and `work` graphs can be re-derived or verified. Separating raw EDM from aligned mocho triples allows independent re-runs of the alignment step without re-ingesting source data.

---

## Decision 21: Debug mode — parquet snapshot + 100-record sample + per-record named files

**Decision**: When `--debug` is passed, the script additionally produces:

1. **Parquet snapshot** (`debug/<sector>-raw.parquet`): all cortex JSON fields before any transform — for DuckDB inspection and field-coverage verification.
2. **100-record sqlite sample** (`debug/<sector>-sample-100.sqlite`): 100 randomly sampled rows from the source DB, same schema — for portable hand-inspection and unit test fixtures.
3. **Per-record named files** (for the 100 sampled records):
   - `debug/<graphname>-<ddb-object-id>.nt` and `.ttl` for each output stream
   - `debug/<ddb-object-id>.jsonld` for the mocho graph only

File naming: `<graphname>` ∈ `{ddb-edm, mocho, work, prov}`; `<ddb-object-id>` is the DDB item identifier string (e.g. `224BB273RJDT6WN7GAIRV4AJ5ES5YPC5`).

**Rationale**: The three debug artifacts serve different inspection needs. The Parquet snapshot enables DuckDB queries across all 100 records (field coverage, value distributions). The sqlite sample is a self-contained fixture for writing unit tests without the full sector DB. The per-record named files allow triple-by-triple inspection and diff between graphs for a single object — the most direct way to verify dispatch and alignment correctness before running at full scale.

---

## Decision 14: Manual curation over automated schema alignment

**Decision**: The alignment table (`alignment_ddbedm_mocho.csv`) and all dispatch
logic (htype lookup, dc:type × sector dispatch, sparte × mediatype class
assignment) were produced by manual curation and explicit decision records (D1–D13),
not by automated schema-matching algorithms [Rahm & Bernstein 2001; Shvaiko &
Euzenat 2013].

**Alternatives considered**:

- *LLM-assisted alignment* [Hertling & Paulheim 2023; Giglou et al. 2023]: Feed
  source JSON keys + sample values + target ontology namespace documentation to an
  LLM and generate `(entity_type, json_key) → predicate IRI` candidate mappings.
  Would have covered approximately 60–70% of the 1:1 property mappings in
  `alignment_ddbedm_mocho.csv` automatically — cases with clear semantic
  correspondences (`prefLabel → skos:prefLabel`, `lat → geo:lat`, `begin →
  schema:startDate`). Cannot produce the conditional class dispatch logic (htype ×
  sparte × mediatype → rdf:type) without domain knowledge of DDB's institutional
  structure and the mocho WEMI model. Useful for bootstrap; insufficient for the
  semantically significant part of the alignment.

- *Instance-based statistical alignment* [Doan et al. 2002; Madhavan et al. 2001]:
  Analyze value distributions per JSON key — IRI vs literal, date format patterns,
  language tags, value overlap with target ontology IRIs — to narrow predicate
  candidates automatically. Good at datatype inference and distinguishing
  IRI-valued from literal-valued properties. Cannot distinguish semantically close
  predicates that share the same datatype (e.g. `rdaa:P50067` date-of-birth vs
  `rdaa:P50068` date-of-death both accept date literals; `rdaw:P10088` vs
  `rico:includesOrIncluded` both accept IRI objects). Requires a human to resolve
  ambiguities among ranked candidates.

- *Rule induction over labeled examples* [Quinlan 1993; Völker & Niepert 2011]:
  Treat the lookup tables as labeled training data and learn the dispatch rules
  (e.g. sparte002 × mt003 × htype → `rdac:C10001 + rdac:C10007`) via a decision
  tree or rule-induction algorithm. Could rediscover the rules already encoded in
  `lookup_htype_doco_rico.csv` and `lookup_dctype_to_class.csv`, and might surface
  coverage gaps or inconsistencies not noticed during manual construction. Not
  applicable before the tables exist; the tables are the training data. Value is
  in post-hoc validation, not in generating the alignment.

**Rationale**: All three automated approaches share a structural precondition
that does not hold here: they assume the target ontology is fixed and complete
before alignment begins [Euzenat & Shvaiko 2013, ch. 2]. mocho is being
co-developed alongside the transformation. New classes (`mocho:ImageWork`,
`mocho:ImmovableWork`, `mocho:ImageObject`) and new properties (`mocho:facsimile`)
were introduced *in response to* patterns discovered in the DDB corpus during
alignment work — the data drives ontology design, not the reverse. An automated
aligner given an incomplete mocho would produce mappings against a moving target,
with no mechanism to signal when the ontology gap itself is the correct resolution
(rather than a nearest-available substitute).

Beyond this precondition failure, the alignment problem has two sub-problems with
different automation profiles even in a stable-ontology scenario. For 1:1 property
mapping (JSON key → predicate IRI), automated approaches are viable and would have
reduced manual effort for the whitelist tables. For conditional class dispatch
(multi-signal decision trees over sector, mediatype, htype, and dc:type), the
rules encode institutional domain knowledge — what it means for a DDB Library
record with htype ht021 (`Monografie`) to be a `rdac:C10001 Work` — that cannot
be derived from schema or ontology definitions alone. The semantically significant
decisions (D9–D13) all fall in this second category. Automated alignment would
have covered the straightforward cases and left the hard ones unsolved.

**Consequence**: The alignment table and dispatch tables are authoritative
artifacts, not derived files. Any re-run of the upstream alignment script
(`align_ddbedm_to_mocho.py`) must not overwrite manual decisions. Patches are
applied via `patch_alignment_inmocho.py` (see §5.1 of `transform-revised-plan.md`)
and tracked in this ADR.

`output/config/lookup_dctype_to_class.csv` is **manually mapped**: each row
(mediatype × sector × dc:type → rdf:type) was authored by hand, informed by
corpus signal coverage (ADR D1 in `transform-adr.md`) and the mediatype-specific
config files (`image_type2class.json`, `video_type2class.json`,
`scripts/old-config/audio_type2class.json`). It is not generated by any script
and must not be overwritten programmatically. The file is pending full verification.
Coverage gaps are tracked via `output/top10_dctype_per_htype.csv`
(script: `scripts/top10_dctype_per_htype.py`).

**References** *(verify before citing in paper)*:

| Key | Details | Confidence |
|---|---|---|
| Rahm & Bernstein 2001 | E. Rahm, P.A. Bernstein. "A survey of approaches to automatic schema matching." *VLDB Journal* 10(4):334–350. | High |
| Shvaiko & Euzenat 2013 | P. Shvaiko, J. Euzenat. "Ontology matching: State of the art and future challenges." *IEEE TKDE* 25(1):158–176. | High |
| Euzenat & Shvaiko 2013 | J. Euzenat, P. Shvaiko. *Ontology Matching* (2nd ed.). Springer. | High — cite ch. 2 for the fixed-target assumption |
| Hertling & Paulheim 2023 | S. Hertling, H. Paulheim. "Olala: Ontology Matching with Large Language Models." *Proc. K-CAP 2023*. | Medium — verify venue and title |
| Giglou et al. 2023 | H.B. Giglou, J. D'Souza, S. Auer. "LLMs4OL: Large Language Models for Ontology Learning." *ISWC 2023*. | Medium — covers ontology learning, not matching directly; verify fit |
| Doan et al. 2002 | A. Doan, J. Madhavan, P. Domingos, A. Halevy. "Learning to map between ontologies on the Semantic Web." *WWW 2002*. | High — instance-based learning for ontology mapping |
| Madhavan et al. 2001 | J. Madhavan, P.A. Bernstein, E. Rahm. "Generic schema matching with Cupid." *VLDB 2001*. | High — statistical/structural schema matching |
| Quinlan 1993 | J.R. Quinlan. *C4.5: Programs for Machine Learning*. Morgan Kaufmann. | High — decision tree rule induction |
| Völker & Niepert 2011 | J. Völker, M. Niepert. "Statistical schema induction." *ESWC 2011*. | Medium — verify this covers ontology rule learning specifically |
