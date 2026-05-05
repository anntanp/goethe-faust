#!/usr/bin/env python3
"""
Purpose:   Resolve werk_staging CHOs to GND Werk authority records; emit WEMI triples.
Usage:     python link_gnd_works.py \
               --staging output/goethe-faust-werk-staging.duckdb \
               --out     output/goethe-faust-work.nq \
               [--endpoint https://gnd.ise.fiz-karlsruhe.de/sparql] \
               [--limit N] [--stats json|none]
Inputs:    werk_staging DuckDB table (written by transform_edm_to_mocho.py)
Outputs:   goethe-faust-work.nq  — N-Quads for graph/work
           werk_staging updated:  status / gnd_uri / confidence / prov_lm columns
           werk_attempts:         append-only attempt log
Dependencies: duckdb
Assumptions: GND SPARQL endpoint uses a self-signed TLS cert (SSL verification disabled).
             creator_uris in staging use http:// — normalized to https:// for GND lookups.
             ql:contains-word FTS not available on this GND endpoint; FILTER(CONTAINS) used.
"""

import argparse
import hashlib
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

import duckdb

# ── Constants ──────────────────────────────────────────────────────────────────

GRAPH_WORK   = "https://gemea.ise.fiz-karlsruhe.de/graph/work"
WORK_BASE    = "https://gemea.ise.fiz-karlsruhe.de/work/"
GND_BASE_OLD = "http://d-nb.info/gnd/"
GND_BASE_NEW = "https://d-nb.info/gnd/"

# rdac / mo target_class URI → GND class URI
TARGET_CLASS_TO_GND = {
    "http://rdaregistry.info/Elements/c/C10001":    "https://d-nb.info/standards/elementset/gnd#Work",
    "http://purl.org/ontology/mo/MusicalWork":      "https://d-nb.info/standards/elementset/gnd#MusicalWork",
}

# Creator predicate per GND class
CREATOR_PRED = {
    "https://d-nb.info/standards/elementset/gnd#Work":        "https://d-nb.info/standards/elementset/gnd#firstAuthor",
    "https://d-nb.info/standards/elementset/gnd#MusicalWork":  "https://d-nb.info/standards/elementset/gnd#firstComposer",
}

MOCHO_NS     = "https://gemea.ise.fiz-karlsruhe.de/ontology/mocho#"
RDF_TYPE     = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
SKOS_EXACT   = "http://www.w3.org/2004/02/skos/core#exactMatch"

# ── SSL context (self-signed cert on GND endpoint) ─────────────────────────────

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# ── Script SHA-256 (for prov_lm) ───────────────────────────────────────────────

def _script_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

_SCRIPT_SHA = _script_sha256()

# ── SPARQL helpers ─────────────────────────────────────────────────────────────

def _sparql_escape(s: str) -> str:
    """Escape a string for use inside a SPARQL double-quoted literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def sparql_query(endpoint: str, query: str, timeout: int = 30) -> list[dict]:
    """Execute a SPARQL SELECT and return bindings list."""
    params = urllib.parse.urlencode({
        "query":  query,
        "format": "application/sparql-results+json",
    })
    req = urllib.request.Request(
        f"{endpoint}?{params}",
        headers={"Accept": "application/sparql-results+json"},
    )
    with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as resp:
        data = json.load(resp)
    return data["results"]["bindings"]


def _normalize_creator_uri(uri: str) -> str:
    """Convert http://d-nb.info/gnd/… → https://d-nb.info/gnd/…"""
    if uri.startswith(GND_BASE_OLD):
        return GND_BASE_NEW + uri[len(GND_BASE_OLD):]
    return uri


# ── ISBD title stripping (Pass 2) ──────────────────────────────────────────────

_ISBD_VOLUME = re.compile(
    r"\s+(Bd\.|Teil|Heft|Nr\.)\s*\d.*$", re.IGNORECASE
)


def isbd_strip(title: str) -> str:
    """Return title_proper by stripping ISBD-standard non-title elements."""
    for sep in (" . -", " : ", " / "):
        if sep in title:
            title = title.split(sep, 1)[0]
    title = _ISBD_VOLUME.sub("", title)
    return title.strip()


# ── GND Werk lookup ────────────────────────────────────────────────────────────

