#!/usr/bin/env python3
"""
Purpose: Analyse dc:language and dcterms:language co-occurrence on ProvidedCHO.
         Check whether both fields always denote the same language,
         and characterise value distributions and URI patterns.
Usage:   python3 scripts/analyse_language.py [path/to/items.json]
Inputs:  DDB items JSON array (default: data/items-all-goethe-faust.json)
Outputs: stdout summary + data/analysis/language_coverage.csv
Dependencies: standard library only
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
LOC_BASE = "http://id.loc.gov/vocabulary/iso639-2/"

IN_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT / "data" / "items-all-goethe-faust.json"
OUT_PATH = PROJECT / "data" / "analysis" / "language_coverage.csv"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def coerce_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def extract_lang_codes(v) -> list:
    """Return dc:language literals as-is (string or list of strings)."""
    return [x for x in coerce_list(v) if isinstance(x, str) and x]


def extract_dt_uris(v) -> list:
    """Return dcterms:language resource URIs from object list."""
    uris = []
    for item in coerce_list(v):
        if isinstance(item, dict):
            uri = item.get("resource") or ""
            if uri:
                uris.append(uri)
    return uris


def uri_to_code(uri: str):
    """Extract ISO 639-2 code from LOC URI, e.g. '…/ger' → 'ger'."""
    if uri.startswith(LOC_BASE):
        return uri[len(LOC_BASE):]
    return None


with IN_PATH.open() as f:
    first = f.read(1)
if first == "[":
    records = json.loads(first + IN_PATH.open().read()[1:])
else:
    records = [json.loads(line) for line in IN_PATH.open() if line.strip()]
total = len(records)

has_lang = 0
has_dt_lang = 0
has_both = 0
has_neither = 0
always_same = 0          # both present and codes match
mismatch = 0             # both present but at least one code differs
dt_not_loc = 0           # dcterms:language URI not from LOC base

lang_counter = Counter()
dt_uri_counter = Counter()
dt_code_counter = Counter()

rows = []  # (record_id, dc_language, dcterms_language_uri, code_match)

for r in records:
    cho = r.get("edm", {}).get("RDF", {}).get("ProvidedCHO", {})
    record_id = cho.get("about", "")

    lang_vals = extract_lang_codes(cho.get("language"))
    dt_uris = extract_dt_uris(cho.get("dcTermsLanguage"))

    if lang_vals:
        has_lang += 1
        for v in lang_vals:
            lang_counter[v] += 1

    if dt_uris:
        has_dt_lang += 1
        for uri in dt_uris:
            dt_uri_counter[uri] += 1
            code = uri_to_code(uri)
            if code:
                dt_code_counter[code] += 1
            else:
                dt_not_loc += 1

    if lang_vals and dt_uris:
        has_both += 1
        lang_set = set(lang_vals)
        dt_codes = {uri_to_code(u) for u in dt_uris if uri_to_code(u)}
        if lang_set == dt_codes:
            always_same += 1
        else:
            mismatch += 1

    if not lang_vals and not dt_uris:
        has_neither += 1

    for lv in lang_vals or [None]:
        for uri in dt_uris or [None]:
            if lv or uri:
                code = uri_to_code(uri) if uri else None
                rows.append({
                    "record_id": record_id,
                    "dc_language": lv or "",
                    "dcterms_language_uri": uri or "",
                    "dcterms_code": code or "",
                    "codes_match": (lv == code) if (lv and code) else "",
                })

with OUT_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["record_id", "dc_language", "dcterms_language_uri", "dcterms_code", "codes_match"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Total records:                   {total:>8,}")
print(f"Has dc:language:                 {has_lang:>8,}  ({has_lang/total:.1%})")
print(f"Has dcterms:language:            {has_dt_lang:>8,}  ({has_dt_lang/total:.1%})")
print(f"Has both:                        {has_both:>8,}  ({has_both/total:.1%})")
print(f"Has neither:                     {has_neither:>8,}  ({has_neither/total:.1%})")
print()
print(f"Both present, codes identical:   {always_same:>8,}  ({always_same/has_both:.1%} of has-both)")
print(f"Both present, codes differ:      {mismatch:>8,}  ({mismatch/has_both:.1%} of has-both)")
print(f"dcterms:language not LOC URI:    {dt_not_loc:>8,}")
print()
print("Top dc:language values:")
for v, n in lang_counter.most_common(10):
    print(f"  {v:<12} {n:>6,}")
print()
print("Top dcterms:language URIs:")
for v, n in dt_uri_counter.most_common(10):
    print(f"  {v:<60} {n:>6,}")
print()
print(f"Output: {OUT_PATH}")
