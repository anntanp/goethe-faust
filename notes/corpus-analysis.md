## 1. Creator–Agent Coverage

**Script**: `scripts/creator_agent_coverage.py`
**Data**: `data/analysis/creator_agent_coverage.csv`
**Schema**: `data/ddbedm/json_schema_paths.csv`
**Corpus**: `data/items-excerpt-1000.json` (1,000 records)

### 1.1 Method

For each `edm.RDF.ProvidedCHO.creator` value, check whether a corresponding `edm.RDF.Agent` declaration exists whose `about` URI is either a DDB organization URI (`http://www.deutsche-digitale-bibliothek.de/organization/…`) or a GND URI (`http://d-nb.info/gnd/…`). Two matching strategies:

- **URI match**: `creator[].resource` == `agent[].about`
- **Label match**: `creator[].$` in `agent[].prefLabel[].$`, with comma-order normalization (`"Lastname, Firstname"` ↔ `"Firstname Lastname"`)

### 1.2 Results

| | n | % of 488 creators |
|---|---|---|
| Creators with a resource URI | 307 | 62.9% |
| **URI match** — any agent | 307 | 62.9% |
| **URI match** — DDB org / GND agent | 301 | 61.7% |
| **Label match** — any agent (after normalization) | 408 | 83.6% |
| **Label match** — DDB org / GND agent (after normalization) | 269 | 55.1% |

### 1.3 Observations

- 37.1% of creator values carry no resource URI; they are label-only strings.
- Before name normalization, label matching found DDB org / GND agents for only 2.7% of creators. After flipping comma-order, coverage rose to 55.1% — nearly matching URI-match precision (61.7%).
- The remaining gap (~6 pp) between URI-match and label-match DDB/GND coverage consists of label-only creators that have no corresponding Agent declaration in the record.
- Name form inconsistency (`"Volbehr, Theodor"` vs `"Theodor Volbehr"`) is the dominant source of label-match failure; comma-order normalization resolves it for the majority of cases.

---

## 1b. Contributor–Agent Coverage

**Script**: `scripts/contributor_agent_coverage.py`
**Data**: `data/analysis/contributor_agent_coverage.csv`
**Schema**: `data/ddbedm/json_schema_paths.csv`
**Corpus**: `data/items-excerpt-1000.json` (1,000 records)

### 1b.1 Method

Identical to §1 (creator–agent). For each `edm.RDF.ProvidedCHO.contributor` value, check whether a corresponding `edm.RDF.Agent` declaration exists whose `about` URI is a DDB organization or GND URI. Same two matching strategies (URI match, label match with comma-order normalization).

### 1b.2 Results

| | n | % of 519 contributors |
|---|---|---|
| Contributors with a resource URI | 326 | 62.8% |
| **URI match** — any agent | 326 | 62.8% |
| **URI match** — DDB org / GND agent | 325 | 62.6% |
| **Label match** — any agent (after normalization) | 332 | 64.0% |
| **Label match** — DDB org / GND agent (after normalization) | 174 | 33.5% |

### 1b.3 Observations

- URI coverage for contributors (62.8%) closely mirrors creator (62.9%): most values carry a resource URI, and nearly all resolve to a DDB org or GND agent.
- Label match DDB/GND coverage is markedly lower than creator: 33.5% vs 55.1%. The gap reflects that many contributor values have a resource URI but a label that does not match any Agent prefLabel — the Agent URI is the reliable join key, not the label.
- Label-match precision for non-target agents is nearly equal to URI match (64.0% vs 62.8%), suggesting that when an Agent declaration exists, labels do align — but fewer contributor Agent declarations are DDB org or GND authority records compared to creators.
- Transform implication: apply the same URI resolution path as creator (D7) — when `contributor[].resource` matches an Agent whose `about` is DDB org or GND, emit `dcterms:contributor <agent.about>`.

---

## 1c. Event hasType Coverage

