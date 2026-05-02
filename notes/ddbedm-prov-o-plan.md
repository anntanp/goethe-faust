# DDB-EDM PROV-O mapping plan

**Date**: 2026-05-01
**Status**: In progress
**Reference**: `references/rm-018-prov-o.pdf` (slides 11–16)
**ADR**: `notes/transform-adr.md` D11, D12
**JSON source**: `data/items-excerpt-1000.json`

---

## 1. Overview

The transform emits a PROV-O graph for each item using the **Without-Activity
pattern** (slide 13). The full Activity pattern (slide 12, with `prov:wasGeneratedBy`
+ `prov:used` + Ingest node) is not used — the added expressivity requires a
blank node or per-item IRI for the Ingest activity and is not needed for the
current use case.

Five nodes per item:

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

---

## 2. Graph structure (Without-Activity pattern)

```
ddb:CHO ──prov:wasDerivedFrom──────────► Dataset
        ──prov:wasAttributedTo──────────► XSLT
        ──prov:generatedAtTime──────────► "2026-01-07T15:40:43+0100"
        ──dcterms:hasVersion────────────► "43"
        ──dcterms:references────────────► "ddb:<source-ref>"

Dataset ──prov:wasAttributedTo──────────► Provider

XSLT    ──prov:actedOnBehalfOf──────────► DDB
```

---

## 3. JSON field → triple mapping

### 3.1 JSON source structure

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

### 3.2 CHO (`ddb:item/<properties.item-id>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `edm:ProvidedCHO`, `prov:Entity` |
| `prov:wasDerivedFrom` | `properties.dataset-id` → Dataset URN | URN |
| `prov:wasAttributedTo` | `properties.mapping-version` → XSLT URN | URN |
| `prov:generatedAtTime` | `properties.ingest-date` | xsd:dateTime literal |
| `dcterms:hasVersion` | `properties.revision-id` | string literal |
| `dcterms:references` | `source.description.record.ref` | `"ddb:<ref>"` literal |

### 3.3 Dataset (`urn:ddbedm:properties:dataset-id:<value>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `dcat:Dataset`, `prov:Entity` |
| `dcterms:identifier` | `properties.dataset-id` | string literal |
| `rdfs:label` | `properties.dataset-label` | `@de` literal |
| `dcterms:type` | `source.description.record.type` | URI |
| `prov:wasAttributedTo` | `provider-info.provider-ddb-id` → Provider URN | URN |

### 3.4 XSLT (`urn:ddbedm:properties:mapping-version:<value>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:SoftwareAgent` |
| `dcterms:hasVersion` | `properties.mapping-version` | string literal |
| `prov:actedOnBehalfOf` | fixed | `<http://www.deutsche-digitale-bibliothek.de>` |

### 3.5 DDB (`<http://www.deutsche-digitale-bibliothek.de>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Agent`, `foaf:Organization` |
| `foaf:name` | fixed | `"Deutsche Digitale Bibliothek"` |

### 3.6 Provider (`urn:ddbedm:provider-info:provider-ddb-id:<value>`)

| Triple | JSON path | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Agent`, `foaf:Organization` |
| `foaf:name` | `provider-info.provider-name` | string literal |
| `schema:url` | `provider-info.provider-uri` | URI |
| `dcterms:identifier` | `provider-info.provider-id` | string literal |
| `lov:isil` | `provider-info.provider-isil` | URI |

### 3.7 Source record (`ddb-api:items/<id>/source/record`)

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

---

## 4. Full Turtle example

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

---

## 5. Skipped fields

| JSON path | Reason |
|---|---|
| `properties.cortex-type` | Not modelled in PROV-O graph |
| `properties.automatically-translated` | Not modelled in PROV-O graph |
| `provider-info.provider-parent-id` | Not modelled in PROV-O graph |
| `provider-info.provider-logo` | Not modelled in PROV-O graph |

---

## 6. Prefix declarations

| Prefix | URI |
|---|---|
| `prov:` | `http://www.w3.org/ns/prov#` |
| `ddb:` | `http://www.deutsche-digitale-bibliothek.de/` |
| `ddb-api:` | `https://api.deutsche-digitale-bibliothek.de/2/` |
| `dcat:` | `http://www.w3.org/ns/dcat#` |
| `dc:` | `http://purl.org/dc/elements/1.1/` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `foaf:` | `http://xmlns.com/foaf/0.1/` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` |
| `schema:` | `https://schema.org/` |
| `lov:` | `http://www.w3.org/ns/iana/media-types/` |
