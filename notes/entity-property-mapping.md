# Entity property mapping: edm.RDF → mocho/RDA/skos

**Date**: 2026-04-20
**Status**: Approved
**Related**: `goethe-faust/notes/transform-adr.md`, `goethe-faust/output/alignment_ddbedm_mocho.csv`

Authoritative per-entity-type property mapping for all 9 `edm.RDF` entity types. Decisions derive from `output/edm_field_profile.csv` (field inventory) + `output/alignment_ddbedm_mocho.csv` (existing alignment). Corrections and additions are noted under each type.

The general transform loop uses the alignment CSV; whitelisted properties bypass it (same pattern as D7–D8 for ProvidedCHO.creator/contributor).

---

## 1. Agent

RDA namespace for agents: `rdaa:` = `http://rdaregistry.info/Elements/a/`

The existing alignment table mapped `Agent.date`, `Agent.hasPart`, `Agent.isPartOf`, `Agent.type` to WEMI-level (Work/Expression/Manifestation) RDA properties — wrong ontological level for an Agent entity. Corrections: keep only `rdaa:P50039` for `date`; set all WEMI-level candidates to `in_mocho=False`.

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `prefLabel` | `skos:prefLabel` | `skos:prefLabel` | Preferred label |
| `altLabel` | `skos:altLabel` | `skos:altLabel` | Variant label |
| `name` | `foaf:name` | `rdaa:P50102` | Has name of person |
| `identifier` | `dc:identifier` | `owl:sameAs` (if IRI) / `rdaa:P50094` (if literal) | Value-type dispatch |
| `date` | `dc:date` | `rdaa:P50039` | Date associated with the person/corporate body; keep only the rdaa: candidate from alignment |
| `begin` | `edm:begin` | `rdaa:P50067` | Date of birth / date of establishment |
| `end` | `edm:end` | `rdaa:P50068` | Date of death / date of termination |
| `dateOfBirth` | `schema:birthDate` | `rdaa:P50067` | |
| `dateOfDeath` | `schema:deathDate` | `rdaa:P50068` | |
| `dateOfEstablishment` | `edm:dateOfEstablishment` | `rdaa:P50067` | Reuse same IRI as dateOfBirth |
| `dateOfTermination` | `edm:dateOfTermination` | `rdaa:P50068` | Reuse same IRI as dateOfDeath |
| `gender` | `schema:gender` | `rdaa:P50116` | Gender of the person |
| `biographicalInformation` | `rdau:P60492` | `rdaa:P50113` | Biographical information |
| `professionOrOccupation` | `schema:hasOccupation` | `rdaa:P50100` | Profession or occupation |
| `placeOfBirth` | `schema:birthPlace` | `rdaa:P50069` | Place of birth |
| `placeOfDeath` | `schema:deathPlace` | `rdaa:P50070` | Place of death |
| `note` | `skos:note` | `skos:note` | General note |
| `sameAs` | `owl:sameAs` | `owl:sameAs` | Authority link (GND, VIAF, etc.) |
| `type` | `edm:type` | ❌ defer | EDM-specific agent type; no mocho equivalent; set all in_mocho=False |
| `hasPart` | `dc:hasPart` | ❌ defer | Not applicable to Agent; set all WEMI candidates in_mocho=False |
| `isPartOf` | `dc:isPartOf` | ❌ defer | Not applicable to Agent; set all WEMI candidates in_mocho=False |
| `hasMet` | `edm:hasMet` | ❌ defer | EDM/CRM; no mocho equivalent |
| `isRelatedTo` | `edm:isRelatedTo` | ❌ defer | EDM/CRM; no mocho equivalent |
| `wasPresentAt` | `edm:wasPresentAt` | ❌ defer | EDM/CRM event link; no mocho equivalent |

**rdf:type**: `rdaa:Agent` or `foaf:Person` / `foaf:Organization` — defer (no `type` key mapped; Agent type not determinable without GND lookup).

---

## 2. WebResource

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `creator` | `dc:creator` | `rdam:P30263` (whitelist) | 247 Work-level fan-out in alignment — same problem as ProvidedCHO.creator (D7); whitelist to Manifestation-level generic creator |
| `type` | `dc:type` | `rdam:P30002` (whitelist) | MIME type string (e.g. "image/jpeg"); WEMI content-type candidates are wrong; whitelist to has media type of manifestation |
| `dcTermsRights` | `dcterms:rights` | `rdam:P30146` + `rdai:P40048` | Keep both existing candidates (terms of use / access conditions) |
| `edmRights` | `edm:rights` | `rdam:P30146` + `rdai:P40048` | Same as above |

**rdf:type**: mt002 records get `mocho:ImageObject + rdac:C10007` (D12 — already implemented).

---

## 3. Place

`geo:` = `http://www.w3.org/2003/01/geo/wgs84_pos#`

Existing alignment has `Place.hasPart`, `Place.isPartOf`, `Place.type` mapped to WEMI-level RDA — wrong for a Place entity. Set all to `in_mocho=False`.

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `prefLabel` | `skos:prefLabel` | `skos:prefLabel` | |
| `altLabel` | `skos:altLabel` | `skos:altLabel` | |
| `note` | `skos:note` | `skos:note` | |
| `sameAs` | `owl:sameAs` | `owl:sameAs` | GeoNames, GND place link |
| `lat` | `geo:lat` | `geo:lat` | WGS84 latitude (decimal string) |
| `long` | `geo:long` | `geo:long` | WGS84 longitude |
| `alt` | `geo:alt` | `geo:alt` | WGS84 altitude |
| `type` | `edm:type` | ❌ defer | Set all WEMI candidates in_mocho=False |
| `hasPart` | `dc:hasPart` | ❌ defer | Set all WEMI candidates in_mocho=False |
| `isPartOf` | `dc:isPartOf` | ❌ defer | Set all WEMI candidates in_mocho=False |
| `isNextInSequence` | `edm:isNextInSequence` | ❌ defer | DDB-internal sequence ordering |

