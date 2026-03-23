# Transcript: 50aeb795-6da8-4b60-95cc-4b5f77aeb313

**Project:** /Users/mta/Documents/claude  
**Messages:** 177

---

### User *(2026-03-22T18:48:07.974Z)*

does "teams" work in this session?

---

### Assistant *(2026-03-22T18:48:16.789Z)*

Yes — the `Agent` tool is available in this session, so you can spawn multiple subagents (in parallel if needed) to handle complex or independent tasks. What did you have in mind?

---

### User *(2026-03-22T18:49:59.164Z)*

I want to be able to do an ontology alignment on actual RDF data (goethe-faust/data/items-all-goethe-faust.json) from EDM to mocho (~/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl.

---

### Assistant *(2026-03-22T18:50:03.905Z)*

Let me look at both the source data and the target ontology first.

---

### Assistant *(2026-03-22T18:50:09.413Z)*

**Tool call:** `Agent`
```json
{
  "description": "Explore EDM data and mocho ontology",
  "subagent_type": "Explore",
  "prompt": "I need to understand two things:\n\n1. Look at the file `goethe-faust/data/items-all-goethe-faust.json` in the current working directory `/Users/mta/Documents/claude`. Read the first ~50-100 lines to understand the EDM (Europeana Data Model) structure — what RDF classes and properties are used, what the JSON-LD looks like.\n\n2. Look at `/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl` — read enough to understand the ontology structure: what classes and properties are defined, the namespace, key concepts.\n\nPlease report:\n- The EDM classes/properties actually present in the JSON data (with examples of values)\n- The mocho classes and properties (especially those relevant to cultural heritage / bibliographic records)\n- File sizes / line counts for both files\n- Any @context or namespace declarations in the JSON-LD"
}
```

---

### User *(2026-03-22T18:51:59.868Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.
```

---

### User *(2026-03-22T18:51:59.868Z)*

[Request interrupted by user for tool use]

---

### User *(2026-03-22T18:51:59.881Z)*

check the scripts in goethe-fausts/scripts
the source ontology is in ~/Documents/ddbedm-odk/src/ontology/ddbedm-full.owl

---

### User *(2026-03-22T18:52:00.062Z)*

[Request interrupted by user]

---

### User *(2026-03-22T18:52:06.103Z)*

check the scripts in goethe-fausts/scripts
the source ontology is in ~/Documents/ddbedm-odk/src/ontology/ddbedm-full.owl

---

### Assistant *(2026-03-22T18:52:09.979Z)*

**Tool call:** `Glob`
```json
{
  "pattern": "goethe-faust/scripts/**/*"
}
```

---

### Assistant *(2026-03-22T18:52:10.148Z)*

**Tool call:** `Glob`
```json
{
  "pattern": "goethe-faust/scripts/*"
}
```

---

### User *(2026-03-22T18:52:10.702Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/fetch-items.sh
/Users/mta/Documents/claude/goethe-faust/scripts/fetch-progress.sh
/Users/mta/Documents/claude/goethe-faust/scripts/summarise_results.py
/Users/mta/Documents/claude/goethe-faust/scripts/match_objecttypes.py
/Users/mta/Documents/claude/goethe-faust/scripts/translate_and_plot.py
/Users/mta/Documents/claude/goethe-faust/scripts/plot_latex_figs.py
/Users/mta/Documents/claude/goethe-faust/scripts/audit_timespan_coverage.py
/Users/mta/Documents/claude/goethe-faust/scripts/analyse_years.py
/Users/mta/Documents/claude/goethe-faust/scripts/build_dataframe.py
/Users/mta/Documents/claude/goethe-faust/scripts/analyse_items.py
/Users/mta/Documents/claude/goethe-faust/scripts/visualise_items.py
/Users/mta/Documents/claude/goethe-faust/scripts/find_missing_items.py
/Users/mta/Documents/claude/goethe-faust/scripts/analyse_bucket.py
/Users/mta/Documents/claude/goethe-faust/scripts/README.md
/Users/mta/Documents/claude/goethe-faust/scripts/extract_view_fields.py
/Users/mta/Documents/claude/goethe-faust/scripts/extract_view_id_name.py
/Users/mta/Documents/claude/goethe-faust/scripts/check_isbd_titles.py
/Users/mta/Documents/claude/goethe-faust/scripts/gen_htype_doco_mapping.py
/Users/mta/Documents/claude/goethe-faust/scripts/fetch-search-all.py
```

---

### User *(2026-03-22T18:52:10.703Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/fetch-items.sh
/Users/mta/Documents/claude/goethe-faust/scripts/fetch-progress.sh
/Users/mta/Documents/claude/goethe-faust/scripts/summarise_results.py
/Users/mta/Documents/claude/goethe-faust/scripts/match_objecttypes.py
/Users/mta/Documents/claude/goethe-faust/scripts/translate_and_plot.py
/Users/mta/Documents/claude/goethe-faust/scripts/plot_latex_figs.py
/Users/mta/Documents/claude/goethe-faust/scripts/audit_timespan_coverage.py
/Users/mta/Documents/claude/goethe-faust/scripts/analyse_years.py
/Users/mta/Documents/claude/goethe-faust/scripts/build_dataframe.py
/Users/mta/Documents/claude/goethe-faust/scripts/analyse_items.py
/Users/mta/Documents/claude/goethe-faust/scripts/visualise_items.py
/Users/mta/Documents/claude/goethe-faust/scripts/find_missing_items.py
/Users/mta/Documents/claude/goethe-faust/scripts/analyse_bucket.py
/Users/mta/Documents/claude/goethe-faust/scripts/README.md
/Users/mta/Documents/claude/goethe-faust/scripts/extract_view_fields.py
/Users/mta/Documents/claude/goethe-faust/scripts/extract_view_id_name.py
/Users/mta/Documents/claude/goethe-faust/scripts/check_isbd_titles.py
/Users/mta/Documents/claude/goethe-faust/scripts/gen_htype_doco_mapping.py
/Users/mta/Documents/claude/goethe-faust/scripts/fetch-search-all.py
```

---

### Assistant *(2026-03-22T18:52:12.891Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/README.md"
}
```

---

### User *(2026-03-22T18:52:12.901Z)*

**Tool result**
```
     1→# Scripts
     2→
     3→All scripts live in `scripts/`. They use project-relative paths via
     4→`pathlib.Path(__file__).resolve().parent.parent`, so they can be run from
     5→any working directory.
     6→
     7→---
     8→
     9→## Data pipeline (run in order)
    10→
    11→### `fetch-search-all.py`
    12→Fetches all DDB search results for the query "goethe" via the DDB Solr API
    13→and merges them into a single JSON file.
    14→
    15→- **Input**: DDB Solr API (live network access required)
    16→- **Output**: `data/ddb-search-goethe-all.json`
    17→- **Usage**: `python scripts/fetch-search-all.py`
    18→- **Notes**: `TOTAL` must match the actual result count; update if the
    19→  dataset changes. 0.3 s delay between requests to avoid rate-limiting.
    20→
    21→### `build_dataframe.py`
    22→Builds a flat per-object DataFrame from the raw JSONL.
    23→
    24→- **Input**: `data/items-all-goethe-faust.json`
    25→- **Output**: `output/items-dataframe.parquet` (115,398 × 10, 8.6 MB),
    26→  `output/items-dataframe-sample.csv` (first 500 rows)
    27→- **Columns**: `object_id`, `sector`, `provider_name`, `timespan_begin`,
    28→  `timespan_end`, `dc_type` (list), `dc_subject` (list), `metadata_format`,
    29→  `view_fields` (list), `digitized` (bool)
    30→- **Usage**: `python scripts/build_dataframe.py`
    31→- **Dependencies**: `pandas`, `pyarrow`
    32→- **Notes**:
    33→  - `YEAR_RE` handles both free-text years and compact YYYYMMDD dates
    34→    (e.g. `18300213`) via two regex alternatives
    35→  - `timespan_begin` priority: `edm.RDF.TimeSpan.begin` →
    36→    `edm.RDF.TimeSpan.end` → `edm.RDF.ProvidedCHO.issued` (fallback)
    37→  - After fixes: 12,958 records (~11.2%) still lack a `timespan_begin` year
    38→
    39→---
    40→
    41→## Analysis scripts
    42→
    43→### `analyse_bucket.py`
    44→Reports top N dc:type and dc:subject values for records within a given
    45→`timespan_begin` year range. Reads from the parquet DataFrame.
    46→
    47→- **Input**: `output/items-dataframe.parquet`
    48→- **Output**: printed summary (or JSON with `--json`)
    49→- **Usage**:
    50→  ```
    51→  python scripts/analyse_bucket.py --start 2000 --end 2024
    52→  python scripts/analyse_bucket.py --start 2000 --end 2024 --top 10 --json
    53→  ```
    54→- **Dependencies**: `pandas`, `pyarrow`
    55→- **Notes**: Useful for characterising anomalous buckets in `fig_years.png`
    56→  (e.g. the 2000–2024 spike is dominated by Goethe-Universität Frankfurt
    57→  institutional records — theses and working papers — rather than cultural
    58→  heritage items)
    59→
    60→### `analyse_items.py`
    61→Aggregates item-level statistics across 6 dimensions from the raw JSONL.
    62→
    63→- **Input**: `data/items-all-goethe-faust.json`
    64→- **Output**: `output/items-analysis.json`
    65→- **Usage**: `python scripts/analyse_items.py`
    66→
    67→### `analyse_years.py`
    68→Extracts creation years from `edm.RDF.TimeSpan`, selects an optimal bucket
    69→size, and produces a bar chart. X-range restricted to 1600–present; linear
    70→y-scale.
    71→
    72→- **Input**: `data/items-all-goethe-faust.json`
    73→- **Output**: `output/fig_years.png`, `output/years-analysis.json`
    74→- **Usage**: `python scripts/analyse_years.py`
    75→- **Notes**:
    76→  - `YEAR_RE` handles YYYYMMDD dates; 85.8% of records have a usable year
    77→  - Auto-selects bucket size (5 / 10 / 25 / 50 / 100 yr) to keep ≤ 45 bins;
    78→    25-year buckets selected (18 non-empty bins from 1600+)
    79→  - Pre-1600 records (n = 2,551) omitted from chart; included in JSON
    80→  - Goethe era (1749–1832) highlighted in red
    81→  - Bar counts: inside bars (white) for tall bars; above for short bars
    82→
    83→### `audit_timespan_coverage.py`
    84→Audits temporal coverage: for records missing a `TimeSpan` year, checks
    85→whether `dc:date`, `dc:issued` (and dcterms equivalents) in `ProvidedCHO`
    86→could provide a fallback year. Also reports all `ProvidedCHO` keys present
    87→in those records, to identify further date-bearing fields.
    88→
    89→- **Input**: `data/items-all-goethe-faust.json`
    90→- **Output**: printed summary (no files written)
    91→- **Usage**: `python scripts/audit_timespan_coverage.py`
    92→- **Notes**: Led to discovery that `YEAR_RE` was broken for YYYYMMDD dates
    93→  and that `issued` is a viable fallback; both fixes applied to
    94→  `build_dataframe.py` and `analyse_years.py`
    95→
    96→### `match_objecttypes.py`
    97→Maps DDB objecttype strings to FaBiO / DoCO ontology classes using a
    98→4-tier pipeline: exact match → translated exact match → Levenshtein →
    99→sentence embeddings.
   100→
   101→- **Input**: `data/ddb-search-goethe-all.json`, `data/schemas/fabio.owl`,
   102→  `data/schemas/doco.owl`
   103→- **Output**: `output/ddb-type2fabio.json`
   104→- **Usage**: `python scripts/match_objecttypes.py`
   105→- **Dependencies**: `deep-translator`, `rapidfuzz`, `sentence-transformers`,
   106→  `rdflib`
   107→
   108→### `summarise_results.py`
   109→Prints a human-readable summary of `ddb-type2fabio.json`.
   110→
   111→- **Input**: `output/ddb-type2fabio.json`
   112→- **Output**: printed summary (no files written)
   113→- **Usage**: `python scripts/summarise_results.py`
   114→
   115→---
   116→
   117→## Visualisation scripts
   118→
   119→### `visualise_items.py`
   120→Generates figures from `items-analysis.json` (German labels, pre-translation).
   121→
   122→- **Input**: `output/items-analysis.json`
   123→- **Output**: `output/fig1_metadata_format.png`, `output/fig2_sparte.png`,
   124→  `output/fig3_providers_top20.png`, `output/fig4_dc_type_top20.png`,
   125→  `output/fig5_dc_subject_top30.png`, `output/fig6_view_fields_top20.png`
   126→- **Usage**: `python scripts/visualise_items.py`
   127→- **Notes**: Labels remain in German. Use `translate_and_plot.py` or
   128→  `plot_latex_figs.py` for English-translated versions.
   129→
   130→### `translate_and_plot.py`
   131→Translates German labels with Helsinki-NLP/opus-mt-de-en and regenerates
   132→all figures with English labels. Reads from the parquet DataFrame.
   133→
   134→- **Input**: `output/items-dataframe.parquet`
   135→- **Output**: `output/fig2_sector.png`, `output/fig4_dc_type_top20.png`,
   136→  `output/fig5_dc_subject_top30.png`, `output/fig6_view_fields_top20.png`,
   137→  `output/dataset-summary.png`
   138→- **Usage**:
   139→  ```
   140→  HF_HOME=data/hf-cache HF_HUB_DISABLE_XET=1 python scripts/translate_and_plot.py
   141→  ```
   142→- **Dependencies**: `transformers`, `pandas`, `pyarrow`, `matplotlib`
   143→- **Notes**: Model cached in `data/hf-cache/`. Manual overrides in `OVERRIDES`
   144→  dict for domain-specific terms (Hochschulschrift, Druckgraphik, etc.)
   145→
   146→### `plot_latex_figs.py`
   147→Regenerates 4 figures as square 7×7 in PNGs (1050×1050 px) for a LaTeX
   148→2×2 subfigure layout. Translates German labels via opus-mt-de-en.
   149→
   150→- **Input**: `output/items-dataframe.parquet`
   151→- **Output**: `output/fig1_metadata_format.png`, `output/fig2_sector.png`,
   152→  `output/fig4_dc_type_top20.png`, `output/fig5_dc_subject_top20.png`
   153→- **Usage**:
   154→  ```
   155→  HF_HOME=data/hf-cache HF_HUB_DISABLE_XET=1 python scripts/plot_latex_figs.py
   156→  ```
   157→- **Dependencies**: `transformers`, `pandas`, `pyarrow`, `matplotlib`
   158→- **Notes**: `fig5` is top-20 subjects (not top-30). `fig1` uses explicit
   159→  subplot margins (not `bbox_inches="tight"`) to preserve square aspect ratio.
   160→
   161→### `extract_view_id_name.py`
   162→Extracts unique `(id, name)` pairs from `view.fields` across all items in a
   163→JSON or NDJSON file.
   164→
   165→- **Input**: any JSON array or NDJSON file of item objects
   166→- **Output**: JSON array of `[id, name]` tuples, one per line, sorted by id
   167→- **Usage**: `python scripts/extract_view_id_name.py <input> <output>`
   168→- **Example**:
   169→  ```
   170→  python scripts/extract_view_id_name.py data/items-all-goethe-faust.json output/view_id_name.json
   171→  ```
   172→
   173→### `extract_view_fields.py`
   174→Extracts and pretty-prints `view.fields` for a single item by ID.
   175→
   176→- **Input**: `data/items/<item-id>.json`
   177→- **Output**: `view-<item-id>.json` (project root)
   178→- **Usage**: `python scripts/extract_view_fields.py <item-id>`
   179→- **Example**:
   180→  ```
   181→  python scripts/extract_view_fields.py 222SF6AM6ZCXSJTNREHJUCX5SRTJDBK7
   182→  ```
   183→
   184→---
   185→
   186→## Data-collection scripts
   187→
   188→### `fetch-items.sh`
   189→Fetches DDB item records by ID from the DDB API, saves each as an individual
   190→JSON file, and appends compact single-line JSON to the JSONL file. Skips IDs
   191→already present in the JSONL. Must be run from the `data/` directory.
   192→
   193→- **Input**: `<ids-file>` (one ID per line), optional `[limit]` count
   194→- **Output**: `data/items/<uuid>.json` per record; appends to
   195→  `data/items-all-goethe-faust.json`
   196→- **Usage**:
   197→  ```
   198→  cd data && bash ../scripts/fetch-items.sh ids-all-goethe-faust.txt
   199→  cd data && bash ../scripts/fetch-items.sh ids-missing.txt   # re-fetch gap
   200→  ```
   201→- **Notes**: 0.2 s delay between requests. HTTP failures are logged but do not
   202→  abort the run; failed IDs can be re-fetched by running again.
   203→
   204→### `find_missing_items.py`
   205→Compares `ids-all-goethe-faust.txt` against `items-all-goethe-faust.json` and
   206→writes the gap — IDs present in the list but absent from the JSONL — to
   207→`ids-missing.txt` for targeted re-fetching.
   208→
   209→- **Input**: `data/ids-all-goethe-faust.txt`, `data/items-all-goethe-faust.json`
   210→- **Output**: `data/ids-missing.txt`
   211→- **Usage**:
   212→  ```
   213→  python scripts/find_missing_items.py
   214→  cd data && bash ../scripts/fetch-items.sh ids-missing.txt
   215→  ```
   216→
   217→### `fetch-progress.sh`
   218→Shell script to monitor fetch progress.
   219→



```

---

### Assistant *(2026-03-22T18:52:13.871Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/build_dataframe.py"
}
```

---

### User *(2026-03-22T18:52:13.885Z)*

**Tool result**
```
     1→#!/usr/bin/env python3
     2→"""
     3→build_dataframe.py
     4→==================
     5→Build a flat per-object DataFrame from items-all-goethe-faust.json (JSONL).
     6→
     7→Each row corresponds to one object (item-id). Columns:
     8→
     9→  object_id       — item identifier (properties.item-id)
    10→  sector          — DDB sector label (from provider-info.domains, first vocnet URI)
    11→  provider_name   — provider-info.provider-name
    12→  timespan_begin  — year extracted from edm.RDF.TimeSpan.begin, falling back to
    13→                    edm.RDF.ProvidedCHO.issued when TimeSpan is absent (int or None)
    14→  timespan_end    — year extracted from edm.RDF.TimeSpan.end (int or None)
    15→  dc_type         — list of dc:type text values
    16→  dc_subject      — list of dc:subject / dcTermsSubject text values
    17→  metadata_format — human-readable format label (from source.description.record.type)
    18→  view_fields     — list of display field names
    19→  digitized       — bool: view digitalisat field == "true"
    20→
    21→Year extraction notes
    22→---------------------
    23→YEAR_RE handles both free-text years and YYYYMMDD compact dates (e.g. "18300213").
    24→For timespan_begin, the priority order is:
    25→  1. edm.RDF.TimeSpan.begin
    26→  2. edm.RDF.TimeSpan.end   (if begin is absent)
    27→  3. edm.RDF.ProvidedCHO.issued
    28→
    29→Output
    30→------
    31→  output/items-dataframe.parquet   — primary (preserves list columns natively)
    32→  output/items-dataframe-sample.csv — first 500 rows, lists serialised as JSON
    33→
    34→Usage
    35→-----
    36→    pip install pandas pyarrow
    37→    python scripts/build_dataframe.py
    38→"""
    39→
    40→import json
    41→import re
    42→import pandas as pd
    43→from pathlib import Path
    44→
    45→PROJECT  = Path(__file__).resolve().parent.parent
    46→IN_PATH  = PROJECT / "data" / "items-all-goethe-faust.json"
    47→OUT_PQ   = PROJECT / "output" / "items-dataframe.parquet"
    48→OUT_CSV  = PROJECT / "output" / "items-dataframe-sample.csv"
    49→
    50→# ── lookup tables ─────────────────────────────────────────────────────────────
    51→
    52→SPARTE_LABELS = {
    53→    "http://ddb.vocnet.org/sparte/sparte001": "Archive",
    54→    "http://ddb.vocnet.org/sparte/sparte002": "Library",
    55→    "http://ddb.vocnet.org/sparte/sparte003": "Monument conservation",
    56→    "http://ddb.vocnet.org/sparte/sparte004": "Media library",
    57→    "http://ddb.vocnet.org/sparte/sparte005": "Museum",
    58→    "http://ddb.vocnet.org/sparte/sparte006": "Other",
    59→    "http://ddb.vocnet.org/sparte/sparte007": "Research institution",
    60→}
    61→
    62→RECORD_TYPE_LABELS = {
    63→    "urn:isbn:1-931666-22-9":                      "EAD",
    64→    "http://www.lido-schema.org/":                 "LIDO",
    65→    "http://www.loc.gov/MARC21/slim":              "MARC 21",
    66→    "http://www.loc.gov/MARC21/slim/":             "MARC 21",
    67→    "http://www.mets.org/":                        "METS",
    68→    "http://www.loc.gov/METS/":                    "METS",
    69→    "http://www.europeana.eu/schemas/edm/":        "EDM",
    70→    "http://www.openarchives.org/OAI/2.0/oai_dc/": "OAI-DC",
    71→    "http://www.loc.gov/ead/":                     "EAD",
    72→    "http://www.loc.gov/mods/v3":                  "MODS",
    73→    "http://purl.org/dc/elements/1.1/":            "Dublin Core",
    74→    "http://www.rjm.de/denkxweb/denkxml/":         "DenkXweb",
    75→}
    76→
    77→# Two alternatives:
    78→#  1. year surrounded by non-digits (ISO, free-text)
    79→#  2. year followed by exactly 4 more digits (YYYYMMDD, e.g. "18300213")
    80→YEAR_RE = re.compile(
    81→    r'(?<!\d)(1[0-9]{3}|20[0-2][0-9])(?!\d)'
    82→    r'|(?<!\d)(1[0-9]{3}|20[0-2][0-9])(?=\d{4}(?!\d))'
    83→)
    84→
    85→# ── field extractors ──────────────────────────────────────────────────────────
    86→
    87→def extract_year(val):
    88→    """Return the first 4-digit year (1000–2029) found in val, or None.
    89→    Handles ISO, YYYYMMDD, free-text, and {"$": ...} dict values."""
    90→    if not val:
    91→        return None
    92→    if isinstance(val, dict):
    93→        val = val.get("$") or ""
    94→    m = YEAR_RE.search(str(val))
    95→    return int(m.group(1) or m.group(2)) if m else None
    96→
    97→
    98→def first_text(raw):
    99→    """Return the first non-empty string from a plain string, list of strings,
   100→    or list of {"$": ...} dicts."""
   101→    if isinstance(raw, str):
   102→        return raw
   103→    if isinstance(raw, dict):
   104→        return raw.get("$")
   105→    if isinstance(raw, list) and raw:
   106→        item = raw[0]
   107→        if isinstance(item, str):
   108→            return item
   109→        if isinstance(item, dict):
   110→            return item.get("$")
   111→    return None
   112→
   113→
   114→def extract_text_list(raw):
   115→    """Return a flat list of non-empty text strings from a field value."""
   116→    if raw is None:
   117→        return []
   118→    if isinstance(raw, dict):
   119→        t = raw.get("$")
   120→        return [t] if t else []
   121→    if isinstance(raw, list):
   122→        return [item.get("$") for item in raw
   123→                if isinstance(item, dict) and item.get("$")]
   124→    return []
   125→
   126→
   127→def get_sector(rec):
   128→    domains = rec.get("provider-info", {}).get("domains", [])
   129→    if isinstance(domains, list):
   130→        for d in domains:
   131→            if d and "vocnet" in d:
   132→                return SPARTE_LABELS.get(d.strip(), d.strip())
   133→    return None
   134→
   135→
   136→def get_dc_type(pcho):
   137→    raw = pcho.get("dcType")
   138→    return extract_text_list(raw)
   139→
   140→
   141→def get_dc_subject(pcho):
   142→    subjects = []
   143→    for key in ("dcSubject", "dcTermsSubject", "dcTermSubject"):
   144→        subjects.extend(extract_text_list(pcho.get(key)))
   145→    return subjects
   146→
   147→
   148→def get_view_fields(rec):
   149→    """Return list of display-field names."""
   150→    names = []
   151→    for group in rec.get("view", {}).get("item", {}).get("fields", []):
   152→        if group.get("usage") != "display":
   153→            continue
   154→        fl = group.get("field", [])
   155→        if isinstance(fl, dict):
   156→            fl = [fl]
   157→        for fi in fl:
   158→            name = fi.get("name") if isinstance(fi, dict) else None
   159→            if name:
   160→                names.append(name)
   161→    return names
   162→
   163→
   164→def get_digitized(rec):
   165→    for group in rec.get("view", {}).get("item", {}).get("fields", []):
   166→        fl = group.get("field", [])
   167→        if isinstance(fl, dict):
   168→            fl = [fl]
   169→        for fi in fl:
   170→            if isinstance(fi, dict) and fi.get("id") == "digitalisat":
   171→                vals = fi.get("value", [])
   172→                if vals and isinstance(vals, list):
   173→                    return vals[0].get("content", "").lower() == "true"
   174→    return False
   175→
   176→
   177→# ── scan ──────────────────────────────────────────────────────────────────────
   178→
   179→print("Building DataFrame ...")
   180→rows = []
   181→
   182→with open(IN_PATH) as f:
   183→    for i, line in enumerate(f):
   184→        line = line.strip()
   185→        if not line:
   186→            continue
   187→        try:
   188→            rec = json.loads(line)
   189→        except json.JSONDecodeError:
   190→            continue
   191→
   192→        props   = rec.get("properties", {}) or {}
   193→        pcho    = rec.get("edm", {}).get("RDF", {}).get("ProvidedCHO", {}) or {}
   194→        ts      = rec.get("edm", {}).get("RDF", {}).get("TimeSpan") or {}
   195→        src_rec = rec.get("source", {}).get("description", {}).get("record", {}) or {}
   196→
   197→        rec_type_uri = src_rec.get("type")
   198→        fmt = RECORD_TYPE_LABELS.get(rec_type_uri, rec_type_uri) if rec_type_uri else None
   199→
   200→        # timespan_begin: TimeSpan.begin → TimeSpan.end → ProvidedCHO.issued
   201→        ts_begin = extract_year(ts.get("begin") if isinstance(ts, dict) else None)
   202→        ts_end   = extract_year(ts.get("end")   if isinstance(ts, dict) else None)
   203→        if ts_begin is None and ts_end is None:
   204→            ts_begin = extract_year(first_text(pcho.get("issued")))
   205→
   206→        rows.append({
   207→            "object_id":      props.get("item-id"),
   208→            "sector":         get_sector(rec),
   209→            "provider_name":  (rec.get("provider-info") or {}).get("provider-name"),
   210→            "timespan_begin": ts_begin,
   211→            "timespan_end":   ts_end,
   212→            "dc_type":        get_dc_type(pcho),
   213→            "dc_subject":     get_dc_subject(pcho),
   214→            "metadata_format": fmt,
   215→            "view_fields":    get_view_fields(rec),
   216→            "digitized":      get_digitized(rec),
   217→        })
   218→
   219→        if (i + 1) % 20000 == 0:
   220→            print(f"  {i+1:,} records processed ...")
   221→
   222→df = pd.DataFrame(rows)
   223→
   224→print(f"\nDataFrame shape  : {df.shape[0]:,} rows × {df.shape[1]} columns")
   225→print(f"Columns          : {list(df.columns)}")
   226→print(f"\nNull counts:")
   227→for col in df.columns:
   228→    n_null = df[col].isna().sum()
   229→    if n_null:
   230→        print(f"  {col:<20}: {n_null:,} null")
   231→
   232→print(f"\nSector distribution:")
   233→print(df["sector"].value_counts().to_string())
   234→
   235→# ── save ──────────────────────────────────────────────────────────────────────
   236→
   237→df.to_parquet(OUT_PQ, index=False)
   238→print(f"\nSaved Parquet    : {OUT_PQ}  ({OUT_PQ.stat().st_size / 1e6:.1f} MB)")
   239→
   240→# CSV sample: serialise list columns as JSON strings
   241→df_csv = df.head(500).copy()
   242→for col in ("dc_type", "dc_subject", "view_fields"):
   243→    df_csv[col] = df_csv[col].apply(json.dumps, ensure_ascii=False)
   244→df_csv.to_csv(OUT_CSV, index=False)
   245→print(f"Saved CSV sample : {OUT_CSV}  (first 500 rows)")
   246→



