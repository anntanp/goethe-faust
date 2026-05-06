#!/usr/bin/env python3
# Purpose:  Split an N-Quads file into one N-Triples file per named graph.
#           The graph IRI is stripped from every quad; the output filename
#           encodes the target graph (slug = last path segment of the IRI).
#           NQ wrapping is deferred to QLever load time (transform-script-adr.md D28).
#
# Usage:    python scripts/split_nq.py output/goethe-faust.nq
#           python scripts/split_nq.py output/goethe-faust.nq --out-dir output/nt
#
# Inputs:   <nq-file>    — N-Quads file produced by transform_edm_to_mocho.py
#
# Outputs:  <out-dir>/<slug>.nt for each named graph IRI found in the input.
#           Default out-dir: same directory as the input file.
#           Example: graph IRI <…/graph/mocho> → mocho.nt
#
# Deps:     stdlib only (pathlib, argparse, collections)
# Assumptions: one quad per line; graph IRI is the fourth whitespace-delimited
#              token; line ends with " ." or ".\n" (standard NQ serialisation).

import argparse
from collections import defaultdict
from pathlib import Path


def split_nq(nq_path: Path, out_dir: Path) -> tuple[dict[str, int], int]:
    graphs: dict[str, list[str]] = defaultdict(list)
    skipped = 0

    with open(nq_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if not line or line.startswith("#"):
                continue
            # Graph IRI is always <...> — find the last " <" to avoid splitting
            # inside literal objects that may contain spaces.
            body = line.rstrip(" .")
            last_lt = body.rfind(" <")
            if last_lt == -1:
                skipped += 1
                continue
            graph_iri = body[last_lt + 1:]
            # Validate: must be a well-formed absolute IRI <scheme://...> with no spaces.
            # Fragments with no scheme (e.g. <br>, <;>) come from unescaped newlines in
            # literal values that split a quad across multiple file lines.
            if not (graph_iri.startswith("<") and graph_iri.endswith(">")
                    and " " not in graph_iri and "://" in graph_iri):
                skipped += 1
                continue
            triple = body[:last_lt] + " .\n"
            graphs[graph_iri].append(triple)

    out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for graph_iri, triples in graphs.items():
        slug = graph_iri.strip("<>").rstrip("/").rsplit("/", 1)[-1]
        out_path = out_dir / f"{slug}.nt"
        out_path.write_text("".join(triples), encoding="utf-8")
        counts[slug] = len(triples)

    return counts, skipped


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split an N-Quads file into per-graph N-Triples files."
    )
    parser.add_argument("nq_file", type=Path, help="Input .nq file")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: same directory as input file)",
    )
    args = parser.parse_args()

    nq_path: Path = args.nq_file.resolve()
    out_dir: Path = args.out_dir.resolve() if args.out_dir else nq_path.parent

    counts, skipped = split_nq(nq_path, out_dir)
    for slug, n in sorted(counts.items()):
        print(f"  {slug}.nt  {n:,} triples")
    if skipped:
        print(f"  WARNING: {skipped:,} lines skipped (malformed — likely unescaped newlines in literals)")


if __name__ == "__main__":
    main()
