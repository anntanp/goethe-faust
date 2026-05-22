# Bug inventory: transform_edm_to_mocho.py

Bugs fixed after initial implementation. Numbered sequentially (B1, B2, …).
Each entry records: symptom, root cause, fix, and code changes.

**Related**: `transform-script-adr.md` (implementation decisions), `transform-adr.md` (dispatch design)

---

## B1: `load_audio_type2class` returns empty dict — audio group dispatch never fires

**Date found**: 2026-05-21  
**Status**: Fixed 2026-05-21  
**Affects**: all mt001 (Audio) records across all sectors  
**Related**: `transform-script-adr.md` D16; `output/config/audio_type2class.json`

### Symptom

All mt001 ProvidedCHOs receive `aco:AudioManifestation` regardless of dc:type.
Group A dc:types (e.g. `Schallplatte`, `CD`, `Langspielplatte`) are not upgraded
to `mo:MusicalManifestation` as specified in D16.

### Root cause

Two mismatches between `load_audio_type2class` (loaders.py:108) and the actual
structure of `audio_type2class.json`:

**Mismatch 1 — top-level structure**: The loader expects either a JSON list or a
dict with an `"entries"` key:
```python
for entry in raw if isinstance(raw, list) else raw.get("entries", []):
```
The file is a plain dict keyed by dc:type string (e.g. `"Schallplatte"`, `"CD"`).
`raw.get("entries", [])` returns `[]`; the loop body never executes.

**Mismatch 2 — dc:type field name**: Even if the loop ran, the loader reads
`entry.get("dc_type_de", "")` to extract the dc:type string. The JSON has no
such field — the dc:type string is the dict key itself, not a value inside the
entry. The guard `if sector and dc_type and group` would drop every row.

Consequence: `audio_type2class` is always `{}`. The lookup in emitters.py:
```python
if audio_type2class.get((sector, dc_text)) == "A":
```
always returns `None`; the `mo:MusicalManifestation` branch is never reached.

**Secondary issue — sector key form**: The JSON stores sector as a short code
(`"sparte004"`), but `sector` in `retype_entities()` is a full IRI
(`http://ddb.vocnet.org/sparte/sparte004`). The current lookup does not account
for this mismatch. Additionally, most entries are sector-agnostic (no `sector`
field), but the lookup only tries `(sector, dc_text)` — it has no fallback for
sector-agnostic entries keyed as `("", dc_text)`.

### Fix

**1. Rewrite `load_audio_type2class` (loaders.py:108–122)**

Iterate `raw.items()` instead of `raw.get("entries", [])`. Skip `_doc` and
`Muster` keys. For each real entry: dc_type = key; group = `entry["group"]`;
sector code = `entry.get("sector") or ""`. Expand non-empty sector codes to
full IRIs using `_SECTOR_PREFIX` (`http://ddb.vocnet.org/sparte/`). Store as
`(sector_iri_or_empty, dc_type)` → group char.

**2. Fix lookup in emitters.py:289**

Add sector-agnostic fallback:
```python
group = audio_type2class.get((sector, dc_text)) or audio_type2class.get(("", dc_text))
if group == "A":
```

**3. Add tests (tests/test_transform.py)**

- Loader test: load real `audio_type2class.json`; assert non-empty result;
  spot-check `("", "Schallplatte") == "A"` and
  `("http://ddb.vocnet.org/sparte/sparte004", "Magnettonband") == "B"`.
- Dispatch test: mt001 record with `dc:type = "Schallplatte"` and `use_htype=False`
  → ProvidedCHO typed as `mo:MusicalManifestation`, not `aco:AudioManifestation`.

### Code changes

| File | Location | Change |
|---|---|---|
| `scripts/transform/loaders.py` | `load_audio_type2class` (line 108) | Rewrite loop to iterate `raw.items()`; extract dc_type from key, not `dc_type_de` field; expand sector code to full IRI |
| `scripts/transform/emitters.py` | audio group dispatch (line 289) | Two-step lookup: sector-specific first, sector-agnostic fallback |
| `scripts/transform/tests/test_transform.py` | new tests | Loader correctness + group A dispatch round-trip |
