# Plan: Map DDB IMAGE Objects to mocho — VRA Core + mocho:ImageWork / mocho:ImageObject

## 0. Context

DDB records with `edm:type = "IMAGE"` and `mediatype = mt002` span ontologically
distinct categories. The existing approach (D9: every ProvidedCHO = `mocho:Manifestation`)
is incorrect for museum visual objects.

Revised model — two new native mocho classes:

| Entity | Class | WEMI level |
|---|---|---|
| Artwork ProvidedCHO (Zeichnung, Gemälde) | `vra:Work` | Work |
| Photo ProvidedCHO (Fotografie, Standfoto) | `mocho:ImageWork` | Work |
| WebResource (digital scan / image file) | `mocho:ImageObject` | Manifestation |

`vra:Image` is aligned to Manifestation in the babel-ddb paper ("visual surrogate or
digital reproduction"); `vra:Image rdfs:subClassOf schema:CreativeWork` in the OWL
(WEMI-neutral), but the semantic intent is documentation image, not photo-as-Work.
Therefore `vra:Image` is NOT used for ProvidedCHOs. `mocho:ImageObject` subsumes its
Manifestation role at the WebResource level.

---

## 1. Conceptual framework

### 1.1 VRA Core 4.0 classes (from `mocho/ontology/vra-core-v4.0.owl`)

IRI base: `http://purl.org/vra/`

- **`vra:Work`** — `rdfs:subClassOf schema:CreativeWork`. The artwork as a creative/physical entity.
  2D artworks (Zeichnung, Gemälde), 3D sculptures, architecture.
- **`vra:Image`** — `rdfs:subClassOf schema:CreativeWork`. A visual image artifact (photograph,
  slide, documentation image). **Work level** — see §1.1.1 for the full discussion.
- **`vra:imageOf`** — ObjectProperty, `owl:inverseOf vra:hasImage`. Links a `vra:Image` to
  the `vra:Work` it documents.

#### 1.1.1 Discussion: WEMI level of `vra:Image`

**The babel-ddb alignment (now revised)**

The babel-ddb paper placed `vra:Image` at **Manifestation** level using a structural argument:
VRA Core's tripartite schema (Work → Image, no intermediate Expression) collapses the FRBR
W→E→M hierarchy, so Image occupies the slot where Manifestation would be. Under this reading,
`vra:Image` is a visual surrogate or digital reproduction of a `vra:Work` — a carrier, not
a creative entity.

**The problem: `schema:CreativeWork` is not WEMI-aligned**

`vra:Image rdfs:subClassOf schema:CreativeWork`. Schema.org has no WEMI hierarchy: its
`schema:CreativeWork` covers books, paintings, photographs, recordings, and software — entities
that span all FRBR levels. Schema.org classes are **WEMI-neutral by design**, but they carry
**WEMI implications through naming and semantic intent**: "CreativeWork" reads as a creative
or intellectual entity, which is Work-level intuition. A reasoner that maps
`schema:CreativeWork → mocho:Work` would infer `vra:Image ⊑ mocho:Work`, directly
contradicting the babel-ddb Manifestation placement.

**Hayes & Warren** compound the ambiguity: *"In many cases the subject image itself will be
the work."* A photograph is a creative act; the photographer made deliberate choices. From
this angle, a `vra:Image` (a photograph) is unambiguously a Work.

**VRA Core's own design intent** supports the Work reading too: VRA describes visual arts
collections from the perspective of image creators. `vra:Work` is the collected artifact;
`vra:Image` is the visual record of it — but the photograph of an artwork is itself an
artifact created by someone, not merely a carrier. VRA does not call `vra:Image` a
Manifestation anywhere in its specification.

**Conclusion and revised alignment**

`vra:Image` is treated as **Work level** in this plan, consistent with:
- Its OWL superclass `schema:CreativeWork`
- VRA Core's creator-centric framing
- Hayes & Warren's observation that images are often Works in their own right

The babel-ddb structural argument (Manifestation slot in a collapsed hierarchy) is noted
but not adopted here. mocho follows the model, not the babel-ddb paper. The key implication:
`vra:Image` belongs in the `mocho:Work` union (not Manifestation); WebResources are typed
with `mocho:ImageObject` (`rdfs:subClassOf mocho:Manifestation`) to make the carrier level
explicit without relying on `vra:Image`.

### 1.2 LIO (from `mocho/odk-ontology/lio_import.owl`)

IRI base: `https://w3id.org/lio/v1#`

- **`lio:depicts`**, **`lio:shows`** — kept for property-level alignment; not used for rdf:type dispatch.
- **`lio:Image`** — NOT used for rdf:type dispatch (see §1.2.1).
- **`mw:facsimile`** — Hayes & Warren 2010 (`http://purl.org/net/mw/`).
  `facsimileOf (Image, Image)`: the subject is a reproduction of the object.
  `lio:fascimile` appeared in rm024-lio.pdf slides but was never implemented in the LIO OWL.
  **Resolution**: define `mocho:facsimile` natively (see §1.3.3). Follow-up ADR.

#### 1.2.1 Decision: `lio:Image` vs `mocho:ImageWork` for photo ProvidedCHOs

**Pros of `lio:Image`**
- Already imported in mocho (`lio_import.owl`) — no new class definition required
- Designed specifically for image description; semantically appropriate for photographs
- WEMI-neutral in the LIO OWL — does not over-commit to Work or Manifestation
- Already in the mocho:Work union (prior state of mocho-edit.owl)
- Broad definition: "any PictorialElement considered to be a complete image" — covers photos, drawings, paintings

**Cons of `lio:Image`**
- Research ontology; not widely adopted in production CH linked data pipelines
- WEMI-neutrality is also a weakness: the class gives no signal about level; dispatch logic must always pair it with `mocho:Work` or `mocho:Manifestation` at instance level
- Semantically overlaps with `vra:Image` and `foaf:Image`; unclear precedence
- `lio:fascimile` was planned in LIO but never implemented — the OWL is incomplete, raising confidence concerns about the namespace long-term
- Mixes an image-description ontology (LIO) with CH-domain ontologies (VRA, RDA, RiC-O) in the same dispatch layer

**Note on `vra:Image` as Manifestation**

The babel-ddb paper aligns `vra:Image` to Manifestation level (structural argument: VRA collapses
W→E→M to W→Image, so Image occupies the Manifestation slot). However, `vra:Image rdfs:subClassOf
schema:CreativeWork` in the OWL — and `schema:CreativeWork` reads as a Work-level entity by name
and Schema.org intent (though Schema.org has no WEMI at all). A reasoner that maps
`schema:CreativeWork → mocho:Work` would infer `vra:Image ⊑ mocho:Work`, directly contradicting
the babel-ddb Manifestation placement. `vra:Image` is therefore ontologically unreliable for
explicit WEMI dispatch in mocho: its OWL superclass pulls toward Work; its VRA design intent
and babel-ddb alignment pull toward Manifestation.

**Final decision: `mocho:ImageWork`**

Reasons:
- `rdfs:subClassOf mocho:Work` gives explicit, unambiguous WEMI commitment — no contradiction from inherited superclasses
- Pairs symmetrically with `mocho:ImageObject` (`rdfs:subClassOf mocho:Manifestation`) for WebResources — both have mocho-native, clean WEMI chains
- Avoids the `vra:Image` / `schema:CreativeWork` WEMI ambiguity entirely
- Native mocho class — no external LIO dependency required for dispatch; LIO import retained only for property use (`lio:depicts`, `lio:shows`)
- Name is self-documenting in the mocho namespace; aligns with mocho's role as a hub ontology

### 1.3 New mocho classes

#### 1.3.1 `mocho:ImageWork` — photographic Work

Photo ProvidedCHOs: the photograph is the creative artifact collected and described in DDB.

```turtle
mocho:ImageWork rdf:type owl:Class ;
    rdfs:subClassOf mocho:Work ;
    rdfs:label "Image Work"@en ;
    rdfs:comment """A photographic or visual image artifact treated as a Work-level entity:
        the photograph, slide, negative, or postcard is itself the creative artifact
        collected and described. Distinct from vra:Image (documentation image of an
        artwork, Manifestation level)."""@en .
```

#### 1.3.2 `mocho:ImageObject` — digital image carrier (Manifestation)

WebResources: the digital file that carries a Work (artwork or photo).

```turtle
mocho:ImageObject rdf:type owl:Class ;
    rdfs:subClassOf mocho:Manifestation ;
    rdfs:label "Image Object"@en ;
    rdfs:comment """A digital image carrier at Manifestation level: a scan, online image
        file, or digital reproduction. Used exclusively for WebResources (edm:isShownBy /
        edm:hasView targets). Subsumes the vra:Image role (visual surrogate /
        documentation image)."""@en .
```

#### 1.3.3 `mocho:facsimile` — reproduction link (follow-up ADR)

Source definition — Hayes & Warren 2010, p. 74, Properties (Domain, Range):

> ***facsimileOf*** (Image, Image) — "The subject is a more or less precise re-rendering,
> reproduction or visual representation of the object. A photograph of a drawing taken for
> exhibition in a catalog would be the typical example. It does not imply exactness of
> reproduction: a lower-resolution thumbnail can be a facsimile, for example."

```turtle
mocho:facsimile rdf:type owl:ObjectProperty ;
    rdfs:label "facsimile of"@en ;
    rdfs:comment """The subject is a more or less precise re-rendering, reproduction or
        visual representation of the object. A photograph of a drawing taken for exhibition
        in a catalog would be the typical example. It does not imply exactness of
        reproduction: a lower-resolution thumbnail can be a facsimile, for example.
        (After Hayes & Warren 2010 mw:facsimileOf, p. 74.)"""@en ;
    rdfs:domain mocho:ImageObject ;
    rdfs:range  owl:Thing .   # mocho:ImageWork or vra:Work
```

### 1.4 mocho-edit.owl changes required

**Summary of changes**

| Change | Detail |
|---|---|
| Define `mocho:ImmovableWork` | New OWL class, `rdfs:subClassOf mocho:Work` |
| Define `mocho:ImageWork` | New OWL class, `rdfs:subClassOf mocho:Work` |
| Define `mocho:ImageObject` | New OWL class, `rdfs:subClassOf mocho:Manifestation` |
| `mocho:Work` union | Add `mocho:ImageWork`; add `vra:Image` (Work level, revised); remove `lio:Image` |
| `mocho:Manifestation` union | Add `mocho:ImageObject`; remove `vra:Image` (no longer Manifestation) |
| Define `mocho:facsimile` | **Out of scope** — not used in goethe-faust corpus; follow-up ADR only |

**OWL definitions to add to `mocho-edit.owl`**

```turtle
@prefix mocho: <https://ise-fizkarlsruhe.github.io/ddbkg/mocho#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

###  mocho:ImmovableWork
mocho:ImmovableWork rdf:type owl:Class ;
    rdfs:subClassOf mocho:Work ;
    rdfs:label "Immovable Work"@en ;
    rdfs:comment """Permanent, fixed, non-transportable tangible assets of significant
        historical, architectural, or archaeological value, including buildings, sites,
        monuments, and urban or rural ensembles. Distinct from moveable built objects
        (furniture, stage sets) which remain vra:Work. Analogous to CIDOC-CRM
        crm:E25 Human-Made Feature."""@en .

###  mocho:ImageWork
mocho:ImageWork rdf:type owl:Class ;
    rdfs:subClassOf mocho:Work ;
    rdfs:label "Image Work"@en ;
    rdfs:comment """A photographic or visual image artifact treated as a Work-level entity:
        the photograph, slide, negative, or postcard is itself the creative artifact
        collected and described. Distinct from vra:Image (used for documentation images
        of artworks; also Work level per §1.1.1) in that mocho:ImageWork makes the
        Work-level WEMI commitment explicit via its subClassOf chain."""@en .

###  mocho:ImageObject
mocho:ImageObject rdf:type owl:Class ;
    rdfs:subClassOf mocho:Manifestation ;
    rdfs:label "Image Object"@en ;
    rdfs:comment """A digital image carrier at Manifestation level: a scan, online image
        file, or digital reproduction. Used for WebResources (edm:isShownBy /
        edm:hasView targets) of mt002 (Photo) records. Subsumes the visual-surrogate
        role of vra:Image at the carrier level."""@en .

###  mocho:facsimile
###  OUT OF SCOPE for current phase — add in follow-up ADR
###  Potential use case: sparte002 (Library) — digital reproductions of manuscripts,
###  early printed books, etc. are facsimiles of the physical originals.
###
###  mocho:facsimile rdf:type owl:ObjectProperty ;
###      rdfs:label "facsimile of"@en ;
###      rdfs:comment """The subject is a more or less precise re-rendering, reproduction
###          or visual representation of the object. A photograph of a drawing taken for
###          exhibition in a catalog would be the typical example. It does not imply
###          exactness of reproduction: a lower-resolution thumbnail can be a facsimile,
###          for example. (After Hayes & Warren 2010 mw:facsimileOf, p. 74.)"""@en ;
###      rdfs:domain mocho:ImageObject ;
###      rdfs:range  owl:Thing .
```

---

## 2. Object-type categorization (dc:type × sector → rdf:type)

### Reference tables

**Sector (sparte)**

| Code | Sector |
|---|---|
| sparte001 | Archive |
| sparte002 | Library |
| sparte003 | Monument Preservation |
| sparte004 | Research |
| sparte005 | Media Library |
| sparte006 | Museum |
| sparte007 | Others |

**Mediatype (mt)**

| Code | Mediatype |
|---|---|
| mt001 | Audio |
| mt002 | Photo |
| mt003 | Text |
| mt005 | Video |
| mt007 | Not Digitized |

This plan covers **mt002 (Photo)** only.

From corpus analysis (`output/dctype_frequency_all.csv` and `image_type2class.json`).

### Group A — 2D Visual Artworks → `vra:Work`

ProvidedCHO is the creative/physical artwork.

```python
ARTWORK_2D = {
    "Zeichnung", "Album Zeichnung", "Handzeichnung", "Zeichnung/Druckgrafik",
    "Druckgraphik", "Druckgrafik", "Druckschrift",
    "Grafik", "Graphik",
    "Studie", "Skizze", "Silhouettenbild", "Zyklus",
    "Gemälde", "Malerei", "Wandbild", "Buchmalerei",
    "Plakat", "Mappenwerk", "Kostümentwurf",
    "Flugblatt", "Einzelblattsammlung", "Akzidenzdruck (Verlagsanzeige)",
    "Rollenporträt", "Porträt",      # in sparte005 (Media Library) / sparte006 (Museum)
}
```

`Druck` in sparte006 (Museum) → `vra:Work` (printed artwork). In sparte005 (Media Library) → `mocho:ImageWork` (photographic print).

### Group B — 3D Objects → `vra:Work`

```python
OBJECTS_3D = {
    "Skulptur", "Büste", "Relief",
    "Medaille", "Münze", "Geldschein", "Notgeldschein",
    "Denkmal",
}
```

### Group C — Photographic Works → `mocho:ImageWork`

ProvidedCHO is the photographic artifact: the photograph is the Work in DDB.
Applies to sectors sparte005 (Media Library) and sparte006 (Museum).

```python
# All sectors in {sparte005, sparte006}
PHOTO_TYPES = {
    "Fotografie", "Foto",
    "Standfoto", "Kontaktbogen", "Kleinbilddia",
    "Negativ", "Negativ s/w", "Positiv",
    "Reprofotografie", "Fotoalbum",
    "Fotomechanische Reproduktion",
    "Bilddokument",
    "Ansichtskarte", "Ansichtskarte / Motivkarte",
    "Ansichtskarte / Motivkarte;Weltpostkarte",
    "Postkarte",
}

# sparte005 (Media Library) only — sector-gated
PHOTO_TYPES_MEDIA_LIBRARY_ONLY = {
    "Bild",   # too generic in other sectors
    "Druck",  # photographic print in Media Library; printed artwork in Museum (→ vra:Work via ARTWORK_2D)
}
```

Dispatch logic: for `Bild` and `Druck`, check sector first: sparte005 → `mocho:ImageWork`; sparte006 → falls through to ARTWORK_2D or sector default (`vra:Work`).

### Group D — Architectural / Built Heritage → `mocho:ImmovableWork`

Applies to **any sector** — Denkmal, Baudenkmal appear across sparte003/004/005/007.

`mocho:ImmovableWork rdfs:subClassOf mocho:Work`: built heritage fixed in the environment
(buildings, monuments, memorials). Distinct from moveable built objects (furniture, stage
sets) which remain `vra:Work`. Analogous to CIDOC-CRM `crm:E25 Human-Made Feature`.

```python
ARCHITECTURE = {
    "Baudenkmal", "Wohnhaus", "Museum", "Schule", "Universitätsinstitut",
    "Denkmal",
}
```

### Group E — Archival Documents → `rico:Record` (via htype dispatch — already handled)

Archive photos (sparte001 + dc:type ∈ PHOTO_TYPES) → **`rico:Record` only**. No image class
is added: archive photographs may or may not be creative works (documentary, bureaucratic,
administrative images are common); asserting `mocho:ImageObject` (Manifestation) or
`mocho:ImageWork` (Work) would over-specify WEMI level. The htype dispatch already gives
`rico:Record`; no additional dc:type layer fires for sparte001 + PHOTO_TYPES.

### Group F — Default → `mocho:Manifestation` (D9)

All remaining dc:types: Buch, Programmheft, Karte, Illustration (bibliographic), Seite, etc.

---

## 3. rdf:type dispatch model

### 3.1 Revised D9: ProvidedCHO typing rule

| Case | ProvidedCHO rdf:type | Condition |
|---|---|---|
| 3.1.1 Artwork 2D | `vra:Work` | dc:type ∈ ARTWORK_2D; sector ∈ {sparte005, sparte006} (Media Library, Museum) |
| 3.1.2 3D Object | `vra:Work` | dc:type ∈ OBJECTS_3D; any sector |
| 3.1.3 Photo Work | `mocho:ImageWork` | dc:type ∈ PHOTO_TYPES; sector ∈ {sparte005, sparte006} (Media Library, Museum) |
| 3.1.4 Archive photo | `rico:Record` (htype dispatch only) | sparte001 + dc:type ∈ PHOTO_TYPES — no image WEMI class added |
| 3.1.5 Architecture | `mocho:ImmovableWork` | dc:type ∈ ARCHITECTURE; any sector |
| 3.1.6 Default | `mocho:Manifestation` (D9) | all remaining |

WebResource → **always** `mocho:ImageObject` for mt002 records.

### 3.2 Turtle patterns: ProvidedCHO

**3.2.1 Museum/Media Library artwork (Zeichnung, Gemälde, Druckgraphik)**
```turtle
@prefix vra: <http://purl.org/vra/> .

<cho-uri> a vra:Work .
```

**3.2.2 Museum/Media Library photo (Fotografie, Standfoto, Postkarte)**
```turtle
@prefix mocho: <https://ise-fizkarlsruhe.github.io/ddbkg/mocho#> .

<cho-uri> a mocho:ImageWork .
# mocho:ImageWork rdfs:subClassOf mocho:Work → Work membership by inference
```

**3.2.3 Archive photo (sparte001 + PHOTO_TYPES)**

No additional class beyond the htype dispatch result. WEMI level is not asserted.

```turtle
@prefix rico: <https://www.ica.org/standards/RiC/ontology#> .

<cho-uri> a rico:Record .   # from htype dispatch; no image WEMI class added
```

### 3.3 Turtle pattern: WebResource (digital carrier)

Applied to the target URI of `edm:isShownBy` or `edm:hasView`.

```turtle
@prefix mocho: <https://ise-fizkarlsruhe.github.io/ddbkg/mocho#> .
@prefix rdac:  <http://rdaregistry.info/Elements/c/> .
@prefix rdam:  <http://rdaregistry.info/Elements/m/> .
@prefix rdact: <http://rdaregistry.info/termList/RDAct/> .
@prefix vra:   <http://purl.org/vra/> .

<webresource-uri>
    a mocho:ImageObject ;    # digital image carrier (subClassOf mocho:Manifestation)
    a rdac:C10007 ;          # RDA Manifestation class
    rdam:P30001 rdact:1018 ; # has carrier type: online resource
    vra:imageOf <cho-uri> .  # interim link; replace with mocho:facsimile in Phase B
```

- `rdact:1018` = `http://rdaregistry.info/termList/RDAct/1018` — "online resource"
- `vra:imageOf` (`owl:inverseOf vra:hasImage`): links the digital image to the Work it documents. Used as interim; `mocho:facsimile` (domain: `mocho:ImageObject`, range: `mocho:ImageWork` / `vra:Work`) replaces it in Phase B (follow-up ADR).
- `rdam:P30139` ("has expression manifested") was considered but is **Manifestation → Expression**, not Work. Dropped — DDB does not model Expression-level entities.

### 3.4 Sector-based defaults (dc:types not matched by any group)

| Sector | Default ProvidedCHO type | Rationale |
|---|---|---|
| sparte006 (Museum) | `vra:Work` | Museum objects assumed to be artworks/3D objects |
| sparte005 (Media Library) | `mocho:ImageWork` | Media Library objects assumed to be photo/image Works |
| sparte003 (Monument Preservation) | `vra:Work` | Built heritage → provisional `vra:Work` |
| sparte001 (Archive) | `mocho:Manifestation` (D9; htype handles `rico:Record`) | Archival records |
| sparte002 (Library), sparte004 (Research), sparte007 (Others) | `mocho:Manifestation` (D9) | Bibliographic / mixed |

---

## 4. Open questions

| # | Question | Status |
|---|---|---|
| 4.1 | `rdam:P30139` | **Resolved: wrong property** — "has expression manifested" (Manifestation → Expression). Dropped; `vra:imageOf` used instead until `mocho:facsimile` is defined. |
| 4.2 | Group D (architecture) | **Resolved: `mocho:ImmovableWork`** — `rdfs:subClassOf mocho:Work`; distinguishes fixed built heritage from moveable works. |
| 4.3 | `mocho:facsimile` — emit in transform for WebResource → CHO link? | **Resolved**: emit `vra:imageOf` now as interim; replace with `mocho:facsimile` in Phase B ADR |
| 4.4 | WebResource typing: in scope for current plan or separate phase? | **Resolved**: in scope — same script as ProvidedCHO dispatch |
| 4.5 | Archive photo | **Resolved**: `rico:Record` only (htype dispatch); no image WEMI class. No additional row in lookup CSV for sparte001 + PHOTO_TYPES. |

---

## 5. Corpus impact

| dc:type | total count | ProvidedCHO type |
|---|---|---|
| Zeichnung | 3379 | `vra:Work` (sparte005 Media Library, sparte006 Museum); `rico:Record` (sparte001 Archive) |
| Fotografie | 3340 | `mocho:ImageWork` (sparte005/sparte006); `rico:Record` (sparte001, htype only) |
| Druckgraphik | 2646 | `vra:Work` (sparte006 Museum, sparte002 Library) |
| Druck | 986 | `vra:Work` (sparte006 Museum); `mocho:ImageWork` (sparte005 Media Library) |
| Archivale | 924 | `rico:Record` (D9 via htype) |
| Brief | 916 | `rico:Record` (D9 via htype) |
| Gemälde | 599 | `vra:Work` (sparte006 Museum) |

WebResources for all IMAGE/mt002 records → `mocho:ImageObject` + `rdac:C10007` + `rdam:P30001 rdact:1018` + `vra:imageOf <cho-uri>` (interim; Phase B: replace with `mocho:facsimile`)

---

## 6. Files to modify

| File | Action |
|---|---|
| `mocho/mocho-odk/mocho/mocho-edit.owl` | **Manual edit** — add `mocho:ImmovableWork`, `mocho:ImageWork`, `mocho:ImageObject` per OWL definitions in §1.4; update Work+Manifestation unions |
| `scripts/gen_image_type2class.py` | Add ARTWORK_2D / OBJECTS_3D / PHOTO_TYPES / ARCHITECTURE; emit ProvidedCHO triples (`vra:Work` / `mocho:ImageWork` / etc.) **and** WebResource triples (`mocho:ImageObject` + `rdac:C10007` + `rdam:P30001 rdact:1018` + `vra:imageOf`) |
| `output/config/image_type2class.json` | Regenerated output |
| `notes/transform-script-plan.md` §3.3 | Update taxonomy |
| `notes/transform-adr.md` | New D11: revised D9 + `mocho:ImageWork`; D12: WebResource as `mocho:ImageObject` |
| `notes/image-type-class-mapping.md` | Write this plan as a standalone mapping reference note |
| `mocho/.claude/CLAUDE.md` | Add sparte/sector + mediatype reference table |
| `babel-ddb/.claude/CLAUDE.md` | Add sparte/sector + mediatype reference table |
| `gemea/.claude/CLAUDE.md` | Add sparte/sector + mediatype reference table |
| `goethe-faust/.claude/CLAUDE.md` | Add sparte/sector + mediatype reference table |

---

## 7. Verification

1. Run `gen_image_type2class.py` → inspect `output/config/image_type2class.json`
2. Spot-check: `Zeichnung__sparte006` → `vra:Work`; `Fotografie__sparte005` → `mocho:ImageWork`
3. Spot-check: `Fotografie__sparte001` → `rico:Record` only (no image WEMI class)
4. Run `gen_dctype_class_mapping.py` → inspect `output/lookup_dctype_to_class.csv`
5. Grep: no Zeichnung/Druckgraphik/Gemälde row has `rdf_type = mocho:ImageWork`
6. Check: WebResource triples → `mocho:ImageObject` + `rdac:C10007` + `rdam:P30001 rdact:1018` + `vra:imageOf <cho-uri>` on all mt002 WebResources
7. Spot-check: every `vra:imageOf` subject is a WebResource URI; object is the corresponding ProvidedCHO URI
8. Run `sample_type_dispatch.py` (Phase C); spot-check museum photo and artwork records
