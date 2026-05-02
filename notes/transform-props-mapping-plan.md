# ProvidedCHO Property Mapping Plan

**Date**: 2026-05-01
**Status**: In progress
**Related**: `transform-adr.md`, `entity-property-mapping-plan.md`, `entity-property-mapping.md`, `output/alignment_ddbedm_mocho.csv`, `references/ddbedm-cho-properties.csv`

---

## §0 Context

All ProvidedCHOs are typed as `mocho:Manifestation` (ADR D9). Target predicates must therefore be at the Manifestation WEMI level (`rdam:`) where a Manifestation-level RDA property exists. The alignment CSV (`output/alignment_ddbedm_mocho.csv`) provides candidates for each json_key but fans out across all WEMI levels without selecting one — this plan selects one target per property and documents the rationale.

Candidate predicates were drawn from `mocho/output/mapping_dct_to_rda.csv`. For properties with no RDA mapping, the source DC/EDM predicate is retained.

For object-range properties (range is a class, not a literal), this plan names the connected class and points to `entity-property-mapping.md` for the properties of that class.

`creator` (D7) and `contributor` (D8) are already decided in `transform-adr.md`; their sections below summarise those decisions and add open questions.

---

## §1 about

| Field | Value |
|---|---|
| EDM IRI | — |
| Range | `xsd:anyURI` |
| Target | **not a predicate** — subject IRI of the CHO node |

The `about` key is the `@subject` of the CHO resource, not a property to be emitted. IRI form: `http://www.deutsche-digitale-bibliothek.de/item/<id>`.

---

## §2 title

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `title` | `dc:title` | `rdam:P30134` has title of manifestation | Manifestation-level; reject `rdaw:P10088` (Work-level, wrong per D9) |

Range: `rdfs:Literal` (lang-tagged string)

---

## §3 hasMet

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hasMet` | `edm:hasMet` | keep `edm:hasMet` | No mocho/RDA equivalent; EDM structural link |

Range: `edm:Event`

**Connected class**: `edm:Event` — all four Event properties (`hasType`, `happenedAt`, `occuredAt`, `P11_had_participant`) are deferred pending CRM import. See `entity-property-mapping.md §8`.

---

## §4 identifier

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `identifier` | `dc:identifier` | keep `dc:identifier` | No entry in `mapping_dct_to_rda.csv`; future: `rdam:P30004` (has manifestation identifier) if added to mocho |

Range: `rdfs:Literal` (string or array; values often include role annotation in parentheses, e.g. `"GSA 28/752"`, `"urn:nbn:…"`)

---

## §5 hasType

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hasType` | `edm:hasType` | keep `edm:hasType` | No mocho/RDA equivalent |

Range: `skos:Concept` (resource refs — DDB internal IDs or GND/LIDO concept URIs)

**Connected class**: `skos:Concept` → `skos:prefLabel`, `skos:notation`. See `entity-property-mapping.md §7`.

---

## §6 hierarchyType

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hierarchyType` | `ddb:hierarchyType` | **not emitted as predicate** | Consumed by `retype_entities()` → `rdf:type` triples (ADR D3) |

Range (source): `rdfs:Literal` controlled codes, e.g. `htype_035`, `htype_021`
Output: one or more `rdf:type` triples per DoCO/RiC-O lookup table.

---

## §7 dcType

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcType` | `dc:type` | keep `dc:type` | Free-text type label; no controlled vocabulary enforced in source data |

Range: `rdfs:Literal` (lang-tagged, e.g. "Fotoalbum", "Dokument", "text")

Open: if values can be normalised to a vocabulary, promote to `rdam:P30002` (has media type). Uncontrolled in the current corpus — deferred.

---

## §8 description

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `description` | `dc:description` | `rdam:P30137` has note on manifestation | Most generic Manifestation-level note in `mapping_dct_to_rda.csv`; multi-valued |

Range: `rdfs:Literal` (lang-tagged string)

---

## §9 aggregationEntity

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `aggregationEntity` | `ddb:aggregationEntity` | **skip** | DDB-internal grouping flag; no mocho/RDA equivalent |

Range (source): serialised boolean string `"true"` / `"false"`. No triple emitted.

---

