#!/usr/bin/env python3
"""
Purpose: Analyse dc:description on ProvidedCHO.
         Report value volume, literal vs URI split, and text length distribution
         broken down by sector (sparte). Tests hypothesis that Museum sector
         has the longest descriptions.
Usage:   python3 scripts/analyse_description.py [path/to/items.json]
Inputs:  DDB items JSONL (default: data/items-all-goethe-faust.json)
Outputs: stdout summary + data/analysis/description_by_sector.csv
Dependencies: standard library only
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

PROJECT  = Path(__file__).resolve().parent.parent
IN_PATH  = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT / "data" / "items-all-goethe-faust.json"
OUT_PATH = PROJECT / "data" / "analysis" / "description_by_sector.csv"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

SPARTE_BASE = "http://ddb.vocnet.org/sparte/"
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


def sparte_code(domains: list) -> str:
    for d in domains:
        if isinstance(d, str) and d.startswith(SPARTE_BASE):
            code = d[len(SPARTE_BASE):]
            return SPARTE_LABELS.get(code, code)
    return "unknown"


with IN_PATH.open() as fh:
    first = fh.read(1)
with IN_PATH.open() as fh:
    records = json.load(fh) if first == '[' else [json.loads(l) for l in fh if l.strip()]

total_records   = len(records)
records_with    = 0
total_values    = 0
has_resource    = 0

# per-sector: list of character lengths
sector_lengths  = defaultdict(list)
sector_counts   = Counter()   # records with description per sector
sector_total    = Counter()   # total records per sector

rows = []

for r in records:
    rdf     = r.get('edm', {}).get('RDF', {})
    cho     = rdf.get('ProvidedCHO', {})
    domains = r.get('provider-info', {}).get('domains', [])
    sector  = sparte_code(coerce_list(domains))
    sector_total[sector] += 1

    vals = coerce_list(cho.get('description'))
    has_desc = False
    for v in vals:
        if not isinstance(v, dict):
            continue
        label    = (v.get('$') or '').strip()
        resource = (v.get('resource') or '').strip()
        if not label and not resource:
            continue
        total_values += 1
        has_desc = True
        if resource:
            has_resource += 1
        length = len(label)
        if label:
            sector_lengths[sector].append(length)
        rows.append({
            'sector':    sector,
            'length':    length,
            'resource':  resource,
            'label_preview': label[:120],
        })

    if has_desc:
        records_with += 1
        sector_counts[sector] += 1


def pct(n, d): return f"{100*n/d:.1f}%" if d else "n/a"
def fmt(x): return f"{x:,.0f}"

print(f"Total records:                   {total_records:>8,}")
print(f"Records with description:        {records_with:>8,}  ({pct(records_with, total_records)})")
print(f"Total description values:        {total_values:>8,}")
print(f"  with resource URI:             {has_resource:>8,}  ({pct(has_resource, total_values)})")
print(f"  literal only:                  {total_values - has_resource:>8,}  ({pct(total_values - has_resource, total_values)})")
print()
print("Text length by sector (characters, literal values only):")
header = f"  {'Sector':<26} {'records':>8}  {'values':>8}  {'mean':>7}  {'median':>7}  {'max':>7}  {'coverage':>9}"
print(header)
print("  " + "-" * (len(header) - 2))
for sector in sorted(sector_lengths, key=lambda s: -mean(sector_lengths[s]) if sector_lengths[s] else 0):
    lengths = sector_lengths[sector]
    if not lengths:
        continue
    rec_n   = sector_counts[sector]
    tot_n   = sector_total[sector]
    print(f"  {sector:<26} {rec_n:>8,}  {len(lengths):>8,}  {mean(lengths):>7.0f}  {median(lengths):>7.0f}  {max(lengths):>7,}  {pct(rec_n, tot_n):>9}")

# sectors with no descriptions
for sector in sector_total:
    if sector not in sector_lengths:
        print(f"  {sector:<26} {'0':>8}  {'0':>8}  {'—':>7}  {'—':>7}  {'—':>7}  {pct(0, sector_total[sector]):>9}")

with OUT_PATH.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sector', 'length', 'resource', 'label_preview'])
    writer.writeheader()
    writer.writerows(rows)

print(f"\nOutput: {OUT_PATH}")
