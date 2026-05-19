# Transform prescan — two-pass architecture plan

**Date**: 2026-05-14
**Status**: Pending — context captured for a later session
**Relates to**: `scripts/transform/__main__.py`, `scripts/run_gemea_transform.sh`,
               `gemea/scripts/py/export_ddb.py`, `gemea/scripts/py/export_ddb_parquet.py`

---

## 1. Motivation

`--prov-db` was added (2026-05-13, `transform-implementation-actual.md §11`) to
deduplicate shared PROV-O node descriptive triples across sector runs. The current
design loads the DB at startup and writes back after the record loop — which breaks
under concurrent workers (DuckDB single-writer constraint).

The fix is a two-pass architecture:

- **Pass 1 (prescan)**: single-process scan that pre-populates `entities.duckdb` and
  builds the Parquet metadata file. No transform, no concurrency.
- **Pass 2 (main transform)**: N concurrent workers load `entities.duckdb` read-only
  at startup and never write to it. No locking needed.

---

## 2. Pass 1 — `scripts/transform/prescan.py`

### 2.1 Inputs

| Arg | Description |
|---|---|
| `--db PATH` | Sector SQLite file (`objs` table, `bufgz` column) |
| `--prov-db PATH` | Shared DuckDB for `prov_entities` table (PROV-O shared nodes) |
| `--concept-labels-db PATH` | Shared DuckDB for `concept_labels` table (URIs from `dcType`/`dc_subject`) |
| `--agent-labels-db PATH` | Shared DuckDB for `agent_labels` table (URIs from creator/contributor/publisher) |
| `--lido PATH` | `lido_event_types.csv` — event-type code → label mapping (needed for `agents.type` and `dates.type` for LIDO-derived entries) |
| `--prov-out PATH` | Output `.nq` file for shared PROV-O descriptive triples |
| `--parquet-out PATH` | Output per-sector Parquet file (e.g. `s2_meta.parquet`) |

### 2.2 What it does

**Single scan** of the SQLite file (sequential, one process):

1. For each record, extract:
   - `properties.mapping-version` → `urn:ddbedm:xslt:<ver>`
   - `properties.dataset-id` → `urn:ddbedm:dataset:<id>`
   - `provider-info.provider-ddb-id` → `urn:ddbedm:provider:<id>`
   - Fixed: `DDB_BASE = "http://www.deutsche-digitale-bibliothek.de"`
   - Parquet metadata row (see §2.3)

2. On first encounter of each PROV-O URI, emit its descriptive triples to
   `prov-shared.nq` via `emit_prov_triples` and register the URI in a local set.

3. After the loop, three sequential lock-and-write operations (each brief; all heavy work done before):
   - Acquire `fcntl.flock` on `$PROV_DB.lock` → `CREATE TABLE IF NOT EXISTS prov_entities` → SELECT which of `new_entities` already exist → insert only the truly new ones → append `.nq` lines **only for truly new URIs** → release. (Prevents duplicate `.nq` lines on re-runs without `--replace-dbs`.)
   - Acquire `fcntl.flock` on `$CONCEPT_LABELS_DB.lock` → write `concept_labels_pending` to `concept_labels.duckdb` → release.
   - Acquire `fcntl.flock` on `$AGENT_LABELS_DB.lock` → write `agent_labels_pending` to `agent_labels.duckdb` → release.
   - Flush the Parquet writer to `--parquet-out` (per-sector file, no locking needed — each worker writes its own path).

**No edm:Agent / Place / Concept / TimeSpan in Pass 1** — those are deduplicated by
`sort -u` at NT merge time (Pass 2 produces per-chunk NT files; Phase 4 merges with
`sort -u`).

### 2.3 Parquet schema changes (also applies to `export_ddb.py` and `export_ddb_parquet.py`)

Changes to `PARQUET_SCHEMA` (defined in `gemea/scripts/py/export_ddb.py`,
imported by `export_ddb_parquet.py`):

