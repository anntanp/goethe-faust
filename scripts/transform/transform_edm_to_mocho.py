#!/usr/bin/env python3
"""
Purpose:    Transform DDB-EDM JSONL records to mocho-aligned N-Quads.
            Produces four named-graph streams: ddbedm (verbatim EDM passthrough),
            mocho (mocho-aligned triples), prov (PROV-O Layer 1), and a DuckDB
            werk_staging table for GND Werk linking (link_gnd_works.py, Phase 0).
            Reference implementation for the mocho ingest pipeline.
            Decisions: transform-adr.md D11/D15/D17, transform-script-adr.md D1–D27.
Usage:      python transform_edm_to_mocho.py
                [--jsonl FILE] [--ids FILE]
                [--outdir DIR]
                [--stats LEVEL] [--log-level LEVEL]
                [--workers N] [--batch-size N] [--ids -] [--limit N]
                [--debug]
Inputs:     data/items-all-goethe-faust.json              JSONL, one record per line
            data/ids-all-goethe-faust.txt                  32-char object IDs, one per line
            output/config/lookup_class_prop_alignment.csv  (target_class, edm_prop) → target_prop
            output/config/lido_event_types.csv             lido_uri → agent predicates per WEMI
            output/config/lookup_htype_doco_rico.csv       htype_code → (rdf_type, rst_iris)
            output/config/lookup_mediatype_class.csv       (sparte, mediatype) → class dispatch row
            output/config/audio_type2class.json            mt001 dc:type → group (A/B/C)
Outputs:    output/transform/YYYYMMDD_HHMMSS/               run directory (one per invocation)
              goethe-faust.nq                              combined N-Quads (all named graphs)
              goethe-faust-werk-staging.duckdb             W-slot staging rows
              transform_stats.json                         run statistics
              transform_errors.jsonl                       per-record errors
              transform.log                                run log
Deps:       stdlib only + duckdb (pip install duckdb)
Assumes:    JSONL: one JSON object per line; record structure edm.RDF.*
            All config CSVs present at output/config/; see notes/transform-implementation-plan.md
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
import traceback
from collections import Counter
from datetime import datetime
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parents[1]   # scripts/transform/ → scripts/ → project root

DEFAULT_JSONL        = PROJECT_DIR / "data"   / "items-all-goethe-faust.json"
DEFAULT_IDS          = PROJECT_DIR / "data"   / "ids-all-goethe-faust.txt"
DEFAULT_ALIGNMENT    = PROJECT_DIR / "output" / "config" / "lookup_class_prop_alignment.csv"
DEFAULT_LIDO         = PROJECT_DIR / "output" / "config" / "lido_event_types.csv"
DEFAULT_HTYPE        = PROJECT_DIR / "output" / "config" / "lookup_htype_doco_rico.csv"
DEFAULT_MEDIATYPE    = PROJECT_DIR / "output" / "config" / "lookup_mediatype_class.csv"
DEFAULT_AUDIO        = PROJECT_DIR / "output" / "config" / "audio_type2class.json"
DEFAULT_OUTPUT_BASE  = PROJECT_DIR / "output" / "transform"

# ─── Constants ────────────────────────────────────────────────────────────────

# Named graph IRIs (D20)
GRAPH_DDBEDM = "https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm"
GRAPH_MOCHO  = "https://gemea.ise.fiz-karlsruhe.de/graph/mocho"
GRAPH_PROV   = "https://gemea.ise.fiz-karlsruhe.de/graph/prov"

# CHO URI bases (D22, D27)
GEMEA_BASE    = "https://gemea.ise.fiz-karlsruhe.de/mocho/"
DDB_ITEM_BASE = "http://www.deutsche-digitale-bibliothek.de/item/"
DDB_BASE      = "http://www.deutsche-digitale-bibliothek.de"
DDB_API_BASE  = "https://api.deutsche-digitale-bibliothek.de/2/"

# Vocnet prefixes for mediatype/sector extraction
_MEDIATYPE_PREFIX = "http://ddb.vocnet.org/medientyp/"
_SECTOR_PREFIX    = "http://ddb.vocnet.org/sparte/"
MT007_IRI         = "http://ddb.vocnet.org/medientyp/mt007"

# Ontology IRIs
RDF_TYPE        = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
RDFS_LABEL      = "http://www.w3.org/2000/01/rdf-schema#label"
OWL_SAMEAS      = "http://www.w3.org/2002/07/owl#sameAs"
SKOS_PREF_LABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
SKOS_CONCEPT    = "http://www.w3.org/2004/02/skos/core#Concept"
DCTERMS_SOURCE  = "http://purl.org/dc/terms/source"
FOAF_THUMBNAIL  = "http://xmlns.com/foaf/0.1/thumbnail"
FOAF_ORG        = "http://xmlns.com/foaf/0.1/Organization"
FOAF_NAME       = "http://xmlns.com/foaf/0.1/name"
EDM_DATA_PROVIDER = "http://www.europeana.eu/schemas/edm/dataProvider"
SCHEMA_URL      = "https://schema.org/url"
MOCHO_ISIL      = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#isil"
MOCHO_NS        = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#"
MOCHO_AGENT     = MOCHO_NS + "Agent"
RICO_HAS_RST    = "http://www.ica.org/standards/RiC/ontology#hasRecordSetType"

# PROV-O (D11)
PROV_ENTITY     = "http://www.w3.org/ns/prov#Entity"
PROV_AGENT      = "http://www.w3.org/ns/prov#Agent"
PROV_SW_AGENT   = "http://www.w3.org/ns/prov#SoftwareAgent"
PROV_DERIVED    = "http://www.w3.org/ns/prov#wasDerivedFrom"
PROV_ATTRIBUTED = "http://www.w3.org/ns/prov#wasAttributedTo"
PROV_GEN_TIME   = "http://www.w3.org/ns/prov#generatedAtTime"
PROV_ON_BEHALF  = "http://www.w3.org/ns/prov#actedOnBehalfOf"
DCAT_DATASET    = "http://www.w3.org/ns/dcat#Dataset"
DCTERMS_ID      = "http://purl.org/dc/terms/identifier"
DCTERMS_TYPE    = "http://purl.org/dc/terms/type"
DCTERMS_HAS_VER = "http://purl.org/dc/terms/hasVersion"
DCTERMS_REF     = "http://purl.org/dc/terms/references"
DCTERMS_RIGHTS  = "http://purl.org/dc/terms/rights"
DC_ID           = "http://purl.org/dc/elements/1.1/identifier"
DC_TITLE        = "http://purl.org/dc/elements/1.1/title"
DC_DESCRIPTION  = "http://purl.org/dc/elements/1.1/description"

# Subject keys (ADR D1)
SUBJECT_KEYS = frozenset({"dcSubject", "dcTermsSubject", "dcTermSubject"})

# Properties skipped in the mocho property loop (handled elsewhere or structural)
_MOCHO_SKIP = frozenset({
    "about", "hierarchyType",
    "creator", "contributor",
    "dcSubject", "dcTermsSubject", "dcTermSubject",
    "dcType",
    "aggregationEntity", "hierarchyPosition",
})

# ─── Prefix table for CURIE expansion ─────────────────────────────────────────

_PREFIXES = {
    "rdam":    "http://rdaregistry.info/Elements/m/",
    "rdaw":    "http://rdaregistry.info/Elements/w/",
    "rdae":    "http://rdaregistry.info/Elements/e/",
    "rdac":    "http://rdaregistry.info/Elements/c/",
    "rdact":   "http://rdaregistry.info/termList/RDACarrierType/",
    "dc":      "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "vra":     "http://purl.org/vra/",
    "rico":    "http://www.ica.org/standards/RiC/ontology#",
    "ric-rst": "http://www.ica.org/standards/RiC/vocabularies/recordSetTypes#",
    "skos":    "http://www.w3.org/2004/02/skos/core#",
    "owl":     "http://www.w3.org/2002/07/owl#",
    "rdfs":    "http://www.w3.org/2000/01/rdf-schema#",
    "foaf":    "http://xmlns.com/foaf/0.1/",
    "edm":     "http://www.europeana.eu/schemas/edm/",
    "mo":      "http://purl.org/ontology/mo/",
    "aco":     "https://w3id.org/ac-ontology/aco#",
    "ec":      "http://www.ebu.ch/metadata/ontologies/ebucoreplus#",
    "doco":    "http://purl.org/spar/doco/",
    "mocho":   MOCHO_NS,
    "gndo":    "https://d-nb.info/standards/elementset/gnd#",
    "ddb":     "http://www.deutsche-digitale-bibliothek.de/",
}

# EDM entity type → rdf:type IRI (for ddbedm passthrough stream)
_EDM_ENTITY_TYPES = {
    "ProvidedCHO": "http://www.europeana.eu/schemas/edm/ProvidedCHO",
    "Agent":       "http://www.europeana.eu/schemas/edm/Agent",
    "Place":       "http://www.europeana.eu/schemas/edm/Place",
    "TimeSpan":    "http://www.europeana.eu/schemas/edm/TimeSpan",
    "WebResource": "http://www.europeana.eu/schemas/edm/WebResource",
    "Aggregation": "http://www.openarchives.org/ore/terms/Aggregation",
    "Concept":     "http://www.w3.org/2004/02/skos/core#Concept",
    "PhysicalThing": "http://www.europeana.eu/schemas/edm/PhysicalThing",
    "Event":       "http://www.europeana.eu/schemas/edm/Event",
}

# ─── Utility functions ────────────────────────────────────────────────────────

NQuad     = str
NQList    = list[NQuad]
PropAlign = dict[tuple[str, str], str]   # (target_class, edm_prop) → target_prop_iri
AgentDict = dict[str, object]


def make_nq(s_nt: str, p_nt: str, o_nt: str, graph_iri: str) -> NQuad:
    """Return one N-Quads line."""
    return f"{s_nt} {p_nt} {o_nt} <{graph_iri}> ."


def coerce_list(val: object) -> list:
    """Normalise None/dict/list to a list."""
    if val is None:
        return []
    if isinstance(val, dict):
        return [val]
    if isinstance(val, list):
        return val
    return []


def _expand_prefix(curie: str) -> str:
    """Expand a CURIE (e.g. 'rdam:P30134') to a full IRI."""
    for prefix, base in _PREFIXES.items():
        if curie.startswith(prefix + ":"):
            return base + curie[len(prefix) + 1:]
    return curie


def _to_curie(iri: str) -> str:
    """Collapse a full IRI to a CURIE using _PREFIXES; return IRI unchanged if no match."""
    for prefix, base in _PREFIXES.items():
        if iri.startswith(base):
            return f"{prefix}:{iri[len(base):]}"
    return iri


# Regex to extract the predicate IRI from an N-Quad line.
# N-Quad format: <subject> <predicate> <object> <graph> .
# Subject is always <iri> in our output (no blank nodes on CHO).
_NQ_PRED_RE = re.compile(r"^<[^>]+> <([^>]+)>")

# Namespaces introduced by mocho alignment — not present in the DDB-EDM source.
_NEW_NS: tuple[str, ...] = (
    "http://rdaregistry.info/Elements/",   # rdam, rdaw, rdae, rdac
    "http://www.ica.org/standards/RiC/",   # rico, ric-rst
    MOCHO_NS,
    "http://purl.org/vra/",
    "http://purl.org/ontology/mo/",
    "https://w3id.org/ac-ontology/",
    "http://www.ebu.ch/metadata/ontologies/ebucoreplus#",
    "http://purl.org/spar/doco/",
)


def mint_cho_uri(obj_id: str) -> str:
    """Return the minted GeMeA mocho CHO URI for a 32-char DDB object ID (D22)."""
    return GEMEA_BASE + obj_id


def mint_bare_id(entity_class: str, raw_id: str) -> str:
    """Expand a bare 32-char ID to a full URI (D27).

    ProvidedCHO bare IDs → DDB item URI.
    All other entity types → urn:ddbedm:<ClassName>:<id>.
    Full URIs and URNs are returned unchanged.
    """
    if raw_id.startswith(("http", "urn")):
        return raw_id
    if entity_class == "ProvidedCHO":
        return DDB_ITEM_BASE + raw_id
    return f"urn:ddbedm:{entity_class}:{raw_id}"


def _escape_literal(s: str) -> str:
    """Escape backslash and double-quote for N-Triples/N-Quads literal content."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def value_to_nt_obj(val: object) -> list[str]:
    """Convert a JSONL field value to a list of N-Triples object strings.

    Handles all value shapes produced by the DDB EDM JSONL:
      None / ""                    → []
      str (non-empty)              → ['"escaped"']
      list                         → recurse and flatten
      {"resource": IRI}            → ["<IRI>"]
      {"lang": L, "$": T}          → ['"T"@L']
      {"lang": null, "$": T}       → ['"T"']
      {"resource": null, "$": ""}  → []
    """
    if val is None:
        return []
    if isinstance(val, str):
        return [f'"{_escape_literal(val)}"'] if val else []
    if isinstance(val, list):
        result = []
        for item in val:
            result.extend(value_to_nt_obj(item))
        return result
    if isinstance(val, dict):
        resource = val.get("resource")
        if resource:
            return [f"<{resource}>"]
        text = val.get("$", "")
        if not text:
            return []
        escaped = _escape_literal(str(text))
        lang = val.get("lang")
        if lang:
            return [f'"{escaped}"@{lang}']
        return [f'"{escaped}"']
    return []