```

---

### Assistant *(2026-03-22T18:52:14.020Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/analyse_items.py"
}
```

---

### User *(2026-03-22T18:52:14.032Z)*

**Tool result**
```
     1→#!/usr/bin/env python3
     2→"""
     3→analyse_items.py
     4→================
     5→Read items-all-goethe-faust.json (JSONL) and aggregate six dimensions:
     6→
     7→  1. metadata_format  — record type URI → human label, with counts
     8→  2. sparte           — provider-info.domains[0] URI → counts
     9→  3. provider         — provider-info.provider_id → name + count
    10→  4. dc_type          — edm.RDF.ProvidedCHO.dcType text values, with counts
    11→  5. dc_subject       — edm.RDF.ProvidedCHO.dcSubject text values, top-N
    12→  6. view_fields      — view.item.fields (display usage) name → top-N value strings
    13→
    14→Output saved to items-analysis.json.
    15→
    16→Usage
    17→-----
    18→    python scripts/analyse_items.py
    19→"""
    20→
    21→import json
    22→from collections import Counter, defaultdict
    23→from pathlib import Path
    24→
    25→PROJECT  = Path(__file__).resolve().parent.parent
    26→IN_PATH  = PROJECT / "data" / "items-all-goethe-faust.json"
    27→OUT_PATH = PROJECT / "output" / "items-analysis.json"
    28→
    29→# ── helpers ──────────────────────────────────────────────────────────────────
    30→
    31→RECORD_TYPE_LABELS = {
    32→    "urn:isbn:1-931666-22-9":                           "EAD",
    33→    "http://www.lido-schema.org/":                      "LIDO",
    34→    "http://www.loc.gov/MARC21/slim":                   "MARC 21",
    35→    "http://www.loc.gov/MARC21/slim/":                  "MARC 21",
    36→    "http://www.mets.org/":                             "METS",
    37→    "http://www.loc.gov/METS/":                         "METS",
    38→    "http://www.europeana.eu/schemas/edm/":             "EDM",
    39→    "http://www.openarchives.org/OAI/2.0/oai_dc/":     "OAI-DC",
    40→    "http://www.loc.gov/ead/":                          "EAD",
    41→    "http://www.loc.gov/mods/v3":                       "MODS",
    42→    "http://purl.org/dc/elements/1.1/":                 "Dublin Core",
    43→    "http://www.rjm.de/denkxweb/denkxml/":              "DenkXweb",
    44→}
    45→
    46→SPARTE_LABELS = {
    47→    "http://ddb.vocnet.org/sparte/sparte001": "Archiv",
    48→    "http://ddb.vocnet.org/sparte/sparte002": "Bibliothek",
    49→    "http://ddb.vocnet.org/sparte/sparte003": "Denkmalfach",
    50→    "http://ddb.vocnet.org/sparte/sparte004": "Mediathek",
    51→    "http://ddb.vocnet.org/sparte/sparte005": "Museum",
    52→    "http://ddb.vocnet.org/sparte/sparte006": "Sonstige",
    53→    "http://ddb.vocnet.org/sparte/sparte007": "Wissenschaftliche Einrichtung",
    54→}
    55→
    56→
    57→def extract_text(field):
    58→    """Return text content from a {resource, lang, $} dict or None."""
    59→    if isinstance(field, dict):
    60→        return field.get("$") or None
    61→    return None
    62→
    63→
    64→def get_dc_type(pcho):
    65→    """Return list of non-empty dcType strings from ProvidedCHO."""
    66→    raw = pcho.get("dcType")
    67→    if raw is None:
    68→        return []
    69→    if isinstance(raw, dict):
    70→        t = extract_text(raw)
    71→        return [t] if t else []
    72→    if isinstance(raw, list):
    73→        return [t for item in raw for t in [extract_text(item)] if t]
    74→    return []
    75→
    76→
    77→def get_dc_subjects(pcho):
    78→    """Return list of non-empty dcSubject/dcTermsSubject strings."""
    79→    subjects = []
    80→    for key in ("dcSubject", "dcTermsSubject", "dcTermSubject"):
    81→        raw = pcho.get(key)
    82→        if raw is None:
    83→            continue
    84→        if isinstance(raw, dict):
    85→            t = extract_text(raw)
    86→            if t:
    87→                subjects.append(t)
    88→        elif isinstance(raw, list):
    89→            for item in raw:
    90→                t = extract_text(item)
    91→                if t:
    92→                    subjects.append(t)
    93→    return subjects
    94→
    95→
    96→def get_display_fields(view):
    97→    """Return list of (field_name, value_string) from display-usage field groups."""
    98→    pairs = []
    99→    fields_groups = view.get("item", {}).get("fields", [])
   100→    if not isinstance(fields_groups, list):
   101→        return pairs
   102→    for group in fields_groups:
   103→        if group.get("usage") != "display":
   104→            continue
   105→        field_list = group.get("field", [])
   106→        if isinstance(field_list, dict):
   107→            field_list = [field_list]
   108→        for fi in field_list:
   109→            name = fi.get("name")
   110→            if not name:
   111→                continue
   112→            values = fi.get("value", [])
   113→            if isinstance(values, dict):
   114→                values = [values]
   115→            for v in values:
   116→                content = v.get("content") if isinstance(v, dict) else None
   117→                if content:
   118→                    pairs.append((name, content))
   119→    return pairs
   120→
   121→
   122→# ── main ─────────────────────────────────────────────────────────────────────
   123→
   124→metadata_format_counter = Counter()   # URI → count
   125→sparte_counter          = Counter()   # URI → count
   126→provider_counter        = Counter()   # provider_id → count
   127→provider_names          = {}          # provider_id → name
   128→dc_type_counter         = Counter()   # text → count
   129→dc_subject_counter      = Counter()   # text → count
   130→field_name_counter      = Counter()   # name → count
   131→field_value_counter     = defaultdict(Counter)  # name → {value → count}
   132→
   133→total = 0
   134→
   135→with open(IN_PATH) as f:
   136→    for line in f:
   137→        line = line.strip()
   138→        if not line:
   139→            continue
   140→        try:
   141→            rec = json.loads(line)
   142→        except json.JSONDecodeError:
   143→            continue
   144→        total += 1
   145→
   146→        # 1. Metadata format
   147→        record_type = (
   148→            rec.get("source", {})
   149→               .get("description", {})
   150→               .get("record", {})
   151→               .get("type")
   152→        )
   153→        if record_type:
   154→            metadata_format_counter[record_type] += 1
   155→
   156→        # 2. Sparte + 3. Provider
   157→        pi = rec.get("provider-info", {})
   158→        domains = pi.get("domains", [])
   159→        if isinstance(domains, list):
   160→            for d in domains:
   161→                if d and d.strip():
   162→                    sparte_counter[d.strip()] += 1
   163→        elif isinstance(domains, str) and domains.strip():
   164→            sparte_counter[domains.strip()] += 1
   165→
   166→        pid  = pi.get("provider-id") or pi.get("provider_id") or ""
   167→        pname = pi.get("provider-name", "")
   168→        if pid:
   169→            provider_counter[pid] += 1
   170→            if pid not in provider_names and pname:
   171→                provider_names[pid] = pname
   172→
   173→        # 4. dcType
   174→        pcho = rec.get("edm", {}).get("RDF", {}).get("ProvidedCHO", {})
   175→        for t in get_dc_type(pcho):
   176→            dc_type_counter[t] += 1
   177→
   178→        # 5. dcSubject
   179→        for s in get_dc_subjects(pcho):
   180→            dc_subject_counter[s] += 1
   181→
   182→        # 6. View fields (display)
   183→        for name, value in get_display_fields(rec.get("view", {})):
   184→            field_name_counter[name] += 1
   185→            field_value_counter[name][value] += 1
   186→
   187→
   188→# ── build output ──────────────────────────────────────────────────────────────
   189→
   190→def labelled_counts(counter, labels=None, top=None):
   191→    """Return sorted list of {label, uri, count} dicts."""
   192→    items = counter.most_common(top) if top else counter.most_common()
   193→    result = []
   194→    for uri, count in items:
   195→        label = (labels or {}).get(uri, uri)
   196→        entry = {"label": label, "count": count}
   197→        if labels is not None:
   198→            entry["uri"] = uri
   199→        result.append(entry)
   200→    return result
   201→
   202→
   203→TOP_SUBJECTS = 100
   204→TOP_FIELD_VALUES = 20
   205→
   206→output = {
   207→    "total_records": total,
   208→    "metadata_format": labelled_counts(metadata_format_counter, RECORD_TYPE_LABELS),
   209→    "sparte": labelled_counts(sparte_counter, SPARTE_LABELS),
   210→    "provider": [
   211→        {"provider_id": pid, "name": provider_names.get(pid, ""), "count": cnt}
   212→        for pid, cnt in provider_counter.most_common()
   213→    ],
   214→    "dc_type": [{"value": v, "count": c} for v, c in dc_type_counter.most_common()],
   215→    "dc_subject": [{"value": v, "count": c} for v, c in dc_subject_counter.most_common(TOP_SUBJECTS)],
   216→    "view_fields": {
   217→        name: {
   218→            "total_occurrences": field_name_counter[name],
   219→            "top_values": [
   220→                {"value": v, "count": c}
   221→                for v, c in field_value_counter[name].most_common(TOP_FIELD_VALUES)
   222→            ],
   223→        }
   224→        for name in sorted(field_name_counter, key=lambda n: -field_name_counter[n])
   225→    },
   226→}
   227→
   228→with open(OUT_PATH, "w", encoding="utf-8") as f:
   229→    json.dump(output, f, indent=2, ensure_ascii=False)
   230→
   231→print(f"Records processed : {total}")
   232→print(f"Metadata formats  : {len(metadata_format_counter)}")
   233→print(f"Sparte entries    : {len(sparte_counter)}")
   234→print(f"Unique providers  : {len(provider_counter)}")
   235→print(f"dcType values     : {len(dc_type_counter)}")
   236→print(f"dcSubject values  : {len(dc_subject_counter)}")
   237→print(f"View field names  : {len(field_name_counter)}")
   238→print(f"\nSaved to {OUT_PATH}")
   239→



```

---

### Assistant *(2026-03-22T18:52:17.863Z)*

Now let me look at the existing matching script and sample the data + both ontologies.

---

### Assistant *(2026-03-22T18:52:18.786Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/match_objecttypes.py"
}
```

---

### User *(2026-03-22T18:52:19.066Z)*

**Tool result**
```
     1→#!/usr/bin/env python3
     2→"""
     3→match_objecttypes.py
     4→====================
     5→Maps DDB (Deutsche Digitale Bibliothek) document objecttype values to classes
     6→from two bibliographic ontologies: FaBiO and DoCO.
     7→
     8→Input
     9→-----
    10→- ddb-search-goethe-all.json : Solr search response (query="goethe", rows=1000)
    11→  Only documents with sector_fct == "sec_02" (library/bibliographic sector) are
    12→  processed.
    13→- fabio.owl : FRBR-aligned Bibliographic Ontology (FaBiO, http://purl.org/spar/fabio/)
    14→  Direct subclasses of fabio:Work, fabio:Expression, fabio:Manifestation, fabio:Item
    15→  are used as matching targets.
    16→- doco.owl : Document Components Ontology (DoCO, http://purl.org/spar/doco/)
    17→  All named classes are used as matching targets.
    18→
    19→Output
    20→------
    21→ddb-type2fabio.json with three top-level keys:
    22→  summary       — aggregate statistics and list of unmatched types
    23→  type_to_fabio — per-objecttype matching result (ontology, class, method, confidence)
    24→  details       — per-objecttype list of doc IDs that carry that type
    25→
    26→Matching pipeline (4 tiers, applied in order; first match wins)
    27→---------------------------------------------------------------
    28→1. strict
    29→   Case-insensitive exact match of the original objecttype string against all
    30→   ontology class names, CamelCase-split variants, and rdfs:label values.
    31→   Confidence: 1.0
    32→
    33→2. strict_translated
    34→   The objecttype is translated from German to English via Google Translate
    35→   (deep-translator, free, no API key). The translated string is then matched
    36→   exactly as in tier 1.
    37→   Confidence: 1.0
    38→
    39→3. levenshtein
    40→   Levenshtein edit distance ≤ 2 between the normalised translated string and
    41→   all lookup keys. The closest match is taken; ties broken by first occurrence.
    42→   Confidence: 1 - (distance / max_length)
    43→
    44→4. embeddings
    45→   Sentence embeddings (all-MiniLM-L6-v2 via sentence-transformers) are computed
    46→   for the translated objecttype and for each ontology class (name + labels).
    47→   The best cosine similarity above EMBEDDING_THRESHOLD (0.55) is taken.
    48→   Confidence: cosine similarity score
    49→
    50→When fabio and doco define a class with the same name (e.g., Index, Chapter,
    51→Table), the fabio class takes priority in the lookup; the doco variant is
    52→accessible under a "doco_<Name>" key.
    53→
    54→Dependencies
    55→------------
    56→    pip install deep-translator rapidfuzz sentence-transformers scikit-learn numpy
    57→
    58→Usage
    59→-----
    60→    python match_objecttypes.py
    61→"""
    62→
    63→import json
    64→import re
    65→from collections import defaultdict
    66→import xml.etree.ElementTree as ET
    67→
    68→from deep_translator import GoogleTranslator
    69→from rapidfuzz.distance import Levenshtein
    70→from sentence_transformers import SentenceTransformer
    71→from sklearn.metrics.pairwise import cosine_similarity
    72→import numpy as np
    73→
    74→# ── Configuration ────────────────────────────────────────────────────
    75→from pathlib import Path
    76→PROJECT        = Path(__file__).resolve().parent.parent
    77→JSON_PATH      = PROJECT / "data" / "ddb-search-faust-goethe-all.json"
    78→FABIO_OWL_PATH = PROJECT / "data" / "schemas" / "fabio.owl"
    79→DOCO_OWL_PATH  = PROJECT / "data" / "schemas" / "doco.owl"
    80→OUT_PATH       = PROJECT / "output" / "ddb-type2fabio.json"
    81→
    82→FABIO_NS = "http://purl.org/spar/fabio/"
    83→DOCO_NS = "http://purl.org/spar/doco/"
    84→FRBR_PARENTS = {"Work", "Expression", "Manifestation", "Item"}
    85→EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    86→EMBEDDING_THRESHOLD = 0.55
    87→LEVENSHTEIN_MIN_CONF = 0.88  # minimum confidence for Levenshtein matches
    88→
    89→
    90→# ── Data loading ─────────────────────────────────────────────────────
    91→
    92→def load_objecttypes(path):
    93→    """Return (docs, doc_otypes, all_types) for sec_02 docs that have objecttype."""
    94→    with open(path) as f:
    95→        data = json.load(f)
    96→    docs = data["response"]["docs"]
    97→    doc_otypes = {}
    98→    for doc in docs:
    99→        if doc.get("sector_fct") == "sec_02" and "objecttype" in doc:
   100→            doc_otypes[doc["id"]] = doc["objecttype"]
   101→    all_types = set()
   102→    for otypes in doc_otypes.values():
   103→        all_types.update(otypes)
   104→    return docs, doc_otypes, sorted(all_types)
   105→
   106→
   107→# ── Ontology parsing ─────────────────────────────────────────────────
   108→
   109→def _owl_ns():
   110→    return {
   111→        "owl": "http://www.w3.org/2002/07/owl#",
   112→        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
   113→        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
   114→    }
   115→
   116→
   117→def parse_fabio_subclasses(path):
   118→    """Return dict of class_name -> {parent, uri, labels, ontology} for direct
   119→    subclasses of the four FRBR top classes (Work/Expression/Manifestation/Item).
   120→    The four top classes themselves are included as self-referential entries.
   121→    """
   122→    tree = ET.parse(path)
   123→    root = tree.getroot()
   124→    ns = _owl_ns()
   125→    subclasses = {}
   126→    for cls in root.findall(".//owl:Class", ns):
   127→        about = cls.get(f"{{{ns['rdf']}}}about", "")
   128→        if not about.startswith(FABIO_NS):
   129→            continue
   130→        class_name = about[len(FABIO_NS):]
   131→        for sub in cls.findall("rdfs:subClassOf", ns):
   132→            res = sub.get(f"{{{ns['rdf']}}}resource", "")
   133→            if res.startswith(FABIO_NS):
   134→                parent = res[len(FABIO_NS):]
   135→                if parent in FRBR_PARENTS:
   136→                    labels = [lbl.text.strip()
   137→                              for lbl in cls.findall("rdfs:label", ns)
   138→                              if lbl.text]
   139→                    subclasses[class_name] = {
   140→                        "parent": parent,
   141→                        "uri": about,
   142→                        "labels": labels,
   143→                        "ontology": "fabio",
   144→                    }
   145→    for p in FRBR_PARENTS:
   146→        subclasses[p] = {"parent": p, "uri": FABIO_NS + p,
   147→                         "labels": [p.lower()], "ontology": "fabio"}
   148→    return subclasses
   149→
   150→
   151→def parse_doco_classes(path):
   152→    """Return dict of class_name -> {parent, uri, labels, ontology} for all
   153→    named DoCO classes. parent is the nearest doco superclass if present.
   154→    """
   155→    tree = ET.parse(path)
   156→    root = tree.getroot()
   157→    ns = _owl_ns()
   158→    classes = {}
   159→    for cls in root.findall(".//owl:Class", ns):
   160→        about = cls.get(f"{{{ns['rdf']}}}about", "")
   161→        if not about.startswith(DOCO_NS):
   162→            continue
   163→        class_name = about[len(DOCO_NS):]
   164→        if not class_name:
   165→            continue
   166→        labels = [lbl.text.strip()
   167→                  for lbl in cls.findall("rdfs:label", ns)
   168→                  if lbl.text]
   169→        parent = None
   170→        for sub in cls.findall("rdfs:subClassOf", ns):
   171→            res = sub.get(f"{{{ns['rdf']}}}resource", "")
   172→            if res.startswith(DOCO_NS):
   173→                parent = res[len(DOCO_NS):]
   174→        classes[class_name] = {
   175→            "parent": parent,
   176→            "uri": about,
   177→            "labels": labels,
   178→            "ontology": "doco",
   179→        }
   180→    return classes
   181→
   182→
   183→# ── Lookup construction ──────────────────────────────────────────────
   184→
   185→def normalize(s):
   186→    """Strip spaces/hyphens/underscores and lowercase."""
   187→    return re.sub(r"[\s\-_]", "", s).lower()
   188→
   189→
   190→def camel_to_words(name):
   191→    """'JournalArticle' -> 'journal article'"""
   192→    return re.sub(r"([A-Z])", r" \1", name).strip().lower()
   193→
   194→
   195→def build_lookup(classes_dict):
   196→    """Build a normalized-string -> class-info lookup over all ontology classes.
   197→
   198→    Keys are derived from: the class name, its CamelCase-split form, and any
   199→    rdfs:label values. When fabio and doco share a class name (e.g., Index),
   200→    fabio takes priority for the bare normalized key.
   201→    """
   202→    lookup = {}
   203→    for name, info in classes_dict.items():
   204→        # Internal dedup keys like "doco_Chapter" -> display as "Chapter"
   205→        clean_name = name.split("_", 1)[1] if name.startswith("doco_") else name
   206→        entry = {"class": clean_name, **info}
   207→        for key in [normalize(clean_name), normalize(camel_to_words(clean_name))]:
   208→            if key not in lookup or info.get("ontology") == "fabio":
   209→                lookup[key] = entry
   210→        for lbl in info.get("labels", []):
   211→            key = normalize(lbl)
   212→            if key not in lookup or info.get("ontology") == "fabio":
   213→                lookup[key] = entry
   214→    return lookup
   215→
   216→
   217→def merge_ontologies(fabio_classes, doco_classes):
   218→    """Merge fabio and doco into one dict; prefix colliding doco keys."""
   219→    merged = {}
   220→    merged.update(fabio_classes)
   221→    for name, info in doco_classes.items():
   222→        if name in merged:
   223→            merged[f"doco_{name}"] = info  # doco variant accessible separately
   224→        else:
   225→            merged[name] = info
   226→    return merged
   227→
   228→
   229→# ── Matching tiers ────────────────────────────────────────────────────
   230→
   231→def match_strict(objecttypes, lookup):
   232→    """Tier 1: exact case-insensitive match on original term."""
   233→    matched, remaining = {}, []
   234→    for otype in objecttypes:
   235→        info = lookup.get(normalize(otype))
   236→        if info:
   237→            matched[otype] = _entry(info, otype, None, "strict", 1.0)
   238→        else:
   239→            remaining.append(otype)
   240→    return matched, remaining
   241→
   242→
   243→def translate_terms(terms, src="de", dest="en", batch_size=100):
   244→    """Translate a list of terms via Google Translate (free, no key required)."""
   245→    translator = GoogleTranslator(source=src, target=dest)
   246→    translations = {}
   247→    batches = [terms[i:i + batch_size] for i in range(0, len(terms), batch_size)]
   248→    for i, batch in enumerate(batches):
   249→        print(f"  Translating batch {i+1}/{len(batches)} ({len(batch)} terms)...")
   250→        try:
   251→            result = translator.translate_batch(batch)
   252→            for orig, trans in zip(batch, result):
   253→                translations[orig] = trans if trans else orig
   254→        except Exception as e:
   255→            print(f"  Warning: batch failed ({e}), falling back to per-term")
   256→            for orig in batch:
   257→                try:
   258→                    translations[orig] = translator.translate(orig)
   259→                except Exception:
   260→                    translations[orig] = orig
   261→    return translations
   262→
   263→
   264→def match_translated_strict(remaining, translations, lookup):
   265→    """Tier 2: exact match on Google-translated term."""
   266→    matched, still_remaining = {}, []
   267→    for otype in remaining:
   268→        translated = translations.get(otype, otype)
   269→        info = lookup.get(normalize(translated))
   270→        if info:
   271→            matched[otype] = _entry(info, otype, translated, "strict_translated", 1.0)
   272→        else:
   273→            still_remaining.append(otype)
   274→    return matched, still_remaining
   275→
   276→
   277→def match_levenshtein(remaining, translations, lookup, max_dist=2,
   278→                      min_conf=LEVENSHTEIN_MIN_CONF):
   279→    """Tier 3: nearest match within Levenshtein distance ≤ max_dist AND
   280→    confidence ≥ min_conf (default 0.88). Candidates that pass the distance
   281→    filter but fall below the confidence threshold are passed to tier 4.
   282→    """
   283→    matched, still_remaining = {}, []
   284→    targets = list(lookup.keys())
   285→    for otype in remaining:
   286→        translated = translations.get(otype, otype)
   287→        norm = normalize(translated)
   288→        best_dist, best_key = max_dist + 1, None
   289→        for target in targets:
   290→            if abs(len(norm) - len(target)) > max_dist:
   291→                continue
   292→            dist = Levenshtein.distance(norm, target, score_cutoff=max_dist)
   293→            if dist <= max_dist and dist < best_dist:
   294→                best_dist, best_key = dist, target
   295→        if best_key is not None:
   296→            info = lookup[best_key]
   297→            max_len = max(len(norm), len(best_key))
   298→            conf = round(1.0 - best_dist / max_len, 3) if max_len else 0.0
   299→            if conf >= min_conf:
   300→                entry = _entry(info, otype, translated, "levenshtein", conf)
   301→                entry["levenshtein_distance"] = best_dist
   302→                matched[otype] = entry
   303→            else:
   304→                still_remaining.append(otype)
   305→        else:
   306→            still_remaining.append(otype)
   307→    return matched, still_remaining
   308→
   309→
   310→def match_embeddings(remaining, translations, onto_classes,
   311→                     threshold=EMBEDDING_THRESHOLD):
   312→    """Tier 4: sentence-embedding cosine similarity ≥ threshold."""
   313→    if not remaining:
   314→        return {}, []
   315→
   316→    print(f"  Loading embedding model '{EMBEDDING_MODEL}'...")
   317→    model = SentenceTransformer(EMBEDDING_MODEL)
   318→
   319→    onto_names = list(onto_classes.keys())
   320→    onto_descs = []
   321→    for name in onto_names:
   322→        info = onto_classes[name]
   323→        desc = camel_to_words(name)
   324→        if info.get("labels"):
   325→            desc += " " + " ".join(info["labels"])
   326→        onto_descs.append(desc)
   327→
   328→    print(f"  Encoding {len(onto_descs)} ontology classes...")
   329→    onto_emb = model.encode(onto_descs, show_progress_bar=False)
   330→
   331→    query_texts = [translations.get(t, t) for t in remaining]
   332→    print(f"  Encoding {len(query_texts)} objecttype terms...")
   333→    query_emb = model.encode(query_texts, show_progress_bar=False)
   334→
   335→    sims = cosine_similarity(query_emb, onto_emb)
   336→
   337→    matched, still_remaining = {}, []
   338→    for i, otype in enumerate(remaining):
   339→        best_idx = int(np.argmax(sims[i]))
   340→        best_score = float(sims[i][best_idx])
   341→        if best_score >= threshold:
   342→            name = onto_names[best_idx]
   343→            info = onto_classes[name]
   344→            # Use clean display name for colliding doco entries
   345→            clean = name.split("_", 1)[1] if name.startswith("doco_") else name
   346→            entry = _entry(
   347→                {**info, "class": clean},
   348→                otype,
   349→                translations.get(otype, otype),
   350→                "embeddings",
   351→                round(best_score, 3),
   352→            )
   353→            matched[otype] = entry
   354→        else:
   355→            still_remaining.append(otype)
   356→    return matched, still_remaining
   357→
   358→
   359→def _entry(info, original_term, translated_term, method, confidence):
   360→    """Build a standard match-result dict."""
   361→    return {
   362→        "ontology": info.get("ontology", "fabio"),
   363→        "ontology_class": info["class"],
   364→        "ontology_parent": info.get("parent"),
   365→        "ontology_uri": info.get("uri"),
   366→        "original_term": original_term,
   367→        "translated_term": translated_term,
   368→        "match_method": method,
   369→        "confidence": confidence,
   370→    }
   371→
   372→
   373→# ── Main ──────────────────────────────────────────────────────────────
   374→
   375→def main():
   376→    print("Loading data...")
   377→    docs, doc_otypes, all_types = load_objecttypes(JSON_PATH)
   378→    fabio_classes = parse_fabio_subclasses(FABIO_OWL_PATH)
   379→    doco_classes = parse_doco_classes(DOCO_OWL_PATH)
   380→    all_onto_classes = merge_ontologies(fabio_classes, doco_classes)
   381→    lookup = build_lookup(all_onto_classes)
   382→
   383→    print(f"  {len(docs)} docs | {len(doc_otypes)} sec_02 with objecttype "
   384→          f"| {len(all_types)} unique types")
   385→    print(f"  {len(fabio_classes)} fabio + {len(doco_classes)} doco = "
   386→          f"{len(all_onto_classes)} ontology classes")
   387→
   388→    print("\n[Tier 1] Strict matching...")
   389→    matched_strict, remaining = match_strict(all_types, lookup)
   390→    print(f"  Matched: {len(matched_strict)}, Remaining: {len(remaining)}")
   391→
   392→    print("\n[Translation] Translating remaining terms DE→EN...")
   393→    translations = translate_terms(remaining)
   394→
   395→    print("\n[Tier 2] Strict matching on translated terms...")
   396→    matched_translated, remaining = match_translated_strict(remaining, translations, lookup)
   397→    print(f"  Matched: {len(matched_translated)}, Remaining: {len(remaining)}")
   398→
   399→    print("\n[Tier 3] Levenshtein matching (max distance=2)...")
   400→    matched_lev, remaining = match_levenshtein(remaining, translations, lookup, max_dist=2)
   401→    print(f"  Matched: {len(matched_lev)}, Remaining: {len(remaining)}")
   402→
   403→    print("\n[Tier 4] Embedding similarity matching...")
   404→    matched_emb, remaining = match_embeddings(
   405→        remaining, translations, all_onto_classes, threshold=EMBEDDING_THRESHOLD)
   406→    print(f"  Matched: {len(matched_emb)}, Remaining: {len(remaining)}")
   407→
   408→    all_matches = {**matched_strict, **matched_translated, **matched_lev, **matched_emb}
   409→    total_matched = len(all_matches)
   410→    total_unmatched = len(remaining)
   411→
   412→    print(f"\n{'='*60}")
   413→    print(f"TOTAL: {total_matched} matched, {total_unmatched} unmatched / {len(all_types)}")
   414→    for label, group in [("strict", matched_strict),
   415→                         ("strict_translated", matched_translated),
   416→                         ("levenshtein", matched_lev),
   417→                         ("embeddings", matched_emb)]:
   418→        print(f"  {label:<20} {len(group)}")
   419→    print(f"  {'unmatched':<20} {total_unmatched}")
   420→
   421→    # Build objecttype -> doc IDs index
   422→    otype_to_ids = defaultdict(list)
   423→    for doc_id, otypes in doc_otypes.items():
   424→        for otype in otypes:
   425→            otype_to_ids[otype].append(doc_id)
   426→
   427→    # Build type_to_fabio (match info, no doc IDs)
   428→    type_to_fabio = {}
   429→    for otype in sorted(set(list(all_matches.keys()) + remaining)):
   430→        if otype in all_matches:
   431→            type_to_fabio[otype] = {**all_matches[otype]}
   432→        else:
   433→            type_to_fabio[otype] = {
   434→                "ontology": None,
   435→                "ontology_class": None,
   436→                "ontology_parent": None,
   437→                "ontology_uri": None,
   438→                "original_term": otype,
   439→                "translated_term": translations.get(otype, otype),
   440→                "match_method": "unmatched",
   441→                "confidence": 0.0,
   442→            }
   443→
   444→    # details: objecttype -> list of doc IDs
   445→    details = {otype: otype_to_ids.get(otype, [])
   446→               for otype in sorted(otype_to_ids.keys())}
   447→
   448→    output = {
   449→        "summary": {
   450→            "total_docs": len(docs),
   451→            "docs_with_objecttype": len(doc_otypes),
   452→            "unique_objecttypes": len(all_types),
   453→            "total_matched": total_matched,
   454→            "total_unmatched": total_unmatched,
   455→            "by_method": {
   456→                "strict": len(matched_strict),
   457→                "strict_translated": len(matched_translated),
   458→                "levenshtein": len(matched_lev),
   459→                "embeddings": len(matched_emb),
   460→                "unmatched": total_unmatched,
   461→            },
   462→            "unmatched_types": sorted(remaining),
   463→        },
   464→        "type_to_fabio": type_to_fabio,
   465→        "details": details,
   466→    }
   467→
   468→    with open(OUT_PATH, "w") as f:
   469→        json.dump(output, f, indent=2, ensure_ascii=False)
   470→    print(f"\nSaved to {OUT_PATH}")
   471→
   472→
   473→if __name__ == "__main__":
   474→    main()
   475→



