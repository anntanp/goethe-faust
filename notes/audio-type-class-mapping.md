# Audio dc:type → MO / ACO Class Mapping — Justification

## 1. Overview

`scripts/old-config/audio_type2class.json` maps 24 German dc:type string values for
mt001 (Audio) to Music Ontology and ACO classes. Vocabularies confirmed in
`mocho-odk/src/ontology/mocho-full.owl`:

- **MO** (Music Ontology) — IRI base `http://purl.org/ontology/mo/`. Used for musical
  carriers: `mo:MusicalWork` (Work level), `mo:MusicalManifestation` (Manifestation level).
- **ACO** (Audio Commons Ontology) — IRI base `https://w3id.org/ac-ontology/aco#`. Used
  for all non-musical audio: `aco:AudioManifestation` (Manifestation level),
  `aco:AudioExpression` (Expression level, future), `aco:AudioFile` (Item level).

**Decision rule**: three-way split by dc:type semantics.

| Group | dc:type semantics | ProvidedCHO class | WEMI slot |
|---|---|---|---|
| A — Musical carriers | dc:type unambiguously denotes a musical carrier | `mo:MusicalManifestation` | M |
| B — Produced audio | dc:type denotes an authored non-musical audio document | `aco:AudioManifestation` | M |
| C — Generic / speech | dc:type is generic or denotes spoken-word content | `aco:AudioManifestation` | M |

**ProvidedCHO is Manifestation level for all audio** — unlike the image dispatch (where
W-slot classes replace `mocho:Manifestation` for the ProvidedCHO), audio ProvidedCHOs
remain at Manifestation level. `mo:MusicalWork` [W] is populated in the CSV for future
Work-entity generation but is not emitted for the ProvidedCHO by the current transform.

**MO is music-only** — `mo:MusicalManifestation`, `mo:MusicalWork`, and related MO classes
apply only to Group A. Groups B and C use ACO exclusively: MO was not designed for
general audio and would be semantically incorrect for radio broadcasts, lectures, or
speech recordings.

**`aco:AudioExpression`** [E] is noted for Group B (produced, authored audio documents)
as a future addition when expression-level modelling is in scope. It is not emitted by
the current transform.

---

## 2. Entry-by-entry justification

### 2.1 Group A — Musical carriers → `mo:MusicalManifestation` [M]

CSV also has `rdf_type_w = mo:MusicalWork` for future Work-entity generation.

#### Schallplatte → `mo:MusicalManifestation`

A standard vinyl phonograph record. The dc:type is the canonical German library term
for a musical disc carrier. MO defines `mo:MusicalManifestation` as the realization
of a musical work on a physical carrier. Sector: any.

#### Schellackplatte → `mo:MusicalManifestation`

A shellac disc (78 rpm predecessor to vinyl). An audio carrier exclusively associated
with early musical recordings. Sector: any.

#### Langspielplatte → `mo:MusicalManifestation`

A long-play vinyl disc. Remarks: "Usual topic: Oper or Opera." The dc:type denotes
a musical carrier format used for extended classical recordings. Sector: any.

#### CD → `mo:MusicalManifestation`

A compact disc audio carrier. All CD records in this corpus are musical. Sector: any.

#### Folie → `mo:MusicalManifestation`

A phonographic foil. Remarks: "Usual topic: Lied or Song." The dc:type denotes a
musical flexible-disc carrier format. Sector: any.

#### Schallfolie → `mo:MusicalManifestation`

A thin flexible phonographic disc. Topics documented in old-config: Lied, Schlager,
Kirchenmusik, Oper, Arie, Tonträger — all musical content. The dc:type is treated
as unambiguously musical across all instances in this corpus. Sector: any.

#### Tondokument → `mo:MusicalManifestation`

An audio document. Topic documented in old-config: Musicethnologie (ethnomusicological
field recordings). Despite the generic dc:type, the corpus instances are
ethnomusicological. Assigned the musical class on the basis of corpus content
(see §3, open question on topic-gating). Sector: any.

#### Ton → `mo:MusicalManifestation`

A sound/audio recording in the Museum sector. Sector: sparte006. Museum audio
objects in this corpus are predominantly musical; the old-config assigns the musical
class for this sector-restricted entry.

---

### 2.2 Group B — Produced audio → `aco:AudioManifestation` [M]

These dc:types denote authored, non-musical audio documents. MO does not apply.
`aco:AudioExpression` [E] is a future addition for expression-level modelling.

#### Audiofile → `aco:AudioManifestation`

A digital audio file. Remarks: "Often recordings of theater performances." The dc:type
is a carrier format; the content is non-musical authored audio. Sector: any.

#### Hörfunksendung → `aco:AudioManifestation`