def normalize_date(s: str) -> list[str]:
    """Normalise a dc:date string to ISO 8601.

    8-digit compact YYYYMMDD → YYYY-MM-DD.
    ISO interval begin/end → [begin, end].
    All other values returned unchanged.
    """
    s = s.strip()
    if "/" in s:
        parts = s.split("/", 1)
        return [normalize_date(p)[0] for p in parts]
    if len(s) == 8 and s.isdigit():
        return [f"{s[:4]}-{s[4:6]}-{s[6:]}"]
    return [s]


def is_ddb_or_gnd(uri: str) -> bool:
    """True if URI is a DDB organization or GND authority URI."""
    return uri.startswith((
        "http://www.deutsche-digitale-bibliothek.de/organization/",
        "http://d-nb.info/gnd/",
        "https://d-nb.info/gnd/",
    ))


def resolve_agent(
    label: str,
    resource: str,
    agents_index: dict[str, AgentDict],
) -> AgentDict | None:
    """Resolve a creator/contributor to an Agent dict.

    URI match preferred; label match fallback.
    Returns None if no match found.
    """
    if resource and resource in agents_index:
        return agents_index[resource]
    if label and label in agents_index:
        return agents_index[label]
    return None


def _extract_mediatype_sector(concepts: object) -> tuple[str, str]:
    """Return (mediatype_iri, sector_iri) from the record's Concept list."""
    mediatype = "any"
    sector    = "any"
    for c in coerce_list(concepts):
        if not isinstance(c, dict):
            continue
        about = c.get("about") or ""
        if about.startswith(_MEDIATYPE_PREFIX):
            mediatype = about
        elif about.startswith(_SECTOR_PREFIX):
            sector = about
    return mediatype, sector


def get_object_id(record: dict) -> str | None:
    """Extract 32-char object ID from ProvidedCHO.about URI. Returns None on failure."""
    try:
        about = record["edm"]["RDF"]["ProvidedCHO"]["about"]
    except (KeyError, TypeError):
        return None
    if not about:
        return None
    # Bare 32-char ID (D27)
    if len(about) == 32 and not about.startswith("http"):
        return about
    obj_id = about.rstrip("/").rsplit("/", 1)[-1]
    return obj_id if len(obj_id) == 32 else None


# ─── Loaders ──────────────────────────────────────────────────────────────────

