#!/usr/bin/env python3
# Purpose:  Frequency table of (mediatype, htype, dc_type) combinations for
#           a given DDB sector, cross-referenced against
#           lookup_dctype_to_class.csv to show current dispatch class.
# Usage:    python scripts/count_dctype_sparte004.py [--sector sparteNNN]
#           Default sector: sparte004
# Inputs:   data/items-all-goethe-faust.json  (JSONL)
#           output/config/lookup_dctype_to_class.csv
# Outputs:  output/dctype_<sector>.csv
#           Columns: mediatype, htype, dc_type_de, count,
#                    rdf_type_w, rdf_type_m, notes, mapped
# Deps:     stdlib only (json, csv, pathlib, collections, argparse)

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT   = Path(__file__).resolve().parents[1]
JSONL  = ROOT / "data" / "items-all-goethe-faust.json"
LOOKUP = ROOT / "output" / "lookup_dctype_to_class.csv"

MEDIATYPE_PFX   = "http://ddb.vocnet.org/medientyp/"
SECTOR_PFX      = "http://ddb.vocnet.org/sparte/"
HIERARCHIETYP   = "http://ddb.vocnet.org/hierarchietyp/"


def extract_mediatype_sector(concepts) -> tuple[str, str]:
    """Return (mediatype_iri, sector_iri) from Concept list."""
    mediatype = sector = "any"
    if not isinstance(concepts, list):
        concepts = [concepts] if isinstance(concepts, dict) else []
    for c in concepts:
        if not isinstance(c, dict):
            continue
        about = c.get("about") or ""
        if about.startswith(MEDIATYPE_PFX):
            mediatype = about
        elif about.startswith(SECTOR_PFX):
            sector = about
    return mediatype, sector


def extract_htype(cho: dict) -> str:
    """Return short htype code (e.g. 'ht021') or empty string."""
    raw = cho.get("hierarchyType") or ""
    if isinstance(raw, dict):
        raw = raw.get("$") or raw.get("resource") or ""
    raw = str(raw).strip()
    # full IRI or short code
    if HIERARCHIETYP in raw:
        return raw.split(HIERARCHIETYP)[-1]
    return raw if raw.startswith("ht") else ""


def extract_dc_types(cho: dict) -> list[str]:
    """Return dc:type literal values from ProvidedCHO."""
    raw = cho.get("type") or cho.get("dcType") or []
    if isinstance(raw, str):
        raw = [raw]
    elif isinstance(raw, dict):
        raw = [raw.get("$") or ""]
    results = []
    for v in raw:
        if isinstance(v, dict):
            v = v.get("$") or ""
        v = str(v).strip()
        if v:
            results.append(v)
    return results


def load_lookup() -> dict[tuple, dict]:
    """Return (mediatype, sector, dc_type_de) → row dict."""
    index: dict[tuple, dict] = {}
    with LOOKUP.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["mediatype"], row["sector"], row["dc_type_de"])
            index[key] = row
    return index


def lookup_class(index: dict, mediatype: str, sector_iri: str, dc_type_de: str) -> dict:
    """Three-level fallback: (mt, sector, dc) → (mt, any, dc) → (any, any, dc)."""
    return (
        index.get((mediatype, sector_iri, dc_type_de))
        or index.get((mediatype, "any", dc_type_de))
        or index.get(("any", "any", dc_type_de))
        or {}
    )


def mt_short(iri: str) -> str:
    return iri.split("/")[-1] if iri != "any" else "any"


def main() -> None:
    parser = argparse.ArgumentParser(description="dc:type frequency table for a DDB sector")
    parser.add_argument("--sector", default="sparte004",
                        help="Sector code, e.g. sparte001 (default: sparte004)")
    args = parser.parse_args()

    sector_code = args.sector
    sector_iri  = SECTOR_PFX + sector_code
    output      = ROOT / "output" / f"dctype_{sector_code}.csv"

    lookup = load_lookup()
    counter: Counter = Counter()
    total = 0

    with JSONL.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rdf = rec.get("edm", {}).get("RDF", {})
            mediatype, sector = extract_mediatype_sector(rdf.get("Concept"))
            if sector != sector_iri:
                continue
            total += 1
            cho = rdf.get("ProvidedCHO") or {}
            htype    = extract_htype(cho)
            dc_types = extract_dc_types(cho) or [""]
            mt = mt_short(mediatype)
            for dc in dc_types:
                counter[(mt, htype, dc)] += 1

    print(f"{sector_code} records : {total}")
    print(f"unique (mt, htype, dc_type) combinations: {len(counter)}\n")

    out_rows = []
    for (mt, htype, dc), count in sorted(counter.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        entry      = lookup_class(lookup, MEDIATYPE_PFX + mt if mt != "any" else "any", sector_iri, dc) if dc else {}
        rdf_type_w = entry.get("rdf_type_w", "")
        rdf_type_m = entry.get("rdf_type_m", "")
        notes      = entry.get("notes", "")
        mapped     = "yes" if (rdf_type_w or rdf_type_m) else ("no" if dc else "no-dctype")
        out_rows.append({
            "mediatype":  mt,
            "htype":      htype,
            "dc_type_de": dc,
            "count":      count,
            "rdf_type_w": rdf_type_w,
            "rdf_type_m": rdf_type_m,
            "notes":      notes,
            "mapped":     mapped,
        })

    fields = ["mediatype", "htype", "dc_type_de", "count", "rdf_type_w", "rdf_type_m", "notes", "mapped"]
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows → {output}\n")

    unmapped = [r for r in out_rows if r["mapped"] == "no"]
    mapped   = [r for r in out_rows if r["mapped"] == "yes"]

    print(f"--- mapped ({len(mapped)}) ---")
    for r in mapped:
        cls = r["rdf_type_w"] or r["rdf_type_m"]
        cls_short = cls.split("#")[-1] if "#" in cls else cls.split("/")[-1]
        print(f"  {r['count']:3d}  {r['mediatype']:<6}  {r['htype']:<8}  {r['dc_type_de']:<35s}  {cls_short}")

    print(f"\n--- unmapped ({len(unmapped)}) ---")
    for r in unmapped:
        print(f"  {r['count']:3d}  {r['mediatype']:<6}  {r['htype']:<8}  {r['dc_type_de']}")


if __name__ == "__main__":
    main()
