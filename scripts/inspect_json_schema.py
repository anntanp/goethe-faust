#!/usr/bin/env python3
"""
Purpose: Enumerate all leaf-node JSON paths across all records and classify value types.
Usage:   python3 scripts/inspect_json_schema.py data/items-excerpt-1000.json
Inputs:  JSON file — array of record objects
Outputs: stdout — sorted path list; leaf paths annotated with observed value types
         data/processed/json_schema_paths.csv — same data as CSV
Dependencies: standard library only
Assumptions: top-level JSON is a list of objects
"""

import json
import re
import sys
import csv
from collections import defaultdict
from pathlib import Path

UUID_RE = re.compile(r'^[0-9a-fA-F]{32}$')
URI_RE  = re.compile(r'^https?://')


def classify(value) -> str:
    if isinstance(value, bool):
        return 'Literals(string)'
    if isinstance(value, (int, float)):
        return 'Literals(numeric)'
    if isinstance(value, str):
        if URI_RE.match(value):
            return 'URI'
        if UUID_RE.match(value):
            return 'Literals(uuid)'
        return 'Literals(string)'
    return 'Literals(string)'


def walk(node, path: str, path_types: dict):
    """Recursively walk node; record value types at leaf nodes."""
    if isinstance(node, dict):
        for key, val in node.items():
            child_path = f"{path}.{key}" if path else key
            walk(val, child_path, path_types)
    elif isinstance(node, list):
        array_path = path + '[]'
        for item in node:
            if isinstance(item, (dict, list)):
                walk(item, array_path, path_types)
            else:
                path_types[array_path].add(classify(item))
        if not node:
            # empty array — mark as array node with no type
            path_types.setdefault(array_path, set())
    else:
        path_types[path].add(classify(node))


def all_prefixes(paths: list[str]) -> set[str]:
    """Return every non-leaf ancestor path (for structural lines without type annotation)."""
    prefixes = set()
    for p in paths:
        parts = p.replace('[]', '').split('.')
        for i in range(1, len(parts)):
            prefixes.add('.'.join(parts[:i]))
    return prefixes


def main(json_path: str):
    src = Path(json_path)
    with src.open() as f:
        records = json.load(f)

    if not isinstance(records, list):
        records = [records]

    path_types: dict[str, set] = defaultdict(set)

    for record in records:
        walk(record, '', path_types)

    # Remove empty-string key if present
    path_types.pop('', None)

    leaf_paths  = sorted(path_types.keys())
    struct_paths = all_prefixes(leaf_paths) - set(leaf_paths)

    # Merge for display
    all_paths = sorted(set(leaf_paths) | struct_paths)

    out_csv = src.parent.parent / 'data' / 'ddbedm' / 'json_schema_paths.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open('w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['path', 'value_types'])
        for p in all_paths:
            types = sorted(path_types.get(p, set()))
            writer.writerow([p, '|'.join(types)])

    for p in all_paths:
        types = sorted(path_types.get(p, set()))
        if types:
            print(f"{p},{','.join(types)}")
        else:
            print(p)

    print(f"\n# {len(leaf_paths)} leaf paths across {len(records)} records", file=sys.stderr)
    print(f"# CSV saved to {out_csv}", file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <json_file>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
