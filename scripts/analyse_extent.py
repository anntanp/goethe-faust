#!/usr/bin/env python3
"""
Purpose: Analyse dc:extent on ProvidedCHO.
         Report value volume, literal vs URI split, top values, and
         pattern breakdown (pagination, dimensions, other free-text).
Usage:   python3 scripts/analyse_extent.py [path/to/items.json]
Inputs:  DDB items JSONL (default: data/items-all-goethe-faust.json)
Outputs: stdout summary + data/analysis/extent_values.csv
Dependencies: standard library only
"""

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT  = Path(__file__).resolve().parent.parent
IN_PATH  = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT / "data" / "items-all-goethe-faust.json"
OUT_PATH = PROJECT / "data" / "analysis" / "extent_values.csv"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# pagination: "244 S.", "V, 244 S.", "3 Bl.", "32 p.", "S. 12-34"
RE_PAGINATION = re.compile(r'\b(S\.|Bl\.|Seiten?|Blatt|[Pp]ages?|p\.|fol\.)', re.IGNORECASE)
# dimensions: "8,5 x 12 x 2,2 cm", "21 × 15 cm", "30 mm"
RE_DIMENSIONS = re.compile(r'\d[\d,.]* *(x|×) *\d|(\d[\d,.]*) *(cm|mm|m\b)', re.IGNORECASE)


def coerce_list(v) -> list:
    return [] if v is None else (v if isinstance(v, list) else [v])


def classify(label: str) -> str:
    if RE_DIMENSIONS.search(label):
        return 'dimensions'
    if RE_PAGINATION.search(label):
        return 'pagination'
    return 'other'


with IN_PATH.open() as fh:
    first = fh.read(1)
with IN_PATH.open() as fh:
    records = json.load(fh) if first == '[' else [json.loads(l) for l in fh if l.strip()]

total_records  = len(records)
records_with   = 0
total_values   = 0
has_resource   = 0
pattern_ctr    = Counter()
label_ctr      = Counter()
rows           = []

for r in records:
    cho = r.get('edm', {}).get('RDF', {}).get('ProvidedCHO', {})
    record_id = cho.get('about', '')
    vals = coerce_list(cho.get('extent'))
    if not vals:
        continue
    records_with += 1
    for v in vals:
        if not isinstance(v, dict):
            continue
        total_values += 1
        resource = (v.get('resource') or '').strip()
        label    = (v.get('$') or '').strip()
        if resource:
            has_resource += 1
        pattern = classify(label) if label else 'no_label'
        pattern_ctr[pattern] += 1
        if label:
            label_ctr[label] += 1
        rows.append({
            'record_id': record_id,
            'label':     label,
            'resource':  resource,
            'pattern':   pattern,
        })

with OUT_PATH.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['record_id', 'label', 'resource', 'pattern'])
    writer.writeheader()
    writer.writerows(rows)

def pct(n, d): return f"{100*n/d:.1f}%" if d else "n/a"

print(f"Total records:                   {total_records:>8,}")
print(f"Records with extent:             {records_with:>8,}  ({pct(records_with, total_records)})")
print(f"Total extent values:             {total_values:>8,}")
print(f"  with resource URI:             {has_resource:>8,}  ({pct(has_resource, total_values)})")
print(f"  literal only:                  {total_values - has_resource:>8,}  ({pct(total_values - has_resource, total_values)})")
print()
print("Value pattern breakdown:")
for pat, n in pattern_ctr.most_common():
    print(f"  {pat:<16} {n:>7,}  ({pct(n, total_values)})")
print()
print("Top 20 extent values:")
for val, n in label_ctr.most_common(20):
    print(f"  {n:>5,}  {val}")
print()
print(f"Distinct values: {len(label_ctr):,}")
print(f"Output: {OUT_PATH}")