def lookup_gnd_werk(
    endpoint: str,
    title: str,
    gnd_class: str,
    creator_uris: list[str],
) -> list[str]:
    """
    Return a list of matching GND Werk URIs for the given title and class.
    Uses CONTAINS(LCASE) for flexible matching; confirms exact match in Python.
    Creator URIs (if any) narrow the query via the class-appropriate predicate.
    """
    if not title.strip():
        return []

    esc_title  = _sparql_escape(title)
    norm_uris  = [_normalize_creator_uri(u) for u in creator_uris]
    creator_pred = CREATOR_PRED.get(gnd_class, CREATOR_PRED[
        "https://d-nb.info/standards/elementset/gnd#Work"
    ])

    creator_clause = ""
    if norm_uris:
        # Use the first URI; additional URIs as UNION would be verbose — first hit is enough
        creator_clause = f'?werk <{creator_pred}> <{norm_uris[0]}> .'

    query = f"""
PREFIX gndo: <https://d-nb.info/standards/elementset/gnd#>
SELECT ?werk ?prefName WHERE {{
  ?werk a <{gnd_class}> ;
        gndo:preferredNameForTheWork ?prefName .
  {creator_clause}
  FILTER(CONTAINS(LCASE(STR(?prefName)), LCASE("{esc_title}")))
}}
LIMIT 20
"""
    bindings = sparql_query(endpoint, query)

    title_lower = title.strip().lower()
    return [
        b["werk"]["value"]
        for b in bindings
        if b["prefName"]["value"].strip().lower() == title_lower
    ]


# ── Work URI minting ───────────────────────────────────────────────────────────

def mint_work_uri(cho_uri: str) -> str:
    uid = uuid.uuid5(uuid.NAMESPACE_URL, cho_uri)
    return WORK_BASE + str(uid)


# ── N-Quads helpers ────────────────────────────────────────────────────────────

def _iri(uri: str) -> str:
    return f"<{uri}>"


def nquad(s: str, p: str, o: str, g: str) -> str:
    return f"{_iri(s)} {_iri(p)} {_iri(o)} {_iri(g)} .\n"


def emit_stub(work_uri: str, cho_uri: str, gnd_class: str, graph: str) -> list[str]:
    lines = [
        nquad(work_uri, RDF_TYPE, gnd_class, graph),
        nquad(work_uri, f"{MOCHO_NS}hasManifestation", cho_uri, graph),
        nquad(cho_uri,  f"{MOCHO_NS}isManifestationOf", work_uri, graph),
    ]
    return lines


def emit_resolved(work_uri: str, cho_uri: str, gnd_uri: str, gnd_class: str, graph: str) -> list[str]:
    lines = emit_stub(work_uri, cho_uri, gnd_class, graph)
    lines.append(nquad(work_uri, SKOS_EXACT, gnd_uri, graph))
    return lines


# ── DuckDB schema migration ────────────────────────────────────────────────────

def ensure_schema(con: duckdb.DuckDBPyConnection) -> None:
    for col, dtype in [
        ("status",     "VARCHAR"),
        ("gnd_uri",    "VARCHAR"),
        ("confidence", "FLOAT"),
        ("prov_lm",    "JSON"),
    ]:
        try:
            con.execute(f"ALTER TABLE werk_staging ADD COLUMN {col} {dtype}")
        except duckdb.CatalogException:
            pass  # column already exists

    con.execute("UPDATE werk_staging SET status = 'pending' WHERE status IS NULL")

    con.execute("""
        CREATE TABLE IF NOT EXISTS werk_attempts (
            ddb_obj_id   VARCHAR,
            attempt_no   INTEGER,
            status       VARCHAR,
            gnd_uri      VARCHAR,
            confidence   FLOAT,
            duration_ms  INTEGER,
            prov_lm      JSON,
            PRIMARY KEY (ddb_obj_id, attempt_no)
        )
    """)


def next_attempt_no(con: duckdb.DuckDBPyConnection, ddb_obj_id: str) -> int:
    row = con.execute(
        "SELECT COALESCE(MAX(attempt_no), 0) + 1 FROM werk_attempts WHERE ddb_obj_id = ?",
        [ddb_obj_id],
    ).fetchone()
    return row[0]


# ── Core linking logic ─────────────────────────────────────────────────────────

