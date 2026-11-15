# Trace: rdac:C10001 emission → werk_staging (sparte002 Library)

**Date**: 2026-05-22  
**Related**: `transform-script-adr.md` D16, D26; `transform-adr.md` D17; `transform-bugs.md` B1

Documents the full call chain from dispatch config to N-Quads emission and
DuckDB staging row, using `rdac:C10001` (Work) as the concrete example.

---

## 1. Config source

`output/config/lookup_htype_doco_rico.csv` — htype rows that carry `rdac:C10001`
in the `rdf_type` column:

| htype_code | Label | rdf_type |
|---|---|---|
| htype_003 | Beigefügtes Werk | `rdac:C10001, rdac:C10007` |
| htype_006 | Aufsatz | `rdac:C10001, rdac:C10007` |
| htype_013 | Handschrift | `rdac:C10001, rdac:C10007` |
| htype_020 | Mehrbändiges Werk | `rdac:C10001, rdac:C10007` |
| htype_021 | Monografie | `rdac:C10001, rdac:C10007` |
| htype_022 | Musik | `rdac:C10001, mo:MusicalWork, rdac:C10007` |
| htype_023 | Fortlaufendes Sammelwerk | `rdac:C10001, rdac:C10007` |
| htype_025 | Rezension | `rdac:C10001, rdac:C10007` |
| htype_044 | Zeitung | `rdac:C10001, rdac:C10007` |

All are scoped to sparte002 Library. The `rdf_type` cell is comma-separated;
`rdac:C10001` is always first (most specific / W-slot).

---

## 2. Loader — `load_htype_map()` (`loaders.py:18`)

```
lookup_htype_doco_rico.csv
        │
        ▼  csv.DictReader → row["rdf_type"].split(",")
        │  _expand_prefix("rdac:C10001")
        │    → _PREFIXES["rdac"] = "http://rdaregistry.info/Elements/c/"
        │    → "http://rdaregistry.info/Elements/c/C10001"
        ▼
htype_map["htype_021"] = (
    ["http://rdaregistry.info/Elements/c/C10001",   # W
     "http://rdaregistry.info/Elements/c/C10007"],  # M
    []                                              # rst_iris (empty for library htypes)
)
```

Rows where `rdf_type` is empty or `"pending"` are excluded.

---

## 3. Dispatch gate — `retype_entities()` Layer 1 (`emitters.py:260`)

```
record → _extract_mediatype_sector(Concept[])
             → sector = "http://ddb.vocnet.org/sparte/sparte002"
             → mediatype = "http://ddb.vocnet.org/medientyp/mt003"
        │
        ▼  mediatype_class_map.get((sector, mediatype))
             → {"use_htype": True, "rdf_type_w": "", "rdf_type_m": "…rdac:C10007"}
        │
        ▼  if use_htype and htype_code:
             htype_code = "htype_021"  (from ProvidedCHO.hierarchyType)
             entry = htype_map["htype_021"]
```

`use_htype=True` is set in `lookup_mediatype_class.csv` for sparte002 × mt003.
For space-separated multi-htype values (e.g. `"htype_007 htype_020"`), only the
first code is used for class dispatch; all codes emit a `ddbedm:hierarchyType`
triple (D-script-ADR D?).

---

## 4. Emission — Layer 1 loop (`emitters.py:265`)

```python
type_iris = ["http://.../C10001", "http://.../C10007"]

for t in type_iris:
    lines.append(make_nq(cho_nt, "<rdf:type>", f"<{t}>", graph_iri))
# → two rdf:type triples:
#   <gemea-cho-uri>  rdf:type  rdac:C10001 .
#   <gemea-cho-uri>  rdf:type  rdac:C10007 .

primary_class = type_iris[0]   # → rdac:C10001
htype_used    = True
wemi          = _CLASS_WEMI["http://.../C10001"]  # → "W"
```

Layer 2 (fixed mediatype class) adds `rdac:C10007` again only if `rdf_type_m`
is set and `primary_class` is still empty — it is not empty here, so the Layer 2
M class is skipped for the primary slot. `rdac:C10007` is already present from
Layer 1.

---

## 5. werk_staging trigger — `werk_staging_row()` (`emitters.py:607`)

```python
_W_SLOT_CLASSES = frozenset({
    "http://rdaregistry.info/Elements/c/C10001",  # rdac:C10001
    "http://purl.org/ontology/mo/MusicalWork",    # mo:MusicalWork
})

if target_class not in _W_SLOT_CLASSES:
    return None           # ← skipped for all other classes
```

`target_class = "http://.../C10001"` → staging row is built and returned.
`transform.py` writes it to `<stem>-werk-staging.duckdb` via DuckDB append.

Staging row fields sourced from `ProvidedCHO`:

| Field | JSON path |
|---|---|
| `ddb_obj_id` | `ProvidedCHO.about` (32-char ID) |
| `cho_uri` | minted GeMeA URI (`gemea.ise.fiz-karlsruhe.de/mocho/<id>`) |
| `target_class` | `rdac:C10001` full IRI |
| `dc_title` | `ProvidedCHO.title[].@value` |
| `dc_alternative` | `ProvidedCHO.alternative[].$` |
| `dc_created` | `ProvidedCHO.date` |
| `creator_uris` | `ProvidedCHO.creator[].resource` (GND URIs) |
| `creator_literals` | `ProvidedCHO.creator[].$` |

---

## 6. Observed output — s2 run

```
gemea/output/s2-werk-staging.duckdb
  werk_staging: 36,197 rows
  target_class: http://rdaregistry.info/Elements/c/C10001 (100%)
```

All 36,197 rows are sparte002 Library records whose htype resolves to
`rdac:C10001`. These are staged for `link_gnd_works.py` (Phase 0) to mint
GeMeA Work URIs and run GND Werk authority lookups.

---

## 7. Full chain summary

```
lookup_htype_doco_rico.csv  (rdac:C10001 in rdf_type column)
        │
        ▼  load_htype_map() → _expand_prefix()
        │
htype_map["htype_0XX"] → ([C10001, C10007], [])
        │
        ▼  retype_entities() Layer 1
        │  use_htype=True (sparte002 × mt003 in lookup_mediatype_class.csv)
        │  htype_code present in record
        │
make_nq → rdf:type rdac:C10001  (W-slot triple, mocho graph)
make_nq → rdf:type rdac:C10007  (M-slot triple, mocho graph)
        │
        ▼  primary_class = rdac:C10001, wemi = "W"
        │
werk_staging_row()
  target_class ∈ _W_SLOT_CLASSES → staging row built
        │
        ▼
<stem>-werk-staging.duckdb  (consumed by link_gnd_works.py)
```