def load_ids(path: Path) -> set[str]:
    """Load ids-all-goethe-faust.txt. Returns set of 32-char object IDs."""
    with open(path, encoding="utf-8") as fh:
        return {line.strip() for line in fh if line.strip()}


def load_htype_map(path: Path) -> dict[str, tuple[list[str], list[str]]]:
    """Load lookup_htype_doco_rico.csv.

    Returns dict[htype_code] → ([rdf_type_iri, ...], [rst_iri, ...]).
    rdf_type may be comma-separated (e.g. 'doco:Section, rdac:C10007').
    Rows where all rdf_types are 'pending' or empty are excluded.
    """
    result: dict = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            type_iris: list[str] = []
            for part in (row.get("rdf_type", "") or "").split(","):
                part = part.strip()
                if part and part != "pending":
                    type_iris.append(_expand_prefix(part))
            if not type_iris:
                continue
            rst_iris: list[str] = []
            for part in (row.get("has_record_set_type", "") or "").split(","):
                part = part.strip()
                if part:
                    rst_iris.append(_expand_prefix(part))
            result[row["htype_code"].strip()] = (type_iris, rst_iris)
    return result


def load_mediatype_class(path: Path) -> dict[tuple[str, str], dict]:
    """Load lookup_mediatype_class.csv.

    Returns dict[(sparte_iri, mediatype_iri)] → row dict with keys:
      use_htype (bool), rdf_type_w (str), rdf_type_m (str).
    CURIEs in rdf_type_w/rdf_type_m are expanded to full IRIs.
    """
    result: dict = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["sparte"].strip(), row["mediatype"].strip())
            result[key] = {
                "use_htype":  row["use_htype"].strip().lower() == "true",
                "rdf_type_w": _expand_prefix(row["rdf_type_w"].strip()),
                "rdf_type_m": _expand_prefix(row["rdf_type_m"].strip()),
            }
    return result


def load_class_prop_alignment(path: Path) -> PropAlign:
    """Load lookup_class_prop_alignment.csv.

    Returns dict[(target_class_curie, edm_prop_curie)] → target_prop_iri.
    Rows where target_prop is empty or 'N/A' are skipped.
    """
    result: PropAlign = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            target_prop = row.get("target_prop", "").strip()
            if not target_prop or target_prop in ("N/A", "TBD", "skip"):
                continue
            key = (
                _expand_prefix(row["target_class"].strip()),
                _expand_prefix(row["edm_prop"].strip()),
            )
            result[key] = _expand_prefix(target_prop)
    return result


def load_lido_event_types(path: Path) -> dict[str, dict[str, str]]:
    """Load lido_event_types.csv.

    Returns dict[lido_uri] → {col_name: expanded_iri}.
    Columns of interest: rdam_agent_prop, rdaw_agent_prop,
    vra_image_agent_prop, vra_work_agent_prop, rico_agent_prop, dc_agent_fallback.
    """
    cols = [
        "rdam_agent_prop", "rdaw_agent_prop",
        "vra_image_agent_prop", "vra_work_agent_prop",
        "rico_agent_prop", "dc_agent_fallback",
    ]
    result: dict = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            uri = row.get("resource", "").strip()
            if not uri:
                continue
            result[uri] = {
                col: _expand_prefix(row.get(col, "").strip())
                for col in cols
            }
    return result


def load_audio_type2class(path: Path) -> dict[tuple[str, str], str]:
    """Load audio_type2class.json.

    Returns dict[(sector_iri, dc_type_de)] → group char ('A', 'B', or 'C').
    """
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    result: dict = {}
    for entry in raw if isinstance(raw, list) else raw.get("entries", []):
        sector   = entry.get("sector", "").strip()
        dc_type  = entry.get("dc_type_de", "").strip()
        group    = entry.get("group", "").strip()
        if sector and dc_type and group:
            result[(sector, dc_type)] = group
    return result


# ─── Additional constants ─────────────────────────────────────────────────────

DCTERMS_CREATOR = "http://purl.org/dc/terms/creator"
DC_CONTRIBUTOR  = "http://purl.org/dc/elements/1.1/contributor"
DC_SUBJECT      = "http://purl.org/dc/elements/1.1/subject"
DCTERMS_SUBJECT = "http://purl.org/dc/terms/subject"
XSD_DATETIME    = "http://www.w3.org/2001/XMLSchema#dateTime"
EDM_NS          = "http://www.europeana.eu/schemas/edm/"
GNDO_NS         = "https://d-nb.info/standards/elementset/gnd#"
CIDOC_NS        = "http://www.cidoc-crm.org/cidoc-crm/"

# W-slot classes that trigger a werk_staging row (D26)
_W_SLOT_CLASSES: frozenset[str] = frozenset({
    "http://rdaregistry.info/Elements/c/C10001",  # rdac:C10001 Work
    "http://purl.org/ontology/mo/MusicalWork",    # mo:MusicalWork
})

# Primary WEMI level per class full IRI — used by contributor column selection
_CLASS_WEMI: dict[str, str] = {
    # W — Work
    "http://rdaregistry.info/Elements/c/C10001":                       "W",
    MOCHO_NS + "ImmovableWork":                                        "W",
    MOCHO_NS + "ImageWork":                                            "W",
    "http://purl.org/ontology/mo/MusicalWork":                         "W",
    "http://purl.org/vra/Work":                                        "W",
    "http://www.ebu.ch/metadata/ontologies/ebucoreplus#EditorialWork":  "W",
    # M — Manifestation
    "http://rdaregistry.info/Elements/c/C10007":                       "M",
    MOCHO_NS + "Manifestation":                                        "M",
    MOCHO_NS + "ImageManifestation":                                   "M",
    "https://w3id.org/ac-ontology/aco#AudioManifestation":             "M",
    "http://purl.org/ontology/mo/MusicalManifestation":                "M",
    "http://www.ebu.ch/metadata/ontologies/ebucoreplus#MediaResource":  "M",
    "http://purl.org/vra/Image":                                       "M",
    # doco fragment types (Manifestation-level document parts)
    "http://purl.org/spar/doco/Section":         "M",
    "http://purl.org/spar/doco/Appendix":        "M",
    "http://purl.org/spar/doco/Part":            "M",
    "http://purl.org/spar/doco/Chapter":         "M",
    "http://purl.org/spar/doco/Figure":          "M",
    "http://purl.org/spar/doco/Index":           "M",
    "http://purl.org/spar/doco/TableOfContents": "M",
    "http://purl.org/spar/doco/TextChunk":       "M",
    "http://purl.org/spar/doco/Stanza":          "M",
    "http://purl.org/spar/doco/Preface":         "M",
    # RiC — no WEMI slot
    "http://www.ica.org/standards/RiC/ontology#RecordSet":  "",
    "http://www.ica.org/standards/RiC/ontology#Record":     "",
    "http://www.ica.org/standards/RiC/ontology#RecordPart": "",
}

# (wemi, target_class_full_iri) → lido_event_types.csv column name (D3/D25)
_CONTRIBUTOR_COL: dict[tuple[str, str], str] = {
    ("M", "http://rdaregistry.info/Elements/c/C10007"):        "rdam_agent_prop",
    ("M", MOCHO_NS + "Manifestation"):                         "rdam_agent_prop",
    ("W", "http://rdaregistry.info/Elements/c/C10001"):        "rdaw_agent_prop",
    ("M", "http://purl.org/vra/Image"):                        "vra_image_agent_prop",
    ("W", "http://purl.org/vra/Work"):                         "vra_work_agent_prop",
    ("",  "http://www.ica.org/standards/RiC/ontology#RecordSet"):  "rico_agent_prop",
    ("",  "http://www.ica.org/standards/RiC/ontology#Record"):     "rico_agent_prop",
    ("",  "http://www.ica.org/standards/RiC/ontology#RecordPart"): "rico_agent_prop",
}