**Script**: `scripts/event_hastype_coverage.py`
**Data**: `data/analysis/event_hastype_coverage.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 1c.1 Method

For each `edm.RDF.Event`, collect `hasType.resource` and `hasType.$`. Count occurrences across the full corpus.

### 1c.2 Results

| n | resource | label |
|---|---|---|
| 74,034 | `http://terminology.lido-schema.org/lido00012` | — |
| 33,412 | `http://terminology.lido-schema.org/lido00228` | — |
| 19,617 | `http://terminology.lido-schema.org/lido00003` | — |
| 15,964 | `http://terminology.lido-schema.org/eventType/publication` | — |
| 6,231 | `http://terminology.lido-schema.org/eventType/creation` | — |
| 5,448 | `http://terminology.lido-schema.org/lido00007` | — |
| 2,635 | `http://terminology.lido-schema.org/lido01127` | — |
| 452 | `http://terminology.lido-schema.org/lido00011` | — |
| 218 | `http://terminology.lido-schema.org/lido00030` | — |
| 99 | `http://terminology.lido-schema.org/lido00224` | — |
| 95 | `http://terminology.lido-schema.org/lido00001` | — |
| 44 | `http://terminology.lido-schema.org/lido00004` | — |
| 34 | `http://terminology.lido-schema.org/lido00006` | — |
| 29 | `http://terminology.lido-schema.org/lido00031` | — |
| 28 | `http://terminology.lido-schema.org/lido00227` | — |
| 15 | `http://terminology.lido-schema.org/lido00226` | — |
| 13 | `http://terminology.lido-schema.org/lido00002` | — |
| 9 | `http://terminology.lido-schema.org/lido00010` | — |
| 5 | `http://terminology.lido-schema.org/lido00021` | — |
| 4 | `http://terminology.lido-schema.org/lido00033` | — |
| 3 | `http://terminology.lido-schema.org/lido00026` | — |
| 2 | `http://terminology.lido-schema.org/lido00034` | — |
| 2 | `http://terminology.lido-schema.org/lido01151` | — |
| 2 | `http://terminology.lido-schema.org/lido00008` | — |
| 2 | `http://terminology.lido-schema.org/lido00402` | — |
| 1 | `http://terminology.lido-schema.org/lido00005` | — |
| 1 | `http://terminology.lido-schema.org/lido00032` | — |

Labels pending lookup. `eventType/creation` and `eventType/publication` are self-describing; opaque `lido000xx` codes require LIDO terminology resolution.

---

## 2. dc:type — Concept Node Coverage

**Script**: `scripts/analyse_dctype.py`
**Data**: `data/analysis/dctype_coverage.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 2.1 Method

For each `ProvidedCHO.dcType` value, check: (1) whether it carries a `resource` URI and which authority it belongs to; (2) whether a `skos:Concept` node in `edm.RDF.Concept[]` declares the same URI as its `about` value (URI match); (3) whether that Concept's `prefLabel.$` matches the `dcType.$` label (label match). GND and DDB are the target authorities per the mapping task.

Note: `d-nb.info` URIs not on the `/gnd/` path are GND subject headings (Sachbegriffe) — counted with GND below. `ddb.vocnet.org` URIs do not appear as `dcType.resource` values in this corpus; they occur only in `hasType` and as `Concept.about` for mediatype/sector nodes.

### 2.2 Results

| | n | % of 92,853 dcType values |
|---|---|---|
| Total dcType values | 92,853 | — |
| Has `resource` URI | 25,607 | 27.6% |
| No `resource` URI (label only) | 67,246 | 72.4% |

URI authority breakdown (values with `resource`):

| Authority | n | % of 25,607 |
|---|---|---|
| GND (`d-nb.info/gnd/`, http+https) | 14,315 | 55.9% |
| Getty AAT (`vocab.getty.edu`) | 8,245 | 32.2% |
| Wikidata (`wikidata.org`) | 3,043 | 11.9% |
| Other | 4 | 0.0% |

Note: earlier run showed 913 `d-nb.info` entries separate from GND — these were `https://d-nb.info/gnd/` URIs not matched by the http-only prefix. Fixed in script; all fold into GND.

GND Concept node match:

