# Scripts

All scripts live in `scripts/`. They use project-relative paths via
`pathlib.Path(__file__).resolve().parent.parent`, so they can be run from
any working directory.

---

## Ontology alignment (run in order)

### `profile_edm_fields.py`
Profiles all field keys present under `edm.RDF.*` entity types in the JSONL
data file. Needed as input for `align_ddbedm_to_mocho.py`.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: `output/edm_field_profile.json`, `output/edm_field_profile.csv`
- **Usage**: `python3 scripts/profile_edm_fields.py`
- **Notes**: Reports per-entity-type field names with record counts and
  coverage percentages. Counts > 100% indicate array-valued entities
  (multiple agents/concepts/events per record).

### `align_ddbedm_to_mocho.py`
Data-driven ontology alignment from DDB-EDM to mocho. Maps each EDM/DC
property actually present in the data to its corresponding RDA properties
in mocho, via the DC→RDA sub-property mapping from the mocho workflow.

- **Input**: `output/edm_field_profile.json` (from above),
  `~/Documents/claude/mocho/ontology/ddbedm_1.0.ttl`,
  `~/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl`,
  `~/Documents/claude/mocho/output/mapping_dct_to_rda.csv`
- **Output**: `output/alignment_ddbedm_mocho.csv`,
  `output/alignment_ddbedm_mocho.json`
- **Usage**: `python3 scripts/align_ddbedm_to_mocho.py`
- **Dependencies**: `rdflib`
- **Notes**:
  - One CSV row per (edm_field × rda_property) pair; high-fanout DC terms
    (e.g. `dc:creator` → 232 RDA sub-properties) produce many rows per field
  - 32 DC/DCT fields matched to RDA properties in mocho (1,271 alignment rows)
  - 55 unmatched fields fall into expected categories: EDM-structural
    (`edm:isShownAt`, `edm:begin/end`), DDB extensions (`ddb:hierarchyType`,
    `ddb:aggregationEntity`), SKOS labels, geo coordinates, and two known
    DCT→RDA gaps (`dc:identifier`, `dcterms:spatial`)
  - `dcTermSubject` (DDB data variant of `dcterms:subject`) handled via
    hard-coded override in `OVERRIDES` dict

---

## Transform pipeline (run in order)

### `transform_edm_to_mocho.py`
Reference transform: DDB-EDM JSONL → mocho-aligned N-Triples + JSON-LD.
Decisions documented in `notes/transform-adr.md` (D1–D12).

- **Input**: `data/items-all-goethe-faust.json`, `data/ids-all-goethe-faust.txt`,
  `output/alignment_ddbedm_mocho.csv`, `output/lookup_htype_doco_rico.csv`
- **Output**: `output/mocho-goethe-faust.nt`, `output/mocho-goethe-faust.jsonld`,
  `output/transform_stats.json`
- **Usage**: `python transform_edm_to_mocho.py [--jsonl FILE] [--ids FILE] [--limit N]`
- **Notes**: Phase D will add dc:type dispatch (lookup_dctype_to_class.csv) and
  WebResource typing for mt002. See `notes/plan-goethe-faust-transform.md`.

### `count_dctype_by_mediatype.py`
Frequency count of dc:type × sector across all mediatypes. Prerequisite for
populating image and video config JSONs before Phase B.

- **Input**: `data/items/*.json`
- **Output**: `output/dctype_frequency_all.csv` (columns: mediatype, sector, dc_type_de, count)
- **Usage**: `python count_dctype_by_mediatype.py`

### `gen_image_type2class.py`
Generates `output/config/image_type2class.json` for mt002 dc:type dispatch.
Implements group-based model from `notes/image-type-class-mapping.md` (D11–D12):
Groups A–D (artwork, objects, photo, architecture) → W-slot classes; Group F → M-slot.

- **Input**: `output/dctype_frequency_all.csv`
- **Output**: `output/config/image_type2class.json`
- **Usage**: `python gen_image_type2class.py [--summary]`

### `gen_video_type2class.py`
Generates `output/config/video_type2class.json` for mt005 dc:type dispatch.
EBUCore Plus split: `EditorialWork` (editorial content) vs `MediaResource` (carrier/fragment).
Decisions in `notes/video-type-class-mapping.md`.

- **Input**: `output/dctype_frequency_all.csv`
- **Output**: `output/config/video_type2class.json`
- **Usage**: `python gen_video_type2class.py`

