# ProvidedCHO Property Mapping Plan

**Date**: 2026-05-01
**Status**: In progress
**Related**: `transform-adr.md`, `entity-property-mapping-plan.md`, `entity-property-mapping.md`, `output/alignment_ddbedm_mocho.csv`, `references/ddbedm-cho-properties.csv`

---

## §-1 Insights on GAI

When using LLMs to assist with EDM property mapping, the indirect paths from CHO to TimeSpan and Place are a recurring failure point. The pattern is:

```
CHO → edm:hasMet → Event → edm:occurredAt  → TimeSpan
                          → edm:happenedAt → Place
```

LLMs consistently collapse this to a direct CHO → TimeSpan / CHO → Place link, skipping Event. The root cause is **ambiguous property usage intent**: `edm:occurredAt` (temporal) and `edm:happenedAt` (spatial) are semantically distinct but structurally parallel, and neither name makes the intermediate Event node salient. The LLM infers the connection by property name semantics ("occurred at" → time, "happened at" → place) without attending to the Event node in between.

The same failure does not occur for the direct paths (`dc:date`, `dc:issued`, `edm:currentLocation`, `dc:spatial` on CHO directly), because those properties appear inline on the CHO without any intermediate node.

A second, related failure: even when the Event node is retained structurally, LLMs miss that it carries **LIDO type** — the event type that distinguishes agent roles (author vs. photographer vs. publisher) and date semantics (creation date vs. publication date). Without LIDO type, all contributors flatten to `dc:contributor` and all dates flatten to `rdam:P30278` "has date of manifestation", losing the typed dispatch that gives the KG its query value.

Both failures share a root cause: LLMs attend to property names as semantic clues and skip structural nodes that appear to be mere connectors, even when those nodes carry discriminating attributes.

---

## §0 Context

All ProvidedCHOs are typed as `mocho:Manifestation` (ADR D9). Target predicates must therefore be at the Manifestation WEMI level (`rdam:`) where a Manifestation-level RDA property exists. The alignment CSV (`output/alignment_ddbedm_mocho.csv`) provides candidates for each json_key but fans out across all WEMI levels without selecting one — this plan selects one target per property and documents the rationale.

Candidate predicates were drawn from `mocho/output/mapping_dct_to_rda.csv`. For properties with no RDA mapping, the source DC/EDM predicate is retained.

For object-range properties (range is a class, not a literal), this plan names the connected class and points to `entity-property-mapping.md` for the properties of that class.

`creator` (D7) and `contributor` (D8) are already decided in `transform-adr.md`; their sections below summarise those decisions and add open questions.

---

## §0.2 Property mapping workflow

For each EDM/DC property on a `ProvidedCHO`, the target predicate is resolved in three steps:

1. **Look up the RDA equivalent** in `mocho/output/mapping_dct_to_rda.csv` — this gives the RDA property (rdam:, rdaw:, rdae:) that corresponds to the source DC/DCTerms predicate. The WEMI level of the RDA property is constrained by the target class (all ProvidedCHOs are Manifestation-level per D9, so rdam: is preferred where it exists).

