# Transform revised plan: EDM → mocho N-Triples

**Date**: 2026-04-29  
**Status**: In progress  
**Supersedes**: `transform-plan.md`, `transform-script-plan.md`, `transform-edm2mocho-plan.md`, `entity-property-mapping-plan.md`  
**Related**: `transform-adr.md` (D0), `transform-script-adr.md` (D1–D14), `entity-property-mapping.md`, `transform-writeup.md`

---

## 1. Pipeline overview

Input: `data/items-all-goethe-faust.json` (115,432 records, JSONL).  
Output: `goethe-faust-mocho.nt` (N-Triples).  
Script: `scripts/transform_edm_to_mocho.py`.

### 1.1 ProvidedCHO class assignment

Signal priority per sector × mediatype is corpus-driven (see `transform-adr.md` D1;
source: `output/dispatch_signal_ratio.csv`). mt007 (NOT DIGITIZED) records are
**skipped** — no mocho triples are emitted. These records carry no binary href and
were incorrectly included by the SOLR query (digitalisat=TRUE flag does not exclude
mt007). For all other mediatypes, the two-signal coverage table in D1 determines
which signal fires first:

- **sparte001 Archive, sparte002 Library** — htype fires first (htypes used heavily;
  htype-only records would be lost under dc:type-first). dc:type is applied as a
  secondary layer, limited to the top-10 dc:types per stratum (D2 annotation).
- **sparte003–007** — dc:type only; htype absent across all records in these sectors.

**Definitive htype list**: `data/ddbedm/ddbedm-htype.csv` is the authoritative
enumeration of all DDB htype codes (`htype_001`–`htype_056`), with German and
English labels and vocnet URIs (`http://ddb.vocnet.org/hierarchietyp/htXXX`).
Use this file as the single source of truth for htype code ↔ label lookups.



Signals checked in priority order: htype → (sector × mediatype) → dc:type. `*` = any value, `—` = not applicable.  
Prefixes: `vocnet-htype: <http://ddb.vocnet.org/hierarchietyp/>`, `ric-rst: <https://www.ica.org/standards/RiC/RiC-O_1-1.html#>`

**sparte001 and sparte002 — two-layer typing**: For Archive and Library records, htype fires first and determines the primary structural class (`rico:*` for sparte001; `doco:*` or `rdac:C10001/C10007` for sparte002). The mediatype then adds a domain-specific class on top — `aco:AudioManifestation`, `mocho:ImageManifestation`, `ec:MediaResource`, etc. — regardless of whether an htype was matched. The two layers are independent and cumulative: a Library audio record with htype ht022 Musik gets `mo:MusicalWork` + `rdac:C10007` (from htype) and `mo:MusicalManifestation` (replaces `aco:AudioManifestation` when `mo:MusicalWork` is present). For sparte001 mt007 Not Digitized, no mediatype class is added (no digital carrier exists).

