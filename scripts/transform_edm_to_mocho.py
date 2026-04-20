#!/usr/bin/env python3
"""
Purpose:    Transform DDB-EDM JSONL records to mocho-aligned RDF triples.
            Produces an N-Triples pipeline intermediate and a JSON-LD companion
            file for inspection/tooling. Reference implementation for the mocho
            ingest pipeline — decisions documented in goethe-faust/notes/alignment-adr.md.
Usage:      python transform_edm_to_mocho.py [--jsonl FILE] [--ids FILE]
                [--alignment FILE] [--htype FILE]
                [--out-nt FILE] [--out-jsonld FILE] [--stats FILE] [--limit N]
Inputs:     data/items-all-goethe-faust.json         JSONL, one record per line
            data/ids-all-goethe-faust.txt             32-char object IDs, one per line
            output/alignment_ddbedm_mocho.csv         (entity_type, json_key) → RDA candidates
            output/lookup_htype_doco_rico.csv         htype_code → DoCO/RiC-O class
            output/lookup_dctype_to_class.csv         (mediatype, sector, dc_type_de) → class IRIs
Outputs:    output/mocho-goethe-faust.nt              N-Triples (pipeline intermediate)
            output/mocho-goethe-faust.jsonld          JSON-LD (inspection/tooling)
            output/transform_stats.json               run stats + ignored-properties inventory
Deps:       stdlib only (json, csv, re, sys, collections, argparse, pathlib)
Assumes:    JSONL: one JSON object per line; record structure edm.RDF.*
            alignment CSV columns: entity_type, json_key, edm_prefix, edm_iri,
              record_count, coverage_pct, rda_iri, rda_label, wemi_level,
              match_method, in_mocho  (in_mocho is string "True"/"False")
            htype CSV column htype_code contains literal values as they appear
              in the JSONL (e.g. "htype_030"), not German/English labels
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

DEFAULT_JSONL      = PROJECT_DIR / "data"   / "items-all-goethe-faust.json"
DEFAULT_IDS        = PROJECT_DIR / "data"   / "ids-all-goethe-faust.txt"
DEFAULT_ALIGNMENT  = PROJECT_DIR / "output" / "alignment_ddbedm_mocho.csv"
DEFAULT_HTYPE      = PROJECT_DIR / "output" / "lookup_htype_doco_rico.csv"
DEFAULT_DCTYPE     = PROJECT_DIR / "output" / "lookup_dctype_to_class.csv"
DEFAULT_OUT_NT     = PROJECT_DIR / "output" / "mocho-goethe-faust.nt"
DEFAULT_OUT_JSONLD = PROJECT_DIR / "output" / "mocho-goethe-faust.jsonld"
DEFAULT_STATS      = PROJECT_DIR / "output" / "transform_stats.json"

# ─── Constants ────────────────────────────────────────────────────────────────

RDF_TYPE            = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
MOCHO_NS            = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#"
MOCHO_MANIFESTATION = MOCHO_NS + "Manifestation"
RICO_HAS_RST        = "http://www.ica.org/standards/RiC/ontology#hasRecordSetType"

# D.1 — dc:type dispatch: vocnet prefixes for mediatype/sector extraction
_MEDIATYPE_PREFIX = "http://ddb.vocnet.org/medientyp/"
_SECTOR_PREFIX    = "http://ddb.vocnet.org/sparte/"
_MT002_IRI        = "http://ddb.vocnet.org/medientyp/mt002"

# D.2 — WebResource typing for mt002 (mocho:ImageObject layer)
_MOCHO_IMAGE_OBJECT = MOCHO_NS + "ImageObject"
_RDAC_C10007        = "http://rdaregistry.info/Elements/c/C10007"          # rdac:Item
_RDAM_P30001        = "http://rdaregistry.info/Elements/m/P30001"          # has carrier type
_RDACT_1018         = "http://rdaregistry.info/termList/RDACarrierType/1018"  # still image
_VRA_IMAGE_OF       = "http://purl.org/vra/imageOf"

# Fan-out whitelist (ADR D7–D8): bypass alignment table for creator/contributor.
#
# D7: dc:creator → rdam:P30263 has creator agent of manifestation.
#     The alignment table produced 464 Work-level candidates for creator, all
#     highly specific (e.g. "has plaintiff corporate body"). Correct WEMI level
#     is Manifestation, consistent with mocho:Manifestation base type (D9).
#     rdam:P30263 is the generic Manifestation-level creator property.
#
# D8: dc:contributor → dc:contributor kept as-is.
#     360 alignment table candidates, none generic (all specific performer roles).
#     No generic "has contributor agent" superclass in mocho's current import.
#     dc:contributor is a valid, well-understood predicate; keeps the link without
#     asserting a role that cannot be determined from the DC value alone.
CREATOR_IRI     = "http://rdaregistry.info/Elements/m/P30263"   # rdam:P30263
CONTRIBUTOR_IRI = "http://purl.org/dc/elements/1.1/contributor" # dc:contributor

# Subject keys: three JSON keys that carry subject data (ADR D6).
# emit_subject_triples() handles value-type dispatch and cross-key deduplication.
# Note: dcTermsSubject was incorrectly resolved to dc:subject in the alignment CSV
# (IRI resolution error in align_ddbedm_to_mocho.py); corrected to dcterms:subject
# in the CSV (42 rows). Dispatch routes IRI-valued subjects to dcterms:subject path
# regardless of which of the three keys carried the value.
SUBJECT_KEYS = frozenset({"dcSubject", "dcTermsSubject", "dcTermSubject"})

# Keys handled outside the main alignment loop — skip silently, do not count
# as ignored properties in stats output.
# hierarchyType → handled by retype_entities() via htype_map
_SKIP_IN_LOOP = frozenset({"about", "hierarchyType"})

# Prefix expansion for htype lookup table
_PREFIXES = {
    "doco":    "http://purl.org/spar/doco/",
    "rico":    "http://www.ica.org/standards/RiC/ontology#",
    "ric-rst": "http://www.ica.org/standards/RiC/vocabularies/recordSetTypes#",
    "mocho":   MOCHO_NS,
}

# ─── Loaders ──────────────────────────────────────────────────────────────────

def load_alignment(path: Path) -> tuple[dict, dict]:
    """Load alignment_ddbedm_mocho.csv.

    Returns:
        alignment: dict[(entity_type, json_key)] → list of candidate dicts
            Only rows where in_mocho == 'True' and rda_iri non-empty.
            Each candidate: {rda_iri, rda_label, wemi_level, match_method}
        edm_iri_map: dict[(entity_type, json_key)] → edm_iri
            For all rows (used to enrich ignored_properties in stats output).
    """
    alignment: dict = defaultdict(list)
    edm_iri_map: dict = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["entity_type"].strip(), row["json_key"].strip())
            edm_iri = row.get("edm_iri", "").strip()
            if edm_iri and key not in edm_iri_map:
                edm_iri_map[key] = edm_iri
            if row["in_mocho"] != "True" or not row["rda_iri"].strip():
                continue
            alignment[key].append({
                "rda_iri":      row["rda_iri"].strip(),
                "rda_label":    row["rda_label"].strip(),
                "wemi_level":   row["wemi_level"].strip(),
                "match_method": row["match_method"].strip(),
            })
    return dict(alignment), edm_iri_map


def _expand_prefix(curie: str) -> str:
    """Expand a prefixed IRI (e.g. 'doco:Section') to a full IRI."""
    for prefix, base in _PREFIXES.items():
        if curie.startswith(prefix + ":"):
            return base + curie[len(prefix) + 1:]
    return curie  # already a full IRI or unrecognised prefix


def load_htype_map(path: Path) -> dict:
    """Load lookup_htype_doco_rico.csv.

    Returns dict[htype_code] → (rdf_type_iri, [rst_iri, ...]).

    Rows where rdf_type == "pending" or empty are excluded.
    has_record_set_type may be comma-separated (e.g. "mocho:Bestand, ric-rst:Fonds");
    each part is expanded to a full IRI and emitted as a separate rico:hasRecordSetType
    triple (see retype_entities).
    """
    result: dict = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rdf_type = row["rdf_type"].strip()
            if not rdf_type or rdf_type == "pending":
                continue
            type_iri = _expand_prefix(rdf_type)
            rst_iris: list[str] = []
            rst_raw = row.get("has_record_set_type", "").strip()
            if rst_raw:
                for part in rst_raw.split(","):
                    part = part.strip()
                    if part:
                        rst_iris.append(_expand_prefix(part))
            result[row["htype_code"].strip()] = (type_iri, rst_iris)
    return result


def load_ids(path: Path) -> set:
    """Load ids-all-goethe-faust.txt. Returns set of 32-char object IDs."""
    with open(path, encoding="utf-8") as fh:
        return {line.strip() for line in fh if line.strip()}


def load_dctype_map(path: Path) -> dict:
    """Load lookup_dctype_to_class.csv into a three-key dispatch index.

    Returns dict[(mediatype, sector, dc_type_de)] → row dict.
    Keys: mediatype and sector are vocnet IRIs or 'any'; dc_type_de is the
    German literal. Three-level fallback is performed at lookup time.
    """
    index: dict = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["mediatype"], row["sector"], row["dc_type_de"])
            index[key] = row
    return index


# ─── dc:type dispatch helpers ─────────────────────────────────────────────────

def _get_dctype_text(value: object) -> str:
    """Extract the German dc:type string from a dcType field value."""
    if isinstance(value, dict):
        return (value.get("$") or "").strip()
    if isinstance(value, str):
        return value.strip()
    return ""


def _extract_mediatype_sector(concepts: object) -> tuple:
    """Return (mediatype_iri, sector_iri) from the record's Concept list."""
    mediatype = "any"
    sector = "any"
    if not isinstance(concepts, list):
        concepts = [concepts] if isinstance(concepts, dict) else []
    for c in concepts:
        if not isinstance(c, dict):
            continue
        about = c.get("about") or ""
        if about.startswith(_MEDIATYPE_PREFIX):
            mediatype = about
        elif about.startswith(_SECTOR_PREFIX):
            sector = about
    return mediatype, sector