# JSON key → predicate full IRI for ddbedm verbatim passthrough and mocho alignment lookup
_DDBEDM_PROP: dict[str, str] = {
    # DC elements 1.1
    "title":               "http://purl.org/dc/elements/1.1/title",
    "creator":             "http://purl.org/dc/elements/1.1/creator",
    "contributor":         "http://purl.org/dc/elements/1.1/contributor",
    "date":                "http://purl.org/dc/elements/1.1/date",
    "description":         "http://purl.org/dc/elements/1.1/description",
    "format":              "http://purl.org/dc/elements/1.1/format",
    "identifier":          "http://purl.org/dc/elements/1.1/identifier",
    "language":            "http://purl.org/dc/elements/1.1/language",
    "publisher":           "http://purl.org/dc/elements/1.1/publisher",
    "relation":            "http://purl.org/dc/elements/1.1/relation",
    "rights":              "http://purl.org/dc/elements/1.1/rights",
    "source":              "http://purl.org/dc/elements/1.1/source",
    "coverage":            "http://purl.org/dc/elements/1.1/coverage",
    "dcSubject":           "http://purl.org/dc/elements/1.1/subject",
    "dcType":              "http://purl.org/dc/elements/1.1/type",
    # DC terms
    "alternative":         "http://purl.org/dc/terms/alternative",
    "dcTermsSubject":      "http://purl.org/dc/terms/subject",
    "dcTermSubject":       "http://purl.org/dc/terms/subject",  # corpus typo variant
    "dcTermsLanguage":     "http://purl.org/dc/terms/language",
    "isPartOf":            "http://purl.org/dc/terms/isPartOf",
    "issued":              "http://purl.org/dc/terms/issued",
    "extent":              "http://purl.org/dc/terms/extent",
    "medium":              "http://purl.org/dc/terms/medium",
    "tableOfContents":     "http://purl.org/dc/terms/tableOfContents",
    "hasPart":             "http://purl.org/dc/terms/hasPart",
    "spatial":             "http://purl.org/dc/terms/spatial",
    "dcTermsRights":       "http://purl.org/dc/terms/rights",
    # EDM
    "currentLocation":     EDM_NS + "currentLocation",
    "hasMet":              EDM_NS + "hasMet",
    "hasType":             EDM_NS + "hasType",
    "isNextInSequence":    EDM_NS + "isNextInSequence",
    "isShownAt":           EDM_NS + "isShownAt",
    "isShownBy":           EDM_NS + "isShownBy",
    "wasPresentAt":        EDM_NS + "wasPresentAt",
    "isRelatedTo":         EDM_NS + "isRelatedTo",
    "edmType":             EDM_NS + "type",
    "object":              EDM_NS + "object",
    "aggregatedCHO":       EDM_NS + "aggregatedCHO",
    "aggregator":          EDM_NS + "aggregator",
    "dataProvider":        EDM_NS + "dataProvider",
    "edmRights":           EDM_NS + "rights",
    "provider":            EDM_NS + "provider",
    "hasView":             EDM_NS + "hasView",
    "begin":               EDM_NS + "begin",
    "end":                 EDM_NS + "end",
    "occurredAt":          EDM_NS + "occurredAt",
    "occuredAt":           EDM_NS + "occurredAt",  # typo variant in corpus
    "happenedAt":          EDM_NS + "happenedAt",
    # SKOS
    "prefLabel":           "http://www.w3.org/2004/02/skos/core#prefLabel",
    "altLabel":            "http://www.w3.org/2004/02/skos/core#altLabel",
    "note":                "http://www.w3.org/2004/02/skos/core#note",
    "notation":            "http://www.w3.org/2004/02/skos/core#notation",
    # RDF / OWL
    "type":                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
    "sameAs":              "http://www.w3.org/2002/07/owl#sameAs",
    # FOAF
    "name":                "http://xmlns.com/foaf/0.1/name",
    # GND
    "biographicalInformation": GNDO_NS + "biographicalInformation",
    "dateOfBirth":             GNDO_NS + "dateOfBirth",
    "dateOfDeath":             GNDO_NS + "dateOfDeath",
    "dateOfEstablishment":     GNDO_NS + "dateOfEstablishment",
    "dateOfTermination":       GNDO_NS + "dateOfTermination",
    "gender":                  GNDO_NS + "gender",
    "placeOfBirth":            GNDO_NS + "placeOfBirth",
    "placeOfDeath":            GNDO_NS + "placeOfDeath",
    "professionOrOccupation":  GNDO_NS + "professionOrOccupation",
    # CIDOC-CRM (LIDO events)
    "P11_had_participant": CIDOC_NS + "P11_had_participant",
    # DDB-internal structural fields (preserved in ddbedm, skipped in mocho)
    "hierarchyType":      "http://www.deutsche-digitale-bibliothek.de/hierarchyType",
    "hierarchyPosition":  "http://www.deutsche-digitale-bibliothek.de/hierarchyPosition",
    "aggregationEntity":  "http://www.deutsche-digitale-bibliothek.de/aggregationEntity",
}


# ─── Stream handlers ──────────────────────────────────────────────────────────

def emit_ddbedm_triples(rdf: dict, graph_iri: str) -> NQList:
    """Emit verbatim EDM passthrough triples for all entity types in rdf (§6.1).

    Subject: original entity['about'] URI. Includes mt007 records.
    """
    lines: NQList = []
    _skip = frozenset({"about"})
    for entity_type, entities in rdf.items():
        edm_class = _EDM_ENTITY_TYPES.get(entity_type)
        for entity in coerce_list(entities):
            if not isinstance(entity, dict):
                continue
            raw_about = (entity.get("about") or "").strip()
            if not raw_about:
                continue
            subj_uri = mint_bare_id(entity_type, raw_about)
            subj_nt  = f"<{subj_uri}>"
            if edm_class:
                lines.append(make_nq(subj_nt, f"<{RDF_TYPE}>", f"<{edm_class}>", graph_iri))
            for key, val in entity.items():
                if key in _skip:
                    continue
                pred_iri = _DDBEDM_PROP.get(key)
                if not pred_iri:
                    continue
                pred_nt = f"<{pred_iri}>"
                for obj_nt in value_to_nt_obj(val):
                    lines.append(make_nq(subj_nt, pred_nt, obj_nt, graph_iri))
    return lines


