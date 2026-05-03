# Transform revised plan: EDM → mocho N-Triples

**Date**: 2026-04-29  
**Status**: In progress  
**Supersedes**: `transform-plan.md`, `transform-edm2mocho-plan.md`, `entity-property-mapping-plan.md`  
**Co-maintained with**: `transform-script-plan.md` (implementation detail) — `transform-script-plan.md §0` is authoritative for pipeline architecture; this document's §0–§1 must stay in sync.  
**Related**: `transform-adr.md` (D0), `transform-script-adr.md` (D1–D14), `entity-property-mapping.md`, `transform-writeup.md`

---

## 0. Architecture

The transformation has two orthogonal problems that should stay separated:

1. **Class dispatch** — what `rdf:type`(s) to assign, driven by sector × mediatype × htype × dc:type
2. **Property mapping** — which predicate to emit per source key, driven by assigned class

Both are already solved in data (lookup CSVs). The goal is a thin engine that reads them rather than re-encoding dispatch logic in code. Mapping corrections then require only a CSV edit.

**At reference-corpus scale (115K records)**: `transform_edm_to_mocho.py` — stdlib Python, record-by-record streaming, special-case handlers called explicitly. See D1–D17 in `transform-script-adr.md`.

**At full-corpus scale (27M records)**: The transform is fundamentally a series of joins — dispatch = join against class tables; property mapping = join against alignment table. Python record-by-record is too slow; SPARQL CONSTRUCT requires a triplestore and performs poorly at this scale. Use a two-stage pipeline instead (see ADR D18):

```
Stage 1 — Flatten (Python streaming, stdlib):
  s2.sqlite (bufgz column) → cho.jsonl, agent.jsonl, webresource.jsonl,
                                  place.jsonl, physicalthing.jsonl,
                                  concept.jsonl, timespan.jsonl
  ⚠ Input is sqlite/bufgz, not JSONL (D19). Sector is known from the DB.

Stage 2 — Dispatch + map (DuckDB, vectorized joins):
  cho.jsonl  + lookup_htype_doco_rico.csv
             + lookup_dctype_to_class.csv     →  class triples (graph/mocho)
             + alignment_ddbedm_mocho.csv     →  property triples (graph/mocho)
  (repeat per entity type)
  edm.RDF fields → raw EDM triples             →  graph/ddb-edm  (priority #1)
  W-level ProvidedCHOs → GND Werk links        →  graph/work
  PROV-O triples                               →  graph/prov

Special-case handlers (Python UDFs or post-processing pass):
  handle_subject_iri_or_literal()
  handle_creator_uri_resolution()
  handle_mt001_audio_group()
  handle_mt002_webresource_typing()
```

Stage 1 is fast (no logic, just fan-out). Stage 2 runs in minutes on a single machine; DuckDB reads JSONL and CSVs natively. The `emit_mode` column in the alignment CSV (`iri`, `literal`, `dual`, `skip`) covers most property-level variants without custom code. The four output named graphs (`ddb-edm`, `mocho`, `work`, `prov`) match the reference-corpus streams in `transform-script-plan.md` §0.

---

## 1. Pipeline overview

**POC**: input `data/items-all-goethe-faust.json` (115,432 records, JSONL); script `scripts/transform_edm_to_mocho.py`.  
**Full corpus**: input `s2.sqlite` (sqlite, `bufgz` column); sector known from DB at query time (D19).  
**Outputs** — four named-graph streams (see `transform-script-plan.md` §0):

| Stream | Named graph | Output file |
|---|---|---|
| Raw EDM | `…/graph/ddb-edm` | `<sector>-ddb-edm.nt` |
| mocho-aligned | `…/graph/mocho` | `<sector>-mocho.nt` |
| GND Work links | `…/graph/work` | `<sector>-work.nt` |
| Provenance | `…/graph/prov` | `<sector>-prov.nt` |

⚠ **Stale**: the earlier single-file output `goethe-faust-mocho.nt` is superseded by the four-stream model above.