def _dctype_lookup(
    dctype_index: dict,
    mediatype: str,
    sector: str,
    dc_type_de: str,
) -> tuple:
    """Three-level fallback lookup. Returns (row_or_None, match_level)."""
    row = dctype_index.get((mediatype, sector, dc_type_de))
    if row:
        return row, "exact"
    row = dctype_index.get((mediatype, "any", dc_type_de))
    if row:
        return row, "any-sector"
    row = dctype_index.get(("any", "any", dc_type_de))
    if row:
        return row, "any-mediatype"
    return None, "fallback"


# ─── Record helpers ───────────────────────────────────────────────────────────

def get_object_id(record: dict):
    """Extract 32-char object ID from ProvidedCHO.about URI. Returns None on failure."""
    try:
        about = record["edm"]["RDF"]["ProvidedCHO"]["about"]
    except (KeyError, TypeError):
        return None
    if not about:
        return None
    obj_id = about.rstrip("/").rsplit("/", 1)[-1]
    return obj_id if len(obj_id) == 32 else None


def _escape_literal(s: str) -> str:
    """Escape backslash and double-quote for N-Triples literal content."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def value_to_nt_obj(val) -> list:
    """Convert a JSONL field value to a list of N-Triples object strings.

    Handles all value shapes produced by the DDB EDM JSONL:
      None / ""                     → []
      str (non-empty)               → ['"escaped"']
      list                          → recurse and flatten
      {"resource": IRI}             → ["<IRI>"]   (IRI non-null/non-empty)
      {"lang": L, "$": T}           → ['"T"@L']   (L non-null, T non-empty)
      {"lang": null, "$": T}        → ['"T"']     (T non-empty)
      {"resource": null, "$": ""}   → []
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
        if resource:  # non-null, non-empty IRI
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