def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
    lines: NQList = []
    props = record.get("properties") or {}
    prov  = record.get("provider-info") or {}

    item_id         = (props.get("item-id")         or "").strip()
    dataset_id      = (props.get("dataset-id")      or "").strip()
    dataset_label   = (props.get("dataset-label")   or "").strip()
    revision        = (props.get("revision-id")     or "").strip()
    ingest_dt       = (props.get("ingest-date")     or "").strip()
    map_ver         = (props.get("mapping-version") or "").strip()
    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
    provider_name   = (prov.get("provider-name")    or "").strip()
    provider_uri    = (prov.get("provider-uri")     or "").strip()
    provider_id     = (prov.get("provider-id")      or "").strip()
    provider_isil   = (prov.get("provider-isil")    or "").strip()

    src_desc  = (record.get("source") or {}).get("description") or {}
    src_ref   = (src_desc.get("record") or {}) if isinstance(src_desc, dict) else {}
    ref_val   = (src_ref.get("ref",  "") or "").strip() if isinstance(src_ref, dict) else ""
    src_href  = (src_ref.get("href", "") or "").strip() if isinstance(src_ref, dict) else ""
    rec_type  = (src_ref.get("type", "") or "").strip() if isinstance(src_ref, dict) else ""

    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
               if provider_ddb_id else ""

    # ── CHO node ──────────────────────────────────────────────────────────────
    cho_nt = f"<{ddb_cho_uri}>"
    lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
    if ds_uri:
        lines.append(make_nq(cho_nt, f"<{PROV_DERIVED}>",   f"<{ds_uri}>",   graph_iri))
    if xslt_uri:
        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
    if ingest_dt:
        lines.append(make_nq(cho_nt, f"<{PROV_GEN_TIME}>",
                             f'"{_escape_literal(ingest_dt)}"^^<{XSD_DATETIME}>', graph_iri))
    if revision:
        lines.append(make_nq(cho_nt, f"<{DCTERMS_HAS_VER}>",
                             f'"{_escape_literal(revision)}"', graph_iri))
    if ref_val:
        lines.append(make_nq(cho_nt, f"<{DCTERMS_REF}>",
                             f'"ddb:{_escape_literal(ref_val)}"', graph_iri))

    # ── Dataset node ──────────────────────────────────────────────────────────
    if ds_uri:
        ds_nt = f"<{ds_uri}>"
        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{DCAT_DATASET}>", graph_iri))
        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
        lines.append(make_nq(ds_nt, f"<{DCTERMS_ID}>",
                             f'"{_escape_literal(dataset_id)}"', graph_iri))
        if dataset_label:
            lines.append(make_nq(ds_nt, f"<{RDFS_LABEL}>",
                                 f'"{_escape_literal(dataset_label)}"@de', graph_iri))
        if rec_type:
            lines.append(make_nq(ds_nt, f"<{DCTERMS_TYPE}>", f"<{rec_type}>", graph_iri))
        if prov_uri:
            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
                                 f"<{prov_uri}>", graph_iri))

    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────
    if xslt_uri:
        xslt_nt = f"<{xslt_uri}>"
        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
        lines.append(make_nq(xslt_nt, f"<{DCTERMS_HAS_VER}>",
                             f'"{_escape_literal(map_ver)}"', graph_iri))
        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))

    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────
    ddb_nt = f"<{DDB_BASE}>"
    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
    lines.append(make_nq(ddb_nt, f"<{FOAF_NAME}>",
                         '"Deutsche Digitale Bibliothek"', graph_iri))

    # ── Provider Agent node ───────────────────────────────────────────────────
    if prov_uri:
        prov_nt = f"<{prov_uri}>"
        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
        if provider_name:
            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
                                 f'"{_escape_literal(provider_name)}"', graph_iri))
        if provider_uri:
            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
        if provider_id:
            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
                                 f'"{_escape_literal(provider_id)}"', graph_iri))
        if provider_isil:
            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>", f"<{provider_isil}>", graph_iri))

    # ── SourceRecord node (one per binary entry under same URI) ───────────────
    if src_href:
        src_rec_uri = DDB_API_BASE + src_href.lstrip("/")
        src_nt      = f"<{src_rec_uri}>"
        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
        for binary in coerce_list((record.get("binaries") or {}).get("binary")):
            if not isinstance(binary, dict):
                continue
            ref   = (binary.get("ref")            or "").strip()
            name  = (binary.get("name")           or "").strip()
            name2 = (binary.get("name2")          or "").strip()
            kind  = (binary.get("kind")           or "").strip()
            lpath = (binary.get("local_pathname") or "").strip()
            if ref:
                lines.append(make_nq(src_nt, f"<{DC_ID}>",
                                     f'"{_escape_literal(ref)}"', graph_iri))
            if name:
                lines.append(make_nq(src_nt, f"<{DC_TITLE}>",
                                     f'"{_escape_literal(name)}"@de', graph_iri))
            desc = (name2 + " | " + name) if name2 and name else (name2 or name)
            if desc:
                lines.append(make_nq(src_nt, f"<{DC_DESCRIPTION}>",
                                     f'"{_escape_literal(desc)}"@de', graph_iri))
            if kind:
                lines.append(make_nq(src_nt, f"<{DCTERMS_RIGHTS}>", f"<{kind}>", graph_iri))
            if lpath and lpath.startswith("http"):
                lines.append(make_nq(src_nt, f"<{DCTERMS_SOURCE}>", f"<{lpath}>", graph_iri))

    return lines


def retype_entities(
    sector: str,
    mediatype: str,
    htype_code: str | None,
    dctype_vals: list,
    cho_nt: str,
    mediatype_class_map: dict,
    htype_map: dict,
    audio_type2class: dict,
    graph_iri: str,
) -> tuple[NQList, str, str, dict]:
    """Dispatch rdf:type triples for a ProvidedCHO (§6.4, transform-revised-plan.md §1.1).

    Returns (lines, target_class_full_iri, wemi, dispatch_flags).
    target_class is used for property alignment lookup; wemi for contributor column selection.
    dispatch_flags: {"htype_used": bool, "fallback": bool}
    """
    lines: NQList = []
    row = (
        mediatype_class_map.get((sector, mediatype))
        or mediatype_class_map.get(("any", "any"))
        or {}
    )
    use_htype  = row.get("use_htype", False)
    rdf_type_w = row.get("rdf_type_w", "")
    rdf_type_m = row.get("rdf_type_m", "")

    primary_class = ""
    htype_used    = False

    # Layer 1: htype-derived class (for htype-first strata)
    if use_htype and htype_code:
        entry = htype_map.get(htype_code)
        if entry:
            type_iris, rst_iris = entry
            for t in type_iris:
                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{t}>", graph_iri))
            for r in rst_iris:
                lines.append(make_nq(cho_nt, f"<{RICO_HAS_RST}>", f"<{r}>", graph_iri))
            primary_class = type_iris[0]  # first = most specific
            htype_used    = True

    # Layer 2: fixed mediatype class (always emit if set; added on top of layer 1)
    if rdf_type_w:
        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_w}>", graph_iri))
        if not primary_class:
            primary_class = rdf_type_w
    if rdf_type_m:
        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_m}>", graph_iri))
        if not primary_class:
            primary_class = rdf_type_m

    # Audio group dispatch: dc:type → mo:MusicalManifestation (Group A) (§2.3)
    _aco_audio = "https://w3id.org/ac-ontology/aco#AudioManifestation"
    _mo_mani   = "http://purl.org/ontology/mo/MusicalManifestation"
    if rdf_type_m == _aco_audio and dctype_vals and not use_htype:
        for dct in dctype_vals:
            dc_text = (dct.get("$") or "").strip() if isinstance(dct, dict) else ""
            if audio_type2class.get((sector, dc_text)) == "A":
                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{_mo_mani}>", graph_iri))
                primary_class = _mo_mani
                break

    # D9 fallback — no class resolved
    is_fallback = not primary_class
    if is_fallback:
        fallback = MOCHO_NS + "Manifestation"
        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{fallback}>", graph_iri))
        primary_class = fallback

    wemi = _CLASS_WEMI.get(primary_class, "M")
    return lines, primary_class, wemi, {"htype_used": htype_used, "fallback": is_fallback}


def emit_subject_triples(
    cho_nt: str,
    subject_vals: list,
    concepts_index: dict[str, dict],
    graph_iri: str,
) -> NQList:
    """Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended)."""
    lines: NQList = []
    seen: set[str] = set()
    for val in subject_vals:
        if not isinstance(val, dict):
            continue
        resource = (val.get("resource") or "").strip()
        label    = (val.get("$")        or "").strip()
        lang     = (val.get("lang")     or "").strip()
        if resource:
            if resource in seen:
                continue
            seen.add(resource)
            lines.append(make_nq(cho_nt, f"<{DCTERMS_SUBJECT}>", f"<{resource}>", graph_iri))
            concept = concepts_index.get(resource)
            if concept:
                for pl in coerce_list(concept.get("prefLabel")):
                    for obj_nt in value_to_nt_obj(pl):
                        lines.append(make_nq(f"<{resource}>", f"<{RDFS_LABEL}>",
                                             obj_nt, graph_iri))
        elif label:
            key = f"lit:{label}"
            if key in seen:
                continue
            seen.add(key)
            escaped = _escape_literal(label)
            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
            lines.append(make_nq(cho_nt, f"<{DC_SUBJECT}>", obj_nt, graph_iri))
    return lines


