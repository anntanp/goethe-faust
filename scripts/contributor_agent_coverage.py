#!/usr/bin/env python3
"""
Purpose: For each ProvidedCHO.contributor, check whether a matching edm.RDF.Agent exists
         whose 'about' URI is a DDB organization or GND URI.
         Matching is attempted two ways: (1) URI: contributor.resource == agent.about,
         (2) Label: contributor.$ in agent.prefLabel[].$ (with comma-order normalization).
Usage:   python3 scripts/contributor_agent_coverage.py data/items-excerpt-1000.json
Inputs:  DDB items JSON array
Outputs: stdout summary + data/analysis/contributor_agent_coverage.csv
Dependencies: standard library only
"""

import json
import sys
import csv
from pathlib import Path
from collections import defaultdict

DDB_ORG  = 'http://www.deutsche-digitale-bibliothek.de/organization'
GND_BASE = 'http://d-nb.info/gnd/'


def is_target_uri(uri: str) -> bool:
    return uri.startswith(DDB_ORG) or uri.startswith(GND_BASE)


def coerce_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def flip_comma_name(name: str) -> str:
    """'Lastname, Firstname' -> 'Firstname Lastname' and vice versa."""
    if ',' in name:
        last, first = name.split(',', 1)
        return f"{first.strip()} {last.strip()}"
    parts = name.rsplit(' ', 1)
    return f"{parts[-1]}, {parts[0]}" if len(parts) == 2 else name


def name_variants(name: str) -> list[str]:
    """Return original + flipped form (deduplicated)."""
    flipped = flip_comma_name(name)
    return [name, flipped] if flipped != name else [name]


def agent_index(rdf: dict):
    """Build two indexes over Agent[]: {about_uri -> agent}, {norm_label -> [agent]}."""
    by_uri   = {}
    by_label = defaultdict(list)
    for agent in coerce_list(rdf.get('Agent')):
        if not isinstance(agent, dict):
            continue
        about = agent.get('about')
        if about:
            by_uri[about] = agent
        for pl in coerce_list(agent.get('prefLabel')):
            label = pl.get('$') if isinstance(pl, dict) else pl
            if label:
                for variant in name_variants(label.strip()):
                    by_label[variant].append(agent)
    return by_uri, by_label


def check_record(rdf: dict) -> list[dict]:
    """Return one row per contributor value with match details."""
    by_uri, by_label = agent_index(rdf)
    rows = []
    cho = rdf.get('ProvidedCHO', {})
    if not isinstance(cho, dict):
        return rows

    for contrib in coerce_list(cho.get('contributor')):
        if not isinstance(contrib, dict):
            contrib = {'$': str(contrib) if contrib else ''}

        c_label    = (contrib.get('$') or '').strip()
        c_resource = (contrib.get('resource') or '').strip()

        # --- URI match ---
        uri_match_agent  = by_uri.get(c_resource) if c_resource else None
        uri_match_target = is_target_uri(uri_match_agent['about']) if uri_match_agent else False

        # --- Label match (try original + flipped form) ---
        seen = set()
        label_match_agents = []
        for variant in (name_variants(c_label) if c_label else []):
            for a in by_label.get(variant, []):
                uid = id(a)
                if uid not in seen:
                    seen.add(uid)
                    label_match_agents.append(a)
        label_match_targets = [a for a in label_match_agents if is_target_uri(a.get('about', ''))]

        rows.append({
            'contributor_label':      c_label,
            'contributor_resource':   c_resource,
            'uri_match':              uri_match_agent is not None,
            'uri_match_target':       uri_match_target,
            'uri_match_about':        uri_match_agent['about'] if uri_match_agent else '',
            'label_match_count':      len(label_match_agents),
            'label_match_target':     len(label_match_targets) > 0,
            'label_match_abouts':     '|'.join(a.get('about', '') for a in label_match_targets),
        })
    return rows


def main(json_path: str):
    src = Path(json_path)
    with src.open() as f:
        records = json.load(f)
    if not isinstance(records, list):
        records = [records]

    all_rows = []
    for record in records:
        rdf = record.get('edm', {}).get('RDF', {})
        if isinstance(rdf, dict):
            all_rows.extend(check_record(rdf))

    total        = len(all_rows)
    has_resource = sum(1 for r in all_rows if r['contributor_resource'])
    uri_any      = sum(1 for r in all_rows if r['uri_match'])
    uri_target   = sum(1 for r in all_rows if r['uri_match_target'])
    label_any    = sum(1 for r in all_rows if r['label_match_count'] > 0)
    label_target = sum(1 for r in all_rows if r['label_match_target'])

    def pct(n, d):
        return f"{100 * n / d:.1f}%" if d else "n/a"

    print(f"Total contributor values:              {total}")
    print(f"  with a resource URI:                 {has_resource}  ({pct(has_resource, total)})")
    print()
    print(f"URI match (contributor.resource == agent.about):")
    print(f"  any agent matched:                   {uri_any}  ({pct(uri_any, total)})")
    print(f"  matched & agent is DDB org / GND:    {uri_target}  ({pct(uri_target, total)})")
    print()
    print(f"Label match (contributor.$ in agent.prefLabel):")
    print(f"  any agent matched:                   {label_any}  ({pct(label_any, total)})")
    print(f"  matched & agent is DDB org / GND:    {label_target}  ({pct(label_target, total)})")

    if not all_rows:
        print("\nNo contributor values found in corpus.")
        return

    out_csv = src.parent.parent / 'data' / 'analysis' / 'contributor_agent_coverage.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nRow-level CSV: {out_csv}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <json_file>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