2. **Look up the vocabulary-specific equivalent** in the parallel mapping files — `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `mapping_mo_to_rda.csv`, `mapping_aco_to_rda.csv` — to find the native property for non-RDA target classes (vra:, rico:, mo:, aco:). Where no match is found, the source DC predicate is kept.

3. **Record the decision** in `output/config/lookup_class_prop_alignment.csv` — one row per `(target_class, edm_prop)` pair with the resolved `target_prop`. This table is the runtime dispatch table consumed by `emit_triples()` in `transform_edm_to_mocho.py`.

4. **For object-valued properties** (range is a URI): always emit an additional label triple alongside the main predicate triple:

   ```
   <cho>  <target_prop>  <URI> .
   <URI>  rdfs:label     "..."@lang .
   ```

   The label source depends on the URI type:

   | URI type | Label source in source record |
   |---|---|
   | `edm:Agent` (creator, contributor) | `edm.RDF.Agent[].prefLabel[].$` + `.lang` |
   | `edm:Place` (currentLocation, spatial) | `edm.RDF.Place[].prefLabel[].$` + `.lang` |
   | `skos:Concept` (dcType URI, dcTermsSubject, hasType) | `edm.RDF.Concept[].prefLabel[].$` + `.lang` |
   | vocnet controlled vocab (mocho:mediaType, ddb:hierarchyType) | `lookup_vocnet.csv` `label_en` → `@en`, `label_de` → `@de` |
   | `dcterms:LinguisticSystem` (dcTermsLanguage) | LOC ISO 639-2 label — deferred; emit URI only for now |
   | parent `edm:ProvidedCHO` (isPartOf) | `dc:title` of parent record if available |

   This rule applies to all URI-valued properties throughout the mapping. Where no label is available in the source record, the triple is omitted (no blank label).

---

## §0.1 Property mapping status

| Domain | Property | §  | Status |
|---|---|---|---|
| `edm:ProvidedCHO` | [about](#1-about) | §1 | ⏭ subject IRI, not a predicate |
| `edm:ProvidedCHO` | [title](#2-title) | §2 | ✅ done |
| `edm:ProvidedCHO` | [alternative](#3-alternative) | §3 | ✅ done |
| `edm:ProvidedCHO` | [creator](#4-creator) | §4 | ✅ done |
| `edm:ProvidedCHO` | [contributor](#5-contributor) | §5 | ✅ done |
| `edm:ProvidedCHO` | [date](#6-date) | §6 | ✅ done |
| `edm:ProvidedCHO` | [issued](#7-issued) | §7 | ✅ done |
| `edm:ProvidedCHO` | [description](#8-description) | §8 | ✅ done |
| `edm:ProvidedCHO` | [dcSubject](#9-dcsubject) | §9 | ✅ done |
| `edm:ProvidedCHO` | [dcTermsSubject / dcTermSubject](#10-dctermssubject--dctermsubject) | §10 | ✅ done |
| `edm:ProvidedCHO` | [isPartOf](#11-ispartof) | §11 | ✅ done |
| `edm:ProvidedCHO` | [identifier](#12-identifier) | §12 | ✅ done |
| `edm:ProvidedCHO` | [language](#13-language) | §13 | ✅ done |
| `edm:ProvidedCHO` | [dcTermsLanguage](#14-dctermslanguage) | §14 | ✅ done |
| `edm:ProvidedCHO` | [dcType](#15-dctype) | §15 | ✅ done |
| `edm:ProvidedCHO` | [spatial](#16-spatial) | §16 | ✅ done |
| `edm:ProvidedCHO` | [currentLocation](#17-currentlocation) | §17 | ✅ done |
| `edm:ProvidedCHO` | [format](#18-format) | §18 | ✅ done |
| `edm:ProvidedCHO` | [extent](#19-extent) | §19 | ✅ done |
| `edm:ProvidedCHO` | [edmType](#20-edmtype) | §20 | ✅ done |
| `edm:ProvidedCHO` | [aggregationEntity](#21-aggregationentity) | §21 | ✅ done |
| `edm:ProvidedCHO` | [hierarchyPosition](#22-hierarchyposition) | §22 | ✅ done |
| `edm:ProvidedCHO` | [hierarchyType](#23-hierarchytype) | §23 | ✅ done |
| `edm:ProvidedCHO` | [hasType](#24-hastype) | §24 | ⏭ skip — covered by `<cho> mocho:mimetype vocnet-mtype:mtXXX` |
| `edm:ProvidedCHO` | [hasMet](#25-hasmet) | §25 | ⏭ skip — EDM event-centric link; `edm:Event` modeling deferred |

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

| Property | EDM IRI | Target predicates | Notes |
|---|---|---|---|
| `title` (Manifestation node) | `dc:title` | `dc:title` + `rdam:P30134` "has title of manifestation" | Dual-emit: `dc:title` as cross-WEMI query handle; `rdam:P30134` as WEMI-specific predicate |
| `title` (Work node, when W+M) | `dc:title` | `dc:title` + `rdaw:P10088` "has title of work" | Dual-emit on the `rdac:C10001` Work node when htype/dc:type produces a W+M assignment |

Range: `rdfs:Literal` (lang-tagged string)

`dc:title` is always emitted. When `target_prop != edm_prop`, the class-specific property is dual-emitted alongside it. When `target_prop == edm_prop`, only `dc:title` is emitted (no vocab-specific equivalent exists for that class).

**Alignment table**: `output/config/lookup_class_prop_alignment.csv` — columns: `edm_class, target_class, wemi, edm_prop, target_prop`. Populated for `dc:title`; extended as other properties are decided.

Notable cases:
- `rdac:C10007`, `mocho:Manifestation` → `rdam:P30134` (dual-emit; rdac classes only)
- `rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`, `ec:EditorialWork` → `rdaw:P10088` (dual-emit)
- `vra:Image`, `vra:Work` → `vra:title` (dual-emit; VRA Core has its own title property)
- `rico:Record*` → `rico:hasOrHadTitle` (dual-emit; RiC-O; WEMI not applicable)
- `aco:AudioManifestation`, `mocho:ImageManifestation`, `mo:Musical*`, `ec:MediaResource`, `doco:*`, `frbr:Manifestation` → `dc:title` only (no vocab-specific title property)

---

## §3 alternative

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `alternative` (M classes) | `dcterms:alternative` | `rdam:P30128` "has variant title of manifestation" | `rdac:C10007`, `mocho:Manifestation` |
| `alternative` (W classes) | `dcterms:alternative` | `rdaw:P10086` "has variant title of work" | `rdac:C10001` |

Range: `rdfs:Literal` (lang-tagged string)

No equivalent found in VRA, RiC-O, MO, or ACO (`mapping_*_to_rda.csv`). RiC-O and all other non-RDA classes keep `dcterms:alternative` as-is.

---

## §4 creator

Range: `edm:Agent` (may carry GND URI in `resource` + role-annotated literal in `$`)

**Connected class**: `edm:Agent` → `rdaa:` properties (`prefLabel`, `altLabel`, `dateOfBirth`, `sameAs`, …). See `entity-property-mapping.md §1`.

Two independent dispatch tracks run for every `creator` value:

**Track 1 — class dispatch** (always runs): predicate is determined by the CHO's target class, looked up from `output/config/lookup_class_prop_alignment.csv` (creator rows to be populated). The `dc:creator` source predicate is the `edm_prop` key; the table provides `target_prop` per class.

**Track 2 — Agent URI resolution** (conditional): If the creator label matches an `edm:Agent` in the record whose `about` is a DDB organization URI (`http://www.deutsche-digitale-bibliothek.de/organization/…`) or GND URI (`http://d-nb.info/gnd/…`), emit:

```turtle
<cho> dcterms:creator <agent.about> .
```

If no matching Agent URI is found, do nothing (no literal fallback). See `transform-props-mapping-adr.md D7`.

**Agent node** (when URI resolves): also emit a stub node for the agent:

```turtle
<agent.about> a mocho:Agent ;
              rdfs:label "Lastname, Firstname" .
```

Label sourced from `edm:Agent.prefLabel[].$` (first value). Applies to both creator and contributor URI resolutions.

### §2.1 RDA creator properties

Generic properties only; typed subproperties (by agent type) are deferred — see `transform-future-plan.md §1`.

| WEMI | Property | label_full |
|---|---|---|
| M | `rdam:P30329` | "has creator agent of manifestation" |
| W | `rdaw:P10065` | "has creator agent of work" |
| E | `rdae:P20053` | "has creator agent of expression" |

---

## §5 contributor

Range: `edm:Agent` (most values are literals with role annotation in parentheses; ~62.6% carry a URI resolvable to DDB org or GND)

**Connected class**: `edm:Agent` (when URI present). See `entity-property-mapping.md §1`.

The target predicate depends on the LIDO event type of the `edm:Event` in which the contributor participates:

```
ProvidedCHO.hasMet[].resource  →  edm:Event.about
edm:Event.hasType.resource     →  LIDO event type URI
edm:Event.P11_had_participant[].resource  ==  contributor[].resource
→  emit <cho> <target_prop> <contributor.resource>
```

Fallback when no matching Event is found (URI absent or label-only): `dc:contributor`.

**LIDO event type → target predicate** (from `output/config/lido_event_types.csv`):

