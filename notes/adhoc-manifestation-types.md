# Ad-hoc: Manifestation type assignment (gen_manifestation_types.py)

**Date**: 2026-04-15
**Script**: `scripts/gen_manifestation_types.py`
**Output**: `output/mocho-goethe-faust.nt`

---

## Context

Quick N-Triples file that assigns `rdf:type` to each DDB object URI in the
Goethe-Faust corpus. Sector-2 (library) items get the stricter RDA class
`rda:Manifestation`; everything else gets the base `mocho:Manifestation`. This is
a prerequisite for the mocho ingest pipeline.

---

## Key facts

| Item | Value |
|---|---|
| Input | `data/items-all-goethe-faust.json` (JSONL, one JSON object per line) |
| URI field | `item["edm"]["RDF"]["ProvidedCHO"]["about"]` |
| Sector-2 test | any string in `provider-info.domains` **or** any parent's `domains` (via `provider-info.provider-parents.parents[].domains`) contains `"sparte002"` |
| htype test | `edm.RDF.ProvidedCHO.hierarchyType` is one of: `htype_007`, `htype_013`, `htype_014`, `htype_020`, `htype_021`, `htype_025` |
| Classification rule | sector2 **OR** htype-signals-manifestation → `rda:Manifestation`; else → `mocho:Manifestation` |
| `rda:Manifestation` IRI | `http://rdaregistry.info/Elements/c/C10007` |
| `mocho:Manifestation` IRI | `https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation` |
| `rdf:type` predicate | `http://www.w3.org/1999/02/22-rdf-syntax-ns#type` |

Manifestation htypes:

| Code | Label |
|---|---|
| htype_007 | Band / Volume |
| htype_013 | Handschrift / Manuscript |
| htype_014 | Heft / Issue |
| htype_020 | Mehrbändiges Werk / Multivolume Work |
| htype_021 | Monografie / Monograph |
| htype_025 | Rezension / Review |

---

## Logic

```python
is_sparte002 = any("sparte002" in (d or "") for d in all_domains)  # item + parents
is_htype_m   = htype in HTYPE_MANIFEST

cls = RDA_MANIFEST if (is_sparte002 or is_htype_m) else MOCHO_MANIFEST
```

---

## Results (2026-04-15)

```
Total triples written : 115,432
rda:Manifestation     :  54,347  (sector2: 54,337 / htype-only: 10)
mocho:Manifestation   :  61,085
Skipped               :       0
```

Nearly all rda:Manifestation assignments come from sector2; only 10 items were
caught by htype alone (the manifestation htypes are rare in this corpus).
