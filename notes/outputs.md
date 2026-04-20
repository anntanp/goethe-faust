# Outputs

Generated files produced by scripts in `scripts/`. Never hand-edit; always regenerate
from the producing script. Each entry records: path, schema, producing script, last
generated, and any downstream consumers.

---

## Transform outputs

### `output/mocho-goethe-faust.nt`

- **Format**: N-Triples (one triple per line)
- **Produced by**: `scripts/transform_edm_to_mocho.py`
- **Content**: mocho-aligned RDF triples for all 115,432 records (D1–D10 decisions)
- **Consumed by**: QLever ingest pipeline (GeMeA)
- **Note**: Phase D will add dc:type dispatch triples and mt002 WebResource typing

### `output/mocho-goethe-faust.jsonld`

- **Format**: JSON-LD
- **Produced by**: `scripts/transform_edm_to_mocho.py`
- **Content**: Same triples as `.nt`; for inspection and tooling only

### `output/transform_stats.json`

- **Format**: JSON
- **Produced by**: `scripts/transform_edm_to_mocho.py`
- **Content**: Run stats (record counts, missing types, ignored-properties inventory)

---

## Dispatch table outputs

### `output/lookup_htype_doco_rico.csv`

- **Format**: CSV
- **Produced by**: `scripts/gen_htype_doco_mapping.py`
- **Columns**: `htype_code`, `doco_class`, `rico_class`, ...
- **Content**: htype_001–048 → DoCO (library) or RiC-O (archival) class
- **Consumed by**: `transform_edm_to_mocho.py` (htype dispatch layer)

### `output/lookup_dctype_to_class.csv`

- **Format**: CSV
- **Produced by**: `scripts/gen_dctype_class_mapping.py` (Phase B — not yet written)
- **Columns**: `mediatype`, `sector`, `dc_type_de`, `dc_type_en`, `dnb_uri`,
  `rdf_type_w`, `rdf_type_e`, `rdf_type_m`, `rdf_type_i`, `source_vocab`, `notes`
- **Content**: (mediatype, sector, dc:type) → mocho-aligned rdf:type class IRIs
- **Lookup key**: `dc_type_de` (current); `dnb_uri` (future — Option 1)
- **Consumed by**: `transform_edm_to_mocho.py` (Phase D dc:type dispatch layer)

---

## Config outputs (input to gen_dctype_class_mapping.py)

### `output/config/image_type2class.json`

- **Format**: JSON, keyed by `dc_type_de__sparte<NNN>`
- **Produced by**: `scripts/gen_image_type2class.py`
- **Last generated**: 2026-04-17
- **Schema**: `{key: {dc_type_de, sector (IRI), count, class: [W, E, M, I], notes}}`
- **Content**: 851 entries; mt002 dc:type × sector → VRA/mocho class dispatch
- **Consumed by**: `gen_dctype_class_mapping.py` (Phase B)

### `output/config/video_type2class.json`

- **Format**: JSON, keyed by dc:type string
- **Produced by**: `scripts/gen_video_type2class.py`
- **Schema**: `{dc_type_de: {remarks, en, sectors, count, class: [W, E, M, I]}}`
- **Content**: 10 entries; mt005 dc:types → EBUCore Plus classes
- **Consumed by**: `gen_dctype_class_mapping.py` (Phase B)

---

## Frequency and coverage outputs

### `output/dctype_frequency_all.csv`

- **Format**: CSV
- **Produced by**: `scripts/count_dctype_by_mediatype.py`
- **Columns**: `mediatype`, `sector`, `dc_type_de`, `count`
- **Content**: 1,386 rows; dc:type frequency per (mediatype, sector) cell
- **Consumed by**: `gen_image_type2class.py`, `gen_video_type2class.py`

### `output/dctype_gnd_coverage.csv`

- **Format**: CSV
- **Produced by**: `scripts/count_dctype_gnd_coverage.py`
- **Last generated**: 2026-04-18
- **Columns**: `mediatype`, `sector`, `dc_type_de`, `count`, `gnd_uri`, `has_gnd`
- **Content**: Per (mediatype, sector, dc:type): occurrence count + vocab URI match (GND or Getty AAT)
- **Key finding**: 48.5% of dc:type occurrences have a GND or Getty AAT URI; 356/1,033 unique dc:types covered

### `output/dctype_dispatch_sample.csv`

- **Format**: CSV
- **Produced by**: `scripts/sample_type_dispatch.py`
- **Last generated**: 2026-04-18
- **Columns**: `mediatype_label`, `sector_label`, `record_id`, `dc_type_de`, `match_level`, `cho_class`, `source_vocab`, `note`, `mediatype`, `sector`
- **Content**: 142 rows (5 samples × 29 cells); sampled records with dispatch results for validation

### `output/dctype_dispatch_summary.csv`

- **Format**: CSV
- **Produced by**: `scripts/sample_type_dispatch.py`
- **Last generated**: 2026-04-18
- **Columns**: `mediatype_label`, `sector_label`, `total`, `exact`, `any_sector`, `any_mediatype`, `fallback`, `pct_matched`, `mediatype`, `sector`
- **Content**: 29 rows; per (mediatype, sector) dispatch match/fallback counts
- **Key finding**: 76.0% matched (70,608/92,853); 22,245 fallback to mocho:Manifestation; no fabio classes emitted

### `output/vocab_coverage_summary.csv`

- **Format**: CSV
- **Produced by**: `scripts/summarise_vocab_coverage.py`
- **Last generated**: 2026-04-18
- **Columns**: `mediatype`, `sector`, `total`, `vocab_uri`, `pct`
- **Content**: 29 rows; dc:type occurrence counts + vocab URI coverage per (mediatype, sector) cell
- **Source**: aggregated from `output/dctype_gnd_coverage.csv`

### `output/dctype_to_gnd_uri.csv`

- **Format**: CSV
- **Produced by**: `scripts/count_dctype_gnd_coverage.py`
- **Last generated**: 2026-04-18
- **Columns**: `dc_type_de`, `gnd_uri`
- **Content**: 356 rows; deduplicated dc:type → vocabulary URI mapping (237 GND, 119 Getty AAT; GND preferred when both present)
- **Note**: Column name `gnd_uri` is kept for schema stability; values may be Getty AAT URIs (`vocab.getty.edu/aat/`) where no GND URI exists
- **Consumed by**: `gen_dctype_class_mapping.py` (Phase B) — source for `dnb_uri` column

---

## Analysis outputs

### `output/alignment_ddbedm_mocho.csv` / `.json`

- **Format**: CSV + JSON
- **Produced by**: `scripts/align_ddbedm_to_mocho.py`
- **Content**: 1,271 rows; (edm_field, rda_property) alignment pairs
- **Consumed by**: `transform_edm_to_mocho.py` (property alignment layer)

### `output/edm_field_profile.csv` / `.json`

- **Format**: CSV + JSON
- **Produced by**: `scripts/profile_edm_fields.py`
- **Content**: Per-entity-type field coverage across corpus

### `output/items-dataframe.parquet`

- **Format**: Parquet
- **Produced by**: `scripts/build_dataframe.py`
- **Content**: 115,398 × 10 flat DataFrame; columns: object_id, sector, provider_name,
  timespan_begin, timespan_end, dc_type, dc_subject, metadata_format, view_fields, digitized
- **Consumed by**: `analyse_bucket.py`, `translate_and_plot.py`, `plot_latex_figs.py`
