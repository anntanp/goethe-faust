# DuckDB transform plan: EDM → mocho at scale

**Date**: 2026-05-03  
**Status**: Draft  
**Context**: Full DDB corpus (~27M records). Two-stage pipeline — see `transform-revised-plan.md §0` and `transform-script-adr.md` D18.

---

## 1. Entity type decision

| Entity type | Instances (GF) | Decision | Reason |
|---|---|---|---|
| ProvidedCHO | 115,432 | **include** | Core entity; all dispatch + property mapping |
| Aggregation | 115,432 | **include** | Rights, provider info, WebResource links |
| WebResource | 312,538 | **include** | ImageObject typing (D12); thumbnail URIs |
| Agent | 422,026 | **include** | Creator/contributor nodes with rdaa: properties |
| PhysicalThing | 55,771 | **include** | sparte001 archival hierarchy (rico: dispatch) |
| Concept | 717,638 | **include** | vocab terms (medientyp/sparte) + subject nodes |
| TimeSpan | 99,930 | **skip nodes** | Inline `begin`/`end` into CHO via Event traversal; no TimeSpan URIs emitted |
| Place | 118,088 | **defer Phase 2** | Reached via Event (`edm:happenedAt`); geo properties not in Phase 1 |
| Event | 158,407 | **include** | LIDO type distinguishes agent roles (author, photographer, publisher…) and date semantics (creation date, publication date…); required for contributor role dispatch (D3) and typed date emission |

---

## 2. Stage 1: Flatten pass output (Python, stdlib)

One streaming pass over the JSONL. No dispatch logic — pure fan-out.

| Output file | Source path | Key columns carried over |
|---|---|---|
| `cho.jsonl` | `edm.RDF.ProvidedCHO` | all mapped fields + inlined TimeSpan begin/end + sector + mediatype |
| `aggregation.jsonl` | `edm.RDF.Aggregation` | about, aggregatedCHO, isShownBy, hasView[], provider, dataProvider, rights, edmRights |
| `webresource.jsonl` | `edm.RDF.WebResource[]` | about, type.resource, format, rights, creator + `cho_uri` from parent |
| `agent.jsonl` | `edm.RDF.Agent[]` | all rdaa-mapped fields (see §3.4) |
| `physicalthing.jsonl` | `edm.RDF.PhysicalThing[]` | about, hierarchyType, title, isPartOf + `cho_uri` from parent |
| `concept.jsonl` | `edm.RDF.Concept[]` | about, prefLabel[], notation; skip `hierarchietyp` IRIs |
| `event.jsonl` | `edm.RDF.Event[]` | about, lido_type (event type), agent_uri, agent_role, occurred_at (TimeSpan IRI), happened_at (Place IRI) + `cho_uri` from parent |

**Temporal data — two paths**:
- Direct: `dc:date` and `dc:issued` literals on CHO (44.99% / 41.48% coverage)
- Structured: CHO → `hasMet` → Event → `edm:occurredAt` → TimeSpan → `begin`/`end`; copy into `cho.jsonl` as `timespan_begin`/`timespan_end`

**Place data — two paths**:
- Direct: `edm:currentLocation` (43.65%) and `dc:spatial` (7.1%) IRIs on CHO
- Event-linked: CHO → `hasMet` → Event → `edm:happenedAt` → Place IRI; copy as `event_place` (Phase 2)

Event nodes are emitted (see §3.7); they carry LIDO type needed for role and date semantics dispatch.

---

## 3. Stage 2: DuckDB tables and joins

### 3.1 `cho` — ProvidedCHO

Dispatch signals + all mapped properties. From `edm_field_profile.csv` (ProvidedCHO, 26 fields):

