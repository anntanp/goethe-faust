# Plan: link_gnd_works.py — GND Werk lookup from werk_staging

## Context

`transform_edm_to_mocho.py` writes a DuckDB staging table (`output/goethe-faust-werk-staging.duckdb`)
for every record whose class dispatch assigns a W-slot class (`rdac:C10001` or `mo:MusicalWork`).
`link_gnd_works.py` (Phase 0) consumes this table, resolves each CHO to a GND Werk authority
record via `https://gnd.ise.fiz-karlsruhe.de/sparql`, mints a GeMeA Work URI, and writes
WEMI link triples into `graph/work` (ADR D17).

## Input / staging table

`output/goethe-faust-werk-staging.duckdb` — table `werk_staging`.

`link_gnd_works.py` adds two columns on first run (ALTER TABLE IF NOT EXISTS pattern):

| Column | Type | Notes |
|---|---|---|
| `ddb_obj_id` | VARCHAR PK | DDB object ID |
| `cho_uri` | VARCHAR | GeMeA CHO URI |
| `target_class` | VARCHAR | `rdac:C10001` or `mo:MusicalWork` |
| `dc_title` | VARCHAR | Raw title string |
| `dc_alternative` | VARCHAR[] | Alternate titles |
| `dc_created` | VARCHAR | Date string |
| `creator_uris` | VARCHAR[] | GND URIs (`http://d-nb.info/gnd/…`) |
| `creator_literals` | VARCHAR[] | `last, first` form |
| **`status`** | VARCHAR | `pending` / `resolved` / `ambiguous` / `unresolved` |
| **`gnd_uri`** | VARCHAR | Matched GND Werk URI, or NULL |
| **`confidence`** | FLOAT | Match confidence score (0.0–1.0), or NULL |
| **`prov_lm`** | JSON | Current-best provenance (mirrors latest attempt) |

Status values:

| Value | Meaning | Reprocessable |
|---|---|---|
| `pending` | Not yet processed by `link_gnd_works.py` | — |
| `resolved` | Single GND match; `skos:exactMatch` emitted | No |
| `ambiguous` | Multiple GND matches; stub emitted | Yes — NER model may disambiguate |
| `unresolved` | No GND match; stub emitted | Yes — NER model may yield better title |

On reprocessing runs, `link_gnd_works.py` filters `WHERE status IN ('pending', 'ambiguous', 'unresolved')` — resolved rows are skipped.

### werk_attempts table (append-only)

`werk_staging` holds the **current best** result. Each linking run appends to `werk_attempts`:

```sql
CREATE TABLE IF NOT EXISTS werk_attempts (
    ddb_obj_id   VARCHAR,
    attempt_no   INTEGER,       -- auto-incremented per ddb_obj_id
    status       VARCHAR,       -- resolved / ambiguous / unresolved
    gnd_uri      VARCHAR,       -- NULL if not resolved
    confidence   FLOAT,         -- 0.0–1.0, NULL if not applicable
    duration_ms  INTEGER,       -- wall-clock time for this attempt
    prov_lm      JSON,          -- system/model provenance
    PRIMARY KEY (ddb_obj_id, attempt_no)
)
```

After each attempt, `werk_staging.status`, `.gnd_uri`, `.confidence`, and `.prov_lm` are
updated to the current best. Cross-attempt analysis stays plain SQL:
`SELECT * FROM werk_attempts WHERE ddb_obj_id = ? ORDER BY attempt_no`.

`prov_lm` JSON schema — **not fixed; extend fields as the pipeline evolves**.
Fields present in v0 (initial rule-based passes):

```json
{
  "schema_version": "0.1",
  "stage":          "isbd_fts_exact",
  "pass":           2,
  "method":         "fts+exact",
  "timestamp":      "2026-05-05T10:00:00Z",
  "endpoint":       "https://gnd.ise.fiz-karlsruhe.de/sparql",
  "script":         "link_gnd_works.py",
  "script_sha256":  "a3f2...",
  "model":          null,
  "model_version":  null,
  "score":          0.94,
  "duration_ms":    143
}
```

Additional fields added when NER runs (v0.2+):

```json
{
  "model":         "xlm-roberta-large",
  "model_version": "1.0.0",
  "model_sha256":  "b7c1...",
  "ner_span":      "Faust",
  "ner_conf":      0.91
}
```

`schema_version` allows consumers to handle field evolution without breaking.
`script_sha256` is the SHA-256 of `link_gnd_works.py` at run time — enables exact reproduction.
`confidence` is mirrored as a top-level column in both tables for aggregate queries without JSON extraction.

## Output

`output/goethe-faust-work.nq` — N-Quads for `graph/work`:

```turtle
<gemea-work-uri>  a rdac:C10001 .                            # or mo:MusicalWork
<gemea-work-uri>  mocho:hasManifestation  <cho-uri> .
<cho-uri>         mocho:isManifestationOf <gemea-work-uri> .
<gemea-work-uri>  skos:exactMatch         <gnd-uri> .        # omitted on stub
```

Work URI scheme: `https://gemea.ise.fiz-karlsruhe.de/work/<uuid5(cho_uri)>`

## Passes

Each pass processes only `status IN ('pending', 'ambiguous', 'unresolved')` rows.
Every attempt appends a row to `werk_attempts`. `werk_staging` is updated to current best after each pass.
Passes are additive — run them independently; earlier passes need not be re-run.

