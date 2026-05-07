# Transform Future Work

**Date**: 2026-05-02
**Status**: Parking lot
**Related**: `transform-props-mapping-plan.md`, `transform-props-mapping-adr.md`

Items deferred from the current transform implementation. Each section notes the prerequisite and the relevant plan/ADR section.

---

## §1 Typed RDA creator subproperties

**Prerequisite**: GND agent type resolved (person / collective agent / corporate body / family) by `link_gnd_agents.py`.

When agent type is known, replace the generic `rdam:P30329` / `rdaw:P10065` / `rdae:P20053` triples with the typed subproperty:

| WEMI | Person | Collective agent | Corporate body | Family |
|---|---|---|---|---|
| M | `rdam:P30363` | `rdam:P30392` | `rdam:P30421` | `rdam:P30450` |
| W | `rdaw:P10437` | `rdaw:P10484` | `rdaw:P10531` | `rdaw:P10578` |
| E | `rdae:P20389` | `rdae:P20448` | `rdae:P20507` | `rdae:P20566` |

**label_full**:
- `rdam:P30363` — "has creator person of manifestation"
- `rdam:P30392` — "has creator collective agent of manifestation"
- `rdam:P30421` — "has creator corporate body of manifestation"
- `rdam:P30450` — "has creator family of manifestation"
- `rdaw:P10437` — "has creator person of work"
- `rdaw:P10484` — "has creator collective agent of work"
- `rdaw:P10531` — "has creator corporate body of work"
- `rdaw:P10578` — "has creator family of work"
- `rdae:P20389` — "has creator person of expression"
- `rdae:P20448` — "has creator collective agent of expression"
- `rdae:P20507` — "has creator corporate body of expression"
- `rdae:P20566` — "has creator family of expression"

Also requires extending `lookup_class_prop_alignment.csv` with typed creator rows per class.

---

## §2 dc:language / dcterms:language — Expression node dispatch

**Prerequisite**: WEMI decomposition (Expression node minting).

`dc:language` and `dcterms:language` are Expression-level in RDA (`rdae:P20006` "has language of expression"). Currently emitted on the Manifestation node as a WEMI mismatch (ADR D11). When Expression nodes are minted:

1. The presence of a `dc:language` or `dcterms:language` value on a ProvidedCHO **triggers Expression node minting** — an Expression instance must be created and linked to the Manifestation via `rdam:P30139` "has expression manifested".
2. Language triples move to the Expression node: `<expression> rdae:P20006 <LOC-URI>` (or `dc:language` literal as a cross-WEMI handle).
3. The same LOC URI typed as `rdae:C10006` (Expression class) may serve as the Expression node IRI if a language-scoped Expression URI pattern is adopted.

This affects all class dispatch paths, not just RDA — RiC-O would use `rico:hasOrHadLanguage` on the Expression analog in the archival model.

See `transform-props-mapping-plan.md §13–14` and `transform-props-mapping-adr.md D11`.

---

## §3 dc:format → rdam:P30001 carrier type

**Prerequisite**: Controlled vocabulary normalization of `dc:format` values.

Current `dc:format` values are free-text technique/medium strings. If values can be normalized to RDA carrier type codes, promote to `rdam:P30001` "has carrier type".

See `transform-props-mapping-plan.md §24`.

---

## §4 dc:issued → rdam:P30011 date of publication

**Prerequisite**: Confirm `rdam:P30011` is present in mocho imports.

Currently `dc:issued` collapses to `rdam:P30278` "has date of manifestation" (same as `dc:date`). If distinction between general date and publication date is needed, use `rdam:P30011` "has date of publication" for `issued`.

See `transform-props-mapping-plan.md §21`.

---

## §5 dcterms:alternative → rdam:P30128 variant title

**Prerequisite**: Corpus analysis of `dcterms:alternative` values.

Currently mapped to `rdam:P30131` "has abbreviated title". If corpus shows non-abbreviated variant titles, switch to `rdam:P30128` "has variant title of manifestation".

See `transform-props-mapping-plan.md §26`.

---

## §6 dc:contributor — typed RDA role properties

**Prerequisite**: GND role resolution.

Currently kept as `dc:contributor`. Options once GND roles are available:
- (a) mediatype dispatch: `rdam:P30328` "has contributor agent of text" for TEXT records
- (b) add generic `rdam:` contributor superclass to mocho imports
- (c) typed role triples from GND `gnd:professionOrOccupation`

See `transform-props-mapping-plan.md §23`.

---

## §7 dc:format — KB linking and controlled-vocab dispatch

**Prerequisite**: Corpus analysis of `dc:format` values + controlled vocabulary normalisation.

`dc:format` values are free-text technique/medium strings (e.g. "Kohlezeichnung (?) (Technik)", "Negativ in color, quer"). All RDA candidates (`rdam:P30001` carrier type, `rdam:P30002` media type, `rdam:P30208` base material) and all vocab-specific candidates (`vra:material`) **require controlled vocabulary objects** — not applicable to raw literals.

Two paths once prerequisite is met:

