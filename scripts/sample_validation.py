#!/usr/bin/env python3
# Purpose:  Sample one DDB object per §1.1 dispatch rule for manual validation.
#           For sparte005 rows, emits 3 sub-rows with distinct dc:type values.
# Usage:    python scripts/sample_validation.py [--seed N]
# Inputs:   data/items-all-goethe-faust.json (JSONL)
# Outputs:  output/validation_sample.csv
#           Columns: sparte, mediatype, htype, dc_type, ddb_url, w_class, m_class
# Deps:     stdlib only
# Assumptions:
#   - Sector IRI: http://ddb.vocnet.org/sparte/sparteNNN
#   - Mediatype IRI: http://ddb.vocnet.org/medientyp/mtNNN
#   - htype from ProvidedCHO.hierarchyType (string "htype_NNN" → "htNNN")
#   - dc:type from ProvidedCHO.dcType[].$ (first non-empty literal)
#   - DDB item URL: https://www.deutsche-digitale-bibliothek.de/item/<item-id>

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Optional

ROOT   = Path(__file__).resolve().parents[1]
JSONL  = ROOT / "data" / "items-all-goethe-faust.json"
OUTPUT = ROOT / "output" / "validation_sample.csv"

SECTOR_PFX    = "http://ddb.vocnet.org/sparte/"
MEDIATYPE_PFX = "http://ddb.vocnet.org/medientyp/"
HIERARCHIETYP = "http://ddb.vocnet.org/hierarchietyp/"
DDB_ITEM_BASE = "https://www.deutsche-digitale-bibliothek.de/item/"

SECTOR_LABELS = {
    "sparte001": "Archive",
    "sparte002": "Library",
    "sparte003": "Monument Preservation",
    "sparte004": "Research",
    "sparte005": "Media Library",
    "sparte006": "Museum",
    "sparte007": "Others",
}
MT_LABELS = {
    "mt001": "Audio",
    "mt002": "Photo",
    "mt003": "Text",
    "mt005": "Video",
    "mt007": "Not Digitized",
}