| LIDO event type | rdam: (M) | rdaw: (W) | vra:Image | vra:Work | rico: |
|---|---|---|---|---|---|
| lido00012 creation | `rdam:P30329` | `rdaw:P10065` | `vra:creator` | `vra:creator` | `rico:hasCreator` |
| lido00228 publication | `rdam:P30083` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `rico:hasPublisher` |
| lido00007 production | `rdam:P30081` | `dc:contributor` | `vra:producer` | `vra:producer` | `dc:contributor` |
| lido01127 photography | `rdam:P30329` | `rdaw:P10056` | `vra:photographer` | `vra:photographer` | `dc:contributor` |
| lido00224 designing | `dc:contributor` | `rdaw:P10051` | `vra:designer` | `vra:designer` | `dc:contributor` |
| lido00226 commissioning | `dc:contributor` | `rdaw:P10287` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
| all others | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` |

For `aco:`, `mo:`, `doco:`, `ec:`, `mocho:` subclasses: `dc:contributor` in all rows.

**Agent node** (when contributor URI resolves): same stub as creator — see §4:

```turtle
<contributor.resource> a mocho:Agent ;
                       rdfs:label "Lastname, Firstname" .
```

See `transform-props-mapping-adr.md D3`.

---

## §6 date

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `date` | `dc:date` | `rdam:P30278` "has date of manifestation" | Manifestation-level from `mapping_dct_to_rda.csv`; format varies: `"2018 (role)"`, `"18300213"` |
| `created` | `dc:created` | — (lookup only) | Work-level creation date; not emitted as a mocho triple; written to GND Werk lookup table (see `transform-revised-plan.md §1.2`) |

Range: `rdfs:Literal`

**Normalization** (corpus analysis `notes/corpus-analysis.md §2`):

- **Compact date YYYYMMDD → ISO 8601** (now): `"18300213"` → `"1830-02-13"`. Decided in `transform-script-adr.md`.
- **Range split** (now): ISO interval `"begin/end"` split on `/`; emit two `rdam:P30278` triples. `"1915-01-01/1920-12-31"` → `rdam:P30278 "1915-01-01"` + `rdam:P30278 "1920-12-31"` (16.7% of records). Decided in `transform-script-adr.md`.
- **Role annotation** (future): `"2018 (Fotografische Aufnahme)"` — do not strip; consider linking role string to other fields (e.g. `edm:Event.hasType`). Deferred.

---

## §7 issued

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `issued` | `dc:issued` | `rdam:P30278` "has date of manifestation" | Non-standard DC term; publication year collapses to same predicate as `date` (§6) |

Range: `rdfs:Literal` (lang-tagged literal year string)

Open: if `dc:issued` (publication date) should be distinguished from `dc:date` (general date), use `rdam:P30011` "has date of publication" — pending confirmation that `rdam:P30011` is in mocho.

---

## §25 hasMet

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hasMet` | `edm:hasMet` | keep `edm:hasMet` | No mocho/RDA equivalent; EDM structural link |

Range: `edm:Event`

**Connected class**: `edm:Event` — all four Event properties (`hasType`, `happenedAt`, `occuredAt`, `P11_had_participant`) are deferred pending CRM import. See `entity-property-mapping.md §8`.

---

## §12 identifier

Range: `rdfs:Literal` (string or array; values often include role annotation in parentheses, e.g. `"GSA 28/752"`, `"urn:nbn:…"`, `"http://d-nb.info/…"`)

**Step 1 (RDA)**: No entry for `dc:identifier` in `mapping_dct_to_rda.csv`. Closest RDA property is `rdam:P30004` "has identifier for manifestation" — not imported into mocho; deferred (see `transform-future-plan.md`).

**Step 2 (vocab-specific)**: RiC-O has `rico:hasOrHadIdentifier` (domain: `rico:Thing`, range: `rico:Identifier`). No identifier property in `mapping_vra_to_rda.csv`, `mapping_mo_to_rda.csv`, or ACO.

**Step 3 (lookup table)**: All non-RiC-O classes → `dc:identifier`; RiC-O classes → `rico:hasOrHadIdentifier`.