## §10 extent

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `extent` | `dc:extent` | keep `dc:extent` | No entry in `mapping_dct_to_rda.csv`; future: `rdam:P30182` (has extent of manifestation) if added to mocho |

Range: `rdfs:Literal` (lang-tagged; physical dimensions or pagination, e.g. "V, 244 S.", "8,5 x 12 x 2,2 cm")

---

## §11 edmType

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `edmType` | `edm:type` | **not emitted as predicate** | Used by mediatype dispatch → `rdf:type` (ADR D11/D12) |

Range (source): uppercase controlled string: `IMAGE`, `TEXT`, `SOUND`, `VIDEO`, `3D`. Not emitted as a triple predicate; drives class assignment for WebResource and the CHO's specific media class. See `image-type-class-mapping.md`.

---

## §12 language

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `language` | `dc:language` | keep `dc:language` | Language is Expression-level in RDA (`rdae:P20006`); applying to a Manifestation node is a WEMI mismatch — deferred until WEMI decomposition |

Range: `rdfs:Literal` (ISO 639-2 string, e.g. `"ger"`)

---

## §13 dcTermsLanguage

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcTermsLanguage` | `dcterms:language` | keep `dcterms:language` | Same WEMI mismatch as §12; links to external LOC URI |

Range: `dcterms:LinguisticSystem` (resource URI, e.g. `http://id.loc.gov/vocabulary/iso639-2/ger`)

**Connected class**: LOC ISO 639-2 authority record — external URI; no mocho properties emitted for it.

---

## §14 dcSubject

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcSubject` | `dc:subject` | via `emit_subject_triples()` (ADR D6) | Literal → RDA alignment candidates for `(ProvidedCHO, dcSubject)`; IRI → promoted to `dcterms:subject` path |

Range: `rdfs:Literal` (literal-primary; some records carry GND URI in `resource` field)

See ADR D6 for full dispatch and deduplication logic.

---

## §15–16 dcTermsSubject / dcTermSubject

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcTermsSubject` / `dcTermSubject` | `dcterms:subject` | `rdaw:P10256` has subject | Two keys, same predicate (D6); dedup by `(pred_nt, obj_nt)` per record |

Range: `skos:Concept` (resource refs — DDB internal IDs or GND URIs)

No Manifestation-level "has subject" exists in RDA. `rdaw:P10256` (Work-level) is semantically appropriate — subject relationships describe intellectual content, not physical carrier — and is consistent with the alignment table.

**Connected class**: `skos:Concept` → `skos:prefLabel`, `skos:notation`. See `entity-property-mapping.md §7`.

---

## §17 isPartOf

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `isPartOf` | `dcterms:isPartOf` | `rdam:P30020` is part of manifestation | Manifestation-level from `mapping_dct_to_rda.csv`; consistent with D9 |

Range: `edm:ProvidedCHO` (resource URI of parent DDB item)

**Connected class**: parent ProvidedCHO → same mapping as this document (recursive).

---

## §18 date

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `date` | `dc:date` | `rdam:P30278` has date of manifestation | Manifestation-level from `mapping_dct_to_rda.csv`; format varies: `"2018 (role)"`, `"18300213"` |

Range: `rdfs:Literal`

---

