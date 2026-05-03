#!/usr/bin/env python3
"""
Purpose: Extract all distinct edm:Event.hasType URIs and their occurrence counts
         across the full corpus. Used to identify LIDO event type vocabulary in use.
Usage:   python3 scripts/event_hastype_coverage.py data/items-all-goethe-faust.json
Inputs:  JSONL file — one DDB record per line
Outputs: stdout table + data/analysis/event_hastype_coverage.csv
Dependencies: standard library only
"""

import json
import csv
import sys
from collections import Counter
from pathlib import Path


def main(json_path: str):
    src = Path(json_path)
    counter = Counter()

    with src.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rdf = rec.get('edm', {}).get('RDF', {})
            events = rdf.get('Event', [])
            if not isinstance(events, list):
                events = [events] if events else []
            for ev in events:
                if not isinstance(ev, dict):
                    continue
                ht = ev.get('hasType')
                if isinstance(ht, dict):
                    r = (ht.get('resource') or '').strip()
                    t = (ht.get('$') or '').strip()
                    if r:
                        counter[(r, t)] += 1

    rows = [{'n': n, 'resource': r, 'label': t} for (r, t), n in counter.most_common()]

    print("n\tresource\tlabel")
    for row in rows:
        print("{}\t{}\t{}".format(row['n'], row['resource'], row['label']))

    out_csv = src.parent.parent / 'data' / 'analysis' / 'lido_event_types.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['n', 'resource', 'label'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nCSV: {out_csv}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <jsonl_file>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