| target_class | wemi | target_prop | Notes |
|---|---|---|---|
| `rdac:C10007`, `mocho:Manifestation` | M | `dc:identifier` | No RDA mapping available |
| `rdac:C10001` | W | `dc:identifier` | No RDA mapping available |
| all non-RDA M/W classes | M/W | `dc:identifier` | Source predicate kept |
| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadIdentifier` | Native RiC-O identifier property |

**Step 4**: `dc:identifier` values are literals — no agent stub applies.

---

## §24 hasType

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `hasType` | `edm:hasType` | keep `edm:hasType` | No mocho/RDA equivalent |

Range: `skos:Concept` (resource refs — DDB internal IDs or GND/LIDO concept URIs)

**Connected class**: `skos:Concept` → `skos:prefLabel`, `skos:notation`. See `entity-property-mapping.md §7`.

---

## §23 hierarchyType

Range: `rdfs:Literal` controlled codes (e.g. `htype_030`, `htype_034`). Resolved against `lookup_vocnet.csv` (category `hierarchyType`) to a vocnet IRI.

**Step 1–2**: No RDA, VRA, MO, or ACO equivalent. `ddb:hierarchyType` source namespace preserved. `retype_entities()` also consumes this value to produce `rdf:type` triples (ADR D3) — the triple below is emitted in addition, not instead.

**Step 3 (lookup table)**: All classes → `ddb:hierarchyType`.

**Step 4**: URI-valued; vocnet IRI is the object. Re-emitted as `<cho> ddb:hierarchyType <http://ddb.vocnet.org/hierarchietyp/htXXX>` in the mocho subgraph.

---

## §15 dcType

Range: mixed — `rdfs:Literal` (72.4% label-only) or URI (27.6%: GND 55.9%, Getty AAT 32.2%, Wikidata 11.9%). See `corpus-analysis.md §2`.

Value-type dispatch runs before class dispatch, mirroring the `dc:subject` / `dcterms:subject` split:
- **Literal** (no `resource`): emit `<cho> dc:type "label"@lang` — all classes
- **URI** (`resource` present): emit `<cho> dcterms:type <uri>` + class-specific predicate (dual-emit for RDA/VRA classes) + Concept stub

**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdam:P30335` "has category of manifestation" (M) and `rdaw:P10004` "has category of work" (W). Both expect controlled vocabulary objects — URI path only.

**Step 2 (vocab-specific)**: RiC-O → `rico:hasOrHadType` (domain: `rico:Thing`, range: `rico:Type`) for URI path; `rico:type` (range: `rdfs:Literal`) for literal path. VRA Core 4 → `vra:worktype` (native property; not yet in `mapping_vra_to_rda.csv` — see `mocho/notes/mocho-gatherer-plan.md §Pending`). MO and ACO have no native type property in their mapping files.

**Step 3 (lookup table)** — URI path (when `dcType.resource` present):

| target_class | wemi | target_prop | Notes |
|---|---|---|---|
| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30335` | dual-emit: also `dcterms:type <uri>` |
| `rdac:C10001` | W | `rdaw:P10004` | dual-emit: also `dcterms:type <uri>` |
| `vra:Image` | M | `vra:worktype` | dual-emit: also `dcterms:type <uri>` |
| `vra:Work` | W | `vra:worktype` | dual-emit: also `dcterms:type <uri>` |
| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadType` | `<uri> a rico:Type` stub; no `dcterms:type` |
| all others (mo:, aco:, doco:, ec:, mocho:Image*, mocho:Immovable*) | M/W | `dcterms:type` | no class-specific predicate |

Literal path: all classes → `dc:type`.

**Step 4 (Concept stub)**: When `dcType.resource` is present, also emit a concept stub sourced from the in-record `Concept[]` node (URI match 99.9% for GND; see `corpus-analysis.md §2.2`):
- Non-RiC-O: `<concept-uri> a skos:Concept ; skos:prefLabel "..."@lang`
- RiC-O: `<concept-uri> a rico:Type` (same re-cast pattern as ADR D11)

---

## §8 description

Range: `rdfs:Literal` (lang-tagged string)

Class-specific dispatch via `output/config/lookup_class_prop_alignment.csv`:

| target_class | wemi | target_prop | Notes |
|---|---|---|---|
| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30137` "has note on manifestation" | RDA Manifestation-level generic note |
| `rdac:C10001` | W | `rdaw:P10330` "has note on work" | RDA Work-level generic note |
| `vra:Image`, `vra:Work` | M/W | `vra:description` | VRA Core has its own free-text description property; no RDA match in `mapping_vra_to_rda.csv` |
| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:note` | Native archival note property; no RDA match in `mapping_rico_to_rda.csv` |
| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dc:description` | No vocab-specific description property; source predicate kept |

