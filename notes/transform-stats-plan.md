# Transform stats plan

**Date**: 2026-05-06
**Status**: Implemented in `scripts/transform/` package
**Output**: `output/transform/<timestamp>/transform_stats.json`

---

## Stats levels (`--stats`)

Controlled by `--stats {none,basic,dispatch,full}` (default: `basic`).

| Level | Sections included | Extra cost at 27M records |
|---|---|---|
| `none` | nothing written | 0 |
| `basic` | `run`, `records`, `triples`, `werk_staging` | ~0 |
| `dispatch` | basic + `dispatch`, `records.by_mediatype`, `records.by_htype`, `ddbedm_classes`, `ddbedm_vocab`, `mocho_vocab` | ~0 — all from emitter Counters and dict lookups |
| `full` | same as `dispatch` (reserved for future additions) | same |

**Recommendation for full-corpus runs**: `--stats dispatch`. All predicate and class counts are collected during emission — no post-hoc N-Quad scanning.

---

## Schema

```json
{
  "run": {
    "timestamp":   "2026-05-06T09:26:58",
    "input":       "data/items-all-goethe-faust.json",
    "stats_level": "dispatch"
  },

  "records": {
    "processed":          115432,
    "skipped_not_in_ids": 0,
    "by_mediatype": {
      "mt003": 52247,
      "mt002": 19154,
      "mt007": 42361,
      "mt001": 466,
      "mt005": 96
    },
    "by_htype": {
      "ht021": 20000,
      "ht030": 500,
      "ht034": 800
    },
    "uri_sanitized":   29,
    "uri_split":       4188,
    "uri_about_split": 1309,
    "errors": {
      "json_parse": 0,
      "transform":  0
    }
  },

  "triples": {
    "total":    14709858,
    "by_graph": {
      "ddbedm": 8241000,
      "mocho":  5768000,
      "prov":   691843
    }
  },

  "ddbedm_classes": {
    "edm:ProvidedCHO":   115432,
    "edm:WebResource":   312538,
    "edm:Agent":         421026,
    "edm:Place":         117058,
    "edm:TimeSpan":       98910,
    "edm:PhysicalThing":  55771,
    "ore:Aggregation":   115432,
    "skos:Concept":       28000
  },

  "ddbedm_vocab": {
    "properties_all": {
      "dc:title":        115432,
      "dc:creator":       88000,
      "edm:type":        115432,
      "dc:date":          72000
    }
  },

  "dispatch": {
    "htype_hits":     42103,
    "mediatype_hits": 71204,
    "fallback_d9":    2125,
    "skipped_mt007":  42361,
    "work_classes": {
      "rdac:C10001":         12380,
      "mo:MusicalWork":          3,
      "mocho:ImmovableWork":   148,
      "mocho:ImageWork":       449,
      "vra:Work":              207,
      "ec:EditorialWork":      205
    },
    "expression_classes": {},
    "manifestation_classes": {
      "rdac:C10007":              88412,
      "aco:AudioManifestation":    1843,
      "mo:MusicalManifestation":      3,
      "mocho:ImageManifestation":  9203,
      "mocho:Manifestation":       2125,
      "ec:MediaResource":           205,
      "vra:Image":                  207,
      "doco:Section":               843,
      "doco:Part":                 1204,
      "doco:Chapter":               412
    },
    "rico_classes": {
      "rico:RecordSet":  4821,
      "rico:Record":     3107,
      "rico:RecordPart":  289
    }
  },

  "mocho_vocab": {
    "properties_all": {
      "dc:title":              115432,
      "rdam:P30263":            91204,
      "rdam:P30278":            88412,
      "rdam:P30011":            44201,
      "rdaw:P10219":            12380,
      "rico:creationDate":       4821,
      "rico:hasRecordSetType":   8217
    },
    "properties_new": {
      "rdam:P30263":            91204,
      "rdam:P30278":            88412,
      "rdam:P30011":            44201,
      "rdaw:P10219":            12380,
      "rico:creationDate":       4821,
      "rico:hasRecordSetType":   8217
    }
  },

  "werk_staging": {
    "rows": 15,
    "by_class": {
      "rdac:C10001":    12,
      "mo:MusicalWork":  3
    }
  }
}
```

---

## Field rationale

### `run`
Reproducibility: timestamp links the stats file to the run directory; input path confirms which corpus was used; `stats_level` records which sections are present.

### `records`
Pipeline accounting. Sum invariant:
```
processed = dispatch.htype_hits + dispatch.mediatype_hits + dispatch.fallback_d9 + skipped_mt007
```
`skipped_not_in_ids` counts records present in the JSONL but absent from the ID filter file.

`by_mediatype` — mediatype distribution within the run (short codes: `mt001`–`mt007`). Since each production run is per-sector, this shows the content-type mix for that sector. Values sum to `records.processed`.