1. **KB linking**: normalise dc:format labels to GND, Getty AAT, or AAT-mapped RDA vocabulary terms. Emit `<cho> dcterms:format <kb-uri>` + Concept stub analogous to `dcType` (§15). Target KBs: GND-Sachbegriff (technique terms), Getty AAT `Materials` facet.

2. **Class-specific dispatch** (after KB linking): once URI objects are available, promote to class-specific predicate:
   - `rdac:C10007`, `mocho:Manifestation` → `rdam:P30208` "has base material of manifestation"
   - `vra:Image`, `vra:Work` → `vra:material`
   - `rico:Record*` → `rico:hasOrHadProductionTechniqueType` (if property exists in RiC-O imports)

See `transform-props-mapping-plan.md §18`.

---

## §8 dc:extent — structured parse and domain-specific property dispatch

**Prerequisite**: Regex-based pattern classifier (pagination / dimensions / digital) + unit normalisation.

Current treatment emits `<cho> dc:extent "..."` as a plain literal. 95,808 values are all literals; pattern breakdown: 47.6% pagination, 29.1% dimensions, 23.2% other (see `notes/corpus-analysis.md §4`).

Once values are parsed, dispatch by pattern and target class:

| pattern | RDA (Manifestation) | VRA |
|---|---|---|
| pagination | `rdam:P30182` "has extent of manifestation" | — |
| dimensions | `rdam:P30169` "has dimensions" | `vra:measurementsSet` |
| still image dimensions | `rdam:P30171` "has dimensions of still image" | `vra:measurementsSet` |
| file size / digital | `rdam:P30183` "has file size" | — |

VRA Core 4 `vra:measurementsSet` supports typed structured measurements (height, width, depth, diameter) with explicit value and unit fields — preferable to a free-text literal for museum/image records (`vra:Image`, `vra:Work`).

See `transform-props-mapping-plan.md §19`.

---

## §9 dc:description — NER enrichment for Museum and Monument Preservation sectors

**Prerequisite**: Corpus analysis of description text length by sector (see `notes/corpus-analysis.md §5`).

Monument Preservation (mean 3,275 chars, median 1,863) and Museum (mean 321, median 188) have substantially longer free-text descriptions than other sectors. These are candidates for NER-based enrichment to extract named entities (persons, places, organisations, dates, materials) and link them to GND/GeoNames/Getty authority records.

Proposed pipeline:

1. **Filter**: select records where `sector ∈ {Museum, Monument Preservation}` and `len(description) > threshold` (e.g. 100 chars).
2. **NER**: run a multilingual NER model (e.g. `xlm-roberta-large` fine-tuned on German heritage text) to tag PER, LOC, ORG, DATE, MATERIAL spans.
3. **Linking**: resolve tagged spans against GND (persons, places, organisations), GeoNames (places), Getty AAT (materials/techniques) via lobid-gnd and AAT SPARQL.
4. **Emit**: for each resolved entity, add triples alongside the description literal:
   - PER → `dc:subject <gnd-person-uri>` or typed `rdam:P30327` "has subject agent"
   - LOC → `dc:spatial <geonames-uri>` (if place of creation/use context)
   - ORG → `dc:subject <gnd-org-uri>`
   - MATERIAL → `vra:material <aat-uri>` / `rdam:P30208`

See `notes/corpus-analysis.md §5`, `notes/nlp-tasks.md` (GeMeA NER decisions), `transform-props-mapping-plan.md §8`.

---

## §10 edm:Agent — domain-specific gndo class dispatch

**Prerequisite**: GND agent type resolved (`gndo:DifferentiatedPerson`, `gndo:CorporateBody`, `gndo:ConferenceOrEvent`, `gndo:Family`) by `link_gnd_agents.py` (GeMeA Phase 1b).

Currently all `edm:Agent` nodes are typed as `mocho:Agent` and properties are emitted under a single mapping row (D13, `transform-props-mapping-adr.md`). Once agent type is known, the `mocho:Agent` stub rows in `lookup_class_prop_alignment.csv` should be split into type-specific rows and the following domain mismatches corrected:

**1. Date properties — type dispatch**

| Property | Current | Correct domain |
|---|---|---|
| `gndo:dateOfBirth` / `gndo:dateOfDeath` | emitted on all agents | `gndo:DifferentiatedPerson` only |
| `gndo:dateOfEstablishment` / `gndo:dateOfTermination` | emitted on all agents | `gndo:CorporateBody`, `gndo:ConferenceOrEvent` only |
| `edm:begin` | passthrough | → `gndo:dateOfBirth` (Person) or `gndo:dateOfEstablishment` (CorporateBody/Event) |
| `edm:end` | passthrough | → `gndo:dateOfDeath` (Person) or `gndo:dateOfTermination` (CorporateBody/Event) |

**2. Label properties — type-specific gndo name properties**

| Property | Current | Target |
|---|---|---|
| `skos:prefLabel` | passthrough | → `gndo:preferredNameForThePerson` / `gndo:preferredNameForTheCorporateBody` etc. |
| `foaf:name` | passthrough | → same as above (gndo preferred name, type-specific) |

**3. Other domain-restricted properties**