def emit_subject_triples(entity: dict, subject_nt: str, alignment: dict) -> list:
    """Emit RDF triples for dc:subject / dcterms:subject (ADR D6).

    Collects values from all three subject keys (dcSubject, dcTermsSubject,
    dcTermSubject), dispatches by value type:
      IRI value     → alignment candidates for ("ProvidedCHO", "dcTermSubject")
                       i.e. dcterms:subject path
      literal value → alignment candidates for ("ProvidedCHO", "dcSubject")
                       i.e. dc:subject path
    Deduplicates (pred_nt, obj_nt) pairs across keys before writing.
    ~60% of records carry duplicate values across the three keys.
    """
    lit_candidates = alignment.get(("ProvidedCHO", "dcSubject"), [])
    iri_candidates = alignment.get(("ProvidedCHO", "dcTermSubject"), [])
    seen: set = set()
    nt_lines: list = []
    for key in SUBJECT_KEYS:
        raw_val = entity.get(key)
        if raw_val is None:
            continue
        for obj_nt in value_to_nt_obj(raw_val):
            candidates = iri_candidates if obj_nt.startswith("<") else lit_candidates
            for row in candidates:
                pred_nt = f"<{row['rda_iri']}>"
                pair = (pred_nt, obj_nt)
                if pair not in seen:
                    seen.add(pair)
                    nt_lines.append(f"{subject_nt} {pred_nt} {obj_nt} .")
    return nt_lines