`by_htype` — hierarchy type distribution (short codes: `ht021`, `ht030`, etc.). Empty for sectors with no htype (sparte005, sparte006). Values sum to records that carry a `hierarchyType` field.

`uri_sanitized` — count of IRI object values that contained characters illegal in N-Triples IRI references (RFC 3987 + NT spec: `[\x00-\x20<>"{}|\\^\x7f]`) and were percent-encoded before emission. Applied inside `value_to_nt_obj` via `_sanitize_iri` (ported from `gemea/scripts/py/export_ddb.py`). Counted across both ddbedm and mocho streams.

`uri_split` — count of individual URIs extracted from `resource` fields that contained multiple space-separated URIs (a DDB data quality issue). Each such field is split on whitespace; each part is emitted as a separate triple. Counted across both ddbedm and mocho streams. In the goethe-faust corpus: 1,250 affected fields across `currentLocation`, `isShownAt`, `isShownBy`, `object`, subject fields, `creator`, `contributor`, `happenedAt`.

`uri_about_split` — count of extra `owl:sameAs` triples emitted for entities whose `about` field contained multiple space-separated URIs. The first URI is used as the RDF subject; each additional URI generates one `owl:sameAs` triple anchoring it to the primary subject. In the goethe-faust corpus: 1,178 affected entities (`Place`, `WebResource`, `Agent`), producing 1,309 extra triples.

### `triples.by_graph`
Validates the four-stream model: a graph at 0 triples signals a broken stream. `prov` carries ~1 triple per record; `ddbedm` is the largest stream (verbatim EDM passthrough). `werk` triples go to DuckDB, not to the N-Quads file.

### `ddbedm_classes`
Entity class instance counts in the ddbedm passthrough graph — derived from `_EDM_ENTITY_TYPES` during emission, no N-Quad scanning. `edm:ProvidedCHO` count equals `records.processed` (every record has exactly one). Other classes vary: `edm:WebResource` reflects digitised items, `edm:Agent` reflects named persons/organisations. `ore:Aggregation` is included; its prefix (`ore: http://www.openarchives.org/ore/terms/`) is registered in `_PREFIXES`.

Used in the paper to characterise ddbedm graph structure per sector.

### `ddbedm_vocab`
Predicate counts for the ddbedm passthrough graph — derived from `_DDBEDM_PROP` during emission. `properties_all` covers every predicate used across all entity types. Includes `rdf:type` (shown as full IRI `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` since `rdf:` is not registered in `_PREFIXES`); class instance counts are separately available in `ddbedm_classes`.

### `dispatch`
Core validation of §1.1 class assignment.

- `htype_hits` — records where htype drove primary class (htype-first strata)
- `mediatype_hits` — records where mediatype lookup drove primary class
- `fallback_d9` — records that received `mocho:Manifestation` because no specific class resolved (D9); lower is better
- `work_classes`, `expression_classes`, `manifestation_classes`, `rico_classes` — per-class counts by WEMI slot; `expression_classes` is currently empty (no E-level dispatch implemented)

### `mocho_vocab`
Predicate counts for the mocho named graph — derived from emitter Counters during emission, no post-hoc N-Quad regex.

- `properties_all` — every predicate used in the mocho stream, including passthrough EDM/DC properties; ordered by frequency
- `properties_new` — subset of `properties_all` restricted to namespaces introduced by the mocho alignment (RDA, RiCO, mocho, VRA, MO, ACO, EBUCore, DoCO); confirms that alignment predicates are exercised

New namespace prefixes counted under `properties_new`:
`rdam`, `rdaw`, `rdae`, `rdac`, `rico`, `ric-rst`, `mocho`, `vra`, `mo`, `aco`, `ec`, `doco`

### `werk_staging`
GND Werk linking staging table. `by_class` confirms only W-slot classes (`rdac:C10001`, `mo:MusicalWork`) produce staging rows, consistent with D26.

---

## Resource paper relevance

| Stat | Paper use |
|---|---|
| `records.processed`, `triples.total`, `triples.by_graph` | Dataset scale — corpus size and graph model coverage |
| `records.by_mediatype`, `records.by_htype` | Content characterisation per sector |
| `ddbedm_classes` | ddbedm graph structural completeness per sector |
| `dispatch.work_classes`, `dispatch.manifestation_classes`, `dispatch.rico_classes` | Ontology coverage — which WEMI levels and vocabularies are populated |
| `dispatch.fallback_d9` / `records.processed` | Alignment precision — share of corpus receiving specific typing vs. generic fallback |
| `mocho_vocab.properties_new` | New vocabulary in use — mocho/RDA properties are exercised, not just defined |
| `werk_staging.rows`, `werk_staging.by_class` | W-level entity resolution — evidence for GND Werk linking pipeline |
