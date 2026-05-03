#!/usr/bin/env python3
"""
Purpose: For each ProvidedCHO.spatial and ProvidedCHO.currentLocation value,
         check whether a matching edm:Place exists whose 'about' URI is a
         GeoNames, GND, or DDB organization URI.
         Matching via URI (resource == about) or label (prefLabel, with comma-order normalization).
Usage:   python3 scripts/analyse_locations.py data/items-all-goethe-faust.json
Inputs:  JSONL file — one DDB record per line
Outputs: stdout summary + data/analysis/locations_coverage.csv
Dependencies: standard library only
"""

import json
import re
import sys
import csv
from pathlib import Path
from collections import defaultdict, Counter

GEONAMES  = ('https://sws.geonames.org/', 'https://www.geonames.org/', 'http://sws.geonames.org/')
GND_BASE  = ('https://d-nb.info/gnd/', 'http://d-nb.info/gnd/')
DDB_ORG   = 'http://www.deutsche-digitale-bibliothek.de/organization'

ROLE_RE = re.compile(r'\s*\([^)]*\)\s*$')


def authority_type(uri: str) -> str:
    if any(uri.startswith(p) for p in GEONAMES):
        return 'GeoNames'
    if any(uri.startswith(p) for p in GND_BASE):
        return 'GND'
    if uri.startswith(DDB_ORG):
        return 'DDB'
    return ''


def coerce_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def extract_str(v) -> str:
    if isinstance(v, dict):
        return (v.get('$') or '').strip()
    return str(v).strip() if v else ''


def flip_comma_name(name: str) -> str:
    if ',' in name:
        last, first = name.split(',', 1)
        return f"{first.strip()} {last.strip()}"
    parts = name.rsplit(' ', 1)
    return f"{parts[-1]}, {parts[0]}" if len(parts) == 2 else name


def place_index(rdf: dict):
    by_uri   = {}
    by_label = defaultdict(list)
    for place in coerce_list(rdf.get('Place')):
        if not isinstance(place, dict):
            continue
        about = (place.get('about') or '').strip()
        if about:
            by_uri[about] = place
        for pl in coerce_list(place.get('prefLabel')):
            label = extract_str(pl)
            if label:
                by_label[label].append(place)
                flipped = flip_comma_name(label)
                if flipped != label:
                    by_label[flipped].append(place)
    return by_uri, by_label


def resolve(resource: str, label: str, by_uri: dict, by_label: dict) -> tuple[str, str]:
    """Return (match_type, authority_type) or ('', '')."""
    if resource:
        place = by_uri.get(resource)
        if place:
            auth = authority_type(resource)
            return 'uri', auth
    if label:
        candidates = by_label.get(label, [])
        if not candidates:
            stripped = ROLE_RE.sub('', label).strip()
            candidates = by_label.get(stripped, [])
        for p in candidates:
            about = p.get('about', '')
            auth = authority_type(about)
            if auth:
                return 'label', auth
        if candidates:
            return 'label', 'internal'
    return '', ''


def analyse_field(values, by_uri, by_label, field_name: str) -> list[dict]:
    rows = []
    for v in values:
        if not isinstance(v, dict):
            v = {'$': str(v) if v else ''}
        resource = (v.get('resource') or '').strip()
        label    = extract_str(v)
        match_type, auth = resolve(resource, label, by_uri, by_label)
        rows.append({
            'field':        field_name,
            'label':        label,
            'resource':     resource,
            'match_type':   match_type,
            'authority':    auth,
        })
    return rows


def main(json_path: str):
    src = Path(json_path)
    all_rows = []

    with src.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rdf = rec.get('edm', {}).get('RDF', {})
            if not isinstance(rdf, dict):
                continue
            by_uri, by_label = place_index(rdf)
            cho = rdf.get('ProvidedCHO', {})
            if not isinstance(cho, dict):
                continue

            spatial_vals = coerce_list(cho.get('spatial'))
            curloc_val   = cho.get('currentLocation')
            curloc_vals  = coerce_list(curloc_val) if curloc_val else []

            all_rows.extend(analyse_field(spatial_vals, by_uri, by_label, 'spatial'))
            all_rows.extend(analyse_field(curloc_vals,  by_uri, by_label, 'currentLocation'))

    def report(field: str):
        rows   = [r for r in all_rows if r['field'] == field]
        total  = len(rows)
        has_r  = sum(1 for r in rows if r['resource'])
        uri_m  = sum(1 for r in rows if r['match_type'] == 'uri')
        lbl_m  = sum(1 for r in rows if r['match_type'] == 'label')
        auth_c = Counter(r['authority'] for r in rows if r['authority'])

        def pct(n, d): return f"{100*n/d:.1f}%" if d else "n/a"

        print(f"  {field} ({total} values):")
        print(f"    with resource URI:              {has_r}  ({pct(has_r, total)})")
        print(f"    URI match → any Place:          {uri_m}  ({pct(uri_m, total)})")
        print(f"    Label match → authority Place:  {lbl_m}  ({pct(lbl_m, total)})")
        for auth in ('GeoNames', 'GND', 'DDB', 'internal'):
            n = auth_c.get(auth, 0)
            if n:
                print(f"      {auth:<12}                {n}  ({pct(n, total)})")

    print(f"Corpus: {src.name}")
    report('spatial')
    print()
    report('currentLocation')

    out_csv = src.parent.parent / 'data' / 'analysis' / 'locations_coverage.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['field','label','resource','match_type','authority'])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nRow-level CSV: {out_csv}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <jsonl_file>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
