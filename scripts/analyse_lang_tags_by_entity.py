"""
Purpose:  Find every (entity_type, field_key, lang_code) combination that carries
          a lang-tagged literal in the DDB EDM JSONL. Flags collective/invalid
          BCP 47 codes to determine whether scope of normalization extends beyond
          ProvidedCHO (e.g. to Agent, Place, WebResource labels).
Usage:    python scripts/analyse_lang_tags_by_entity.py
Inputs:   data/items-all-goethe-faust.json  (JSONL)
Outputs:  data/processed/lang_tag_by_entity.csv
          Columns: entity_type, field_key, lang_code, count, is_collective, example
Dependencies: stdlib only
Assumptions: Each line is a JSON record with structure record["edm"]["RDF"].
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

COLLECTIVE_CODES = {
    "wen", "alg", "bat", "bnt", "btk", "cau", "crp", "dra",
    "gem", "inc", "ira", "map", "mkh", "myn", "nic", "nub",
    "oto", "pra", "roa", "sai", "sal", "sem", "sit", "sla",
    "smi", "tai", "tup", "tut",
}

ROOT = Path(__file__).resolve().parent.parent
DATA_IN  = ROOT / "data" / "items-all-goethe-faust.json"
DATA_OUT = ROOT / "data" / "processed" / "lang_tag_by_entity.csv"


def _walk(val: object, entity_type: str, field_key: str,
          acc: dict) -> None:
    """Recursively find {"$": text, "lang": code} dicts and record them."""
    if isinstance(val, dict):
        lang = val.get("lang")
        text = val.get("$", "")
        if lang and text:
            key = (entity_type, field_key, str(lang))
            if key not in acc:
                acc[key] = {"count": 0, "example": str(text)[:100]}
            acc[key]["count"] += 1
        for k, v in val.items():
            if k not in ("$", "lang", "resource", "about"):
                _walk(v, entity_type, field_key, acc)
    elif isinstance(val, list):
        for item in val:
            _walk(item, entity_type, field_key, acc)


def main() -> None:
    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    acc: dict = {}
    n = 0

    with DATA_IN.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            n += 1
            rdf = (record.get("edm") or {}).get("RDF") or {}
            for entity_type, entities in rdf.items():
                for entity in (entities if isinstance(entities, list) else [entities]):
                    if not isinstance(entity, dict):
                        continue
                    for field_key, val in entity.items():
                        if field_key == "about":
                            continue
                        _walk(val, entity_type, field_key, acc)

    print(f"Processed {n:,} records", file=sys.stderr)

    rows = [
        {
            "entity_type":  et,
            "field_key":    fk,
            "lang_code":    lc,
            "count":        v["count"],
            "is_collective": lc in COLLECTIVE_CODES,
            "example":      v["example"],
        }
        for (et, fk, lc), v in acc.items()
    ]
    rows.sort(key=lambda r: (-int(r["is_collective"]), -r["count"]))

    with DATA_OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"Saved → {DATA_OUT}  ({len(rows)} combinations)", file=sys.stderr)

    # Print collective rows to stdout
    collective = [r for r in rows if r["is_collective"]]
    if collective:
        print(f"\nCollective lang codes ({len(collective)} combinations):")
        print(f"{'entity_type':<20} {'field_key':<25} {'lang':<8} {'count':>7}")
        print("-" * 65)
        for r in collective:
            print(f"{r['entity_type']:<20} {r['field_key']:<25} {r['lang_code']:<8} {r['count']:>7,}")
    else:
        print("\nNo collective lang codes found.")


if __name__ == "__main__":
    main()