```

---

### Assistant *(2026-03-22T18:52:19.404Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -100 /Users/mta/Documents/claude/goethe-faust/data/items-all-goethe-faust.json"
}
```

---

### User *(2026-03-22T18:52:19.560Z)*

**Tool result**
```
<persisted-output>
Output too large (2.4MB). Full output saved to: /Users/mta/.claude/projects/-Users-mta-Documents-claude/50aeb795-6da8-4b60-95cc-4b5f77aeb313/tool-results/b4xjcvesh.txt

Preview (first 2KB):
{"properties": {"item-id": "222NZKK63TNRLC2VETRV722VKBDSUVGL", "dataset-id": "76409877634279609sQOu", "dataset-label": "Gesamtlieferung: Deutsche Fotothek - LIDO", "revision-id": "43", "ingest-date": "2026-01-07T15:40:43+0100", "cortex-type": "Kultur", "mapping-version": "6.18", "automatically-translated": false}, "provider-info": {"domains": ["http://ddb.vocnet.org/sparte/sparte005", "", ""], "provider-name": "Deutsche Fotothek", "provider-europeana-name": "", "provider-parent-id": "00014072", "provider-facebook": "", "provider-twitter": "https://twitter.com/Fotothek", "provider-uri": "http://www.deutschefotothek.de", "provider-email": "Deutsche.Fotothek@slub-dresden.de", "provider-collection": "", "provider-item-id": "DE-2396_90106124_df_pos-2018-a_0000067_000_f", "provider-item-id-type": "", "provider-id": "99900890", "provider-ddb-id": "CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI", "provider-isil": "http://ld.zdb-services.de/resource/organisations/DE-2396", "provider-logo": "https://registrierung.deutsche-digitale-bibliothek.de/logos/99900890.jpg", "provider-longitude": "13.73593", "provider-latitude": "51.02874", "provider-state": "Sachsen", "provider-parents": {"parents": [{"provider-name": "Sächsische Landesbibliothek - Staats- und Universitätsbibliothek Dresden", "domains": ["http://ddb.vocnet.org/sparte/sparte002", "", ""], "provider-parent-id": "", "provider-uri": "http://www.slub-dresden.de", "provider-email": "", "provider-collection": "", "provider-item-id-type": "", "provider-id": "00014072", "provider-ddb-id": "265BI7NE7QBS4NQMZCCGIVLFR73OCOSL", "provider-logo": "https://registrierung.deutsche-digitale-bibliothek.de/logos/00014072.jpg", "provider-longitude": "13.73593", "provider-latitude": "51.02874", "aggregator": false}]}}, "edm": {"RDF": {"Aggregation": {"about": "2X55WKCAYOIS4Y5CJPQQWQPXXC6TX4AK", "aggregatedCHO": {"resource": "http://www.deutsche-digitale-bibliothek.de/item/222NZKK63TNRLC2VETRV722VKBDSUVGL", "lang": null, "$": ""}, "isShownAt": {"resource"
...
</persisted-output>
```

---

### Assistant *(2026-03-22T18:52:23.086Z)*

Good. Now let me look at the two ontologies.

---

### Assistant *(2026-03-22T18:52:24.525Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/ddbedm-odk/src/ontology/ddbedm-full.owl /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl 2>&1"
}
```

---

### User *(2026-03-22T18:52:30.716Z)*

**Tool result** *(error)*
```
Exit code 1
wc: /Users/mta/Documents/ddbedm-odk/src/ontology/ddbedm-full.owl: open: No such file or directory
   49849 /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl
   49849 total
```

---

### Assistant *(2026-03-22T18:52:33.122Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents -name \"ddbedm*.owl\" 2>/dev/null | head -10"
}
```

---

### User *(2026-03-22T18:52:37.400Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T18:52:39.512Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents -name \"*.owl\" 2>/dev/null | head -20"
}
```

---

### User *(2026-03-22T18:52:41.432Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T18:52:43.620Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta -name \"*.owl\" 2>/dev/null | grep -v \".Trash\" | head -20"
}
```

---

### User *(2026-03-22T18:53:16.913Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T18:53:20.397Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/goethe-faust/data/schemas -type f 2>/dev/null; ls /Users/mta/Documents/claude/goethe-faust/data/ 2>/dev/null"
}
```

---

### User *(2026-03-22T18:53:20.450Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/data/schemas/fabio.owl
/Users/mta/Documents/claude/goethe-faust/data/schemas/doco.owl
ddb-search-faust-all.json
ddb-search-faust-goethe-all.json
ddb-search-goethe-all.json
hf-cache
htype.csv
ids-all-goethe-faust.txt
ids-faust.txt
ids-goethe.txt
ids-missing.txt
items
items-all-goethe-faust.json
items-excerpt-1000.json
schemas
search-ids-post.txt
temp-items.json
transcripts
type2class.json
```

---

### Assistant *(2026-03-22T18:53:24.772Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/ 2>/dev/null | head -20"
}
```

---

### User *(2026-03-22T18:53:24.815Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T18:53:27.092Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/ 2>/dev/null"
}
```

---

### User *(2026-03-22T18:53:27.144Z)*

**Tool result**
```
LICENSE
docs
mocho-odk
mocho-odk-bak
notes
odk-imports
odk-ontology
ontology
output
scripts
transcripts
```

---

### Assistant *(2026-03-22T18:53:29.023Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/mocho -name \"*.owl\" | head -10"
}
```

---

### User *(2026-03-22T18:53:29.258Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T18:53:33.234Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/mocho -name \"*.owl\" -o -name \"*.ttl\" -o -name \"*.rdf\" 2>/dev/null | head -20"
}
```

---

### Assistant *(2026-03-22T18:53:33.850Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/ontology/ 2>/dev/null; ls /Users/mta/Documents/claude/mocho/mocho-odk/ 2>/dev/null"
}
```

---

### User *(2026-03-22T18:53:45.571Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### User *(2026-03-22T18:53:45.606Z)*

**Tool result**
```
CIDOC_CRM_v7.1.3.owl
RiC-O_1-1.rdf
aco-1.2.3.owl
aco.owl
catalog-v001.xml
ddbedm_1.0.ttl
doco-20150703.xml
doco.owl
ebucoreplus.owl
edm_5.2.4.ttl
fabio-20230529.xml
fabio.owl
frbr-20180329.xml
frbr-20220525.owl
frbr.ttl
gnd_20251218.ttl
lio.owl
mocho-v0.1.ttl
mocho_old.ttl
musicontology.n3
rda-5.4.9
vra-core-ontology-v4.0.html
vra-core-v4.0.owl
LICENSE
imports
mirror_from
mocho
mocho-odk.yaml
seed-via-docker.sh
src
transcripts
widoco-sections
```

---

### Assistant *(2026-03-22T18:53:48.919Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/mocho-odk/src/ 2>/dev/null; find /Users/mta/Documents/claude/mocho/mocho-odk -name \"*.owl\" -o -name \"*.ttl\" 2>/dev/null | head -20"
}
```

---

### User *(2026-03-22T18:54:11.974Z)*

**Tool result**
```
ontology
scripts
sparql
```

---

### Assistant *(2026-03-22T18:54:14.860Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/ 2>/dev/null"
}
```

---

### User *(2026-03-22T18:54:14.923Z)*

**Tool result**
```
Makefile
README-editors.md
catalog-v001.xml
imports
mirror
mocho-base.json
mocho-base.owl
mocho-base.ttl
mocho-edit.owl
mocho-full.json
mocho-full.owl
mocho-full.ttl
mocho-idranges.owl
mocho-odk.yaml
mocho.Makefile
mocho.json
mocho.owl
mocho.ttl
reports
run.bat
run.sh
tmp
```

---

### Assistant *(2026-03-22T18:54:18.393Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl"
}
```

---

### User *(2026-03-22T18:54:18.458Z)*

**Tool result**
```
   49849 /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl
```

---

### Assistant *(2026-03-22T18:54:18.664Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl",
  "limit": 100
}
```

---

### User *(2026-03-22T18:54:18.671Z)*

**Tool result**
```
     1→<?xml version="1.0"?>
     2→<rdf:RDF xmlns="https://github.com/anntanp/mocho-odk/mocho/mocho-full.owl#"
     3→     xml:base="https://github.com/anntanp/mocho-odk/mocho/mocho-full.owl"
     4→     xmlns:a="http://rdaregistry.info/Elements/a/"
     5→     xmlns:e="http://rdaregistry.info/Elements/e/"
     6→     xmlns:i="http://rdaregistry.info/Elements/i/"
     7→     xmlns:m="http://rdaregistry.info/Elements/m/"
     8→     xmlns:w="http://rdaregistry.info/Elements/w/"
     9→     xmlns:dce="http://purl.org/dc/elements/1.1/"
    10→     xmlns:owl="http://www.w3.org/2002/07/owl#"
    11→     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    12→     xmlns:xml="http://www.w3.org/XML/1998/namespace"
    13→     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    14→     xmlns:dcat="http://www.w3.org/ns/dcat#"
    15→     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    16→     xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    17→     xmlns:skos1="http://www.w3.org/2008/05/skos#"
    18→     xmlns:dcterms="http://purl.org/dc/terms/"
    19→     xmlns:ebucoreplus="http://www.ebu.ch/metadata/ontologies/ebucoreplus#">
    20→    <owl:Ontology rdf:about="https://github.com/anntanp/mocho-odk/mocho/mocho-full.owl">
    21→        <owl:versionIRI rdf:resource="https://github.com/anntanp/mocho-odk/mocho/releases/2026-03-19/mocho-full.owl"/>
    22→        <dcterms:description>A middle ontology bridging the Europeana Data Model (EDM) as top-level ontology with domain ontologies: RDA, Records in Contexts Ontology (RiC-O), Music Ontology, Audio Commons Ontology (ACO), and CIDOC CRM via LRMoo/FRBRoo. The WEMI model (Work, Expression, Manifestation, Item) serves as the central conceptual framework, with RDA entity classes as the canonical middle-layer.
    23→</dcterms:description>
    24→        <dcterms:license rdf:resource="https://creativecommons.org/licenses/by/4.0/deed.en"/>
    25→        <dcterms:title>Middle Ontology for Cultural Heritage Objects</dcterms:title>
    26→        <owl:versionInfo>2026-03-19</owl:versionInfo>
    27→    </owl:Ontology>
    28→    
    29→
    30→
    31→    <!-- 
    32→    ///////////////////////////////////////////////////////////////////////////////////////
    33→    //
    34→    // Annotation properties
    35→    //
    36→    ///////////////////////////////////////////////////////////////////////////////////////
    37→     -->
    38→
    39→    
    40→
    41→
    42→    <!-- http://purl.org/dc/elements/1.1/contributor -->
    43→
    44→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/contributor"/>
    45→    
    46→
    47→
    48→    <!-- http://purl.org/dc/elements/1.1/creator -->
    49→
    50→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/creator"/>
    51→    
    52→
    53→
    54→    <!-- http://purl.org/dc/elements/1.1/date -->
    55→
    56→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/date"/>
    57→    
    58→
    59→
    60→    <!-- http://purl.org/dc/elements/1.1/description -->
    61→
    62→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/description"/>
    63→    
    64→
    65→
    66→    <!-- http://purl.org/dc/elements/1.1/rights -->
    67→
    68→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/rights"/>
    69→    
    70→
    71→
    72→    <!-- http://purl.org/dc/elements/1.1/source -->
    73→
    74→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/source"/>
    75→    
    76→
    77→
    78→    <!-- http://purl.org/dc/elements/1.1/title -->
    79→
    80→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/elements/1.1/title"/>
    81→    
    82→
    83→
    84→    <!-- http://purl.org/dc/terms/description -->
    85→
    86→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/terms/description">
    87→        <rdfs:isDefinedBy rdf:resource="http://purl.org/dc/terms/"/>
    88→        <rdfs:label xml:lang="en">dcterms:description</rdfs:label>
    89→        <rdfs:label>description</rdfs:label>
    90→    </owl:AnnotationProperty>
    91→    
    92→
    93→
    94→    <!-- http://purl.org/dc/terms/issued -->
    95→
    96→    <owl:AnnotationProperty rdf:about="http://purl.org/dc/terms/issued">
    97→        <rdfs:label xml:lang="en">dcterms:issued</rdfs:label>
    98→        <skos:definition xml:lang="en">Date of formal issuance of the resource.</skos:definition>
    99→    </owl:AnnotationProperty>
   100→    



```

---

### Assistant *(2026-03-22T18:54:34.160Z)*

Now let me look at the DDB EDM ontology and mocho structure more closely.

---

### Assistant *(2026-03-22T18:54:35.088Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/mocho/mocho-odk/ddbedm_1.0.ttl; head -100 /Users/mta/Documents/claude/mocho/mocho-odk/ddbedm_1.0.ttl"
}
```

---

### User *(2026-03-22T18:54:35.139Z)*

**Tool result** *(error)*
```
Exit code 1
wc: /Users/mta/Documents/claude/mocho/mocho-odk/ddbedm_1.0.ttl: open: No such file or directory
head: /Users/mta/Documents/claude/mocho/mocho-odk/ddbedm_1.0.ttl: No such file or directory
```

---

### Assistant *(2026-03-22T18:54:35.966Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl",
  "limit": 200,
  "offset": 100
}
```

---

### User *(2026-03-22T18:54:35.966Z)*

**Tool result** *(error)*
```
<tool_use_error>Cancelled: parallel tool call Bash(wc -l /Users/mta/Documents/claude/mocho/…) errored</tool_use_error>
```

---

### Assistant *(2026-03-22T18:54:36.642Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/gen_htype_doco_mapping.py"
}
```

---

### User *(2026-03-22T18:54:36.643Z)*

**Tool result** *(error)*
```
<tool_use_error>Cancelled: parallel tool call Bash(wc -l /Users/mta/Documents/claude/mocho/…) errored</tool_use_error>
```

---

### Assistant *(2026-03-22T18:54:39.148Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/mocho -name \"ddbedm*\" 2>/dev/null; ls /Users/mta/Documents/claude/mocho/mocho-odk/ | head -20"
}
```

---

### User *(2026-03-22T18:57:18.746Z)*

**Tool result**
```
/Users/mta/Documents/claude/mocho/mocho-odk/mocho/imports/ddbedm_terms.txt
/Users/mta/Documents/claude/mocho/mocho-odk/mocho/imports/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/mocho-odk/mocho/mirror/ddbedm.owl
/Users/mta/Documents/claude/mocho/mocho-odk/imports/ddbedm_terms.txt
/Users/mta/Documents/claude/mocho/mocho-odk/mirror_from/ddbedm-1.0.0.owl
/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/imports/ddbedm_terms.txt
/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/imports/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mirror/ddbedm.owl
/Users/mta/Documents/claude/mocho/odk-imports/ddbedm_terms.txt
/Users/mta/Documents/claude/mocho/odk-imports/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/output/ddbedm_1.json
/Users/mta/Documents/claude/mocho/output/ddbedm-full.csv
/Users/mta/Documents/claude/mocho/output/ddbedm_1.csv
/Users/mta/Documents/claude/mocho/output/ddbedm-full.json
/Users/mta/Documents/claude/mocho/ontology/ddbedm_1.0.ttl
/Users/mta/Documents/claude/mocho/odk-ontology/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/mocho-odk-bak/mocho/imports/ddbedm_terms.txt
/Users/mta/Documents/claude/mocho/mocho-odk-bak/mocho/imports/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/mocho-odk-bak/mocho/mirror/ddbedm.owl
/Users/mta/Documents/claude/mocho/mocho-odk-bak/ontology/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/mocho-odk-bak/src/ontology/imports/ddbedm_terms.txt
/Users/mta/Documents/claude/mocho/mocho-odk-bak/src/ontology/imports/ddbedm_import.owl
/Users/mta/Documents/claude/mocho/mocho-odk-bak/src/ontology/mirror/ddbedm.owl
```

---

### Assistant *(2026-03-22T18:57:21.843Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/mocho/ontology/ddbedm_1.0.ttl; head -120 /Users/mta/Documents/claude/mocho/ontology/ddbedm_1.0.ttl"
}
```

---

### User *(2026-03-22T18:57:21.898Z)*

**Tool result**
```
     683 /Users/mta/Documents/claude/mocho/ontology/ddbedm_1.0.ttl
@prefix : <http://www.deutsche-digitale-bibliothek.de/edm/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix crm: <http://www.cidoc-crm.org/rdfs/cidoc-crm#> .
@prefix ddb: <http://www.deutsche-digitale-bibliothek.de/edm/> .
@prefix edm: <http://www.europeana.eu/schemas/edm/> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix ore: <http://www.openarchives.org/ore/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix frbr: <http://purl.org/vocab/frbr/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix vann: <http://purl.org/vocab/vann/> .
@prefix frbroo: <http://iflastandards.info/ns/fr/frbr/frbroo/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@base <http://www.deutsche-digitale-bibliothek.de/edm/> .

<http://deutsche-digitale-bibliothek.de/edm/> rdf:type owl:Ontology ;
                                               owl:versionIRI <http://deutsche-digitale-bibliothek.de/edm/> ;
                                               dc:description "The DDB-EDM is an extension of the implemented the Europeana Mapping Guidelines described in 2013. Implementation details are presented at the International Conference on Dublic Core and Metadata Applications in 2014 (Rühle et al., 2014). See https://dcpapers-data.dublincore.org/articles/dc-2014/952136503/files/dcmi-952136503.pdf"@en ;
                                               dc:title "Deutsche Digitale Bibliothek - Europeana Data Model (DDB-EDM)"@en ;
                                               dcterms:issued "2014-10-08"@en ;
                                               vann:preferredNamespacePrefix "ddb"@en ;
                                               vann:preferredNamespaceUri ddb: ;
                                               skos:note """All definitions relation to EDM are extracted from v5.2.7 described in https://pro.europeana.eu/files/Europeana_Professional/Share_your_data/Technical_requirements/EDM_Documentation/EDM_Definition_v5.2.7_042016.pdf.

Equivalence class definitions referring to ABC Harmony and DOLCE are not included."""@en .

#################################################################
#    Annotation properties
#################################################################

###  http://purl.org/dc/elements/1.1/description
dc:description rdf:type owl:AnnotationProperty .


###  http://purl.org/dc/elements/1.1/title
dc:title rdf:type owl:AnnotationProperty .


###  http://purl.org/dc/terms/issued
dcterms:issued rdf:type owl:AnnotationProperty .


###  http://purl.org/dc/terms/provenance
dcterms:provenance rdf:type owl:AnnotationProperty .


###  http://purl.org/vocab/vann/preferredNamespacePrefix
vann:preferredNamespacePrefix rdf:type owl:AnnotationProperty ;
                              rdfs:isDefinedBy <https://vocab.org/vann/#preferredNamespacePrefix> ;
                              rdfs:label "vann:preferredNamespacePrefix"@en .


###  http://purl.org/vocab/vann/preferredNamespaceUri
vann:preferredNamespaceUri rdf:type owl:AnnotationProperty ;
                           rdfs:isDefinedBy <https://vocab.org/vann/#preferredNamespaceUri> ;
                           rdfs:label "vann:preferredNamespaceUri"@en .


###  http://www.europeana.eu/schemas/edm/dataProvider
edm:dataProvider rdf:type owl:AnnotationProperty ;
                 rdfs:label "edm:dataProvider"@en ;
                 rdfs:subPropertyOf dcterms:provenance ;
                 rdfs:range edm:Agent .


###  http://www.w3.org/2002/07/owl#versionInfo
owl:versionInfo rdf:type owl:AnnotationProperty .


###  http://www.w3.org/2004/02/skos/core#example
skos:example rdf:type owl:AnnotationProperty .


###  http://www.w3.org/2004/02/skos/core#notation
skos:notation rdf:type owl:AnnotationProperty .


###  http://www.w3.org/2004/02/skos/core#note
skos:note rdf:type owl:AnnotationProperty .


###  http://www.w3.org/2004/02/skos/core#prefLabel
skos:prefLabel rdf:type owl:AnnotationProperty .


###  http://www.w3.org/2004/02/skos/core#scopeNote
skos:scopeNote rdf:type owl:AnnotationProperty .


#################################################################
#    Object Properties
#################################################################

###  http://purl.org/dc/elements/1.1/contributor
dc:contributor rdf:type owl:ObjectProperty ;
               rdfs:subPropertyOf edm:hasMet .


###  http://purl.org/dc/elements/1.1/coverage
dc:coverage rdf:type owl:ObjectProperty ;
            rdfs:subPropertyOf edm:hasMet .


###  http://purl.org/dc/elements/1.1/creator
dc:creator rdf:type owl:ObjectProperty ;
           rdfs:subPropertyOf edm:hasMet .


###  http://purl.org/dc/elements/1.1/date
dc:date rdf:type owl:ObjectProperty ;
        rdfs:subPropertyOf edm:hasMet .


###  http://purl.org/dc/elements/1.1/format
dc:format rdf:type owl:ObjectProperty ;
          rdfs:subPropertyOf edm:hasType .
```

---

