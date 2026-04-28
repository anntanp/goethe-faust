# Transform writeup: EDM → mocho N-Triples

## 1. Input structure

Each record in `data/items-all-goethe-faust.json` is one DDB cultural object (JSONL, one record per line):

```
edm.RDF
  ├── ProvidedCHO      ← the cultural object itself (title, creator, date, dc:type …)
  ├── WebResource      ← digital file URL(s)
  ├── PhysicalThing    ← archival containers (folder, box, fonds …)
  ├── Aggregation      ← Europeana aggregation metadata
  └── Concept[]        ← controlled-vocab terms: mediatype, sector, dc:type concepts
```

---

## 2. Three mapping layers

### 2.1 Property alignment (all entity types)

**File**: `output/alignment_ddbedm_mocho.csv`

For each entity (ProvidedCHO, WebResource, Aggregation …), the transform iterates its JSON keys and looks up `(entity_type, json_key)` in the alignment CSV. Each match gives one or more RDA predicate IRIs. Only rows where `in_mocho = True` are used.

Example: `ProvidedCHO.dcTitle` → `rdaw:P10088` (has title of work)

Three keys get special treatment (bypass the table):

| Key | Predicate | Reason |
|---|---|---|
| `creator` | `rdam:P30263` | Table had 464 overly-specific candidates; generic Manifestation-level property used |
| `contributor` | `dc:contributor` | No generic RDA equivalent in mocho's current import |
| `dcSubject` / `dcTermsSubject` / `dcTermSubject` | `dcterms:subject` (IRI values) or `dc:subject` (literals) | Three keys carry overlapping data; deduplicated before emit |

### 2.2 `rdf:type` via hierarchyType (htype)

**File**: `output/lookup_htype_doco_rico.csv`

`ProvidedCHO.hierarchyType` and `PhysicalThing.hierarchyType` carry archival hierarchy codes (`htype_030`–`htype_048`). The lookup maps each code to a DoCO or RiC-O class plus optional `rico:hasRecordSetType` values.

Example: `htype_036` → `rico:RecordSet` + `ric-rst:Fonds`

### 2.3 `rdf:type` via dc:type (domain-specific classes)

**File**: `output/lookup_dctype_to_class.csv`

The German free-text dc:type value (`"Fotografie"`, `"Zeichnung"` …) is looked up with three-level fallback:

```
exact   (mediatype, sector, dc_type_de)
  → any-sector  (mediatype, any, dc_type_de)
  → any-mediatype  (any, any, dc_type_de)
  → fallback: mocho:Manifestation
```

The table has WEMI slots (W, E, M, I):
- **W-slot** class found → emitted *instead of* `mocho:Manifestation` for ProvidedCHO
- **M-slot** class found → emitted *alongside* `mocho:Manifestation`
- No match → `mocho:Manifestation` only (D9 fallback)

Example: museum Zeichnung (mt002, sparte006) → `vra:Work` (W-slot)

Layers 2.2 and 2.3 are **independent** — both can fire for the same record.

#### 2.3.1 WebResource typing (mt002 / Photo only)

For photo records, each WebResource URI also gets:

```turtle
<wr-uri> a mocho:ImageObject ;
         a rdac:C10007 ;               # rdac:Item
         rdam:P30001 rdact:1018 ;      # has carrier type: still image
         vra:imageOf <cho-uri> .
```

---

## 3. What is NOT emitted: Concept entities

`Concept[]` entries are never written to the output. They are only *read* to extract:
- the mediatype IRI (e.g. `http://ddb.vocnet.org/medientyp/mt002`)
- the sector IRI (e.g. `http://ddb.vocnet.org/sparte/sparte006`)

These two values key into the dc:type dispatch table (§2.3).

---

## 4. Run results (full corpus, 2026-04-20)

| Stat | Value |
|---|---|
| Records processed | 115,432 |
| Triples out | 44.4M |
| dc:type W-slot matched | 13,392 |
| dc:type M-slot accumulated | 106 |
| dc:type fallback (mocho:Manifestation only) | 101,934 |
| WebResources typed (mt002) | 103,496 |

Verification: `output/transform_stats.json`