| sparte | mediatype | htype | dc:type | Domain class | WEMI | Entity linking | Source |
|---|---|---|---|---|---|---|---|
| sparte001 Archive | * | ht048 Tektonische Sammlung | — | `rico:RecordSet` + `ric-rst:Collection` + `vocnet-htype:ht048` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht037 Bestand Klassifikation | — | `rico:RecordSet` + `ric-rst:Collection` + `vocnet-htype:ht037` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht036 Bestandsserie | — | `rico:RecordSet` + `ric-rst:Collection` + `vocnet-htype:ht036` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht030 Bestand | — | `rico:RecordSet` + `ric-rst:Fonds` + `vocnet-htype:ht030` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht031 Gliederung | — | `rico:RecordSet` + `ric-rst:Series` + `vocnet-htype:ht031` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht032 Serie | — | `rico:RecordSet` + `ric-rst:Series` + `vocnet-htype:ht032` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht033 Unterserie | — | `rico:RecordSet` + `ric-rst:Series` + `vocnet-htype:ht033` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht034 Archivale | — | `rico:Record` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | * | ht035 Teil | — | `rico:RecordPart` | — | — | `output/config/lookup_htype_doco_rico.csv`, `mocho/notes/archival-objects.md` |
| sparte001 Archive | mt001 Audio | — | dc:type | dc:type determines class: Group A musical → `mo:MusicalManifestation`; Groups B/C non-musical → `aco:AudioManifestation`. Both added alongside htype-derived `rico:*`. | M | — | `notes/audio-type-class-mapping.md` |
| sparte001 Archive | mt002 Photo | — | — | `mocho:ImageManifestation` (also added alongside htype-derived `rico:*`) | M | — | — |
| sparte001 Archive | mt003 Text | — | — | `mocho:Manifestation` (also added alongside htype-derived `rico:*`; not `rdac:C10007` — archival text is not necessarily literary) | M | — | `notes/transform-script-adr.md` D9 |
| sparte001 Archive | mt005 Video | — | — | `ec:MediaResource` (also added alongside htype-derived `rico:*`) | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte001 Archive | mt007 Not Digitized | — | — | htype dispatch only; no media-specific class (no digital carrier) | — | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht001 Abschnitt | — | `doco:Section` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht002 Anhang | — | `doco:Appendix` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht003 Beigefügtes Werk | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht004 Annotation | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht005 Anrede | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht006 Aufsatz | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht007 Band | — | `doco:Part` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht008 Beilage | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht009 Einleitung | — | `doco:Section` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht010 Eintrag | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht011 Faszikel | — | `doco:Part` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht012 Fragment | — | `doco:TextChunk` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht013 Handschrift | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `notes/transform-revised-plan.md` §1.1 |
| sparte002 Library | mt003 Text | ht014 Heft | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht015 Illustration | — | `doco:Figure` + `rdac:C10007` "Manifestation" + `mocho:ImageWork` | M+W | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht016 Index | — | `doco:Index` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht017 Inhaltsverzeichnis | — | `doco:TableOfContents` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht018 Kapitel | — | `doco:Chapter` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht019 Karte | — | `doco:Figure` + `rdac:C10007` "Manifestation" + `mocho:ImageWork` | M+W | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht020 Mehrbändiges Werk | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht021 Monografie | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht022 Musik | — | `rdac:C10001` "Work" + `mo:MusicalWork` + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht023 Fortlaufendes Sammelwerk | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht024 Privilegie | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht025 Rezension | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht026 Text | — | `doco:TextChunk` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht027 Vers | — | `doco:Stanza` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht028 Vorwort | — | `doco:Preface` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht029 Widmung | — | `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht044 Zeitung | — | `rdac:C10001` "Work" + `rdac:C10007` "Manifestation" | W+M | GND Werk | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht045 Jahrgang | — | `doco:Part` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht046 Monat | — | `doco:Part` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt003 Text | ht047 Tag | — | `doco:Part` + `rdac:C10007` "Manifestation" | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte002 Library | mt001 Audio | — | — | `aco:AudioManifestation` (also added alongside htype-derived class; use `mo:MusicalManifestation` instead if htype = ht022 → `mo:MusicalWork`) | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte002 Library | mt002 Photo | — | — | `mocho:ImageManifestation` (also added alongside htype-derived class) | M | — | `notes/image-type-class-mapping.md` §3.1 |
| sparte002 Library | mt005 Video | — | — | `ec:MediaResource` (also added alongside htype-derived class) | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte002 Library | mt007 Not Digitized | — | — | htype-derived class; `rdac:C10007` "Manifestation" if no htype | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte003 Monument | mt002 Photo | — | — | `mocho:ImmovableWork` | W | — | — |
| sparte003 Monument | mt003 Text | — | — | `mocho:ImmovableWork` + `rdac:C10007` "Manifestation" | W+M | — | — |
| sparte003 Monument | mt001 Audio | — | — | `mocho:ImmovableWork` + `aco:AudioManifestation` | W+M | — | — |
| sparte003 Monument | mt005 Video | — | — | `mocho:ImmovableWork` + `ec:MediaResource` | W+M | — | — |
| sparte003 Monument | mt007 Not Digitized | — | — | `mocho:ImmovableWork` | W | — | — |
| sparte004 Research | mt001 Audio | — | — | `aco:AudioManifestation` | M | — | ⚠ check dc:type values |
| sparte004 Research | mt002 Photo | — | dc:type match | dc:type dispatch via `image_type2class.json` (same as sparte005/006 — `vra:Work`, `mocho:ImmovableWork`, etc.) | W or M | — | `output/config/image_type2class.json` |
| sparte004 Research | mt002 Photo | — | unmatched | `mocho:ImageManifestation` | M | — | — |
| sparte004 Research | mt003 Text | — | — | htype-derived class (same dispatch as sparte002); `rdac:C10007` "Manifestation" if no htype | M | — | ⚠ check dc:type values |
| sparte004 Research | mt005 Video | — | — | `ec:MediaResource` | M | — | ⚠ check dc:type values |
| sparte004 Research | mt007 Not Digitized | — | — | `mocho:Manifestation` | M | — | ⚠ check dc:type values |
| sparte005 Media | mt001 Audio | — | — | `aco:AudioManifestation` | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte005 Media | mt005 Video | — | — | `ec:MediaResource` | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte005 Media | mt002 Photo | — | 2D Artworks (Zeichnung, Gemälde …) | `vra:Work` | W | — | `notes/image-type-class-mapping.md` §3.1.1, `output/config/lookup_dctype_to_class.csv` |
| sparte005 Media | mt002 Photo | — | Photo Works (Fotografie, Standfoto …) | `mocho:ImageWork` | W | — | `notes/image-type-class-mapping.md` §3.1.3, `output/config/lookup_dctype_to_class.csv` |
| sparte005 Media | mt002 Photo | — | Architecture (Baudenkmal …) | `mocho:ImmovableWork` | W | — | `notes/image-type-class-mapping.md` §3.1.5, `output/config/lookup_dctype_to_class.csv` |
| sparte005 Media | mt002 Photo | — | unmatched | `mocho:ImageWork` | W | — | `notes/image-type-class-mapping.md` §3.1 |
| sparte006 Museum | mt002 Photo | — | 2D Artworks (Zeichnung, Gemälde …) | `vra:Work` | W | — | `notes/image-type-class-mapping.md` §3.1.1, `output/config/lookup_dctype_to_class.csv` |
| sparte006 Museum | mt002 Photo | — | 3D Objects (Skulptur, Büste …) | `vra:Work` | W | — | `notes/image-type-class-mapping.md` §3.1.2, `output/config/lookup_dctype_to_class.csv` |
| sparte006 Museum | mt002 Photo | — | Photo Works (Fotografie, Standfoto …) | `mocho:ImageWork` | W | — | `notes/image-type-class-mapping.md` §3.1.3, `output/config/lookup_dctype_to_class.csv` |
| sparte006 Museum | mt002 Photo | — | Architecture (Baudenkmal …) | `mocho:ImmovableWork` | W | — | `notes/image-type-class-mapping.md` §3.1.5, `output/config/lookup_dctype_to_class.csv` |
| sparte006 Museum | mt002 Photo | — | unmatched | `vra:Work` | W | — | `notes/image-type-class-mapping.md` §3.1 |
| sparte006 Museum | * | — | — | `frbr:Manifestation` | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte004/007 | * | — | — | `mocho:Manifestation` | M | — | `notes/transform-script-adr.md` D9 |
| * | * | — | — | `mocho:Manifestation` (D9 fallback) | M | — | `notes/transform-script-adr.md` D9 |

For `rico:RecordSet` rows, `rico:hasRecordSetType` is asserted twice: `ric-rst:*` (coarse) and `vocnet-htype:htXXX` (fine-grained). `PhysicalThing` ancestors use the same htype rows with no `mocho:Manifestation`.

dc:type dispatch uses `output/config/lookup_dctype_to_class.csv` (1,647 rows) with three-level fallback: `(mediatype, sector, dc_type_de)` → `(*, sector, dc_type_de)` → `(*, *, dc_type_de)`. When a W-slot class is assigned, `mocho:Manifestation` is **not** emitted — the Manifestation role is fulfilled by the WebResource (`mocho:ImageObject`, D12).

### 1.2 Property mapping (all entity types)

For all 9 `edm.RDF` entity types: `output/alignment_ddbedm_mocho.csv` keyed by `(entity_type, json_key)` → predicate IRI; only `in_mocho=True` rows emitted. Per-type whitelists bypass the table for fan-out or wrong-level properties — see §5.4.

---

## 2. Completed work

- ADR D0 accepted (`transform-adr.md`); D1–D12 accepted (`transform-script-adr.md`)
- All lookup tables generated and verified:
  - `output/alignment_ddbedm_mocho.csv` — complete
  - `output/config/lookup_htype_doco_rico.csv` — complete
  - `output/config/lookup_dctype_to_class.csv` — complete, 1,647 rows, 0 TBDs
- Script infrastructure in place: `_extract_mediatype_sector()`, `_dctype_lookup()`, `load_dctype_map()`, `load_htype_map()`, `load_alignment()` — all written
- ProvidedCHO and Aggregation fully mapped
- Baseline run (2026-04-20): 44.4M triples, 115,432 records

---

## 3. Entity type status

| Entity type | Instances | Property mapping | rdf:type | Impl status |
|---|---|---|---|---|
| ProvidedCHO | 115,432 | alignment CSV + creator/contributor whitelists | `mocho:Manifestation` + dc:type dispatch + htype | ✅ done |
| Aggregation | 115,432 | alignment CSV (EDM-structural `in_mocho=False` per D4) | — | ✅ done |
| WebResource | 312,538 | creator→`rdam:P30263`; type→`rdam:P30002` (whitelists); dcTermsRights/edmRights from CSV | mt002: `mocho:ImageObject` + `rdac:C10007` | ☐ pending |
| Agent | 422,026 | rdaa: whitelists + skos: labels + `owl:sameAs`; wrong-WEMI rows corrected | — (defer) | ☐ pending |
| Place | 118,088 | `geo:lat/long/alt` + skos: labels + `owl:sameAs` | — (defer) | ☐ pending |
| PhysicalThing | 55,771 | `title`→`rdaw:P10088`; `isPartOf`→`rico:includesOrIncluded` | htype dispatch only (no `mocho:Manifestation`) | ☐ pending |
| TimeSpan | 99,930 | `begin`→`schema:startDate`; `end`→`schema:endDate` | — (defer) | ☐ pending |
| Concept | 717,638 | `prefLabel`→`skos:prefLabel`; `notation`→`skos:notation` | `skos:Concept` + IRI-prefix dispatch | ☐ pending |
| Event | 158,407 | all deferred (CRM not in mocho) | — | ❌ deferred |

---

## 4. Concept entities

Concept nodes in `edm.RDF.Concept[]` serve multiple roles. The `about` IRI prefix determines the role:

| IRI prefix | Role | Action |
|---|---|---|
| `ddb.vocnet.org/medientyp/` | Mediatype vocab term | emit `skos:Concept` + `skos:prefLabel` + `skos:notation` |
| `ddb.vocnet.org/sparte/` | Sector vocab term | emit `skos:Concept` + `skos:prefLabel` + `skos:notation` |
| `ddb.vocnet.org/hierarchietyp/` | htype vocab term | skip (already declared as named individuals in mocho) |
| GND / VIAF / other authority | Subject / agent / place ref | emit `skos:Concept` + `skos:prefLabel` if present |
| Unknown / other | Generic controlled term | emit `skos:Concept` + available properties |

All Concept nodes: emit `rdf:type skos:Concept`. Properties `prefLabel` → `skos:prefLabel` (lang-tagged), `notation` → `skos:notation`.

---

## 5. Implementation steps

### 5.1 Patch alignment CSV

**Script**: `scripts/patch_alignment_inmocho.py` (new)  
Set `in_mocho=False` for wrong-WEMI-level rows:
- `Agent`: `date` (keep only `rdaa:P50039`), `hasPart`, `isPartOf`, `type` — all WEMI candidates
- `Place`: `hasPart`, `isPartOf`, `type` — all WEMI candidates
- `PhysicalThing`: `title` candidates except `rdaw:P10088`

Run against `output/alignment_ddbedm_mocho.csv`; verify row counts before/after.

### 5.2 Wire dc:type dispatch in retype_entities()

Call `_dctype_lookup(mediatype, sector, dc_type_de)` inside `retype_entities()` for ProvidedCHO. Emit W-slot class instead of `mocho:Manifestation` (or M-slot class alongside it). Functions already exist — just needs to be called.

### 5.3 mt002 WebResource typing

Inside `retype_entities()`, when `mediatype == mt002`, for each WebResource URI emit:
```
<wr-uri>  rdf:type  mocho:ImageObject
<wr-uri>  rdf:type  rdac:C10007          # RDA Manifestation
<wr-uri>  rdam:P30001  rdact:1018        # has carrier type
<wr-uri>  vra:imageOf  <cho-uri>
```

### 5.4 Entity-type whitelists

Add per-type whitelist dicts in `transform_edm_to_mocho.py`. Whitelisted keys bypass the alignment CSV loop entirely.

**WebResource**

| Key | Target predicate |
|---|---|
| `creator` | `rdam:P30263` "has creator agent of manifestation" |
| `type` | `rdam:P30002` "has media type of manifestation" |

**Agent**

| Key | Target predicate |
|---|---|
| `prefLabel` | `skos:prefLabel` |
| `altLabel` | `skos:altLabel` |
| `name` | `rdaa:P50102` |
| `identifier` | `owl:sameAs` (if IRI) / `rdaa:P50094` (if literal) |
| `begin` | `rdaa:P50067` |
| `end` | `rdaa:P50068` |
| `dateOfBirth` | `rdaa:P50067` |
| `dateOfDeath` | `rdaa:P50068` |
| `dateOfEstablishment` | `rdaa:P50067` |
| `dateOfTermination` | `rdaa:P50068` |
| `gender` | `rdaa:P50116` |
| `biographicalInformation` | `rdaa:P50113` |
| `professionOrOccupation` | `rdaa:P50100` |
| `placeOfBirth` | `rdaa:P50069` |
| `placeOfDeath` | `rdaa:P50070` |
| `note` | `skos:note` |
| `sameAs` | `owl:sameAs` |

**Place**

| Key | Target predicate |
|---|---|
| `prefLabel` | `skos:prefLabel` |
| `altLabel` | `skos:altLabel` |
| `note` | `skos:note` |
| `sameAs` | `owl:sameAs` |
| `lat` | `geo:lat` |
| `long` | `geo:long` |
| `alt` | `geo:alt` |

**PhysicalThing**

| Key | Target predicate |
|---|---|
| `title` | `rdaw:P10088` |
| `isPartOf` | `rico:includesOrIncluded` |

**TimeSpan**

| Key | Target predicate |
|---|---|
| `begin` | `schema:startDate` |
| `end` | `schema:endDate` |

### 5.5 Concept emission

Add Concept to the entity emit loop in `transform_record()`. For each Concept node:
1. Emit `rdf:type skos:Concept`
2. Emit `skos:prefLabel` from `prefLabel` key (lang-tagged `@de` if present)
3. Emit `skos:notation` from `notation` key
4. IRI-prefix check: skip htype individuals (`ddb.vocnet.org/hierarchietyp/`)

### 5.6 ADR update

Add D15–D1N to `notes/transform-script-adr.md` covering:
- D13: Agent property whitelist (rdaa: namespace)
- D14: Place property whitelist (geo: + skos: + owl:sameAs)
- D15: WebResource.type → rdam:P30002
- D16: PhysicalThing.isPartOf → rico:includesOrIncluded (correction from rico:isOrWasPartOf)
- D17: TimeSpan → schema:startDate/endDate
- D18: Concept emission (skos:Concept + IRI-prefix dispatch)

### 5.7 Housekeeping

- `scripts/README.md` — add `patch_alignment_inmocho.py`
- `notes/transform-writeup.md §3` — update stale "Concepts are never emitted" statement

---

## 6. Files to modify

| File | Action |
|---|---|
| `scripts/patch_alignment_inmocho.py` | Create |
| `scripts/transform_edm_to_mocho.py` | Modify — §5.2–5.5 |
| `notes/transform-script-adr.md` | Modify — add D15–D18 |
| `scripts/README.md` | Modify |
| `notes/transform-writeup.md` | Modify — §3 |
| `output/alignment_ddbedm_mocho.csv` | Modified by patch script |

---

## 7. Verification

After all steps:

| Check | Method |
|---|---|
| Triple count vs 44.4M baseline | Compare `transform_stats.json` |
| Agent: `rdaa:P50067` present | `grep rdaa/P50067 goethe-faust-mocho.nt \| head` |
| Place: `geo:lat` present | `grep geo/wgs84.*lat goethe-faust-mocho.nt \| head` |
| WebResource mt002: `mocho:ImageObject` + `vra:imageOf` | Sample one mt002 record |
| Concept medientyp: `skos:Concept` + `skos:prefLabel` | `grep medientyp goethe-faust-mocho.nt \| head` |
| PhysicalThing: `rico:includesOrIncluded` used (not `isOrWasPartOf`) | `grep includesOrIncluded goethe-faust-mocho.nt \| wc -l` |
| Concept htype: NOT emitted (skipped) | `grep hierarchietyp goethe-faust-mocho.nt \| wc -l` → 0 |