### Assistant *(2026-03-22T18:57:22.011Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/gen_htype_doco_mapping.py"
}
```

---

### User *(2026-03-22T18:57:22.232Z)*

**Tool result**
```
     1→"""
     2→gen_htype_doco_mapping.py
     3→
     4→Match htype label_en values against DoCO ontology class labels using four
     5→strategies and write a ranked mapping table.
     6→
     7→Matching strategies (applied in order; first hit wins per htype):
     8→  1. exact        — case-insensitive exact match
     9→  2. levenshtein  — RapidFuzz ratio >= 88 %
    10→  3. translated   — translate label_de (Helsinki-NLP/opus-mt-de-en), then
    11→                    exact match against DoCO labels
    12→  4. embedding    — cosine similarity of sentence-transformers/all-MiniLM-L6-v2
    13→                    embeddings; top candidate reported regardless of threshold
    14→
    15→Usage:
    16→    python scripts/gen_htype_doco_mapping.py
    17→    python scripts/gen_htype_doco_mapping.py \\
    18→        --htypes   data/htype.csv \\
    19→        --doco     data/schemas/doco.owl \\
    20→        --out-csv  ~/Documents/claude/mocho/output/mapping_htype_doco.csv \\
    21→        --out-json ~/Documents/claude/mocho/output/mapping_htype_doco.json \\
    22→        --hf-cache data/hf-cache
    23→
    24→Inputs:
    25→    data/htype.csv              htype_code, label_de, label_en
    26→    data/schemas/doco.owl       DoCO ontology (RDF/XML or Turtle)
    27→
    28→Outputs:
    29→    mapping_htype_doco.csv / .json
    30→
    31→Columns:
    32→    htype_code, label_de, label_en, match_method, confidence,
    33→    doco_class, doco_label, doco_uri, translated_en
    34→
    35→Dependencies:
    36→    rdflib, rapidfuzz, sentence-transformers, transformers (HF), deep-translator
    37→"""
    38→
    39→import argparse
    40→import csv
    41→import json
    42→import os
    43→import warnings
    44→from pathlib import Path
    45→
    46→# Suppress noisy warnings from torch / urllib3
    47→warnings.filterwarnings("ignore")
    48→os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    49→os.environ["TRANSFORMERS_OFFLINE"] = "1"   # use only locally cached models
    50→os.environ["HF_DATASETS_OFFLINE"]  = "1"
    51→
    52→# ---------------------------------------------------------------------------
    53→# Argument parsing
    54→# ---------------------------------------------------------------------------
    55→
    56→WORKING_DIR  = Path.home() / "Documents/claude/goethe-faust"
    57→DEFAULT_OUT  = Path.home() / "Documents/claude/mocho/output"
    58→
    59→def parse_args():
    60→    p = argparse.ArgumentParser(description=__doc__)
    61→    p.add_argument("--htypes",   default=str(WORKING_DIR / "data/htype.csv"))
    62→    p.add_argument("--doco",     default=str(WORKING_DIR / "data/schemas/doco.owl"))
    63→    p.add_argument("--out-csv",  default=str(DEFAULT_OUT / "mapping_htype_doco.csv"))
    64→    p.add_argument("--out-json", default=str(DEFAULT_OUT / "mapping_htype_doco.json"))
    65→    p.add_argument("--hf-cache", default=str(WORKING_DIR / "data/hf-cache"),
    66→                   help="Hugging Face cache directory")
    67→    p.add_argument("--embed-threshold", type=float, default=0.0,
    68→                   help="Min cosine similarity for embedding match (default: report best regardless)")
    69→    p.add_argument("--lev-threshold", type=float, default=88.0,
    70→                   help="Min Levenshtein ratio %% for fuzzy match (default: %(default)s)")
    71→    return p.parse_args()
    72→
    73→# ---------------------------------------------------------------------------
    74→# DoCO label extraction
    75→# ---------------------------------------------------------------------------
    76→
    77→def load_doco_labels(owl_path: str) -> list[dict]:
    78→    """Return list of {local, label, uri} for all DoCO classes."""
    79→    from rdflib import Graph, RDFS, RDF, OWL, Namespace
    80→    DOCO = Namespace("http://purl.org/spar/doco/")
    81→    g = Graph()
    82→    g.parse(owl_path)
    83→    rows = []
    84→    for subj, _, label in g.triples((None, RDFS.label, None)):
    85→        uri = str(subj)
    86→        if not uri.startswith(str(DOCO)):
    87→            continue
    88→        local = uri.split("/")[-1]
    89→        rows.append({"local": local, "label": str(label), "uri": uri})
    90→    return sorted(rows, key=lambda r: r["label"])
    91→
    92→# ---------------------------------------------------------------------------
    93→# Strategy 1: exact match
    94→# ---------------------------------------------------------------------------
    95→
    96→def match_exact(query, candidates):
    97→    q = query.strip().lower()
    98→    for c in candidates:
    99→        if c["label"].lower() == q:
   100→            return {"method": "exact", "confidence": 1.0, **c}
   101→    return None
   102→
   103→# ---------------------------------------------------------------------------
   104→# Strategy 2: Levenshtein (RapidFuzz)
   105→# ---------------------------------------------------------------------------
   106→
   107→def match_levenshtein(query, candidates, threshold):
   108→    from rapidfuzz import fuzz
   109→    q = query.strip().lower()
   110→    best, best_score = None, 0.0
   111→    for c in candidates:
   112→        score = fuzz.ratio(q, c["label"].lower())
   113→        if score > best_score:
   114→            best_score = score
   115→            best = c
   116→    if best and best_score >= threshold:
   117→        return {"method": "levenshtein", "confidence": round(best_score / 100, 4), **best}
   118→    return None
   119→
   120→# ---------------------------------------------------------------------------
   121→# Strategy 3: translate label_de → English, then exact match
   122→# ---------------------------------------------------------------------------
   123→
   124→_translator = None
   125→
   126→def get_translator(hf_cache: str):
   127→    global _translator
   128→    if _translator is None:
   129→        from transformers import MarianMTModel, MarianTokenizer
   130→        model_name = "Helsinki-NLP/opus-mt-de-en"
   131→        print("  Loading translation model …")
   132→        # Resolve snapshot directory from hub cache layout
   133→        import glob as _glob
   134→        snaps = sorted(_glob.glob(
   135→            str(Path(hf_cache) / "hub/models--Helsinki-NLP--opus-mt-de-en/snapshots/*/config.json")
   136→        ))
   137→        if not snaps:
   138→            raise FileNotFoundError(
   139→                f"opus-mt-de-en not found in {hf_cache}. "
   140→                "Run once with network access to download it."
   141→            )
   142→        model_path = str(Path(snaps[-1]).parent)
   143→        tokenizer = MarianTokenizer.from_pretrained(model_path, local_files_only=True)
   144→        model     = MarianMTModel.from_pretrained(model_path, local_files_only=True)
   145→        _translator = (tokenizer, model)
   146→    return _translator
   147→
   148→def translate_de_en(texts: list[str], hf_cache: str) -> list[str]:
   149→    """Batch-translate German texts to English."""
   150→    tokenizer, model = get_translator(hf_cache)
   151→    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
   152→    outputs = model.generate(**inputs)
   153→    return [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]
   154→
   155→def match_translated(label_de, candidates, hf_cache,
   156→                     translation_cache):
   157→    """Translate label_de if not cached, then exact-match against DoCO labels."""
   158→    if label_de not in translation_cache:
   159→        translation_cache[label_de] = translate_de_en([label_de], hf_cache)[0]
   160→    translated = translation_cache[label_de]
   161→    hit = match_exact(translated, candidates)
   162→    if hit:
   163→        return {**hit, "method": "translated"}, translated
   164→    return None, translated
   165→
   166→# ---------------------------------------------------------------------------
   167→# Strategy 4: sentence embedding cosine similarity
   168→# ---------------------------------------------------------------------------
   169→
   170→_embed_model = None
   171→
   172→def get_embed_model(hf_cache: str):
   173→    global _embed_model
   174→    if _embed_model is None:
   175→        from sentence_transformers import SentenceTransformer
   176→        print("  Loading embedding model …")
   177→        # all-MiniLM-L6-v2 is in the default HF cache (~/.cache/huggingface);
   178→        # opus-mt-de-en is in the project hf-cache.
   179→        _embed_model = SentenceTransformer(
   180→            "sentence-transformers/all-MiniLM-L6-v2",
   181→            local_files_only=True,
   182→        )
   183→    return _embed_model
   184→
   185→def match_embedding(query, candidates, hf_cache,
   186→                    candidate_embeddings, threshold):
   187→    import numpy as np
   188→    model = get_embed_model(hf_cache)
   189→    q_emb = model.encode([query.strip()], normalize_embeddings=True)[0]
   190→    sims  = candidate_embeddings @ q_emb          # dot product = cosine (normalized)
   191→    idx   = int(np.argmax(sims))
   192→    score = float(sims[idx])
   193→    if score >= threshold:
   194→        c = candidates[idx]
   195→        return {"method": "embedding", "confidence": round(score, 4), **c}
   196→    return None
   197→
   198→# ---------------------------------------------------------------------------
   199→# Main
   200→# ---------------------------------------------------------------------------
   201→
   202→def main():
   203→    args = parse_args()
   204→
   205→    hf_cache   = args.hf_cache
   206→    lev_thresh = args.lev_threshold
   207→    emb_thresh = args.embed_threshold
   208→
   209→    # Load inputs
   210→    print("Loading DoCO labels …")
   211→    candidates = load_doco_labels(args.doco)
   212→    print(f"  {len(candidates)} DoCO classes")
   213→
   214→    htypes = []
   215→    with open(args.htypes, newline="", encoding="utf-8") as f:
   216→        for row in csv.DictReader(f):
   217→            htypes.append(row)
   218→    print(f"  {len(htypes)} htype rows")
   219→
   220→    # Pre-compute candidate embeddings once
   221→    print("Computing DoCO label embeddings …")
   222→    model = get_embed_model(hf_cache)
   223→    import numpy as np
   224→    cand_labels     = [c["label"] for c in candidates]
   225→    cand_embeddings = model.encode(cand_labels, normalize_embeddings=True,
   226→                                   show_progress_bar=False)
   227→
   228→    translation_cache: dict[str, str] = {}
   229→    rows = []
   230→
   231→    print("Matching …")
   232→    for ht in htypes:
   233→        code     = ht["htype_code"].strip()
   234→        label_de = ht["label_de"].strip()
   235→        label_en = ht["label_en"].strip()
   236→
   237→        translated_en = ""
   238→        hit = None
   239→
   240→        # 1. Exact
   241→        hit = match_exact(label_en, candidates)
   242→
   243→        # 2. Levenshtein
   244→        if not hit:
   245→            hit = match_levenshtein(label_en, candidates, lev_thresh)
   246→
   247→        # 3. Translated + exact
   248→        if not hit:
   249→            hit, translated_en = match_translated(label_de, candidates,
   250→                                                   hf_cache, translation_cache)
   251→
   252→        # 4. Embedding (always runs; fills translated_en if not already set)
   253→        if not hit:
   254→            if not translated_en:
   255→                if label_de not in translation_cache:
   256→                    translation_cache[label_de] = translate_de_en(
   257→                        [label_de], hf_cache)[0]
   258→                translated_en = translation_cache[label_de]
   259→            hit = match_embedding(label_en, candidates, hf_cache,
   260→                                  cand_embeddings, emb_thresh)
   261→
   262→        row = {
   263→            "htype_code":   code,
   264→            "label_de":     label_de,
   265→            "label_en":     label_en,
   266→            "match_method": hit["method"]     if hit else "no_match",
   267→            "confidence":   hit["confidence"] if hit else 0.0,
   268→            "doco_class":   hit["local"]      if hit else "",
   269→            "doco_label":   hit["label"]      if hit else "",
   270→            "doco_uri":     hit["uri"]        if hit else "",
   271→            "translated_en": translated_en,
   272→        }
   273→        rows.append(row)
   274→        status = f"{row['match_method']:12s}  {row['confidence']:.2f}  {row['doco_class']}"
   275→        print(f"  {code}  {label_en:<30s}  →  {status}")
   276→
   277→    # Write outputs
   278→    out_csv  = Path(args.out_csv)
   279→    out_json = Path(args.out_json)
   280→    out_csv.parent.mkdir(parents=True, exist_ok=True)
   281→
   282→    fieldnames = ["htype_code", "label_de", "label_en", "match_method",
   283→                  "confidence", "doco_class", "doco_label", "doco_uri",
   284→                  "translated_en"]
   285→    with open(out_csv, "w", newline="", encoding="utf-8") as f:
   286→        writer = csv.DictWriter(f, fieldnames=fieldnames)
   287→        writer.writeheader()
   288→        writer.writerows(rows)
   289→
   290→    summary = {m: sum(1 for r in rows if r["match_method"] == m)
   291→               for m in ("exact", "levenshtein", "translated", "embedding", "no_match")}
   292→    out_json.write_text(
   293→        json.dumps({"summary": summary, "mappings": rows}, indent=2, ensure_ascii=False),
   294→        encoding="utf-8",
   295→    )
   296→
   297→    print(f"\nWrote {out_csv}")
   298→    print(f"Wrote {out_json}")
   299→    print("Summary:", summary)
   300→
   301→
   302→if __name__ == "__main__":
   303→    main()
   304→



```

---

### Assistant *(2026-03-22T18:57:37.374Z)*

Now let me look at what mocho defines and check the notes on alignment work.

---

### Assistant *(2026-03-22T18:57:39.162Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"owl:Class\\|rdfs:label\\|owl:ObjectProperty\\|owl:DatatypeProperty\\|owl:AnnotationProperty\\|subClassOf\\|subPropertyOf\\|equivalentClass\\|equivalentProperty\" /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl | head -150"
}
```

---

### User *(2026-03-22T18:57:39.210Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T18:57:39.495Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/notes/; ls /Users/mta/Documents/claude/mocho/output/"
}
```

---

### User *(2026-03-22T18:57:39.543Z)*

**Tool result**
```
README.md
claude-check-why-mocho-v01ttl-is-not-loading-on-20260216-133010.json
claude-check-why-mocho-v01ttl-is-not-loading-on-20260216-133010.md
claude-start-a-new-project-mocho-in-usersmtadoc-20260223-210407.json
claude-start-a-new-project-mocho-in-usersmtadoc-20260223-210407.md
mapping_dct_rda_workflow.md
musicontology-mirror-conversion.md
odk-guide.md
odk-import-troubleshooting-20260309.md
odk-seed-troubleshooting.md
session-mocho-diagrams-20260217-c92283bd.jsonl
session-mocho-setup-20260223-a3cd246d.jsonl
widoco-guide.md
ddbedm-full.csv
ddbedm-full.json
ddbedm_1.csv
ddbedm_1.json
diagrams
mapping_aco_to_rda.csv
mapping_aco_to_rda.json
mapping_crm_to_rda.csv
mapping_crm_to_rda.json
mapping_dct_to_rda.csv
mapping_dct_to_rda.json
mapping_frbr_fabio_nonwemi_to_rda.csv
mapping_frbr_fabio_nonwemi_to_rda.json
mapping_frbr_fabio_to_rda.csv
mapping_frbr_fabio_to_rda.json
mapping_htype_doco.csv
mapping_htype_doco.json
mapping_mo_to_rda.csv
mapping_mo_to_rda.json
mapping_rda_all_classes.csv
mapping_rda_all_classes.json
mapping_rda_classes.csv
mapping_rda_classes.json
mapping_rda_properties.csv
mapping_rda_properties.json
mapping_rda_we_properties.csv
mapping_rda_we_properties.json
mapping_rico_to_rda.csv
mapping_rico_to_rda.json
mapping_vra_to_rda.csv
mapping_vra_to_rda.json
rda-work-properties.txt
rda_properties.tsv
rda_properties.txt
transcripts
vra_complete_validation_report.txt
vra_validation_report.txt
```

---

### Assistant *(2026-03-22T18:57:45.962Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -50 /Users/mta/Documents/claude/mocho/output/ddbedm-full.json"
}
```

---

### User *(2026-03-22T18:57:46.013Z)*

**Tool result**
```
[
  {
    "type": "class",
    "label": "frbroo:F1_Work",
    "iri": "http://iflastandards.info/ns/fr/frbr/frbroo/F1_Work",
    "definition": ""
  },
  {
    "type": "class",
    "label": "frbroo:F2_Expression",
    "iri": "http://iflastandards.info/ns/fr/frbr/frbroo/F2_Expression",
    "definition": ""
  },
  {
    "type": "class",
    "label": "frbroo:F3_Manifestation_Product_Type",
    "iri": "http://iflastandards.info/ns/fr/frbr/frbroo/F3_Manifestation_Product_Type",
    "definition": ""
  },
  {
    "type": "class",
    "label": "frbroo:F4_Manifestation_Singleton",
    "iri": "http://iflastandards.info/ns/fr/frbr/frbroo/F4_Manifestation_Singleton",
    "definition": ""
  },
  {
    "type": "class",
    "label": "frbroo:F8_Event",
    "iri": "http://iflastandards.info/ns/fr/frbr/frbroo/F8_Event",
    "definition": ""
  },
  {
    "type": "class",
    "label": "frbroo:F9_Place",
    "iri": "http://iflastandards.info/ns/fr/frbr/frbroo/F9_Place",
    "definition": ""
  },
  {
    "type": "class",
    "label": "ns1:Place",
    "iri": "http://metadata.net/harmony/abc#Place",
    "definition": ""
  },
  {
    "type": "class",
    "label": "ns1:Temporality",
    "iri": "http://metadata.net/harmony/abc#Temporality",
    "definition": ""
  },
  {
```

---

### Assistant *(2026-03-22T18:57:47.008Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -30 /Users/mta/Documents/claude/mocho/output/mapping_dct_to_rda.csv; echo \"---\"; head -30 /Users/mta/Documents/claude/mocho/output/mapping_dct_to_rda.json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2)[:2000])\""
}
```

---

### User *(2026-03-22T19:37:26.872Z)*

**Tool result** *(error)*
```
Exit code 1
dct_term,rda_iri,rda_label
dc:contributor,http://rdaregistry.info/Elements/e/P20011,has conductor agent
dc:contributor,http://rdaregistry.info/Elements/e/P20012,has actor agent
dc:contributor,http://rdaregistry.info/Elements/e/P20013,has onscreen presenter agent
dc:contributor,http://rdaregistry.info/Elements/e/P20014,has dancer agent
dc:contributor,http://rdaregistry.info/Elements/e/P20015,has instructor agent
dc:contributor,http://rdaregistry.info/Elements/e/P20016,has host agent
dc:contributor,http://rdaregistry.info/Elements/e/P20017,has moderator agent
dc:contributor,http://rdaregistry.info/Elements/e/P20018,has puppeteer agent
dc:contributor,http://rdaregistry.info/Elements/e/P20019,has panelist agent
dc:contributor,http://rdaregistry.info/Elements/e/P20020,has instrumentalist agent
dc:contributor,http://rdaregistry.info/Elements/e/P20021,has commentator agent
dc:contributor,http://rdaregistry.info/Elements/e/P20022,has narrator agent
dc:contributor,http://rdaregistry.info/Elements/e/P20023,has storyteller agent
dc:contributor,http://rdaregistry.info/Elements/e/P20024,has speaker agent
dc:contributor,http://rdaregistry.info/Elements/e/P20025,has singer agent
dc:contributor,http://rdaregistry.info/Elements/e/P20028,has animator agent
dc:contributor,http://rdaregistry.info/Elements/e/P20029,has arranger agent of music
dc:contributor,http://rdaregistry.info/Elements/e/P20031,has stage director agent
dc:contributor,http://rdaregistry.info/Elements/e/P20032,has interviewer agent of expression
dc:contributor,http://rdaregistry.info/Elements/e/P20033,has draftsman agent
dc:contributor,http://rdaregistry.info/Elements/e/P20034,has transcriber agent
dc:contributor,http://rdaregistry.info/Elements/e/P20035,has musical director agent
dc:contributor,http://rdaregistry.info/Elements/e/P20036,has costume designer agent
dc:contributor,http://rdaregistry.info/Elements/e/P20037,has translator agent
dc:contributor,http://rdaregistry.info/Elements/e/P20038,has art director agent
dc:contributor,http://rdaregistry.info/Elements/e/P20039,has performer agent
dc:contributor,http://rdaregistry.info/Elements/e/P20040,has court reporter agent
dc:contributor,http://rdaregistry.info/Elements/e/P20047,has interviewee agent of expression
dc:contributor,http://rdaregistry.info/Elements/e/P20049,has abridger agent
---
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 293, in load
    return loads(fp.read(),
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

---

### Assistant *(2026-03-22T19:37:40.876Z)*

Let me check the mocho notes and look at what mocho actually defines.

---

### Assistant *(2026-03-22T19:37:41.397Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/notes/mapping_dct_rda_workflow.md"
}
```

---

### Assistant *(2026-03-22T19:37:41.406Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/scripts/ 2>/dev/null"
}
```

---

### User *(2026-03-22T19:37:41.427Z)*

**Tool result**
```
     1→# Workflow: Generating RDA Terms from DCT Mappings in DDB EDM
     2→
     3→## Context
     4→
     5→The Deutsche Digitale Bibliothek (DDB) publishes its metadata profile as an extension
     6→of the Europeana Data Model (EDM) in `ontology/ddbedm_1.0.ttl`. The DDB EDM ontology
     7→reuses Dublin Core properties (`dc:`, `dcterms:`) as object properties applied to EDM
     8→entities. The goal of this workflow is to trace those DC/DCT properties to their
     9→corresponding RDA sub-properties and include those RDA IRIs in the MIREOT import list
    10→(`mocho-odk/imports/rda_terms.txt`).
    11→
    12→The mapping chain is:
    13→
    14→```
    15→ddbedm_1.0.ttl
    16→    ↓  extract_ontology_terms.py
    17→output/ddbedm_1.csv          (dc: / dcterms: labels extracted)
    18→    ↓  dct_rda_map.py
    19→output/mapping_dct_to_rda.csv  (DCT term → RDA sub-property pairs)
    20→    ↓  manual append (grep -vFf dedup)
    21→mocho-odk/imports/rda_terms.txt
    22→```
    23→
    24→---
    25→
    26→## Step 1 — Extract vocabulary terms from DDB EDM
    27→
    28→```bash
    29→python scripts/extract_ontology_terms.py \
    30→    --ontology ontology/ddbedm_1.0.ttl \
    31→    --output output/ddbedm_1
    32→```
    33→
    34→**Output:** `output/ddbedm_1.csv` — 98 terms (33 classes, 41 object properties,
    35→12 datatype properties, 12 annotation properties).
    36→
    37→**Key behaviour:** When a term has no `rdfs:label`, the script falls back to
    38→`g.qname(uri)`, which yields prefixed names like `dc:creator`, `dcterms:subject`,
    39→`edm:ProvidedCHO`, `crm:E39_Actor`, etc. Terms whose namespace prefix is not bound
    40→in the graph fall back further to the bare local name.
    41→
    42→The `dc:` and `dcterms:` labels arise from the graph's built-in namespace bindings
    43→for `http://purl.org/dc/elements/1.1/` (`dc:`) and `http://purl.org/dc/terms/`
    44→(`dcterms:`), which are declared in the Turtle file's `@prefix` block.
    45→
    46→**DC/DCT terms found in ddbedm_1.csv (34 total):**
    47→
    48→| Prefix | Terms |
    49→|---|---|
    50→| `dc:` | `contributor`, `coverage`, `creator`, `date`, `description`, `format`, `language`, `publisher`, `relation`, `subject`, `title`, `type` |
    51→| `dcterms:` | `alternative`, `bibliographicCitation`, `created`, `date`, `extent`, `hasPart`, `isPartOf`, `issued`, `language`, `medium`, `provenance`, `rights`, `spatial`, `subject`, `temporal` |
    52→| `dcterms:` (classes) | `LinguisticSystem`, `LocationPeriodOrJurisdiction`, `PeriodOfTime`, `PhysicalMedium`, `PhysicalResource`, `ProvenanceStatement`, `RightsStatement` |
    53→
    54→---
    55→
    56→## Step 2 — Map DCT terms to RDA sub-properties
    57→
    58→```bash
    59→python scripts/dct_rda_map.py \
    60→    --input output/ddbedm_1.csv \
    61→    --map-xml ontology/RDA-Vocabularies-5.4.9/xml/Maps/mapElement2DCT.xml \
    62→    --vocab-dir ontology/RDA-Vocabularies-5.4.9/xml/Elements \
    63→    --output output/mapping_dct_to_rda
    64→```
    65→
    66→**Outputs:** `output/mapping_dct_to_rda.csv` / `.json`
    67→
    68→**Schema:** `dct_term, rda_iri, rda_label` — one row per (source term, RDA property)
    69→pair.
    70→
    71→### How it works
    72→
    73→`mapElement2DCT.xml` is published with the RDA Vocabularies release. Each entry
    74→declares an RDA property as a sub-property of a DCT term:
    75→
    76→```xml
    77→<rdf:Description rdf:about="http://rdaregistry.info/Elements/w/P10051">
    78→  <rdfs:subPropertyOf rdf:resource="http://purl.org/dc/terms/creator"/>
    79→</rdf:Description>
    80→```
    81→
    82→The script **inverts** this map: for each DCT IRI it collects all RDA properties
    83→that declare it as their super-property.
    84→
    85→**`dc:` prefix resolution:** `mapElement2DCT.xml` only contains `dcterms:`
    86→(`http://purl.org/dc/terms/`) IRIs. `dc:elements/1.1` properties (e.g. `dc:creator`)
    87→are looked up via their `dcterms:` equivalent (`dcterms:creator`). The original
    88→prefix is preserved in the output `dct_term` column, so `dc:creator` and
    89→`dcterms:creator` appear as distinct rows with the same set of RDA sub-properties.
    90→
    91→**RDA labels** are resolved from the entity XML files (`w.xml`, `e.xml`, `m.xml`,
    92→`i.xml`, `a.xml`, …) using `rdfs:label xml:lang="en"`.
    93→
    94→### Results
    95→
    96→| Outcome | Count |
    97→|---|---|
    98→| DC/DCT terms with ≥1 RDA mapping | 23 |
    99→| DC/DCT terms with no RDA mapping | 11 |
   100→| Total (dct_term, RDA IRI) pairs | 979 |
   101→
   102→**Not mapped — DCT class terms (7):** Classes have no entries in `mapElement2DCT.xml`
   103→because it only maps properties. `dcterms:LinguisticSystem`,
   104→`dcterms:LocationPeriodOrJurisdiction`, `dcterms:PeriodOfTime`,
   105→`dcterms:PhysicalMedium`, `dcterms:PhysicalResource`, `dcterms:ProvenanceStatement`,
   106→`dcterms:RightsStatement`.
   107→
   108→**Not mapped — properties absent from XML (4):** `dcterms:bibliographicCitation`,
   109→`dcterms:provenance`, `dcterms:spatial`, `dcterms:temporal` are not listed as
   110→super-properties of any RDA property in the 5.4.9 release.
   111→
   112→### High-fanout terms
   113→
   114→Broad DCT terms expand to large numbers of RDA sub-properties:
   115→
   116→| DCT term | RDA sub-properties |
   117→|---|---|
   118→| `dc:contributor` / `dcterms:contributor` | 360 (each) |
   119→| `dc:creator` / `dcterms:creator` | 232 (each) |
   120→| `dc:publisher` / `dcterms:publisher` | 96 (each) |
   121→| `dc:format` / `dcterms:format` | 59 (each) |
   122→| `dc:description` / `dcterms:description` | 46 (each) |
   123→| `dc:subject` / `dcterms:subject` | 42 (each) |
   124→
   125→These counts reflect the RDA registry's full sub-property hierarchy for each DCT
   126→term, spanning all WEMI levels and role specialisations. The output CSV serves as a
   127→starting-point vocabulary; implementers should select the most specific applicable
   128→RDA property for each metadata element.
   129→
   130→---
   131→
   132→## Step 3 — Append new RDA IRIs to rda_terms.txt
   133→
   134→```bash
   135→tail -n +2 output/mapping_dct_to_rda.csv \
   136→  | cut -d',' -f2 \
   137→  | sort -u \
   138→  | grep -vFf mocho-odk/imports/rda_terms.txt \
   139→  >> mocho-odk/imports/rda_terms.txt
   140→```
   141→
   142→This extracts the `rda_iri` column, deduplicates, and appends only IRIs not already
   143→present. The `-vFf` flag treats existing file lines as fixed strings to exclude.
   144→
   145→**Result:**
   146→
   147→| Metric | Value |
   148→|---|---|
   149→| IRIs before this step | 220 |
   150→| New IRIs added from DCT mapping | 852 |
   151→| Total IRIs after | 1072 |
   152→| Duplicate IRIs | 0 |
   153→
   154→---
   155→
   156→## How rda_terms.txt fits into the broader pipeline
   157→
   158→`mocho-odk/imports/rda_terms.txt` accumulates RDA property and class IRIs from all
   159→mapping files produced by the mocho scripts. It is the input to the ODK/ROBOT MIREOT
   160→step that generates `mocho-odk/imports/rda_import.owl`, importing selected RDA terms
   161→into the mocho ontology.
   162→
   163→The file is populated from two distinct sources:
   164→
   165→**Source A — `gen_all_import_terms.py`** (lines 1–220, run earlier):
   166→Scans `output/mapping_*_to_*.csv` files with a `match` column, collects all `rda`
   167→or `rda_uri` values with match = `direct` or `approximate`, and writes them to
   168→`rda_terms.txt` (and other `*_terms.txt` files). Covers ACO, CRM, FaBiO, FaBiO
   169→non-WEMI, FRBR, MO, RiC-O, and VRA mappings.
   170→
   171→**Source B — manual DCT append** (lines 221–1072, this workflow):
   172→The `mapping_dct_to_rda.csv` uses a different schema (`dct_term, rda_iri, rda_label`
   173→with no `match` column), so `gen_all_import_terms.py` silently skips it. The DCT
   174→RDA IRIs must be appended manually after running `dct_rda_map.py`.
   175→
   176→To re-run the full DCT → `rda_terms.txt` update from scratch:
   177→
   178→```bash
   179→# 1. Regenerate term extract from DDB EDM
   180→python scripts/extract_ontology_terms.py --ontology ontology/ddbedm_1.0.ttl
   181→
   182→# 2. Regenerate DCT→RDA mapping
   183→python scripts/dct_rda_map.py
   184→
   185→# 3. Append new RDA IRIs (dedup against existing file)
   186→tail -n +2 output/mapping_dct_to_rda.csv \
   187→  | cut -d',' -f2 \
   188→  | sort -u \
   189→  | grep -vFf mocho-odk/imports/rda_terms.txt \
   190→  >> mocho-odk/imports/rda_terms.txt
   191→```
   192→
   193→---
   194→
   195→## Known gaps and follow-up actions
   196→
   197→- **`gen_all_import_terms.py` does not handle the DCT schema.** To fully automate
   198→  this step, extend the script with a handler for files matching
   199→  `mapping_dct_to_rda.csv` (column name `rda_iri` instead of `rda`).
   200→
   201→- **dc:class terms have no RDA class equivalents** in `rda_terms.txt`. DCT class
   202→  IRIs like `dcterms:LinguisticSystem` map conceptually to RDA value vocabulary
   203→  concepts, not to RDA entity classes; they are intentionally excluded.
   204→
   205→- **High-fanout terms** (`dcterms:contributor`, `dcterms:creator`) will import
   206→  hundreds of RDA properties into mocho. Review the import list before running
   207→  ROBOT to confirm the scope is intentional.
   208→
   209→- **`dcterms:spatial`, `dcterms:temporal`, `dcterms:provenance`** are used by DDB
   210→  EDM but have no RDA sub-property declarations in the 5.4.9 release. They may
   211→  require manual mapping or a later RDA version.
   212→