Reference Schema: `output/edm_field_profile.csv`

| Entity type | Instances | Mapping status | Details |
|---|---|---|---|
| ProvidedCHO | 115,432 | ✅ done | class dispatch: §1.1; property mapping: `transform-props-mapping-plan.md`; ADR D1–D12 |
| Agent | 115,432 | ✅ done | `transform-props-mapping-adr.md` D13; `lookup_class_prop_alignment.csv` rows 549–572 |
| Event | 110,059 | ❌ not emitted | no standalone triples; traversed as dispatch intermediary — see §3 |
| Place | 59,249 | ✅ label stub only | object of `dc:spatial` and `edm:currentLocation`; `prefLabel` label triple — see §4 |
| TimeSpan | 99,930 | ✅ via dc:date / dc:issued | not emitted; date literals on CHO; class-specific predicate dispatch — see §5 |
| WebResource | 115,432 | ✅ URI passthrough | linked via Aggregation `edm:isShownAt`; URI → `dcterms:source` on CHO — see §6 |
| Concept | 115,432 | ☐ pending | — |
| Aggregation | 115,432 | ✅ URI extraction | bridges CHO ↔ WebResource; emits `<cho> dcterms:source <wr-uri>` — see §7 |
| PhysicalThing | 22,265 | ❌ deferred | htype retyping deferred; transform-adr.md D14 |



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
| sparte001 Archive | mt001 Audio | — | — | `aco:AudioManifestation` (also added alongside htype-derived `rico:*`) | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte001 Archive | mt002 Photo | — | — | `mocho:ImageManifestation` (also added alongside htype-derived `rico:*`) | M | — | — |
| sparte001 Archive | mt003 Text | — | — | `mocho:Manifestation` (also added alongside htype-derived `rico:*`; not `rdac:C10007` — archival text is not necessarily literary) | M | — | `notes/transform-script-adr.md` D9 |
| sparte001 Archive | mt005 Video | — | — | `ec:EditorialWork` (W) + `ec:MediaResource` (M) (also added alongside htype-derived `rico:*`) | W+M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
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
| sparte002 Library | mt005 Video | — | — | `ec:EditorialWork` (W) + `ec:MediaResource` (M) (also added alongside htype-derived class) | W+M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte002 Library | mt007 Not Digitized | — | — | htype-derived class; `rdac:C10007` "Manifestation" if no htype | M | — | `output/config/lookup_htype_doco_rico.csv` |
| sparte003 Monument | mt002 Photo | — | — | `mocho:ImmovableWork` (W) + `mocho:ImageManifestation` (M) | W+M | — | — |
| sparte003 Monument | mt003 Text | — | — | `mocho:ImmovableWork` + `rdac:C10007` "Manifestation" | W+M | — | — |
| sparte003 Monument | mt001 Audio | — | — | `mocho:ImmovableWork` + `aco:AudioManifestation` | W+M | — | — |
| sparte003 Monument | mt005 Video | — | — | `mocho:ImmovableWork` + `ec:MediaResource` | W+M | — | — |
| sparte003 Monument | mt007 Not Digitized | — | — | `mocho:ImmovableWork` | W | — | — |
| sparte004 Research | mt001 Audio | — | — | `aco:AudioManifestation` | M | — | ⚠ check dc:type values |
| sparte004 Research | mt002 Photo | — | — | `mocho:ImageManifestation` | M | — | — |
| sparte004 Research | mt003 Text | — | — | htype-derived class (same dispatch as sparte002); `rdac:C10007` "Manifestation" if no htype | M | — | ⚠ check dc:type values |
| sparte004 Research | mt005 Video | — | — | `ec:MediaResource` | M | — | ⚠ check dc:type values |
| sparte004 Research | mt007 Not Digitized | — | — | `mocho:Manifestation` | M | — | ⚠ check dc:type values |
| sparte005 Media | mt001 Audio | — | — | `aco:AudioManifestation` | M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte005 Media | mt005 Video | — | — | `ec:EditorialWork` (W) + `ec:MediaResource` (M) | W+M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte005 Media | mt002 Photo | — | — | `mocho:ImageWork` (W) + `mocho:ImageManifestation` (M) | W+M | — | `notes/transform-adr.md` §1.2 |
| sparte006 Museum | mt002 Photo | — | — | `vra:Work` (W) + `vra:Image` (M) | W+M | — | `notes/transform-adr.md` §1.2 |
| sparte006 Museum | mt005 Video | — | — | `ec:EditorialWork` (W) + `ec:MediaResource` (M) | W+M | — | `mocho/notes/mocho-gatherer-adr.md` §8 |
| sparte007 Others | mt002 Photo | — | — | `mocho:ImageManifestation` | M | — | `notes/transform-adr.md` §1.2 |
| sparte004/007 | * | — | — | `mocho:Manifestation` | M | — | `notes/transform-script-adr.md` D9 |
| * | * | — | — | `mocho:Manifestation` (D9 fallback) | M | — | `notes/transform-script-adr.md` D9 |