| | n | % of 14,315 GND values |
|---|---|---|
| Concept node found (URI match) | 14,302 | 99.9% |
| + `prefLabel.$` matches `dcType.$` | 14,300 | 99.9% |

### 2.3 Linked-KB coverage by sector

| Sector | total dcType | GND | Getty AAT | Wikidata | linked% |
|---|---|---|---|---|---|
| Archive | 45,488 | 213 | 3,361 | 0 | 7.9% |
| Library | 32,378 | 8,397 | 159 | 3,043 | 35.8% |
| Museum | 9,215 | 2,875 | 4,123 | 0 | 75.9% |
| Media Library | 4,290 | 2,770 | 79 | 0 | 66.4% |
| Research | 1,283 | 38 | 510 | 0 | 42.7% |
| Monument Preservation | 112 | 0 | 0 | 0 | 0.0% |
| Others | 85 | 22 | 13 | 0 | 41.2% |

### 2.4 Observations

- 72.4% of `dcType` values are label-only (no `resource` URI) — uncontrolled free-text strings (e.g. "Fotoalbum", "Dokument").
- Of the 27.6% with a URI, GND accounts for 55.9%; Getty AAT 32.2%; Wikidata 11.9%.
- **Museum** has the highest linked-KB rate (75.9%), dominated by Getty AAT (4,123) alongside GND (2,875) — consistent with visual-arts cataloguing practice using AAT for object type.
- **Media Library** follows at 66.4%, entirely GND — audio/video content typed via GND subject headings.
- **Library** at 35.8% splits between GND (8,397) and Wikidata (3,043) — Wikidata appears only in Library records.
- **Archive** has the lowest rate (7.9%) despite the largest volume (45,488 values) — most archival dc:type values are uncontrolled text labels. The linked 7.9% are mainly Getty AAT.
- **Monument Preservation** at 0.0% — all dc:type values are free-text label-only.
- For GND-URI values, the `skos:Concept` node is present in-record at 99.9% and the `prefLabel` matches at 99.9%. The Concept stub is a reliable inline source.
- Transform implication: for `dcType` values carrying an authority URI, emit `<cho> dc:type <concept-uri>` and re-emit the Concept stub. Label-only values remain plain literals. See `transform-props-mapping-plan.md §7`.

---

## 3. Language Field Co-occurrence

**Script**: `scripts/analyse_language.py`
**Data**: `data/analysis/language_coverage.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 2.1 Method

For each `ProvidedCHO`, collect `dc:language` (ISO 639-2 literal) and `dcterms:language` (list of `{resource: URI}` objects pointing to `http://id.loc.gov/vocabulary/iso639-2/<code>`). Compare code sets per record; flag mismatches. Count co-occurrence and absence patterns.

### 2.2 Results

| | n | % of 115,432 |
|---|---|---|
| Has `dc:language` | 71,681 | 62.1% |
| Has `dcterms:language` | 71,681 | 62.1% |
| Has both | 71,681 | 62.1% |
| Has neither | 43,751 | 37.9% |
| Both present, codes identical | 71,119 | 99.2% of has-both |
| Both present, codes differ | 562 | 0.8% of has-both |
| `dcterms:language` not LOC URI | 0 | — |

Top language codes (`dc:language`):

| Code | n |
|---|---|
| `ger` | 63,110 |
| `eng` | 5,707 |
| `und` | 671 |
| `fre` | 522 |
| `spa` | 391 |
| `lat` | 370 |
| `ita` | 217 |
| `zxx` | 132 |
| `pol` | 90 |
| `por` | 59 |

Mismatch cardinality (562 records with differing code sets):

| dc:language cardinality | dcterms:language cardinality | n |
|---|---|---|
| 1 | 2 | 377 |
| 1 | 3 | 31 |
| 1 | 4 | 139 |
| 1 | 5–11 | 15 |

### 2.3 Observations