Source: `mapping_dct_to_rda.csv` for RDA candidates; `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv` for vocab equivalents.

---

## §21 aggregationEntity

Range: `rdfs:Literal` (`"true"` / `"false"`). DDB-internal grouping flag indicating whether the record is an aggregation container rather than a leaf item.

**Step 1–2**: No RDA, VRA, RiC-O, MO, or ACO equivalent. Source namespace `ddb:` preserved.

**Step 3 (lookup table)**: All classes → `ddb:aggregationEntity`.

**Step 4**: Literal-valued; no stub. Re-emitted as `<cho> ddb:aggregationEntity "true"/"false"` in the mocho subgraph.

---

## §19 extent

Range: `rdfs:Literal` (lang-tagged; physical dimensions or pagination, e.g. `"V, 244 S."`, `"8,5 x 12 x 2,2 cm"`). 95,808 values; 47.6% pagination, 29.1% dimensions, 23.2% other (see `corpus-analysis.md §4`).

**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `dcterms:extent` → `rdam:P30182` "has extent of manifestation" (M-level). Values are free-text literals — not normalised to RDA-controlled extent vocabulary. WEMI mismatch is absent (M-level exists), but structured parse is required before dispatch → keep `dc:extent`.

**Step 2 (vocab-specific)**: VRA Core 4 → `vra:measurementsSet` (structured typed measurement — height/width/depth with unit fields); no plain-literal form available. RiC-O → `rico:hasExtent` (expects `rico:Extent` instance, not a literal). MO/ACO → no extent property. All require structured values → keep `dc:extent` for all classes.

**Step 3 (lookup table)**: All classes → `dc:extent`. See `transform-future-plan.md §8` for deferred structured-parse dispatch.

**Step 4**: Literal-valued; no stub.

---

## §20 edmType

Range: uppercase controlled string (`IMAGE`, `TEXT`, `SOUND`, `VIDEO`, `3D`). Resolved against `lookup_vocnet.csv` (category `mediaType`) to a vocnet IRI.

**Step 1–2**: No RDA, VRA, RiC-O, MO, or ACO equivalent. `mocho:mediaType` is the mocho-native property (ObjectProperty, domain `edm:ProvidedCHO`, range `skos:Concept`; defined in `mocho-edit.owl`). The mediatype dispatch also consumes this value to produce `rdf:type` triples (ADR D11/D12) — the triple below is emitted in addition.

**Step 3 (lookup table)**: All classes → `mocho:mediaType`.

**Step 4**: URI-valued; vocnet IRI is the object. Emitted as `<cho> mocho:mediaType <http://ddb.vocnet.org/medientyp/mtXXX>` in the mocho subgraph.

---

## §13 language

Range: `rdfs:Literal` (ISO 639-2 string, e.g. `"ger"`). Always co-occurs with `dcterms:language` (§14) — 62.1% of records have both, 37.9% have neither. `dc:language` carries the primary language only; `dcterms:language` is multi-valued (see `corpus-analysis.md §2`).

**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdae:P20006` "has language of expression" (E-level); `rdaw:P10353` "has language of representative expression" (W-level). No `rdam:` equivalent. WEMI mismatch for M-level nodes → keep `dc:language`.

**Step 2 (vocab-specific)**: VRA and MO have no language property. RiC-O has `rico:hasOrHadLanguage`, but its range is `rico:Language` (a URI-valued class), not a literal — `dc:language` is a plain ISO code string. No viable RiC-O mapping for the literal form → keep `dc:language` for all classes.

**Step 3 (lookup table)**: All classes → `dc:language`.

**Step 4**: Literal-valued; no stub.

---

## §14 dcTermsLanguage

Range: `dcterms:LinguisticSystem` (resource URI, e.g. `http://id.loc.gov/vocabulary/iso639-2/ger`). Same WEMI mismatch as §13 (see ADR D11).

**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdae:P20006` "has language of expression" (E-level); no `rdam:` equivalent. WEMI mismatch for M-level nodes → keep `dcterms:language`.

**Step 2 (vocab-specific)**: RiC-O has `rico:hasOrHadLanguage` (domain: `rico:Record*`, range: `rico:Language`). The LOC URI is re-cast as `rico:Language` per ADR D11. All other vocabularies have no language property → keep `dcterms:language`.

**Step 3 (lookup table)**:

| target_class | wemi | target_prop | Notes |
|---|---|---|---|
| `rdac:C10007`, `mocho:Manifestation`, all M non-RDA | M | `dcterms:language` | No rdam: equivalent; kept as-is |
| `rdac:C10001`, all W non-RDA | W | `dcterms:language` | WEMI mismatch; kept as-is |
| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadLanguage` | LOC URI re-typed as `rico:Language` (ADR D11) |

