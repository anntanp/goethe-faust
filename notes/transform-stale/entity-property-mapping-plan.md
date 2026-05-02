# Plan: Property mapping for all edm.RDF entity types

**Date**: 2026-04-21
**Status**: In progress
**Related**: `goethe-faust/notes/transform-adr.md`, `goethe-faust/notes/entity-property-mapping.md`, `goethe-faust/output/alignment_ddbedm_mocho.csv`

---

## 1. Ground-truth property inventory (full corpus verified)

Verified by running `scripts/profile_edm_fields.py` against all 115,432 records.
Script is correct: `record_count` in output = entity instance count (not record count).

| Entity type | Instances | Actual json_keys (excl. `about`) |
|---|---|---|
| Agent | 422,026 | altLabel, begin, biographicalInformation, date, dateOfBirth, dateOfDeath, dateOfEstablishment, dateOfTermination, end, gender, hasMet, hasPart, identifier, isPartOf, isRelatedTo, name, note, placeOfBirth, placeOfDeath, prefLabel, professionOrOccupation, sameAs, type, wasPresentAt |
| Aggregation | 115,432 | aggregatedCHO, aggregator, dataProvider, dcTermsRights, edmRights, hasView, isShownAt, isShownBy, object, provider |
| Concept | 717,638 | notation, prefLabel |
| Event | 158,407 | P11_had_participant, happenedAt, hasType, **occuredAt** (DDB API typo — one 'r') |
| PhysicalThing | 55,771 | aggregationEntity, hierarchyPosition, hierarchyType, isPartOf, title |
| Place | 118,088 | alt, altLabel, hasPart, isNextInSequence, isPartOf, lat, long, note, prefLabel, sameAs, type |
| ProvidedCHO | 115,432 | aggregationEntity, alternative, contributor, creator, currentLocation, date, dcSubject, dcTermSubject, dcTermsLanguage, dcTermsSubject, dcType, description, edmType, extent, format, hasMet, hasType, hierarchyPosition, hierarchyType, identifier, isPartOf, issued, language, spatial, title |
| TimeSpan | 99,930 | begin, end |
| WebResource | 312,538 | creator, dcTermsRights, edmRights, type |

**Discrepancy vs. `edm_field_profile.json`**: JSON has `occurredAt` (corrected spelling); actual data has `occuredAt` (DDB API typo). The JSON was manually edited — the typo key is what the transform sees.

---

## 2. Context

`alignment_ddbedm_mocho.csv` was built by a generic DC→RDA algorithm without considering entity-type context. Problems for non-ProvidedCHO types:
- WEMI-level candidates assigned to Agent/Place/PhysicalThing properties (wrong ontological level)
- WebResource.creator: 247 Work-level fan-out candidates (same D7 problem as ProvidedCHO.creator)
- WebResource.type: WEMI content-type candidates — value is a MIME type string
- Agent, Place, Concept, Event, TimeSpan: many unmapped properties needing entity-type-appropriate predicates (rdaa:, geo:, skos:, rico:, crm:)

---

## 3. Mapping decisions (per entity type)

### 3.1 Agent (rdaa: namespace)

| Property | Current | Decision |
|---|---|---|
| `prefLabel` | unmapped | → `skos:prefLabel` |
| `altLabel` | unmapped | → `skos:altLabel` |
| `name` | unmapped | → `rdaa:P50102` (has name of person) |
| `identifier` | unmapped | → `owl:sameAs` if IRI, else `rdaa:P50094` |
| `date` | 5 candidates (1 rdaa: correct) | keep `rdaa:P50039` only; set WEMI-level rows in_mocho=False |
| `begin` | unmapped | → `rdaa:P50067` (date of birth / date of establishment) |
| `end` | unmapped | → `rdaa:P50068` (date of death / date of termination) |
| `dateOfBirth` | unmapped | → `rdaa:P50067` |
| `dateOfDeath` | unmapped | → `rdaa:P50068` |
| `dateOfEstablishment` | unmapped | → `rdaa:P50067` |
| `dateOfTermination` | unmapped | → `rdaa:P50068` |
| `gender` | unmapped | → `rdaa:P50116` |
| `biographicalInformation` | unmapped | → `rdaa:P50113` |
| `professionOrOccupation` | unmapped | → `rdaa:P50100` |
| `placeOfBirth` | unmapped | → `rdaa:P50069` |
| `placeOfDeath` | unmapped | → `rdaa:P50070` |
| `note` | unmapped | → `skos:note` |
| `sameAs` | unmapped | → `owl:sameAs` |
| `type` | 11 WEMI-level candidates | set all in_mocho=False (no mocho equivalent) |
| `hasPart`, `isPartOf` | WEMI-level candidates | set all in_mocho=False (not applicable to Agent) |
| `hasMet`, `isRelatedTo`, `wasPresentAt` | unmapped | → defer (EDM/CRM; no mocho equivalent) |

