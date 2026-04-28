# Graph Views Plan

## 1. Semantic Web Equivalents to Database Views

| Approach | Analog | Materialized? | Portable? | Notes |
|---|---|---|---|---|
| SPARQL CONSTRUCT query | SQL view (virtual) | No | Yes | Recomputed on demand; results can be written to a named graph |
| Named graph | Schema/partition | Yes | Yes | Organizational layer; query across selected graphs |
| OWL inference / reasoning | Computed columns | No (virtual) | Yes | Inferred triples via HermiT, ELK, or SPARQL entailment regime |
| Engine-level virtual graphs | Materialized view | Live | No | Stardog, Virtuoso — not supported by QLever |
| SHACL shapes | Schema + constraint | No | Yes | Define and validate the expected shape of each layer |

**QLever note**: no stored views; pattern is CONSTRUCT → write to named graph at pipeline time.

---

## 1.1 QLever and Named Graphs

> ⚠️ **Unconfirmed** — verify against QLever docs and current release before relying on these details.

**Supported:**
- Named graphs (quads) — index must be built from N-Quads or TriG
- `GRAPH` keyword in SELECT/CONSTRUCT queries
- Querying across multiple named graphs with `UNION` or multiple `GRAPH` clauses
- `FROM NAMED` / `DATASET` clauses

**Known limitations (to confirm):**
- **SPARQL Update** (`INSERT DATA INTO GRAPH`, `DROP GRAPH`) is limited or absent — graphs may be write-once at index time, unlike Virtuoso/Stardog
- **Default graph semantics**: QLever's default graph may be the union of all named graphs (configurable) — differs from strict SPARQL 1.1 where the default graph is empty; verify if queries depend on this

**Pipeline implication (to confirm):** the CONSTRUCT → named graph pattern likely requires graphs to be defined at index build time (loaded as N-Quads with graph IRIs), not via runtime SPARQL Update. Each pipeline run may require a full or partial reindex.

---

## 2. Goal

Relevance-ranked **work-level search** (e.g. Gounod's opera, Goethe's Faust, a stage production) with **item-level drill-down** for specialists (illustrations, manuscript pages, audio recordings).

Examples:
- "Faust" → top result is the Work entity (Goethe's text)
- "Faust Music" → Gounod's opera surfaces via sector/domain facet
- "Faust Theater" → stage productions
- Drill-down → individual items: illustrations in editions, manuscript folios, audio

---

## 3. Planned Layers

| Layer | Role | Search / UI behavior |
|---|---|---|
| **Provenance** | Source tracking (DDB, DNB, institution…) | Filtering, trust weighting, attribution |
| **Sector / Mediatype** | DDB sparte (Archive, Library, Museum…) × mediatype (Text, Audio, Photo…) | Facets: "Book", "Manuscript", "Serials", "Audio" |
| **EDM** | Individual items — photo, book scan, score page, audio file | Item-level drill-down detail |
| **mocho (FRBR/RDA)** | Work → Expression → Manifestation → Item grouping | Top result = Work entity; drives ES index |
| **Domain ontologies** | CIDOC CRM, VRA Core, RiC-O, LIO, MO, ACO, EBUCorePlus | Typed expressions, richer facets, cross-domain links |

**Sector roles** (DDB sparte, not genre):
- Book, Manuscript, Serials — primary bibliographic sectors in scope
- Also: Archive, Museum, Media Library depending on corpus

**Domain ontologies in scope** — eight alignment targets in mocho:

| Ontology | Domain | Key class(es) |
|---|---|---|
| CIDOC CRM | Museum | Events, actors, physical objects |
| VRA Core | Visual arts | `vra:Work`, `vra:Image`, `vra:Collection` |
| RiC-O | Archive | Fonds, series, file, item; provenance chain |
| LIO | Images / photo | `lio:Image` (depiction semantics) |
| MO | Music | `mo:MusicalWork/Expression/Manifestation/Item` |
| ACO | Non-musical audio | No Work-level class; generalizes MO for field recordings, oral traditions |
| EBUCorePlus | Audiovisual / broadcast | `ec:EditorialWork`, `ec:MediaResource`; no Expression tier |

**Structural stepping stones** (not alignment targets): FRBR, DocO, RDA — used in BFS traversal and bibliographic description but not independent targets.

*Not in mocho*: DOREMUS (music-specific, not integrated), TaDiRAH (research activity taxonomy, not integrated).

---

## 4. Architecture

**Approach**: materialized named graphs per layer, built by a SPARQL CONSTRUCT pipeline at ingest time. ES index driven from the mocho layer.

- **Named graph per layer** (QLever) — each CONSTRUCT step reads from the previous graph and writes to the next
- **ES index built from the mocho layer** — work-level entities drive search ranking and faceting
- **API default = work view** (mocho layer); drill-down = EDM item view
- **Sector / domain layer** drives facets — "Faust Music" routes via mediatype + domain type

**Pipeline sketch**:

```
DDB raw JSON-LD
  → [CONSTRUCT] → named graph: provenance
  → [CONSTRUCT] → named graph: sector-mediatype
  → [CONSTRUCT] → named graph: edm-normalized
  → [CONSTRUCT] → named graph: mocho-wemi
  → [CONSTRUCT] → named graph: domain-typed
  → [ES index]  ← built from mocho-wemi + domain-typed
```

**Query-time vs. materialized**: materialized is required for ES indexing and fast ranked search; SPARQL CONSTRUCT queries at query-time are reserved for ad-hoc exploration and validation.

**SHACL** validates the expected shape of each named graph after each CONSTRUCT step.