## §19 hierarchyPosition

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hierarchyPosition` | `ddb:hierarchyPosition` | **skip** | DDB-internal sort key; no mocho/RDA equivalent |

Range (source): zero-padded numeric string, e.g. `"000000000014848"`. No triple emitted.

---

## §20 currentLocation

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `currentLocation` | `edm:currentLocation` | keep `edm:currentLocation` | No mocho/RDA equivalent |

Range: `edm:Place` (resource ref — DDB internal Place ID or GND place URI)

**Connected class**: `edm:Place` → `geo:lat`, `geo:long`, `geo:alt`, `skos:prefLabel`, `skos:altLabel`, `owl:sameAs`. See `entity-property-mapping.md §3`.

---

## §21 issued

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `issued` | `dc:issued` | `rdam:P30278` has date of manifestation | Non-standard DC term; publication year collapses to same predicate as `date` (§18) |

Range: `rdfs:Literal` (lang-tagged literal year string)

Open: if `dc:issued` (publication date) should be distinguished from `dc:date` (general date), use `rdam:P30011` (has date of publication) — pending confirmation that `rdam:P30011` is in mocho.

---

## §22 creator

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `creator` | `dc:creator` | `rdam:P30263` has creator agent of manifestation | D7 whitelist; bypasses 464 Work-level alignment candidates |

Range: `edm:Agent` (may carry GND URI in `resource` + role-annotated literal in `$`)

**Connected class**: `edm:Agent` → `rdaa:` properties (`prefLabel`, `altLabel`, `dateOfBirth`, `sameAs`, …). See `entity-property-mapping.md §1`.

Open: D7 does not specify whether a GND URI in `resource` should cause an `edm:Agent` node to be minted and linked via `rdam:P30263`, or whether a plain literal is emitted. Phase 1b GND enrichment (`link_gnd_agents.py`) is the intended resolution path.

---

## §23 contributor

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `contributor` | `dc:contributor` | keep `dc:contributor` | D8; no generic Manifestation-level contributor property in mocho; 360 fan-out candidates all role-specific |

Range: `edm:Agent` (potential; most values are unlinked literals with role annotation)

**Connected class**: `edm:Agent` (when URI present — rare for contributor). Same as §22.

Open (D8 follow-up — three options):
- (a) mediatype dispatch: whitelist e.g. `rdam:P30328` (has contributor agent of text) for `TEXT` records
- (b) add a generic `rdam:` contributor superclass to mocho imports, then whitelist it
- (c) keep `dc:contributor` until Phase 1b typed GND role triples replace it

Option (c) is the current decision. (a) and (b) remain open for the post-POC pass.

---

## §24 format

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `format` | `dc:format` | keep `dc:format` | Free-text technique/medium strings; `rdam:P30001` (carrier type) and `rdam:P30002` (media type) expect controlled vocab |

Range: `rdfs:Literal` (lang-tagged, e.g. "Kohlezeichnung (?) (Technik)", "Negativ in color, quer")

Open: if values can be normalised to RDA carrier type codes, promote to `rdam:P30001`.

---

## §25 spatial

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `spatial` | `dc:spatial` | keep `dc:spatial` | Not in `mapping_dct_to_rda.csv`; no mocho RDA equivalent; `schema:locationCreated` is an alternative |

Range: `edm:Place` (resource URI — GeoNames or other authority)

**Connected class**: `edm:Place` → same properties as `currentLocation` (§20).

---

## §26 alternative

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `alternative` | `dcterms:alternative` | `rdam:P30131` has abbreviated title | Manifestation-level; from alignment CSV |

Range: `rdfs:Literal` (lang-tagged string)

Open: `rdam:P30128` (has variant title of manifestation) may be semantically more accurate for a generic alternative title; `P30131` implies an abbreviated form specifically. Revisit if corpus analysis shows non-abbreviated alternates.

---

## Summary: transform actions

| json_key | Current predicate | Change to | Status |
|---|---|---|---|
| `title` | `dc:title` | `rdam:P30134` | ☐ update |
| `description` | `dc:description` | `rdam:P30137` | ☐ update |
| `date` | `dc:date` | `rdam:P30278` | ☐ update |
| `issued` | `dc:issued` | `rdam:P30278` | ☐ update |
| `isPartOf` | `dcterms:isPartOf` | `rdam:P30020` | ☐ update |
| `alternative` | `dcterms:alternative` | `rdam:P30131` | ✅ in alignment CSV |
| `hierarchyType` | `ddb:hierarchyType` | no triple (dispatch) | ✅ implemented (D3) |
| `edmType` | `edm:type` | no triple (dispatch) | ✅ implemented (D11/D12) |
| `aggregationEntity` | `ddb:aggregationEntity` | skip | ☐ add skip |
| `hierarchyPosition` | `ddb:hierarchyPosition` | skip | ☐ add skip |
| `creator` | `dc:creator` | `rdam:P30263` | ✅ D7 |
| `contributor` | `dc:contributor` | keep as-is | ✅ D8 |
| all others | — | keep as-is | ✅ no change |

---

## Files to update

| File | Action |
|---|---|
| `scripts/transform_edm_to_mocho.py` | Update 5 predicate strings (title, description, date, issued, isPartOf); add skip for aggregationEntity and hierarchyPosition |
| `notes/transform-adr.md` | New decisions D13–D17 for the 5 changed predicates |