| Column | Coverage | Target predicate | Notes |
|---|---|---|---|
| `uri` | 100% | subject | `about` |
| `sector` | derived | dispatch signal | from `provider-info.domains[0]` |
| `mediatype` | derived | dispatch signal | from `WebResource[0].type.resource` |
| `htype` | 80.5% | dispatch signal | → `lookup_htype_doco_rico.csv` |
| `dc_type` | 80.4% | dispatch signal | → `lookup_dctype_to_class.csv` |
| `title` | 100% | class-specific title pred | dual-emit: rdam/rdaw/rdaa depending on assigned class |
| `identifier` | 87.7% | `rdam:P30168` "has identifier for manifestation" | |
| `description` | 76.6% | class-specific note pred | |
| `extent` | 66.5% | `rdam:P30137` "has extent of manifestation" | |
| `edm_type` | 63.3% | — | used for dispatch cross-check only |
| `language` | 62.1% | class-specific language pred | dedup with `dcTermsLanguage` |
| `dc_subject` | 60.3% | `dcterms:subject` | dedup `dcSubject`/`dcTermsSubject`/`dcTermSubject` |
| `is_part_of` | 58.5% | `dcterms:isPartOf` | |
| `date` | 45.0% | `rdam:P30278` "has date of manifestation" | normalise D17 |
| `timespan_begin` | ~45% | `rdam:P30278` | inlined from TimeSpan |
| `timespan_end` | ~45% | `rdam:P30278` | inlined from TimeSpan |
| `issued` | 41.5% | class-specific issued pred | |
| `current_location` | 43.7% | `schema:location` | |
| `creator` | 36.9% | `rdam:P30329` "has creator agent of manifestation" | IRI or literal; special-case handler |
| `contributor` | 26.2% | `dc:contributor` → Phase 1b | LIDO role dispatch later |
| `format` | 17.8% | `rdam:P30002` "has media type of manifestation" | |
| `spatial` | 7.1% | Place IRI | Phase 2 |
| `alternative` | 5.2% | class-specific variant title pred | |
| ~~`aggregation_entity`~~ | 66.6% | skip | D6 |
| ~~`hierarchy_position`~~ | 44.2% | skip | D6 |

**Dispatch join**:
```sql
SELECT c.uri, h.rdf_types AS htype_classes, d.rdf_types AS dctype_classes
FROM cho c
LEFT JOIN read_csv('lookup_htype_doco_rico.csv') h ON c.htype = h.htype_code
LEFT JOIN read_csv('lookup_dctype_to_class.csv') d
  ON c.mediatype = d.mediatype AND c.sector = d.sector AND c.dc_type = d.dc_type_de
```

**Property mapping join**:
```sql
SELECT c.uri, p.target_pred, c[p.source_key] AS value, p.emit_mode
FROM cho c
JOIN read_csv('alignment_ddbedm_mocho.csv') p
  ON p.entity_type = 'ProvidedCHO' AND p.in_mocho = true
```

### 3.2 `aggregation`

| Column | Target predicate |
|---|---|
| `uri` | subject |
| `cho_uri` | `edm:aggregatedCHO` |
| `is_shown_by` | `edm:isShownBy` |
| `has_view` | `edm:hasView` (LIST — one triple per item) |
| `provider` | `edm:provider` |
| `data_provider` | `edm:dataProvider` |
| `rights` | `dc:rights` |
| `edm_rights` | `edm:rights` |

No dispatch. Property mapping via alignment CSV (`entity_type = 'Aggregation'`).

### 3.3 `webresource`

| Column | Target predicate |
|---|---|
| `uri` | subject |
| `cho_uri` | `vra:imageOf` (mt002 only) |
| `type_resource` | dispatch signal → mt002 ImageObject typing |
| `format` | `rdam:P30002` "has media type of manifestation" |
| `rights` | `dc:rights` |
| `creator` | `rdam:P30329` "has creator agent of manifestation" |

mt002 dispatch emits: `mocho:ImageObject` + `rdac:C10007` "Manifestation" + `rdam:P30001` "has carrier type" `rdact:1018` + `vra:imageOf cho_uri` (D12).

### 3.4 `agent`

⚠ **Note**: several IRIs in `transform-revised-plan.md §5.4` Agent whitelist are wrong — corrected here from `mocho/output/rda_properties_rda-5.4.9.csv`.