| Field | Current | New |
|---|---|---|
| `lang` | `pa.string()` | **dropped** — split into `lang_title` and `lang_obj` |
| `provider_id` | _(absent)_ | `pa.string()` — `provider-info.provider-ddb-id` |
| `dataset_id` | _(absent)_ | `pa.string()` — `properties.dataset-id` |
| `lang_title` | _(absent)_ | `pa.string()` — language tag of `ProvidedCHO.title` (e.g. `ger`, `eng`, `zxx`) |
| `lang_obj` | _(absent)_ | `pa.string()` — content language from `dc:language` / `dcterms:language` (e.g. `ger`, `eng`) |
| `description` | _(absent)_ | `pa.list_(pa.string())` — `ProvidedCHO.description` (multilingual, multi-valued; 41% of records have >1 value) |
| `dc_type` | `pa.string()` | `pa.list_(CONCEPT_STRUCT)` — `{name, is_ext_uri}` structs (see below) |
| `dc_date` | `pa.string()` | **dropped** — merged into `dates` |
| `dc_date_qualifier` | `pa.string()` | **dropped** — merged into `dates` |
| `dc_issued` | `pa.list_(pa.string())` | **dropped** — merged into `dates` |
| `dc_created` | `pa.list_(pa.string())` | **dropped** — merged into `dates` |
| `dates` | _(absent)_ | `pa.list_(struct(value: string, begin: string, end: string, type: string))` — new unified field |
| `dc_creator` | `pa.list_(struct(name: string, type: string))` | **dropped** — merged into `agents` |
| `dc_contributor` | `pa.list_(struct(name: string, type: string))` | **dropped** — merged into `agents` |
| `dc_publisher` | `pa.list_(struct(name: string, type: string))` | **dropped** — merged into `agents` |
| `agents` | `pa.list_(pa.string())` | `pa.list_(struct(name: string, type: string, is_ext_uri: bool))` — unified |
| `dc_subject` | `pa.list_(pa.string())` | `pa.list_(CONCEPT_STRUCT)` — `{name, is_ext_uri}` structs (same logic as `dc_type`) |
| `dc_subject_uris` | `pa.list_(pa.string())` | **dropped** |
| `mediatype` | _(absent)_ | `pa.int16()` — new field |
| `sector` | _(absent)_ | `pa.int16()` — new field |
| `hierarchy_type` | `pa.string()` | `pa.int16()` |

**`dc_type`** and **`dc_subject`** use the shared `CONCEPT_STRUCT = pa.struct([("name", pa.string()), ("is_ext_uri", pa.bool_())])`.
Values are a mix of plain literals (`"Fotoalbum"`, `"Dokument"`) and authority URIs (Getty AAT, GND, Wikidata).
Each entry stores the resolved label in `name` and `True` in `is_ext_uri` when the value came from a URI.

Extraction logic (identical for both fields):

1. Build a `concept_labels` dict from all `Concept[].about → prefLabel.$` in the record.
2. For each entry:
   - Has `$` (plain literal) → `{name: lit, is_ext_uri: False}`.
   - Has `resource` (URI) that resolves in `concept_labels` → `{name: label, is_ext_uri: True}`.
   - Has `resource` (non-DDB URI) **not** in `concept_labels` → store `(uri, None)` in
     `concept_labels.duckdb` for later enrichment; omit from Parquet list for now.
3. DDB vocnet URIs (`http://ddb.vocnet.org/medientyp/…`, `http://ddb.vocnet.org/sparte/…`)
   are silently skipped — sector/mediatype codes are captured in the `mediatype`/`sector` columns instead.
4. `dc_subject` additionally skips bare 32-char DDB IDs (no http prefix).

Corpus sample results (1,000 records): 561 literal values, 231 URI values. Of the URIs,
Getty AAT and GND resolve via same-record Concept blocks; Wikidata URIs often do not
(no matching Concept entry in the record).

```python
# resolve dc_type values → list[{name, is_ext_uri}]
dc_type: list[dict] = []
for v in coerce_list(cho.get("dcType")):
    if isinstance(v, dict):
        lit, res = v.get("$") or "", v.get("resource") or ""
        if lit:
            dc_type.append({"name": lit, "is_ext_uri": False})
        elif res and not res.startswith("http://ddb.vocnet.org/") and _is_ext_uri(res):
            label = concept_labels.get(res)
            if label:
                dc_type.append({"name": label, "is_ext_uri": True})
            else:
                concept_labels_pending.setdefault(res, None)
    elif isinstance(v, str) and v:
        dc_type.append({"name": v, "is_ext_uri": False})
# dc_subject uses the same pattern + skips bare 32-char DDB IDs
```

