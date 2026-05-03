#!/usr/bin/env python3
"""
Purpose: For each record, check whether ProvidedCHO.spatial[].resource URIs
         overlap with edm:Event.happenedAt[].resource URIs (same Place about URI).
         Reports: what % of spatial values are also referenced via happenedAt.
Usage:   python3 scripts/analyse_spatial_event_overlap.py data/items-all-goethe-faust.json
Inputs:  JSONL file — one DDB record per line
Outputs: stdout summary + data/analysis/spatial_event_overlap.csv
Dependencies: standard library only
"""

import csv
import json
import sys
from pathlib import Path
from collections import Counter


def coerce_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def main(json_path: str):
    src = Path(json_path)

    total_spatial = 0
    has_resource  = 0
    overlap_exact = 0

    hastype_counter = Counter()  # hasType.resource → count of matched spatial values
    rows = []

    with src.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rdf = rec.get('edm', {}).get('RDF', {})
            if not isinstance(rdf, dict):
                continue

            cho = rdf.get('ProvidedCHO', {})
            if not isinstance(cho, dict):
                continue

            # map happenedAt URI → set of hasType URIs for the event(s) that use it
            happened_at_to_hastypes: dict[str, set] = {}
            for ev in coerce_list(rdf.get('Event')):
                if not isinstance(ev, dict):
                    continue
                ht = ev.get('hasType')
                hastype_uri = ''
                if isinstance(ht, dict):
                    hastype_uri = (ht.get('resource') or '').strip()
                elif isinstance(ht, str):
                    hastype_uri = ht.strip()
                for ha in coerce_list(ev.get('happenedAt')):
                    if isinstance(ha, dict):
                        r = (ha.get('resource') or '').strip()
                    elif isinstance(ha, str):
                        r = ha.strip()
                    else:
                        continue
                    if r:
                        happened_at_to_hastypes.setdefault(r, set()).add(hastype_uri)

            for sp in coerce_list(cho.get('spatial')):
                if not isinstance(sp, dict):
                    continue
                total_spatial += 1
                resource = (sp.get('resource') or '').strip()
                label    = (sp.get('$') or '').strip()

                in_happened_at = False
                matched_hastypes = ''
                if resource:
                    has_resource += 1
                    if resource in happened_at_to_hastypes:
                        overlap_exact += 1
                        in_happened_at = True
                        types = happened_at_to_hastypes[resource]
                        matched_hastypes = '|'.join(sorted(t for t in types if t))
                        for t in types:
                            if t:
                                hastype_counter[t] += 1

                rows.append({
                    'spatial_resource':  resource,
                    'spatial_label':     label,
                    'in_happenedAt':     in_happened_at,
                    'matched_hastypes':  matched_hastypes,
                })

    def pct(n, d):
        return f"{100*n/d:.1f}%" if d else "n/a"

    print(f"Corpus: {src.name}")
    print(f"Total spatial values:              {total_spatial:>8,}")
    print(f"  with resource URI:               {has_resource:>8,}  ({pct(has_resource, total_spatial)})")
    print(f"  URI also in Event.happenedAt:    {overlap_exact:>8,}  ({pct(overlap_exact, total_spatial)} of all / {pct(overlap_exact, has_resource)} of with-URI)")
    print()
    print("Event hasType URIs for matched spatial values:")
    for uri, n in hastype_counter.most_common():
        print(f"  {n:>6,}  {uri}")

    out_csv = src.parent.parent / 'data' / 'analysis' / 'spatial_event_overlap.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['spatial_resource', 'spatial_label', 'in_happenedAt', 'matched_hastypes'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nRow-level CSV: {out_csv}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <jsonl_file>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
