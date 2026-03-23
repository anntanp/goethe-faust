#!/usr/bin/env python3
"""
fetch-search-all.py
===================
Fetch all DDB search results for the query "goethe" via the DDB Solr API
and merge them into a single JSON file.

Uses cursor-based pagination (cursorMark + sort=id asc) to bypass Solr's
maxResultWindow limit, which blocks offset-based pagination beyond ~10,000.
Saves progress to a .cursor state file so the run can be resumed if interrupted.

Input
-----
  DDB Solr API (live, requires network access):
    https://api.deutsche-digitale-bibliothek.de/2/search/index/search/select

Output
------
  data/ddb-search-goethe-all.json       — merged Solr response with all docs
  data/ddb-search-goethe-all.cursor     — resume state (deleted on completion)

Usage
-----
    python scripts/fetch-search-all.py

Notes
-----
  The commented-out TOTAL is the Faust-specific count; kept for reference.
  Total is now discovered dynamically from the first response.
"""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.deutsche-digitale-bibliothek.de/2/search/index/search/select"
QUERY = "goethe"
ROWS = 1000
PROJECT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT / "data" / "ddb-search-goethe-all.json"
STATE = PROJECT / "data" / "ddb-search-goethe-all.cursor"


def build_url(cursor: str) -> str:
    parts = [
        ("q", QUERY),
        ("rows", ROWS),
        ("sort", "id asc"),
        ("cursorMark", cursor),
        ("wt", "json"),
    ]
    return f"{API}?{urllib.parse.urlencode(parts)}"


# Resume: load existing docs and saved cursor
all_docs = []
base = None
cursor = "*"

if STATE.exists() and OUTPUT.exists():
    print("Resuming from saved state...")
    with open(OUTPUT, encoding="utf-8") as f:
        base = json.load(f)
    all_docs = base["response"]["docs"]
    cursor = STATE.read_text().strip()
    print(f"  Loaded {len(all_docs)} docs, cursor: {cursor[:40]}...")

while True:
    url = build_url(cursor)
    print(f"Fetching (cursor={'*' if cursor == '*' else cursor[:30] + '...'}, docs so far: {len(all_docs)})...")
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())

    if base is None:
        base = data
        total = data["response"]["numFound"]
        print(f"Total matching: {total}")

    docs = data["response"]["docs"]
    next_cursor = data.get("nextCursorMark", cursor)

    if not docs or next_cursor == cursor:
        break

    all_docs.extend(docs)
    print(f"  Got {len(docs)} docs (total so far: {len(all_docs)})")

    # Save progress
    base["response"]["docs"] = all_docs
    base["response"]["numFound"] = len(all_docs)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=2, ensure_ascii=False)
    STATE.write_text(next_cursor)

    cursor = next_cursor
    time.sleep(0.3)

# Finalize
base["response"]["docs"] = all_docs
base["response"]["start"] = 0
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(base, f, indent=2, ensure_ascii=False)
STATE.unlink(missing_ok=True)

print(f"Done. Saved {len(all_docs)} docs to {OUTPUT}")