**`mediatype`**: not in `properties.*`. It comes from `edm.RDF.Concept[].about` —
scan concept `about` values for the pattern `http://ddb.vocnet.org/medientyp/mt*`
and extract the `mt*` code (last path segment). Take the first unique match; there
can be duplicates within a record (same URI repeated). Sample: `mt002`, `mt003`,
`mt001`, `mt005`, `mt007`.

Extraction snippet:
```python
mediatype = ""
sector = ""
concepts = rdf.get("Concept") or []
if isinstance(concepts, dict):
    concepts = [concepts]
for c in concepts:
    if not isinstance(c, dict):
        continue
    about = c.get("about") or ""
    if not mediatype and "/medientyp/mt" in about:
        mediatype = int(about.rsplit("/mt", 1)[-1])      # "mt002" → 2
    if not sector and "/sparte/sparte" in about:
        sector = int(about.rsplit("/sparte", 1)[-1])     # "sparte005" → 5

# hierarchy_type: strip "htype_" prefix, cast to int
raw_ht = (_scalar_values(cho.get("hierarchyType")) or [None])[0]
hierarchy_type = int(raw_ht.replace("htype_", "")) if raw_ht else None  # "htype_015" → 15
```

**`concept_labels.duckdb`** — new DuckDB file written by prescan. Collects all
`(uri, label)` pairs seen in `dcType` and `dc_subject` source fields across the corpus,
for later lookup and enrichment.

```sql
CREATE TABLE IF NOT EXISTS concept_labels (
    uri     VARCHAR PRIMARY KEY,
    label   VARCHAR          -- skos:prefLabel resolved from same-record Concept block;
                             -- NULL if not resolvable within the record
)
```

**What goes in**: all non-DDB-internal URIs from `dcType`, `dcSubject`, `dcTermsSubject`,
and `dcTermSubject` (the last two are typo variants of the same field, both present in
the corpus). Excluded: DDB vocnet URIs (`http://ddb.vocnet.org/…`) and bare 32-character
DDB-internal IDs (e.g. `YUVZR2OFQCZ5HKUOCBWXTII5WN6DCLOK`).

**`dcTermSubject` note**: a misspelling of `dcterms:subject` present in 590/1,000
sampled records (alongside `dcTermsSubject`). Both fields contain the same structure —
bare DDB IDs and GND URIs — and are scanned together. Bare IDs are excluded from
`concept_labels.duckdb` (entity resolution problem, not a label lookup problem).

**Populated via** `INSERT OR IGNORE (uri, label)` for every qualifying URI encountered,
where `label` is the `skos:prefLabel` resolved from the same record's `Concept[]`
block (or `NULL` if no matching Concept exists — e.g. some Wikidata URIs lack a
Concept entry). `INSERT OR IGNORE` means the first non-null label seen wins; a later
enrichment pass can fill in nulls via authority endpoint queries (Getty AAT SPARQL,
Wikidata API, lobid-gnd).

**Parquet impact**: `dc_type` and `dc_subject` in Parquet are `list_(CONCEPT_STRUCT)`.
Entries with unresolvable URIs (NULL labels) are omitted from Parquet but written to
`concept_labels.duckdb` for enrichment. `dc_subject_uris` column is **dropped**
(superseded by `concept_labels.duckdb`). The `is_ext_uri` flag on each entry records
whether the value originated from an authority URI (`True`) or a plain literal (`False`).

**`agent_labels.duckdb`** — new DuckDB file, parallel to `concept_labels.duckdb`,
for `dc_creator`, `dc_contributor`, `dc_publisher` agent URIs.

```sql
CREATE TABLE IF NOT EXISTS agent_labels (
    uri     VARCHAR PRIMARY KEY,
    label   VARCHAR          -- from $-field of the same dict; rarely NULL for agents
)
```

**What goes in**: HTTP URIs from creator/contributor/publisher dicts (primarily GND:
`http://d-nb.info/gnd/…`). Bare 32-char DDB IDs are not observed in agent fields
(corpus sample: 0 bare IDs across 200 records); if encountered they are excluded.

**Key difference from `concept_labels`**: no Concept block lookup needed — the label
is already inline in the same `{'resource': uri, '$': label}` dict. Extract both in
one pass:

```python
agent_labels_pending: dict[str, str | None] = {}
agent_label_list: list[str] = []

val = cho.get("creator") or []
if isinstance(val, dict): val = [val]
for v in val:
    if not isinstance(v, dict): continue
    res = v.get("resource"); lit = v.get("$") or ""
    if lit:
        agent_label_list.append(lit)
    if res and res not in (None, "None", "") and res.startswith("http"):
        agent_labels_pending[res] = lit or None  # → agent_labels.duckdb
# same loop for contributor and publisher
```

`INSERT OR IGNORE (uri, label)` — first label seen wins. A later enrichment pass can
resolve NULLs via lobid-gnd or Wikidata.

**Unified `agents` column** — replaces the current `dc_creator`, `dc_contributor`,
`dc_publisher`, and `agents` (LIDO participants) columns with a single
`pa.list_(pa.struct([pa.field("name", pa.string()), pa.field("type", pa.string()), pa.field("is_ext_uri", pa.bool_())]))`.

Type vocabulary — noun form throughout for consistency with LIDO labels:

| Source | `type` value |
|---|---|
| `ProvidedCHO.creator` | `creation` |
| `ProvidedCHO.publisher` | `publication` |
| `ProvidedCHO.contributor` | `contribution` |
| `hasMet → P11_had_participant` | LIDO label from `lido_event_types.csv` (`creation`, `publication`, `production`, `photography`, `performance`, `provenance`, `designing`, `commissioning`, `unknown_event`, …) |

`dc:contributor` uses `contribution` (not `contributor`) to follow the noun pattern.
It has no direct LIDO equivalent — it is the generic `dc_agent_fallback` for most
LIDO event types and does not derive from event traversal.

**Unified `dates` column** — replaces `dc_date`, `dc_date_qualifier`, `dc_issued`,
`dc_created` with a single struct list:

```python
DATE_STRUCT = pa.struct([
    pa.field("value", pa.string()),  # set for point-in-time; null for ranges
    pa.field("begin", pa.string()),  # set for ranges; null for point-in-time
    pa.field("end",   pa.string()),  # set for ranges; null for point-in-time
    pa.field("type",  pa.string()),  # event-type label (noun form)
])

("dates", pa.list_(DATE_STRUCT))
```

Type vocabulary — same noun pattern as agents:

| Source | `type` value |
|---|---|
| `ProvidedCHO.created` + LIDO creation event chain (`lido00012`, `eventType/creation`) | `creation` |
| `ProvidedCHO.issued` + LIDO publication event chain (`lido00228`, `eventType/publication`) | `publication` |
| `ProvidedCHO.date` (direct field, no LIDO traversal) | `unknown_event` |

`dc_date_qualifier` (e.g. `circa`, `before`, `after`) is dropped for now — can be
added as a third struct field `qualifier` if needed later.

### 2.4 Files to update for Parquet schema change

| File | Change |
|---|---|
| `gemea/scripts/py/export_ddb.py` | `PARQUET_SCHEMA`: drop `lang`, `dc_date`, `dc_date_qualifier`, `dc_issued`, `dc_created`, `dc_creator`, `dc_contributor`, `dc_publisher`, `dc_subject_uris`; change `dc_type` → `list_(CONCEPT_STRUCT)`, `dc_subject` → `list_(CONCEPT_STRUCT)`, `hierarchy_type` → `int16`, `agents` → `list_(AGENT_STRUCT)`; add `description list_(string)`, `lang_title`, `lang_obj`, `provider_id`, `dataset_id`, `dates list_(DATE_STRUCT)`, `mediatype int16`, `sector int16`. `extract_meta`: unified agents/dates structs, `dc_type`/`dc_subject` → CONCEPT_STRUCT, `description` list, `lang_title`/`lang_obj` split, int extractions, `provider_id`/`dataset_id`. |
| `gemea/scripts/py/export_ddb_parquet.py` | Same `PARQUET_SCHEMA` and `extract_meta` changes (this file re-implements `extract_meta` with dc_created/dc_issued fixes — keep those fixes, apply all schema changes above on top). |

### 2.5 DuckDB schema written by prescan

**`prov.duckdb`** (passed as `--prov-db`). Contains one table:

