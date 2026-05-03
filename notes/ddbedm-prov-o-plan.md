# DDB-EDM PROV-O mapping plan

**Date**: 2026-05-01 (updated 2026-05-03)
**Status**: In progress
**Reference**: `references/rm-018-prov-o.pdf` (slides 11–16)
**ADR**: `notes/transform-adr.md` D11, D12
**JSON source**: `data/items-excerpt-1000.json`

---

## 1. Overview

Two provenance layers:

| Layer | Granularity | Pattern | Storage |
|---|---|---|---|
| **1 — Item** | Per CHO: DDB-EDM source metadata | Without-Activity (slide 13) | Item's own named graph |
| **2 — Graph** | Per named graph: pipeline run that produced it | Full Activity (slide 12) | `<urn:goethe-faust:graph/prov>` |

Layer 1 answers: *where does this CHO's data come from in the DDB ecosystem?*
Layer 2 answers: *which script run, at what version and time, wrote triples into this graph — and was inference involved?*

---

## 2. Layer 1 — Fine-grained item provenance

### 2.1 Graph structure (Without-Activity pattern)

Five nodes per item. The full Activity pattern is not used — added expressivity
(blank node or per-item Activity IRI) is not justified for ingest-time metadata.

```
ddb:CHO ──prov:wasDerivedFrom──────────► Dataset
        ──prov:wasAttributedTo──────────► XSLT
        ──prov:generatedAtTime──────────► "2026-01-07T15:40:43+0100"
        ──dcterms:hasVersion────────────► "43"
        ──dcterms:references────────────► "ddb:<source-ref>"

Dataset ──prov:wasAttributedTo──────────► Provider

XSLT    ──prov:actedOnBehalfOf──────────► DDB
```

| Node | PROV-O type | URI pattern |
|---|---|---|
| CHO | `prov:Entity` | `ddb:item/<properties.item-id>` |
| Dataset | `dcat:Dataset`, `prov:Entity` | `urn:ddbedm:properties:dataset-id:<id>` |
| XSLT | `prov:SoftwareAgent` | `urn:ddbedm:properties:mapping-version:<ver>` |
| Provider | `prov:Agent`, `foaf:Organization` | `urn:ddbedm:provider-info:provider-ddb-id:<id>` |
| DDB | `prov:Agent`, `foaf:Organization` | `<http://www.deutsche-digitale-bibliothek.de>` (fixed) |

**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key
chain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without
requiring a dereferenceable endpoint.

### 2.2 JSON field → triple mapping

#### 2.2.1 JSON source structure

The relevant fields are spread across three top-level blocks:

```json
{
  "properties": {
    "item-id":            "222NZKK63TNRLC2VETRV722VKBDSUVGL",
    "dataset-id":         "76409877634279609sQOu",
    "dataset-label":      "Gesamtlieferung: Deutsche Fotothek - LIDO",
    "revision-id":        "43",
    "ingest-date":        "2026-01-07T15:40:43+0100",
    "mapping-version":    "6.18",
    "cortex-type":        "Kultur"
  },
  "provider-info": {
    "provider-name":      "Deutsche Fotothek",
    "provider-uri":       "http://www.deutschefotothek.de",
    "provider-id":        "99900890",
    "provider-ddb-id":    "CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI",
    "provider-isil":      "http://ld.zdb-services.de/resource/organisations/DE-2396"
  },
  "source": {
    "description": {
      "record": {
        "ref":  "222NZKK63TNRLC2VETRV722VKBDSUVGL",
        "href": "/items/222NZKK63TNRLC2VETRV722VKBDSUVGL/source/record",
        "type": "http://www.lido-schema.org/"
      }
    }
  },
  "binaries": {
    "binary": [
      {
        "ref":            "0ac6ad6e-a985-4251-91ca-f4b918326ead",
        "name":           "Abb. Vorsatz. Titelblatt auf fliegendem Blatt...",
        "name2":          "Urheber*in: DDZ (Fotografische Aufnahme)",
        "kind":           "http://rightsstatements.org/vocab/InC/1.0/",
        "local_pathname": "http://fotothek.slub-dresden.de/fotos/df_pos-2018-a_0000067_000_f.jpg",
        "primary":        true
      }
    ]
  }
}
```

#### 2.2.2 CHO (`ddb:item/<properties.item-id>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `edm:ProvidedCHO`, `prov:Entity` |
| `prov:wasDerivedFrom` | `properties.dataset-id` → Dataset URN | URN |
| `prov:wasAttributedTo` | `properties.mapping-version` → XSLT URN | URN |
| `prov:generatedAtTime` | `properties.ingest-date` | xsd:dateTime literal |
| `dcterms:hasVersion` | `properties.revision-id` | string literal |
| `dcterms:references` | `source.description.record.ref` | `"ddb:<ref>"` literal |

