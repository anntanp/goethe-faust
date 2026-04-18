# Video dc:type → EBUCore Plus Class Mapping — Justification

## 1. Overview

`output/config/video_type2class.json` maps 10 German dc:type string values for
mt005 (Video) to EBUCore Plus classes at the Manifestation level. The vocabulary
is confirmed in `mocho-odk/src/ontology/mocho-full.owl`; IRI base:
`http://www.ebu.ch/metadata/ontologies/ebucoreplus#`.

**Decision rule**: the Manifestation-level class (`rdf_type_m`) is assigned on a
binary split:

- `ebucoreplus:EditorialWork` — when the dc:type denotes a self-contained
  editorial work with intellectual content (documentary, interview, stage recording,
  event capture, general film). The object is an authored programme or production.
- `ebucoreplus:MediaResource` — when the dc:type denotes a media carrier, fragment,
  or promotional artefact without independent editorial status (trailer, teaser,
  film opening, slide show, generic moving image).

---

## 2. Entry-by-entry justification

### Dokumentarfilm → `ebucoreplus:EditorialWork`

A documentary film is a complete editorial work with an authorial perspective and
narrative structure. EBUCore Plus defines `EditorialObject` as content with
editorial intent; `EditorialWork` is its most general named subclass. A documentary
satisfies this definition regardless of sector. Sector: sparte005 (Museum).

### Filmanfang → `ebucoreplus:MediaResource`

A film opening (opening sequence) is a fragment of a larger work, not an
independent editorial object. It is best described as a media resource — a segment
extracted from a carrier. No independent editorial status. Sector: sparte005.

### Inszenierung → `ebucoreplus:EditorialWork`

A stage production recording (`Inszenierung`) is a video documentation of a
theatrical or musical performance. Despite being a recording of a live event, the
production itself carries authorial intent and constitutes an editorial work.
Sector: sparte006 (Research institution).

### Interview → `ebucoreplus:EditorialWork`

A recorded interview is an authored editorial object — questions and responses
constitute structured content with communicative intent. Archival interviews
(sparte001) are primary sources and editorial works in the EBUCore Plus sense.
Sector: sparte001 (Archive).

### Teaser → `ebucoreplus:EditorialWork`

A teaser is a short promotional clip produced with editorial intent to promote a
work. Although derived from or related to a larger production, it is a standalone
authored object with its own narrative structure and communicative purpose. In this
corpus (sparte005, Museum), teasers are treated as self-contained editorial works
rather than subordinate media fragments. Sector: sparte005.

### Tonbild → `ebucoreplus:EditorialWork`

*Tonbild* is a historical audiovisual format combining projected slides with
synchronised audio — a precursor to early cinema and the Gesamtkunstwerk tradition.
Despite being a combined carrier format, it is an authored work with distinct
intellectual and artistic content. In this corpus (sparte005, count=1) it is
treated as a standalone editorial work. Sector: sparte005.

### Trailer → `ebucoreplus:EditorialWork`

A trailer is a short authored promotional work produced to present a larger
production to an audience. Although it draws on material from a parent work, it
has its own editorial structure and communicative intent as a standalone artefact.
In this corpus (sparte005, Museum, count=40 — the largest single mt005 group),
trailers are treated as self-contained editorial works. Sector: sparte005.

### Veranstaltungsmitschnitt → `ebucoreplus:EditorialWork`

An event recording (`Veranstaltungsmitschnitt`) is a documentation of a live event
(concert, reading, symposium, etc.). Although it is a recording rather than an
authored work, it captures the event as a complete, bounded editorial object.
Sector: sparte005.

### Videofilm → `ebucoreplus:EditorialWork`

`Videofilm` is a generic term for a video film — a self-contained moving-image
work. Without more specificity, it defaults to the most general editorial class.
Sector: sparte006.

### zweidimensionales bewegtes Bild → `ebucoreplus:MediaResource`

"Two-dimensional moving image" (`zweidimensionales bewegtes Bild`) is a generic
RDA/ISBD carrier description term, not a content type. It describes the physical
or digital medium rather than the editorial nature of the content. Assigned
`MediaResource` as the most appropriate carrier-level class. Sector: sparte002
(Library).

---

## 3. Open questions

- **Tonbild**: only 1 instance. If more examples appear from other sectors,
  verify that the intellectual content is complete and self-contained — the
  EditorialWork assignment should hold, but manual review is warranted.
- **zweidimensionales bewegtes Bild**: the dc:type is a format descriptor, not a
  content descriptor. If genre information is available via other fields, a more
  specific class may be warranted.