def emit_creator_triples(
    cho_nt: str,
    creator_vals: list,
    agents_index: dict[str, AgentDict],
    target_class: str,
    class_prop_align: PropAlign,
    graph_iri: str,
) -> NQList:
    """Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).

    Both tracks run independently for each creator value (D2 / props-mapping §4).
    """
    lines: NQList = []
    dc_creator_iri = "http://purl.org/dc/elements/1.1/creator"
    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), "")

    for val in coerce_list(creator_vals):
        if not isinstance(val, dict):
            continue
        resource = (val.get("resource") or "").strip()
        label    = (val.get("$")        or "").strip()
        lang     = (val.get("lang")     or "").strip()

        # Track 1: class-specific predicate (always runs when target_prop is known)
        if track1_prop:
            if resource:
                lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{resource}>", graph_iri))
            elif label:
                escaped = _escape_literal(label)
                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
                lines.append(make_nq(cho_nt, f"<{track1_prop}>", obj_nt, graph_iri))

        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)
        agent = resolve_agent(label, resource, agents_index)
        if agent:
            agent_uri = (agent.get("about") or "").strip()
            if agent_uri and is_ddb_or_gnd(agent_uri):
                lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>",
                                     f"<{agent_uri}>", graph_iri))
                agent_nt = f"<{agent_uri}>"
                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
                pref = agent.get("prefLabel") or label
                if pref and isinstance(pref, str):
                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>",
                                         f'"{_escape_literal(pref)}"', graph_iri))
    return lines


def emit_contributor_triples(
    cho_nt: str,
    contributor_vals: list,
    event_participant_index: dict[str, str],
    lido_dispatch: dict[str, dict],
    target_class: str,
    wemi: str,
    graph_iri: str,
) -> NQList:
    """Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5)."""
    lines: NQList = []
    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), "dc_agent_fallback")

    for val in coerce_list(contributor_vals):
        if not isinstance(val, dict):
            continue
        resource = (val.get("resource") or "").strip()
        label    = (val.get("$")        or "").strip()
        lang     = (val.get("lang")     or "").strip()

        lido_type   = event_participant_index.get(resource) if resource else None
        lido_row    = lido_dispatch.get(lido_type) if lido_type else None
        target_prop = (
            (lido_row.get(prop_col) or lido_row.get("dc_agent_fallback") or DC_CONTRIBUTOR)
            if lido_row else DC_CONTRIBUTOR
        )

        if resource:
            lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{resource}>", graph_iri))
            agent_nt = f"<{resource}>"
            lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
            if label:
                escaped = _escape_literal(label)
                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
                lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
        elif label:
            escaped = _escape_literal(label)
            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
            lines.append(make_nq(cho_nt, f"<{DC_CONTRIBUTOR}>", obj_nt, graph_iri))
    return lines


def emit_aggregation_triples(agg: dict, cho_nt: str, graph_iri: str) -> NQList:
    """Emit mocho triples derived from the Aggregation block (D23)."""
    lines: NQList = []
    _edm_dp = EDM_NS + "dataProvider"
    _org_prefix = "http://www.deutsche-digitale-bibliothek.de/organization/"

    is_shown = agg.get("isShownAt") or {}
    if isinstance(is_shown, dict):
        uri = (is_shown.get("resource") or "").strip()
        if uri:
            lines.append(make_nq(cho_nt, f"<{DCTERMS_SOURCE}>", f"<{uri}>", graph_iri))

    for dp in coerce_list(agg.get("dataProvider")):
        if not isinstance(dp, dict):
            continue
        uri = (dp.get("resource") or "").strip()
        if uri and uri.startswith(_org_prefix):
            lines.append(make_nq(cho_nt, f"<{_edm_dp}>", f"<{uri}>", graph_iri))

    for obj in coerce_list(agg.get("object")):
        if not isinstance(obj, dict):
            continue
        uri = (obj.get("resource") or "").strip()
        if uri:
            lines.append(make_nq(cho_nt, f"<{FOAF_THUMBNAIL}>", f"<{uri}>", graph_iri))

    return lines