**Step 4 (URI stub)**: For RiC-O classes, also emit `<LOC-URI> a rico:Language`. This is distinct from agent stubs — no `rdfs:label` is added (authority label resides at the LOC endpoint). See ADR D11.

---

## §9 dcSubject

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcSubject` | `dc:subject` | via `emit_subject_triples()` (ADR D1) | Literal → `dc:subject`; IRI → promoted to `dcterms:subject` path |

Range: `rdfs:Literal` (literal-primary; some records carry GND URI in `resource` field)

Subject describes intellectual content — a Work-level concern. **`dc:subject` is only emitted for Work-level target classes** (`rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`). Manifestation-level classes receive `N/A` in `lookup_class_prop_alignment.csv` — no triple emitted. Domain-specific Work classes (`vra:Work`, `mo:MusicalWork`, `ec:EditorialWork`, `rico:*`) are `TBD`.

See `transform-props-mapping-adr.md D1` for full dispatch and deduplication logic.

---

## §10 dcTermsSubject / dcTermSubject

| Property | EDM IRI | Target predicate | Notes |
|---|---|---|---|
| `dcTermsSubject` / `dcTermSubject` | `dcterms:subject` | `rdaw:P10256` "has subject" (Work-level only) | Two keys, same predicate (D1); dedup by `(pred_nt, obj_nt)` per record |

Range: `skos:Concept` (resource refs — DDB internal IDs or GND URIs)

No Manifestation-level "has subject" exists in RDA — subject relationships describe intellectual content, not physical carrier. `rdaw:P10256` (Work-level) is therefore only emitted for Work-level target classes (`rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`). All Manifestation-level classes receive `N/A` in `lookup_class_prop_alignment.csv`. Domain-specific Work classes (`vra:Work`, `mo:MusicalWork`, `ec:EditorialWork`, `rico:*`) are `TBD`.

**Connected class**: `skos:Concept` → `skos:prefLabel`, `skos:notation`. See `entity-property-mapping.md §7`.

---

## §11 isPartOf

Range: IRI (parent DDB item URI or internal UUID) or plain literal (collection name string, ~1% of values).

Class-specific dispatch via `output/config/lookup_class_prop_alignment.csv`:

| target_class | wemi | target_prop | Notes |
|---|---|---|---|
| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30020` "is part of manifestation" | RDA Manifestation-level part relation |
| `rdac:C10001` | W | `rdaw:P10019` "is part of work" | RDA Work-level part relation |
| `vra:Image`, `vra:Work` | M/W | `vra:partOf` | Native VRA part relation; maps to `rdaw:P10019` per `mapping_vra_to_rda.csv` |
| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `dcterms:isPartOf` | No clean native RiC-O equivalent — `rico:isOrWasComponentOf` domain is `rico:Instantiation`, not `rico:RecordResource`; source predicate kept |
| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dcterms:isPartOf` | No vocab-specific part relation; source predicate kept |

**Connected class**: parent `ProvidedCHO` → same class dispatch applies recursively (parent item is typed independently during its own transform).

---

## §22 hierarchyPosition

Range: `rdfs:Literal` (zero-padded numeric string, e.g. `"000000000014848"`). DDB-internal sort key encoding the record's position within its hierarchy tree.

**Step 1–2**: No RDA, VRA, RiC-O, MO, or ACO equivalent. Source namespace `ddb:` preserved.

**Step 3 (lookup table)**: All classes → `ddb:hierarchyPosition`.

**Step 4**: Literal-valued; no stub. Re-emitted as `<cho> ddb:hierarchyPosition "000000000014848"` in the mocho subgraph.

---

## §17 currentLocation

Range: `edm:Place` (resource URI — DDB internal Place ID or GND place URI).

**Step 1 (RDA)**: `edm:currentLocation` is an EDM property, not in `mapping_dct_to_rda.csv`. No RDA equivalent.

**Step 2 (vocab-specific)**: Not in `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `mapping_mo_to_rda.csv`, or `mapping_aco_to_rda.csv`. No vocab-specific equivalent.

