# Snapshot: transform-revised-plan.md §1.1 — 2026-05-02

Saved before updating `output/config/lookup_htype_doco_rico.csv` has_record_set_type values
for ht030–ht037 to match §1.1 (replacing mocho: custom class names with ric-rst: values).

---

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



## 3. Completed work

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