def emit_place_stubs(places: object, graph_iri: str) -> NQList:
    """Emit rdfs:label stubs for each Place entity referenced by the record (D24)."""
    lines: NQList = []
    for place in coerce_list(places):
        if not isinstance(place, dict):
            continue
        raw_about = (place.get("about") or "").strip()
        if not raw_about:
            continue
        place_uri = mint_bare_id("Place", raw_about)
        place_nt  = f"<{place_uri}>"
        for lbl in coerce_list(place.get("prefLabel")):
            for obj_nt in value_to_nt_obj(lbl):
                lines.append(make_nq(place_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
    return lines


def werk_staging_row(cho_uri: str, cho: dict, target_class: str) -> dict | None:
    """Build a werk_staging dict if target_class is a W-slot class (D26). Else None."""
    if target_class not in _W_SLOT_CLASSES:
        return None

    title = ""
    tv = cho.get("title")
    if isinstance(tv, dict):
        title = (tv.get("$") or "").strip()
    elif isinstance(tv, list) and tv:
        first = tv[0]
        title = (first.get("$") or "").strip() if isinstance(first, dict) else ""

    dc_alt: list[str] = []
    for v in coerce_list(cho.get("alternative")):
        t = (v.get("$") or "").strip() if isinstance(v, dict) else ""
        if t:
            dc_alt.append(t)

    dc_created = ""
    for v in coerce_list(cho.get("date")):
        t = (v if isinstance(v, str) else "").strip()
        if t:
            dc_created = t
            break

    creator_uris: list[str] = []
    creator_lits: list[str] = []
    for v in coerce_list(cho.get("creator")):
        if not isinstance(v, dict):
            continue
        uri = (v.get("resource") or "").strip()
        lit = (v.get("$")        or "").strip()
        if uri:
            creator_uris.append(uri)
        elif lit:
            creator_lits.append(lit)

    obj_id = cho_uri.rsplit("/", 1)[-1]
    return {
        "ddb_obj_id":       obj_id,
        "cho_uri":          cho_uri,
        "target_class":     target_class,
        "dc_title":         title,
        "dc_alternative":   dc_alt,
        "dc_created":       dc_created,
        "creator_uris":     creator_uris,
        "creator_literals": creator_lits,
    }


def emit_mocho_triples(
    rdf: dict,
    cho_uri: str,
    ddb_uri: str,
    sector: str,
    mediatype: str,
    mediatype_class_map: dict,
    htype_map: dict,
    audio_type2class: dict,
    class_prop_align: PropAlign,
    lido_dispatch: dict,
    graph_iri: str,
) -> tuple[NQList, str, str, dict]:
    """Emit all mocho-graph triples for one record (§6.3). Returns (lines, target_class, wemi, dispatch_flags)."""
    lines: NQList = []

    cho: dict = rdf.get("ProvidedCHO") or {}
    if isinstance(cho, list):
        cho = cho[0] if cho else {}

    cho_nt      = f"<{cho_uri}>"
    htype       = (cho.get("hierarchyType") or "").strip() or None
    dctype_vals = coerce_list(cho.get("dcType"))

    # ── Class dispatch ────────────────────────────────────────────────────────
    type_lines, target_class, wemi, dispatch_flags = retype_entities(
        sector, mediatype, htype, dctype_vals,
        cho_nt, mediatype_class_map, htype_map, audio_type2class, graph_iri,
    )
    lines.extend(type_lines)

    # owl:sameAs link to original DDB URI (D22)
    lines.append(make_nq(cho_nt, f"<{OWL_SAMEAS}>", f"<{ddb_uri}>", graph_iri))

    # ── Build per-record indexes ───────────────────────────────────────────────
    agents_index: dict[str, AgentDict] = {}
    for agent in coerce_list(rdf.get("Agent")):
        if not isinstance(agent, dict):
            continue
        about = (agent.get("about") or "").strip()
        if about:
            agents_index[mint_bare_id("Agent", about)] = agent
        for pl in coerce_list(agent.get("prefLabel")):
            t = (pl.get("$") or "").strip() if isinstance(pl, dict) else ""
            if t:
                agents_index.setdefault(t, agent)

    event_participant_index: dict[str, str] = {}
    for event in coerce_list(rdf.get("Event")):
        if not isinstance(event, dict):
            continue
        ht = event.get("hasType") or {}
        if isinstance(ht, list):
            ht = ht[0] if ht else {}
        lido_type_uri = (ht.get("resource") or "").strip() if isinstance(ht, dict) else ""
        for p in coerce_list(event.get("P11_had_participant")):
            puri = (p.get("resource") or "").strip() if isinstance(p, dict) else ""
            if puri and lido_type_uri:
                event_participant_index[puri] = lido_type_uri

    concepts_index: dict[str, dict] = {}
    for concept in coerce_list(rdf.get("Concept")):
        if not isinstance(concept, dict):
            continue
        about = (concept.get("about") or "").strip()
        if about:
            concepts_index[about] = concept

    # ── dc:title — dual-emit (props-mapping D4) ───────────────────────────────
    dc_title_iri = "http://purl.org/dc/elements/1.1/title"
    title_prop   = class_prop_align.get((target_class, dc_title_iri), "")
    for obj_nt in value_to_nt_obj(cho.get("title")):
        lines.append(make_nq(cho_nt, f"<{dc_title_iri}>", obj_nt, graph_iri))
        if title_prop and title_prop != dc_title_iri:
            lines.append(make_nq(cho_nt, f"<{title_prop}>", obj_nt, graph_iri))

    # ── Generic property loop ─────────────────────────────────────────────────
    dc_date_iri    = "http://purl.org/dc/elements/1.1/date"
    dcterms_iss    = "http://purl.org/dc/terms/issued"
    dcterms_ipart  = "http://purl.org/dc/terms/isPartOf"
    _subject_keys  = frozenset({"dcSubject", "dcTermsSubject", "dcTermSubject"})
    _special_keys  = frozenset({"creator", "contributor", "title"}) | _subject_keys | _MOCHO_SKIP

    subject_vals: list = []
    for skey in _subject_keys:
        subject_vals.extend(coerce_list(cho.get(skey)))

    for prop, val in cho.items():
        if prop in _special_keys:
            continue
        prop_iri = _DDBEDM_PROP.get(prop)
        if not prop_iri:
            continue
        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
        if not target_prop:
            continue

        if prop_iri in (dc_date_iri, dcterms_iss):
            # Date normalisation (D15 / props-mapping §3.1)
            for v in coerce_list(val):
                raw = (v if isinstance(v, str) else
                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
                for normed in normalize_date(raw):
                    if normed:
                        lines.append(make_nq(cho_nt, f"<{target_prop}>",
                                             f'"{_escape_literal(normed)}"', graph_iri))
            continue

        if prop_iri == dcterms_ipart:
            # isPartOf URI sanitisation (props-mapping §3.1)
            for obj_nt in value_to_nt_obj(val):
                if not obj_nt.startswith("<"):
                    continue  # literal isPartOf skipped in mocho graph
                uri = obj_nt[1:-1]
                if not uri.startswith("http"):
                    if len(uri) == 32:
                        uri = DDB_ITEM_BASE + uri
                    else:
                        continue
                lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{uri}>", graph_iri))
            continue

        for obj_nt in value_to_nt_obj(val):
            lines.append(make_nq(cho_nt, f"<{target_prop}>", obj_nt, graph_iri))

    # ── Special handlers ──────────────────────────────────────────────────────
    lines.extend(emit_creator_triples(
        cho_nt, cho.get("creator"), agents_index, target_class, class_prop_align, graph_iri,
    ))
    lines.extend(emit_contributor_triples(
        cho_nt, cho.get("contributor"),
        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,
    ))
    if subject_vals:
        lines.extend(emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri))

    # ── Aggregation & Place ───────────────────────────────────────────────────
    agg = rdf.get("Aggregation") or {}
    if isinstance(agg, list):
        agg = agg[0] if agg else {}
    lines.extend(emit_aggregation_triples(agg, cho_nt, graph_iri))
    lines.extend(emit_place_stubs(rdf.get("Place"), graph_iri))

    return lines, target_class, wemi, dispatch_flags


# ─── Core transform ───────────────────────────────────────────────────────────

def transform_record(
    record: dict,
    ids_set: set[str] | None,
    mediatype_class_map: dict,
    htype_map: dict,
    audio_type2class: dict,
    class_prop_align: PropAlign,
    lido_dispatch: dict,
) -> tuple[dict[str, NQList], dict | None, dict]:
    """Transform one JSONL record into per-graph N-Quads lists (§7.1).

    Returns (streams, werk_row, dispatch_info).
    streams is empty dict when record is filtered by IDs.
    dispatch_info: {"target_class", "wemi", "htype_used", "fallback", "is_mt007"}
    """
    obj_id = get_object_id(record)
    if obj_id is None:
        raise ValueError("Cannot extract object ID from record")

    if ids_set is not None and obj_id not in ids_set:
        return {}, None, {}

    rdf = record["edm"]["RDF"]
    cho: dict = rdf.get("ProvidedCHO") or {}
    if isinstance(cho, list):
        cho = cho[0] if cho else {}

    ddb_uri = mint_bare_id("ProvidedCHO", (cho.get("about") or obj_id).strip())
    cho_uri = mint_cho_uri(obj_id)

    mediatype, sector = _extract_mediatype_sector(rdf.get("Concept"))
    is_mt007 = (mediatype == MT007_IRI)

    streams: dict[str, NQList] = {}

    # Streams [1] and [4] always run, including mt007 (faithfulness + audit trail)
    streams["ddbedm"] = emit_ddbedm_triples(rdf, GRAPH_DDBEDM)
    streams["prov"]   = emit_prov_triples(record, ddb_uri, GRAPH_PROV)

    # Stream [2] mocho and [3] werk: skip mt007 (D15)
    werk_row: dict | None = None
    dispatch_info: dict = {"target_class": "", "wemi": "", "htype_used": False,
                           "fallback": False, "is_mt007": is_mt007}
    if not is_mt007:
        mocho_lines, target_class, wemi, dflags = emit_mocho_triples(
            rdf, cho_uri, ddb_uri, sector, mediatype,
            mediatype_class_map, htype_map, audio_type2class,
            class_prop_align, lido_dispatch, GRAPH_MOCHO,
        )
        streams["mocho"] = mocho_lines
        werk_row = werk_staging_row(cho_uri, cho, target_class)
        dispatch_info.update({"target_class": target_class, "wemi": wemi, **dflags})

    return streams, werk_row, dispatch_info


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transform DDB-EDM JSONL to mocho N-Quads (§8)"
    )

    io = parser.add_argument_group("I/O")
    io.add_argument("--jsonl",  type=Path, default=DEFAULT_JSONL,
                    help="JSONL input file (one DDB-EDM JSON object per line); "
                         "default: data/items-all-goethe-faust.json")
    io.add_argument("--ids",    type=str,  default=None,
                    help="Path to ID allowlist file (one 32-char DDB ID per line), "
                         "or '-' to read from stdin; omit to process all records")
    io.add_argument("--outdir", type=Path, default=None,
                    help="Output directory; auto-timestamped if omitted "
                         "(default: output/transform/YYYYMMDD_HHMMSS)")

    cfg = parser.add_argument_group("Config")
    cfg.add_argument("--alignment", type=Path, default=DEFAULT_ALIGNMENT,
                     help="Property alignment lookup CSV "
                          "(target_class, edm_prop) → mocho property; "
                          "default: output/config/lookup_class_prop_alignment.csv")
    cfg.add_argument("--lido",      type=Path, default=DEFAULT_LIDO,
                     help="LIDO event type dispatch CSV "
                          "(event URI → agent predicates per WEMI level); "
                          "default: output/config/lido_event_types.csv")
    cfg.add_argument("--htype",     type=Path, default=DEFAULT_HTYPE,
                     help="htype → class lookup CSV "
                          "(htype_code → rdf:type IRIs for §1.1 dispatch); "
                          "default: output/config/lookup_htype_doco_rico.csv")
    cfg.add_argument("--mediatype", type=Path, default=DEFAULT_MEDIATYPE,
                     help="Mediatype × sector → class lookup CSV "
                          "(sector, mediatype → WEMI class IRIs); "
                          "default: output/config/lookup_mediatype_class.csv")
    cfg.add_argument("--audio",     type=Path, default=DEFAULT_AUDIO,
                     help="mt001 dc:type → audio group JSON "
                          "(dc:type value → A/B/C group for audio class dispatch); "
                          "default: output/config/audio_type2class.json")

    run = parser.add_argument_group("Run control")
    run.add_argument("--stats",     choices=["none", "basic", "dispatch", "full"],
                     default="basic",
                     help="Stats verbosity written to transform_stats.json: "
                          "none=nothing written, basic=run/records/triples/werk_staging, "
                          "dispatch=basic+WEMI class counts (recommended for full-corpus runs), "
                          "full=dispatch+per-predicate mocho counts (slow — use with --limit); "
                          "default: basic")
    run.add_argument("--log-level", default="INFO",
                     choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                     dest="log_level",
                     help="Console and file log verbosity; default: INFO")
    run.add_argument("--limit",     type=int, default=None,
                     help="Stop after N records — for smoke-testing and sampling")
    run.add_argument("--debug",     action="store_true",
                     help="Enable DEBUG logging (shorthand for --log-level DEBUG)")

    args = parser.parse_args()

    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = args.outdir or (DEFAULT_OUTPUT_BASE / ts)
    outdir.mkdir(parents=True, exist_ok=True)

    out_path    = outdir / "goethe-faust.nq"
    werk_path   = outdir / "goethe-faust-werk-staging.duckdb"
    stats_path  = outdir / "transform_stats.json"
    errors_path = outdir / "transform_errors.jsonl"
    log_path    = outdir / "transform.log"

    logging.basicConfig(
        filename=str(log_path),
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger(__name__)

    log.info("Loading config tables")
    class_prop_align    = load_class_prop_alignment(args.alignment)
    lido_dispatch       = load_lido_event_types(args.lido)
    htype_map           = load_htype_map(args.htype)
    mediatype_class_map = load_mediatype_class(args.mediatype)
    audio_type2class    = load_audio_type2class(args.audio)

    ids_set: set[str] | None = None
    if args.ids == "-":
        ids_set = {line.strip() for line in sys.stdin if line.strip()}
    elif args.ids:
        ids_set = load_ids(Path(args.ids))

    import duckdb
    conn = duckdb.connect(str(werk_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS werk_staging (
            ddb_obj_id       VARCHAR PRIMARY KEY,
            cho_uri          VARCHAR,
            target_class     VARCHAR,
            dc_title         VARCHAR,
            dc_alternative   VARCHAR[],
            dc_created       VARCHAR,
            creator_uris     VARCHAR[],
            creator_literals VARCHAR[]
        )
    """)

    stats_level = args.stats   # "none" | "basic" | "dispatch" | "full"

    stats:  Counter = Counter()
    errors: list    = []

    # dispatch / full only
    class_counts: dict[str, Counter] = {"W": Counter(), "E": Counter(), "M": Counter(), "": Counter()}
    # full only
    prop_all: Counter = Counter()
    prop_new: Counter = Counter()
    # basic+
    werk_by_class: Counter = Counter()

    with open(args.jsonl, encoding="utf-8") as inp, \
         open(out_path, "w", encoding="utf-8") as out:

        for line_no, raw in enumerate(inp, 1):
            raw = raw.strip()
            if not raw:
                continue
            if args.limit and line_no > args.limit:
                break

            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append({"line": line_no, "issue": f"JSON parse error: {exc}"})
                stats["json_errors"] += 1
                continue

            obj_id = get_object_id(record) or f"line:{line_no}"
            try:
                streams, werk_row, dispatch_info = transform_record(
                    record, ids_set,
                    mediatype_class_map, htype_map, audio_type2class,
                    class_prop_align, lido_dispatch,
                )
            except Exception as exc:
                errors.append({
                    "id":        obj_id,
                    "issue":     str(exc),
                    "traceback": traceback.format_exc(),
                })
                stats["record_errors"] += 1
                continue

            if not streams:
                stats["filtered"] += 1
                continue

            for graph_name, graph_lines in streams.items():
                for nq in graph_lines:
                    out.write(nq + "\n")
                    stats["triples_total"] += 1
                    stats[f"triples_{graph_name}"] += 1

            stats["records_processed"] += 1

            if stats_level in ("dispatch", "full"):
                # Dispatch method accounting
                if dispatch_info.get("is_mt007"):
                    stats["skipped_mt007"] += 1
                elif dispatch_info.get("fallback"):
                    stats["dispatch_fallback"] += 1
                elif dispatch_info.get("htype_used"):
                    stats["dispatch_htype"] += 1
                else:
                    stats["dispatch_mediatype"] += 1

                # Class counts by WEMI slot
                tc = dispatch_info.get("target_class", "")
                if tc:
                    wemi = dispatch_info.get("wemi", "M")
                    class_counts[wemi][_to_curie(tc)] += 1

            if stats_level == "full":
                # Property counts in mocho stream — O(triples_mocho); use on samples only
                for nq in streams.get("mocho", []):
                    m = _NQ_PRED_RE.match(nq)
                    if m:
                        pred_iri = m.group(1)
                        curie = _to_curie(pred_iri)
                        prop_all[curie] += 1
                        if any(pred_iri.startswith(ns) for ns in _NEW_NS):
                            prop_new[curie] += 1

            if werk_row:
                conn.execute(
                    "INSERT OR REPLACE INTO werk_staging VALUES (?,?,?,?,?,?,?,?)",
                    [
                        werk_row["ddb_obj_id"],
                        werk_row["cho_uri"],
                        werk_row["target_class"],
                        werk_row["dc_title"],
                        werk_row["dc_alternative"],
                        werk_row["dc_created"],
                        werk_row["creator_uris"],
                        werk_row["creator_literals"],
                    ],
                )
                stats["werk_staging_rows"] += 1
                werk_by_class[_to_curie(werk_row["target_class"])] += 1

    conn.close()

    if stats_level != "none":
        stats_out: dict = {
            "run": {
                "timestamp": ts,
                "input":     str(args.jsonl),
                "stats_level": stats_level,
            },
            "records": {
                "processed":          stats["records_processed"],
                "skipped_not_in_ids": stats["filtered"],
                "errors": {
                    "json_parse": stats["json_errors"],
                    "transform":  stats["record_errors"],
                },
            },
            "triples": {
                "total":    stats["triples_total"],
                "by_graph": {
                    "ddbedm": stats["triples_ddbedm"],
                    "mocho":  stats["triples_mocho"],
                    "prov":   stats["triples_prov"],
                },
            },
            "werk_staging": {
                "rows":     stats["werk_staging_rows"],
                "by_class": dict(werk_by_class.most_common()),
            },
        }

        if stats_level in ("dispatch", "full"):
            stats_out["dispatch"] = {
                "htype_hits":            stats["dispatch_htype"],
                "mediatype_hits":        stats["dispatch_mediatype"],
                "fallback_d9":           stats["dispatch_fallback"],
                "skipped_mt007":         stats["skipped_mt007"],
                "work_classes":          dict(class_counts["W"].most_common()),
                "expression_classes":    dict(class_counts["E"].most_common()),
                "manifestation_classes": dict(class_counts["M"].most_common()),
                "rico_classes":          dict(class_counts[""].most_common()),
            }

        if stats_level == "full":
            stats_out["mocho_vocab"] = {
                "properties_all": dict(prop_all.most_common()),
                "properties_new": dict(prop_new.most_common()),
            }

        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(stats_out, f, indent=2)

    if errors:
        with open(errors_path, "w", encoding="utf-8") as f:
            for err in errors:
                f.write(json.dumps(err, ensure_ascii=False) + "\n")

    log.info(
        "Done: %d records, %d triples (mocho %d), %d errors",
        stats["records_processed"],
        stats["triples_total"],
        stats["triples_mocho"],
        stats["record_errors"] + stats["json_errors"],
    )


if __name__ == "__main__":
    main()
