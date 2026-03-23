#!/usr/bin/env python3
"""
Purpose:  Extract edm.RDF.ProvidedCHO.title values from items JSON and check
          how many contain ISBD punctuation marks.
Usage:    python3 check_isbd_titles.py [--data PATH] [--report PATH]
Inputs:   items-all-goethe-faust.json (list of DDB item dicts)
Outputs:  console summary; optional Markdown report written to --report path
Dependencies: standard library only
Assumptions:  title field is a string, dict {"$": ...}, or list thereof
"""

import json
import re
import argparse
from collections import Counter
from pathlib import Path

DATA_DEFAULT = Path(__file__).parent.parent / "data" / "items-all-goethe-faust.json"

# ISBD punctuation patterns and their meaning
# Each tuple: (label, compiled regex)
ISBD_PATTERNS = [
    ("space-slash",    re.compile(r" /")),          # /  statement of responsibility
    ("space-colon",    re.compile(r" :")),           # :  other title info
    ("space-equals",   re.compile(r" =")),           # =  parallel title
    ("space-semi",     re.compile(r" ;")),           # ;  subsequent SoR / series
    ("ellipsis",       re.compile(r"\.\.\.|…")),     # … abbreviation / truncation
    ("sq-brackets",    re.compile(r"\[.+?\]")),      # [] supplied/inferred data
    ("trailing-dot",   re.compile(r"[^.]\.$")),      # terminal period (area end)
]


def extract_titles(item: dict) -> list[str]:
    """Pull all title strings from one item dict."""
    try:
        cho = item["edm"]["RDF"]["ProvidedCHO"]
    except (KeyError, TypeError):
        return []
    raw = cho.get("title")
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, dict):
        # {"$": "text", "lang": "..."} — single title as dict
        return [raw["$"]] if raw.get("$") else []
    if isinstance(raw, list):
        # each element may be {"$": "text", "lang": "..."} or a plain string
        out = []
        for t in raw:
            if isinstance(t, str):
                out.append(t)
            elif isinstance(t, dict) and t.get("$"):
                out.append(t["$"])
        return out
    return []


def check_isbd(title: str) -> list[str]:
    """Return list of ISBD pattern labels found in title."""
    return [label for label, pat in ISBD_PATTERNS if pat.search(title)]


def main(data_path: Path) -> None:
    with open(data_path, encoding="utf-8") as f:
        first = f.read(1)
        f.seek(0)
        if first == "[":
            items = json.load(f)
        else:
            # JSON Lines
            items = [json.loads(line) for line in f if line.strip()]

    total_items = len(items)
    all_titles: list[str] = []
    items_without_title = 0

    for item in items:
        titles = extract_titles(item)
        if not titles:
            items_without_title += 1
        all_titles.extend(titles)

    total_titles = len(all_titles)

    # Count ISBD matches
    pattern_counts = Counter()
    flagged_titles: list[tuple[str, list[str]]] = []

    for title in all_titles:
        hits = check_isbd(title)
        if hits:
            flagged_titles.append((title, hits))
            for h in hits:
                pattern_counts[h] += 1

    n_flagged = len(flagged_titles)

    print(f"Items total:          {total_items:>6}")
    print(f"Items without title:  {items_without_title:>6}")
    print(f"Titles total:         {total_titles:>6}")
    pct = n_flagged / total_titles * 100 if total_titles else 0
    print(f"Titles with ISBD:     {n_flagged:>6}  ({pct:.1f}%)")
    print()
    print("Pattern breakdown:")
    for label, pat in ISBD_PATTERNS:
        n = pattern_counts[label]
        print(f"  {label:<16} {n:>5}  ({n/total_titles*100:.1f}%)" if total_titles else f"  {label:<16} {n:>5}")

    print()
    print("Sample flagged titles (up to 20):")
    for title, hits in flagged_titles[:20]:
        print(f"  [{', '.join(hits)}]  {title!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check ISBD punctuation in DDB titles.")
    parser.add_argument("--data", type=Path, default=DATA_DEFAULT)
    args = parser.parse_args()
    main(args.data)