def retype_entities(rdf: dict, htype_map: dict, dctype_index: dict, stats: dict) -> list:
    """Emit rdf:type triples for ProvidedCHO and PhysicalThing (ADR D9–D12).

    ProvidedCHO — two independent dispatch layers (both may fire):

      Layer 1 — htype dispatch (D9/D10):
        If hierarchyType mapped: emit DoCO/RiC-O class + rico:hasRecordSetType.
        If absent/pending: count in objects_missing_specific_type.

      Layer 2 — dc:type dispatch (D11/D12):
        Three-level lookup in lookup_dctype_to_class.csv:
          exact (mediatype, sector, dc_type_de)
          → any-sector (mediatype, any, dc_type_de)
          → any-mediatype (any, any, dc_type_de)
          → fallback: mocho:Manifestation only (D9)

        W-slot class found → emit W-slot IRI instead of mocho:Manifestation.
        M-slot class found (not mocho:Manifestation) → emit alongside mocho:Manifestation.
        No match or empty slots → mocho:Manifestation only.

      D.2 — WebResource typing (mt002 only):
        For photo records: each WebResource typed as mocho:ImageObject + rdac:C10007,
        with rdam:P30001 rdact:1018 (still-image carrier) and vra:imageOf <cho-uri>.

    PhysicalThing (D10):
      Archival hierarchy ancestors. Typed via htype lookup; no mocho:Manifestation.
    """
    nt_lines: list = []
    rdf_type_nt  = f"<{RDF_TYPE}>"
    rico_rst_nt  = f"<{RICO_HAS_RST}>"

    # ── Extract mediatype + sector from Concept list (needed for both layers) ──
    mediatype, sector = _extract_mediatype_sector(rdf.get("Concept"))

    # ── ProvidedCHO ───────────────────────────────────────────────────────────
    cho = rdf.get("ProvidedCHO")
    if isinstance(cho, dict):
        about = cho.get("about")
        if about:
            s = f"<{about}>"

            # Layer 2: dc:type dispatch — determines ProvidedCHO rdf:type
            dc_types_raw = cho.get("dcType")
            if dc_types_raw is None:
                dc_types_raw = []
            elif not isinstance(dc_types_raw, list):
                dc_types_raw = [dc_types_raw]

            dc_type_de = _get_dctype_text(dc_types_raw[0]) if dc_types_raw else ""
            matched_row, _level = _dctype_lookup(dctype_index, mediatype, sector, dc_type_de)

            rdf_type_w = matched_row["rdf_type_w"] if matched_row else ""
            rdf_type_m = matched_row["rdf_type_m"] if matched_row else ""

            if rdf_type_w:
                # W-slot replaces mocho:Manifestation for ProvidedCHO
                nt_lines.append(f"{s} {rdf_type_nt} <{rdf_type_w}> .")
                stats["dctype_w_assigned"] += 1
            elif rdf_type_m and rdf_type_m != MOCHO_MANIFESTATION:
                # M-slot accumulated alongside mocho:Manifestation
                nt_lines.append(f"{s} {rdf_type_nt} <{MOCHO_MANIFESTATION}> .")
                nt_lines.append(f"{s} {rdf_type_nt} <{rdf_type_m}> .")
                stats["dctype_m_accumulated"] += 1
            else:
                # D9 fallback
                nt_lines.append(f"{s} {rdf_type_nt} <{MOCHO_MANIFESTATION}> .")
                stats["dctype_fallback"] += 1

            # Layer 1: htype dispatch — independent of dc:type layer
            htype = cho.get("hierarchyType")
            if htype and htype in htype_map:
                type_iri, rst_iris = htype_map[htype]
                nt_lines.append(f"{s} {rdf_type_nt} <{type_iri}> .")
                for rst_iri in rst_iris:
                    nt_lines.append(f"{s} {rico_rst_nt} <{rst_iri}> .")
            else:
                stats["objects_missing_specific_type"] += 1

            # D.2: WebResource typing — mt002 (Photo) only
            if mediatype == _MT002_IRI:
                web_resources = rdf.get("WebResource")
                if web_resources is None:
                    web_resources = []
                elif isinstance(web_resources, dict):
                    web_resources = [web_resources]
                for wr in web_resources:
                    if not isinstance(wr, dict):
                        continue
                    wr_uri = wr.get("about")
                    if not wr_uri:
                        continue
                    wr_s = f"<{wr_uri}>"
                    cho_s = s
                    nt_lines.append(f"{wr_s} {rdf_type_nt} <{_MOCHO_IMAGE_OBJECT}> .")
                    nt_lines.append(f"{wr_s} {rdf_type_nt} <{_RDAC_C10007}> .")
                    nt_lines.append(
                        f"{wr_s} <{_RDAM_P30001}> <{_RDACT_1018}> ."
                    )
                    nt_lines.append(f"{wr_s} <{_VRA_IMAGE_OF}> {cho_s} .")
                    stats["webresources_typed"] += 1

    # ── PhysicalThing ─────────────────────────────────────────────────────────
    physical_things = rdf.get("PhysicalThing")
    if isinstance(physical_things, list):
        for entity in physical_things:
            if not isinstance(entity, dict):
                continue
            about = entity.get("about")
            if not about:
                continue
            htype = entity.get("hierarchyType")
            if htype and htype in htype_map:
                s = f"<{about}>"
                type_iri, rst_iris = htype_map[htype]
                nt_lines.append(f"{s} {rdf_type_nt} <{type_iri}> .")
                for rst_iri in rst_iris:
                    nt_lines.append(f"{s} {rico_rst_nt} <{rst_iri}> .")

    return nt_lines