- `dc:language` and `dcterms:language` always co-occur: both are present or both are absent in every record.
- They are **not** duplicates. `dc:language` carries the **primary/dominant language** as a single ISO 639-2 literal. `dcterms:language` is a **multi-valued list** of all languages as LOC URIs. In 562 records, `dcterms:language` lists additional languages not in `dc:language` — the primary code is always among the LOC URIs.
- The mismatch pattern is exclusively `dc:language` cardinality 1 vs `dcterms:language` cardinality 2–11; never the reverse.
- All `dcterms:language` URIs use `http://id.loc.gov/vocabulary/iso639-2/` — no non-LOC authority URIs in the corpus.
- Transform implication: emit both fields independently; do not merge or deduplicate. For RiC-O classes, `dcterms:language` maps to `rico:hasOrHadLanguage` with the LOC URI re-typed as `rico:Language` (ADR D11). `dc:language` is kept as a literal on all classes — no RiC-O literal-valued language property exists.

---

## 2. TimeSpan ↔ date/issued Coverage

**Script**: `scripts/timespan_date_coverage.py`
**Data**: `data/analysis/timespan_date_coverage.csv`
**Schema**: `data/ddbedm/json_schema_paths.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 2.1 Method

For each record, collect `edm.RDF.ProvidedCHO.date[]` (raw strings) and `edm.RDF.ProvidedCHO.issued[].$` values, and compare against `edm.RDF.TimeSpan.begin.$` and `edm.RDF.TimeSpan.end.$`. Four match types tested in priority order:

- **exact** — date string == begin or end
- **role_stripped** — trailing role annotation stripped (`"2018 (Fotografische Aufnahme)"` → `"2018"`) before comparison
- **range_split** — ISO interval `"begin/end"` split on `/`; both parts match begin and end respectively
- **range_partial** — only one part of a split range matches
- **substring** — begin or end appears as a substring of the date string

### 2.2 Results

| | n | % of 115,432 records |
|---|---|---|
| Records with TimeSpan (begin or end) | 99,928 | 86.6% |
| Records with date or issued | 99,812 | 86.5% |
| Records with both | 96,131 | 83.3% |

Of 96,131 records with both:

| Match type | n | % of both |
|---|---|---|
| **Matched (any type)** | **94,430** | **98.2%** |
| exact | 67,394 | 70.1% |
| range_split | 16,026 | 16.7% |
| role_stripped | 4,928 | 5.1% |
| substring | 6,069 | 6.3% |
| range_partial | 13 | 0.0% |
| No match | 1,701 | 1.8% |

### 2.3 Observations

- 98.2% of records that have both a TimeSpan and date/issued values match on at least one value — TimeSpan begin/end reliably encodes the structured form of `dc:date`.
- The dominant match type is exact (70.1%), where the date string and TimeSpan value are identical.
- Range dates (`"1915-01-01/1920-12-31"`) account for 16.7% and are cleanly split by the `/` delimiter into begin and end.
- Role-annotated dates (`"2018 (Fotografische Aufnahme)"`) are resolved by stripping the trailing parenthetical (5.1%).
- 1.8% of records with both fields have no match — likely unusual date formats or data inconsistencies.
- Transform implication: `edm:TimeSpan.begin` and `.end` are the reliable structured date source for `rdam:P30278`; `dc:date` can serve as the human-readable fallback literal.

---

## 3. Place Coverage — spatial and currentLocation

**Script**: `scripts/analyse_locations.py`
**Data**: `data/analysis/locations_coverage.csv`
**Schema**: `data/ddbedm/json_schema_paths.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 3.1 Method

For each `ProvidedCHO.spatial[]` and `ProvidedCHO.currentLocation` value, check whether a matching `edm:Place` declaration exists. URI match: `value.resource == place.about`. Label match: `value.$` against `place.prefLabel[].$` with comma-order normalization. Place authority classified as GeoNames (`sws.geonames.org`, `www.geonames.org`), GND (`d-nb.info/gnd/`), or DDB internal UUID.

### 3.2 Results

**spatial** (12,332 values across corpus):

| | n | % |
|---|---|---|
| With resource URI | 10,027 | 81.3% |
| URI match → any Place | 9,984 | 81.0% |
| Label match → authority Place | 1,124 | 9.1% |
| — GeoNames | 9,201 | 74.6% |
| — GND | 419 | 3.4% |
| — DDB internal UUID | 1,094 | 8.9% |

