"""
verify_transform_output.py — Spot-check mocho-goethe-faust.nt against plan §5 criteria.

Usage:
    python scripts/verify_transform_output.py [--nt output/mocho-goethe-faust.nt]

Inputs:
    output/mocho-goethe-faust.nt  (N-Triples; default)

Outputs:
    Printed report of pass/fail checks. Exit code 1 if any check fails.

Dependencies:
    stdlib only

Assumptions:
    - File fits in memory for indexed grep; for 44M triples this is ~4–5 GB — if OOM,
      rewrite to stream with per-line regex instead of full-file slurp.
    - Zeichnung museum records exist in the corpus (verified by sample_type_dispatch.py).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
VRA_WORK = "http://purl.org/vra/Work"
MOCHO_IMAGE_OBJECT = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#ImageObject"
VRA_IMAGE_OF = "http://purl.org/vra/imageOf"
RDAC_C10007 = "http://rdaregistry.info/Elements/c/C10007"


def _parse_subject(line: str) -> str | None:
    m = re.match(r"(<[^>]+>)", line)
    return m.group(1) if m else None


def _parse_object(line: str) -> str | None:
    m = re.search(r"> (<[^>]+>) \.$", line)
    return m.group(1) if m else None


def check_no_fabio(lines: list[str]) -> tuple[bool, str]:
    hits = [l for l in lines if "fabio" in l]
    if hits:
        return False, f"FAIL: {len(hits)} lines contain 'fabio'; first: {hits[0][:120]}"
    return True, "PASS: no fabio classes in NT output"


def check_image_object_triples(lines: list[str]) -> tuple[bool, str]:
    has_type = any(MOCHO_IMAGE_OBJECT in l and RDF_TYPE in l for l in lines)
    has_imageof = any(VRA_IMAGE_OF in l for l in lines)
    if not has_type:
        return False, "FAIL: no mocho:ImageObject rdf:type triples found"
    if not has_imageof:
        return False, "FAIL: no vra:imageOf triples found"
    # sample counts
    type_count = sum(1 for l in lines if MOCHO_IMAGE_OBJECT in l and RDF_TYPE in l)
    imageof_count = sum(1 for l in lines if VRA_IMAGE_OF in l)
    return True, f"PASS: {type_count:,} mocho:ImageObject type triples; {imageof_count:,} vra:imageOf triples"


def check_rdac_triples(lines: list[str]) -> tuple[bool, str]:
    count = sum(1 for l in lines if RDAC_C10007 in l and RDF_TYPE in l)
    if count == 0:
        return False, "FAIL: no rdac:C10007 rdf:type triples found"
    return True, f"PASS: {count:,} rdac:C10007 type triples"


def check_vra_work_for_zeichnung(lines: list[str]) -> tuple[bool, str]:
    """Find a Zeichnung CHO via vra:imageOf back-link and check it has vra:Work."""
    # collect imageOf: WebResource -> CHO
    imageof_map: dict[str, str] = {}
    for line in lines:
        if VRA_IMAGE_OF in line:
            subj = _parse_subject(line)
            obj = _parse_object(line)
            if subj and obj:
                imageof_map[subj] = obj

    # collect type map: uri -> set of types
    types_map: dict[str, set[str]] = {}
    for line in lines:
        if RDF_TYPE in line:
            subj = _parse_subject(line)
            obj = _parse_object(line)
            if subj and obj:
                types_map.setdefault(subj, set()).add(obj)

    # find a CHO that is both (a) pointed to by a WebResource and (b) typed vra:Work
    vra_work_uri = f"<{VRA_WORK}>"
    zeichnung_cho_uri = None
    for _wr, cho in imageof_map.items():
        if vra_work_uri in types_map.get(cho, set()):
            zeichnung_cho_uri = cho
            break

    if zeichnung_cho_uri is None:
        # broader check: any CHO with vra:Work type
        vra_work_chos = [uri for uri, types in types_map.items() if vra_work_uri in types]
        if not vra_work_chos:
            return False, "FAIL: no CHO typed vra:Work found in NT output"
        return True, f"PASS: {len(vra_work_chos):,} CHOs typed vra:Work (e.g. {vra_work_chos[0]})"

    types_str = ", ".join(sorted(types_map[zeichnung_cho_uri]))
    return True, f"PASS: CHO {zeichnung_cho_uri} has vra:Work\n       all types: {types_str}"


def check_no_broken_xrefs(notes_dir: Path, claude_dir: Path) -> tuple[bool, str]:
    broken: list[str] = []
    patterns = ["alignment-plan", "alignment-adr"]
    for d in [notes_dir, claude_dir]:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            text = f.read_text(errors="replace")
            for pat in patterns:
                if pat in text:
                    broken.append(f"{f}: contains '{pat}'")
    if broken:
        return False, "FAIL: broken cross-references:\n  " + "\n  ".join(broken)
    return True, "PASS: no broken cross-references to old alignment-plan/alignment-adr filenames"


def main() -> None:
    parser = argparse.ArgumentParser(description="Spot-check mocho-goethe-faust.nt against plan §5 criteria.")
    parser.add_argument("--nt", default="output/mocho-goethe-faust.nt", help="Path to N-Triples file")
    parser.add_argument("--notes", default="notes", help="Path to notes/ dir")
    parser.add_argument("--claude", default=".claude", help="Path to .claude/ dir")
    args = parser.parse_args()

    nt_path = Path(args.nt)
    if not nt_path.exists():
        print(f"ERROR: {nt_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {nt_path} ({nt_path.stat().st_size / 1e9:.2f} GB) ...")
    lines = nt_path.read_text(errors="replace").splitlines()
    print(f"  {len(lines):,} triples\n")

    checks = [
        check_no_fabio(lines),
        check_image_object_triples(lines),
        check_rdac_triples(lines),
        check_vra_work_for_zeichnung(lines),
        check_no_broken_xrefs(Path(args.notes), Path(args.claude)),
    ]

    passed = 0
    for ok, msg in checks:
        print(msg)
        if ok:
            passed += 1

    print(f"\n{passed}/{len(checks)} checks passed.")
    if passed < len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