| Property | Correct domain |
|---|---|
| `gndo:gender` | `gndo:DifferentiatedPerson` only |
| `gndo:placeOfBirth` / `gndo:placeOfDeath` | `gndo:DifferentiatedPerson` only |
| `gndo:professionOrOccupation` | `gndo:DifferentiatedPerson`, `gndo:Family` only |

**Implementation**: extend `lookup_class_prop_alignment.csv` with rows keyed by gndo subclass instead of `mocho:Agent`; update `gen_agent_alignment_rows.py` to generate the split rows; retire the `mocho:Agent` stub rows.

See `transform-props-mapping-adr.md` D13.

---

## §11 Linking to internal Expression KB

**Prerequisite**: Expression node minting (§2).

When Expression nodes are minted, language becomes an additional lookup dimension alongside title and creator. The GND Werk lookup table (see `transform-revised-plan.md §1.2`) covers Work-level linking; the Expression KB extends this with language to identify distinct expressions of the same Work.

Expression lookup key: `(dc:title, dc:creator, dc:language)` — Work title + creator + language of expression.

| Field | Source path | Role |
|---|---|---|
| `dc:title` / `rdaw:P10088` | Work-level title | primary key |
| `dc:language` / `rdae:P20006` | language of expression | expression-discriminating dimension |
| `dc:creator` (URI or `last, first` literal) | GND URI or normalized name | creator key |
| `dc:date` | expression date/version | secondary discriminator (optional) |

Two records sharing the same (title, creator, language) tuple are candidate expressions of the same Work. Deduplication and URI assignment for Expression nodes depends on this lookup.

See `transform-props-mapping-plan.md §13–14` and `transform-props-mapping-adr.md D11`.

---

## §12 Linking vra:Work and mocho:ImageWork to ArtKB and Wikidata

**Prerequisite**: Work-level URI assignment (werk_staging populated; GND Werk lookup complete for §1.2 classes).

`vra:Work` (ht015 Illustration, ht019 Karte, sparte005/mt002 Image) and `mocho:ImageWork` are currently written to N-Quads and DuckDB werk_staging but have no external authority links. Two target KBs:

| KB | Scope | Link predicate |
|---|---|---|
| ArtKB | Art works, images, visual objects (German heritage focus) | `owl:sameAs` or `skos:exactMatch` |
| Wikidata | Broad coverage; Q-items for artworks, maps, photographs | `owl:sameAs` or `skos:exactMatch` |

**Lookup strategy**: title + creator + date tuple → KB entity lookup, analogous to GND Werk lookup in `link_gnd_works.py`. Key fields from werk_staging: `dc_title`, `creator_uris`, `dc_created`.

**Emit**: for each resolved match, add to the mocho named graph:
```
<work-uri> owl:sameAs <artkb-uri> .
<work-uri> owl:sameAs <wikidata-uri> .
```

**Open questions**:
- ArtKB API / SPARQL endpoint availability and query interface
- Wikidata: use `wikidata:P180` (depicts) or direct work Q-item match?
- Confidence threshold for string-match vs. exact-match linking

---

## §13 QLever text-entity link files for `ql:contains-word` support

**Prerequisite**: N-Quads output from the transform pipeline (any run).

QLever's `ql:contains-word` / `ql:has-word` predicates require the text index to be built with entity-to-text-record links. The `-W` flag (`--text-words-from-literals`) builds a word vocabulary from literals but does NOT create these links. The result: `ql:contains-word "word"` finds text records but their internal IDs cannot be joined back to KG entities via triple patterns or `ql:contains-entity`.

To enable `ql:contains-word` queries against the KG, the index must be rebuilt with a docstrings file (`-d`) that maps entity IRIs to their associated text. Two files are required by `qlever-index`:

| File | Format | Content |
|---|---|---|
| words file (`-w`) | `word\tentity_IRI\tdoc_id\tscore\n` (one row per word) | tokenised literal values per entity |
| docs file (`-d`) | `doc_id\tentity_IRI\tfull_text\n` | full literal text per entity |

**Generation approach**: post-process the N-Quads output. For each triple `<subject> <predicate> <literal>` where `<predicate>` is a text-searchable property (at minimum `dc:title`, `dc:description`, `dc:subject`):

1. Emit one docs-file row: `doc_id → subject IRI → concatenated literal values`
2. Emit one words-file row per token (whitespace-tokenised, lowercased) in the literal

**Script location**: `scripts/transform/gen_qlever_text_files.py`

**Affected properties** (initial set):
- `dc:title`, `dcterms:title`, `rdam:P30156`
- `dc:description`
- `dc:subject` (literal values only)
- `dc:creator`, `dc:contributor` (literal values only — GND-linked values are entity IRIs)

**Re-indexing**: rebuild `docker-compose.qlever.yml` to pass `-d` and `-w` alongside (or instead of) `-W`.

**Why it matters**: once these files exist, `FILTER(CONTAINS(...))` in Query 3 of the ISWC paper can be replaced with `ql:contains-word`, giving an order-of-magnitude speedup on large corpora and enabling ranked retrieval via BM25 (`--bm25-k`/`--bm25-b` flags). Also unblocks the "KG-grounded retrieval" use case in Section 5.3 of the paper.