def process_row(
    con: duckdb.DuckDBPyConnection,
    row: dict,
    endpoint: str,
    nq_lines: list[str],
    ts: str,
) -> dict:
    """
    Run Pass 1 (raw title) then Pass 2 (ISBD-stripped) for one staging row.
    Returns a stats-update dict: {"resolved":0/1, "ambiguous":0/1, "unresolved":0/1}.
    """
    ddb_obj_id    = row["ddb_obj_id"]
    cho_uri       = row["cho_uri"]
    target_class  = row["target_class"]
    dc_title      = row["dc_title"] or ""
    creator_uris  = list(row["creator_uris"]) if row["creator_uris"] is not None else []

    gnd_class = TARGET_CLASS_TO_GND.get(
        target_class,
        "https://d-nb.info/standards/elementset/gnd#Work",
    )
    work_uri = mint_work_uri(cho_uri)

    attempt_no = next_attempt_no(con, ddb_obj_id)
    t_start = datetime.now(timezone.utc)

    def _prov(stage: str, pass_no: int) -> dict:
        return {
            "schema_version": "0.1",
            "stage":          stage,
            "pass":           pass_no,
            "method":         "contains+exact",
            "timestamp":      ts,
            "endpoint":       endpoint,
            "script":         "link_gnd_works.py",
            "script_sha256":  _SCRIPT_SHA,
            "model":          None,
            "model_version":  None,
            "score":          None,
            "duration_ms":    None,
        }

    def _elapsed_ms() -> int:
        return int((datetime.now(timezone.utc) - t_start).total_seconds() * 1000)

    def _update_staging(status: str, gnd_uri, confidence, prov: dict) -> None:
        prov["duration_ms"] = _elapsed_ms()
        con.execute(
            """UPDATE werk_staging
               SET status = ?, gnd_uri = ?, confidence = ?, prov_lm = ?
               WHERE ddb_obj_id = ?""",
            [status, gnd_uri, confidence, json.dumps(prov), ddb_obj_id],
        )

    def _log_attempt(status: str, gnd_uri, confidence, prov: dict) -> None:
        con.execute(
            """INSERT INTO werk_attempts
               (ddb_obj_id, attempt_no, status, gnd_uri, confidence, duration_ms, prov_lm)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                ddb_obj_id,
                attempt_no,
                status,
                gnd_uri,
                confidence,
                _elapsed_ms(),
                json.dumps(prov),
            ],
        )

    # Pass 1 — raw title
    prov1 = _prov("raw_fts_exact", 1)
    matches = lookup_gnd_werk(endpoint, dc_title, gnd_class, creator_uris)

    if len(matches) == 1:
        prov1["score"] = 1.0
        _update_staging("resolved", matches[0], 1.0, prov1)
        _log_attempt("resolved", matches[0], 1.0, prov1)
        nq_lines.extend(emit_resolved(work_uri, cho_uri, matches[0], gnd_class, GRAPH_WORK))
        return {"resolved": 1, "ambiguous": 0, "unresolved": 0}

    if len(matches) > 1:
        prov1["score"] = None
        _update_staging("ambiguous", None, None, prov1)
        _log_attempt("ambiguous", None, None, prov1)
        nq_lines.extend(emit_stub(work_uri, cho_uri, gnd_class, GRAPH_WORK))
        return {"resolved": 0, "ambiguous": 1, "unresolved": 0}

    # Pass 2 — ISBD-stripped title
    prov2 = _prov("isbd_fts_exact", 2)
    title_stripped = isbd_strip(dc_title)
    if title_stripped and title_stripped != dc_title:
        matches2 = lookup_gnd_werk(endpoint, title_stripped, gnd_class, creator_uris)
        if len(matches2) == 1:
            prov2["score"] = 0.9
            _update_staging("resolved", matches2[0], 0.9, prov2)
            _log_attempt("resolved", matches2[0], 0.9, prov2)
            nq_lines.extend(emit_resolved(work_uri, cho_uri, matches2[0], gnd_class, GRAPH_WORK))
            return {"resolved": 1, "ambiguous": 0, "unresolved": 0}

        if len(matches2) > 1:
            prov2["score"] = None
            _update_staging("ambiguous", None, None, prov2)
            _log_attempt("ambiguous", None, None, prov2)
            nq_lines.extend(emit_stub(work_uri, cho_uri, gnd_class, GRAPH_WORK))
            return {"resolved": 0, "ambiguous": 1, "unresolved": 0}

    # No match — stub
    prov2["score"] = 0.0
    _update_staging("unresolved", None, None, prov2)
    _log_attempt("unresolved", None, None, prov2)
    nq_lines.extend(emit_stub(work_uri, cho_uri, gnd_class, GRAPH_WORK))
    return {"resolved": 0, "ambiguous": 0, "unresolved": 1}


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GND Werk lookup for werk_staging rows.")
    p.add_argument("--staging",  required=True, help="Path to werk_staging DuckDB file")
    p.add_argument("--out",      required=True, help="Output N-Quads file path")
    p.add_argument("--endpoint", default="https://gnd.ise.fiz-karlsruhe.de/sparql")
    p.add_argument("--limit",    type=int, default=None, help="Process at most N rows")
    p.add_argument("--stats",    choices=["json", "none"], default="json")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    con = duckdb.connect(args.staging)
    ensure_schema(con)

    rows = con.execute(
        "SELECT * FROM werk_staging WHERE status IN ('pending', 'ambiguous', 'unresolved')"
        + (f" LIMIT {args.limit}" if args.limit else "")
    ).fetchdf().to_dict("records")

    nq_lines: list[str] = []
    totals = {"resolved": 0, "ambiguous": 0, "unresolved": 0}

    for row in rows:
        result = process_row(con, row, args.endpoint, nq_lines, ts)
        for k in totals:
            totals[k] += result[k]
        label = "resolved" if result["resolved"] else ("ambiguous" if result["ambiguous"] else "unresolved")
        print(f"  {row['ddb_obj_id'][:20]}  {label}  {row['dc_title'][:60]}", file=sys.stderr)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(nq_lines)

    con.close()

    if args.stats == "json":
        totals["total"] = sum(totals[k] for k in ("resolved", "ambiguous", "unresolved"))
        totals["resolution_rate"] = (
            round(totals["resolved"] / totals["total"], 4) if totals["total"] else 0.0
        )
        print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