**currentLocation** (50,385 values across corpus):

| | n | % |
|---|---|---|
| With resource URI | 50,385 | 100.0% |
| URI match → any Place | 48,386 | 96.0% |
| — GeoNames | 283 | 0.6% |
| — GND | 34,250 | 68.0% |
| — DDB internal UUID | ~13,853 | ~27.5% |

### 3.3 Event type behind spatial values

**Script**: `scripts/analyse_spatial_event_overlap.py`
**Data**: `data/analysis/spatial_event_overlap.csv`

99.5% of `spatial` resource URIs match an `Event.happenedAt` URI in the same record. The LIDO event type (`Event.hasType.resource`) for those events:

| count | % of matched | LIDO URI | label |
|------:|-------------:|----------|-------|
| 8,620 | 86.4% | lido00003 | unknown_event |
| 972 | 9.7% | lido00007 | production |
| 372 | 3.7% | lido00011 | use |
| 24 | 0.2% | lido00030 | performance |
| 18 | 0.2% | lido00002 | finding |
| 9 | 0.1% | lido00228 | publication |
| 3 | 0.0% | lido00226 | commissioning |
| 2 | 0.0% | lido00402 | conservation |
| 1 | 0.0% | lido00227 | provenance |

### 3.4 Observations

- `spatial` links primarily to GeoNames (74.6%) — geographic coordinates for the depicted or related place. GND accounts for 3.4%.
- `currentLocation` links primarily to GND (68.0%) — authority records for holding institutions (libraries, archives, museums). All values carry a resource URI (100%).
- DDB internal UUIDs appear in both fields (~9% spatial, ~28% currentLocation) — these are DDB-internal place nodes with no external authority URI, resolvable only within the DDB graph.
- Transform implication: `spatial` and `currentLocation` can emit IRI-valued triples directly from `value.resource` when the URI is GeoNames or GND. DDB internal UUID Places are valid graph nodes but not dereferenceable externally.

---

## 4. Extent — dc:extent

**Script**: `scripts/analyse_extent.py`
**Data**: `data/analysis/extent_values.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 4.1 Volume

| | n | % |
|---|---|---|
| Records with extent | 76,759 | 66.5% |
| Total extent values | 95,808 | — |
| With resource URI | 0 | 0.0% |
| Literal only | 95,808 | 100.0% |
| Distinct values | 23,988 | — |

### 4.2 Value pattern breakdown

| Pattern | n | % |
|---|---|---|
| pagination | 45,649 | 47.6% |
| dimensions | 27,895 | 29.1% |
| other free-text | 22,264 | 23.2% |

Pagination detected by presence of `S.`, `Bl.`, `Seiten`, `Blatt`, `p.`, `fol.`. Dimensions by `\d x \d` or unit suffix (`cm`, `mm`).

### 4.3 Top values (sample)

| n | value |
|---|---|
| 9,657 | Online-Ressource |
| 9,148 | Umfang: 1 Stück, 2 Blatt |
| 8,275 | Umfang: 1 Stück, 1 Blatt |
| 4,379 | 21 cm |
| 2,595 | 30 cm |
| 1,597 | 8 |
| 913 | 24 cm |
| 693 | 22 cm |
| 631 | 23 cm |
| 559 | Umfang: 1 Stück, 4 Blatt |

### 4.4 Observations

- All 95,808 values are plain literals — no authority URI. Transform emits `<cho> dc:extent "..."` directly with no dispatch needed.
- 47.6% are pagination (German/Latin: `S.`, `Bl.`, `p.`). 29.1% are physical dimensions. 23.2% are unstructured free-text.
- `Online-Ressource` (9,657) is a catalogue placeholder, not a physical extent.
- Book format codes (`8`, `gr. 8`, `kl. 8`, `12`) are historical octavo/duodecimo designations, not dimensions.

### 4.5 Future: domain-specific property dispatch

Current treatment (`dc:extent` literal) is a placeholder. A structured parse pass could dispatch into:

| pattern | RDA (Manifestation) | VRA |
|---|---|---|
| pagination | `rdam:P30182` "has extent of manifestation" | — |
| dimensions | `rdam:P30169` "has dimensions" | `vra:measurementsSet` (structured: type, value, unit) |
| still image dimensions | `rdam:P30171` "has dimensions of still image" | `vra:measurementsSet` |
| file size / digital | `rdam:P30183` "has file size" | — |

VRA Core 4 `vra:measurementsSet` supports typed structured measurements (height, width, depth, diameter) with explicit value and unit fields — preferable to a free-text literal for museum/image records.

---

## 5. Description — dc:description

**Script**: `scripts/analyse_description.py`
**Data**: `data/analysis/description_by_sector.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 5.1 Volume