```sql
CREATE TABLE IF NOT EXISTS prov_entities (
    uri         VARCHAR PRIMARY KEY,
    entity_type VARCHAR NOT NULL
)
```

Populated rows after prescan (entity_type values):

| entity_type | Example URI |
|---|---|
| `prov_xslt` | `urn:ddbedm:xslt:6.18` |
| `prov_dataset` | `urn:ddbedm:dataset:<id>` |
| `prov_provider` | `urn:ddbedm:provider:<id>` |
| `prov_ddb` | `http://www.deutsche-digitale-bibliothek.de` |

### 2.6 Output: `prov-shared.nq`

Contains the descriptive triples for all unique PROV-O shared nodes, emitted once,
as N-Quads with the named graph `https://gemea.ise.fiz-karlsruhe.de/graph/prov` as
the fourth element on every line. Processed by `split_nq.py` in Phase 4 alongside
the per-chunk `.nq` files; its `prov` slug merges into `$NT_DIR/prov.nt`.

---

## 3. Pass 2 — changes to `__main__.py`

Replace the current entities DB block (load + write-back via persistent connection)
with a read-only load-and-close:

```python
prov_entities: dict[str, str] = {}
if args.prov_db:
    try:
        import duckdb as _ddb_ent
        _c = _ddb_ent.connect(str(args.prov_db), read_only=True)
        rows = _c.execute(
            "SELECT uri, entity_type FROM prov_entities"
        ).fetchall()
        _c.close()
        prov_entities = {uri: etype for uri, etype in rows}
        log.info("Loaded %d emitted entities from %s",
                 len(prov_entities), args.prov_db)
    except ImportError:
        log.warning("duckdb not available — --prov-db ignored")
    except Exception as exc:
        log.warning("Could not read --prov-db %s: %s", args.prov_db, exc)
```

**Remove entirely**: the write-back block (lines 400–406) and the `entities_conn`
variable. Workers never write to the entities DB.

---

## 4. Changes to `run_gemea_transform.sh`

### 4.0 New CLI arguments

```
--prov-db PATH           Shared PROV-O entities DuckDB (default: $OUT_BASE/prov.duckdb)
--concept-labels-db PATH concept_labels.duckdb (default: $OUT_BASE/concept_labels.duckdb)
--agent-labels-db PATH   agent_labels.duckdb   (default: $OUT_BASE/agent_labels.duckdb)
--parquet-dir PATH       Output dir for per-sector Parquet files (default: $OUT_BASE/parquet/)
--parquet-merge PATH     If set, run merge_parquet.py after all prescan workers finish,
                         concatenating per-sector files into one combined Parquet at PATH
--replace-dbs            Wipe and rebuild the three label DuckDB files and prov-shared.nq
                         before prescan; without this flag, prescan appends (INSERT OR IGNORE)
```

`--prov-db`, `--concept-labels-db`, `--agent-labels-db`, and `--parquet-dir` may live
**outside** `$OUT_BASE` to persist across versioned runs.

`--replace-dbs` wipes only the label DBs and `prov-shared.nq`; it does not affect
`$OUT_BASE` sector output. The existing `--new` flag wipes `$OUT_BASE` entirely.

### 4.1 Add prescan phase (before the sector loop)

```bash
PROV_DB=${PROV_DB_ARG:-$OUT_BASE/prov.duckdb}
CONCEPT_LABELS_DB=${CONCEPT_LABELS_DB_ARG:-$OUT_BASE/concept_labels.duckdb}
AGENT_LABELS_DB=${AGENT_LABELS_DB_ARG:-$OUT_BASE/agent_labels.duckdb}
PARQUET_DIR=${PARQUET_DIR_ARG:-$OUT_BASE/parquet}
PROV_SHARED=$OUT_BASE/prov-shared.nq

mkdir -p "$PARQUET_DIR"

if [[ "$REPLACE_DBS" == "1" ]]; then
  rm -f "$PROV_DB" "$CONCEPT_LABELS_DB" "$AGENT_LABELS_DB" "$PROV_SHARED"
  echo "[$(date '+%F %T')] --replace-dbs: wiped label DBs and prov-shared.nq"
fi

for n in 1 2 3 4 5 6 7; do
  (
    echo "[$(date '+%F %T')] [s${n}] prescan starting"
    "$PYTHON" "$SCRIPTS/transform/prescan.py" \
      --db                "$SQLITE_DIR/s${n}.sqlite" \
      --prov-db           "$PROV_DB" \
      --concept-labels-db "$CONCEPT_LABELS_DB" \
      --agent-labels-db   "$AGENT_LABELS_DB" \
      --lido              "$CFG/lido_event_types.csv" \
      --prov-out          "$PROV_SHARED" \
      --parquet-out       "$PARQUET_DIR/s${n}_meta.parquet"
    echo "[$(date '+%F %T')] [s${n}] prescan done"
  ) &
done
wait

# optional merge into one combined Parquet
if [[ -n "$PARQUET_MERGE_ARG" ]]; then
  echo "[$(date '+%F %T')] Merging per-sector Parquet → $PARQUET_MERGE_ARG"
  "$PYTHON" "$SCRIPTS/transform/merge_parquet.py" \
    --indir  "$PARQUET_DIR" \
    --out    "$PARQUET_MERGE_ARG"
  echo "[$(date '+%F %T')] Parquet merge done"
fi
```

