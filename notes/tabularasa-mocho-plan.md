# Plan: Fix §1.1 Domain-Class Assignments (transform-revised-plan.md)

## Context

The ProvidedCHO class assignment table (§1.1 of `transform-revised-plan.md`) was written against a planned version of mocho, not the actual ontology. Two categories of breakage:

1. **mocho: subclasses** (`mocho:ImageManifestation`, `mocho:ImageWork`, `mocho:ImmovableWork`) are planned but not yet in mocho-edit.owl — they must be added.
2. **DoCO classes** (`doco:Section`, `doco:Chapter`, `doco:Stanza`, etc.) are used for Library/Text htype rows but DoCO is not imported in mocho — DoCO must be imported.

Additionally, many *(pending)* and *(TBD)* rows need WEMI-level decisions.

Naming decision: **`mocho:ImageManifestation`** (not `mocho:ImageObject`) — consistent with WEMI theme (`aco:AudioManifestation`, `mo:MusicalManifestation`).

---

## Stream 1 — mocho ontology (`mocho-edit.owl`)

**File**: `mocho/mocho-odk/src/ontology/mocho-edit.owl`

### 1.1 Add three new mocho: classes

Per ADR note: mocho-native subclasses do NOT go into the WEMI union axioms (those list only external domain classes).

| Class | SubClassOf |
|---|---|
| `mocho:ImageManifestation` | `mocho:Manifestation`, `rdac:C10007`, `vra:Image` |
| `mocho:ImageWork` | `mocho:Work`, `rdac:C10001`, `vra:Work` |
| `mocho:ImmovableWork` | `mocho:Work`, `crm:E24_Physical_Man-Made_Thing` |

Each class needs: `owl:Class` declaration, `rdfs:label` (EN + DE), `skos:definition`, `rdfs:subClassOf` for each parent.

### 1.2 Import DoCO

Add to the imports block in mocho-edit.owl:
```xml
<owl:imports rdf:resource="http://purl.org/spar/doco/"/>
```

### 1.3 Rebuild mocho-full.owl

Run ODK pipeline from `mocho/mocho-odk/`:
```bash
sh run.sh make prepare_release
```
Verify: `mocho-full.owl` contains `mocho:ImageManifestation`, `mocho:ImageWork`, `mocho:ImmovableWork`, and DoCO class IRIs.

---

## Stream 2 — §1.1 table rewrite (`transform-revised-plan.md`)

**File**: `goethe-faust/notes/transform-revised-plan.md`

### 2.1 Fix mocho:Image* references

Replace `mocho:ImageObject` → `mocho:ImageManifestation` throughout §1.1.

### 2.2 DoCO-mapped Library/Text rows — add rdac:C10007

**Rule**: all Library/Text htype rows that map to a doco: class get a second type `rdac:C10007` (Manifestation). Apply to all existing and new doco: rows:

`doco:Section + rdac:C10007`, `doco:Appendix + rdac:C10007`, `doco:Part + rdac:C10007`, `doco:TextChunk + rdac:C10007`, `doco:Figure + rdac:C10007`, `doco:Index + rdac:C10007`, `doco:TableOfContents + rdac:C10007`, `doco:Chapter + rdac:C10007`, `doco:Stanza + rdac:C10007`, `doco:Preface + rdac:C10007`.

### 2.3 Fill *(pending)* Library/Text htype rows

**Work-level rule**: use `rdac:C10001`, not `mocho:Work`. Exceptions:
- ht022 Musik + mt001 Audio → `mo:MusicalWork`
- ht022 Musik + mt003 Text → `rdac:C10001` (musical score)
- ht015 Illustration + mt002 Photo → `mocho:ImageWork`
- ht019 Karte + mt002 Photo → `mocho:ImageWork`

| htype | German | Class(es) | WEMI |
|---|---|---|---|
| ht003 Beigefügtes Werk | Appended work | `rdac:C10001` | W |
| ht004 Annotation | Annotation | `doco:Annotation` + `rdac:C10007` | M |
| ht005 Anrede | Salutation | `mocho:Expression` | E |
| ht006 Aufsatz | Essay/Article | `rdac:C10001` | W |
| ht008 Beilage | Supplement/insert | `mocho:Manifestation` | M |
| ht010 Eintrag | Entry | `mocho:Expression` | E |
| ht014 Heft | Issue/booklet | `doco:Part` + `rdac:C10007` | M |
| ht015 Illustration | Illustration | `mocho:ImageWork` (mt002) / `rdac:C10001` (else) | W |
| ht019 Karte | Map | `mocho:ImageWork` (mt002) / `rdac:C10001` (else) | W |
| ht020 Mehrbändiges Werk | Multi-volume work | `rdac:C10001` | W |
| ht021 Monografie | Monograph | `rdac:C10001` | W |
| ht022 Musik | Music | `mo:MusicalWork` (mt001) / `rdac:C10001` (mt003) | W |
| ht023 Fortlaufendes Sammelwerk | Serial | `rdac:C10001` | W |
| ht024 Privilegie | Privilege letter | `rdac:C10001` | W |
| ht025 Rezension | Review | `rdac:C10001` | W |
| ht029 Widmung | Dedication | `mocho:Expression` | E |
| ht044 Zeitung | Newspaper | `rdac:C10001` | W |

*DoCO class availability to be confirmed at import time — fallback to `rdac:C10007` alone if a specific doco: term doesn't exist.*

### 2.4 Fill *(TBD)* Archive non-photo rows

| sparte | mediatype | Class | Rationale |
|---|---|---|---|
| sparte001 Archive | mt001 Audio | `aco:AudioManifestation` | Consistent with sparte005 Audio |
| sparte001 Archive | mt003 Text | `rico:Record` | Archive text = archival record |
| sparte001 Archive | mt005 Video | `ebucoreplus:MediaResource` | Consistent with sparte005 Video |
| sparte001 Archive | mt007 Not Digitized | `rico:Record` | Undigitized archival record |

### 2.5 Update prose below table

Note that `mocho:ImageManifestation` replaces `mocho:ImageObject`, and DoCO is now imported.

---

## Stream 3 — Transform script (`transform_edm_to_mocho.py`)

**File**: `goethe-faust/scripts/transform_edm_to_mocho.py`

Rename constant (line 62):
```python
# Before
_MOCHO_IMAGE_OBJECT = MOCHO_NS + "ImageObject"

# After
_MOCHO_IMAGE_MANIFESTATION = MOCHO_NS + "ImageManifestation"
```

Update all references in `retype_entities()` (lines 419–421).

---

## Verification

1. `grep "ImageManifestation" mocho/mocho-odk/mocho/mocho-full.owl` — class present
2. `grep "doco" mocho/mocho-odk/mocho/mocho-full.owl | head` — DoCO imported and classes resolved
3. `grep "ImageObject" goethe-faust/scripts/transform_edm_to_mocho.py` — zero results
4. `grep -E "pending|TBD" goethe-faust/notes/transform-revised-plan.md` — zero results in §1.1
5. Run transform sample: `python transform_edm_to_mocho.py --limit 100`; check `webresources_typed > 0`

---

## Files modified

| File | Change |
|---|---|
| `mocho/mocho-odk/src/ontology/mocho-edit.owl` | Add 3 classes + DoCO import |
| `mocho/mocho-odk/mocho/mocho-full.owl` | Rebuilt by ODK (not hand-edited) |
| `goethe-faust/notes/transform-revised-plan.md` | §1.1 table rewrite |
| `goethe-faust/scripts/transform_edm_to_mocho.py` | Rename `_MOCHO_IMAGE_OBJECT` constant |
