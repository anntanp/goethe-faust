# ISBD Punctuation Analysis — Goethe-Faust Titles

**Dataset:** `data/items-all-goethe-faust.json` (115,432 items, one title each)
**Script:** `scripts/check_isbd_titles.py`
**Date:** 2026-03-13

## Summary

| Metric | Count | % |
|---|---|---|
| Items total | 115,432 | — |
| Items without title | 0 | 0% |
| Titles with ≥1 ISBD pattern | 33,561 | **29.1%** |

## Pattern Breakdown

| Pattern | Signal | Count | % of titles |
|---|---|---|---|
| ` :` | Other title information | 20,767 | 18.0% |
| trailing `.` | Area-end period | 8,257 | 7.2% |
| `[ ]` | Supplied/inferred data | 5,653 | 4.9% |
| ` ;` | Subsequent SoR / series | 2,910 | 2.5% |
| ` /` | Statement of responsibility | 2,478 | 2.1% |
| `...` / `…` | Ellipsis / truncation | 1,873 | 1.6% |
| ` =` | Parallel title | 464 | 0.4% |

## Notes

- ` :` is the dominant signal — nearly 1 in 5 titles carries other-title-information punctuation.
- Trailing period is tricky: it can be ISBD area-end or just an abbreviation (e.g., `Bd. 2.`). The pattern `[^.]\.$` excludes `..` but can still catch abbreviations.
- `[ ]` brackets in DDB titles typically mark cataloger-supplied information (medium, series, subunit identifiers).
- Patterns are not mutually exclusive; some titles match multiple.