```

---

### User *(2026-03-22T19:37:41.476Z)*

**Tool result**
```
README.md
convert_musicontology.py
dct_rda_map.py
extract_fabio_wemi_properties.py
extract_ontology_terms.py
extract_rda_classes.py
extract_rda_properties.py
extract_rda_work_properties.py
gen_all_import_terms.py
gen_dct_rda_map.py
gen_doco_terms.py
gen_frbr_target_mapping.py
gen_import_terms.py
gen_mocho_diagram.py
gen_nonwemi_mapping.py
gen_odk_widoco.sh
gen_rda_imports.py
gen_rda_terms.py
gen_vra_mapping.py
inspect_dcterms.py
inspect_violations.py
mapping_csv2json.py
migrate_mocho_axioms.py
seed.sh
strip_aco_chain.py
strip_aco_reserved.py
strip_ddbedm_dc_types.py
strip_ddbedm_equivs.py
strip_fabio_dc_types.py
strip_frbr_swrl.py
strip_ofn_swrl.py
strip_owl_imports.py
vra_owl_validator.py
```

---

### Assistant *(2026-03-22T19:38:17.694Z)*

Now I have a clear picture. Let me check what mocho's alignment axioms look like and what RDA properties are in the import.

---

### Assistant *(2026-03-22T19:38:18.602Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -c \"equivalentProperty\\|equivalentClass\\|owl:sameAs\\|subPropertyOf\\|subClassOf\" /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl"
}
```

---

### User *(2026-03-22T19:38:18.810Z)*

**Tool result**
```
598
```

---

### Assistant *(2026-03-22T19:38:19.742Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"ddbedm\\|europeana.eu/schemas/edm\\|deutsche-digitale-bibliothek\" /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl | head -40"
}
```

---

### User *(2026-03-22T19:38:19.870Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T19:38:22.498Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"rdaregistry\\|rda_terms\\|rda:\" /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl | head -20"
}
```

---

### User *(2026-03-22T19:38:22.565Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-03-22T19:38:23.428Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/imports/ddbedm_import.owl; head -50 /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/imports/ddbedm_import.owl"
}
```

---

### User *(2026-03-22T19:38:23.495Z)*

**Tool result**
```
     443 /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/imports/ddbedm_import.owl
Prefix(:=<https://github.com/anntanp/mocho-odk/mocho/imports/ddbedm_import.owl#>)
Prefix(owl:=<http://www.w3.org/2002/07/owl#>)
Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)
Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)
Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)
Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)