# (sparte, mt, htype, w_class, m_class)
# mt="*" = any mediatype (htype-driven rows)
# htype="" = no htype filter (mediatype-driven rows)
# SPARTE005_DC_TYPES = 3 indicates the row is expanded to 3 dc:type sub-rows
RULES = [
    # sparte001 Archive — htype layer (WEMI=—; rico class placed in w_class)
    ("sparte001", "*",    "ht048", "rico:RecordSet + ric-rst:Collection + vocnet-htype:ht048", ""),
    ("sparte001", "*",    "ht037", "rico:RecordSet + ric-rst:Collection + vocnet-htype:ht037", ""),
    ("sparte001", "*",    "ht036", "rico:RecordSet + ric-rst:Collection + vocnet-htype:ht036", ""),
    ("sparte001", "*",    "ht030", "rico:RecordSet + ric-rst:Fonds + vocnet-htype:ht030",      ""),
    ("sparte001", "*",    "ht031", "rico:RecordSet + ric-rst:Series + vocnet-htype:ht031",     ""),
    ("sparte001", "*",    "ht032", "rico:RecordSet + ric-rst:Series + vocnet-htype:ht032",     ""),
    ("sparte001", "*",    "ht033", "rico:RecordSet + ric-rst:Series + vocnet-htype:ht033",     ""),
    ("sparte001", "*",    "ht034", "rico:Record",    ""),
    ("sparte001", "*",    "ht035", "rico:RecordPart", ""),
    # sparte001 Archive — mediatype layer (cumulative with htype)
    ("sparte001", "mt001", "",    "",                 "aco:AudioManifestation"),
    ("sparte001", "mt002", "",    "",                 "mocho:ImageManifestation"),
    ("sparte001", "mt003", "",    "",                 "mocho:Manifestation"),
    ("sparte001", "mt005", "",    "ec:EditorialWork", "ec:MediaResource"),
    ("sparte001", "mt007", "",    "",                 ""),  # htype dispatch only; no media class

    # sparte002 Library — htype layer (mt003)
    ("sparte002", "mt003", "ht001", "",                    "doco:Section + rdac:C10007"),
    ("sparte002", "mt003", "ht002", "",                    "doco:Appendix + rdac:C10007"),
    ("sparte002", "mt003", "ht003", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht004", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht005", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht006", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht007", "",                    "doco:Part + rdac:C10007"),
    ("sparte002", "mt003", "ht008", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht009", "",                    "doco:Section + rdac:C10007"),
    ("sparte002", "mt003", "ht010", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht011", "",                    "doco:Part + rdac:C10007"),
    ("sparte002", "mt003", "ht012", "",                    "doco:TextChunk + rdac:C10007"),
    ("sparte002", "mt003", "ht013", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht014", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht015", "mocho:ImageWork",     "doco:Figure + rdac:C10007"),
    ("sparte002", "mt003", "ht016", "",                    "doco:Index + rdac:C10007"),
    ("sparte002", "mt003", "ht017", "",                    "doco:TableOfContents + rdac:C10007"),
    ("sparte002", "mt003", "ht018", "",                    "doco:Chapter + rdac:C10007"),
    ("sparte002", "mt003", "ht019", "mocho:ImageWork",     "doco:Figure + rdac:C10007"),
    ("sparte002", "mt003", "ht020", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht021", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht022", "rdac:C10001 + mo:MusicalWork", "rdac:C10007"),
    ("sparte002", "mt003", "ht023", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht024", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht025", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht026", "",                    "doco:TextChunk + rdac:C10007"),
    ("sparte002", "mt003", "ht027", "",                    "doco:Stanza + rdac:C10007"),
    ("sparte002", "mt003", "ht028", "",                    "doco:Preface + rdac:C10007"),
    ("sparte002", "mt003", "ht029", "",                    "rdac:C10007"),
    ("sparte002", "mt003", "ht044", "rdac:C10001",         "rdac:C10007"),
    ("sparte002", "mt003", "ht045", "",                    "doco:Part + rdac:C10007"),
    ("sparte002", "mt003", "ht046", "",                    "doco:Part + rdac:C10007"),
    ("sparte002", "mt003", "ht047", "",                    "doco:Part + rdac:C10007"),
    # sparte002 Library — mediatype layer
    ("sparte002", "mt001", "",    "",                 "aco:AudioManifestation"),
    ("sparte002", "mt002", "",    "",                 "mocho:ImageManifestation"),
    ("sparte002", "mt005", "",    "ec:EditorialWork", "ec:MediaResource"),
    ("sparte002", "mt007", "",    "",                 "rdac:C10007"),

    # sparte003 Monument Preservation
    ("sparte003", "mt001", "",    "mocho:ImmovableWork", "aco:AudioManifestation"),
    ("sparte003", "mt002", "",    "mocho:ImmovableWork", "mocho:ImageManifestation"),
    ("sparte003", "mt003", "",    "mocho:ImmovableWork", "rdac:C10007"),
    ("sparte003", "mt005", "",    "mocho:ImmovableWork", "ec:MediaResource"),
    ("sparte003", "mt007", "",    "mocho:ImmovableWork", ""),

    # sparte004 Research
    ("sparte004", "mt001", "",    "",                 "aco:AudioManifestation"),
    ("sparte004", "mt002", "",    "",                 "mocho:ImageManifestation"),
    ("sparte004", "mt003", "",    "",                 "rdac:C10007"),
    ("sparte004", "mt005", "",    "",                 "ec:MediaResource"),
    ("sparte004", "mt007", "",    "",                 "mocho:Manifestation"),

    # sparte005 Media Library — dc:type driven; each row expands to 3 dc:type sub-rows
    ("sparte005", "mt001", "",    "",                 "aco:AudioManifestation"),
    ("sparte005", "mt002", "",    "mocho:ImageWork",  "mocho:ImageManifestation"),
    ("sparte005", "mt005", "",    "ec:EditorialWork", "ec:MediaResource"),

    # sparte006 Museum
    ("sparte006", "mt002", "",    "vra:Work",         "vra:Image"),
    ("sparte006", "mt005", "",    "ec:EditorialWork", "ec:MediaResource"),

    # sparte007 Others
    ("sparte007", "mt002", "",    "",                 "mocho:ImageManifestation"),

    # Fallback
    ("*",         "*",     "",    "",                 "mocho:Manifestation"),
]


def coerce_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def extract_fields(record: dict) -> Optional[dict]:
    """Extract (sector, mt, ht, dc_type, item_id) from a JSONL record."""
    rdf     = record.get("edm", {}).get("RDF", {})
    cho     = rdf.get("ProvidedCHO", {})
    concepts = coerce_list(rdf.get("Concept"))

    sector = mt = ""
    for c in concepts:
        if not isinstance(c, dict):
            continue
        about = c.get("about") or ""
        if about.startswith(SECTOR_PFX):
            sector = about[len(SECTOR_PFX):]
        elif about.startswith(MEDIATYPE_PFX):
            mt = about[len(MEDIATYPE_PFX):]

    if not sector or not mt:
        return None

    # htype: "htype_NNN" → "htNNN"
    raw_ht = cho.get("hierarchyType") or ""
    if isinstance(raw_ht, dict):
        raw_ht = raw_ht.get("$") or raw_ht.get("resource") or ""
    raw_ht = str(raw_ht).strip()
    if HIERARCHIETYP in raw_ht:
        raw_ht = raw_ht.split(HIERARCHIETYP)[-1]
    # normalise "htype_NNN" → "htNNN"
    if raw_ht.startswith("htype_"):
        raw_ht = "ht" + raw_ht[len("htype_"):]
    ht = raw_ht if raw_ht.startswith("ht") else ""

    # dc:type: first non-empty literal
    dc_type = ""
    for dt in coerce_list(cho.get("dcType")):
        if isinstance(dt, dict):
            val = (dt.get("$") or "").strip()
        else:
            val = str(dt).strip()
        if val:
            dc_type = val
            break

    item_id = (
        record.get("properties", {}).get("item-id")
        or record.get("indexing-profile", {}).get("item-id")
        or ""
    )

    return {"sector": sector, "mt": mt, "ht": ht, "dc_type": dc_type, "item_id": item_id}


def build_index(jsonl_path: Path) -> list[dict]:
    records = []
    with jsonl_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                continue
            f = extract_fields(raw)
            if f and f["item_id"]:
                records.append(f)
    return records


def sample_rule(records: list[dict], sector: str, mt: str, ht: str, n: int = 1) -> list[dict]:
    candidates = [
        r for r in records
        if (sector == "*" or r["sector"] == sector)
        and (mt == "*" or r["mt"] == mt)
        and (ht == "" or r["ht"] == ht)
    ]
    if not candidates:
        return []
    return random.sample(candidates, min(n, len(candidates)))


def sample_sparte005_dctypes(records: list[dict], mt: str, n: int = 3) -> list[dict]:
    """Return up to n records with distinct dc:type values for sparte005 × mt."""
    candidates = [
        r for r in records
        if r["sector"] == "sparte005" and r["mt"] == mt and r["dc_type"]
    ]
    by_type: dict[str, list] = defaultdict(list)
    for r in candidates:
        by_type[r["dc_type"]].append(r)
    chosen_types = random.sample(sorted(by_type), min(n, len(by_type)))
    return [random.choice(by_type[dt]) for dt in chosen_types]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    random.seed(args.seed)

    print(f"Reading {JSONL} …")
    all_records = build_index(JSONL)
    print(f"  {len(all_records):,} records indexed")

    out_rows = []
    missing  = []

    for sector, mt, ht, w_class, m_class in RULES:
        is_sparte005 = sector == "sparte005"
        sparte_label = SECTOR_LABELS.get(sector, sector)
        mt_label     = MT_LABELS.get(mt, mt)

        if is_sparte005:
            hits = sample_sparte005_dctypes(all_records, mt, n=3)
        else:
            hits = sample_rule(all_records, sector, mt, ht, n=1)

        if not hits:
            missing.append(f"  {sector} {mt} {ht or '—'}")
            out_rows.append({
                "sparte":    f"{sector} {sparte_label}" if sector != "*" else "*",
                "mediatype": f"{mt} {mt_label}"         if mt    != "*" else "*",
                "htype":     ht or "—",
                "dc_type":   "—",
                "ddb_url":   "NO EXAMPLE FOUND",
                "w_class":   w_class or "—",
                "m_class":   m_class or "—",
            })
            continue

        for hit in hits:
            out_rows.append({
                "sparte":    f"{sector} {sparte_label}" if sector != "*" else "*",
                "mediatype": f"{mt} {mt_label}"         if mt    != "*" else "*",
                "htype":     ht or "—",
                "dc_type":   hit["dc_type"] if is_sparte005 else "—",
                "ddb_url":   DDB_ITEM_BASE + hit["item_id"],
                "w_class":   w_class or "—",
                "m_class":   m_class or "—",
            })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = ["sparte", "mediatype", "htype", "dc_type", "ddb_url", "w_class", "m_class"]
    with OUTPUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows → {OUTPUT}")
    if missing:
        print(f"\nNo examples found for {len(missing)} rule(s):")
        for m in missing:
            print(m)


if __name__ == "__main__":
    main()