**rdf:type**: `schema:Place` or `geo:SpatialThing` — defer (not currently needed for QLever queries).

---

## 4. PhysicalThing

`rico:` = `http://www.ica.org/standards/RiC/ontology#`  
**Reference**: `mocho/notes/archival-objects.md`

PhysicalThing entities are archival hierarchy containers (Bestand, Gliederung, Akte) — the Tektonik and Findbuch ancestors of the described `ProvidedCHO`. See `archival-objects.md` for the full htype→RiC-O mapping table and the Tektonik/Findbuch structural rules. Existing alignment maps `title` to 28 WEMI-level candidates and `isPartOf` to 3 WEMI-level candidates — right field, wrong level. Narrow to archival-appropriate predicates.

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `title` | `dc:title` | `rdaw:P10088` "has title of work" (whitelist) | Single predicate; set all other WEMI candidates in_mocho=False |
| `isPartOf` | `dc:isPartOf` | `rico:includesOrIncluded` (whitelist) | RecordSet→RecordSet containment per `archival-objects.md` §3; set WEMI candidates in_mocho=False. ⚠️ Earlier drafts used `rico:isOrWasPartOf` (general part-of) — `rico:includesOrIncluded` is the correct RiC-O containment relation for the archival hierarchy. |
| `aggregationEntity` | DDB-internal | ❌ defer | DDB-internal grouping key |
| `hierarchyPosition` | DDB-internal | ❌ defer | DDB-internal sort position |
| `hierarchyType` | DDB-internal | handled by `retype_entities()` | Not in property loop |

**rdf:type**: via `retype_entities()` htype lookup — full mapping in `archival-objects.md` §3. RecordSet nodes also get dual `rico:hasRecordSetType` triples (standard `ric-rst:*` + DDB-specific `vocnet-htype:htXXX`).

---

## 5. Aggregation

EDM-structural properties (`aggregatedCHO`, `aggregator`, `dataProvider`, `hasView`, `isShownAt`, `isShownBy`, `object`, `provider`) remain `in_mocho=False` per ADR D4.

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcTermsRights` | `dcterms:rights` | `rdam:P30146` + `rdai:P40048` | Keep existing mapping |
| `edmRights` | `edm:rights` | `rdam:P30146` + `rdai:P40048` | Keep existing mapping |

---

## 6. TimeSpan

`schema:` = `http://schema.org/`

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `begin` | `edm:begin` | `schema:startDate` | Start of the time span |
| `end` | `edm:end` | `schema:endDate` | End of the time span |

**rdf:type**: `schema:Event` or `time:Interval` — defer.

---

## 7. Concept

Emit as `skos:Concept` triples. Concept entities are referenced from ProvidedCHO (dc:type), Agent, Place, and Event via controlled-vocabulary links — emitting them enables label resolution graph-wide.

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `prefLabel` | `skos:prefLabel` | `skos:prefLabel` | German label; lang-tagged |
| `notation` | `skos:notation` | `skos:notation` | Code (e.g. mediatype/sector code) |

**rdf:type**: `skos:Concept` (emit for all Concept entities).

---

## 8. Event

All four properties (`hasType`, `happenedAt`, `occuredAt`, `P11_had_participant`) require CIDOC-CRM (`crm:`), which is not currently imported in mocho. Defer pending CRM import decision.

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hasType` | `edm:hasType` | ❌ defer | `crm:P2_has_type` |
| `happenedAt` | `edm:happenedAt` | ❌ defer | `crm:P7_took_place_at` |
| `occuredAt` | `edm:occurredAt` | ❌ defer | `crm:P4_has_time-span` |
| `P11_had_participant` | `crm:P11_had_participant` | ❌ defer | `crm:P11_had_participant` |

---

## 9. ProvidedCHO

No changes — fully mapped. See `transform-adr.md` D1–D12 and `alignment_ddbedm_mocho.csv`.

**`edmType` note**: `ProvidedCHO.edmType` (JSON key for `edm:type` on the CHO) carries one of five uppercase EDM type literals (`IMAGE`, `SOUND`, `TEXT`, `VIDEO`, `3D`), mapping directly to the mediatype labels. A five-entry hardcoded lookup resolves these to vocnet IRIs — simpler than scanning `Concept[].about`. The current transform uses the Concept list instead. Not mapped to a mocho output property. See `mocho/notes/mocho-gatherer-adr.md` §7.1 for path details.

---

## Summary: transform implementation

| Entity type | Implementation path | Status |
|---|---|---|
| ProvidedCHO | alignment CSV + retype_entities() | ✅ done |
| WebResource | alignment CSV + retype_entities() (mt002) + **new whitelists** | update needed |
| Agent | alignment CSV corrections + **new whitelists** | update needed |
| PhysicalThing | retype_entities() (htype) + **new whitelists** | update needed |
| Place | **new whitelists** (geo:, skos:, owl:sameAs) | update needed |
| Aggregation | alignment CSV (no changes) | ✅ done |
| TimeSpan | **new whitelists** (schema:startDate/endDate) | update needed |
| Concept | **new whitelist** (emit skos:Concept + prefLabel + notation) | update needed |
| Event | ❌ defer (CRM not in mocho) | deferred |