| | n | % |
|---|---|---|
| Records with description | 88,443 | 76.6% |
| Total description values | 141,935 | — |
| With resource URI | 0 | 0.0% |
| Literal only | 141,935 | 100.0% |

### 5.2 Text length by sector

| Sector | records w/ desc | values | mean (chars) | median (chars) | max (chars) | coverage |
|---|---|---|---|---|---|---|
| Monument Preservation | 89 | 90 | 3,275 | 1,863 | 25,359 | 79.5% |
| Others | 81 | 138 | 405 | 76 | 3,721 | 95.3% |
| Museum | 7,835 | 17,316 | 321 | 188 | 20,415 | 85.0% |
| Archive | 49,210 | 72,208 | 317 | 138 | 96,319 | 98.0% |
| Research | 713 | 2,881 | 101 | 26 | 10,497 | 55.6% |
| Media Library | 4,233 | 9,713 | 101 | 98 | 4,776 | 98.7% |
| Library | 26,282 | 39,589 | 98 | 27 | 51,608 | 52.3% |

### 5.3 Observations

- Hypothesis (Museum has longest descriptions) is **not confirmed**: Monument Preservation has by far the highest mean (3,275 chars) and median (1,863 chars). Museum ranks third (mean 321, median 188).
- Monument Preservation sample is small (89 records) — the long descriptions likely reflect detailed heritage site documentation (provenance, architectural history, condition assessments).
- Museum descriptions are longer than Archive/Library/Media Library (mean 321 vs ~100–317) and have a high max (20,415 chars), suggesting rich curatorial prose for some objects.
- Archive has the largest absolute volume (72,208 values, 49,210 records) and near-complete coverage (98.0%) — descriptions are short (median 138 chars) and formulaic.
- Library and Research have low median lengths (27 and 26 chars) suggesting many values are brief notes rather than full descriptions.

---

## 6. isPartOf — dcterms:isPartOf

**Script**: `scripts/analyse_ispartof.py`
**Data**: `data/analysis/ispartof_coverage.csv`
**Corpus**: `data/items-all-goethe-faust.json` (115,432 records)

### 6.1 Volume

| | n | % |
|---|---|---|
| Records with isPartOf | 67,539 | 58.5% |
| Total isPartOf values | 70,311 | — |

### 6.2 Resource classification

| Kind | n | % of values |
|---|---|---|
| Full DDB item URL (`…/item/<UUID>`) | 43,814 | 62.3% |
| Bare 32-char UUID (no base URL) | 22,265 | 31.7% |
| Label only (no resource) | 4,232 | 6.0% |
| Other URI | 0 | 0.0% |

### 6.3 Observations

- 94% of values carry a resource — either full URL or bare UUID. No external authority URIs appear.
- 62.3% use the complete `http://www.deutsche-digitale-bibliothek.de/item/<UUID>` form — directly usable as object IRI.
- 31.7% carry only the bare 32-char UUID — requires prefixing with `http://www.deutsche-digitale-bibliothek.de/item/` at transform time to produce a valid IRI.
- 6.0% are label-only with no resource URI — emit as `dcterms:isPartOf "label"^^xsd:string` or skip if IRI-valued triples are required.
- Transform: normalise bare UUIDs to full URLs; emit `<cho> dcterms:isPartOf <ddb-item-uri>`.