# ─── Core transform ───────────────────────────────────────────────────────────

def transform_record(
    record: dict,
    alignment: dict,
    htype_map: dict,
    dctype_index: dict,
    ids_filter: set,
    stats: dict,
    ignored_keys: Counter,
) -> list:
    """Transform one JSONL record to a list of N-Triples lines.

    Returns empty list if the record's object ID is not in ids_filter
    or if the record structure is malformed.
    """
    obj_id = get_object_id(record)
    if obj_id not in ids_filter:
        stats["records_skipped_not_in_ids"] += 1
        return []

    try:
        rdf = record["edm"]["RDF"]
    except (KeyError, TypeError):
        stats["records_skipped_not_in_ids"] += 1
        return []

    nt_lines: list = []

    for entity_type, entities in rdf.items():
        if entities is None:
            continue
        if isinstance(entities, dict):
            entities = [entities]
        if not isinstance(entities, list):
            continue

        for entity in entities:
            if not isinstance(entity, dict):
                continue
            subject = entity.get("about")
            if not subject:
                continue
            subject_nt = f"<{subject}>"

            # Subject key dispatch + cross-key deduplication (ADR D6)
            if entity_type == "ProvidedCHO":
                nt_lines.extend(emit_subject_triples(entity, subject_nt, alignment))

            for json_key, raw_val in entity.items():
                if json_key in _SKIP_IN_LOOP or raw_val is None:
                    continue

                # Subject keys handled above
                if entity_type == "ProvidedCHO" and json_key in SUBJECT_KEYS:
                    continue

                # Fan-out whitelist (ADR D7–D8)
                if entity_type == "ProvidedCHO" and json_key in ("creator", "contributor"):
                    pred_iri = CREATOR_IRI if json_key == "creator" else CONTRIBUTOR_IRI
                    pred_nt = f"<{pred_iri}>"
                    for obj_nt in value_to_nt_obj(raw_val):
                        nt_lines.append(f"{subject_nt} {pred_nt} {obj_nt} .")
                    continue

                candidates = alignment.get((entity_type, json_key), [])
                if not candidates:
                    vals = value_to_nt_obj(raw_val)
                    if vals:
                        ignored_keys[f"{entity_type}.{json_key}"] += len(vals)
                    continue

                pred_nt_cache: dict = {}
                for row in candidates:
                    pred_iri = row["rda_iri"]
                    if pred_iri not in pred_nt_cache:
                        pred_nt_cache[pred_iri] = f"<{pred_iri}>"
                    pred_nt = pred_nt_cache[pred_iri]
                    for obj_nt in value_to_nt_obj(raw_val):
                        nt_lines.append(f"{subject_nt} {pred_nt} {obj_nt} .")

    # rdf:type for ProvidedCHO (dc:type + htype layers) and PhysicalThing + WebResources
    nt_lines.extend(retype_entities(rdf, htype_map, dctype_index, stats))

    stats["records_processed"] += 1
    stats["triples_out"] += len(nt_lines)
    return nt_lines