For `rico:RecordSet` rows, `rico:hasRecordSetType` is asserted twice: `ric-rst:*` (coarse) and `vocnet-htype:htXXX` (fine-grained). `PhysicalThing` ancestors use the same htype rows with no `mocho:Manifestation`.

dc:type dispatch uses `output/config/lookup_dctype_to_class.csv` (1,647 rows) with three-level fallback: `(mediatype, sector, dc_type_de)` → `(*, sector, dc_type_de)` → `(*, *, dc_type_de)`. When a W-slot class is assigned, `mocho:Manifestation` is **not** emitted — the Manifestation role is fulfilled by the WebResource (`mocho:ImageObject`, D12).

### 1.2 Work-level GND Werk lookup table

When §1.1 class dispatch assigns a Work-level class (`rdac:C10001` or `mo:MusicalWork`), an additional row is written to a DuckDB lookup table for GND Werk authority file linking. This is separate from the mocho N-Triples output — it is a staging table consumed by the GND Werk linker (`link_gnd_works.py`, Phase 0).

| Field | Source path | Notes |
|---|---|---|
| `dc:title` | `ProvidedCHO.title[].@value` | primary lookup key |
| `dc:alternative` | `ProvidedCHO.alternative[].$` | multiple values; alternate lookup keys |
| `dc:created` | `ProvidedCHO.created` | creation date |
| `dc:creator` (URIs) | `ProvidedCHO.creator[].resource` | GND URIs only (`http://d-nb.info/gnd/…`); null or list |
| `dc:creator` (literals) | `ProvidedCHO.creator[].$` | stored as `last, first` — GND normalized form (see §4 of `transform-props-mapping-plan.md`) |

Name literal format is `last, first` — consistent with GND "Familienname, Vorname" ordering and the existing agent stub label convention.

### 1.3 Property mapping (all entity types)

See `notes/transform-props-mapping.plan` for per-entity-type property decisions.

---

## 2. edm:Agent

### 2.1 Class dispatch

Driven by `edm:Agent.type.resource` — the gndo subtype is already present in the source record:

| `edm:Agent.type.resource` | mocho class |
|---|---|
| `gndo:DifferentiatedPerson` | `mocho:Agent` |
| `gndo:CorporateBody` | `mocho:CorporateBody` |
| `gndo:ConferenceOrEvent` | `gndo:ConferenceOrEvent` (as-is) |
| `gndo:Family` | `mocho:Family` |

Current Phase 0 stub: all → `mocho:Agent`. Type-based dispatch is ready to implement without waiting for Phase 1b.

### 2.2 Property dispatch

Done. 24 properties mapped per `output/config/lookup_class_prop_alignment.csv` (rows 549–572). Decision: `transform-props-mapping-adr.md` D13. Script: `scripts/gen_agent_alignment_rows.py`.

Agent nodes are minted when `creator` (§4, `transform-props-mapping-plan.md`) or `contributor` (§5) values resolve to a DDB org or GND URI:

```turtle
<agent.about> a mocho:Agent ;
              rdfs:label "..."@lang .
```

Non-trivial remappings:

| edm_prop | target_prop |
|---|---|
| `dc:identifier` | `gndo:gndIdentifier` |
| `edm:altLabel` | `skos:altLabel` |
| `edm:sameAs` | `owl:sameAs` |

All `gndo:` demographic properties and EDM relational properties (`edm:begin`, `edm:end`, `edm:hasMet`, `edm:isRelatedTo`, `edm:wasPresentAt`) are passthrough. Domain-restricted property dispatch follows from class dispatch above — see `transform-future-plan.md §10`.

---

## 3. edm:Event

### 3.1 Class dispatch

`edm:Event` nodes are **not typed or emitted** as standalone RDF entities — CIDOC-CRM is not imported into mocho. Event nodes serve as dispatch intermediaries only.

### 3.2 Role in property dispatch

Event data is traversed in two contexts during ProvidedCHO transformation:

**1. Contributor predicate dispatch (D3, `transform-props-mapping-adr.md`)**: The LIDO event type (`edm:Event.hasType.resource`) resolves the predicate for each `dc:contributor` value:

```
ProvidedCHO.hasMet[].resource  →  edm:Event.about
edm:Event.hasType.resource     →  LIDO event type URI
edm:Event.P11_had_participant[].resource  ==  contributor[].resource
→  emit <cho> <target_prop> <contributor.resource>
```

Dispatch table: `output/config/lido_event_types.csv`. Key types:

| LIDO event type | Role |
|---|---|
| lido00012 creation | creator / `rdam:P30329` |
| lido00228 publication | publisher / `rdam:P30083` |
| lido00007 production | producer / `rdam:P30081` |
| lido01127 photography | photographer / `rdam:P30329` |
| lido00224 designing | designer / `rdaw:P10051` |
| lido00226 commissioning | commissioner / `rdaw:P10287` |

**2. Spatial data (`edm:Event.happenedAt`)**: 99.5% of `happenedAt` URIs duplicate `dc:spatial` on the CHO directly — no event traversal needed for place. See `data/analysis/spatial_event_overlap.csv`.

**3. Temporal data (`edm:Event.occurredAt`)**: Event-specific dates (creation date, publication date) are currently not extracted separately — `dc:date` on the CHO is used instead. Typed date dispatch by LIDO event type is deferred.

---

## 4. edm:Place

### 4.1 Class dispatch

`edm:Place` nodes are **not typed** in Phase 0 — neither `geo:SpatialThing` nor `schema:Place` is imported into mocho. Only a label stub is emitted (see §4.2). Class typing is deferred.

### 4.2 Role in property dispatch

Place nodes appear as the range of two ProvidedCHO properties:

- **`dc:spatial`** (§16, `transform-props-mapping-plan.md`): passthrough; no RDA/vocab equivalent for a place-as-URI; object URI used directly. 99.5% of `dc:spatial` URIs duplicate `edm:Event.happenedAt` — no event traversal is needed (see `data/analysis/spatial_event_overlap.csv`).
- **`edm:currentLocation`** (§17, `transform-props-mapping-plan.md`): passthrough for all classes; emitted as-is.

For each Place URI referenced by either property, a label stub is emitted:

```
<place-uri>  rdfs:label  "..."@lang
```

Source: `edm.RDF.Place[].prefLabel[].@value` + `.@language` (§0.2, `transform-props-mapping-plan.md`).

No additional Place-level triples are emitted in Phase 0.

---

## 5. edm:TimeSpan

### 5.1 Class dispatch

`edm:TimeSpan` nodes are **not typed or emitted** as standalone RDF entities — no TimeSpan class (e.g. `time:Interval`) is imported into mocho. Date values reach the output exclusively as literals on the ProvidedCHO via `dc:date` and `dc:issued`.

### 5.2 Role in property dispatch

TimeSpan data enters the pipeline through two CHO-level source properties:

