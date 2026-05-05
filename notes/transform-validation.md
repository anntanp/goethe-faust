# Transform validation findings

Output checks and spec discrepancy findings for `scripts/transform/transform_edm_to_mocho.py`.
Reference run: `output/transform/20260505_092658/`.

---

## 1. werk_staging coverage

### 1.1 Current state

Run `20260505_092658`: **15 rows**, all `rdac:C10001`. Zero `mo:MusicalWork` rows (no ht022 Musik records in the Goethe-Faust corpus).

`WERK_STAGING_CLASSES` in the script (§10, `_W_SLOT_CLASSES`) matches §1.2 of `transform-revised-plan.md`: triggers on `rdac:C10001` and `mo:MusicalWork` only.

### 1.2 Spec discrepancy — `mocho:ImageWork` missing

§1.1 marks `mocho:ImageWork` as "GND Werk" in the entity linking column (ht015 Illustration, ht019 Karte, sparte005 mt002). §1.2 text does not mention it. `WERK_STAGING_CLASSES` does not include it.

**Status:** open — no `mocho:ImageWork` records in the Goethe-Faust corpus, so no impact on current run. Fix before running on a broader corpus.

### 1.3 `ec:EditorialWork` — scope question

Adding `ec:EditorialWork` to `WERK_STAGING_CLASSES` would generate **88 new rows** from mt005 (Video) records:

| sector | count |
|---|---|
| sparte005 Media | 63 |
| sparte006 Museum | 18 |
| sparte002 Library (no htype) | 7 |
| sparte001 Archive | 0 (htype always fires; EditorialWork never becomes `target_class`) |

The remaining 8 mt005 records already land in werk_staging via `rdac:C10001` (sparte002 Library video where an htype such as ht021 fired first).

**Decision needed:** §1.1 has no "GND Werk" in the entity linking column for any mt005/ec:EditorialWork row. Adding it would be an intentional scope extension — video productions do not have GND Werk authority records. Left out for now; revisit when GND linking scope is finalised.