# ─── JSON-LD helpers ──────────────────────────────────────────────────────────

# Matches our generated NT lines: <subj> <pred> <obj> .
_NT_RE = re.compile(r'^(<[^>]+>)\s+(<[^>]+>)\s+(.+) \.$')
_LANG_LIT_RE  = re.compile(r'^"((?:[^"\\]|\\.)*)"@([\w-]+)$')
_PLAIN_LIT_RE = re.compile(r'^"((?:[^"\\]|\\.)*)"$')

_JSONLD_CONTEXT = {
    "rdf":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs":    "http://www.w3.org/2000/01/rdf-schema#",
    "dc":      "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "edm":     "http://www.europeana.eu/schemas/edm/",
    "mocho":   MOCHO_NS,
    "rico":    "http://www.ica.org/standards/RiC/ontology#",
    "doco":    "http://purl.org/spar/doco/",
    "rdam":    "http://rdaregistry.info/Elements/m/",
    "rdaw":    "http://rdaregistry.info/Elements/w/",
    "rdaa":    "http://rdaregistry.info/Elements/a/",
    "skos":    "http://www.w3.org/2004/02/skos/core#",
}


def _nt_obj_to_jsonld(obj_nt: str) -> dict:
    """Convert an N-Triples object string to a JSON-LD value object."""
    if obj_nt.startswith("<") and obj_nt.endswith(">"):
        return {"@id": obj_nt[1:-1]}
    m = _LANG_LIT_RE.match(obj_nt)
    if m:
        text = m.group(1).replace('\\"', '"').replace("\\\\", "\\")
        return {"@value": text, "@language": m.group(2)}
    m = _PLAIN_LIT_RE.match(obj_nt)
    if m:
        text = m.group(1).replace('\\"', '"').replace("\\\\", "\\")
        return {"@value": text}
    return {"@value": obj_nt}  # fallback