### 3.2 WebResource

| Property | Current | Decision |
|---|---|---|
| `creator` | 247 Work-level candidates | whitelist → `rdam:P30263` (Manifestation-level creator, per D7 pattern) |
| `type` | 11 WEMI content-type candidates | set all in_mocho=False; whitelist → `rdam:P30002` (media type of manifestation) |
| `dcTermsRights` | `rdai:P40048` + `rdam:P30146` | keep both |
| `edmRights` | `rdai:P40048` + `rdam:P30146` | keep both |

### 3.3 Place

| Property | Current | Decision |
|---|---|---|
| `prefLabel` | unmapped | → `skos:prefLabel` |
| `altLabel` | unmapped | → `skos:altLabel` |
| `note` | unmapped | → `skos:note` |
| `sameAs` | unmapped | → `owl:sameAs` |
| `lat` | unmapped | → `geo:lat` (WGS84) |
| `long` | unmapped | → `geo:long` |
| `alt` | unmapped | → `geo:alt` |
| `type` | 11 WEMI-level candidates | set all in_mocho=False |
| `hasPart`, `isPartOf` | WEMI-level candidates | set all in_mocho=False; defer |
| `isNextInSequence` | unmapped | → defer (DDB-internal sequence) |

### 3.4 PhysicalThing (rico: context)

| Property | Current | Decision |
|---|---|---|
| `title` | 28 WEMI-level candidates | keep `rdaw:P10088` only; set others in_mocho=False |
| `isPartOf` | 3 WEMI-level candidates | set all in_mocho=False; whitelist → `rico:isOrWasPartOf` |
| `aggregationEntity` | unmapped | → defer (DDB-internal) |
| `hierarchyPosition` | unmapped | → defer (DDB-internal ordering) |

### 3.5 Aggregation

| Property | Current | Decision |
|---|---|---|
| `dcTermsRights` | `rdai:P40048` + `rdam:P30146` | keep |
| `edmRights` | `rdai:P40048` + `rdam:P30146` | keep |
| all others | EDM-structural | keep as-is (D4) |

### 3.6 TimeSpan

| Property | Current | Decision |
|---|---|---|
| `begin` | unmapped | → `schema:startDate` |
| `end` | unmapped | → `schema:endDate` |

### 3.7 Concept

Emit as `skos:Concept` triples — referenced from ProvidedCHO, Event, Agent, Place.

| Property | Current | Decision |
|---|---|---|
| `prefLabel` | unmapped | → `skos:prefLabel` |
| `notation` | unmapped | → `skos:notation` |
| rdf:type | none | → `skos:Concept` |

### 3.8 Event

| Property | Current | Decision |
|---|---|---|
| `hasType`, `happenedAt`, `occuredAt`, `P11_had_participant` | all unmapped | → defer (require CRM; not in mocho) |

---

## 4. Implementation steps

1. ✅ Write `notes/entity-property-mapping.md` — authoritative mapping table
2. ☐ Write `scripts/patch_alignment_inmocho.py` — sets in_mocho=False for wrong-WEMI-level rows; run against `output/alignment_ddbedm_mocho.csv`
3. ☐ Update `scripts/transform_edm_to_mocho.py` — add whitelists:
   - `WebResource.creator` → `rdam:P30263`
   - `WebResource.type` → `rdam:P30002`
   - `PhysicalThing.isPartOf` → `rico:isOrWasPartOf`
   - New predicates: `geo:lat/long/alt`, `owl:sameAs`, `skos:prefLabel/altLabel/note/notation`, `schema:startDate/endDate`, `skos:Concept` rdf:type for Concept entities
   - Agent whitelisted properties (rdaa:, skos:, owl:sameAs)
4. ☐ Update `notes/transform-adr.md` — new decisions D13+ per entity type

---

## 5. Files to modify

| File | Action |
|---|---|
| `notes/entity-property-mapping.md` | ✅ Written |
| `notes/transform-adr.md` | Add D13–D1N |
| `output/alignment_ddbedm_mocho.csv` | In_mocho corrections via patch script |
| `scripts/patch_alignment_inmocho.py` | New — patch script |
| `scripts/transform_edm_to_mocho.py` | New whitelists |
