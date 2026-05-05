# Transform stats plan

**Date**: 2026-05-05
**Status**: Implemented in `scripts/transform/transform_edm_to_mocho.py`
**Output**: `output/transform/<timestamp>/transform_stats.json`

---

## Stats levels (`--stats`)

Controlled by `--stats {none,basic,dispatch,full}` (default: `basic`).

| Level | Sections included | Extra cost at 27M records |
|---|---|---|
| `none` | nothing written | 0 |
| `basic` | `run`, `records`, `triples`, `werk_staging` | ~0 — Counter increments already in the hot path |
| `dispatch` | basic + `dispatch` (WEMI class counts, method counts) | ~0 — 1 dict lookup + 1 Counter increment per record |
| `full` | dispatch + `mocho_vocab` (property counts) | O(triples_mocho) — regex per mocho triple; use on corpus samples only |

**Recommendation for full-corpus runs**: use `--stats dispatch`. Run `--stats full` on a sample (`--limit 50000`) when you need vocabulary coverage data for the paper.

The bottleneck at `full` is the per-triple predicate regex in the mocho stream. At 27M records × ~50 mocho triples per record ≈ 1.35B regex matches, this adds several minutes even with a compiled pattern.

---

## Schema

```json
{
  "run": {
    "timestamp": "2026-05-05T09:26:58",
    "input":     "data/items-all-goethe-faust.json"
  },

  "records": {
    "processed":          115432,
    "skipped_not_in_ids": 0,
    "skipped_mt007":      4821,
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

  "dispatch": {
    "htype_hits":     42103,
    "mediatype_hits": 71204,
    "fallback_d9":    2125,
    "work_classes": {
      "rdac:C10001":        12380,
      "mo:MusicalWork":     3,
      "mocho:ImmovableWork": 148,
      "mocho:ImageWork":    449,
      "vra:Work":           207,
      "ec:EditorialWork":   205
    },
    "expression_classes": {},
    "manifestation_classes": {
      "rdac:C10007":              88412,
      "aco:AudioManifestation":   1843,
      "mo:MusicalManifestation":  3,
      "mocho:ImageManifestation": 9203,
      "mocho:Manifestation":      2125,
      "ec:MediaResource":         205,
      "vra:Image":                207,
      "doco:Section":             843,
      "doco:Part":                1204,
      "doco:Chapter":             412
    },
    "rico_classes": {
      "rico:RecordSet":  4821,
      "rico:Record":     3107,
      "rico:RecordPart": 289
    }
  },

  "mocho_vocab": {
    "properties_all": {
      "dc:title":              115432,
      "rdam:P30263":           91204,
      "rdam:P30278":           88412,
      "rdam:P30011":           44201,
      "rdaw:P10219":           12380,
      "rico:creationDate":     4821,
      "rico:hasRecordSetType": 8217
    },
    "properties_new": {
      "rdam:P30263":           91204,
      "rdam:P30278":           88412,
      "rdam:P30011":           44201,
      "rdaw:P10219":           12380,
      "rico:creationDate":     4821,
      "rico:hasRecordSetType": 8217
    }
  },

  "werk_staging": {
    "rows": 15,
    "by_class": {
      "rdac:C10001":    12,
      "mo:MusicalWork": 3
    }
  }
}
```

---

## Field rationale

### `run`
Reproducibility: timestamp links the stats file to the run directory; input path confirms which corpus was used.

### `records`
Pipeline accounting. Sum invariant:
```
processed = dispatch.htype_hits + dispatch.mediatype_hits + dispatch.fallback_d9 + skipped_mt007
```
`skipped_not_in_ids` counts records present in the JSONL but absent from the ID filter file. `skipped_mt007` records are included in `processed` but receive no mocho stream (D15).

### `triples.by_graph`
Validates the four-stream model: a graph at 0 triples signals a broken stream. `prov` carries ~1 triple per record (provenance stub); `ddbedm` is the largest stream (verbatim EDM passthrough). `werk` triples are written to DuckDB, not to the N-Quads file, so they are not counted here.

### `dispatch`
Core validation of §1.1 class assignment.

- `htype_hits` — records where htype drove primary class (sparte001/002 htype-first strata)
- `mediatype_hits` — records where mediatype lookup drove primary class
- `fallback_d9` — records that received `mocho:Manifestation` because no specific class resolved (D9); lower is better
- `work_classes`, `expression_classes`, `manifestation_classes`, `rico_classes` — per-class counts by WEMI slot; `expression_classes` is currently empty (no E-level dispatch implemented)

### `mocho_vocab`
Tracks which predicates are actually emitted in the mocho named graph.

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
| `dispatch.work_classes`, `dispatch.manifestation_classes`, `dispatch.rico_classes` | Ontology coverage — which WEMI levels and vocabularies are populated |
| `dispatch.fallback_d9` / `records.processed` | Alignment precision — share of corpus receiving specific typing vs. generic fallback |
| `mocho_vocab.properties_new` | New vocabulary in use — mocho/RDA properties are exercised, not just defined |
| `werk_staging.rows`, `werk_staging.by_class` | W-level entity resolution — evidence for GND Werk linking pipeline |

`properties_all` and an `ignored_properties` breakdown are useful for debugging and completeness audits but are reported in prose in the paper, not as tables.