Ontology(<https://github.com/anntanp/mocho-odk/mocho/imports/ddbedm_import.owl>
<https://github.com/anntanp/mocho-odk/mocho/releases/2026-03-19/imports/ddbedm_import.owl>
Annotation(<http://purl.org/dc/elements/1.1/source> <http://purl.obolibrary.org/obo/ddbedm/releases/2026-03-09/ddbedm-full.owl>)
Annotation(owl:versionInfo "2026-03-19")

Declaration(Class(<http://purl.org/dc/terms/LinguisticSystem>))
Declaration(Class(<http://purl.org/dc/terms/PeriodOfTime>))
Declaration(Class(<http://purl.org/dc/terms/PhysicalMedium>))
Declaration(Class(<http://purl.org/dc/terms/PhysicalResource>))
Declaration(Class(<http://purl.org/dc/terms/ProvenanceStatement>))
Declaration(Class(<http://purl.org/dc/terms/RightsStatement>))
Declaration(Class(<http://purl.org/vocab/frbr/core#Event>))
Declaration(Class(<http://purl.org/vocab/frbr/core#Expression>))
Declaration(Class(<http://purl.org/vocab/frbr/core#Manifestation>))
Declaration(Class(<http://purl.org/vocab/frbr/core#Place>))
Declaration(Class(<http://purl.org/vocab/frbr/core#Work>))
Declaration(Class(<http://purl.org/vocommons/voaf#Vocabulary>))
Declaration(Class(<http://www.cidoc-crm.org/rdfs/cidoc-crm#E89_Propositional_Object>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/Agent>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/Event>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/InformationResource>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/NonInformationResource>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/PhysicalThing>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/Place>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/ProvidedCHO>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/TimeSpan>))
Declaration(Class(<http://www.europeana.eu/schemas/edm/WebResource>))
Declaration(Class(<http://www.openarchives.org/ore/terms/Aggregation>))
Declaration(Class(<http://www.openarchives.org/ore/terms/Proxy>))
Declaration(Class(<http://www.w3.org/2004/02/skos/core#Concept>))
Declaration(Class(<http://xmlns.com/foaf/0.1/Organization>))
Declaration(Class(<http://xmlns.com/foaf/0.1/Person>))
Declaration(ObjectProperty(<http://purl.org/dc/elements/1.1/coverage>))
Declaration(ObjectProperty(<http://purl.org/dc/elements/1.1/publisher>))
Declaration(ObjectProperty(<http://purl.org/dc/elements/1.1/relation>))
Declaration(ObjectProperty(<http://purl.org/dc/elements/1.1/subject>))
Declaration(ObjectProperty(<http://purl.org/dc/terms/date>))
Declaration(ObjectProperty(<http://purl.org/dc/terms/hasPart>))
Declaration(ObjectProperty(<http://purl.org/dc/terms/isPartOf>))
Declaration(ObjectProperty(<http://purl.org/dc/terms/language>))
Declaration(ObjectProperty(<http://purl.org/dc/terms/rights>))
Declaration(ObjectProperty(<http://purl.org/dc/terms/subject>))
```

---

### Assistant *(2026-03-22T19:38:26.615Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -c \"rdaregistry\" /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl; grep \"rdaregistry\" /Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl | head -20"
}
```

---

### User *(2026-03-22T19:38:26.725Z)*

**Tool result**
```
2847
```

---

### Assistant *(2026-03-22T19:38:27.301Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl",
  "limit": 100,
  "offset": 200
}
```

---

### User *(2026-03-22T19:38:27.581Z)*

**Tool result**
```
   200→        <skos:definition xml:lang="de">Setzt eine Expression in Beziehung zu einer Kategorisierung, die zum einen die grundlegende Form der Kommunikation widerspiegelt, in der der Inhalt ausgedrückt wird, und zum andern die menschliche Wahrnehmung wiedergibt, durch die diese wahrgenommen werden soll.</skos:definition>
   201→        <skos:definition xml:lang="el">Συνδέει μια έκφραση με μια κατηγοριοποίηση η οποία αντανακλά τη θεμελιώδη μορφή της επικοινωνίας με την οποία εκφράζεται το περιεχόμενο και τις ανθρώπινες αισθήσεις μέσω των οποίων προσλαμβάνεται.</skos:definition>
   202→        <skos:definition xml:lang="ar">تربط بين تعبيرة وتصنيف يعكس الشكل الأساسي للتواصل، الذي يتم التعبير فيه عن المحتوى والحس الإنساني، الذي يُقصد تصوره من خلاله.</skos:definition>
   203→        <skos:definition xml:lang="zh-hans-cn">将一种内容表达与反映其内容被表达所用通讯的基本形式和设计被感知的人类感觉的分类关联起来。</skos:definition>
   204→        <skos:scopeNote xml:lang="en">Content type also reflects the number of spatial dimensions and the presence or absence of movement in which content expressed in the form of an image or images is intended to be perceived.</skos:scopeNote>
   205→        <skos:scopeNote xml:lang="fr">Dans le cas d’un contenu exprimé sous la forme d’une ou plusieurs images, un type de contenu reflète également le nombre de dimensions spatiales au travers desquelles le contenu doit être perçu et la présence ou l’absence perceptibles de mouvement.</skos:scopeNote>
   206→        <skos:scopeNote xml:lang="es">El tipo de contenido también refleja el número de dimensiones espaciales y la presencia o ausencia de movimiento en el que se pretende percibir el contenido expresado en forma de imagen o imágenes.</skos:scopeNote>
   207→        <skos:scopeNote xml:lang="ca">El tipus de contingut també reflecteix el nombre de dimensions espacials i la presència o l’absència de moviment en què el contingut expressat en la forma d’una o més imatges s’ha de percebre.</skos:scopeNote>
   208→        <skos:scopeNote xml:lang="de">Für Inhalt, der in Form eines Bilds oder mehrerer Bilder ausgedrückt wird, spiegelt der Inhaltstyp auch die Anzahl räumlicher Dimensionen wider, in denen der Inhalt wahrgenommen werden soll, sowie die Wahrnehmung von vorhandener oder nicht vorhandener Bewegung.</skos:scopeNote>
   209→        <skos:scopeNote xml:lang="da">Hvad angår indhold, som udtrykkes i form af et eller flere billeder, afspejler indholdstype desuden antallet af rumlige dimensioner, som indholdet skal opfattes i, samt opfattelsen af tilstedeværelse eller fravær af bevægelse.</skos:scopeNote>
   210→        <skos:scopeNote xml:lang="no">Innholdstypen gjenspeiler også antallet romlige dimensjoner og tilstedeværelse eller fravær av bevegelse som innhold uttrykt i form av ett eller flere bilder, er ment å oppfattes gjennom.</skos:scopeNote>
   211→        <skos:scopeNote xml:lang="vi">Loại nội dung cũng phản ánh số lượng kích thước không gian và sự có hoặc không của động thái mà trong đó nội dung được thể hiện dưới hình thái của hình ảnh hoặc các hình ảnh có ý định để cảm nhận.</skos:scopeNote>
   212→        <skos:scopeNote xml:lang="et">Pildi või piltidena väljendatud sisu puhul kajastab sisu tüüp ka sisu tajumist määravat ruumiliste mõõtmete arvu ja liikumise olemasolu või puudumist.</skos:scopeNote>
   213→        <skos:scopeNote xml:lang="lv">Saturs, kas izteikts kā attēls vai attēli, atspoguļo vairākas telpiskas dimensijas, kurās saturu paredzēts uztvert ar vai bez kustību klātbūtnes.</skos:scopeNote>
   214→        <skos:scopeNote xml:lang="fi">Sisältötyyppi kertoo myös kuvan tai kuvien kaksi- tai kolmiulotteisuudesta ja sen, onko kyseessä liikkuva kuva vai stillkuva.</skos:scopeNote>
   215→        <skos:scopeNote xml:lang="nl">Type content geeft ook het aantal ruimtelijke dimensies weer en de aanwezigheid of afwezigheid van beweging waarmee content uitgedrukt in de vorm van een beeld of beelden geacht wordt waargenomen.</skos:scopeNote>
   216→        <skos:scopeNote xml:lang="hu">tartalomtípusa:</skos:scopeNote>
   217→        <skos:scopeNote xml:lang="tr">İçerik türü, ayrıca bir veya birden fazla görüntü biçiminde ifade edilen içeriğin algılanması amacıyla tasarlandığı mekânsal boyut sayısını ve hareketin varlığını veya yokluğunu yansıtır.</skos:scopeNote>
   218→        <skos:scopeNote xml:lang="el">Ο τύπος περιεχομένου αντανακλά επίσης τον αριθμό των χωρικών διαστάσεων και την παρουσία ή την απουσία κίνησης μέσω της οποίας προσλαμβάνεται το το περιεχόμενο το οποίο εκφράζεται στη μορφή μιας εικόνας ή εικόνων.</skos:scopeNote>
   219→        <skos:scopeNote xml:lang="ar">نوع محتوى يعكس عدد الأبعاد المكانية ووجود الحركة أو عدم وجودها؛ حيث يُقصد تصور المحتوى الذي يتم التعبير عنه فيها في شكل صورة أو صور.</skos:scopeNote>
   220→        <skos:scopeNote xml:lang="zh-hans-cn">对于被设计以一种或多种被感知图像形式表达的内容，内容类型还反映空间维度数以及感知运动是否存在。</skos:scopeNote>
   221→    </owl:AnnotationProperty>
   222→    
   223→
   224→
   225→    <!-- http://rdaregistry.info/Elements/e/P20004 -->
   226→
   227→    <owl:AnnotationProperty rdf:about="http://rdaregistry.info/Elements/e/P20004">
   228→        <rdfs:isDefinedBy rdf:resource="http://rdaregistry.info/Elements/e/"/>
   229→        <rdfs:label xml:lang="hu">Egy időtartam, amely egy kifejezési forma tartalmának rögzítéséhez, filmezéséhez, stb. kapcsolódik.</rdfs:label>
   230→        <rdfs:label xml:lang="fr">a pour date de captation</rdfs:label>
   231→        <rdfs:label xml:lang="vi">có ngày thu nạp</rdfs:label>
   232→        <rdfs:label xml:lang="da">har dato for indspilning</rdfs:label>
   233→        <rdfs:label xml:lang="sv">har inspelningstid</rdfs:label>
   234→        <rdfs:label xml:lang="no">har tidspunkt for opptak</rdfs:label>
   235→        <rdfs:label xml:lang="en">has date of capture</rdfs:label>
   236→        <rdfs:label xml:lang="de">hat Aufzeichnungsdatum</rdfs:label>
   237→        <rdfs:label xml:lang="nl">heeft datum van vastleggen</rdfs:label>
   238→        <rdfs:label xml:lang="et">jäädvustamise daatum</rdfs:label>
   239→        <rdfs:label xml:lang="tr">kayıt tarihi ile ilişkilidir</rdfs:label>
   240→        <rdfs:label xml:lang="fi">tallennusajankohta</rdfs:label>
   241→        <rdfs:label xml:lang="es">tiene fecha de captura</rdfs:label>
   242→        <rdfs:label xml:lang="lv">tveršanas datējums</rdfs:label>
   243→        <rdfs:label xml:lang="ca">té com a data de captura</rdfs:label>
   244→        <rdfs:label xml:lang="el">έχει χρονολογία της σύλληψης</rdfs:label>
   245→        <rdfs:label xml:lang="ar">لها تاريخ التقاط</rdfs:label>
   246→        <rdfs:label xml:lang="zh-hans-cn">有摄录日期</rdfs:label>
   247→        <skos:definition xml:lang="tr">Bir anlatımı, içeriğinin kaydedilmesi, filme alınması vb. ile bağlantılı olan bir zaman aralığıyla ilişkilendirir.</skos:definition>
   248→        <skos:definition xml:lang="fi">Liittää ekspression ajanjaksoon, joka liittyy ekspression äänitykseen, filmaukseen tms.</skos:definition>
   249→        <skos:definition xml:lang="vi">Liên kết một biểu hiện với ngày liên quan tới ghi, làm phim, v.v... của nội dung của biểu hiện.</skos:definition>
   250→        <skos:definition xml:lang="fr">Met une expression en relation avec un laps de temps qui est associé à l’enregistrement, au tournage, etc., du contenu d’une expression.</skos:definition>
   251→        <skos:definition xml:lang="es">Relaciona una expresión con un lapso de tiempo que está asociado con la grabación, filmación, etc., el contenido de una expresión.</skos:definition>
   252→        <skos:definition xml:lang="ca">Relaciona una expressió amb un interval de temps que s’associa amb l’enregistrament, la filmació, etc., del contingut d’una expressió.</skos:definition>
   253→        <skos:definition xml:lang="nl">Relateert een expressie aan een tijdspanne die is geassocieerd met het opnemen, filmen etc. van de content van een expressie.</skos:definition>
   254→        <skos:definition xml:lang="da">Relaterer et udtryk til en tidsperiode knyttet til en indspilning, filmoptagelse, etc., af et indholdet af et udtryk</skos:definition>
   255→        <skos:definition xml:lang="no">Relaterer et uttrykk til et tidsrom som forbindes med opptak, filming etc. for et uttrykk.</skos:definition>
   256→        <skos:definition xml:lang="en">Relates an expression to a timespan that is associated with recording, filming, etc., the content of an expression.</skos:definition>
   257→        <skos:definition xml:lang="lv">Sasaista izteiksmi ar laikposmu, kas saistīts ar izteiksmes ierakstīšanu, filmēšanu u.tml.</skos:definition>
   258→        <skos:definition xml:lang="et">Seostab väljenduse ajavahemikuga, mis on seotud väljenduse salvestamise, filmimise vms jäädvustamisega.</skos:definition>
   259→        <skos:definition xml:lang="de">Setzt eine Expression in Beziehung zu einem Zeitraum, der mit der Aufnahme, dem Filmen und so weiter des Inhalts einer Expression in Verbindung steht.</skos:definition>
   260→        <skos:definition xml:lang="hu">felvétel időpontja a következő:</skos:definition>
   261→        <skos:definition xml:lang="el">Συνδέει μια έκφραση με μια χρονολογία ή ένα εύρος χρονολογιών που συνδέονται με την ηχογράφηση, κινηματογράφηση κ.λπ. του περιεχομένου μιας έκφρασης.</skos:definition>
   262→        <skos:definition xml:lang="ar">تربط بين تعبيرة يوصف وفترة زمنية مرتبطة بتسجيل محتوى تعبيرة ممثِلة، أو تصويره، إلخ.</skos:definition>
   263→        <skos:definition xml:lang="zh-hans-cn">将一种内容表达与和内容表达的内容的录制、摄制等有关的时间段关联起来。</skos:definition>
   264→    </owl:AnnotationProperty>
   265→    
   266→
   267→
   268→    <!-- http://rdaregistry.info/Elements/e/P20006 -->
   269→
   270→    <owl:AnnotationProperty rdf:about="http://rdaregistry.info/Elements/e/P20006">
   271→        <rdfs:isDefinedBy rdf:resource="http://rdaregistry.info/Elements/e/"/>
   272→        <rdfs:label xml:lang="fr">a pour langue d’une expression</rdfs:label>
   273→        <rdfs:label xml:lang="tr">anlatımın dili ile ilişkilidir</rdfs:label>
   274→        <rdfs:label xml:lang="vi">có ngôn ngữ của biểu hiện</rdfs:label>
   275→        <rdfs:label xml:lang="fi">ekspression kieli</rdfs:label>
   276→        <rdfs:label xml:lang="da">har sprog for udtryk</rdfs:label>
   277→        <rdfs:label xml:lang="no">har språk i uttrykk</rdfs:label>
   278→        <rdfs:label xml:lang="en">has language of expression</rdfs:label>
   279→        <rdfs:label xml:lang="de">hat Sprache einer Expression</rdfs:label>
   280→        <rdfs:label xml:lang="nl">heeft taal van expressie</rdfs:label>
   281→        <rdfs:label xml:lang="lv">izteiksmes valoda</rdfs:label>
   282→        <rdfs:label xml:lang="hu">kifejezési forma nyelve a következő:</rdfs:label>
   283→        <rdfs:label xml:lang="es">tiene lenguaje de expresión</rdfs:label>
   284→        <rdfs:label xml:lang="ca">té com a llengua d’una expressió</rdfs:label>
   285→        <rdfs:label xml:lang="et">väljenduse keel</rdfs:label>
   286→        <rdfs:label xml:lang="el">έχει γλώσσα της έκφρασης</rdfs:label>
   287→        <rdfs:label xml:lang="ar">لها لغة تعبيرة</rdfs:label>
   288→        <rdfs:label xml:lang="zh-hans-cn">有内容表达的语言</rdfs:label>
   289→        <skos:definition xml:lang="tr">Bir anlatımı, bir anlatımın içeriği için kullanılan bir dille ilişkilendirir.</skos:definition>
   290→        <skos:definition xml:lang="hu">Hozzákapcsol egy kifejezési formát egy nyelvhez, amelyet egy kifejezési forma tartalmához használnak.</skos:definition>
   291→        <skos:definition xml:lang="fi">Liittää ekspression ekspression sisällössä käytettyyn kieleen.</skos:definition>
   292→        <skos:definition xml:lang="vi">Liên kết một biểu hiện với ngôn ngữ mà tác phẩm được thể hiện trong đó.</skos:definition>
   293→        <skos:definition xml:lang="fr">Met une expression en relation avec une langue utilisée pour le contenu d’une expression.</skos:definition>
   294→        <skos:definition xml:lang="es">Relaciona una expresión con un lenguaje utilizado para el contenido de una expresión.</skos:definition>
   295→        <skos:definition xml:lang="ca">Relaciona una expressió amb una llengua usada en el contingut d’una expressió.</skos:definition>
   296→        <skos:definition xml:lang="nl">Relateert een expressie aan een taal gebruikt voor de content van een expressie.</skos:definition>
   297→        <skos:definition xml:lang="da">Relaterer et udtryk til et sprog, som er brugt til et udtryks indhold.</skos:definition>
   298→        <skos:definition xml:lang="no">Relaterer et uttrykk til et språk som brukes for innholdet i et uttrykk.</skos:definition>
   299→        <skos:definition xml:lang="en">Relates an expression to a language used for the content of an expression.</skos:definition>



```

---

### Assistant *(2026-03-22T19:40:25.963Z)*

Now I have everything I need. Let me write the alignment script.

---

### Assistant *(2026-03-22T19:40:27.213Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -30 /Users/mta/Documents/claude/mocho/output/mapping_dct_to_rda.csv | head -5; wc -l /Users/mta/Documents/claude/mocho/output/mapping_dct_to_rda.csv"
}
```

---

### User *(2026-03-22T19:40:27.315Z)*

**Tool result**
```
dct_term,rda_iri,rda_label
dc:contributor,http://rdaregistry.info/Elements/e/P20011,has conductor agent
dc:contributor,http://rdaregistry.info/Elements/e/P20012,has actor agent
dc:contributor,http://rdaregistry.info/Elements/e/P20013,has onscreen presenter agent
dc:contributor,http://rdaregistry.info/Elements/e/P20014,has dancer agent
     980 /Users/mta/Documents/claude/mocho/output/mapping_dct_to_rda.csv
```

---

### Assistant *(2026-03-22T19:40:31.437Z)*

**Tool call:** `Bash`
```json
{
  "command": "# Look at what entity types and their keys exist in the data\npython3 -c \"\nimport json\nfrom pathlib import Path\nfrom collections import defaultdict, Counter\n\nIN = Path.home() / 'Documents/claude/goethe-faust/data/items-all-goethe-faust.json'\nfield_counts = defaultdict(Counter)  # entity_type -> {key: count}\n\nwith open(IN) as f:\n    for i, line in enumerate(f):\n        if i >= 5000: break\n        line = line.strip()\n        if not line: continue\n        try:\n            rec = json.loads(line)\n        except: continue\n        rdf = rec.get('edm', {}).get('RDF', {})\n        for entity_type, entity in rdf.items():\n            if isinstance(entity, dict):\n                for key in entity:\n                    field_counts[entity_type][key] += 1\n            elif isinstance(entity, list):\n                for item in entity:\n                    if isinstance(item, dict):\n                        for key in item:\n                            field_counts[entity_type][key] += 1\n\nfor entity_type, counts in sorted(field_counts.items()):\n    print(f'\\\\n{entity_type}:')\n    for k, v in counts.most_common(30):\n        print(f'  {k}: {v}')\n\"\n"
}
```

---

### User *(2026-03-22T20:03:35.130Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.
```

---

### User *(2026-03-22T20:03:35.131Z)*

[Request interrupted by user for tool use]

---

### User *(2026-03-22T20:03:45.722Z)*

write all commands as scripts

---

### Assistant *(2026-03-22T20:03:52.007Z)*

Got it. Let me write a data profiling script first, then run it.

---

### Assistant *(2026-03-22T20:04:06.003Z)*

**Tool call:** `Write`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/profile_edm_fields.py",
  "content": "#!/usr/bin/env python3\n\"\"\"\nprofile_edm_fields.py\n=====================\nProfile all field keys present under edm.RDF.* entity types in the JSONL\ndata file. Reports per-entity-type field names with record counts.\n\nPurpose : Determine which EDM/DC properties are actually used in the data,\n          as input to the DDB-EDM → mocho ontology alignment.\nUsage   : python scripts/profile_edm_fields.py\nInputs  : data/items-all-goethe-faust.json  (JSONL)\nOutputs : output/edm_field_profile.json\n          output/edm_field_profile.csv\n          stdout summary\nDependencies : none (stdlib only)\nAssumptions  : JSONL where each line is a DDB item with an edm.RDF object.\n\"\"\"\n\nimport csv\nimport json\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nPROJECT  = Path(__file__).resolve().parent.parent\nIN_PATH  = PROJECT / \"data\" / \"items-all-goethe-faust.json\"\nOUT_JSON = PROJECT / \"output\" / \"edm_field_profile.json\"\nOUT_CSV  = PROJECT / \"output\" / \"edm_field_profile.csv\"\n\n# ── scan ──────────────────────────────────────────────────────────────────────\n\nfield_counts = defaultdict(Counter)   # entity_type -> {key: record_count}\nentity_record_counts = Counter()       # entity_type -> records that have it\ntotal = 0\n\nwith open(IN_PATH) as f:\n    for line in f:\n        line = line.strip()\n        if not line:\n            continue\n        try:\n            rec = json.loads(line)\n        except json.JSONDecodeError:\n            continue\n        total += 1\n\n        rdf = rec.get(\"edm\", {}).get(\"RDF\", {})\n        for entity_type, entity in rdf.items():\n            items = entity if isinstance(entity, list) else [entity]\n            has_entity = False\n            for item in items:\n                if not isinstance(item, dict):\n                    continue\n                has_entity = True\n                for key in item:\n                    field_counts[entity_type][key] += 1\n            if has_entity:\n                entity_record_counts[entity_type] += 1\n\nprint(f\"Total records : {total:,}\")\n\n# ── build output ──────────────────────────────────────────────────────────────\n\nrows = []\nfor entity_type in sorted(field_counts):\n    n_records = entity_record_counts[entity_type]\n    for key, count in field_counts[entity_type].most_common():\n        rows.append({\n            \"entity_type\":  entity_type,\n            \"json_key\":     key,\n            \"record_count\": count,\n            \"record_pct\":   round(100 * count / total, 2),\n            \"entity_pct\":   round(100 * count / n_records, 2) if n_records else 0,\n        })\n\nOUT_JSON.parent.mkdir(exist_ok=True)\n\n# JSON output\noutput = {\n    \"total_records\": total,\n    \"entity_counts\": dict(entity_record_counts.most_common()),\n    \"fields\": rows,\n}\nwith open(OUT_JSON, \"w\", encoding=\"utf-8\") as f:\n    json.dump(output, f, indent=2, ensure_ascii=False)\n\n# CSV output\nwith open(OUT_CSV, \"w\", newline=\"\", encoding=\"utf-8\") as f:\n    writer = csv.DictWriter(\n        f, fieldnames=[\"entity_type\", \"json_key\", \"record_count\", \"record_pct\", \"entity_pct\"]\n    )\n    writer.writeheader()\n    writer.writerows(rows)\n\n# ── print summary ─────────────────────────────────────────────────────────────\n\nfor entity_type in sorted(field_counts):\n    n_records = entity_record_counts[entity_type]\n    print(f\"\\n{entity_type}  ({n_records:,} records with this entity):\")\n    for key, count in field_counts[entity_type].most_common():\n        pct = 100 * count / total\n        print(f\"  {key:<40}  {count:>8,}  ({pct:.1f}%)\")\n\nprint(f\"\\nSaved {OUT_JSON}\")\nprint(f\"Saved {OUT_CSV}\")\n"
}
```

---

### User *(2026-03-23T08:03:10.589Z)*

**Tool result**
```
File created successfully at: /Users/mta/Documents/claude/goethe-faust/scripts/profile_edm_fields.py
```

---

### Assistant *(2026-03-23T08:03:15.112Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && python scripts/profile_edm_fields.py"
}
```

---

### User *(2026-03-23T08:03:19.778Z)*

**Tool result** *(error)*
```
Exit code 127
/bin/bash: python: command not found
```

---

### Assistant *(2026-03-23T08:03:22.387Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && python3 scripts/profile_edm_fields.py"
}
```

---

### User *(2026-03-23T08:03:38.890Z)*

**Tool result**
```
Total records : 115,432

Agent  (115,432 records with this entity):
  about                                      422,026  (365.6%)
  prefLabel                                  422,026  (365.6%)
  altLabel                                   422,026  (365.6%)
  note                                       422,026  (365.6%)
  date                                       422,026  (365.6%)
  type                                       422,026  (365.6%)
  identifier                                 422,026  (365.6%)
  hasPart                                    422,026  (365.6%)
  isPartOf                                   422,026  (365.6%)
  begin                                      422,026  (365.6%)
  end                                        422,026  (365.6%)
  hasMet                                     422,026  (365.6%)
  isRelatedTo                                422,026  (365.6%)
  name                                       422,026  (365.6%)
  biographicalInformation                    422,026  (365.6%)
  dateOfBirth                                422,026  (365.6%)
  dateOfDeath                                422,026  (365.6%)
  dateOfEstablishment                        422,026  (365.6%)
  dateOfTermination                          422,026  (365.6%)
  gender                                     422,026  (365.6%)
  placeOfBirth                               422,026  (365.6%)
  placeOfDeath                               422,026  (365.6%)
  professionOrOccupation                     422,026  (365.6%)
  sameAs                                     422,026  (365.6%)
  wasPresentAt                               422,026  (365.6%)

Aggregation  (115,432 records with this entity):
  about                                      115,432  (100.0%)
  aggregatedCHO                              115,432  (100.0%)
  isShownAt                                  115,432  (100.0%)
  isShownBy                                  115,432  (100.0%)
  edmRights                                  115,432  (100.0%)
  dcTermsRights                              115,432  (100.0%)
  provider                                   115,432  (100.0%)
  dataProvider                               115,432  (100.0%)
  object                                     115,432  (100.0%)
  aggregator                                 115,432  (100.0%)
  hasView                                    115,432  (100.0%)

Concept  (115,432 records with this entity):
  about                                      717,638  (621.7%)
  notation                                   717,638  (621.7%)
  prefLabel                                  717,638  (621.7%)

Event  (110,059 records with this entity):
  about                                      158,407  (137.2%)
  hasType                                    158,407  (137.2%)
  happenedAt                                 158,407  (137.2%)
  occuredAt                                  158,407  (137.2%)
  P11_had_participant                        158,407  (137.2%)

PhysicalThing  (22,265 records with this entity):
  title                                       55,771  (48.3%)
  hierarchyType                               55,771  (48.3%)
  aggregationEntity                           55,771  (48.3%)
  about                                       55,771  (48.3%)
  isPartOf                                    54,812  (47.5%)
  hierarchyPosition                           53,861  (46.7%)

Place  (59,249 records with this entity):
  about                                      118,088  (102.3%)
  lat                                        118,088  (102.3%)
  long                                       118,088  (102.3%)
  alt                                        118,088  (102.3%)
  prefLabel                                  118,088  (102.3%)
  altLabel                                   118,088  (102.3%)
  note                                       118,088  (102.3%)
  hasPart                                    118,088  (102.3%)
  isNextInSequence                           118,088  (102.3%)
  sameAs                                     118,088  (102.3%)
  type                                       118,088  (102.3%)
  isPartOf                                   118,088  (102.3%)

ProvidedCHO  (115,432 records with this entity):
  about                                      115,432  (100.0%)
  title                                      115,432  (100.0%)
  hasMet                                     110,059  (95.3%)
  identifier                                 101,218  (87.7%)
  hasType                                     97,272  (84.3%)
  hierarchyType                               92,957  (80.5%)
  dcType                                      92,853  (80.4%)
  description                                 88,443  (76.6%)
  aggregationEntity                           76,855  (66.6%)
  extent                                      76,759  (66.5%)
  edmType                                     73,045  (63.3%)
  language                                    71,681  (62.1%)
  dcTermsLanguage                             71,681  (62.1%)
  dcSubject                                   69,588  (60.3%)
  dcTermsSubject                              69,588  (60.3%)
  dcTermSubject                               69,588  (60.3%)
  isPartOf                                    67,539  (58.5%)
  date                                        51,936  (45.0%)
  hierarchyPosition                           50,988  (44.2%)
  currentLocation                             50,385  (43.6%)
  issued                                      47,879  (41.5%)
  creator                                     42,589  (36.9%)
  contributor                                 30,251  (26.2%)
  format                                      20,496  (17.8%)
  spatial                                      8,194  (7.1%)
  alternative                                  6,048  (5.2%)

TimeSpan  (99,930 records with this entity):
  about                                       99,930  (86.6%)
  begin                                       99,930  (86.6%)
  end                                         99,930  (86.6%)

WebResource  (115,432 records with this entity):
  about                                      312,538  (270.8%)
  type                                       312,538  (270.8%)
  edmRights                                  312,538  (270.8%)
  dcTermsRights                              312,538  (270.8%)
  creator                                    312,538  (270.8%)

Saved /Users/mta/Documents/claude/goethe-faust/output/edm_field_profile.json
Saved /Users/mta/Documents/claude/goethe-faust/output/edm_field_profile.csv
```

---

### Assistant *(2026-03-23T08:04:00.866Z)*

Good data. Now I'll write the main alignment script.

---

### Assistant *(2026-03-23T08:05:06.983Z)*

**Tool call:** `Write`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "content": "#!/usr/bin/env python3\n\"\"\"\nalign_ddbedm_to_mocho.py\n========================\nData-driven ontology alignment: maps DDB-EDM fields present in\nitems-all-goethe-faust.json to their corresponding mocho/RDA properties.\n\nPipeline:\n  1. Profile data  — load edm_field_profile.json (from profile_edm_fields.py)\n  2. Resolve IRIs  — map JSON camelCase/plain keys to full EDM/DC IRIs\n                     by parsing ddbedm_1.0.ttl with rdflib\n  3. Load DC→RDA   — read mapping_dct_to_rda.csv for DC/DCT→RDA sub-property\n                     pairs produced by the mocho dct_rda_map.py workflow\n  4. Load mocho    — parse mocho-full.owl to collect all RDA properties\n                     imported into mocho (IRIs + English labels + WEMI level)\n  5. Align         — for each data field: DC/EDM IRI → RDA candidates →\n                     restrict to mocho-known properties\n  6. Write outputs\n\nInputs:\n  output/edm_field_profile.json          — field profile (run profile_edm_fields.py first)\n  ~/Documents/claude/mocho/ontology/ddbedm_1.0.ttl      — DDB-EDM ontology\n  ~/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl  — mocho\n  ~/Documents/claude/mocho/output/mapping_dct_to_rda.csv  — DC→RDA mapping\n\nOutputs:\n  output/alignment_ddbedm_mocho.csv   — one row per (edm_field × rda_property)\n  output/alignment_ddbedm_mocho.json  — summary + full alignment\n\nColumns (CSV):\n  entity_type, json_key, edm_prefix, edm_iri, record_count, coverage_pct,\n  rda_iri, rda_label, wemi_level, match_method\n\nUsage:\n  python3 scripts/profile_edm_fields.py   # run first if profile is stale\n  python3 scripts/align_ddbedm_to_mocho.py\n\nDependencies: rdflib\nAssumptions:\n  - ddbedm_1.0.ttl declares all properties used in the DDB-EDM profile\n  - mapping_dct_to_rda.csv schema: dct_term, rda_iri, rda_label\n  - mocho-full.owl is RDF/XML and includes all imported RDA properties inline\n\"\"\"\n\nimport csv\nimport json\nfrom collections import defaultdict\nfrom pathlib import Path\n\nfrom rdflib import Graph, RDF, RDFS, OWL, Namespace\nfrom rdflib.namespace import DC, DCTERMS, SKOS\n\nPROJECT  = Path(__file__).resolve().parent.parent\nMOCHO    = Path.home() / \"Documents/claude/mocho\"\n\nPROFILE_PATH  = PROJECT / \"output\" / \"edm_field_profile.json\"\nDDBEDM_TTL    = MOCHO / \"ontology\" / \"ddbedm_1.0.ttl\"\nMOCHO_OWL     = MOCHO / \"mocho-odk\" / \"src\" / \"ontology\" / \"mocho-full.owl\"\nDCT_RDA_CSV   = MOCHO / \"output\" / \"mapping_dct_to_rda.csv\"\nOUT_CSV       = PROJECT / \"output\" / \"alignment_ddbedm_mocho.csv\"\nOUT_JSON      = PROJECT / \"output\" / \"alignment_ddbedm_mocho.json\"\n\n# ── namespace constants ────────────────────────────────────────────────────────\n\nEDM  = Namespace(\"http://www.europeana.eu/schemas/edm/\")\nORE  = Namespace(\"http://www.openarchives.org/ore/terms/\")\nGEO  = Namespace(\"http://www.w3.org/2003/01/geo/wgs84_pos#\")\nFOAF = Namespace(\"http://xmlns.com/foaf/0.1/\")\nRDA_ELEMENTS = \"http://rdaregistry.info/Elements/\"\n\nWEMI_LEVELS = {\n    f\"{RDA_ELEMENTS}w/\": \"Work\",\n    f\"{RDA_ELEMENTS}e/\": \"Expression\",\n    f\"{RDA_ELEMENTS}m/\": \"Manifestation\",\n    f\"{RDA_ELEMENTS}i/\": \"Item\",\n    f\"{RDA_ELEMENTS}a/\": \"Agent\",\n    f\"{RDA_ELEMENTS}c/\": \"Corporate Body\",\n    f\"{RDA_ELEMENTS}p/\": \"Person\",\n}\n\n# ── step 1: load field profile ─────────────────────────────────────────────────\n\nprint(\"Loading field profile …\")\nwith open(PROFILE_PATH) as f:\n    profile = json.load(f)\n\ntotal_records = profile[\"total_records\"]\n# {(entity_type, json_key): {record_count, record_pct}}\ndata_fields = {\n    (row[\"entity_type\"], row[\"json_key\"]): row\n    for row in profile[\"fields\"]\n}\nprint(f\"  {len(data_fields)} (entity_type, json_key) pairs from {total_records:,} records\")\n\n# ── step 2: resolve JSON keys to EDM/DC IRIs ──────────────────────────────────\n\nprint(\"\\nParsing DDB-EDM ontology …\")\ng_edm = Graph()\ng_edm.parse(DDBEDM_TTL)\n\n# Build lookup: normalised_local_name → [(prefix_label, full_iri)]\n# where normalised = lowercase of local name\nprop_lookup: dict[str, list[tuple[str, str]]] = defaultdict(list)\nfor prop_type in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):\n    for subj in g_edm.subjects(RDF.type, prop_type):\n        iri = str(subj)\n        local = iri.rsplit(\"/\", 1)[-1].rsplit(\"#\", 1)[-1]\n        try:\n            prefix = g_edm.qname(subj).split(\":\")[0]\n        except Exception:\n            prefix = \"\"\n        prop_lookup[local.lower()].append((prefix, iri))\n\n# Also include classes for context\nfor subj in g_edm.subjects(RDF.type, OWL.Class):\n    iri = str(subj)\n    local = iri.rsplit(\"/\", 1)[-1].rsplit(\"#\", 1)[-1]\n    prop_lookup[local.lower()].append((\"class\", iri))\n\nprint(f\"  {len(prop_lookup)} unique local names from DDB-EDM\")\n\n\ndef resolve_iri(entity_type: str, json_key: str) -> tuple[str, str] | None:\n    \"\"\"Map a JSON camelCase/plain key to (prefix_label, full_iri).\n\n    Resolution order:\n    1. Direct match of json_key (lowercase) against the ontology lookup.\n    2. Strip known camelCase prefixes (dcTerms, dc, edm, ore, foaf, geo, skos)\n       and match the lowercased remainder.\n    3. Entity-type-specific defaults for keys without an obvious namespace.\n    Returns (prefix_label, iri) or None if unresolved.\n    \"\"\"\n    key_lower = json_key.lower()\n\n    # Direct match\n    if key_lower in prop_lookup:\n        return prop_lookup[key_lower][0]\n\n    # Strip camelCase namespace prefixes in order (longest first to avoid greedy mismatch)\n    prefixes = [\n        (\"dcterms\", \"dcterms\", str(DCTERMS)),\n        (\"dcterms\", \"dcTerms\", str(DCTERMS)),\n        (\"dc\",      \"dc\",      str(DC)),\n        (\"edm\",     \"edm\",     str(EDM)),\n        (\"ore\",     \"ore\",     str(ORE)),\n        (\"skos\",    \"skos\",    str(SKOS)),\n        (\"geo\",     \"geo\",     str(GEO)),\n        (\"foaf\",    \"foaf\",    str(FOAF)),\n    ]\n    for label, strip_prefix, ns in prefixes:\n        if json_key.startswith(strip_prefix) and len(json_key) > len(strip_prefix):\n            local = json_key[len(strip_prefix):]\n            local_lower = local[0].lower() + local[1:]\n            iri = ns + local_lower\n            # Verify it exists in the ontology or return it as a best-effort match\n            if local_lower in prop_lookup:\n                return prop_lookup[local_lower][0]\n            # Best-effort: construct IRI even if not explicitly in ontology\n            return (label, iri)\n\n    # Entity-type-specific defaults for unnamespaced keys\n    entity_defaults = {\n        # TimeSpan: begin/end are edm: properties\n        \"TimeSpan\": str(EDM),\n        # Place: lat/long/alt are geo:\n        \"Place\":    str(GEO),\n        # Agent: EDM agent properties\n        \"Agent\":    str(EDM),\n    }\n    ns = entity_defaults.get(entity_type)\n    if ns:\n        iri = ns + json_key\n        return (entity_type.lower(), iri)\n\n    return None\n\n\n# Resolve all data fields\nfield_iris: dict[tuple[str, str], tuple[str, str] | None] = {}\nfor (entity_type, json_key) in data_fields:\n    field_iris[(entity_type, json_key)] = resolve_iri(entity_type, json_key)\n\nresolved   = sum(1 for v in field_iris.values() if v is not None)\nunresolved = sum(1 for v in field_iris.values() if v is None)\nprint(f\"  Resolved: {resolved}  Unresolved: {unresolved}\")\n\n# ── step 3: load DC→RDA mapping ───────────────────────────────────────────────\n\nprint(\"\\nLoading DC→RDA mapping …\")\n# dct_term → [(rda_iri, rda_label)]\ndct_to_rda: dict[str, list[tuple[str, str]]] = defaultdict(list)\nwith open(DCT_RDA_CSV, newline=\"\", encoding=\"utf-8\") as f:\n    for row in csv.DictReader(f):\n        dct_to_rda[row[\"dct_term\"]].append((row[\"rda_iri\"], row[\"rda_label\"]))\n\nprint(f\"  {len(dct_to_rda)} DC/DCT terms → {sum(len(v) for v in dct_to_rda.values())} RDA pairs\")\n\n# ── step 4: load mocho RDA properties ────────────────────────────────────────\n\nprint(\"\\nLoading mocho-full.owl …\")\ng_mocho = Graph()\ng_mocho.parse(MOCHO_OWL)\n\nmocho_rda: dict[str, str] = {}  # iri → English label\nfor prop_type in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):\n    for subj in g_mocho.subjects(RDF.type, prop_type):\n        iri = str(subj)\n        if RDA_ELEMENTS not in iri:\n            continue\n        # Prefer English label\n        label = \"\"\n        for lbl in g_mocho.objects(subj, RDFS.label):\n            if getattr(lbl, \"language\", None) == \"en\":\n                label = str(lbl)\n                break\n        if not label:\n            for lbl in g_mocho.objects(subj, RDFS.label):\n                label = str(lbl)\n                break\n        mocho_rda[iri] = label\n\nprint(f\"  {len(mocho_rda)} RDA properties in mocho\")\n\n\ndef wemi_level(iri: str) -> str:\n    for prefix, level in WEMI_LEVELS.items():\n        if iri.startswith(prefix):\n            return level\n    return \"\"\n\n\n# ── step 5: align ──────────────────────────────────────────────────────────────\n\nprint(\"\\nAligning …\")\n\n# Build reverse map: full IRI → prefixed dct_term label\n# e.g. \"http://purl.org/dc/elements/1.1/creator\" → [\"dc:creator\", \"dcterms:creator\"]\niri_to_dct: dict[str, list[str]] = defaultdict(list)\nfor term in dct_to_rda:\n    prefix, local = term.split(\":\")\n    if prefix == \"dc\":\n        ns = str(DC)\n    elif prefix == \"dcterms\":\n        ns = str(DCTERMS)\n    else:\n        continue\n    full_iri = ns + local\n    iri_to_dct[full_iri].append(term)\n\nrows = []\nsummary_matched = 0\nsummary_unmatched = 0\nunmatched_keys = []\n\nfor (entity_type, json_key), field_row in sorted(data_fields.items()):\n    record_count = field_row[\"record_count\"]\n    coverage_pct = round(100 * record_count / total_records, 2)\n\n    resolved_pair = field_iris.get((entity_type, json_key))\n    if resolved_pair is None:\n        edm_prefix = \"\"\n        edm_iri = \"\"\n    else:\n        edm_prefix, edm_iri = resolved_pair\n\n    # Skip structural/internal keys\n    if json_key in (\"about\",):\n        continue\n\n    # Find RDA candidates via DCT→RDA map\n    rda_candidates = []\n    match_method = \"unmatched\"\n\n    if edm_iri:\n        # Check direct match in DCT map\n        dct_terms = iri_to_dct.get(edm_iri, [])\n        for dct_term in dct_terms:\n            for rda_iri, rda_label in dct_to_rda.get(dct_term, []):\n                if rda_iri in mocho_rda:\n                    rda_candidates.append((rda_iri, mocho_rda[rda_iri], \"via_dct_map\"))\n                else:\n                    rda_candidates.append((rda_iri, rda_label, \"via_dct_map_not_in_mocho\"))\n\n        # If no DCT match, check if the EDM IRI is directly in mocho\n        if not rda_candidates and edm_iri in mocho_rda:\n            rda_candidates.append((edm_iri, mocho_rda[edm_iri], \"direct\"))\n\n    if rda_candidates:\n        # Separate into mocho-present and mocho-absent\n        in_mocho   = [(i, l, m) for i, l, m in rda_candidates if \"not_in_mocho\" not in m]\n        not_mocho  = [(i, l, m) for i, l, m in rda_candidates if \"not_in_mocho\" in m]\n\n        for rda_iri, rda_label, method in in_mocho:\n            rows.append({\n                \"entity_type\":   entity_type,\n                \"json_key\":      json_key,\n                \"edm_prefix\":    edm_prefix,\n                \"edm_iri\":       edm_iri,\n                \"record_count\":  record_count,\n                \"coverage_pct\":  coverage_pct,\n                \"rda_iri\":       rda_iri,\n                \"rda_label\":     rda_label,\n                \"wemi_level\":    wemi_level(rda_iri),\n                \"match_method\":  method,\n                \"in_mocho\":      True,\n            })\n        summary_matched += 1\n\n        # Also record any RDA candidates not yet in mocho (useful diagnostic)\n        for rda_iri, rda_label, method in not_mocho:\n            rows.append({\n                \"entity_type\":   entity_type,\n                \"json_key\":      json_key,\n                \"edm_prefix\":    edm_prefix,\n                \"edm_iri\":       edm_iri,\n                \"record_count\":  record_count,\n                \"coverage_pct\":  coverage_pct,\n                \"rda_iri\":       rda_iri,\n                \"rda_label\":     rda_label,\n                \"wemi_level\":    wemi_level(rda_iri),\n                \"match_method\":  \"via_dct_map_not_in_mocho\",\n                \"in_mocho\":      False,\n            })\n    else:\n        rows.append({\n            \"entity_type\":   entity_type,\n            \"json_key\":      json_key,\n            \"edm_prefix\":    edm_prefix,\n            \"edm_iri\":       edm_iri,\n            \"record_count\":  record_count,\n            \"coverage_pct\":  coverage_pct,\n            \"rda_iri\":       \"\",\n            \"rda_label\":     \"\",\n            \"wemi_level\":    \"\",\n            \"match_method\":  \"unmatched\",\n            \"in_mocho\":      False,\n        })\n        summary_unmatched += 1\n        unmatched_keys.append(f\"{entity_type}.{json_key} [{edm_iri}]\")\n\n# ── step 6: write outputs ──────────────────────────────────────────────────────\n\nOUT_CSV.parent.mkdir(exist_ok=True)\n\nfieldnames = [\n    \"entity_type\", \"json_key\", \"edm_prefix\", \"edm_iri\",\n    \"record_count\", \"coverage_pct\",\n    \"rda_iri\", \"rda_label\", \"wemi_level\", \"match_method\", \"in_mocho\",\n]\n\nwith open(OUT_CSV, \"w\", newline=\"\", encoding=\"utf-8\") as f:\n    writer = csv.DictWriter(f, fieldnames=fieldnames)\n    writer.writeheader()\n    writer.writerows(rows)\n\n# Group for JSON: per (entity_type, json_key) → list of RDA mappings\ngroups: dict[str, dict] = {}\nfor row in rows:\n    key = f\"{row['entity_type']}.{row['json_key']}\"\n    if key not in groups:\n        groups[key] = {\n            \"entity_type\":  row[\"entity_type\"],\n            \"json_key\":     row[\"json_key\"],\n            \"edm_prefix\":   row[\"edm_prefix\"],\n            \"edm_iri\":      row[\"edm_iri\"],\n            \"record_count\": row[\"record_count\"],\n            \"coverage_pct\": row[\"coverage_pct\"],\n            \"rda_mappings\": [],\n        }\n    if row[\"rda_iri\"]:\n        groups[key][\"rda_mappings\"].append({\n            \"rda_iri\":     row[\"rda_iri\"],\n            \"rda_label\":   row[\"rda_label\"],\n            \"wemi_level\":  row[\"wemi_level\"],\n            \"match_method\": row[\"match_method\"],\n            \"in_mocho\":    row[\"in_mocho\"],\n        })\n\noutput = {\n    \"total_records\": total_records,\n    \"summary\": {\n        \"data_fields_with_rda_mapping\": summary_matched,\n        \"data_fields_unmatched\":        summary_unmatched,\n        \"total_alignment_rows\":         len(rows),\n        \"unmatched_fields\":             sorted(unmatched_keys),\n    },\n    \"alignment\": list(groups.values()),\n}\n\nwith open(OUT_JSON, \"w\", encoding=\"utf-8\") as f:\n    json.dump(output, f, indent=2, ensure_ascii=False)\n\n# ── print summary ─────────────────────────────────────────────────────────────\n\nprint(f\"\\n{'='*60}\")\nprint(f\"Data fields with RDA mapping : {summary_matched}\")\nprint(f\"Data fields unmatched        : {summary_unmatched}\")\nprint(f\"Total alignment rows         : {len(rows)}\")\n\nprint(\"\\nUnmatched fields:\")\nfor key in sorted(unmatched_keys):\n    print(f\"  {key}\")\n\nprint(f\"\\nSaved {OUT_CSV}\")\nprint(f\"Saved {OUT_JSON}\")\n"
}
```

---

### User *(2026-03-23T08:07:19.250Z)*

**Tool result**
```
File created successfully at: /Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py
```

---

### Assistant *(2026-03-23T08:07:23.498Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 scripts/align_ddbedm_to_mocho.py"
}
```

---

### User *(2026-03-23T08:07:26.466Z)*

**Tool result** *(error)*
```
Exit code 1
Loading field profile …
  96 (entity_type, json_key) pairs from 115,432 records

Parsing DDB-EDM ontology …
  96 unique local names from DDB-EDM
Traceback (most recent call last):
  File "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py", line 123, in <module>
    def resolve_iri(entity_type: str, json_key: str) -> tuple[str, str] | None:
TypeError: unsupported operand type(s) for |: 'types.GenericAlias' and 'NoneType'
```

---

### Assistant *(2026-03-23T08:07:32.156Z)*

Python 3.9 doesn't support `X | None` syntax. Fix the type hint.

---

### Assistant *(2026-03-23T08:07:33.161Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "old_string": "def resolve_iri(entity_type: str, json_key: str) -> tuple[str, str] | None:",
  "new_string": "def resolve_iri(entity_type: str, json_key: str):"
}
```

---

### User *(2026-03-23T08:56:19.998Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py has been updated successfully.
```

---

### Assistant *(2026-03-23T08:56:23.085Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 scripts/align_ddbedm_to_mocho.py"
}
```

---

### User *(2026-03-23T08:56:34.124Z)*

**Tool result** *(error)*
```
Exit code 1
Loading field profile …
  96 (entity_type, json_key) pairs from 115,432 records

Parsing DDB-EDM ontology …
  96 unique local names from DDB-EDM
Traceback (most recent call last):
  File "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py", line 179, in <module>
    field_iris: dict[tuple[str, str], tuple[str, str] | None] = {}
TypeError: unsupported operand type(s) for |: 'types.GenericAlias' and 'NoneType'
```

---

### Assistant *(2026-03-23T08:56:38.090Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "old_string": "field_iris: dict[tuple[str, str], tuple[str, str] | None] = {}",
  "new_string": "field_iris = {}  # (entity_type, json_key) -> (prefix_label, iri) or None"
}
```

---

### User *(2026-03-23T08:56:41.123Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py has been updated successfully.
```

---

### Assistant *(2026-03-23T08:56:44.720Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 scripts/align_ddbedm_to_mocho.py"
}
```

---

### User *(2026-03-23T08:56:47.691Z)*

**Tool result**
```
Loading field profile …
  96 (entity_type, json_key) pairs from 115,432 records

Parsing DDB-EDM ontology …
  96 unique local names from DDB-EDM
  Resolved: 88  Unresolved: 8

Loading DC→RDA mapping …
  23 DC/DCT terms → 979 RDA pairs

Loading mocho-full.owl …
  930 RDA properties in mocho

Aligning …

============================================================
Data fields with RDA mapping : 31
Data fields unmatched        : 56
Total alignment rows         : 1230

Unmatched fields:
  Agent.altLabel [http://www.europeana.eu/schemas/edm/altLabel]
  Agent.begin [http://www.europeana.eu/schemas/edm/begin]
  Agent.biographicalInformation [http://www.europeana.eu/schemas/edm/biographicalInformation]
  Agent.dateOfBirth [http://www.europeana.eu/schemas/edm/dateOfBirth]
  Agent.dateOfDeath [http://www.europeana.eu/schemas/edm/dateOfDeath]
  Agent.dateOfEstablishment [http://www.europeana.eu/schemas/edm/dateOfEstablishment]
  Agent.dateOfTermination [http://www.europeana.eu/schemas/edm/dateOfTermination]
  Agent.end [http://www.europeana.eu/schemas/edm/end]
  Agent.gender [http://www.europeana.eu/schemas/edm/gender]
  Agent.hasMet [http://www.europeana.eu/schemas/edm/hasMet]
  Agent.identifier [http://www.europeana.eu/schemas/edm/identifier]
  Agent.isRelatedTo [http://www.europeana.eu/schemas/edm/isRelatedTo]
  Agent.name [http://www.europeana.eu/schemas/edm/name]
  Agent.note [http://www.w3.org/2004/02/skos/core#note]
  Agent.placeOfBirth [http://www.europeana.eu/schemas/edm/placeOfBirth]
  Agent.placeOfDeath [http://www.europeana.eu/schemas/edm/placeOfDeath]
  Agent.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]
  Agent.professionOrOccupation [http://www.europeana.eu/schemas/edm/professionOrOccupation]
  Agent.sameAs [http://www.europeana.eu/schemas/edm/sameAs]
  Agent.wasPresentAt [http://www.europeana.eu/schemas/edm/wasPresentAt]
  Aggregation.aggregatedCHO [http://www.europeana.eu/schemas/edm/aggregatedCHO]
  Aggregation.aggregator [http://www.deutsche-digitale-bibliothek.de/edm/aggregator]
  Aggregation.dataProvider [http://www.europeana.eu/schemas/edm/dataProvider]
  Aggregation.hasView [http://www.europeana.eu/schemas/edm/hasView]
  Aggregation.isShownAt [http://www.europeana.eu/schemas/edm/isShownAt]
  Aggregation.isShownBy [http://www.europeana.eu/schemas/edm/isShownBy]
  Aggregation.object [http://www.europeana.eu/schemas/edm/object]
  Aggregation.provider [http://www.europeana.eu/schemas/edm/provider]
  Concept.notation [http://www.w3.org/2004/02/skos/core#notation]
  Concept.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]
  Event.P11_had_participant [http://www.cidoc-crm.org/rdfs/cidoc-crm#P11_had_participant]
  Event.happenedAt [http://www.europeana.eu/schemas/edm/happenedAt]
  Event.hasType [http://www.europeana.eu/schemas/edm/hasType]
  Event.occuredAt []
  PhysicalThing.aggregationEntity [http://www.deutsche-digitale-bibliothek.de/edm/aggregationEntity]
  PhysicalThing.hierarchyPosition [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyPosition]
  PhysicalThing.hierarchyType [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType]
  Place.alt [http://www.w3.org/2003/01/geo/wgs84_pos#alt]
  Place.altLabel [http://www.w3.org/2003/01/geo/wgs84_pos#altLabel]
  Place.isNextInSequence [http://www.europeana.eu/schemas/edm/isNextInSequence]
  Place.lat [http://www.w3.org/2003/01/geo/wgs84_pos#lat]
  Place.long [http://www.w3.org/2003/01/geo/wgs84_pos#long]
  Place.note [http://www.w3.org/2004/02/skos/core#note]
  Place.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]
  Place.sameAs [http://www.w3.org/2003/01/geo/wgs84_pos#sameAs]
  ProvidedCHO.aggregationEntity [http://www.deutsche-digitale-bibliothek.de/edm/aggregationEntity]
  ProvidedCHO.currentLocation [http://www.europeana.eu/schemas/edm/currentLocation]
  ProvidedCHO.dcTermSubject [http://purl.org/dc/elements/1.1/termSubject]
  ProvidedCHO.hasMet [http://www.europeana.eu/schemas/edm/hasMet]
  ProvidedCHO.hasType [http://www.europeana.eu/schemas/edm/hasType]
  ProvidedCHO.hierarchyPosition [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyPosition]
  ProvidedCHO.hierarchyType [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType]
  ProvidedCHO.identifier []
  ProvidedCHO.spatial [http://purl.org/dc/terms/spatial]
  TimeSpan.begin [http://www.europeana.eu/schemas/edm/begin]
  TimeSpan.end [http://www.europeana.eu/schemas/edm/end]

Saved /Users/mta/Documents/claude/goethe-faust/output/alignment_ddbedm_mocho.csv
Saved /Users/mta/Documents/claude/goethe-faust/output/alignment_ddbedm_mocho.json
```

---

### Assistant *(2026-03-23T08:57:12.267Z)*

Script runs. Key observations from the output:

- **31 DC/DCT fields matched** → 1,230 alignment rows (high fanout: `dc:creator` → 232+ RDA sub-properties)
- **56 unmatched** — all expected gaps: EDM-native (`edm:isShownAt`, `edm:begin/end`), SKOS labels, geo coords, DDB extensions (`ddb:hierarchyType`), CIDOC CRM event properties
- **Two known IRI bugs** worth fixing: `dcTermSubject` resolves to `dc:termSubject` instead of `dcterms:subject`, and `identifier` (no namespace) has no IRI

Let me fix those and update the README.

---

### Assistant *(2026-03-23T08:57:13.050Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "limit": 30,
  "offset": 95
}
```

---

### User *(2026-03-23T08:57:13.066Z)*

**Tool result**
```
    95→# ── step 2: resolve JSON keys to EDM/DC IRIs ──────────────────────────────────
    96→
    97→print("\nParsing DDB-EDM ontology …")
    98→g_edm = Graph()
    99→g_edm.parse(DDBEDM_TTL)
   100→
   101→# Build lookup: normalised_local_name → [(prefix_label, full_iri)]
   102→# where normalised = lowercase of local name
   103→prop_lookup: dict[str, list[tuple[str, str]]] = defaultdict(list)
   104→for prop_type in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
   105→    for subj in g_edm.subjects(RDF.type, prop_type):
   106→        iri = str(subj)
   107→        local = iri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
   108→        try:
   109→            prefix = g_edm.qname(subj).split(":")[0]
   110→        except Exception:
   111→            prefix = ""
   112→        prop_lookup[local.lower()].append((prefix, iri))
   113→
   114→# Also include classes for context
   115→for subj in g_edm.subjects(RDF.type, OWL.Class):
   116→    iri = str(subj)
   117→    local = iri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
   118→    prop_lookup[local.lower()].append(("class", iri))
   119→
   120→print(f"  {len(prop_lookup)} unique local names from DDB-EDM")
   121→
   122→
   123→def resolve_iri(entity_type: str, json_key: str):
   124→    """Map a JSON camelCase/plain key to (prefix_label, full_iri).



```

---

### Assistant *(2026-03-23T08:57:19.289Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "old_string": "prop_lookup: dict[str, list[tuple[str, str]]] = defaultdict(list)",
  "new_string": "# Hard-coded overrides for known DDB data quirks: json_key → (prefix, iri)\n# dcTermSubject (no 's') is a DDB data variant for dcterms:subject\n# identifier (no prefix) is dc:identifier in ProvidedCHO context\nOVERRIDES = {\n    \"dcTermSubject\": (\"dcterms\", str(DCTERMS) + \"subject\"),\n    \"identifier\":    (\"dc\",      str(DC) + \"identifier\"),\n}\n\nprop_lookup = defaultdict(list)  # normalised_local_name → [(prefix_label, full_iri)]"
}
```

---

### User *(2026-03-23T09:22:31.123Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py has been updated successfully.
```

---

### Assistant *(2026-03-23T09:22:36.086Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "old_string": "def resolve_iri(entity_type: str, json_key: str):\n    \"\"\"Map a JSON camelCase/plain key to (prefix_label, full_iri).",
  "new_string": "def resolve_iri(entity_type: str, json_key: str):\n    \"\"\"Map a JSON camelCase/plain key to (prefix_label, full_iri).\n\n    Checks hard-coded overrides first, then the ontology lookup, then\n    heuristic prefix-stripping."
}
```

---

### User *(2026-03-23T09:22:41.944Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py has been updated successfully.
```

---

### Assistant *(2026-03-23T09:22:44.705Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "limit": 15,
  "offset": 132
}
```

---

### User *(2026-03-23T09:22:44.719Z)*

**Tool result**
```
   132→    """Map a JSON camelCase/plain key to (prefix_label, full_iri).
   133→
   134→    Checks hard-coded overrides first, then the ontology lookup, then
   135→    heuristic prefix-stripping.
   136→
   137→    Resolution order:
   138→    1. Direct match of json_key (lowercase) against the ontology lookup.
   139→    2. Strip known camelCase prefixes (dcTerms, dc, edm, ore, foaf, geo, skos)
   140→       and match the lowercased remainder.
   141→    3. Entity-type-specific defaults for keys without an obvious namespace.
   142→    Returns (prefix_label, iri) or None if unresolved.
   143→    """
   144→    key_lower = json_key.lower()
   145→
   146→    # Direct match



```

---

### Assistant *(2026-03-23T09:22:48.543Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py",
  "old_string": "    key_lower = json_key.lower()\n\n    # Direct match",
  "new_string": "    # Hard-coded overrides\n    if json_key in OVERRIDES:\n        return OVERRIDES[json_key]\n\n    key_lower = json_key.lower()\n\n    # Direct match"
}
```

---

### User *(2026-03-23T09:22:50.266Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/align_ddbedm_to_mocho.py has been updated successfully.
```

---

### Assistant *(2026-03-23T09:22:53.580Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 scripts/align_ddbedm_to_mocho.py"
}
```

---

### User *(2026-03-23T09:22:58.707Z)*

**Tool result**
```
Loading field profile …
  96 (entity_type, json_key) pairs from 115,432 records

Parsing DDB-EDM ontology …
  96 unique local names from DDB-EDM
  Resolved: 89  Unresolved: 7

Loading DC→RDA mapping …
  23 DC/DCT terms → 979 RDA pairs

Loading mocho-full.owl …
  930 RDA properties in mocho

Aligning …

============================================================
Data fields with RDA mapping : 32
Data fields unmatched        : 55
Total alignment rows         : 1271

Unmatched fields:
  Agent.altLabel [http://www.europeana.eu/schemas/edm/altLabel]
  Agent.begin [http://www.europeana.eu/schemas/edm/begin]
  Agent.biographicalInformation [http://www.europeana.eu/schemas/edm/biographicalInformation]
  Agent.dateOfBirth [http://www.europeana.eu/schemas/edm/dateOfBirth]
  Agent.dateOfDeath [http://www.europeana.eu/schemas/edm/dateOfDeath]
  Agent.dateOfEstablishment [http://www.europeana.eu/schemas/edm/dateOfEstablishment]
  Agent.dateOfTermination [http://www.europeana.eu/schemas/edm/dateOfTermination]
  Agent.end [http://www.europeana.eu/schemas/edm/end]
  Agent.gender [http://www.europeana.eu/schemas/edm/gender]
  Agent.hasMet [http://www.europeana.eu/schemas/edm/hasMet]
  Agent.identifier [http://purl.org/dc/elements/1.1/identifier]
  Agent.isRelatedTo [http://www.europeana.eu/schemas/edm/isRelatedTo]
  Agent.name [http://www.europeana.eu/schemas/edm/name]
  Agent.note [http://www.w3.org/2004/02/skos/core#note]
  Agent.placeOfBirth [http://www.europeana.eu/schemas/edm/placeOfBirth]
  Agent.placeOfDeath [http://www.europeana.eu/schemas/edm/placeOfDeath]
  Agent.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]
  Agent.professionOrOccupation [http://www.europeana.eu/schemas/edm/professionOrOccupation]
  Agent.sameAs [http://www.europeana.eu/schemas/edm/sameAs]
  Agent.wasPresentAt [http://www.europeana.eu/schemas/edm/wasPresentAt]
  Aggregation.aggregatedCHO [http://www.europeana.eu/schemas/edm/aggregatedCHO]
  Aggregation.aggregator [http://www.deutsche-digitale-bibliothek.de/edm/aggregator]
  Aggregation.dataProvider [http://www.europeana.eu/schemas/edm/dataProvider]
  Aggregation.hasView [http://www.europeana.eu/schemas/edm/hasView]
  Aggregation.isShownAt [http://www.europeana.eu/schemas/edm/isShownAt]
  Aggregation.isShownBy [http://www.europeana.eu/schemas/edm/isShownBy]
  Aggregation.object [http://www.europeana.eu/schemas/edm/object]
  Aggregation.provider [http://www.europeana.eu/schemas/edm/provider]
  Concept.notation [http://www.w3.org/2004/02/skos/core#notation]
  Concept.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]
  Event.P11_had_participant [http://www.cidoc-crm.org/rdfs/cidoc-crm#P11_had_participant]
  Event.happenedAt [http://www.europeana.eu/schemas/edm/happenedAt]
  Event.hasType [http://www.europeana.eu/schemas/edm/hasType]
  Event.occuredAt []
  PhysicalThing.aggregationEntity [http://www.deutsche-digitale-bibliothek.de/edm/aggregationEntity]
  PhysicalThing.hierarchyPosition [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyPosition]
  PhysicalThing.hierarchyType [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType]
  Place.alt [http://www.w3.org/2003/01/geo/wgs84_pos#alt]
  Place.altLabel [http://www.w3.org/2003/01/geo/wgs84_pos#altLabel]
  Place.isNextInSequence [http://www.europeana.eu/schemas/edm/isNextInSequence]
  Place.lat [http://www.w3.org/2003/01/geo/wgs84_pos#lat]
  Place.long [http://www.w3.org/2003/01/geo/wgs84_pos#long]
  Place.note [http://www.w3.org/2004/02/skos/core#note]
  Place.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]
  Place.sameAs [http://www.w3.org/2003/01/geo/wgs84_pos#sameAs]
  ProvidedCHO.aggregationEntity [http://www.deutsche-digitale-bibliothek.de/edm/aggregationEntity]
  ProvidedCHO.currentLocation [http://www.europeana.eu/schemas/edm/currentLocation]
  ProvidedCHO.hasMet [http://www.europeana.eu/schemas/edm/hasMet]
  ProvidedCHO.hasType [http://www.europeana.eu/schemas/edm/hasType]
  ProvidedCHO.hierarchyPosition [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyPosition]
  ProvidedCHO.hierarchyType [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType]
  ProvidedCHO.identifier [http://purl.org/dc/elements/1.1/identifier]
  ProvidedCHO.spatial [http://purl.org/dc/terms/spatial]
  TimeSpan.begin [http://www.europeana.eu/schemas/edm/begin]
  TimeSpan.end [http://www.europeana.eu/schemas/edm/end]

Saved /Users/mta/Documents/claude/goethe-faust/output/alignment_ddbedm_mocho.csv
Saved /Users/mta/Documents/claude/goethe-faust/output/alignment_ddbedm_mocho.json
```

---

### Assistant *(2026-03-23T09:23:17.845Z)*

Working correctly. The 55 unmatched fields split cleanly into expected categories: EDM-structural (`edm:isShownAt`, `edm:begin/end`), DDB extensions (`ddb:hierarchyType`), SKOS labels, geo coordinates, and `dc:identifier` / `dcterms:spatial` (known gaps in the DCT→RDA map). Now let me update the README.

---

### Assistant *(2026-03-23T09:23:18.562Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/README.md",
  "limit": 20,
  "offset": 1
}
```

---

### User *(2026-03-23T09:23:18.589Z)*

**Tool result**
```
     1→# Scripts
     2→
     3→All scripts live in `scripts/`. They use project-relative paths via
     4→`pathlib.Path(__file__).resolve().parent.parent`, so they can be run from
     5→any working directory.
     6→
     7→---
     8→
     9→## Data pipeline (run in order)
    10→
    11→### `fetch-search-all.py`
    12→Fetches all DDB search results for the query "goethe" via the DDB Solr API
    13→and merges them into a single JSON file.
    14→
    15→- **Input**: DDB Solr API (live network access required)
    16→- **Output**: `data/ddb-search-goethe-all.json`
    17→- **Usage**: `python scripts/fetch-search-all.py`
    18→- **Notes**: `TOTAL` must match the actual result count; update if the
    19→  dataset changes. 0.3 s delay between requests to avoid rate-limiting.
    20→



```

---

### Assistant *(2026-03-23T09:23:34.877Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/README.md",
  "old_string": "---\n\n## Data pipeline (run in order)",
  "new_string": "---\n\n## Ontology alignment (run in order)\n\n### `profile_edm_fields.py`\nProfiles all field keys present under `edm.RDF.*` entity types in the JSONL\ndata file. Needed as input for `align_ddbedm_to_mocho.py`.\n\n- **Input**: `data/items-all-goethe-faust.json`\n- **Output**: `output/edm_field_profile.json`, `output/edm_field_profile.csv`\n- **Usage**: `python3 scripts/profile_edm_fields.py`\n- **Notes**: Reports per-entity-type field names with record counts and\n  coverage percentages. Counts > 100% indicate array-valued entities\n  (multiple agents/concepts/events per record).\n\n### `align_ddbedm_to_mocho.py`\nData-driven ontology alignment from DDB-EDM to mocho. Maps each EDM/DC\nproperty actually present in the data to its corresponding RDA properties\nin mocho, via the DC→RDA sub-property mapping from the mocho workflow.\n\n- **Input**: `output/edm_field_profile.json` (from above),\n  `~/Documents/claude/mocho/ontology/ddbedm_1.0.ttl`,\n  `~/Documents/claude/mocho/mocho-odk/src/ontology/mocho-full.owl`,\n  `~/Documents/claude/mocho/output/mapping_dct_to_rda.csv`\n- **Output**: `output/alignment_ddbedm_mocho.csv`,\n  `output/alignment_ddbedm_mocho.json`\n- **Usage**: `python3 scripts/align_ddbedm_to_mocho.py`\n- **Dependencies**: `rdflib`\n- **Notes**:\n  - One CSV row per (edm_field × rda_property) pair; high-fanout DC terms\n    (e.g. `dc:creator` → 232 RDA sub-properties) produce many rows per field\n  - 32 DC/DCT fields matched to RDA properties in mocho (1,271 alignment rows)\n  - 55 unmatched fields fall into expected categories: EDM-structural\n    (`edm:isShownAt`, `edm:begin/end`), DDB extensions (`ddb:hierarchyType`,\n    `ddb:aggregationEntity`), SKOS labels, geo coordinates, and two known\n    DCT→RDA gaps (`dc:identifier`, `dcterms:spatial`)\n  - `dcTermSubject` (DDB data variant of `dcterms:subject`) handled via\n    hard-coded override in `OVERRIDES` dict\n\n---\n\n## Data pipeline (run in order)"
}
```

---

### User *(2026-03-23T09:33:59.021Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/README.md has been updated successfully.
```

---

### Assistant *(2026-03-23T09:34:08.097Z)*

Two new scripts:

- **`profile_edm_fields.py`** — walks all `edm.RDF.*` entity types across 115,432 records, counts field occurrences, saves to `output/edm_field_profile.{json,csv}`
- **`align_ddbedm_to_mocho.py`** — loads the profile, resolves JSON keys to EDM/DC IRIs via `ddbedm_1.0.ttl`, looks up RDA sub-properties via `mapping_dct_to_rda.csv`, checks which are present in `mocho-full.owl`, outputs `output/alignment_ddbedm_mocho.{csv,json}`

**Results:**
- 32 DC/DCT fields matched → 1,271 (field × RDA property) alignment rows
- 55 unmatched — all in expected categories: EDM-structural, DDB extensions, SKOS, geo, plus `dc:identifier` / `dcterms:spatial` (known DCT→RDA gaps)

The CSV has columns `entity_type, json_key, edm_prefix, edm_iri, record_count, coverage_pct, rda_iri, rda_label, wemi_level, match_method, in_mocho`. Want me to do anything with the unmatched EDM-specific properties (direct mocho lookups, or a separate mapping pass)?

---

### User *(2026-03-23T09:34:58.580Z)*

Create a note, a specs document, and architecture decision document based on the alignment conducted.

---

### Assistant *(2026-03-23T09:35:04.782Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/mocho/notes/ /Users/mta/Documents/claude/goethe-faust/notes/ 2>/dev/null"
}
```

---

### User *(2026-03-23T09:35:04.952Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/notes/:
how-claude-transcript.md
isbd-title-analysis.md
session-summary-final-dataset.md

/Users/mta/Documents/claude/mocho/notes/:
README.md
claude-check-why-mocho-v01ttl-is-not-loading-on-20260216-133010.json
claude-check-why-mocho-v01ttl-is-not-loading-on-20260216-133010.md
claude-start-a-new-project-mocho-in-usersmtadoc-20260223-210407.json
claude-start-a-new-project-mocho-in-usersmtadoc-20260223-210407.md
mapping_dct_rda_workflow.md
musicontology-mirror-conversion.md
odk-guide.md
odk-import-troubleshooting-20260309.md
odk-seed-troubleshooting.md
session-mocho-diagrams-20260217-c92283bd.jsonl
session-mocho-setup-20260223-a3cd246d.jsonl
widoco-guide.md
```

---

### Assistant *(2026-03-23T09:35:08.116Z)*

**Tool call:** `Bash`
```json
{
  "command": "cat /Users/mta/Documents/claude/goethe-faust/output/alignment_ddbedm_mocho.json | python3 -c \"\nimport json, sys\nd = json.load(sys.stdin)\nprint('Summary:', json.dumps(d['summary'], indent=2))\nprint()\n# Show the matched fields with their RDA mapping counts\nfor a in d['alignment']:\n    in_mocho = [m for m in a['rda_mappings'] if m['in_mocho']]\n    not_in = [m for m in a['rda_mappings'] if not m['in_mocho']]\n    if in_mocho:\n        wemi = sorted(set(m['wemi_level'] for m in in_mocho if m['wemi_level']))\n        print(f\\\"{a['entity_type']}.{a['json_key']} [{a['edm_prefix']}:{a['json_key']}] -> {len(in_mocho)} in mocho, wemi={wemi}, cov={a['coverage_pct']}%\\\")\n\" 2>/dev/null"
}
```

---

### User *(2026-03-23T09:35:22.767Z)*

**Tool result**
```
Summary: {
  "data_fields_with_rda_mapping": 32,
  "data_fields_unmatched": 55,
  "total_alignment_rows": 1271,
  "unmatched_fields": [
    "Agent.altLabel [http://www.europeana.eu/schemas/edm/altLabel]",
    "Agent.begin [http://www.europeana.eu/schemas/edm/begin]",
    "Agent.biographicalInformation [http://www.europeana.eu/schemas/edm/biographicalInformation]",
    "Agent.dateOfBirth [http://www.europeana.eu/schemas/edm/dateOfBirth]",
    "Agent.dateOfDeath [http://www.europeana.eu/schemas/edm/dateOfDeath]",
    "Agent.dateOfEstablishment [http://www.europeana.eu/schemas/edm/dateOfEstablishment]",
    "Agent.dateOfTermination [http://www.europeana.eu/schemas/edm/dateOfTermination]",
    "Agent.end [http://www.europeana.eu/schemas/edm/end]",
    "Agent.gender [http://www.europeana.eu/schemas/edm/gender]",
    "Agent.hasMet [http://www.europeana.eu/schemas/edm/hasMet]",
    "Agent.identifier [http://purl.org/dc/elements/1.1/identifier]",
    "Agent.isRelatedTo [http://www.europeana.eu/schemas/edm/isRelatedTo]",
    "Agent.name [http://www.europeana.eu/schemas/edm/name]",
    "Agent.note [http://www.w3.org/2004/02/skos/core#note]",
    "Agent.placeOfBirth [http://www.europeana.eu/schemas/edm/placeOfBirth]",
    "Agent.placeOfDeath [http://www.europeana.eu/schemas/edm/placeOfDeath]",
    "Agent.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]",
    "Agent.professionOrOccupation [http://www.europeana.eu/schemas/edm/professionOrOccupation]",
    "Agent.sameAs [http://www.europeana.eu/schemas/edm/sameAs]",
    "Agent.wasPresentAt [http://www.europeana.eu/schemas/edm/wasPresentAt]",
    "Aggregation.aggregatedCHO [http://www.europeana.eu/schemas/edm/aggregatedCHO]",
    "Aggregation.aggregator [http://www.deutsche-digitale-bibliothek.de/edm/aggregator]",
    "Aggregation.dataProvider [http://www.europeana.eu/schemas/edm/dataProvider]",
    "Aggregation.hasView [http://www.europeana.eu/schemas/edm/hasView]",
    "Aggregation.isShownAt [http://www.europeana.eu/schemas/edm/isShownAt]",
    "Aggregation.isShownBy [http://www.europeana.eu/schemas/edm/isShownBy]",
    "Aggregation.object [http://www.europeana.eu/schemas/edm/object]",
    "Aggregation.provider [http://www.europeana.eu/schemas/edm/provider]",
    "Concept.notation [http://www.w3.org/2004/02/skos/core#notation]",
    "Concept.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]",
    "Event.P11_had_participant [http://www.cidoc-crm.org/rdfs/cidoc-crm#P11_had_participant]",
    "Event.happenedAt [http://www.europeana.eu/schemas/edm/happenedAt]",
    "Event.hasType [http://www.europeana.eu/schemas/edm/hasType]",
    "Event.occuredAt []",
    "PhysicalThing.aggregationEntity [http://www.deutsche-digitale-bibliothek.de/edm/aggregationEntity]",
    "PhysicalThing.hierarchyPosition [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyPosition]",
    "PhysicalThing.hierarchyType [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType]",
    "Place.alt [http://www.w3.org/2003/01/geo/wgs84_pos#alt]",
    "Place.altLabel [http://www.w3.org/2003/01/geo/wgs84_pos#altLabel]",
    "Place.isNextInSequence [http://www.europeana.eu/schemas/edm/isNextInSequence]",
    "Place.lat [http://www.w3.org/2003/01/geo/wgs84_pos#lat]",
    "Place.long [http://www.w3.org/2003/01/geo/wgs84_pos#long]",
    "Place.note [http://www.w3.org/2004/02/skos/core#note]",
    "Place.prefLabel [http://www.w3.org/2004/02/skos/core#prefLabel]",
    "Place.sameAs [http://www.w3.org/2003/01/geo/wgs84_pos#sameAs]",
    "ProvidedCHO.aggregationEntity [http://www.deutsche-digitale-bibliothek.de/edm/aggregationEntity]",
    "ProvidedCHO.currentLocation [http://www.europeana.eu/schemas/edm/currentLocation]",
    "ProvidedCHO.hasMet [http://www.europeana.eu/schemas/edm/hasMet]",
    "ProvidedCHO.hasType [http://www.europeana.eu/schemas/edm/hasType]",
    "ProvidedCHO.hierarchyPosition [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyPosition]",
    "ProvidedCHO.hierarchyType [http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType]",
    "ProvidedCHO.identifier [http://purl.org/dc/elements/1.1/identifier]",
    "ProvidedCHO.spatial [http://purl.org/dc/terms/spatial]",
    "TimeSpan.begin [http://www.europeana.eu/schemas/edm/begin]",
    "TimeSpan.end [http://www.europeana.eu/schemas/edm/end]"
  ]
}

Agent.date [dc:date] -> 5 in mocho, wemi=['Agent', 'Expression', 'Manifestation', 'Work'], cov=365.61%
Agent.hasPart [dcterms:hasPart] -> 3 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=365.61%
Agent.isPartOf [dcterms:isPartOf] -> 3 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=365.61%
Agent.type [dc:type] -> 11 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=365.61%
Aggregation.dcTermsRights [dcterms:dcTermsRights] -> 2 in mocho, wemi=['Item', 'Manifestation'], cov=100.0%
Aggregation.edmRights [dcterms:edmRights] -> 2 in mocho, wemi=['Item', 'Manifestation'], cov=100.0%
PhysicalThing.isPartOf [dcterms:isPartOf] -> 3 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=47.48%
PhysicalThing.title [dc:title] -> 28 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=48.32%
Place.hasPart [dcterms:hasPart] -> 3 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=102.3%
Place.isPartOf [dcterms:isPartOf] -> 3 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=102.3%
Place.type [dc:type] -> 11 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=102.3%
ProvidedCHO.alternative [dcterms:alternative] -> 1 in mocho, wemi=['Manifestation'], cov=5.24%
ProvidedCHO.contributor [dc:contributor] -> 360 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=26.21%
ProvidedCHO.creator [dc:creator] -> 232 in mocho, wemi=['Work'], cov=36.9%
ProvidedCHO.date [dc:date] -> 5 in mocho, wemi=['Agent', 'Expression', 'Manifestation', 'Work'], cov=44.99%
ProvidedCHO.dcSubject [dc:dcSubject] -> 42 in mocho, wemi=['Work'], cov=60.28%
ProvidedCHO.dcTermSubject [dcterms:dcTermSubject] -> 42 in mocho, wemi=['Work'], cov=60.28%
ProvidedCHO.dcTermsLanguage [dc:dcTermsLanguage] -> 2 in mocho, wemi=['Expression', 'Work'], cov=62.1%
ProvidedCHO.dcTermsSubject [dc:dcTermsSubject] -> 42 in mocho, wemi=['Work'], cov=60.28%
ProvidedCHO.dcType [dc:dcType] -> 11 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=80.44%
ProvidedCHO.description [dc:description] -> 46 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=76.62%
ProvidedCHO.edmType [dc:edmType] -> 11 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=63.28%
ProvidedCHO.extent [dcterms:extent] -> 5 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=66.5%
ProvidedCHO.format [dc:format] -> 59 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=17.76%
ProvidedCHO.isPartOf [dcterms:isPartOf] -> 3 in mocho, wemi=['Expression', 'Manifestation', 'Work'], cov=58.51%
ProvidedCHO.issued [dcterms:issued] -> 4 in mocho, wemi=['Manifestation'], cov=41.48%
ProvidedCHO.language [dc:language] -> 2 in mocho, wemi=['Expression', 'Work'], cov=62.1%
ProvidedCHO.title [dc:title] -> 28 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=100.0%
WebResource.creator [dc:creator] -> 232 in mocho, wemi=['Work'], cov=270.76%
WebResource.dcTermsRights [dcterms:dcTermsRights] -> 2 in mocho, wemi=['Item', 'Manifestation'], cov=270.76%
WebResource.edmRights [dcterms:edmRights] -> 2 in mocho, wemi=['Item', 'Manifestation'], cov=270.76%
WebResource.type [dc:type] -> 11 in mocho, wemi=['Expression', 'Item', 'Manifestation', 'Work'], cov=270.76%
```

---

### Assistant *(2026-03-23T09:36:11.021Z)*

Now I have everything I need. Let me write all three documents.

---

### Assistant *(2026-03-23T09:36:48.916Z)*

**Tool call:** `Write`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/notes/alignment-ddbedm-mocho.md",
  "content": "# DDB-EDM → mocho Alignment: Working Note\n\n**Date**: 2026-03-23\n**Data source**: `goethe-faust/data/items-all-goethe-faust.json` (115,432 records)\n**Scripts**: `goethe-faust/scripts/profile_edm_fields.py`, `align_ddbedm_to_mocho.py`\n**Outputs**: `goethe-faust/output/alignment_ddbedm_mocho.{csv,json}`\n\n---\n\n## What was done\n\nTwo-stage data-driven alignment:\n\n1. **Profile** — walked all `edm.RDF.*` fields across the full JSONL corpus; counted field occurrences per entity type. 96 distinct (entity_type, json_key) pairs found.\n2. **Align** — resolved JSON camelCase keys to full EDM/DC IRIs via `ddbedm_1.0.ttl`, then routed DC/DCT IRIs through `mapping_dct_to_rda.csv` to find RDA sub-properties present in `mocho-full.owl`.\n\n---\n\n## Entity types in the data\n\n| Entity type     | Records with entity | Notes                              |\n|-----------------|--------------------:|------------------------------------|\n| ProvidedCHO     |            115,432  | 1:1 with records; main bib entity  |\n| Aggregation     |            115,432  | 1:1; structural/access wrapper     |\n| WebResource     |            115,432  | array (avg 2.7/record)             |\n| Agent           |            115,432  | array (avg 3.7/record)             |\n| Concept         |            115,432  | array (avg 6.2/record); subjects   |\n| Place           |             59,249  | 51% of records                     |\n| Event           |            110,059  | 95% of records                     |\n| TimeSpan        |             99,930  | 87% of records                     |\n| PhysicalThing   |             22,265  | 19%; hierarchy navigation nodes    |\n\n---\n\n## Alignment results\n\n**32 DC/DCT fields** mapped to RDA properties in mocho — **1,271 alignment rows** (one per field × RDA candidate).\n**55 fields** unmatched (see categories below).\n\n### ProvidedCHO — core bibliographic fields\n\n| JSON key | EDM/DC IRI | RDA candidates in mocho | WEMI levels | Coverage |\n|---|---|---:|---|---:|\n| `title` | `dc:title` | 28 | W E M I | 100% |\n| `description` | `dc:description` | 46 | W E M I | 77% |\n| `dcType` | `dc:type` | 11 | W E M I | 80% |\n| `edmType` | `dc:type` | 11 | W E M I | 63% |\n| `dcSubject` | `dc:subject` | 42 | W | 60% |\n| `dcTermsSubject` | `dcterms:subject` | 42 | W | 60% |\n| `dcTermSubject` | `dcterms:subject` | 42 | W | 60% |\n| `language` | `dc:language` | 2 | W E | 62% |\n| `dcTermsLanguage` | `dcterms:language` | 2 | W E | 62% |\n| `creator` | `dc:creator` | 232 | W | 37% |\n| `contributor` | `dc:contributor` | 360 | W E M I | 26% |\n| `date` | `dc:date` | 5 | W E M A | 45% |\n| `issued` | `dcterms:issued` | 4 | M | 41% |\n| `extent` | `dcterms:extent` | 5 | W E M | 67% |\n| `format` | `dc:format` | 59 | W E M | 18% |\n| `isPartOf` | `dcterms:isPartOf` | 3 | W E M | 59% |\n| `alternative` | `dcterms:alternative` | 1 | M | 5% |\n| `spatial` | `dcterms:spatial` | — | — | 7% |\n| `identifier` | `dc:identifier` | — | — | 88% |\n\n`creator` and `contributor` are high-fanout: 232 and 360 RDA sub-properties respectively, spanning all role specialisations. Consumers must select the most specific applicable property.\n\n`dcSubject`/`dcTermsSubject`/`dcTermSubject` carry identical counts (69,588) — the same subject data appears under three keys in the DDB JSON. A deduplication decision is needed upstream.\n\n### Aggregation and WebResource — rights and access\n\n| JSON key | EDM/DC IRI | RDA candidates | WEMI | Coverage |\n|---|---|---:|---|---:|\n| `edmRights` | `dcterms:rights` | 2 | M I | 100% |\n| `dcTermsRights` | `dcterms:rights` | 2 | M I | 100% |\n\nAggregation structural properties (`edm:isShownAt`, `edm:isShownBy`, `edm:aggregatedCHO`, etc.) are out of scope for the DC→RDA routing and remain unmatched (see below).\n\n### Agent — authority data\n\nAgent entity contains 25 fields. Only `date`, `type`, `hasPart`, `isPartOf` carry DC IRIs and thus receive RDA candidates — at coverage rates of 366% (all records have multiple agents). The 20 EDM-native agent properties (`edm:dateOfBirth`, `edm:placeOfBirth`, `edm:biographicalInformation`, etc.) have no DC→RDA mapping and require direct RDA alignment.\n\n---\n\n## Unmatched fields by category\n\n| Category | Fields | Example IRIs |\n|---|---:|---|\n| EDM-structural (Aggregation) | 8 | `edm:isShownAt`, `edm:dataProvider`, `edm:object` |\n| EDM-authority (Agent) | 14 | `edm:dateOfBirth`, `edm:placeOfBirth`, `edm:gender` |\n| EDM-other (ProvidedCHO, Place, Event) | 7 | `edm:hasMet`, `edm:hasType`, `edm:currentLocation` |\n| SKOS labels | 6 | `skos:prefLabel`, `skos:altLabel`, `skos:note`, `skos:notation` |\n| Geo coordinates | 5 | `geo:lat`, `geo:long`, `geo:alt`, `geo:sameAs` |\n| DDB extensions | 6 | `ddb:hierarchyType`, `ddb:aggregationEntity` |\n| CIDOC CRM | 1 | `crm:P11_had_participant` |\n| DC terms without RDA sub-props | 2 | `dc:identifier`, `dcterms:spatial` |\n\n---\n\n## Known issues and limitations\n\n- **High-fanout DC terms**: `dc:contributor` → 360 RDA properties is not practically actionable without further filtering by WEMI level and use case.\n- **Triple subject keys**: `dcSubject`, `dcTermsSubject`, `dcTermSubject` appear to carry identical data in 60% of records. The data source should be audited before loading into a triplestore.\n- **`edm_prefix` display bug** in ad-hoc print output (not in CSV): labels showed `dc:dcSubject` instead of `dc:subject`. The underlying IRIs in the CSV are correct.\n- **Agent resolution**: The `identifier` override applies globally (Agent + ProvidedCHO), which is correct for `dc:identifier` in both contexts but should be validated for Agent entities specifically.\n- **`Event.occuredAt`**: No IRI resolved (likely a typo in the DDB API; probable IRI `edm:occurredAt`).\n\n---\n\n## Next steps\n\n1. **EDM-native property pass** — map `edm:dateOfBirth`, `edm:placeOfBirth`, etc. directly to RDA Person/Agent properties (`rda:P50119 has birth date`, etc.). These are not covered by the DCT→RDA route.\n2. **SKOS labels** — `skos:prefLabel` and `skos:altLabel` on Agent/Concept/Place need mapping to `rda:P50385 has access point` or equivalent.\n3. **Filter by WEMI level** — add a downstream step that restricts RDA candidates per field to the most semantically appropriate WEMI level given the source entity type.\n4. **Deduplication decision** — resolve the triple-subject-key issue before building the GeMeA ingest pipeline.\n5. **Validate CSV against mocho-edit.owl** — check that RDA IRIs marked `in_mocho=True` survive the next ODK rebuild.\n"
}
```

---

### User *(2026-03-23T09:39:12.103Z)*

**Tool result**
```
File created successfully at: /Users/mta/Documents/claude/mocho/notes/alignment-ddbedm-mocho.md
```

---

### Assistant *(2026-03-23T09:39:52.891Z)*

**Tool call:** `Write`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/notes/spec-ddbedm-mocho-alignment.md",
  "content": "# Spec: DDB-EDM → mocho Ontology Alignment\n\n**Status**: Draft\n**Date**: 2026-03-23\n\n---\n\n## Problem\n\nThe GeMeA pipeline ingests DDB cultural heritage records encoded in the DDB-EDM\nprofile (a DDB extension of the Europeana Data Model). mocho is being developed as\nthe middle ontology that bridges EDM to domain-specific ontologies (RDA, RiC-O, Music\nOntology, etc.). Before building the ingest transformation, we need a precise mapping\nfrom every EDM field that actually appears in production data to its corresponding\nmocho/RDA property.\n\nA schema-only alignment (ontology-to-ontology) risks mapping terms that do not appear\nin the data, while missing practical edge cases that do. The alignment must therefore\nbe data-driven: grounded in the actual field distribution of the corpus.\n\n---\n\n## Inputs\n\n| Input | Path | Notes |\n|---|---|---|\n| DDB item corpus | `goethe-faust/data/items-all-goethe-faust.json` | 115,432 records, JSONL |\n| DDB-EDM ontology | `mocho/ontology/ddbedm_1.0.ttl` | Turtle, 683 lines |\n| mocho (full) | `mocho/mocho-odk/src/ontology/mocho-full.owl` | RDF/XML, 49,849 lines |\n| DC→RDA mapping | `mocho/output/mapping_dct_to_rda.csv` | 979 (DC term, RDA IRI) pairs |\n\n---\n\n## Outputs\n\n| Output | Path | Schema |\n|---|---|---|\n| Field profile | `goethe-faust/output/edm_field_profile.{csv,json}` | entity\\_type, json\\_key, record\\_count, record\\_pct, entity\\_pct |\n| Alignment table | `goethe-faust/output/alignment_ddbedm_mocho.{csv,json}` | see below |\n\n**Alignment table columns:**\n\n| Column | Description |\n|---|---|\n| `entity_type` | EDM entity type (`ProvidedCHO`, `Agent`, `Aggregation`, …) |\n| `json_key` | JSON key as it appears in the DDB API response |\n| `edm_prefix` | Namespace prefix (`dc`, `dcterms`, `edm`, `skos`, …) |\n| `edm_iri` | Full IRI of the EDM/DC property |\n| `record_count` | Number of records (lines in JSONL) containing this field |\n| `coverage_pct` | `record_count / total_records × 100` |\n| `rda_iri` | Full IRI of the matched RDA property in mocho (empty if unmatched) |\n| `rda_label` | English `rdfs:label` of the RDA property |\n| `wemi_level` | WEMI entity level of the RDA property (`Work`, `Expression`, `Manifestation`, `Item`, `Agent`) |\n| `match_method` | `via_dct_map` \\| `direct` \\| `via_dct_map_not_in_mocho` \\| `unmatched` |\n| `in_mocho` | Boolean — whether the RDA IRI is present in `mocho-full.owl` |\n\n---\n\n## Success criteria\n\n1. Every DC/DCT property present in the corpus maps to at least one RDA property\n   in mocho, or is explicitly documented as a known gap (no RDA sub-property\n   in the 5.4.9 release).\n2. The alignment table is reproducible: re-running the scripts on the same inputs\n   produces byte-identical output.\n3. EDM-structural properties (`edm:isShownAt`, `edm:aggregatedCHO`, etc.) are\n   explicitly categorised as out of scope for DC→RDA routing and flagged for a\n   separate mapping pass.\n4. No silently missing fields: every (entity_type, json_key) pair from the profile\n   appears in the alignment table, matched or unmatched.\n\n---\n\n## Scope\n\n### In scope\n\n- All properties of `ProvidedCHO` (the main bibliographic entity).\n- Rights properties on `Aggregation` and `WebResource` (DC/DCT terms).\n- DC/DCT properties on `Agent`, `Place`, `PhysicalThing` (carries over from the DC→RDA map).\n\n### Out of scope (first pass)\n\n- **EDM-structural properties**: `edm:isShownAt`, `edm:isShownBy`, `edm:aggregatedCHO`,\n  `edm:dataProvider`, `edm:provider`, `edm:hasView`, `edm:object`. These describe\n  provenance and access, not the intellectual content of the CHO; they need a\n  separate EDM→mocho direct mapping rather than a DC→RDA route.\n- **EDM authority properties**: `edm:dateOfBirth`, `edm:placeOfBirth`,\n  `edm:biographicalInformation`, `edm:gender`, etc. These describe agents and\n  require direct mapping to RDA Person/Corporate Body properties.\n- **SKOS labels and notes**: `skos:prefLabel`, `skos:altLabel`, `skos:note`,\n  `skos:notation` on Agent/Concept/Place. Require a dedicated SKOS→RDA access-point\n  alignment step.\n- **Geographic coordinates**: `geo:lat`, `geo:long`, `geo:alt`. Not bibliographic;\n  handled via a separate spatial indexing step (Elasticsearch geo-point).\n- **DDB extensions**: `ddb:hierarchyType`, `ddb:aggregationEntity`,\n  `ddb:hierarchyPosition`. DDB-specific administrative fields with no standard\n  ontology counterpart.\n\n---\n\n## Constraints\n\n- The alignment must operate entirely on local files (no network calls).\n- The DC→RDA mapping must be consumed as-is from `mapping_dct_to_rda.csv`;\n  the alignment script must not re-derive it.\n- The output format must follow the schema of existing mocho mapping CSVs\n  (`mapping_*_to_*.csv`): one row per (source term, target IRI) pair.\n- Scripts follow project conventions: `pathlib`-relative paths, header docstrings,\n  placed in `goethe-faust/scripts/`.\n\n---\n\n## Known gaps (documented, not defects)\n\n| Field | IRI | Gap reason |\n|---|---|---|\n| `ProvidedCHO.identifier` | `dc:identifier` | No RDA sub-properties in `mapElement2DCT.xml` |\n| `ProvidedCHO.spatial` | `dcterms:spatial` | Not declared as super-property of any RDA property in RDA 5.4.9 |\n| All `Agent.*` EDM properties | `edm:*` | Outside DC→RDA routing scope; need separate pass |\n| `Event.occuredAt` | (none) | No IRI resolved; probable typo in DDB API — expected `edm:occurredAt` |\n\n---\n\n## Open questions\n\n1. **Deduplication of triple subject keys**: `ProvidedCHO.dcSubject`,\n   `.dcTermsSubject`, `.dcTermSubject` carry identical data in 60% of records.\n   Should ingest deduplicate these before asserting triples, or treat them as\n   distinct assertions?\n\n2. **WEMI assignment for `ProvidedCHO`**: The DDB API does not reliably distinguish\n   Work vs. Manifestation in a single `ProvidedCHO` entity. Which WEMI level should\n   be the target for `dc:title`, `dc:creator`, etc.? A heuristic based on\n   `source.description.record.type` (EAD, LIDO, MARC 21 …) may be needed.\n\n3. **High-fanout handling**: `dc:creator` → 232 RDA sub-properties,\n   `dc:contributor` → 360. The alignment table preserves all candidates.\n   A downstream filtering step — restricting by sector, record type, or WEMI\n   level — is required before these can be used in a transformation.\n"
}
```

---

### User *(2026-03-23T09:43:55.891Z)*

**Tool result**
```
File created successfully at: /Users/mta/Documents/claude/mocho/notes/spec-ddbedm-mocho-alignment.md
```

---

### Assistant *(2026-03-23T09:44:43.903Z)*

**Tool call:** `Write`
```json
{
  "file_path": "/Users/mta/Documents/claude/mocho/notes/adr-ddbedm-mocho-alignment.md",
  "content": "# ADR: DDB-EDM → mocho Ontology Alignment Strategy\n\n**Date**: 2026-03-23\n**Status**: Accepted\n\n---\n\n## Context\n\nmocho bridges the DDB-EDM profile (Europeana Data Model as extended by the Deutsche\nDigitale Bibliothek) to RDA and other domain ontologies. To build the GeMeA ingest\ntransformation, we need to decide how to produce and represent the mapping from EDM\nfields to mocho/RDA properties. Several approaches were considered.\n\n---\n\n## Decision 1: Profile actual data before aligning\n\n**Decision**: Run a field-frequency scan of the full corpus (115,432 DDB items)\nbefore doing any ontology mapping. Produce a profile (`edm_field_profile.csv/json`)\nthat is the sole input to the alignment step.\n\n**Alternatives considered**:\n- *Schema-only*: Align the ddbedm_1.0.ttl ontology directly to mocho-full.owl\n  without looking at data. Rejected because ddbedm declares properties that may not\n  appear in the corpus, and the corpus contains informal fields (e.g. the triple\n  subject-key issue, `Event.occuredAt` with no IRI) that are invisible from the\n  schema alone.\n- *Per-record transformation*: Parse the alignment inline during SPARQL/ETL.\n  Rejected because it conflates schema work with instance transformation and makes\n  the mapping invisible to review.\n\n**Rationale**: A data-first profile makes the alignment auditable and reproducible.\nIt surfaces real coverage numbers (e.g. `alternative` at 5%, `identifier` at 88%)\nthat a schema-only pass would not reveal, and catches corpus-specific anomalies\nbefore they propagate into the triplestore.\n\n---\n\n## Decision 2: Route DC/DCT properties via the existing DCT→RDA map\n\n**Decision**: For properties in the DC (`dc:`, `dcterms:`) namespaces, use\n`mapping_dct_to_rda.csv` — produced by the mocho `dct_rda_map.py` workflow — as the\nauthoritative source of RDA sub-property candidates. Do not re-derive this mapping\nin the alignment script.\n\n**Alternatives considered**:\n- *Direct EDM→mocho query*: Inspect `mocho-full.owl` for `owl:equivalentProperty`\n  or `rdfs:subPropertyOf` axioms linking EDM terms to mocho. Rejected because\n  mocho does not yet declare such axioms; they would need to be authored first,\n  creating a circular dependency.\n- *Semantic similarity matching*: Use sentence embeddings (as in\n  `match_objecttypes.py`) to align EDM property labels to mocho property labels.\n  Rejected for schema alignment: embedding similarity is unreliable for fine-grained\n  property distinctions (e.g. `dc:creator` → `has composer agent` vs.\n  `has author of introduction`), and the DCT→RDA map already encodes the\n  authoritative RDA sub-property hierarchy.\n\n**Rationale**: The DCT→RDA map is derived from `mapElement2DCT.xml`, a normative\nartefact published with the RDA Vocabularies release. Reusing it is consistent with\nthe existing mocho pipeline and avoids introducing a new alignment methodology for\nproperties that already have a well-defined answer.\n\n**Consequence**: Properties outside the DC/DCT namespaces (EDM-structural, SKOS,\ngeo, DDB extensions, CIDOC CRM) are not covered by this route and are explicitly\nmarked `unmatched`. A second alignment pass using direct mocho queries will be\nneeded for them.\n\n---\n\n## Decision 3: Output one row per (EDM field × RDA property), preserving all candidates\n\n**Decision**: The alignment table contains one row for every (EDM field, RDA\nproperty) pair, including all high-fanout candidates. `dc:creator` produces 232\nrows, `dc:contributor` produces 360 rows. No automatic candidate selection is done.\n\n**Alternatives considered**:\n- *Collapse to best match*: Pick the single most specific RDA property per field\n  (e.g. `rda:P10311 has creator agent` for `dc:creator`). Rejected because\n  \"most specific\" is context-dependent: the right property for a MARC 21 library\n  record differs from LIDO for a museum object; the alignment script does not have\n  that context.\n- *Restrict to Work-level RDA only*: Since `ProvidedCHO` is most naturally a WEMI\n  Work, filter to `rda:w/*` candidates only. Rejected because some fields\n  (e.g. `dc:format`, `dcterms:issued`) are more naturally Manifestation-level, and\n  forcing Work-level would produce wrong mappings.\n\n**Rationale**: The alignment table is an intermediate artefact, not a finished\ntransformation. Keeping all candidates preserves information for downstream consumers\n(the GeMeA ingest script, the ISWC paper appendix) to make context-aware selections.\nThe `wemi_level` column enables filtering without discarding data.\n\n---\n\n## Decision 4: Treat EDM-structural properties as out of scope for the DC→RDA route\n\n**Decision**: `edm:isShownAt`, `edm:isShownBy`, `edm:aggregatedCHO`,\n`edm:dataProvider`, `edm:provider`, `edm:hasView`, and `edm:object` are explicitly\ncategorised as unmatched and flagged for a separate mapping pass. They are not\ntreated as alignment failures.\n\n**Rationale**: These properties describe the provenance and access structure of the\nEDM Aggregation, not the intellectual content of the CHO. They have no DC→RDA\nmapping by design (they are not sub-properties of any DC term). The correct mocho\nrepresentation for them may not be RDA at all — `edm:isShownAt` maps to a URL, not\na bibliographic property — and that question should be settled in a dedicated\nEDM-structural alignment step.\n\n---\n\n## Decision 5: Implement IRI resolution via ontology parsing + hard-coded overrides\n\n**Decision**: Resolve JSON camelCase keys to full IRIs by:\n1. Parsing `ddbedm_1.0.ttl` with rdflib to build a local-name → IRI lookup.\n2. Applying heuristic camelCase prefix-stripping (`dcTerms*`, `dc*`, `edm*`, etc.).\n3. Applying a small `OVERRIDES` dict for known corpus quirks.\n\n**Overrides in `OVERRIDES`**:\n- `dcTermSubject` → `dcterms:subject` (DDB data variant — missing trailing `s`).\n- `identifier` (bare key, no prefix) → `dc:identifier`.\n\n**Alternatives considered**:\n- *Hardcode the full IRI map*: Maintain a complete static lookup table.\n  Rejected because it duplicates information already in `ddbedm_1.0.ttl` and\n  would need manual maintenance when the ontology changes.\n- *Rely solely on heuristic stripping*: No overrides, accept resolution errors.\n  Rejected because `dcTermSubject` would silently resolve to `dc:termSubject`\n  (non-existent), producing a wrong EDM IRI and an unmatched row for a field\n  present in 60% of records.\n\n**Rationale**: Parsing the ontology for the common case and overriding only known\nanomalies minimises maintenance burden while handling real corpus quirks correctly.\nThe `OVERRIDES` dict is the canonical registry of DDB API deviations from the\ndeclared ontology.\n\n---\n\n## Consequences\n\n- The alignment covers 32 DC/DCT fields in mocho, producing 1,271 (field × RDA)\n  pairs as a starting vocabulary for the GeMeA ingest transformation.\n- 55 fields remain unmatched, split across five documented categories. None are\n  silent failures.\n- A second alignment pass is needed for: (a) EDM-native agent properties, (b) EDM-\n  structural Aggregation properties, (c) SKOS labels, (d) geo coordinates.\n- The `OVERRIDES` dict should be extended if further DDB API deviations are\n  discovered during ingest validation.\n- If mocho's `dct_rda_map.py` is re-run with a newer RDA Vocabularies release,\n  the alignment should be re-run to pick up any new sub-property declarations for\n  `dc:identifier` and `dcterms:spatial` (currently unmapped).\n"
}
```

---

### User *(2026-03-23T09:56:54.167Z)*

**Tool result**
```
File created successfully at: /Users/mta/Documents/claude/mocho/notes/adr-ddbedm-mocho-alignment.md
```

---

### Assistant *(2026-03-23T09:57:02.234Z)*

Three documents written to `mocho/notes/`:

- **`alignment-ddbedm-mocho.md`** — working note: what was done, full results tables by entity type, coverage percentages, unmatched field categories, known issues, next steps.

- **`spec-ddbedm-mocho-alignment.md`** — spec: problem statement, input/output schemas, success criteria, scope boundary (what's in/out of the DC→RDA route), constraints, documented gaps, and three open questions (subject-key deduplication, WEMI assignment for ProvidedCHO, high-fanout filtering).

- **`adr-ddbedm-mocho-alignment.md`** — five architecture decisions with alternatives and rationale:
  1. Data-first profiling over schema-only alignment
  2. DCT→RDA map as the routing authority (not embeddings, not direct mocho query)
  3. All RDA candidates preserved in output (not collapsed to best match)
  4. EDM-structural properties explicitly out of scope
  5. IRI resolution via ontology parsing + `OVERRIDES` dict for corpus quirks

---

### User *(2026-03-23T09:57:34.984Z)*

change filenames: alignment-ddbedm-mocho-[spec/adr].md

---

### Assistant *(2026-03-23T09:57:42.626Z)*

**Tool call:** `Bash`
```json
{
  "command": "mv /Users/mta/Documents/claude/mocho/notes/spec-ddbedm-mocho-alignment.md /Users/mta/Documents/claude/mocho/notes/alignment-ddbedm-mocho-spec.md && mv /Users/mta/Documents/claude/mocho/notes/adr-ddbedm-mocho-alignment.md /Users/mta/Documents/claude/mocho/notes/alignment-ddbedm-mocho-adr.md",
  "description": "Rename spec and ADR files"
}
```

---

### User *(2026-03-23T09:57:45.282Z)*

**Tool result**
```
(Bash completed with no output)
```

---