### `count_dctype_gnd_coverage.py`
Measures what fraction of dc:type values have a controlled-vocabulary URI
(GND preferred, Getty AAT accepted) via `edm.RDF.Concept` prefLabel match.
Exports dc_type_de → vocab URI mapping for use as `dnb_uri` column in
`lookup_dctype_to_class.csv`.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: `output/dctype_gnd_coverage.csv`, `output/dctype_to_gnd_uri.csv`
- **Usage**: `python scripts/count_dctype_gnd_coverage.py`
- **Notes**: 48.5% coverage corpus-wide; 356/1,033 unique dc:types have a vocab URI
  (237 GND, 119 Getty AAT). See `notes/plan-goethe-faust-transform.md` §3.0.

### `sample_type_dispatch.py`
Validates the dc:type dispatch table by sampling records per (mediatype, sector)
cell, running the three-level lookup (exact → any-sector → any-mediatype → D9
fallback) against `lookup_dctype_to_class.csv`, and reporting the assigned class.

- **Input**: `data/items-all-goethe-faust.json`, `output/lookup_dctype_to_class.csv`
- **Output**: `output/dctype_dispatch_sample.csv`, `output/dctype_dispatch_summary.csv`
- **Usage**: `python scripts/sample_type_dispatch.py [--sample-size N]`
- **Notes**: 76.0% matched (no fabio classes emitted); Photo 100% exact;
  Audio/Media Library 100% any-sector. See plan §3.2 for dispatch logic.

### `summarise_vocab_coverage.py`
Aggregates `output/dctype_gnd_coverage.csv` by (mediatype, sector) and writes
a human-readable summary of vocab URI coverage per cell.

- **Input**: `output/dctype_gnd_coverage.csv`
- **Output**: `output/vocab_coverage_summary.csv`
- **Usage**: `python scripts/summarise_vocab_coverage.py`
- **Notes**: 29 rows; columns: mediatype, sector, total, vocab_uri, pct.
  Source for the coverage table in `notes/plan-goethe-faust-transform.md` §3.0.

---

## Data pipeline (run in order)

### `gen_manifestation_types.py`
Emits `rdf:type` triples for every DDB object URI in the corpus. Items from
sector 2 (sparte002, library) or with a manifestation-level htype are typed as
`rda:Manifestation` (`rdaregistry.info/Elements/c/C10007`); all others as
`mocho:Manifestation`. Sector-2 check covers both the item's own
`provider-info.domains` and parent institution domains.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: `output/mocho-goethe-faust.nt`
- **Usage**: `python scripts/gen_manifestation_types.py`
- **Notes**: Manifestation htypes: htype_007 (Volume), htype_013 (Manuscript),
  htype_014 (Issue), htype_020 (Multivolume Work), htype_021 (Monograph),
  htype_025 (Review). Stats printed on completion.

### `fetch-search-all.py`
Fetches all DDB search results for the query "goethe" via the DDB Solr API
and merges them into a single JSON file.

- **Input**: DDB Solr API (live network access required)
- **Output**: `data/ddb-search-goethe-all.json`
- **Usage**: `python scripts/fetch-search-all.py`
- **Notes**: `TOTAL` must match the actual result count; update if the
  dataset changes. 0.3 s delay between requests to avoid rate-limiting.

### `build_dataframe.py`
Builds a flat per-object DataFrame from the raw JSONL.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: `output/items-dataframe.parquet` (115,398 × 10, 8.6 MB),
  `output/items-dataframe-sample.csv` (first 500 rows)
- **Columns**: `object_id`, `sector`, `provider_name`, `timespan_begin`,
  `timespan_end`, `dc_type` (list), `dc_subject` (list), `metadata_format`,
  `view_fields` (list), `digitized` (bool)
- **Usage**: `python scripts/build_dataframe.py`
- **Dependencies**: `pandas`, `pyarrow`
- **Notes**:
  - `YEAR_RE` handles both free-text years and compact YYYYMMDD dates
    (e.g. `18300213`) via two regex alternatives
  - `timespan_begin` priority: `edm.RDF.TimeSpan.begin` →
    `edm.RDF.TimeSpan.end` → `edm.RDF.ProvidedCHO.issued` (fallback)
  - After fixes: 12,958 records (~11.2%) still lack a `timespan_begin` year

---

## Analysis scripts

### `analyse_bucket.py`
Reports top N dc:type and dc:subject values for records within a given
`timespan_begin` year range. Reads from the parquet DataFrame.