Prescans run **in parallel** (one background process per sector, same as the main
transform loop). Each worker acquires an exclusive `fcntl.flock` lock on the
corresponding `.lock` file before writing to the shared DuckDB and (for prov)
appending to `prov-shared.nq`, then releases immediately. Since each write batch is
small (one sector's unique PROV-O URIs, typically tens to low hundreds of rows),
lock contention is negligible.

Locking pattern inside `prescan.py` (write phase only; scan phase is lock-free).
Each DuckDB file is separate, so each gets its own lock file and connection:

```python
import fcntl

# --- prov.duckdb + prov-shared.nq ---
with open(str(prov_db_path) + ".lock", "a") as lf:
    fcntl.flock(lf, fcntl.LOCK_EX)
    try:
        conn = duckdb.connect(str(prov_db_path))
        conn.execute("""CREATE TABLE IF NOT EXISTS prov_entities (
                            uri         VARCHAR PRIMARY KEY,
                            entity_type VARCHAR NOT NULL)""")
        # find which URIs are truly new (not already in DB from a prior run)
        uris = list(new_entities.keys())
        if uris:
            placeholders = ",".join("?" * len(uris))
            existing = {r[0] for r in conn.execute(
                f"SELECT uri FROM prov_entities WHERE uri IN ({placeholders})", uris
            ).fetchall()}
        else:
            existing = set()
        truly_new = {u: t for u, t in new_entities.items() if u not in existing}
        conn.executemany("INSERT OR IGNORE INTO prov_entities VALUES (?, ?)",
                         list(truly_new.items()))
        conn.close()
        # only append .nq lines for URIs that were actually new
        with open(prov_out_path, "a") as pf:
            for line in new_prov_lines:
                if any(uri in line for uri in truly_new):
                    pf.write(line)
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)

# --- concept_labels.duckdb ---
with open(str(concept_labels_db_path) + ".lock", "a") as lf:
    fcntl.flock(lf, fcntl.LOCK_EX)
    try:
        conn = duckdb.connect(str(concept_labels_db_path))
        conn.execute("""CREATE TABLE IF NOT EXISTS concept_labels (
                            uri   VARCHAR PRIMARY KEY,
                            label VARCHAR)""")
        conn.executemany("INSERT OR IGNORE INTO concept_labels VALUES (?, ?)",
                         list(concept_labels_pending.items()))
        conn.close()
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)

# --- agent_labels.duckdb ---
with open(str(agent_labels_db_path) + ".lock", "a") as lf:
    fcntl.flock(lf, fcntl.LOCK_EX)
    try:
        conn = duckdb.connect(str(agent_labels_db_path))
        conn.execute("""CREATE TABLE IF NOT EXISTS agent_labels (
                            uri   VARCHAR PRIMARY KEY,
                            label VARCHAR)""")
        conn.executemany("INSERT OR IGNORE INTO agent_labels VALUES (?, ?)",
                         list(agent_labels_pending.items()))
        conn.close()
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)
```

All heavy work (scanning, extracting, building `new_entities` / `new_prov_lines` /
Parquet rows) happens before the lock is acquired. The lock is held only for the
final DB insert + file append.

### 4.2 Pass `--prov-db` to all transform workers

Add `--prov-db "$PROV_DB"` to both the single-worker and multi-worker
transform invocations.

### 4.3 Include `prov-shared.nq` in Phase 4 NT merge

In the Phase 4 merge loop, ensure `prov-shared.nq` is split and included:

```bash
"$PYTHON" "$SCRIPTS/split_nq.py" "$PROV_SHARED" &
```

Then the `prov.nt` merge will include the shared-node triples alongside the
per-chunk prov NT files.

### 4.4 Update `--new` wipe

```bash
rm -rf "$OUT_BASE"/s{1..7} "$OUT_BASE/nt" \
       "$OUT_BASE/werk-staging-merged.duckdb" \
       "$OUT_BASE/prov.duckdb" \
       "$OUT_BASE/prov-shared.nq"
```

---

## 5. Files to create / modify

| File | Action |
|---|---|
| `scripts/transform/prescan.py` | **Create** — single-pass prescan: PROV-O node extraction, `prov.duckdb` + `prov-shared.nq` writes, `concept_labels.duckdb` + `agent_labels.duckdb` writes, per-sector Parquet build |
| `scripts/transform/merge_parquet.py` | **Create** — reads per-sector Parquet files from `--indir`, concatenates into one file at `--out` (pyarrow `ParquetWriter`) |
| `scripts/transform/__main__.py` | **Modify** — read-only `prov.duckdb` load at startup, remove write-back block and `entities_conn` variable |
| `scripts/run_gemea_transform.sh` | **Modify** — add prescan phase (§4.1), pass `--prov-db` to all transform workers (§4.2), include `prov-shared.nq` in Phase 4 NT merge (§4.3), update `--new` wipe (§4.4) |
| `gemea/scripts/py/export_ddb.py` | **Modify** — full schema update per §2.3 and §2.4 |
| `gemea/scripts/py/export_ddb_parquet.py` | **Modify** — same schema update per §2.3 and §2.4 |

---

## 6. Tests to add

- `test_prescan_prov.py`: mock SQLite with 3 records sharing one XSLT version and two
  providers; assert `prov.duckdb` (`prov_entities`) has exactly 4 rows (xslt×1,
  provider×2, ddb×1); assert `prov-shared.nq` line count matches expected triple count;
  assert Parquet row count = 3.

- `test_prescan_concept_labels.py`: record with two `dcType` values — one URI resolving
  via same-record Concept block, one Wikidata URI without a matching Concept entry;
  assert `concept_labels.duckdb` has 1 row (the unresolved URI with `NULL`); assert
  `dc_type` in Parquet is `[{name: "Gemälde", is_ext_uri: True}]` (length 1, not 2).

- `test_prescan_agent_labels.py`: record with one `dc:creator` carrying a GND URI and
  inline label; assert `agent_labels.duckdb` has 1 row with that URI and label; assert
  `agents` list in Parquet has one struct `{name=<label>, type="creation", is_ext_uri=True}`.

- `test_agents_struct.py`: record with a creator (GND URI + label), a contributor (bare
  string, no URI), and a LIDO photography-event participant; assert `agents` list has 3
  structs with `type` values `"creation"`, `"contribution"`, and the LIDO photography
  label; assert `is_ext_uri` is `True` for the GND entry and `False` for the bare string.

- `test_dates_struct.py`: record with a `dc_created` TimeSpan (begin=end → point-in-time),
  a `dc_issued` value, and a bare `dc_date` with no LIDO event; assert `dates` list has 3
  structs with `type` values `"creation"`, `"publication"`, `"unknown_event"`; assert
  point-in-time struct has `value` set and `begin`/`end` null; assert a range TimeSpan
  (begin≠end) has `value` null and `begin`/`end` set.

- `test_lang_split.py`: record with a French-tagged title (`@xml:lang="fre"`) and
  `dc:language="ger"`; assert `lang_title="fre"` and `lang_obj="ger"` in the Parquet row.

- `test_sector_mediatype_int.py`: record whose Concept block contains a `sparte006` URI
  and a `mt002` URI; assert `sector=6` (int) and `mediatype=2` (int) in Parquet row.

- `test_dc_type_list.py`: assert `extract_record` returns a `list` of `CONCEPT_STRUCT`
  dicts for `dc_type`; two `dcType` literal values → `[{name, is_ext_uri: False}, ...]`
  of length 2.