**Step 3**: All classes → keep `edm:currentLocation`.

**Step 4 (Place stub)**: Re-emit the matching `edm.RDF.Place[]` node in the mocho subgraph — sourced from `Place[].about == currentLocation.resource`. Emit all available properties: `geo:lat`, `geo:long`, `geo:alt`, `skos:prefLabel`, `skos:altLabel`, `owl:sameAs`. See `entity-property-mapping.md §3`.

---

## §18 format

Range: `rdfs:Literal` (lang-tagged free-text; technique/medium descriptions, e.g. "Kohlezeichnung (?) (Technik)", "Negativ in color, quer").

**Step 1 (RDA)**: `mapping_dct_to_rda.csv` maps `dc:format` to carrier/media/material properties (`rdam:P30001` "has carrier type", `rdam:P30002` "has media type", `rdam:P30208` "has base material of manifestation", and 50+ others). **All expect controlled vocabulary objects** — none are applicable to free-text strings. No clean RDA mapping.

**Step 2 (vocab-specific)**: `vra:material` → `rdam:P30208` (VRA mapping file). No equivalent in RiC-O, MO, or ACO mapping files. **All vocab-specific candidates also expect controlled vocabulary or structured values.**

**Step 3**: All classes → keep `dc:format`.

**Step 4**: Literal-valued; no stub.

KB linking and controlled-vocab dispatch deferred. See `transform-future-plan.md §7`.

---

## §16 spatial

**Step 1 (RDA)**: `dc:spatial` not in `mapping_dct_to_rda.csv`. No RDA equivalent.

**Step 2 (vocab-specific)**: Not in `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `mapping_mo_to_rda.csv`, or `mapping_aco_to_rda.csv`. No vocab-specific equivalent.

**Step 3**: All classes → keep `dc:spatial`.

**Step 4**: Object-valued (URI). Range is `edm:Place` — use resource URI directly as object: `<cho> dc:spatial <URI>`. No agent stub. 99.5% of spatial resource URIs equal the record's `Event.happenedAt` URIs — no event traversal needed (see `data/analysis/spatial_event_overlap.csv`).

---

## Summary: transform actions

| json_key | Current predicate | Change to | Status |
|---|---|---|---|
| `title` (Manifestation) | `dc:title` | `dc:title` + `rdam:P30134` | ☐ update |
| `title` (Work, W+M nodes) | `dc:title` | `dc:title` + `rdaw:P10088` | ☐ update |
| `description` | `dc:description` | `rdam:P30137` | ☐ update |
| `date` | `dc:date` | `rdam:P30278` | ☐ update |
| `issued` | `dc:issued` | `rdam:P30278` | ☐ update |
| `isPartOf` | `dcterms:isPartOf` | `rdam:P30020` | ☐ update |
| `alternative` (M) | `dcterms:alternative` | `rdam:P30128` | ✅ props-mapping D8 |
| `alternative` (W) | `dcterms:alternative` | `rdaw:P10086` | ✅ props-mapping D8 |
| `hierarchyType` | `ddb:hierarchyType` | no triple (dispatch) | ✅ implemented (D3) |
| `edmType` | `edm:type` | no triple (dispatch) | ✅ implemented (D11/D12) |
| `aggregationEntity` | `ddb:aggregationEntity` | skip | ☐ add skip |
| `hierarchyPosition` | `ddb:hierarchyPosition` | skip | ☐ add skip |
| `creator` (Agent resolved) | `dc:creator` | `dcterms:creator <URI>` | ✅ props-mapping D7 |
| `creator` (fallback literal) | `dc:creator` | `rdam:P30329` | ✅ D2 (IRI corrected from P30263) |
| `contributor` | `dc:contributor` | keep as-is | ✅ D8 |
| all others | — | keep as-is | ✅ no change |

---

## Files to update

| File | Action |
|---|---|
| `scripts/transform_edm_to_mocho.py` | Update 5 predicate strings (title, description, date, issued, isPartOf); add skip for aggregationEntity and hierarchyPosition |
| `notes/transform-adr.md` | New decisions D13–D17 for the 5 changed predicates |

