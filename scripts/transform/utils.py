"""Utility functions: N-Quads formatting, URI minting, value normalisation."""

from __future__ import annotations

import re
from collections import Counter

from .constants import (
    AgentDict, NQuad, NQList,
    GEMEA_BASE, DDB_ITEM_BASE,
    _PREFIXES, _MEDIATYPE_PREFIX, _SECTOR_PREFIX,
)

# Characters forbidden inside N-Triples IRI references (RFC 3987 + NT spec)
_IRI_UNSAFE_RE = re.compile(r'[\x00-\x20<>"{}|\\^`\x7f]')


def _sanitize_iri(iri: str) -> str:
    """Percent-encode characters illegal inside NT IRI references."""
    return _IRI_UNSAFE_RE.sub(lambda m: f"%{ord(m.group()):02X}", iri)


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
    """Escape characters illegal in N-Triples/N-Quads literal content."""
    return (s.replace("\\", "\\\\")
             .replace('"', '\\"')
             .replace("\n", "\\n")
             .replace("\r", "\\r")
             .replace("\t", "\\t"))


def value_to_nt_obj(val: object, sani_ctr: Counter | None = None) -> list[str]:
    """Convert a JSONL field value to a list of N-Triples object strings.

    Handles all value shapes produced by the DDB EDM JSONL:
      None / ""                    → []
      str (non-empty)              → ['"escaped"']
      list                         → recurse and flatten
      {"resource": IRI}            → ["<IRI>"] (IRI percent-encoded if unsafe chars present)
      {"lang": L, "$": T}          → ['"T"@L']
      {"lang": null, "$": T}       → ['"T"']
      {"resource": null, "$": ""}  → []

    sani_ctr: if provided, incremented once per IRI that required sanitisation.
    """
    if val is None:
        return []
    if isinstance(val, str):
        return [f'"{_escape_literal(val)}"'] if val else []
    if isinstance(val, list):
        result = []
        for item in val:
            result.extend(value_to_nt_obj(item, sani_ctr))
        return result
    if isinstance(val, dict):
        resource = val.get("resource")
        if resource:
            parts = resource.split()  # split handles multi-URI values (DDB data quality issue)
            result = []
            for uri in parts:
                sanitized = _sanitize_iri(uri)
                if sani_ctr is not None and sanitized != uri:
                    sani_ctr["uri_sanitized"] += 1
                result.append(f"<{sanitized}>")
            if sani_ctr is not None and len(parts) > 1:
                sani_ctr["uri_split"] += len(parts)
            return result
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