A radio broadcast. Radio programmes are authored non-musical audio documents.
`aco:AudioManifestation` as the broadcast carrier at Manifestation level. Sector: any.

#### Inszenierung → `aco:AudioManifestation`

An audio recording of a stage production. Remarks: "Often recordings of theater
performances." Stage productions are non-musical authored works. Sector: any.

#### Band → `aco:AudioManifestation`

A volume. Remarks: "Often an audio book." The dc:type denotes a publication unit;
audio book content is authored non-musical speech. Sector: any.

#### Monografie → `aco:AudioManifestation`

A monograph in audio form (audio book or spoken-word recording of a scholarly work).
The dc:type denotes a publication type, not a musical form. Sector: any.

#### Magnettonband → `aco:AudioManifestation`

A magnetic tape reel. Sector: sparte004 (Research). Topics: Mono, Stereo (technical
characteristics). Remarks: "Audio books." Used in research and lecture recording
contexts; content is non-musical. Sector: sparte004.

#### Magnettonband / Vortrag → `aco:AudioManifestation`

A magnetic tape recording of a lecture (*Vortrag*). The compound dc:type explicitly
names both the carrier (tape) and the content type (lecture). Non-musical authored
speech. Sector: sparte006 (Museum).

#### Mono → `aco:AudioManifestation`

A monophonic audio recording. The dc:type is a technical characteristic of the
carrier, not a music type. Treated as a non-musical audio document in the Research
context. Sector: sparte004.

#### Stereo → `aco:AudioManifestation`

A stereophonic audio recording. Like `Mono`, a technical carrier descriptor in the
Research sector context. Non-musical. Sector: sparte004.

#### Platte → `aco:AudioManifestation`

A disc. In the Research sector, audio discs are catalogued as research audio
documents. Distinguished from `Schallplatte` (explicitly musical) by the generic
term and sector. Sector: sparte004.

---

### 2.3 Group C — Generic / speech → `aco:AudioManifestation` [M]

These dc:types are generic, format-level, or speech-only. No expression-level class
is assigned.

#### default → `aco:AudioManifestation`

The fallback for any mt001 record not matched by a specific dc:type. Remarks:
"Except when type is Foto, Archivalie" (handled by other dispatch layers).

#### Interview → `aco:AudioManifestation`

A recorded interview. Speech content; no musical content. Generic audio carrier.

#### Sprechplatte → `aco:AudioManifestation`

A speech disc. Remarks: "This is for specific topic to handle other types of
Schallfolie." A disc format for spoken-word recordings (poetry, radio plays, speeches).
Explicitly non-musical; `aco:AudioManifestation` rather than `aco:AudioClip`
(which denotes an excerpt, not a carrier format). Sector: any.

#### Tonaufnahme → `aco:AudioManifestation`

An audio recording. Sector: sparte002 (Library). Topics: Tierstimme (animal sounds),
Industriegeräusche (industrial sounds), Lesung (reading), Interview. Generic carrier
label; content varies widely. Sector: sparte002.

#### Tondokumente → `aco:AudioManifestation`

Plural of `Tondokument`; 3 instances of city council meeting recordings. The corpus
instances are deliberative speech, not music. Generic audio carrier. Sector: any.

#### Kardiologie → `aco:AudioManifestation`

Remarks: "This is a topic with objecttype Magnettonband." Sector: sparte006. The
dc:type is a subject field used as dc:type in some Magnettonband records. Treated
as a generic audio carrier at Manifestation level. Sector: sparte006.

---

## 3. Open questions

- **`Tondokument` topic-gating**: the musical class is assigned to all `Tondokument`
  records based on the documented `Musicethnologie` topic. If other corpora contain
  `Tondokument` records that are not ethnomusicological, the assignment is wrong.
  A topic-gated secondary dispatch cannot be implemented within the current CSV lookup
  model; flag for future controlled-vocabulary work.
- **`Ton` (Museum)**: only sparte006 documented. If `Ton` appears in other sectors,
  verify whether the musical assignment holds.
- **`aco:AudioExpression` for Group B**: deferred. When expression-level modelling
  is in scope, Group B entries should be revisited to add `rdf_type_e = aco:AudioExpression`.
- **`mo:MusicalWork` W-slot**: populated in CSV but not emitted for ProvidedCHO by
  the current transform. When Work-entity generation is implemented, Group A records
  should emit a separate Work node typed `mo:MusicalWork`.
- **GND URI dispatch**: dc:type literal is fragile as a long-term lookup key. The
  corpus already carries GND Sachbegriff URIs via `edm.RDF.Concept.about` — 98.8%
  of dc:type occurrences have a corresponding GND URI (see
  `notes/transform-edm2mocho-plan.md` §3.0). Future dispatch should key on the
  GND URI rather than the German string.
