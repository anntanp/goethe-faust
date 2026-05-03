#!/usr/bin/env python3
"""
Purpose: Check what % of records have ProvidedCHO.date / issued values that match
         edm:TimeSpan begin or end, and characterise the match types.
Usage:   python3 scripts/timespan_date_coverage.py data/items-all-goethe-faust.json
Inputs:  JSONL file — one DDB record per line
Outputs: stdout summary + data/analysis/timespan_date_coverage.csv
Dependencies: standard library only
Assumptions: TimeSpan is a single dict (not array); date[] are strings; issued[] have $ subfield
"""

import json
import re
import sys
import csv
from pathlib import Path
from collections import Counter

ROLE_RE  = re.compile(r'\s*\([^)]*\)\s*$')   # trailing "(role annotation)"
RANGE_RE = re.compile(r'^(.+)/(.+)$')         # ISO interval: begin/end


def coerce_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def extract_str(v) -> str:
    if isinstance(v, dict):
        return (v.get('$') or '').strip()
    return str(v).strip() if v else ''


def timespan_values(rdf: dict) -> tuple[str, str]:
    """Return (begin, end) strings from edm:TimeSpan; empty string if absent."""
    ts = rdf.get('TimeSpan')
    if not ts or not isinstance(ts, dict):
        return '', ''
    return extract_str(ts.get('begin')), extract_str(ts.get('end'))


def date_strings(rdf: dict) -> list[str]:
    cho = rdf.get('ProvidedCHO', {})
    if not isinstance(cho, dict):
        return []
    dates = [extract_str(v) for v in coerce_list(cho.get('date'))]
    issued = [extract_str(v) for v in coerce_list(cho.get('issued'))]
    return [s for s in dates + issued if s]


def match_type(raw: str, begin: str, end: str) -> str:
    """Return match classification or '' if no match."""
    ts_vals = {v for v in (begin, end) if v}
    if not ts_vals:
        return ''

    # 1. Exact
    if raw in ts_vals:
        return 'exact'

    # 2. Role-stripped
    stripped = ROLE_RE.sub('', raw).strip()
    if stripped != raw and stripped in ts_vals:
        return 'role_stripped'

    # 3. Range split: "begin/end"
    m = RANGE_RE.match(raw)
    if m:
        r_begin, r_end = m.group(1).strip(), m.group(2).strip()
        if r_begin == begin and r_end == end:
            return 'range_split'
        if r_begin in ts_vals or r_end in ts_vals:
            return 'range_partial'

    # 4. Substring containment (begin or end appears inside date string)
    for v in ts_vals:
        if v and v in raw:
            return 'substring'

    return ''


def analyse_record(rdf: dict) -> dict:
    begin, end = timespan_values(rdf)
    dates = date_strings(rdf)
    has_timespan = bool(begin or end)
    has_dates    = bool(dates)

    best = ''
    for d in dates:
        mt = match_type(d, begin, end)
        if mt:
            best = mt
            break   # first match wins for summary; CSV has per-record detail

    return {
        'has_timespan':  has_timespan,
        'has_dates':     has_dates,
        'both':          has_timespan and has_dates,
        'match':         best if (has_timespan and has_dates) else '',
        'n_dates':       len(dates),
        'ts_begin':      begin,
        'ts_end':        end,
        'date_values':   '|'.join(dates),
    }


def main(json_path: str):
    src = Path(json_path)
    rows = []
    with src.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rdf = rec.get('edm', {}).get('RDF', {})
            if isinstance(rdf, dict):
                rows.append(analyse_record(rdf))

    total         = len(rows)
    has_ts        = sum(1 for r in rows if r['has_timespan'])
    has_dates     = sum(1 for r in rows if r['has_dates'])
    both          = sum(1 for r in rows if r['both'])
    matched       = sum(1 for r in rows if r['match'])
    match_counts  = Counter(r['match'] for r in rows if r['match'])

    def pct(n, d):
        return f"{100 * n / d:.1f}%" if d else "n/a"

    print(f"Total records:                         {total}")
    print(f"  with TimeSpan (begin or end):         {has_ts}  ({pct(has_ts, total)})")
    print(f"  with date or issued:                  {has_dates}  ({pct(has_dates, total)})")
    print(f"  with both:                            {both}  ({pct(both, total)})")
    print()
    print(f"Of records with both:")
    print(f"  matched (any type):                   {matched}  ({pct(matched, both)})")
    for mtype in ('exact', 'role_stripped', 'range_split', 'range_partial', 'substring'):
        n = match_counts.get(mtype, 0)
        print(f"    {mtype:<20}          {n}  ({pct(n, both)})")
    no_match = both - matched
    print(f"  no match:                             {no_match}  ({pct(no_match, both)})")

    out_csv = src.parent.parent / 'data' / 'analysis' / 'timespan_date_coverage.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nRow-level CSV: {out_csv}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <jsonl_file>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