- **`dc:date`** (§6, `transform-props-mapping-plan.md`): general date literal; format varies (`"2018 (role)"`, `"18300213"`).
- **`dc:issued`** (§7, `transform-props-mapping-plan.md`): publication year; non-standard DC term; treated as a publication date.

Both are mapped **per target class** (D9, `transform-props-mapping-adr.md`):

| target_class | `dc:date` → | `dc:issued` → |
|---|---|---|
| `rdac:C10007`, `mocho:Manifestation` | `rdam:P30278` "has date of manifestation" | `rdam:P30011` "has date of publication" |
| `rdac:C10001` | `rdaw:P10219` "has date of work" | N/A |
| `vra:Image` | `vra:dateCreated` | `dc:issued` |
| `vra:Work` | `vra:dateCreated` | N/A |
| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | `rico:creationDate` | `rico:publicationDate` |
| `aco:*`, `mo:*`, `doco:*`, `ec:*`, `mocho:Image*`, `mocho:Immovable*` | `dc:date` | `dc:issued` |

N/A rows are not emitted.

The indirect path `CHO → edm:hasMet → Event → edm:occurredAt → TimeSpan` is not traversed — event-scoped date extraction (creation date vs. publication date by LIDO type) is deferred (§3.2 item 3).

Source: `output/config/lookup_class_prop_alignment.csv` (dc:date and dc:issued rows).

---

## 6. edm:WebResource

### 6.1 Class dispatch

`edm:WebResource` nodes are not typed or emitted as standalone RDF entities. The WebResource URI is extracted from the Aggregation and attached to the ProvidedCHO as a `dcterms:source` object (see §7).

### 6.2 Role in property dispatch

The WebResource URI (`edm:WebResource.about`) is the URL of the digitised object as hosted by the providing institution. It is the target of `edm:isShownAt` on the Aggregation. No WebResource-level properties (e.g. `edm:rights`, `dc:format`) are mapped in Phase 0.

---

## 7. edm:Aggregation

### 7.1 Class dispatch

`edm:Aggregation` nodes are not typed or emitted. The Aggregation is traversed solely to extract the WebResource URI.

### 7.2 Properties mapping

All Aggregation properties are present on 100% of records (115,432). The Aggregation is traversed to resolve `<cho-uri>` via `aggregatedCHO`; no Aggregation-level triples are emitted.

| EDM field | EDM predicate | Triple emitted on CHO | Comment |
|---|---|---|---|
| `about` | — (Aggregation node IRI) |  | Aggregation URI | |
| `aggregatedCHO` | `edm:aggregatedCHO` | — (navigation to `<cho-uri>`) | |
| `isShownAt` | `edm:isShownAt` | `<cho> dcterms:source <wr-uri>` | |
| `isShownBy` | `edm:isShownBy` | — | |
| `edmRights` | `edm:rights` | ❌ | "EDM Rights Statements see: http://pro.europeana.eu/web/guest/available-rights-statements"|
| `dcTermsRights` | `dcterms:rights` | <cho> dcterms:rights <dcTermsRights.resource> > |
| `provider` | `edm:provider` | ❌ | DDB, as the provider to Europeana |
| `dataProvider` | `edm:dataProvider` | `<cho> edm:dataProvider <uri>` where `uri` starts with `http://www.deutsche-digitale-bibliothek.de/organization/` | |
| `object` | `edm:object` | `<cho> foaf:thumbnail <uri>` where `uri` = `object[].resource` | |
| `aggregator` | `edm:aggregator` | — | |
| `hasView` | `edm:hasView` | — | |

`dcterms:source` is the appropriate predicate for `isShownAt`: the WebResource is the digital surrogate at which the CHO is shown by the providing institution.

Quoted comments source: https://docs.google.com/spreadsheets/d/1hpEthDrlpjVoB9RjABUS18WsQEZJ-iP6/edit?gid=497286012#gid=497286012

---

## 8. Completed work

See `transform-props-mapping-adr.md` for all decisions (D1–D13) and `transform-script-adr.md` for implementation decisions.