#### 2.2.3 Dataset (`urn:ddbedm:properties:dataset-id:<value>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `dcat:Dataset`, `prov:Entity` |
| `dcterms:identifier` | `properties.dataset-id` | string literal |
| `rdfs:label` | `properties.dataset-label` | `@de` literal |
| `dcterms:type` | `source.description.record.type` | URI |
| `prov:wasAttributedTo` | `provider-info.provider-ddb-id` → Provider URN | URN |

#### 2.2.4 XSLT (`urn:ddbedm:properties:mapping-version:<value>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:SoftwareAgent` |
| `dcterms:hasVersion` | `properties.mapping-version` | string literal |
| `prov:actedOnBehalfOf` | fixed | `<http://www.deutsche-digitale-bibliothek.de>` |

#### 2.2.5 DDB (`<http://www.deutsche-digitale-bibliothek.de>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Agent`, `foaf:Organization` |
| `foaf:name` | fixed | `"Deutsche Digitale Bibliothek"` |

#### 2.2.6 Provider (`urn:ddbedm:provider-info:provider-ddb-id:<value>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Agent`, `foaf:Organization` |
| `foaf:name` | `provider-info.provider-name` | string literal |
| `schema:url` | `provider-info.provider-uri` | URI |
| `dcterms:identifier` | `provider-info.provider-id` | string literal |
| `lov:isil` | `provider-info.provider-isil` | URI |

#### 2.2.7 Source record (`ddb-api:items/<id>/source/record`)

URI constructed from `source.description.href` by stripping the leading `/` and
prepending `ddb-api: <https://api.deutsche-digitale-bibliothek.de/2/>`.

One block of triples per `binaries.binary[i]` entry:

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Entity` |
| `dc:identifier` | `binaries.binary[i].ref` | string literal |
| `dc:title` | `binaries.binary[i].name` | `@de` literal |
| `dc:description` | concat(`name2 \| name`) | `@de` literal (nulls → `""`) |
| `dcterms:rights` | `binaries.binary[i].kind` | URI |
| `dcterms:source` | `binaries.binary[i].local_pathname` | URI |

### 2.3 Full Turtle example

```turtle
@prefix prov:     <http://www.w3.org/ns/prov#> .
@prefix ddb:      <http://www.deutsche-digitale-bibliothek.de/> .
@prefix ddb-api:  <https://api.deutsche-digitale-bibliothek.de/2/> .
@prefix dcat:     <http://www.w3.org/ns/dcat#> .
@prefix dc:       <http://purl.org/dc/elements/1.1/> .
@prefix dcterms:  <http://purl.org/dc/terms/> .
@prefix foaf:     <http://xmlns.com/foaf/0.1/> .
@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema:   <https://schema.org/> .
@prefix lov:      <http://www.w3.org/ns/iana/media-types/> .

# ── CHO ───────────────────────────────────────────────────────────────────────

ddb:item/222NZKK63TNRLC2VETRV722VKBDSUVGL
    a prov:Entity ;
    prov:wasDerivedFrom
        <urn:ddbedm:properties:dataset-id:76409877634279609sQOu> ;
    prov:wasAttributedTo
        <urn:ddbedm:properties:mapping-version:6.18> ;
    prov:generatedAtTime "2026-01-07T15:40:43+0100" ;
    dcterms:hasVersion   "43" ;
    dcterms:references   "ddb:222NZKK63TNRLC2VETRV722VKBDSUVGL" .

# ── Dataset ───────────────────────────────────────────────────────────────────

<urn:ddbedm:properties:dataset-id:76409877634279609sQOu>
    a dcat:Dataset, prov:Entity ;
    dcterms:identifier "76409877634279609sQOu" ;
    rdfs:label         "Gesamtlieferung: Deutsche Fotothek - LIDO"@de ;
    dcterms:type       <http://www.lido-schema.org/> ;
    prov:wasAttributedTo
        <urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .

# ── XSLT SoftwareAgent ────────────────────────────────────────────────────────

<urn:ddbedm:properties:mapping-version:6.18>
    a prov:SoftwareAgent ;
    dcterms:hasVersion "6.18" ;
    prov:actedOnBehalfOf <http://www.deutsche-digitale-bibliothek.de> .

# ── DDB Agent ─────────────────────────────────────────────────────────────────