def nt_lines_to_jsonld_nodes(nt_lines: list) -> list:
    """Convert a list of N-Triples lines to JSON-LD node objects.

    Groups triples by subject → one node dict per subject:
      {"@id": subject_iri, pred_iri: [obj_value, ...], ...}
    """
    nodes: dict = {}
    for line in nt_lines:
        m = _NT_RE.match(line.strip())
        if not m:
            continue
        subj = m.group(1)[1:-1]
        pred = m.group(2)[1:-1]
        obj_nt = m.group(3).strip()
        node = nodes.setdefault(subj, {"@id": subj})
        node.setdefault(pred, []).append(_nt_obj_to_jsonld(obj_nt))
    return list(nodes.values())


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transform DDB-EDM JSONL to mocho-aligned RDF (N-Triples + JSON-LD)."
    )
    parser.add_argument("--jsonl",      default=DEFAULT_JSONL,      type=Path)
    parser.add_argument("--ids",        default=DEFAULT_IDS,        type=Path)
    parser.add_argument("--alignment",  default=DEFAULT_ALIGNMENT,  type=Path)
    parser.add_argument("--htype",      default=DEFAULT_HTYPE,      type=Path)
    parser.add_argument("--dctype",     default=DEFAULT_DCTYPE,     type=Path)
    parser.add_argument("--out-nt",     default=DEFAULT_OUT_NT,     type=Path, dest="out_nt")
    parser.add_argument("--out-jsonld", default=DEFAULT_OUT_JSONLD, type=Path, dest="out_jsonld")
    parser.add_argument("--stats",      default=DEFAULT_STATS,      type=Path)
    parser.add_argument("--limit",      default=0, type=int,
                        help="Stop after N records (0 = no limit, default)")
    args = parser.parse_args()

    print("Loading alignment table ...", file=sys.stderr)
    alignment, edm_iri_map = load_alignment(args.alignment)
    print(f"  {sum(len(v) for v in alignment.values())} candidate rows across "
          f"{len(alignment)} (entity_type, json_key) keys", file=sys.stderr)

    print("Loading htype map ...", file=sys.stderr)
    htype_map = load_htype_map(args.htype)
    print(f"  {len(htype_map)} htype codes mapped", file=sys.stderr)

    print("Loading dc:type dispatch table ...", file=sys.stderr)
    dctype_index = load_dctype_map(args.dctype)
    print(f"  {len(dctype_index)} dc:type dispatch entries", file=sys.stderr)

    print("Loading IDs filter ...", file=sys.stderr)
    ids_filter = load_ids(args.ids)
    print(f"  {len(ids_filter):,} IDs loaded", file=sys.stderr)

    stats: dict = {
        "records_processed":             0,
        "records_skipped_not_in_ids":    0,
        "triples_out":                   0,
        "objects_missing_specific_type": 0,
        "dctype_w_assigned":             0,  # W-slot replaced mocho:Manifestation
        "dctype_m_accumulated":          0,  # M-slot added alongside mocho:Manifestation
        "dctype_fallback":               0,  # D9 fallback (no dc:type match or empty slots)
        "webresources_typed":            0,  # mt002 WebResource triples emitted
        "whitelisted_keys": {
            "creator":     "rdam:P30263 has creator agent of manifestation",
            "contributor": "dc:contributor (no generic RDA equivalent in mocho)",
        },
    }
    ignored_keys: Counter = Counter()

    print(f"Streaming {args.jsonl.name} ...", file=sys.stderr)

    with (
        open(args.jsonl, encoding="utf-8")           as in_fh,
        open(args.out_nt, "w", encoding="utf-8")     as nt_fh,
        open(args.out_jsonld, "w", encoding="utf-8") as jld_fh,
    ):
        # JSON-LD header: {"@context": {...}, "@graph": [
        jld_fh.write('{\n  "@context": ')
        jld_fh.write(json.dumps(_JSONLD_CONTEXT, ensure_ascii=False))
        jld_fh.write(',\n  "@graph": [\n')
        first_node = True

        for lineno, raw_line in enumerate(in_fh):
            if args.limit and lineno >= args.limit:
                break
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                print(f"  WARNING line {lineno + 1}: JSON decode error: {exc}",
                      file=sys.stderr)
                continue

            nt_lines = transform_record(
                record, alignment, htype_map, dctype_index, ids_filter, stats, ignored_keys
            )
            if not nt_lines:
                continue

            # Write N-Triples
            for line in nt_lines:
                nt_fh.write(line + "\n")

            # Write JSON-LD nodes (one per subject in this record's triples)
            for node in nt_lines_to_jsonld_nodes(nt_lines):
                if not first_node:
                    jld_fh.write(",\n")
                jld_fh.write("    " + json.dumps(node, ensure_ascii=False))
                first_node = False

            if (lineno + 1) % 10_000 == 0:
                print(f"  {lineno + 1:,} lines, "
                      f"{stats['records_processed']:,} processed, "
                      f"{stats['triples_out']:,} triples", file=sys.stderr)

        jld_fh.write("\n  ]\n}\n")

    # Build stats output
    triples_ignored = sum(ignored_keys.values())
    ignored_properties = {
        k: {
            "count":   v,
            "edm_iri": edm_iri_map.get(tuple(k.split(".", 1))),
        }
        for k, v in ignored_keys.most_common()
    }
    stats_out = {
        **stats,
        "triples_ignored":     triples_ignored,
        "ignored_properties":  ignored_properties,
    }
    with open(args.stats, "w", encoding="utf-8") as fh:
        json.dump(stats_out, fh, indent=2, ensure_ascii=False)

    print(
        f"\nDone. {stats['records_processed']:,} records, "
        f"{stats['triples_out']:,} triples written, "
        f"{triples_ignored:,} values ignored.",
        file=sys.stderr,
    )
    print(
        f"  dc:type dispatch: W-slot={stats['dctype_w_assigned']:,}  "
        f"M-slot={stats['dctype_m_accumulated']:,}  "
        f"fallback={stats['dctype_fallback']:,}  "
        f"WebResources typed={stats['webresources_typed']:,}",
        file=sys.stderr,
    )
    print(f"  NT:     {args.out_nt}", file=sys.stderr)
    print(f"  JSON-LD:{args.out_jsonld}", file=sys.stderr)
    print(f"  Stats:  {args.stats}", file=sys.stderr)


if __name__ == "__main__":
    main()
