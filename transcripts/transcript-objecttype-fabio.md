# Transcript: DDB objecttype → FaBiO/DoCO matching

**Date:** 2026-02-21
**Working directory:** `/Users/mta/Documents/claude/`
**Script:** `/tmp/claude/match_types_v3.py`
**Output:** `ddb-type2fabio.json`

---

## Session summary

Built and iteratively refined a 4-tier pipeline to match DDB Solr `objecttype` field values to classes from the FaBiO and DoCO ontologies. The DDB data is in German; the ontology classes are in English. The pipeline bridges this gap through translation followed by progressively softer matching.

---

## Conversation

### Turn 1 — Initial task

**User:**
1. read ddb-search-goethe-all.json
2. take all the values of response → docs → objecttype into a list of dict, where key is the doc id, and the list consists of all the objecttype values per doc
3. take all the subclasses of fabio:Work, fabio:Expression, fabio:Manifestation, fabio:Item from fabio.owl
4. try to match the objecttype with the subclass names
5. Save result in ddb-type2fabio.json

**Assistant:** Parsed `ddb-search-goethe-all.json` (97,172 docs) and `fabio.owl` using Python's `xml.etree.ElementTree`. Found 94 fabio subclasses (30 Work, 57 Expression, 4 Manifestation, 3 Item). Applied case-insensitive exact matching on normalized class names and labels. Result: **7 matches** out of 952 unique objecttype values — most types are in German, fabio classes are in English.

---

### Turn 2 — Add translation + approximate matching

**User:** Revise the matching script:
1. translate German terms to English
2. match translated terms to fabio subclasses
3. for unmatched terms: use approximate matching
   3.1 levenshtein distance of 2
   3.2 word embeddings
4. for approximate matching, indicate confidence score
5. save matching criteria: strict, levenshtein, embeddings

**Assistant:** Created a Python venv at `/Users/mta/Documents/claude/.venv` and installed `deep-translator`, `rapidfuzz`, `sentence-transformers`.

Implemented 4-tier pipeline in `match_types_v3.py`:

| Tier | Method | Description |
|------|--------|-------------|
| 1 | `strict` | Case-insensitive exact match on class name, CamelCase-split words, and rdfs:labels |
| 2 | `strict_translated` | Translate via Google Translate (DE→EN), then exact match |
| 3 | `levenshtein` | `rapidfuzz` Levenshtein distance ≤ 2; confidence = `1 - dist/max_len` |
| 4 | `embeddings` | `sentence-transformers` `all-MiniLM-L6-v2`; cosine similarity ≥ 0.55 |

Each match record includes: `ontology_class`, `ontology_parent`, `ontology_uri`, `original_term`, `translated_term`, `match_method`, `confidence`.

**Result (all sectors):** 249 matched / 703 unmatched out of 952 unique types.

| Method | Count |
|--------|-------|
| strict | 7 |
| strict_translated | 20 |
| levenshtein | 21 |
| embeddings | 201 |
| unmatched | 703 |

---

### Turn 3 — Filter to sector_fct == "sec_02"

**User:** Revise the script to only match objecttype when doc → sector_fct is "sec_02".

**Assistant:** Added filter in `load_objecttypes()`:

```python
if doc.get("sector_fct") == "sec_02" and "objecttype" in doc:
```

**Result (sec_02 only):** 27,768 docs, 303 unique objecttype values, **99 matched / 204 unmatched**.

| Method | Count |
|--------|-------|
| strict | 7 |
| strict_translated | 13 |
| levenshtein | 4 |
| embeddings | 75 |
| unmatched | 204 |

---

### Turn 4 — Add doc ID lists per objecttype

**User:** Revise the script to also save a list of id for each objecttype term, use "object_id" as the key term.

**Assistant:** Built an `objecttype → [doc_id, ...]` mapping with `collections.defaultdict` and added `"object_id"` to each entry in `type_to_fabio`. Example: `"Abschnitt"` has 1,452 doc IDs; `"Abschlussarbeit (Bachelor)"` has 1.