<http://www.deutsche-digitale-bibliothek.de>
    a prov:Agent, foaf:Organization ;
    foaf:name "Deutsche Digitale Bibliothek" .

# ── Provider Agent ────────────────────────────────────────────────────────────

<urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
    a prov:Agent, foaf:Organization ;
    foaf:name          "Deutsche Fotothek" ;
    schema:url         <http://www.deutschefotothek.de> ;
    dcterms:identifier "99900890" ;
    lov:isil           <http://ld.zdb-services.de/resource/organisations/DE-2396> .

# ── Source record ─────────────────────────────────────────────────────────────

ddb-api:items/222NZKK63TNRLC2VETRV722VKBDSUVGL/source/record
    a prov:Entity ;
    dc:identifier  "0ac6ad6e-a985-4251-91ca-f4b918326ead" ;
    dc:title       "Abb. Vorsatz. Titelblatt auf fliegendem Blatt..."@de ;
    dc:description "Urheber*in: DDZ (Fotografische Aufnahme) | Abb. Vorsatz. Titelblatt..."@de ;
    dcterms:rights <http://rightsstatements.org/vocab/InC/1.0/> ;
    dcterms:source <http://fotothek.slub-dresden.de/fotos/df_pos-2018-a_0000067_000_f.jpg> .
```

### 2.4 Skipped fields

| JSON path | Reason |
|---|---|
| `properties.cortex-type` | Not modelled in PROV-O graph |
| `properties.automatically-translated` | Not modelled in PROV-O graph |
| `provider-info.provider-parent-id` | Not modelled in PROV-O graph |
| `provider-info.provider-logo` | Not modelled in PROV-O graph |

---

## 3. Layer 2 — Graph-level pipeline provenance

### 3.1 Design

Layer 2 uses the **full Activity pattern** (slide 12): each named graph in the
triplestore is a `prov:Entity`; each script run that produced it is a
`prov:Activity`; the script binary is a `prov:SoftwareAgent`.

All Layer 2 triples are stored in a single meta-graph:
`<urn:goethe-faust:graph/prov>`.

URI patterns:

| Resource | URI pattern |
|---|---|
| Named graph | `urn:goethe-faust:graph/<name>` |
| Script run (Activity) | `urn:goethe-faust:run/<script-stem>/<ISO8601-timestamp>` |
| Script agent | `urn:goethe-faust:agent/<script-stem>` |
| LLM agent | `urn:goethe-faust:agent/<model-id>` |

The `gf:inferenceMethod` property flags the epistemic status of graph contents:

| Value | Meaning |
|---|---|
| `gf:Deterministic` | Pure rule-based transform; output is fully reproducible |
| `gf:Heuristic` | Rule-based with uncertain matches (e.g. title-string GND lookup) |
| `gf:NER` | Triples derived from NER model output |
| `gf:LLMGenerated` | Triples produced or ranked by an LLM |

### 3.2 Named graphs catalogue

| Named graph | Producing script | Inference method |
|---|---|---|
| `urn:goethe-faust:graph/transform` | `transform_edm_to_mocho.py` | `gf:Deterministic` |
| `urn:goethe-faust:graph/gnd-agents` | `link_gnd_agents.py` | `gf:Heuristic` |
| `urn:goethe-faust:graph/gnd-works` | `link_gnd_works.py` | `gf:Heuristic` |
| `urn:goethe-faust:graph/ner` | NER script (TBD) | `gf:NER` |
| `urn:goethe-faust:graph/llm` | LLM enrichment script (TBD) | `gf:LLMGenerated` |
| `urn:goethe-faust:graph/prov` | all scripts (self-referential) | `gf:Deterministic` |

### 3.3 Triple mapping

Each script run writes the following triples into `<urn:goethe-faust:graph/prov>`.

#### 3.3.1 Named graph node (`urn:goethe-faust:graph/<name>`)

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Entity` |
| `prov:wasGeneratedBy` | runtime | run IRI |
| `gf:inferenceMethod` | script config | `gf:` vocab term |

#### 3.3.2 Run node (`urn:goethe-faust:run/<script-stem>/<timestamp>`)

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Activity` |
| `prov:startedAtTime` | runtime | xsd:dateTime |
| `prov:endedAtTime` | runtime | xsd:dateTime |
| `prov:wasAssociatedWith` | script config | script agent IRI |
| `prov:used` | script config | input graph IRI(s) |
| `rdfs:comment` | optional | free-text note |

#### 3.3.3 Script agent (`urn:goethe-faust:agent/<script-stem>`)

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:SoftwareAgent` |
| `rdfs:label` | script header | filename string |
| `dcterms:hasVersion` | script header or git tag | string literal |

