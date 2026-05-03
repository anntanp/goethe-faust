#!/usr/bin/env python3
"""
Purpose: Analyse dc:type (json key: dcType) on ProvidedCHO.
         For each dcType value, check:
           1. Whether it carries a resource URI, and which authority it belongs to.
           2. Whether a skos:Concept node in edm.RDF.Concept[] declares that URI as
              its 'about' value (URI match).
           3. Whether the Concept's prefLabel.$ matches the dcType.$ label (label match).
         Report separately for GND and DDB URIs per the task definition.
Usage:   python3 scripts/analyse_dctype.py [path/to/items.json]
Inputs:  DDB items JSON (JSONL or JSON array)
Outputs: stdout summary + data/analysis/dctype_coverage.csv
Dependencies: standard library only
         4. Break down linked-KB coverage by sector (sparte) from provider-info.domains[].
Usage:   python3 scripts/analyse_dctype.py [path/to/items.json]
Inputs:  DDB items JSON (JSONL or JSON array)
Outputs: stdout summary + data/analysis/dctype_coverage.csv
Dependencies: standard library only
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

PROJECT  = Path(__file__).resolve().parent.parent
IN_PATH  = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT / "data" / "items-all-goethe-faust.json"
OUT_PATH = PROJECT / "data" / "analysis" / "dctype_coverage.csv"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

GND_BASES    = ("http://d-nb.info/gnd/", "https://d-nb.info/gnd/")
DNB_BASES    = ("http://d-nb.info/",     "https://d-nb.info/")     # GND-Sachbegriff (non-/gnd/ path)
DDB_BASE     = "http://www.deutsche-digitale-bibliothek.de/"
SPARTE_BASE  = "http://ddb.vocnet.org/sparte/"

SPARTE_LABELS = {
    "sparte001": "Archive",
    "sparte002": "Library",
    "sparte003": "Monument Preservation",
    "sparte004": "Research",
    "sparte005": "Media Library",
    "sparte006": "Museum",
    "sparte007": "Others",
}


def coerce_list(v) -> list:
    return [] if v is None else (v if isinstance(v, list) else [v])


def uri_authority(uri: str) -> str:
    if any(uri.startswith(b) for b in GND_BASES):
        return "GND"
    if any(uri.startswith(b) for b in DNB_BASES):
        return "GND-Sachbegriff"
    if uri.startswith(DDB_BASE):
        return "DDB"
    netloc = urlparse(uri).netloc
    return netloc if netloc else "other"


def sparte_code(domains: list) -> str:
    for d in domains:
        if isinstance(d, str) and d.startswith(SPARTE_BASE):
            code = d[len(SPARTE_BASE):]
            return SPARTE_LABELS.get(code, code)
    return "unknown"


def norm_label(s) -> str:
    return (s or "").strip().lower()


with IN_PATH.open() as fh:
    first = fh.read(1)
with IN_PATH.open() as fh:
    if first == "[":
        records = json.load(fh)
    else:
        records = [json.loads(line) for line in fh if line.strip()]

total_records  = len(records)
total_dctype   = 0
has_resource   = 0
authority_ctr  = Counter()

# GND/DDB-specific counters
gnd_ddb_total          = 0
gnd_ddb_concept_uri    = 0
gnd_ddb_label_match    = 0

# sector breakdown: sector → {authority → count}
sector_authority_ctr   = defaultdict(Counter)
sector_total_ctr       = Counter()   # total dcType values per sector

rows = []

for r in records:
    rdf     = r.get("edm", {}).get("RDF", {})
    cho     = rdf.get("ProvidedCHO", {})
    domains = r.get("provider-info", {}).get("domains", [])
    sector  = sparte_code(coerce_list(domains))

    # build concept lookup: about → prefLabel.$
    concept_index = {}
    for c in coerce_list(rdf.get("Concept")):
        about = c.get("about") or ""
        pl = c.get("prefLabel")
        label = pl.get("$", "") if isinstance(pl, dict) else (pl or "")
        if about:
            concept_index[about] = label

    for dt in coerce_list(cho.get("dcType")):
        if not isinstance(dt, dict):
            continue
        total_dctype += 1
        resource = dt.get("resource") or ""
        label    = dt.get("$") or ""

        authority = uri_authority(resource) if resource else "none"
        sector_total_ctr[sector] += 1
        if resource:
            has_resource += 1
            authority_ctr[authority] += 1
            sector_authority_ctr[sector][authority] += 1

        concept_uri_match   = False
        concept_label_match = False

        if authority in ("GND", "GND-Sachbegriff", "DDB"):
            gnd_ddb_total += 1
            if resource in concept_index:
                concept_uri_match = True
                gnd_ddb_concept_uri += 1
                if norm_label(concept_index[resource]) == norm_label(label):
                    concept_label_match = True
                    gnd_ddb_label_match += 1

        rows.append({
            "record_id":           cho.get("about", ""),
            "sector":              sector,
            "dctype_label":        label,
            "dctype_resource":     resource,
            "authority":           authority,
            "concept_uri_match":   concept_uri_match,
            "concept_label_match": concept_label_match,
            "concept_prefLabel":   concept_index.get(resource, "") if resource else "",
        })

with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "record_id", "sector", "dctype_label", "dctype_resource",
        "authority", "concept_uri_match", "concept_label_match", "concept_prefLabel",
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Total records:                      {total_records:>8,}")
print(f"Total dcType values:                {total_dctype:>8,}")
print(f"  with resource URI:                {has_resource:>8,}  ({has_resource/total_dctype:.1%})")
print()
print("URI authority breakdown (values with resource):")
for auth, n in authority_ctr.most_common():
    print(f"  {auth:<40} {n:>6,}  ({n/has_resource:.1%})")
print()
print(f"GND / DDB / GND-Sachbegriff:        {gnd_ddb_total:>8,}")
if gnd_ddb_total:
    print(f"  Concept node found (URI match):   {gnd_ddb_concept_uri:>8,}  ({gnd_ddb_concept_uri/gnd_ddb_total:.1%})")
    print(f"  + prefLabel matches dcType.$:     {gnd_ddb_label_match:>8,}  ({gnd_ddb_label_match/gnd_ddb_total:.1%})")
print()
print("Linked-KB coverage by sector (dcType values with any external URI):")
kb_auths = ["GND", "GND-Sachbegriff", "vocab.getty.edu", "www.wikidata.org"]
header = f"  {'Sector':<26} {'total':>7}  " + "  ".join(f"{a.split('.')[0]:>10}" for a in kb_auths) + f"  {'linked%':>8}"
print(header)
for sector in sorted(sector_total_ctr, key=lambda s: -sector_total_ctr[s]):
    total_s  = sector_total_ctr[sector]
    linked_s = sum(sector_authority_ctr[sector].get(a, 0) for a in kb_auths)
    counts   = "  ".join(f"{sector_authority_ctr[sector].get(a,0):>10,}" for a in kb_auths)
    pct      = linked_s / total_s if total_s else 0
    print(f"  {sector:<26} {total_s:>7,}  {counts}  {pct:>8.1%}")
print()
print(f"Output: {OUT_PATH}")