- **Input**: `output/items-dataframe.parquet`
- **Output**: printed summary (or JSON with `--json`)
- **Usage**:
  ```
  python scripts/analyse_bucket.py --start 2000 --end 2024
  python scripts/analyse_bucket.py --start 2000 --end 2024 --top 10 --json
  ```
- **Dependencies**: `pandas`, `pyarrow`
- **Notes**: Useful for characterising anomalous buckets in `fig_years.png`
  (e.g. the 2000–2024 spike is dominated by Goethe-Universität Frankfurt
  institutional records — theses and working papers — rather than cultural
  heritage items)

### `analyse_items.py`
Aggregates item-level statistics across 6 dimensions from the raw JSONL.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: `output/items-analysis.json`
- **Usage**: `python scripts/analyse_items.py`

### `analyse_years.py`
Extracts creation years from `edm.RDF.TimeSpan`, selects an optimal bucket
size, and produces a bar chart. X-range restricted to 1600–present; linear
y-scale.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: `output/fig_years.png`, `output/years-analysis.json`
- **Usage**: `python scripts/analyse_years.py`
- **Notes**:
  - `YEAR_RE` handles YYYYMMDD dates; 85.8% of records have a usable year
  - Auto-selects bucket size (5 / 10 / 25 / 50 / 100 yr) to keep ≤ 45 bins;
    25-year buckets selected (18 non-empty bins from 1600+)
  - Pre-1600 records (n = 2,551) omitted from chart; included in JSON
  - Goethe era (1749–1832) highlighted in red
  - Bar counts: inside bars (white) for tall bars; above for short bars

### `audit_timespan_coverage.py`
Audits temporal coverage: for records missing a `TimeSpan` year, checks
whether `dc:date`, `dc:issued` (and dcterms equivalents) in `ProvidedCHO`
could provide a fallback year. Also reports all `ProvidedCHO` keys present
in those records, to identify further date-bearing fields.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: printed summary (no files written)
- **Usage**: `python scripts/audit_timespan_coverage.py`
- **Notes**: Led to discovery that `YEAR_RE` was broken for YYYYMMDD dates
  and that `issued` is a viable fallback; both fixes applied to
  `build_dataframe.py` and `analyse_years.py`

### `match_objecttypes.py`
Maps DDB objecttype strings to FaBiO / DoCO ontology classes using a
4-tier pipeline: exact match → translated exact match → Levenshtein →
sentence embeddings.

- **Input**: `data/ddb-search-goethe-all.json`, `data/schemas/fabio.owl`,
  `data/schemas/doco.owl`
- **Output**: `output/ddb-type2fabio.json`
- **Usage**: `python scripts/match_objecttypes.py`
- **Dependencies**: `deep-translator`, `rapidfuzz`, `sentence-transformers`,
  `rdflib`

### `summarise_results.py`
Prints a human-readable summary of `ddb-type2fabio.json`.

- **Input**: `output/ddb-type2fabio.json`
- **Output**: printed summary (no files written)
- **Usage**: `python scripts/summarise_results.py`

### `gen_htype_doco_mapping.py`
Matches htype label_en values against DoCO ontology class labels using four
strategies (exact, Levenshtein, translated, embedding). Writes mapping table.

- **Input**: `data/htype.csv`, `data/schemas/doco.owl`
- **Output**: `~/Documents/claude/mocho/output/mapping_htype_doco.csv`,
  `~/Documents/claude/mocho/output/mapping_htype_doco.json`
- **Usage**: `python scripts/gen_htype_doco_mapping.py`
- **Dependencies**: `rdflib`, `rapidfuzz`, `deep-translator`, `sentence-transformers`

### `check_isbd_titles.py`
Checks how many `ProvidedCHO.title` values contain ISBD punctuation marks.

- **Input**: `data/items-all-goethe-faust.json`
- **Output**: console summary; optional Markdown report (`--report PATH`)
- **Usage**: `python check_isbd_titles.py [--report PATH]`

---

## Visualisation scripts

### `visualise_items.py`
Generates figures from `items-analysis.json` (German labels, pre-translation).

- **Input**: `output/items-analysis.json`
- **Output**: `output/fig1_metadata_format.png`, `output/fig2_sparte.png`,
  `output/fig3_providers_top20.png`, `output/fig4_dc_type_top20.png`,
  `output/fig5_dc_subject_top30.png`, `output/fig6_view_fields_top20.png`