| Pass | Title input | Heuristics | Creator filter | Stage tag |
|---|---|---|---|---|
| 1 | `dc_title` raw | None | URI if present, literal fallback | `raw_fts_exact` |
| 2 | `dc_title` ISBD-stripped | ISBD punctuation rules | URI if present, literal fallback | `isbd_fts_exact` |
| 3 | `dc_alternative[]` raw | None | URI if present | `alt_raw_fts_exact` |
| 4 | NER-extracted title | xlm-roberta-large | URI if present | `ner_fts_exact` |

Further passes can be added; `stage` in `prov_lm` is the identifier.

### Pass 1 — Raw FTS (no heuristics)

`dc_title` passed directly to QLever FTS, confirmed with exact string match.
Fast baseline; catches well-formed titles that match GND `preferredNameForTheWork` verbatim.

### Pass 2 — ISBD-stripped FTS

Strip non-title-proper content from `dc_title` per `gemea/notes/ner/sr01_isbd-applicability.md §2.1`:

| Signal | Pattern | Action |
|---|---|---|
| Area separator | `. -` | Split; take part before first occurrence |
| Subtitle | ` :` | Split; take part before |
| Statement of responsibility | ` /` | Split; take part before |
| Volume | `Bd.`/`Teil`/`Heft`/`Nr.` + digit | Strip from end |

Result: `title_proper` passed to FTS + exact confirm.

### Pass 3 — dc:alternative fallback

Apply same raw FTS logic to each value in `dc_alternative[]`. First hit wins.

### Pass 4 — NER fallback (deferred)

NER model (xlm-roberta-large) extracts title entity from raw `dc_title`.
Extracted span passed to FTS. `prov_lm.model` set to model name + version.

### FTS + confirm query (all passes)

`ql:contains-word` is deprecated (see [qlever#2688](https://github.com/ad-freiburg/qlever/issues/2688)).
Current FTS syntax uses `ql:has-word` inside a `GRAPH` pattern, where the graph variable binds the relevance score ([qlever#2579](https://github.com/ad-freiburg/qlever/pull/2579)):

```sparql
PREFIX gndo: <https://d-nb.info/standards/elementset/gnd#>
PREFIX ql:   <http://qlever.cs.uni-freiburg.de/builtin-functions/>

SELECT ?werk ?prefName ?score WHERE {
  ?werk  a gndo:Work ;                          # or gndo:MusicalWork per target_class
         gndo:preferredNameForTheWork ?prefName .
  GRAPH ?score { ?prefName ql:has-word "<title_tokens>" }
}
ORDER BY DESC(?score)
LIMIT 20
```

`target_class` selects the GND class: `rdac:C10001` → `gndo:Work`; `mo:MusicalWork` → `gndo:MusicalWork`.
Candidates confirmed with `FILTER(STR(?prefName) = "<title>")` or in Python after fetch.

**Note**: the GND SPARQL endpoint at `gnd.ise.fiz-karlsruhe.de` did not return FTS results in
pilot testing (May 2026) — neither `ql:contains-word` nor `ql:has-word` matched, likely because
the endpoint's text index does not cover `gndo:preferredNameForTheWork`. The pilot script
(`link_gnd_works.py`) falls back to `FILTER(CONTAINS(LCASE(STR(?prefName)), LCASE("...")))`,
which scans the full predicate (~11 s without creator filter, ~20 ms with). Use `ql:has-word`
when loading GND data into a self-hosted QLever instance with a text index built over
`gndo:preferredNameForTheWork`.

### Creator filter (all passes)

| Condition | Filter added |
|---|---|
| `creator_uris` non-empty | `?werk gndo:firstAuthor <uri> .` (or `gndo:firstComposer` for MusicalWork); URIs normalized `http://` → `https://` |
| `creator_uris` empty, `creator_literals` non-empty | FTS on `gndo:preferredNameForThePerson` using first literal token |
| Both empty | Title match only |

### Emit triples

| Outcome | Triples emitted | `status` | `gnd_uri` |
|---|---|---|---|
| Single GND match | Full WEMI + `skos:exactMatch` | `resolved` | GND URI |
| Multiple matches | Stub (`rdf:type` + WEMI only) | `ambiguous` | NULL |
| No match | Stub (`rdf:type` + WEMI only) | `unresolved` | NULL |

Stubs preserve the W-slot classification in `graph/work`. Resolution rate (resolved / total)
is a reportable metric for the paper. Ambiguous and unresolved rows are reprocessable when
the NER model is ready.

## Script

**Location**: `goethe-faust/scripts/link_gnd_works.py`

**CLI**:
```
python link_gnd_works.py \
  --staging output/goethe-faust-werk-staging.duckdb \
  --out     output/goethe-faust-work.nq \
  --endpoint https://gnd.ise.fiz-karlsruhe.de/sparql \
  [--limit N] [--stats json|none]
```

**Dependencies**: `duckdb`, `urllib` (stdlib) for SPARQL GET — no extra HTTP client needed.

## Verification

1. Run `transform_edm_to_mocho.py` to produce the staging `.duckdb`
2. Run `link_gnd_works.py` and inspect `--stats` output: resolved / stub / ambiguous counts
3. Spot-check 5–10 rows in `goethe-faust-work.nq`: confirm `skos:exactMatch` URIs are valid GND Werk URIs
4. Load into QLever, query `GRAPH <…/graph/work>` — confirm WEMI triples are present and `cho_uri` values match `graph/mocho`
5. MCP: `SELECT ?w ?gnd WHERE { GRAPH <…/graph/work> { ?w skos:exactMatch ?gnd } } LIMIT 10`
