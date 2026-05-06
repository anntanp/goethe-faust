"""
Purpose:   Export N records from s2.sqlite to JSONL for transform dry-run.
Usage:     python scripts/extract_sqlite_sample.py [--db PATH] [--ids FILE] [--limit N] [--out FILE]
Inputs:    gemea/data/sqlite/s2.sqlite  (objs table: uid PK, bufgz BLOB)
           gemea/data/sqlite/ids_sec_02_digitalisat.txt  (one UID per line)
Outputs:   /tmp/s2-sample.jsonl  (or --out path), one JSON object per line
Deps:      stdlib only (gzip, json, sqlite3)
Assumes:   Run from Documents/claude/ so relative paths to gemea/ resolve.
           bufgz blobs decompress to DDB-EDM JSON matching goethe-faust record structure.
"""

import argparse
import gzip
import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).parent.parent.parent  # Documents/claude/

parser = argparse.ArgumentParser(description="Export records from s2.sqlite to JSONL")
parser.add_argument("--db",    type=Path, default=BASE / "gemea/data/sqlite/s2.sqlite")
parser.add_argument("--ids",   type=Path, default=BASE / "gemea/data/sqlite/ids_sec_02_digitalisat.txt")
parser.add_argument("--limit", type=int,  default=500)
parser.add_argument("--out",   type=Path, default=Path("/tmp/s2-sample.jsonl"))
args = parser.parse_args()

conn = sqlite3.connect(str(args.db))
written = 0
missing = 0

with open(args.ids) as id_file, open(args.out, "w", encoding="utf-8") as out:
    for line in id_file:
        uid = line.strip()
        if not uid:
            continue
        row = conn.execute("SELECT bufgz FROM objs WHERE uid = ?", (uid,)).fetchone()
        if row:
            print(json.dumps(json.loads(gzip.decompress(row[0])), ensure_ascii=False), file=out)
            written += 1
        else:
            missing += 1
        if written >= args.limit:
            break

conn.close()
print(f"Wrote {written} records to {args.out}" + (f" ({missing} UIDs not found)" if missing else ""))
