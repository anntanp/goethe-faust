# ADR: EDM JSONL → mocho RDF Transform (goethe-faust POC)

**Date**: 2026-04-14
**Status**: Accepted
**Related**: `mocho/notes/alignment-ddbedm-mocho-adr.md`, `goethe-faust/notes/alignment-plan.md`

---

## Context

`transform_edm_to_mocho.py` converts the goethe-faust DDB-EDM JSONL corpus
(115,432 records) to mocho-aligned N-Triples. The alignment table
`alignment_ddbedm_mocho.csv` is an intermediate produced by the mocho pipeline;
this document records decisions that govern how the transform script uses — and
in some cases departs from — that table.

Upstream decisions in `mocho/notes/alignment-ddbedm-mocho-adr.md` (D1–D5)
are inherited without modification. Decisions here either extend them or
resolve implementation-level issues discovered during corpus inspection.

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

## Decision 3: htype lookup keyed by `htype_code`, pending rows skipped

**Decision**: `load_htype_map()` uses the `htype_code` column (e.g. `"htype_030"`)
as the lookup key. Rows where `rdf_type == "pending"` are excluded.

**Rationale**: Corpus inspection confirmed that `ddb:hierarchyType` is an
`owl:DatatypeProperty` whose literal values are `htype_code` strings. Grepping
`items-all-goethe-faust.json` for `"htype_0"` yields exactly 92,957 matches —
equal to the `record_count` for `ProvidedCHO,hierarchyType` in the field
profile.

The original draft keyed by `label_en (lowercased)`; this was corrected when
the literal format was confirmed.

**Pending rows** (16 codes — Monograph, Serial, Article, Annotation, Charter,
Dedication, etc.) have no DoCO or RiC-O class assigned. They fall through the
htype lookup without emitting an additional rdf:type. All ProvidedCHOs still
receive `mocho:Manifestation` as their base type regardless (see D9); pending
htype codes are counted in `objects_missing_specific_type` in stats output.

---

## Decision 4: PhysicalThing.hierarchyType skipped this pass

**Decision**: `retype_cho()` handles `ProvidedCHO` only. `PhysicalThing`
entities (55,771 records, 48.3% coverage) also carry `hierarchyType` but are
not retyped in this pass.

**Rationale**: The scope of this POC is the CHO graph. PhysicalThing is an
EDM modelling artefact for physical carrier description; its rdf:type mapping
requires a separate alignment decision (likely CIDOC-CRM or LRMoo). Skipping
it does not affect the correctness of the ProvidedCHO output.

**Consequence**: `PhysicalThing.hierarchyType` will appear in the unmatched
keys stats. This is expected and documented.

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

**Decision**: Three JSON keys carry subject data: `dcSubject`, `dcTermsSubject`,
`dcTermSubject`. These are handled by a dedicated `emit_subject_triples()`
function, not the generic alignment loop.

**Background**: Corpus inspection revealed that `dcTermsSubject` was
incorrectly mapped to `dc:subject` (`http://purl.org/dc/elements/1.1/subject`)
in `alignment_ddbedm_mocho.csv`. The correct IRI is `dcterms:subject`
(`http://purl.org/dc/terms/subject`). This was a derivation error in the
alignment script's IRI resolution step; `dcTermSubject` (note: missing `s`) was
the one correctly resolved to `dcterms:subject` via an explicit `OVERRIDES` entry
in `align_ddbedm_to_mocho.py`. The fix was applied directly to the CSV (42 rows:
`edm_prefix` `dc→dcterms`, `edm_iri` corrected).

**Dispatch logic**:
- Literal value (string or lang-tagged text) → RDA candidates for
  `("ProvidedCHO", "dcSubject")` — i.e. the dc:subject path.
- IRI value (`{"resource": ...}`) → RDA candidates for
  `("ProvidedCHO", "dcTermSubject")` — i.e. the dcterms:subject path.

**Deduplication**: `emit_subject_triples()` collects values from all three keys
and deduplicates `(pred_nt, obj_nt)` pairs in a per-record set before writing.
This prevents duplicate triples when the same value appears under multiple keys
(occurs in ~60% of records).

**Rationale**: `dc:subject` is conventionally used for uncontrolled literals;
`dcterms:subject` for IRI references to controlled vocabulary terms (GND, LCSH,
etc.). Value-type dispatch applies this convention without requiring agent-type
knowledge. The per-record set dedup is cheap (reset each record) and removes
the problem at the source.

---

## Decision 7: Creator fan-out — whitelist to Manifestation-level creator property

**Decision**: `dc:creator` (json_key: `creator`) is mapped to a single RDA
property: `rdam:P30263 has creator agent of manifestation`
(`http://rdaregistry.info/Elements/m/P30263`). The alignment table's 464
Work-level candidates are bypassed.

**Background**: The alignment table produces 464 candidates for `creator`,
all at the Work WEMI level — including highly specific properties such as
"has production company", "has plaintiff corporate body", "has appellee
corporate body". These are correct sub-properties of Work-level creator
properties in the RDA hierarchy but are wrong for a generic `dc:creator` value
where the creator role is unknown.