For LLM agents, add:

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:SoftwareAgent` |
| `rdfs:label` | config | model name string |
| `dcterms:hasVersion` | config | model version / API version |
| `gf:modelProvider` | config | string literal (e.g. `"Anthropic"`) |

### 3.4 Turtle example

One run of `transform_edm_to_mocho.py` and one run of `link_gnd_agents.py`,
stored in the prov graph.

```turtle
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix gf:      <urn:goethe-faust:vocab/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .

# ── Named graph entities ──────────────────────────────────────────────────────

<urn:goethe-faust:graph/transform>
    a prov:Entity ;
    prov:wasGeneratedBy <urn:goethe-faust:run/transform_edm_to_mocho/2026-05-03T09:14:22Z> ;
    gf:inferenceMethod  gf:Deterministic .

<urn:goethe-faust:graph/gnd-agents>
    a prov:Entity ;
    prov:wasGeneratedBy <urn:goethe-faust:run/link_gnd_agents/2026-05-03T10:02:47Z> ;
    gf:inferenceMethod  gf:Heuristic .

# ── Run: transform ────────────────────────────────────────────────────────────

<urn:goethe-faust:run/transform_edm_to_mocho/2026-05-03T09:14:22Z>
    a prov:Activity ;
    prov:startedAtTime    "2026-05-03T09:14:22Z"^^xsd:dateTime ;
    prov:endedAtTime      "2026-05-03T09:31:05Z"^^xsd:dateTime ;
    prov:wasAssociatedWith <urn:goethe-faust:agent/transform_edm_to_mocho> ;
    prov:used             <urn:goethe-faust:graph/raw-json> .

<urn:goethe-faust:agent/transform_edm_to_mocho>
    a prov:SoftwareAgent ;
    rdfs:label         "transform_edm_to_mocho.py" ;
    dcterms:hasVersion "0.9.1" .

# ── Run: GND agent linking ────────────────────────────────────────────────────

<urn:goethe-faust:run/link_gnd_agents/2026-05-03T10:02:47Z>
    a prov:Activity ;
    prov:startedAtTime    "2026-05-03T10:02:47Z"^^xsd:dateTime ;
    prov:endedAtTime      "2026-05-03T10:44:19Z"^^xsd:dateTime ;
    prov:wasAssociatedWith <urn:goethe-faust:agent/link_gnd_agents> ;
    prov:used             <urn:goethe-faust:graph/transform> ;
    rdfs:comment          "lobid-gnd API; confidence threshold 0.85" .

<urn:goethe-faust:agent/link_gnd_agents>
    a prov:SoftwareAgent ;
    rdfs:label         "link_gnd_agents.py" ;
    dcterms:hasVersion "0.3.0" .

# ── Example: LLM enrichment run (when applicable) ────────────────────────────

<urn:goethe-faust:graph/llm>
    a prov:Entity ;
    prov:wasGeneratedBy <urn:goethe-faust:run/llm_enrich/2026-05-03T11:00:00Z> ;
    gf:inferenceMethod  gf:LLMGenerated .

<urn:goethe-faust:run/llm_enrich/2026-05-03T11:00:00Z>
    a prov:Activity ;
    prov:startedAtTime    "2026-05-03T11:00:00Z"^^xsd:dateTime ;
    prov:endedAtTime      "2026-05-03T11:28:33Z"^^xsd:dateTime ;
    prov:wasAssociatedWith <urn:goethe-faust:agent/claude-sonnet-4-6> ;
    prov:used             <urn:goethe-faust:graph/transform> .

<urn:goethe-faust:agent/claude-sonnet-4-6>
    a prov:SoftwareAgent ;
    rdfs:label         "claude-sonnet-4-6" ;
    dcterms:hasVersion "claude-sonnet-4-6" ;
    gf:modelProvider   "Anthropic" .
```

---

## 4. Prefix declarations

| Prefix | URI |
|---|---|
| `prov:` | `http://www.w3.org/ns/prov#` |
| `gf:` | `urn:goethe-faust:vocab/` |
| `ddb:` | `http://www.deutsche-digitale-bibliothek.de/` |
| `ddb-api:` | `https://api.deutsche-digitale-bibliothek.de/2/` |
| `dcat:` | `http://www.w3.org/ns/dcat#` |
| `dc:` | `http://purl.org/dc/elements/1.1/` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `foaf:` | `http://xmlns.com/foaf/0.1/` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` |
| `schema:` | `https://schema.org/` |
| `lov:` | `http://www.w3.org/ns/iana/media-types/` |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` |