| Column | Target predicate | ADR had |
|---|---|---|
| `uri` | subject | |
| `pref_label` (LIST) | `skos:prefLabel` | ✓ |
| `alt_label` (LIST) | `skos:altLabel` | ✓ |
| `name` | `rdaa:P50111` "has name of person" | ~~P50102~~ |
| `identifier` | `owl:sameAs` (IRI) / `rdaa:P50094` "has identifier for person" (literal) | ✓ |
| `begin` / `date_of_birth` | `rdaa:P50121` "has date of birth" | ~~P50067~~ |
| `end` / `date_of_death` | `rdaa:P50120` "has date of death" | ~~P50068~~ |
| `date_of_establishment` | `rdaa:P50037` "has date of establishment" | ~~P50067~~ |
| `date_of_termination` | `rdaa:P50038` "has date of termination" | ~~P50068~~ |
| `gender` | `rdaa:P50116` "has gender" | ✓ |
| `biographical_information` | `rdaa:P50113` "has biographical information" | ✓ |
| `profession_or_occupation` | `rdaa:P50104` "has profession or occupation" | ~~P50100~~ |
| `place_of_birth` | `rdaa:P50119` "has place of birth" | ~~P50069~~ |
| `place_of_death` | `rdaa:P50118` "has place of death" | ~~P50070~~ |
| `same_as` (LIST) | `owl:sameAs` | ✓ |
| `note` | `skos:note` | ✓ |

No class dispatch in Phase 1. GND resolution runs in Phase 1b (`link_gnd_agents.py`).

### 3.5 `physicalthing`

| Column | Target predicate |
|---|---|
| `uri` | subject |
| `cho_uri` | — (context only; not emitted) |
| `htype` | dispatch → `lookup_htype_doco_rico.csv` → `rico:RecordSet/Record/RecordPart` + `rico:hasRecordSetType` |
| `title` | `rdaw:P10088` "has title of work" |
| `is_part_of` | `rico:includesOrIncluded` |

No `mocho:Manifestation` fallback (D10). If htype absent or pending: no rdf:type emitted.

### 3.6 `concept`

| Column | Target predicate |
|---|---|
| `uri` | subject |
| `iri_prefix` | dispatch signal: `medientyp`, `sparte`, `hierarchietyp`, `gnd`, `viaf`, `other` |
| `pref_label` (LIST) | `skos:prefLabel` |
| `notation` | `skos:notation` |

Dispatch on `iri_prefix`: `hierarchietyp` → skip; all others → emit `rdf:type skos:Concept` + labels.

### 3.7 `event`

| Column | Role |
|---|---|
| `uri` | subject |
| `cho_uri` | link back to CHO (from `edm:hasMet`) |
| `lido_type` | LIDO event type — dispatch key for agent role and date semantics |
| `agent_uri` | agent involved in this event |
| `agent_role` | role label (if present alongside LIDO type) |
| `occurred_at` | TimeSpan IRI → join to extract `begin`/`end` |
| `happened_at` | Place IRI (Phase 2) |

**LIDO type dispatch** (two uses):
- **Agent role**: e.g. "Herstellung" → creator/author, "Verlag" → publisher, "Fotografiert von" → photographer. Drives typed contributor triples (D3).
- **Date semantics**: e.g. "Herstellung" → creation date, "Erscheinen" → publication date. Drives which rdam: date predicate to emit rather than a generic `rdam:P30278` "has date of manifestation".

No mocho class assigned to Event nodes themselves; they are structural connectors. Exact LIDO type vocabulary and predicate mappings TBD.

---

## 4. Output assembly

One `.nt` file per entity type; concatenate for QLever ingest:

```bash
cat cho.nt aggregation.nt webresource.nt agent.nt physicalthing.nt concept.nt event.nt \
  > ddb-mocho.nt
```

Special-case handlers (Python UDFs in DuckDB or post-processing pass):

| Handler | Trigger |
|---|---|
| `handle_subject_iri_or_literal()` | `dc_subject` — IRI vs literal dispatch |
| `handle_creator_uri_resolution()` | `creator` IRI → `dcterms:creator` when GND/DDB org resolves |
| `handle_mt001_audio_group()` | `mo:MusicalManifestation` vs `aco:AudioManifestation` |
| `handle_mt002_webresource_typing()` | ImageObject triples (§3.3) |