The choice of WEMI level is determined by D9: since all ProvidedCHOs are typed
as `mocho:Manifestation`, the creator property should be at the Manifestation
level. `rdam:P30263` is present in mocho (confirmed in `mocho-full.owl`).

**Note on alignment CSV**: `rdam:P30263` was found in `alignment_ddbedm_mocho.csv`
under `dc:format` with the wrong label "has reduction ratio designation" — a
DC→RDA map derivation error (P30263 has no semantic relation to dc:format).
The erroneous row was removed from both `alignment_ddbedm_mocho.csv` and the
upstream `mocho/output/mapping_dct_to_rda.csv`.

**Alternatives considered**:
- *Emit all 464*: Semantically very noisy; a Goethe letter would assert
  "has plaintiff corporate body" for the author. Rejected.
- *Use rdaw:P10065 has creator agent of work*: Work-level; inconsistent with
  the Manifestation typing of ProvidedCHO (D9). Rejected.
- *Use mediatype dispatch*: Route to specific properties based on the record's
  mediatype Concept IRI. Adds complexity; correct role remains unknown even
  with mediatype. Rejected for POC.

**Rationale**: `rdam:P30263` is the generic Manifestation-level creator property,
consistent with the `mocho:Manifestation` base type assigned to all ProvidedCHOs
(D9). Specific role properties should be emitted only after GND agent enrichment
(Phase 1b) resolves the creator's function.

---

## Decision 8: Contributor fan-out — keep dc:contributor as-is

**Decision**: `dc:contributor` (json_key: `contributor`) is emitted using the
original `dc:contributor` predicate
(`http://purl.org/dc/elements/1.1/contributor`). No RDA property is used.

**Background**: The alignment table produces 360 candidates for `contributor`,
spread across Expression (293), Manifestation (50), Item (16), and Work (1)
WEMI levels. The single Work-level candidate is "has academic supervisor" —
semantically wrong as a default. The Expression-level candidates are all specific
performer roles (conductor, actor, dancer, etc.). No generic "has contributor
agent" superclass exists in mocho's current import.

**Alternatives considered**:
- *Whitelist generic RDA property*: No suitable candidate found. `P20052` in
  the alignment table is incorrectly mapped as "has recordist agent" (a
  derivation error in the DC→RDA map). Rejected.
- *Emit all 360*: Semantically noisy; a 19th-century correspondence bundle
  would assert "has dancer agent" for each addressee. Rejected.
- *Skip contributor entirely*: Loses the contributor link for 26.2% of records
  until Phase 1b. Rejected in favour of keeping the DC predicate.
- *Mediatype dispatch*: Route to Manifestation-level properties by mediatype
  (e.g. `mt003 Text → rdam:P30328 has contributor agent of text`). Adds
  complexity and is still wrong for mixed-media records. Rejected for POC.

**Rationale**: `dc:contributor` is a valid, well-understood predicate. Keeping
it preserves the contributor link in the output graph without asserting a
specific role that cannot be determined from the DC value alone. The output is
not mocho-RDA aligned for this field, but it is correct and queryable. Phase 1b
GND agent enrichment will replace this with typed RDA role triples.

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

## Decision 9: Every ProvidedCHO is typed as mocho:Manifestation

**Decision**: `retype_cho()` unconditionally emits
`<cho_uri> rdf:type mocho:Manifestation` for every ProvidedCHO. Where a
`hierarchyType` code is present and maps to a DoCO or RiC-O class, that class
is emitted as an additional, more specific rdf:type. The `edm:ProvidedCHO`
fallback type is not emitted.

**Rationale**: `edm:ProvidedCHO` is an EDM modelling artefact describing the
role of the entity within an EDM Aggregation, not an ontological type for the
object itself. In the mocho/WEMI model, DDB items — regardless of media type,
institutional sector, or structural position — represent cultural heritage
objects as provided by an institution, which maps to the Manifestation level of
the WEMI hierarchy. `mocho:Manifestation` is therefore the correct base type
for all ProvidedCHOs.

The DoCO or RiC-O class (where present) is a specialisation of this base type,
describing the structural or archival nature of the object within its
Manifestation. Emitting both types allows SPARQL queries to match either the
general Manifestation class or the specific structural class.

**Alternatives considered**:
- *Keep `edm:ProvidedCHO` as fallback*: Preserves EDM provenance but asserts
  an EDM structural class in the mocho graph. Rejected: mixes EDM and mocho
  semantics in a way that misleads downstream consumers.
- *Omit rdf:type for pending/missing htype*: Leaves ~22,475 records (19.5%)
  with no class. Rejected: untyped nodes are harder to query and do not reflect
  the known WEMI alignment.
- *Type as mocho:Work instead*: A DDB item could be argued to be a Work. Rejected:
  the ProvidedCHO represents the object as held and provided — the carrier level
  — which is Manifestation, not the abstract Work.

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