---

### Turn 5 — Add DoCO classes

**User:** Revise the script to also extract doco classes. and try to match objecttype to fabio subclasses AND doco classes.

**Assistant:** Added `parse_doco_classes()` to parse `doco.owl` (53 classes, e.g. Section, Chapter, Bibliography, TableOfContents, Stanza, Preface, Title). Merged fabio and doco into a unified lookup; fabio takes priority on name collisions. Internal dedup keys (`doco_Chapter` etc.) stripped in `build_lookup()` so output shows clean class names.

Each match record now includes `"ontology": "fabio"` or `"ontology": "doco"`. All fields renamed to `ontology_class`, `ontology_parent`, `ontology_uri`.

**Result (sec_02, fabio + doco):** **107 matched / 196 unmatched** out of 303 types.

| Method | Count |
|--------|-------|
| strict | 7 |
| strict_translated | 18 |
| levenshtein | 5 |
| embeddings | 77 |
| unmatched | 196 |

New doco matches: `Abschnitt`→Section, `Bibliografie`→Bibliography, `Inhaltsverzeichnis`→TableOfContents, `Vorwort`→Preface, `Titelblatt`→Title, `Vers`→Stanza, `Lyrik`→Stanza, `Einführung`→Preface.

---

### Turn 6 — Restructure output: separate "details" section

**User:** Revise output file to save the list of dicts (objecttype: [list of object_id]) into "details" section of the main dictionary, outside of "summary".

**Assistant:** Moved `object_id` lists out of `type_to_fabio` entries into a new top-level `"details"` key. Removed the `docs` per-document section. Final output structure:

```json
{
  "summary": {
    "total_docs": 97172,
    "docs_with_objecttype": 27768,
    "unique_objecttypes": 303,
    "total_matched": 107,
    "total_unmatched": 196,
    "by_method": { "strict": 7, "strict_translated": 18, "levenshtein": 5, "embeddings": 77, "unmatched": 196 },
    "unmatched_types": [...]
  },
  "type_to_fabio": {
    "Buch": {
      "ontology": "fabio",
      "ontology_class": "Book",
      "ontology_parent": "Expression",
      "ontology_uri": "http://purl.org/spar/fabio/Book",
      "original_term": "Buch",
      "translated_term": "Book",
      "match_method": "strict_translated",
      "confidence": 1.0
    }
  },
  "details": {
    "Buch": ["doc_id_1", "doc_id_2", ...]
  }
}
```

---

### Turn 7 — Generate requirements.txt

**User:** Generate requirements.txt based on the venv settings.

**Assistant:** Ran `pip freeze` in the venv and wrote `requirements.txt` with 34 pinned packages including `deep-translator==1.11.4`, `RapidFuzz==3.13.0`, `sentence-transformers==5.1.2`, `torch==2.8.0`, `transformers==4.57.6`.

---

## Key files

| File | Description |
|------|-------------|
| `ddb-search-goethe-all.json` | Source: 97,172 DDB Solr docs for query "goethe" |
| `/tmp/claude/match_types_v3.py` | Matching pipeline script |
| `ddb-type2fabio.json` | Output: type mappings + doc ID lists |
| `requirements.txt` | Pinned venv dependencies |
| `/Users/mta/Documents/FIZ/workspace/fiz-ddb/schema/fabio.owl` | FaBiO ontology (98 classes) |
| `/Users/mta/Documents/FIZ/workspace/fiz-ddb/schema/doco.owl` | DoCO ontology (53 classes) |
| `/Users/mta/Documents/claude/.venv/` | Python virtual environment |

## Pipeline config

```python
SECTOR_FILTER     = "sec_02"
EMBEDDING_MODEL   = "all-MiniLM-L6-v2"
EMBEDDING_THRESHOLD = 0.55
LEVENSHTEIN_MAX_DIST = 2
TRANSLATE_SRC     = "de"
TRANSLATE_DEST    = "en"
```
