#!/usr/bin/env python3
"""
Purpose:   Emit rdf:type triples for every DDB object in the Goethe-Faust corpus.
           Classification rule (OR): sector-2 (sparte002) OR htype signals
           manifestation → rda:Manifestation (rdaregistry C10007); else →
           mocho:Manifestation.
Usage:     python gen_manifestation_types.py [--jsonl FILE] [--out FILE]
Inputs:    data/items-all-goethe-faust.json   JSONL, one record per line
Outputs:   output/mocho-goethe-faust.nt       N-Triples
Deps:      stdlib only (json, argparse, pathlib)
Assumes:   JSONL: one JSON object per line; record structure edm.RDF.ProvidedCHO
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

DEFAULT_JSONL = PROJECT_DIR / "data"   / "items-all-goethe-faust.json"
DEFAULT_OUT   = Path("/Users/mta/Documents/claude/ddbkg/goethe-faust/data") / "mocho-goethe-faust.nt"

RDF_TYPE       = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
RDA_MANIFEST   = "http://rdaregistry.info/Elements/c/C10007"
MOCHO_MANIFEST = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation"

# htype codes that signal a manifestation-level object
HTYPE_MANIFEST = {
    "htype_007",   # Band / Volume
    "htype_013",   # Handschrift / Manuscript
    "htype_014",   # Heft / Issue
    "htype_020",   # Mehrbändiges Werk / Multivolume Work
    "htype_021",   # Monografie / Monograph
    "htype_025",   # Rezension / Review
}


def is_sector2(item: dict) -> bool:
    """Return True if the item or any parent institution belongs to sparte002."""
    pi = item.get("provider-info") or {}
    domains: list = pi.get("domains") or []
    parents: list = (pi.get("provider-parents") or {}).get("parents") or []
    parent_domains = [d for p in parents for d in (p.get("domains") or [])]
    all_domains = domains + parent_domains
    return any("sparte002" in (d or "") for d in all_domains)


def classify(item: dict) -> str:
    cho   = (item.get("edm") or {}).get("RDF", {}).get("ProvidedCHO") or {}
    htype = cho.get("hierarchyType")
    if is_sector2(item) or htype in HTYPE_MANIFEST:
        return RDA_MANIFEST
    return MOCHO_MANIFEST


def nt_triple(subject: str, predicate: str, obj: str) -> str:
    return f"<{subject}> <{predicate}> <{obj}> .\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate rdf:type N-Triples for Goethe-Faust corpus")
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL, help="Input JSONL file")
    parser.add_argument("--out",   type=Path, default=DEFAULT_OUT,   help="Output .nt file")
    args = parser.parse_args()

    if not args.jsonl.exists():
        sys.exit(f"Input file not found: {args.jsonl}")

    args.out.parent.mkdir(parents=True, exist_ok=True)

    total = skipped = rda_sector = rda_htype = mocho_count = 0

    with args.jsonl.open(encoding="utf-8") as fin, \
         args.out.open("w", encoding="utf-8") as fout:

        for lineno, line in enumerate(fin, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"  WARNING line {lineno}: JSON parse error — {exc}", file=sys.stderr)
                skipped += 1
                continue

            try:
                cho = (item.get("edm") or {}).get("RDF", {}).get("ProvidedCHO")
                if not cho:
                    raise ValueError("missing ProvidedCHO")
                uri = cho.get("about")
                if not uri:
                    raise ValueError("missing ProvidedCHO.about")
            except (KeyError, ValueError) as exc:
                print(f"  WARNING line {lineno}: {exc}", file=sys.stderr)
                skipped += 1
                continue

            htype = cho.get("hierarchyType")
            sector2 = is_sector2(item)
            htype_m = htype in HTYPE_MANIFEST

            if sector2 or htype_m:
                cls = RDA_MANIFEST
                if sector2:
                    rda_sector += 1
                else:
                    rda_htype += 1
            else:
                cls = MOCHO_MANIFEST
                mocho_count += 1

            fout.write(nt_triple(uri, RDF_TYPE, cls))
            total += 1

    print(f"Done.")
    print(f"  Total triples written : {total:,}")
    print(f"  rda:Manifestation     : {rda_sector + rda_htype:,}  "
          f"(sector2: {rda_sector:,}, htype: {rda_htype:,})")
    print(f"  mocho:Manifestation   : {mocho_count:,}")
    print(f"  Skipped               : {skipped:,}")
    print(f"  Output                : {args.out}")


if __name__ == "__main__":
    main()