- **Usage**: `python scripts/visualise_items.py`
- **Notes**: Labels remain in German. Use `translate_and_plot.py` or
  `plot_latex_figs.py` for English-translated versions.

### `translate_and_plot.py`
Translates German labels with Helsinki-NLP/opus-mt-de-en and regenerates
all figures with English labels. Reads from the parquet DataFrame.

- **Input**: `output/items-dataframe.parquet`
- **Output**: `output/fig2_sector.png`, `output/fig4_dc_type_top20.png`,
  `output/fig5_dc_subject_top30.png`, `output/fig6_view_fields_top20.png`,
  `output/dataset-summary.png`
- **Usage**:
  ```
  HF_HOME=data/hf-cache HF_HUB_DISABLE_XET=1 python scripts/translate_and_plot.py
  ```
- **Dependencies**: `transformers`, `pandas`, `pyarrow`, `matplotlib`
- **Notes**: Model cached in `data/hf-cache/`. Manual overrides in `OVERRIDES`
  dict for domain-specific terms (Hochschulschrift, Druckgraphik, etc.)

### `plot_latex_figs.py`
Regenerates 4 figures as square 7×7 in PNGs (1050×1050 px) for a LaTeX
2×2 subfigure layout. Translates German labels via opus-mt-de-en.

- **Input**: `output/items-dataframe.parquet`
- **Output**: `output/fig1_metadata_format.png`, `output/fig2_sector.png`,
  `output/fig4_dc_type_top20.png`, `output/fig5_dc_subject_top20.png`
- **Usage**:
  ```
  HF_HOME=data/hf-cache HF_HUB_DISABLE_XET=1 python scripts/plot_latex_figs.py
  ```
- **Dependencies**: `transformers`, `pandas`, `pyarrow`, `matplotlib`
- **Notes**: `fig5` is top-20 subjects (not top-30). `fig1` uses explicit
  subplot margins (not `bbox_inches="tight"`) to preserve square aspect ratio.

### `extract_view_id_name.py`
Extracts unique `(id, name)` pairs from `view.fields` across all items in a
JSON or NDJSON file.

- **Input**: any JSON array or NDJSON file of item objects
- **Output**: JSON array of `[id, name]` tuples, one per line, sorted by id
- **Usage**: `python scripts/extract_view_id_name.py <input> <output>`
- **Example**:
  ```
  python scripts/extract_view_id_name.py data/items-all-goethe-faust.json output/view_id_name.json
  ```

### `extract_view_fields.py`
Extracts and pretty-prints `view.fields` for a single item by ID.

- **Input**: `data/items/<item-id>.json`
- **Output**: `view-<item-id>.json` (project root)
- **Usage**: `python scripts/extract_view_fields.py <item-id>`
- **Example**:
  ```
  python scripts/extract_view_fields.py 222SF6AM6ZCXSJTNREHJUCX5SRTJDBK7
  ```

---

## Data-collection scripts

### `fetch-items.sh`
Fetches DDB item records by ID from the DDB API, saves each as an individual
JSON file, and appends compact single-line JSON to the JSONL file. Skips IDs
already present in the JSONL. Must be run from the `data/` directory.

- **Input**: `<ids-file>` (one ID per line), optional `[limit]` count
- **Output**: `data/items/<uuid>.json` per record; appends to
  `data/items-all-goethe-faust.json`
- **Usage**:
  ```
  cd data && bash ../scripts/fetch-items.sh ids-all-goethe-faust.txt
  cd data && bash ../scripts/fetch-items.sh ids-missing.txt   # re-fetch gap
  ```
- **Notes**: 0.2 s delay between requests. HTTP failures are logged but do not
  abort the run; failed IDs can be re-fetched by running again.

### `find_missing_items.py`
Compares `ids-all-goethe-faust.txt` against `items-all-goethe-faust.json` and
writes the gap — IDs present in the list but absent from the JSONL — to
`ids-missing.txt` for targeted re-fetching.

- **Input**: `data/ids-all-goethe-faust.txt`, `data/items-all-goethe-faust.json`
- **Output**: `data/ids-missing.txt`
- **Usage**:
  ```
  python scripts/find_missing_items.py
  cd data && bash ../scripts/fetch-items.sh ids-missing.txt
  ```

### `fetch-progress.sh`
Shell script to monitor fetch progress.
