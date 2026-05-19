# Transcript: 0de9cbbf-84af-4e5a-9d27-80f146854276

**Project:** /Users/mta/Documents/claude/goethe-faust/scripts  
**Messages:** 303

---

### User *(2026-05-13T12:14:47.247Z)*

which part of the transform scripts /Users/mta/Documents/claude/goethe-faust/scripts/transform is responsible for emitting provenance triples?

---

### Assistant *(2026-05-13T12:14:50.579Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -rn \"provenance\\|prov:\" /Users/mta/Documents/claude/goethe-faust/scripts/transform --include=\"*.py\" -l",
  "description": "Find files mentioning provenance in transform scripts"
}
```

---

### User *(2026-05-13T12:14:50.712Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-05-13T12:14:53.852Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -rn \"prov\\|Provenance\\|wasGeneratedBy\\|wasDerivedFrom\\|Activity\\|Entity\" /Users/mta/Documents/claude/goethe-faust/scripts/transform --include=\"*.py\" -l",
  "description": "Broader search for provenance-related terms"
}
```

---

### User *(2026-05-13T12:14:53.903Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py
```

---

### Assistant *(2026-05-13T12:14:53.986Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/goethe-faust/scripts/transform/",
  "description": "List transform scripts directory"
}
```

---

### User *(2026-05-13T12:14:54.039Z)*

**Tool result**
```
README.md
__init__.py
__main__.py
constants.py
emitters.py
loaders.py
merge.py
sqlite_export.py
tests
transform.py
utils.py
```

---

### Assistant *(2026-05-13T12:14:57.277Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"prov\\|Provenance\\|wasGeneratedBy\\|wasDerivedFrom\\|Activity\\|Entity\\|PROV\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "description": "Search emitters.py for provenance terms"
}
```

---

### User *(2026-05-13T12:14:57.336Z)*

**Tool result**
```
1:"""Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, and werk_staging."""
15:    PROV_ENTITY, PROV_AGENT, PROV_SW_AGENT,
16:    PROV_DERIVED, PROV_ATTRIBUTED, PROV_GEN_TIME, PROV_ON_BEHALF,
82:def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
83:    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
86:    prov  = record.get("provider-info") or {}
94:    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
95:    provider_name   = (prov.get("provider-name")    or "").strip()
96:    provider_uri    = (prov.get("provider-uri")     or "").strip()
97:    provider_id     = (prov.get("provider-id")      or "").strip()
98:    provider_isil   = (prov.get("provider-isil")    or "").strip()
108:    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
109:               if provider_ddb_id else ""
113:    lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
115:        lines.append(make_nq(cho_nt, f"<{PROV_DERIVED}>",   f"<{ds_uri}>",   graph_iri))
117:        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
119:        lines.append(make_nq(cho_nt, f"<{PROV_GEN_TIME}>",
132:        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
140:        if prov_uri:
141:            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
142:                                 f"<{prov_uri}>", graph_iri))
147:        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
150:        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
154:    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
160:    if prov_uri:
161:        prov_nt = f"<{prov_uri}>"
162:        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
163:        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
164:        if provider_name:
165:            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
166:                                 f'"{_escape_literal(provider_name)}"', graph_iri))
167:        if provider_uri:
168:            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
169:        if provider_id:
170:            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
171:                                 f'"{_escape_literal(provider_id)}"', graph_iri))
172:        if provider_isil:
173:            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>",
174:                                 f"<{_sanitize_iri(provider_isil)}>", graph_iri))
180:        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
```

---

### Assistant *(2026-05-13T12:14:58.263Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -rn \"prov\\|Provenance\\|wasGeneratedBy\\|wasDerivedFrom\\|Activity\\|PROV\\|named.graph\\|namedGraph\" /Users/mta/Documents/claude/goethe-faust/scripts/transform --include=\"*.py\" | grep -v \"test_\"",
  "description": "Broad provenance search across all transform scripts"
}
```

---

### User *(2026-05-13T12:14:58.315Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:33:GRAPH_PROV       = "https://gemea.ise.fiz-karlsruhe.de/graph/prov"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:70:EDM_DATA_PROVIDER = EDM_NS + "dataProvider"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:77:PROV_ENTITY     = "http://www.w3.org/ns/prov#Entity"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:78:PROV_AGENT      = "http://www.w3.org/ns/prov#Agent"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:79:PROV_SW_AGENT   = "http://www.w3.org/ns/prov#SoftwareAgent"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:80:PROV_DERIVED    = "http://www.w3.org/ns/prov#wasDerivedFrom"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:81:PROV_ATTRIBUTED = "http://www.w3.org/ns/prov#wasAttributedTo"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:82:PROV_GEN_TIME   = "http://www.w3.org/ns/prov#generatedAtTime"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:83:PROV_ON_BEHALF  = "http://www.w3.org/ns/prov#actedOnBehalfOf"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:274:    "provider":            EDM_NS + "provider",
/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py:142:    sani_ctr: if provided, incremented once per IRI that required sanitisation.
/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py:143:    lang_coll: if provided, receives original collective lang codes that were normalized.
/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py:9:    MT007_IRI, GRAPH_DDBEDM, GRAPH_MOCHO, GRAPH_PROV, GRAPH_LANG_TITLE,
/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py:12:from .emitters import emit_ddbedm_triples, emit_prov_triples, emit_mocho_triples, werk_staging_row
/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py:61:    streams["prov"]   = emit_prov_triples(record, ddb_uri, GRAPH_PROV)
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:1:"""Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, and werk_staging."""
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:15:    PROV_ENTITY, PROV_AGENT, PROV_SW_AGENT,
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:16:    PROV_DERIVED, PROV_ATTRIBUTED, PROV_GEN_TIME, PROV_ON_BEHALF,
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:82:def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:83:    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:86:    prov  = record.get("provider-info") or {}
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:94:    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:95:    provider_name   = (prov.get("provider-name")    or "").strip()
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:96:    provider_uri    = (prov.get("provider-uri")     or "").strip()
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:97:    provider_id     = (prov.get("provider-id")      or "").strip()
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:98:    provider_isil   = (prov.get("provider-isil")    or "").strip()
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:108:    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:109:               if provider_ddb_id else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:113:    lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:115:        lines.append(make_nq(cho_nt, f"<{PROV_DERIVED}>",   f"<{ds_uri}>",   graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:117:        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:119:        lines.append(make_nq(cho_nt, f"<{PROV_GEN_TIME}>",
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:132:        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:140:        if prov_uri:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:141:            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:142:                                 f"<{prov_uri}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:147:        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:150:        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:154:    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:160:    if prov_uri:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:161:        prov_nt = f"<{prov_uri}>"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:162:        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:163:        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:164:        if provider_name:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:165:            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:166:                                 f'"{_escape_literal(provider_name)}"', graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:167:        if provider_uri:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:168:            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:169:        if provider_id:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:170:            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:171:                                 f'"{_escape_literal(provider_id)}"', graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:172:        if provider_isil:
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:173:            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>",
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:174:                                 f"<{_sanitize_iri(provider_isil)}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:180:        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py:3:            Produces four named-graph streams: ddbedm (verbatim EDM passthrough),
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py:4:            mocho (mocho-aligned triples), prov (PROV-O Layer 1), and a DuckDB
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py:22:              <stem>.nq                                    combined N-Quads (all named graphs)
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py:402:                    "prov":   stats["triples_prov"],
```

---

### Assistant *(2026-05-13T12:15:07.991Z)*

The provenance logic is split across two files:

**[emitters.py:82-180](goethe-faust/scripts/transform/emitters.py#L82-L180)** — `emit_prov_triples()` is where all PROV-O triples are actually constructed. It implements PROV-O Layer 1 (Without-Activity) and emits quads for:
- the CHO as `prov:Entity` with `wasDerivedFrom` (source dataset), `wasAttributedTo` (XSLT agent), and `generatedAtTime`
- the source dataset as `prov:Entity` attributed to the providing institution
- the XSLT stylesheet as `prov:SoftwareAgent` acting on behalf of DDB
- DDB and the provider institution as `prov:Agent` / `foaf:Organization`

**[transform.py:61](goethe-faust/scripts/transform/transform.py#L61)** — the call site: `streams["prov"] = emit_prov_triples(record, ddb_uri, GRAPH_PROV)`, invoked once per record.

**[constants.py:33](goethe-faust/scripts/transform/constants.py#L33)** — defines the named graph IRI (`GRAPH_PROV = "https://gemea.ise.fiz-karlsruhe.de/graph/prov"`) and the eight PROV-O term URIs (lines 77–83).

So: all triple generation lives in `emitters.py::emit_prov_triples`, orchestration in `transform.py`, vocabulary constants in `constants.py`.

---

### User *(2026-05-13T12:30:26.567Z)*

check out this script if there is mention of prov

---

### Assistant *(2026-05-13T12:30:30.439Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"prov\\|Prov\\|PROV\" /Users/mta/Documents/FIZ/workspace/fiz-ddb/src/xml2json-recursive.py",
  "description": "Search for prov mentions in xml2json-recursive.py"
}
```

---

### User *(2026-05-13T12:30:58.388Z)*

**Tool result**
```
15:CLASSES = ['ProvidedCHO', 'PhysicalThing', 'Agent', 'Event', 'Place', 'TimeSpan', 'Concept', 'Aggregation', 'WebResource', 'ProvenanceStatement', 'LinguisticSystem']
34:    'properties': 'parse_provenance',
35:    'provider-info': 'parse_provider',
40:VALID_ELEMS = ['cortex', 'edm', 'RDF', 'view', 'item', 'fields', 'properties', 'provider-info', 'source']
44:PROVENANCE_FIELDS = dict()
392:            PROVENANCE_FIELDS['source-type'] = elem.attrib['type']
399:                    if not 'source-ic' in PROVENANCE_FIELDS:
400:                        PROVENANCE_FIELDS['source-ic'] = []
401:                    PROVENANCE_FIELDS['source-ic'].append(ic_code)
406:                    PROVENANCE_FIELDS['lido-source'] = lido_obj
413:                        PROVENANCE_FIELDS['source-ref'] = field.attrib['ref']
415:                    PROVENANCE_FIELDS['source-type'] = field.attrib['type']
421:def parse_provenance(root):
423:        PROVENANCE_FIELDS[elem.tag.split('}')[-1]] = elem.text
425:def parse_provider(root):
426:    details_to_save = ['provider-name', 'provider-uri', 'provider-id', 'provider-ddb-id', 'provider-isil']
427:    PROVENANCE_FIELDS['provider'] = dict()
431:            PROVENANCE_FIELDS['provider']["".join(field.split('-')[1:])] = elem.text
453:    primary_id = PROVENANCE_FIELDS.get('source-ref', '')
455:    parent_ids = OBJECTS[OBJECT_ID]['edm:ProvidedCHO'].get('dcterms:isPartOf', [])
504:        OBJECTS[OBJECT_ID]['Prov'] = PROVENANCE_FIELDS.copy()
506:        PROVENANCE_FIELDS.clear()
```

---

### Assistant *(2026-05-13T12:31:06.578Z)*

There's provenance handling, but it's called `Prov` / `PROVENANCE_FIELDS` — not PROV-O. A few things to note:

- **Line 44 / 504**: `PROVENANCE_FIELDS` is a global dict populated during parsing, then stored under `OBJECTS[OBJECT_ID]['Prov']` at the end of each record. This is the raw source metadata (source type, IC codes, LIDO source, provider name/URI/id/isil), not PROV-O triples.
- **Lines 421–431**: `parse_provenance()` (maps to the `properties` element) and `parse_provider()` (maps to `provider-info`) fill `PROVENANCE_FIELDS` from the XML. The fields collected — `provider-name`, `provider-uri`, `provider-id`, `provider-ddb-id`, `provider-isil` — are exactly what `emit_prov_triples()` in your transform scripts reads from `record["provider-info"]`.
- **Line 15**: `ProvenanceStatement` appears in the EDM class list, but that's just part of the EDM vocabulary enumeration, not actively used for PROV-O emission here.

So this script is the **upstream source**: it extracts and bundles provider/source metadata into the JSON record. The actual PROV-O triple emission from that data happens downstream in [emitters.py:82](goethe-faust/scripts/transform/emitters.py#L82).

---

### User *(2026-05-13T12:32:22.140Z)*

there is also a portion in this script which keeps tracks of the software agent. if the software agent triple has already been emitted, there is no need to emit the descriptive triples repeatedly. can you check?

---

### Assistant *(2026-05-13T12:32:28.529Z)*

Let me check both the xml2json script and emitters for any deduplication/guard logic on the software agent.

---

### Assistant *(2026-05-13T12:32:29.043Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"software\\|SoftwareAgent\\|xslt\\|agent\\|emitted\\|already\\|once\\|seen\\|flag\\|_done\\|_sent\" /Users/mta/Documents/FIZ/workspace/fiz-ddb/src/xml2json-recursive.py",
  "description": "Search xml2json-recursive.py for software agent deduplication logic"
}
```

---

### Assistant *(2026-05-13T12:32:30.218Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"software\\|SoftwareAgent\\|xslt\\|_emitted\\|_done\\|_once\\|_seen\\|already\\|emitted_once\\|first_time\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "description": "Search emitters.py for software agent deduplication logic"
}
```

---

### User *(2026-05-13T12:32:30.297Z)*

**Tool result**
```
107:    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
116:    if xslt_uri:
117:        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
144:    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────
145:    if xslt_uri:
146:        xslt_nt = f"<{xslt_uri}>"
147:        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
148:        lines.append(make_nq(xslt_nt, f"<{DCTERMS_HAS_VER}>",
150:        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
```

---

### User *(2026-05-13T12:32:46.080Z)*

**Tool result**
```
15:CLASSES = ['ProvidedCHO', 'PhysicalThing', 'Agent', 'Event', 'Place', 'TimeSpan', 'Concept', 'Aggregation', 'WebResource', 'ProvenanceStatement', 'LinguisticSystem']
211:                            # key already exists: change to list of dicts:
395:                <lido:conceptID lido:source="iconclass" lido:type="uri">http://iconclass.org/rkd/71/</lido:conceptID>
```

---

### Assistant *(2026-05-13T12:32:48.536Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 80,
  "limit": 110
}
```

---

### User *(2026-05-13T12:32:48.612Z)*

**Tool result**
```
80	
81	
82	def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
83	    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
84	    lines: NQList = []
85	    props = record.get("properties") or {}
86	    prov  = record.get("provider-info") or {}
87	
88	    item_id         = (props.get("item-id")         or "").strip()
89	    dataset_id      = (props.get("dataset-id")      or "").strip()
90	    dataset_label   = (props.get("dataset-label")   or "").strip()
91	    revision        = (props.get("revision-id")     or "").strip()
92	    ingest_dt       = (props.get("ingest-date")     or "").strip()
93	    map_ver         = (props.get("mapping-version") or "").strip()
94	    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
95	    provider_name   = (prov.get("provider-name")    or "").strip()
96	    provider_uri    = (prov.get("provider-uri")     or "").strip()
97	    provider_id     = (prov.get("provider-id")      or "").strip()
98	    provider_isil   = (prov.get("provider-isil")    or "").strip()
99	
100	    src_desc  = (record.get("source") or {}).get("description") or {}
101	    src_ref   = (src_desc.get("record") or {}) if isinstance(src_desc, dict) else {}
102	    ref_val   = (src_ref.get("ref",  "") or "").strip() if isinstance(src_ref, dict) else ""
103	    src_href  = (src_ref.get("href", "") or "").strip() if isinstance(src_ref, dict) else ""
104	    rec_type  = (src_ref.get("type", "") or "").strip() if isinstance(src_ref, dict) else ""
105	
106	    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
107	    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
108	    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
109	               if provider_ddb_id else ""
110	
111	    # ── CHO node ──────────────────────────────────────────────────────────────
112	    cho_nt = f"<{ddb_cho_uri}>"
113	    lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
114	    if ds_uri:
115	        lines.append(make_nq(cho_nt, f"<{PROV_DERIVED}>",   f"<{ds_uri}>",   graph_iri))
116	    if xslt_uri:
117	        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
118	    if ingest_dt:
119	        lines.append(make_nq(cho_nt, f"<{PROV_GEN_TIME}>",
120	                             f'"{_escape_literal(ingest_dt)}"^^<{XSD_DATETIME}>', graph_iri))
121	    if revision:
122	        lines.append(make_nq(cho_nt, f"<{DCTERMS_HAS_VER}>",
123	                             f'"{_escape_literal(revision)}"', graph_iri))
124	    if ref_val:
125	        lines.append(make_nq(cho_nt, f"<{DCTERMS_REF}>",
126	                             f'"ddb:{_escape_literal(ref_val)}"', graph_iri))
127	
128	    # ── Dataset node ──────────────────────────────────────────────────────────
129	    if ds_uri:
130	        ds_nt = f"<{ds_uri}>"
131	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{DCAT_DATASET}>", graph_iri))
132	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
133	        lines.append(make_nq(ds_nt, f"<{DCTERMS_ID}>",
134	                             f'"{_escape_literal(dataset_id)}"', graph_iri))
135	        if dataset_label:
136	            lines.append(make_nq(ds_nt, f"<{RDFS_LABEL}>",
137	                                 f'"{_escape_literal(dataset_label)}"@de', graph_iri))
138	        if rec_type:
139	            lines.append(make_nq(ds_nt, f"<{DCTERMS_TYPE}>", f"<{rec_type}>", graph_iri))
140	        if prov_uri:
141	            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
142	                                 f"<{prov_uri}>", graph_iri))
143	
144	    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────
145	    if xslt_uri:
146	        xslt_nt = f"<{xslt_uri}>"
147	        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
148	        lines.append(make_nq(xslt_nt, f"<{DCTERMS_HAS_VER}>",
149	                             f'"{_escape_literal(map_ver)}"', graph_iri))
150	        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
151	
152	    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────
153	    ddb_nt = f"<{DDB_BASE}>"
154	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
155	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
156	    lines.append(make_nq(ddb_nt, f"<{FOAF_NAME}>",
157	                         '"Deutsche Digitale Bibliothek"', graph_iri))
158	
159	    # ── Provider Agent node ───────────────────────────────────────────────────
160	    if prov_uri:
161	        prov_nt = f"<{prov_uri}>"
162	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
163	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
164	        if provider_name:
165	            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
166	                                 f'"{_escape_literal(provider_name)}"', graph_iri))
167	        if provider_uri:
168	            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
169	        if provider_id:
170	            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
171	                                 f'"{_escape_literal(provider_id)}"', graph_iri))
172	        if provider_isil:
173	            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>",
174	                                 f"<{_sanitize_iri(provider_isil)}>", graph_iri))
175	
176	    # ── SourceRecord node (one per binary entry under same URI) ───────────────
177	    if src_href:
178	        src_rec_uri = DDB_API_BASE + src_href.lstrip("/")
179	        src_nt      = f"<{src_rec_uri}>"
180	        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
181	        for binary in coerce_list((record.get("binaries") or {}).get("binary")):
182	            if not isinstance(binary, dict):
183	                continue
184	            ref   = (binary.get("ref")            or "").strip()
185	            name  = (binary.get("name")           or "").strip()
186	            name2 = (binary.get("name2")          or "").strip()
187	            kind  = (binary.get("kind")           or "").strip()
188	            lpath = (binary.get("local_pathname") or "").strip()
189	            if ref:
```

---

### Assistant *(2026-05-13T12:32:56.544Z)*

No deduplication guard exists in `emitters.py` — the XSLT SoftwareAgent node triples ([lines 145–150](goethe-faust/scripts/transform/emitters.py#L145-L150)) and the DDB Agent node triples ([lines 152–157](goethe-faust/scripts/transform/emitters.py#L152-L157)) are re-emitted for every record. Since `xslt_uri` and `DDB_BASE` are static per run, these identical quads are repeated across all records.

`xml2json-recursive.py` has no such guard either — it only collects source data, doesn't emit triples.

The optimization you're describing — emit the descriptive triples for the XSLT agent and DDB agent only once, then just emit the `wasAttributedTo` / `actedOnBehalfOf` link per record — is currently missing. The typical pattern would be a `_emitted_agents: set` passed into `emit_prov_triples` (or held in a closure/class), checking before appending the descriptive triples. Would you like me to add that?

---

### User *(2026-05-13T12:35:06.626Z)*

plan first what to change, also (there needs to be a duckdb lookup to make this happen, right)? finally, update corresponding notes.

---

### Assistant *(2026-05-13T12:35:21.680Z)*

Let me read the relevant files before planning.

---

### Assistant *(2026-05-13T12:35:21.680Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py"
}
```

---

### Assistant *(2026-05-13T12:35:21.682Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 1,
  "limit": 82
}
```

---

### User *(2026-05-13T12:35:21.691Z)*

**Tool result**
```
1	"""Core transform: orchestrates per-record triple emission."""
2	
3	from __future__ import annotations
4	
5	from collections import Counter
6	
7	from .constants import (
8	    NQList, PropAlign,
9	    MT007_IRI, GRAPH_DDBEDM, GRAPH_MOCHO, GRAPH_PROV, GRAPH_LANG_TITLE,
10	)
11	from .utils import get_object_id, make_nq, mint_bare_id, mint_cho_uri, _extract_mediatype_sector, coerce_list
12	from .emitters import emit_ddbedm_triples, emit_prov_triples, emit_mocho_triples, werk_staging_row
13	
14	_DCTERMS_LANGUAGE = "http://purl.org/dc/terms/language"
15	_ISO639_2_BASE    = "http://id.loc.gov/vocabulary/iso639-2/"
16	
17	
18	def transform_record(
19	    record: dict,
20	    ids_set: set[str] | None,
21	    mediatype_class_map: dict,
22	    htype_map: dict,
23	    audio_type2class: dict,
24	    class_prop_align: PropAlign,
25	    lido_dispatch: dict,
26	) -> tuple[dict[str, NQList], dict | None, dict, dict]:
27	    """Transform one JSONL record into per-graph N-Quads lists (§7.1).
28	
29	    Returns (streams, werk_row, dispatch_info, pred_info).
30	    streams is empty dict when record is filtered by IDs.
31	    dispatch_info: {"target_class", "wemi", "htype_used", "fallback", "is_mt007", "mediatype"}
32	    pred_info: {"ddbedm_classes", "ddbedm_preds", "mocho_preds_all", "mocho_preds_new"} — Counters
33	    """
34	    obj_id = get_object_id(record)
35	    if obj_id is None:
36	        raise ValueError("Cannot extract object ID from record")
37	
38	    if ids_set is not None and obj_id not in ids_set:
39	        return {}, None, {}, {}
40	
41	    rdf = record["edm"]["RDF"]
42	    cho: dict = rdf.get("ProvidedCHO") or {}
43	    if isinstance(cho, list):
44	        cho = cho[0] if cho else {}
45	
46	    about_str = (cho.get("about") or "").strip()
47	    ddb_uri   = mint_bare_id("ProvidedCHO", (about_str.split()[0] if about_str else obj_id))
48	    cho_uri = mint_cho_uri(obj_id)
49	
50	    mediatype, sector = _extract_mediatype_sector(rdf.get("Concept"))
51	    is_mt007 = (mediatype == MT007_IRI)
52	
53	    streams: dict[str, NQList] = {}
54	    lang_coll: set[str] = set()
55	
56	    # Streams [1] and [4] always run, including mt007 (faithfulness + audit trail)
57	    ddbedm_lines, ddbedm_classes, ddbedm_preds, ddbedm_sani = emit_ddbedm_triples(
58	        rdf, GRAPH_DDBEDM, lang_coll,
59	    )
60	    streams["ddbedm"] = ddbedm_lines
61	    streams["prov"]   = emit_prov_triples(record, ddb_uri, GRAPH_PROV)
62	
63	    # Stream [2] mocho and [3] werk: skip mt007 (D15)
64	    werk_row: dict | None = None
65	    dispatch_info: dict = {"target_class": "", "wemi": "", "htype_used": False,
66	                           "fallback": False, "is_mt007": is_mt007, "mediatype": mediatype}
67	    if not is_mt007:
68	        mocho_lines, target_class, wemi, dflags = emit_mocho_triples(
69	            rdf, cho_uri, ddb_uri, sector, mediatype,
70	            mediatype_class_map, htype_map, audio_type2class,
71	            class_prop_align, lido_dispatch, GRAPH_MOCHO,
72	            lang_coll=lang_coll,
73	        )
74	        streams["mocho"] = mocho_lines
75	        werk_row = werk_staging_row(cho_uri, cho, target_class)
76	        mocho_preds_all  = dflags.pop("preds_all",      Counter())
77	        mocho_preds_new  = dflags.pop("preds_new",      Counter())
78	        mocho_uri_sani   = dflags.pop("uri_sanitized",  0)
79	        mocho_uri_split  = dflags.pop("uri_split",      0)
80	        dispatch_info.update({"target_class": target_class, "wemi": wemi, **dflags})
81	    else:
82	        mocho_preds_all = Counter()
83	        mocho_preds_new = Counter()
84	        mocho_uri_sani  = 0
85	        mocho_uri_split = 0
86	
87	    if lang_coll:
88	        ddb_nt = f"<{ddb_uri}>"
89	        lang_title_lines: NQList = []
90	        for orig_lang in sorted(lang_coll):
91	            lang_title_lines.append(make_nq(
92	                ddb_nt,
93	                f"<{_DCTERMS_LANGUAGE}>",
94	                f"<{_ISO639_2_BASE}{orig_lang}>",
95	                GRAPH_LANG_TITLE,
96	            ))
97	        streams[GRAPH_LANG_TITLE] = lang_title_lines
98	
99	    pred_info: dict = {
100	        "ddbedm_classes":   ddbedm_classes,
101	        "ddbedm_preds":     ddbedm_preds,
102	        "mocho_preds_all":  mocho_preds_all,
103	        "mocho_preds_new":  mocho_preds_new,
104	        "uri_sanitized":    ddbedm_sani["uri_sanitized"]  + mocho_uri_sani,
105	        "uri_split":        ddbedm_sani["uri_split"]      + mocho_uri_split,
106	        "uri_about_split":  ddbedm_sani["uri_about_split"],
107	    }
108	    return streams, werk_row, dispatch_info, pred_info
109	
```

---

### User *(2026-05-13T12:35:21.687Z)*

**Tool result**
```
1	"""Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, and werk_staging."""
2	
3	from __future__ import annotations
4	
5	from collections import Counter
6	
7	from .constants import (
8	    AgentDict, NQList, PropAlign,
9	    RDF_TYPE, RDFS_LABEL, OWL_SAMEAS,
10	    DCTERMS_SOURCE, DCTERMS_ID, DCTERMS_TYPE, DCTERMS_HAS_VER, DCTERMS_REF,
11	    DCTERMS_RIGHTS, DCTERMS_CREATOR, DCTERMS_SUBJECT,
12	    DC_ID, DC_TITLE, DC_DESCRIPTION, DC_SUBJECT, DC_CONTRIBUTOR,
13	    FOAF_ORG, FOAF_NAME, FOAF_THUMBNAIL,
14	    SCHEMA_URL, MOCHO_ISIL, MOCHO_NS, MOCHO_AGENT, RICO_HAS_RST,
15	    PROV_ENTITY, PROV_AGENT, PROV_SW_AGENT,
16	    PROV_DERIVED, PROV_ATTRIBUTED, PROV_GEN_TIME, PROV_ON_BEHALF,
17	    DCAT_DATASET, XSD_DATETIME,
18	    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, DDB_HIERARCHY_TYPE, EDM_NS, EDM_HAS_TYPE,
19	    _HTYPE_PREFIX,
20	    _EDM_ENTITY_TYPES, _DDBEDM_PROP, _MOCHO_SKIP, _NEW_NS,
21	    _CLASS_WEMI, _CONTRIBUTOR_COL, _W_SLOT_CLASSES, SUBJECT_KEYS,
22	)
23	from .utils import (
24	    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,
25	    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,
26	    build_bare_id_index, expand_obj_nt, resource_uris,
27	)
28	
29	
30	def emit_ddbedm_triples(
31	    rdf: dict,
32	    graph_iri: str,
33	    lang_coll: set[str] | None = None,
34	) -> tuple[NQList, Counter, Counter, Counter]:
35	    """Emit verbatim EDM passthrough triples for all entity types in rdf (§6.1).
36	
37	    Subject: first URI in entity['about']; owl:sameAs emitted for any additional URIs.
38	    Includes mt007 records.
39	    Returns (lines, class_ctr, pred_ctr, sani_ctr) where sani_ctr tracks
40	    uri_sanitized, uri_split, and uri_about_split counts.
41	    """
42	    lines:     NQList  = []
43	    class_ctr: Counter = Counter()
44	    pred_ctr:  Counter = Counter()
45	    sani_ctr:  Counter = Counter()
46	    _skip = frozenset({"about"})
47	    bare_id_to_uri = build_bare_id_index(rdf)
48	    for entity_type, entities in rdf.items():
49	        edm_class = _EDM_ENTITY_TYPES.get(entity_type)
50	        for entity in coerce_list(entities):
51	            if not isinstance(entity, dict):
52	                continue
53	            raw_about = (entity.get("about") or "").strip()
54	            if not raw_about:
55	                continue
56	            about_parts = raw_about.split()
57	            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
58	            subj_nt  = f"<{subj_uri}>"
59	            if len(about_parts) > 1:
60	                sani_ctr["uri_about_split"] += len(about_parts) - 1
61	                for alt in about_parts[1:]:
62	                    lines.append(make_nq(subj_nt, f"<{OWL_SAMEAS}>",
63	                                         f"<{_sanitize_iri(alt)}>", graph_iri))
64	            if edm_class:
65	                lines.append(make_nq(subj_nt, f"<{RDF_TYPE}>", f"<{edm_class}>", graph_iri))
66	                class_ctr[_to_curie(edm_class)] += 1
67	            for key, val in entity.items():
68	                if key in _skip:
69	                    continue
70	                pred_iri = _DDBEDM_PROP.get(key)
71	                if not pred_iri:
72	                    continue
73	                pred_nt = f"<{pred_iri}>"
74	                curie   = _to_curie(pred_iri)
75	                for obj_nt in value_to_nt_obj(val, sani_ctr, lang_coll):
76	                    lines.append(make_nq(subj_nt, pred_nt,
77	                                         expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))
78	                    pred_ctr[curie] += 1
79	    return lines, class_ctr, pred_ctr, sani_ctr
80	
81	
82	def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
```

---

### Assistant *(2026-05-13T12:35:25.402Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/sqlite_export.py"
}
```

---

### Assistant *(2026-05-13T12:35:25.405Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py"
}
```

---

### User *(2026-05-13T12:35:25.415Z)*

**Tool result**
```
1	"""Sequential SQLite → JSONL export for a single-sector corpus file (Option C)."""
2	
3	from __future__ import annotations
4	
5	import argparse
6	import gzip
7	import json
8	import logging
9	import sqlite3
10	from pathlib import Path
11	
12	log = logging.getLogger(__name__)
13	
14	
15	def export(
16	    db_path: Path,
17	    out_path: Path,
18	    *,
19	    log_interval: int = 100_000,
20	    limit: int | None = None,
21	) -> int:
22	    """Export all records from a single-sector SQLite to a JSONL file.
23	
24	    Sequential full-table scan of objs — no per-UID random access.
25	    Returns total records written.
26	    """
27	    out_path.parent.mkdir(parents=True, exist_ok=True)
28	    conn = sqlite3.connect(str(db_path))
29	    written = errors = 0
30	
31	    try:
32	        with open(out_path, "w", encoding="utf-8") as out:
33	            for uid, buf in conn.execute("SELECT uid, bufgz FROM objs"):
34	                try:
35	                    out.write(json.dumps(json.loads(gzip.decompress(buf)), ensure_ascii=False) + "\n")
36	                    written += 1
37	                except Exception as exc:
38	                    errors += 1
39	                    log.warning("%s uid=%s error: %s", db_path.name, uid, exc)
40	
41	                if written % log_interval == 0:
42	                    log.info("Exported %d records", written)
43	                if limit and written >= limit:
44	                    break
45	    finally:
46	        conn.close()
47	
48	    if errors:
49	        log.warning("Skipped %d records due to decompress/parse errors", errors)
50	    log.info("Export complete: %d records → %s", written, out_path)
51	    return written
52	
53	
54	def main() -> None:
55	    parser = argparse.ArgumentParser(
56	        description="Export a single-sector s{N}.sqlite to JSONL (Option C prep)"
57	    )
58	    parser.add_argument("--db",  type=Path, required=True,
59	                        help="Path to sector SQLite file (e.g. s2.sqlite)")
60	    parser.add_argument("--out", type=Path, required=True,
61	                        help="Output JSONL file path")
62	    parser.add_argument("--limit", type=int, default=None,
63	                        help="Stop after N records (for dryruns)")
64	    parser.add_argument("--log-level", default="INFO", dest="log_level",
65	                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
66	    args = parser.parse_args()
67	
68	    logging.basicConfig(
69	        level=getattr(logging, args.log_level),
70	        format="%(asctime)s %(levelname)s %(message)s",
71	    )
72	
73	    n = export(args.db, args.out, limit=args.limit)
74	    print(f"{n:,} records → {args.out}")
75	
76	
77	if __name__ == "__main__":
78	    main()
79	
```

---

### User *(2026-05-13T12:35:25.416Z)*

**Tool result**
```
1	"""
2	Purpose:    Transform DDB-EDM JSONL records to mocho-aligned N-Quads.
3	            Produces four named-graph streams: ddbedm (verbatim EDM passthrough),
4	            mocho (mocho-aligned triples), prov (PROV-O Layer 1), and a DuckDB
5	            werk_staging table for GND Werk linking (link_gnd_works.py, Phase 0).
6	            Reference implementation for the mocho ingest pipeline.
7	            Decisions: transform-adr.md D11/D15/D17, transform-script-adr.md D1–D27.
8	Usage:      python -m transform
9	                [--jsonl FILE] [--ids FILE] [--outdir DIR]
10	                [--alignment FILE] [--lido FILE] [--htype FILE]
11	                [--mediatype FILE] [--audio FILE]
12	                [--stats LEVEL] [--log-level LEVEL]
13	                [--limit N] [--total N] [--log-interval N] [--debug]
14	Inputs:     data/items-all-goethe-faust.json              JSONL, one record per line
15	            data/ids-all-goethe-faust.txt                  32-char object IDs, one per line
16	            output/config/lookup_class_prop_alignment.csv  (target_class, edm_prop) → target_prop
17	            output/config/lido_event_types.csv             lido_uri → agent predicates per WEMI
18	            output/config/lookup_htype_doco_rico.csv       htype_code → (rdf_type, rst_iris)
19	            output/config/lookup_mediatype_class.csv       (sparte, mediatype) → class dispatch row
20	            output/config/audio_type2class.json            mt001 dc:type → group (A/B/C)
21	Outputs:    output/transform/YYYYMMDD_HHMMSS/               run directory (one per invocation)
22	              <stem>.nq                                    combined N-Quads (all named graphs)
23	              <stem>-werk-staging.duckdb                  W-slot staging rows
24	              <stem>-stats.json                           run statistics
25	              <stem>-errors.jsonl                         per-record errors (written live)
26	              <stem>.log                                  run log
27	            <stem> is the input filename without extension (e.g. s2 → s2.nq)
28	Deps:       stdlib only + duckdb (pip install duckdb)
29	Assumes:    JSONL: one JSON object per line; record structure edm.RDF.*
30	            All config CSVs present at output/config/
31	            Graceful exit on SIGINT/SIGTERM: partial stats and errors are written.
32	"""
33	
34	from __future__ import annotations
35	
36	import argparse
37	import json
38	import logging
39	import signal
40	import sys
41	import time
42	import traceback
43	from collections import Counter
44	from datetime import datetime
45	from pathlib import Path
46	
47	from .constants import (
48	    DEFAULT_JSONL, DEFAULT_ALIGNMENT, DEFAULT_LIDO, DEFAULT_HTYPE,
49	    DEFAULT_MEDIATYPE, DEFAULT_AUDIO, DEFAULT_OUTPUT_BASE,
50	)
51	from .utils import get_object_id, _to_curie
52	from .loaders import (
53	    load_ids, load_class_prop_alignment, load_lido_event_types,
54	    load_htype_map, load_mediatype_class, load_audio_type2class,
55	)
56	from .transform import transform_record
57	
58	
59	_stop = False
60	
61	
62	def _handle_signal(sig, frame) -> None:
63	    global _stop
64	    _stop = True
65	    print(f"\nSignal {sig} received — stopping after current record ...", file=sys.stderr)
66	
67	
68	signal.signal(signal.SIGINT,  _handle_signal)
69	signal.signal(signal.SIGTERM, _handle_signal)
70	
71	
72	def _fmt_duration(seconds: float) -> str:
73	    h, r = divmod(int(seconds), 3600)
74	    m, s = divmod(r, 60)
75	    return f"{h:02d}:{m:02d}:{s:02d}"
76	
77	
78	def main() -> None:
79	    if len(sys.argv) > 1 and sys.argv[1] == "merge":
80	        from .merge import main as _merge_main
81	        sys.argv = [sys.argv[0]] + sys.argv[2:]
82	        _merge_main()
83	        return
84	
85	    parser = argparse.ArgumentParser(
86	        description="Transform DDB-EDM JSONL to mocho N-Quads (§8)"
87	    )
88	
89	    io = parser.add_argument_group("I/O")
90	    io.add_argument("--jsonl",  type=Path, default=DEFAULT_JSONL,
91	                    help="JSONL input file (one DDB-EDM JSON object per line); "
92	                         "default: data/items-all-goethe-faust.json")
93	    io.add_argument("--db",     type=Path, default=None,
94	                    help="SQLite sector file — reads directly without intermediate JSONL export; "
95	                         "mutually exclusive with --jsonl")
96	    io.add_argument("--offset", type=int,  default=0,
97	                    help="Skip first N rows in SQLite (for parallel workers; use with --db and --limit)")
98	    io.add_argument("--ids",    type=str,  default=None,
99	                    help="Path to ID allowlist file (one 32-char DDB ID per line), "
100	                         "or '-' to read from stdin; omit to process all records")
101	    io.add_argument("--outdir", type=Path, default=None,
102	                    help="Output directory; auto-timestamped if omitted "
103	                         "(default: output/transform/YYYYMMDD_HHMMSS)")
104	    io.add_argument("--stem", type=str, default=None,
105	                    help="Output filename stem (overrides the input filename); "
106	                         "e.g. --stem items-all-goethe-faust → items-all-goethe-faust.nq, etc.")
107	
108	    cfg = parser.add_argument_group("Config")
109	    cfg.add_argument("--alignment", type=Path, default=DEFAULT_ALIGNMENT,
110	                     help="Property alignment lookup CSV "
111	                          "(target_class, edm_prop) → mocho property; "
112	                          "default: output/config/lookup_class_prop_alignment.csv")
113	    cfg.add_argument("--lido",      type=Path, default=DEFAULT_LIDO,
114	                     help="LIDO event type dispatch CSV "
115	                          "(event URI → agent predicates per WEMI level); "
116	                          "default: output/config/lido_event_types.csv")
117	    cfg.add_argument("--htype",     type=Path, default=DEFAULT_HTYPE,
118	                     help="htype → class lookup CSV "
119	                          "(htype_code → rdf:type IRIs for §1.1 dispatch); "
120	                          "default: output/config/lookup_htype_doco_rico.csv")
121	    cfg.add_argument("--mediatype", type=Path, default=DEFAULT_MEDIATYPE,
122	                     help="Mediatype × sector → class lookup CSV "
123	                          "(sector, mediatype → WEMI class IRIs); "
124	                          "default: output/config/lookup_mediatype_class.csv")
125	    cfg.add_argument("--audio",     type=Path, default=DEFAULT_AUDIO,
126	                     help="mt001 dc:type → audio group JSON "
127	                          "(dc:type value → A/B/C group for audio class dispatch); "
128	                          "default: output/config/audio_type2class.json")
129	
130	    run = parser.add_argument_group("Run control")
131	    run.add_argument("--stats",     choices=["none", "basic", "dispatch", "full"],
132	                     default="basic",
133	                     help="Stats verbosity written to transform_stats.json: "
134	                          "none=nothing written, basic=run/records/triples/werk_staging, "
135	                          "dispatch=basic+WEMI class counts (recommended for full-corpus runs), "
136	                          "full=dispatch+per-predicate mocho counts (slow — use with --limit); "
137	                          "default: basic")
138	    run.add_argument("--log-level", default="INFO",
139	                     choices=["DEBUG", "INFO", "WARNING", "ERROR"],
140	                     dest="log_level",
141	                     help="Console and file log verbosity; default: INFO")
142	    run.add_argument("--limit",        type=int, default=None,
143	                     help="Stop after N records — for smoke-testing and sampling")
144	    run.add_argument("--total",        type=int, default=None,
145	                     help="Expected total records — enables ETA in progress log")
146	    run.add_argument("--log-interval", type=int, default=100_000, dest="log_interval",
147	                     help="Log a progress line every N records (default: 100000)")
148	    run.add_argument("--debug",     action="store_true",
149	                     help="Enable DEBUG logging (shorthand for --log-level DEBUG)")
150	
151	    args = parser.parse_args()
152	    if args.debug:
153	        args.log_level = "DEBUG"
154	
155	    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
156	    outdir = args.outdir or (DEFAULT_OUTPUT_BASE / ts)
157	    outdir.mkdir(parents=True, exist_ok=True)
158	
159	    if args.stem:
160	        stem = args.stem
161	    elif args.db:
162	        stem = args.db.stem + (f"-{args.offset}" if args.offset else "")
163	    else:
164	        stem = Path(args.jsonl).stem
165	    out_path    = outdir / f"{stem}.nq"
166	    werk_path   = outdir / f"{stem}-werk-staging.duckdb"
167	    stats_path  = outdir / f"{stem}-stats.json"
168	    errors_path = outdir / f"{stem}-errors.jsonl"
169	    log_path    = outdir / f"{stem}.log"
170	
171	    logging.basicConfig(
172	        filename=str(log_path),
173	        level=getattr(logging, args.log_level),
174	        format="%(asctime)s %(levelname)s %(message)s",
175	    )
176	    log = logging.getLogger(__name__)
177	
178	    log.info("Loading config tables")
179	    class_prop_align    = load_class_prop_alignment(args.alignment)
180	    lido_dispatch       = load_lido_event_types(args.lido)
181	    htype_map           = load_htype_map(args.htype)
182	    mediatype_class_map = load_mediatype_class(args.mediatype)
183	    audio_type2class    = load_audio_type2class(args.audio)
184	
185	    ids_set: set[str] | None = None
186	    if args.ids == "-":
187	        ids_set = {line.strip() for line in sys.stdin if line.strip()}
188	    elif args.ids:
189	        ids_set = load_ids(Path(args.ids))
190	
191	    try:
192	        import duckdb
193	        conn = duckdb.connect(str(werk_path))
194	    except ImportError:
195	        log.warning("duckdb not available — werk_staging will not be written")
196	        conn = None
197	    if conn is not None:
198	        conn.execute("""
199	        CREATE TABLE IF NOT EXISTS werk_staging (
200	            ddb_obj_id       VARCHAR PRIMARY KEY,
201	            cho_uri          VARCHAR,
202	            target_class     VARCHAR,
203	            dc_title         VARCHAR,
204	            dc_alternative   VARCHAR[],
205	            dc_created       VARCHAR,
206	            creator_uris     VARCHAR[],
207	            creator_literals VARCHAR[]
208	        )
209	    """)
210	
211	    stats_level = args.stats
212	
213	    stats:  Counter = Counter()
214	
215	    class_counts: dict[str, Counter] = {"W": Counter(), "E": Counter(), "M": Counter(), "": Counter()}
216	    mt_dist:         Counter = Counter()
217	    ht_dist:         Counter = Counter()
218	    ddbedm_cls:      Counter = Counter()
219	    ddbedm_preds:    Counter = Counter()
220	    mocho_preds_all: Counter = Counter()
221	    mocho_preds_new: Counter = Counter()
222	    werk_by_class:   Counter = Counter()
223	
224	    start_time = time.monotonic()
225	    interrupted = False
226	
227	    def _iter_input():
228	        if args.db:
229	            import gzip
230	            import sqlite3 as _sqlite3
231	            conn = _sqlite3.connect(str(args.db))
232	            try:
233	                q = "SELECT uid, bufgz FROM objs"
234	                if args.offset:
235	                    q += f" LIMIT -1 OFFSET {args.offset}"
236	                for uid, buf in conn.execute(q):
237	                    try:
238	                        yield json.dumps(json.loads(gzip.decompress(buf)))
239	                    except Exception as exc:
240	                        log.warning("%s uid=%s: %s", args.db.name, uid, exc)
241	                        yield ""
242	            finally:
243	                conn.close()
244	        else:
245	            with open(args.jsonl, encoding="utf-8") as f:
246	                yield from f
247	
248	    with open(out_path, "w", encoding="utf-8") as out, \
249	         open(errors_path, "w", encoding="utf-8") as err_fh:
250	
251	        for line_no, raw in enumerate(_iter_input(), 1):
252	            if _stop:
253	                interrupted = True
254	                log.warning("Interrupted at line %d — writing partial output", line_no)
255	                break
256	
257	            raw = raw.strip()
258	            if not raw:
259	                continue
260	            if args.limit and line_no > args.limit:
261	                break
262	
263	            try:
264	                record = json.loads(raw)
265	            except json.JSONDecodeError as exc:
266	                entry = {"line": line_no, "issue": f"JSON parse error: {exc}"}
267	                err_fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
268	                stats["json_errors"] += 1
269	                continue
270	
271	            obj_id = get_object_id(record) or f"line:{line_no}"
272	            try:
273	                streams, werk_row, dispatch_info, pred_info = transform_record(
274	                    record, ids_set,
275	                    mediatype_class_map, htype_map, audio_type2class,
276	                    class_prop_align, lido_dispatch,
277	                )
278	            except Exception as exc:
279	                entry = {
280	                    "id":        obj_id,
281	                    "issue":     str(exc),
282	                    "traceback": traceback.format_exc(),
283	                }
284	                err_fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
285	                stats["record_errors"] += 1
286	                continue
287	
288	            if not streams:
289	                stats["filtered"] += 1
290	                continue
291	
292	            for graph_name, graph_lines in streams.items():
293	                for nq in graph_lines:
294	                    out.write(nq + "\n")
295	                    stats["triples_total"] += 1
296	                    stats[f"triples_{graph_name}"] += 1
297	
298	            stats["records_processed"]  += 1
299	            stats["uri_sanitized"]      += pred_info.get("uri_sanitized",   0)
300	            stats["uri_split"]          += pred_info.get("uri_split",       0)
301	            stats["uri_about_split"]    += pred_info.get("uri_about_split", 0)
302	
303	            if stats_level in ("dispatch", "full"):
304	                if dispatch_info.get("is_mt007"):
305	                    stats["skipped_mt007"] += 1
306	                elif dispatch_info.get("fallback"):
307	                    stats["dispatch_fallback"] += 1
308	                elif dispatch_info.get("htype_used"):
309	                    stats["dispatch_htype"] += 1
310	                else:
311	                    stats["dispatch_mediatype"] += 1
312	
313	                tc = dispatch_info.get("target_class", "")
314	                if tc:
315	                    wemi = dispatch_info.get("wemi", "M")
316	                    class_counts[wemi][_to_curie(tc)] += 1
317	
318	                mt = (dispatch_info.get("mediatype", "") or "").split("/")[-1]
319	                if mt:
320	                    mt_dist[mt] += 1
321	
322	                rdf_top = record["edm"]["RDF"]
323	                cho_raw = rdf_top.get("ProvidedCHO") or {}
324	                if isinstance(cho_raw, list):
325	                    cho_raw = cho_raw[0] if cho_raw else {}
326	                raw_ht = (cho_raw.get("hierarchyType") or "").strip()
327	                if raw_ht:
328	                    ht_dist[raw_ht.replace("htype_", "ht")] += 1
329	
330	                ddbedm_cls.update(pred_info["ddbedm_classes"])
331	                ddbedm_preds.update(pred_info["ddbedm_preds"])
332	                mocho_preds_all.update(pred_info["mocho_preds_all"])
333	                mocho_preds_new.update(pred_info["mocho_preds_new"])
334	
335	            if werk_row and conn is not None:
336	                conn.execute(
337	                    "INSERT OR REPLACE INTO werk_staging VALUES (?,?,?,?,?,?,?,?)",
338	                    [
339	                        werk_row["ddb_obj_id"],
340	                        werk_row["cho_uri"],
341	                        werk_row["target_class"],
342	                        werk_row["dc_title"],
343	                        werk_row["dc_alternative"],
344	                        werk_row["dc_created"],
345	                        werk_row["creator_uris"],
346	                        werk_row["creator_literals"],
347	                    ],
348	                )
349	                stats["werk_staging_rows"] += 1
350	                werk_by_class[_to_curie(werk_row["target_class"])] += 1
351	
352	            processed = stats["records_processed"]
353	            if args.log_interval and processed and processed % args.log_interval == 0:
354	                elapsed = time.monotonic() - start_time
355	                rate    = processed / elapsed if elapsed > 0 else 0
356	                errors  = stats["json_errors"] + stats["record_errors"]
357	                eta_str = ""
358	                if args.total and rate > 0:
359	                    remaining = (args.total - processed) / rate
360	                    eta_str   = f" | ETA {_fmt_duration(remaining)}"
361	                total_str = f"/{args.total:,}" if args.total else ""
362	                log.info(
363	                    "Progress: %s%s records | triples %d | errors %d"
364	                    " | %.0f rec/s | elapsed %s%s",
365	                    f"{processed:,}", total_str,
366	                    stats["triples_total"], errors,
367	                    rate, _fmt_duration(elapsed), eta_str,
368	                )
369	
370	    if conn is not None:
371	        conn.close()
372	
373	    elapsed_total = time.monotonic() - start_time
374	
375	    if stats_level != "none":
376	        stats_out: dict = {
377	            "run": {
378	                "timestamp":   ts,
379	                "input":       str(args.jsonl),
380	                "stats_level": stats_level,
381	                "elapsed_s":   round(elapsed_total, 1),
382	                "interrupted": interrupted,
383	            },
384	            "records": {
385	                "processed":          stats["records_processed"],
386	                "skipped_not_in_ids": stats["filtered"],
387	                "by_mediatype": dict(mt_dist.most_common()),
388	                "by_htype":     dict(ht_dist.most_common()),
389	                "uri_sanitized":   stats["uri_sanitized"],
390	                "uri_split":       stats["uri_split"],
391	                "uri_about_split": stats["uri_about_split"],
392	                "errors": {
393	                    "json_parse": stats["json_errors"],
394	                    "transform":  stats["record_errors"],
395	                },
396	            },
397	            "triples": {
398	                "total":    stats["triples_total"],
399	                "by_graph": {
400	                    "ddbedm": stats["triples_ddbedm"],
401	                    "mocho":  stats["triples_mocho"],
402	                    "prov":   stats["triples_prov"],
403	                },
404	            },
405	            "werk_staging": {
406	                "rows":     stats["werk_staging_rows"],
407	                "by_class": dict(werk_by_class.most_common()),
408	            },
409	        }
410	
411	        if stats_level in ("dispatch", "full"):
412	            stats_out["dispatch"] = {
413	                "htype_hits":            stats["dispatch_htype"],
414	                "mediatype_hits":        stats["dispatch_mediatype"],
415	                "fallback_d9":           stats["dispatch_fallback"],
416	                "skipped_mt007":         stats["skipped_mt007"],
417	                "work_classes":          dict(class_counts["W"].most_common()),
418	                "expression_classes":    dict(class_counts["E"].most_common()),
419	                "manifestation_classes": dict(class_counts["M"].most_common()),
420	                "rico_classes":          dict(class_counts[""].most_common()),
421	            }
422	            stats_out["ddbedm_classes"] = dict(ddbedm_cls.most_common())
423	            stats_out["ddbedm_vocab"]   = {"properties_all": dict(ddbedm_preds.most_common())}
424	            stats_out["mocho_vocab"]    = {
425	                "properties_all": dict(mocho_preds_all.most_common()),
426	                "properties_new": dict(mocho_preds_new.most_common()),
427	            }
428	
429	        with open(stats_path, "w", encoding="utf-8") as f:
430	            json.dump(stats_out, f, indent=2)
431	
432	    status = "Interrupted" if interrupted else "Done"
433	    log.info(
434	        "%s: %d records in %s (%.0f rec/s) | triples %d (mocho %d) | errors %d",
435	        status,
436	        stats["records_processed"],
437	        _fmt_duration(elapsed_total),
438	        stats["records_processed"] / elapsed_total if elapsed_total > 0 else 0,
439	        stats["triples_total"],
440	        stats["triples_mocho"],
441	        stats["record_errors"] + stats["json_errors"],
442	    )
443	
444	
445	if __name__ == "__main__":
446	    main()
447	
```

---

### Assistant *(2026-05-13T12:35:52.340Z)*

Now let me check what notes exist for PROV-O.

---

### Assistant *(2026-05-13T12:35:52.668Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/goethe-faust/notes/ && find /Users/mta/Documents/claude/goethe-faust/notes -name \"*prov*\" -o -name \"*adr*\"",
  "description": "List notes directory and find prov/adr notes"
}
```

---

### User *(2026-05-13T12:35:52.756Z)*

**Tool result**
```
adhoc-manifestation-types.md
audio-type-class-mapping.md
corpus-analysis.md
ddbedm-prov-o-plan.md
entity-property-mapping.md
goethe-faust-gnd-linking-plan.md
graph-views-plan.md
how-claude-transcript.md
image-type-class-mapping.md
images
infra-local-setup.md
inputs.md
isbd-title-analysis.md
memory-handover-20260414.md
mermaid-shmarql-qlever-mcp.pdf
mermaid-yasgui-qlever-mcp-shmarql-pyoxygraph.pdf
ollama-qlever-mcp-plan.md
openwebui-native-tool.md
openwebui-ollama-setup.md
outputs.md
plan-check-script.md
plan-configurable-setup.md
prov-lm-future-plan.md
s4-dispatch-plan.md
session-summary-final-dataset.md
tabularasa-mocho-plan.md
tabularasa.md
teach01-shmarql-qlever.pdf
transform-adr.md
transform-cli-spec.md
transform-dryrun-plan.md
transform-duckdb-plan.md
transform-future-plan.md
transform-implementation-actual.md
transform-implementation-plan.md
transform-lezdoit-plan.md
transform-props-mapping-adr.md
transform-props-mapping-plan.md
transform-revised-plan.md
transform-script-adr.md
transform-script-plan.md
transform-stale
transform-stats-plan.md
transform-validation.md
transform-writeup.md
troubleshooting-mcpo.md
troubleshooting-openwebui-password.md
video-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/prov-lm-future-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md
```

---

### Assistant *(2026-05-13T12:35:54.985Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md"
}
```

---

### User *(2026-05-13T12:35:55.003Z)*

**Tool result**
```
1	# DDB-EDM PROV-O mapping plan
2	
3	**Date**: 2026-05-01 (updated 2026-05-03)
4	**Status**: In progress
5	**Reference**: `references/rm-018-prov-o.pdf` (slides 11–16)
6	**ADR**: `notes/transform-adr.md` D11, D12
7	**JSON source**: `data/items-excerpt-1000.json`
8	
9	---
10	
11	## 1. Overview
12	
13	Two provenance layers:
14	
15	| Layer | Granularity | Pattern | Storage |
16	|---|---|---|---|
17	| **1 — Item** | Per CHO: DDB-EDM source metadata | Without-Activity (slide 13) | Item's own named graph |
18	| **2 — Graph** | Per named graph: pipeline run that produced it | Full Activity (slide 12) | `<urn:goethe-faust:graph/prov>` |
19	
20	Layer 1 answers: *where does this CHO's data come from in the DDB ecosystem?*
21	Layer 2 answers: *which script run, at what version and time, wrote triples into this graph — and was inference involved?*
22	
23	---
24	
25	## 2. Layer 1 — Fine-grained item provenance
26	
27	### 2.1 Graph structure (Without-Activity pattern)
28	
29	Five nodes per item. The full Activity pattern is not used — added expressivity
30	(blank node or per-item Activity IRI) is not justified for ingest-time metadata.
31	
32	```
33	ddb:CHO ──prov:wasDerivedFrom──────────► Dataset
34	        ──prov:wasAttributedTo──────────► XSLT
35	        ──prov:generatedAtTime──────────► "2026-01-07T15:40:43+0100"
36	        ──dcterms:hasVersion────────────► "43"
37	        ──dcterms:references────────────► "ddb:<source-ref>"
38	
39	Dataset ──prov:wasAttributedTo──────────► Provider
40	
41	XSLT    ──prov:actedOnBehalfOf──────────► DDB
42	```
43	
44	| Node | PROV-O type | URI pattern |
45	|---|---|---|
46	| CHO | `prov:Entity` | `ddb:item/<properties.item-id>` |
47	| Dataset | `dcat:Dataset`, `prov:Entity` | `urn:ddbedm:properties:dataset-id:<id>` |
48	| XSLT | `prov:SoftwareAgent` | `urn:ddbedm:properties:mapping-version:<ver>` |
49	| Provider | `prov:Agent`, `foaf:Organization` | `urn:ddbedm:provider-info:provider-ddb-id:<id>` |
50	| DDB | `prov:Agent`, `foaf:Organization` | `<http://www.deutsche-digitale-bibliothek.de>` (fixed) |
51	
52	**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key
53	chain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without
54	requiring a dereferenceable endpoint.
55	
56	### 2.2 JSON field → triple mapping
57	
58	#### 2.2.1 JSON source structure
59	
60	The relevant fields are spread across three top-level blocks:
61	
62	```json
63	{
64	  "properties": {
65	    "item-id":            "222NZKK63TNRLC2VETRV722VKBDSUVGL",
66	    "dataset-id":         "76409877634279609sQOu",
67	    "dataset-label":      "Gesamtlieferung: Deutsche Fotothek - LIDO",
68	    "revision-id":        "43",
69	    "ingest-date":        "2026-01-07T15:40:43+0100",
70	    "mapping-version":    "6.18",
71	    "cortex-type":        "Kultur"
72	  },
73	  "provider-info": {
74	    "provider-name":      "Deutsche Fotothek",
75	    "provider-uri":       "http://www.deutschefotothek.de",
76	    "provider-id":        "99900890",
77	    "provider-ddb-id":    "CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI",
78	    "provider-isil":      "http://ld.zdb-services.de/resource/organisations/DE-2396"
79	  },
80	  "source": {
81	    "description": {
82	      "record": {
83	        "ref":  "222NZKK63TNRLC2VETRV722VKBDSUVGL",
84	        "href": "/items/222NZKK63TNRLC2VETRV722VKBDSUVGL/source/record",
85	        "type": "http://www.lido-schema.org/"
86	      }
87	    }
88	  },
89	  "binaries": {
90	    "binary": [
91	      {
92	        "ref":            "0ac6ad6e-a985-4251-91ca-f4b918326ead",
93	        "name":           "Abb. Vorsatz. Titelblatt auf fliegendem Blatt...",
94	        "name2":          "Urheber*in: DDZ (Fotografische Aufnahme)",
95	        "kind":           "http://rightsstatements.org/vocab/InC/1.0/",
96	        "local_pathname": "http://fotothek.slub-dresden.de/fotos/df_pos-2018-a_0000067_000_f.jpg",
97	        "primary":        true
98	      }
99	    ]
100	  }
101	}
102	```
103	
104	#### 2.2.2 CHO (`ddb:item/<properties.item-id>`)
105	
106	| Triple | JSON path | Value type |
107	|---|---|---|
108	| `rdf:type` | — | `edm:ProvidedCHO`, `prov:Entity` |
109	| `prov:wasDerivedFrom` | `properties.dataset-id` → Dataset URN | URN |
110	| `prov:wasAttributedTo` | `properties.mapping-version` → XSLT URN | URN |
111	| `prov:generatedAtTime` | `properties.ingest-date` | xsd:dateTime literal |
112	| `dcterms:hasVersion` | `properties.revision-id` | string literal |
113	| `dcterms:references` | `source.description.record.ref` | `"ddb:<ref>"` literal |
114	
115	#### 2.2.3 Dataset (`urn:ddbedm:properties:dataset-id:<value>`)
116	
117	| Triple | JSON path | Value type |
118	|---|---|---|
119	| `rdf:type` | — | `dcat:Dataset`, `prov:Entity` |
120	| `dcterms:identifier` | `properties.dataset-id` | string literal |
121	| `rdfs:label` | `properties.dataset-label` | `@de` literal |
122	| `dcterms:type` | `source.description.record.type` | URI |
123	| `prov:wasAttributedTo` | `provider-info.provider-ddb-id` → Provider URN | URN |
124	
125	#### 2.2.4 XSLT (`urn:ddbedm:properties:mapping-version:<value>`)
126	
127	| Triple | JSON path | Value type |
128	|---|---|---|
129	| `rdf:type` | — | `prov:SoftwareAgent` |
130	| `dcterms:hasVersion` | `properties.mapping-version` | string literal |
131	| `prov:actedOnBehalfOf` | fixed | `<http://www.deutsche-digitale-bibliothek.de>` |
132	
133	#### 2.2.5 DDB (`<http://www.deutsche-digitale-bibliothek.de>`)
134	
135	| Triple | JSON path | Value type |
136	|---|---|---|
137	| `rdf:type` | — | `prov:Agent`, `foaf:Organization` |
138	| `foaf:name` | fixed | `"Deutsche Digitale Bibliothek"` |
139	
140	#### 2.2.6 Provider (`urn:ddbedm:provider-info:provider-ddb-id:<value>`)
141	
142	| Triple | JSON path | Value type |
143	|---|---|---|
144	| `rdf:type` | — | `prov:Agent`, `foaf:Organization` |
145	| `foaf:name` | `provider-info.provider-name` | string literal |
146	| `schema:url` | `provider-info.provider-uri` | URI |
147	| `dcterms:identifier` | `provider-info.provider-id` | string literal |
148	| `mocho:isil` | `provider-info.provider-isil` | URI |
149	
150	#### 2.2.7 Source record (`ddb-api:items/<id>/source/record`)
151	
152	URI constructed from `source.description.href` by stripping the leading `/` and
153	prepending `ddb-api: <https://api.deutsche-digitale-bibliothek.de/2/>`.
154	
155	One block of triples per `binaries.binary[i]` entry:
156	
157	| Triple | JSON path | Value type |
158	|---|---|---|
159	| `rdf:type` | — | `prov:Entity` |
160	| `dc:identifier` | `binaries.binary[i].ref` | string literal |
161	| `dc:title` | `binaries.binary[i].name` | `@de` literal |
162	| `dc:description` | concat(`name2 \| name`) | `@de` literal (nulls → `""`) |
163	| `dcterms:rights` | `binaries.binary[i].kind` | URI |
164	| `dcterms:source` | `binaries.binary[i].local_pathname` | URI |
165	
166	### 2.3 Full Turtle example
167	
168	```turtle
169	@prefix prov:     <http://www.w3.org/ns/prov#> .
170	@prefix ddb:      <http://www.deutsche-digitale-bibliothek.de/> .
171	@prefix ddb-api:  <https://api.deutsche-digitale-bibliothek.de/2/> .
172	@prefix dcat:     <http://www.w3.org/ns/dcat#> .
173	@prefix dc:       <http://purl.org/dc/elements/1.1/> .
174	@prefix dcterms:  <http://purl.org/dc/terms/> .
175	@prefix foaf:     <http://xmlns.com/foaf/0.1/> .
176	@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .
177	@prefix schema:   <https://schema.org/> .
178	@prefix lov:      <http://www.w3.org/ns/iana/media-types/> .
179	
180	# ── CHO ───────────────────────────────────────────────────────────────────────
181	
182	ddb:item/222NZKK63TNRLC2VETRV722VKBDSUVGL
183	    a prov:Entity ;
184	    prov:wasDerivedFrom
185	        <urn:ddbedm:properties:dataset-id:76409877634279609sQOu> ;
186	    prov:wasAttributedTo
187	        <urn:ddbedm:properties:mapping-version:6.18> ;
188	    prov:generatedAtTime "2026-01-07T15:40:43+0100" ;
189	    dcterms:hasVersion   "43" ;
190	    dcterms:references   "ddb:222NZKK63TNRLC2VETRV722VKBDSUVGL" .
191	
192	# ── Dataset ───────────────────────────────────────────────────────────────────
193	
194	<urn:ddbedm:properties:dataset-id:76409877634279609sQOu>
195	    a dcat:Dataset, prov:Entity ;
196	    dcterms:identifier "76409877634279609sQOu" ;
197	    rdfs:label         "Gesamtlieferung: Deutsche Fotothek - LIDO"@de ;
198	    dcterms:type       <http://www.lido-schema.org/> ;
199	    prov:wasAttributedTo
200	        <urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .
201	
202	# ── XSLT SoftwareAgent ────────────────────────────────────────────────────────
203	
204	<urn:ddbedm:properties:mapping-version:6.18>
205	    a prov:SoftwareAgent ;
206	    dcterms:hasVersion "6.18" ;
207	    prov:actedOnBehalfOf <http://www.deutsche-digitale-bibliothek.de> .
208	
209	# ── DDB Agent ─────────────────────────────────────────────────────────────────
210	
211	<http://www.deutsche-digitale-bibliothek.de>
212	    a prov:Agent, foaf:Organization ;
213	    foaf:name "Deutsche Digitale Bibliothek" .
214	
215	# ── Provider Agent ────────────────────────────────────────────────────────────
216	
217	<urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
218	    a prov:Agent, foaf:Organization ;
219	    foaf:name          "Deutsche Fotothek" ;
220	    schema:url         <http://www.deutschefotothek.de> ;
221	    dcterms:identifier "99900890" ;
222	    mocho:isil         <http://ld.zdb-services.de/resource/organisations/DE-2396> .
223	
224	# ── Source record ─────────────────────────────────────────────────────────────
225	
226	ddb-api:items/222NZKK63TNRLC2VETRV722VKBDSUVGL/source/record
227	    a prov:Entity ;
228	    dc:identifier  "0ac6ad6e-a985-4251-91ca-f4b918326ead" ;
229	    dc:title       "Abb. Vorsatz. Titelblatt auf fliegendem Blatt..."@de ;
230	    dc:description "Urheber*in: DDZ (Fotografische Aufnahme) | Abb. Vorsatz. Titelblatt..."@de ;
231	    dcterms:rights <http://rightsstatements.org/vocab/InC/1.0/> ;
232	    dcterms:source <http://fotothek.slub-dresden.de/fotos/df_pos-2018-a_0000067_000_f.jpg> .
233	```
234	
235	### 2.4 Skipped fields
236	
237	| JSON path | Reason |
238	|---|---|
239	| `properties.cortex-type` | Not modelled in PROV-O graph |
240	| `properties.automatically-translated` | Not modelled in PROV-O graph |
241	| `provider-info.provider-parent-id` | Not modelled in PROV-O graph |
242	| `provider-info.provider-logo` | Not modelled in PROV-O graph |
243	
244	---
245	
246	## 3. Layer 2 — Graph-level pipeline provenance
247	
248	### 3.1 Design
249	
250	Layer 2 uses the **full Activity pattern** (slide 12): each named graph in the
251	triplestore is a `prov:Entity`; each script run that produced it is a
252	`prov:Activity`; the script binary is a `prov:SoftwareAgent`.
253	
254	All Layer 2 triples are stored in a single meta-graph:
255	`<urn:goethe-faust:graph/prov>`.
256	
257	URI patterns:
258	
259	| Resource | URI pattern |
260	|---|---|
261	| Named graph | `urn:goethe-faust:graph/<name>` |
262	| Script run (Activity) | `urn:goethe-faust:run/<script-stem>/<ISO8601-timestamp>` |
263	| Script agent | `urn:goethe-faust:agent/<script-stem>` |
264	| LLM agent | `urn:goethe-faust:agent/<model-id>` |
265	
266	The `gf:inferenceMethod` property flags the epistemic status of graph contents:
267	
268	| Value | Meaning |
269	|---|---|
270	| `gf:Deterministic` | Pure rule-based transform; output is fully reproducible |
271	| `gf:Heuristic` | Rule-based with uncertain matches (e.g. title-string GND lookup) |
272	| `gf:NER` | Triples derived from NER model output |
273	| `gf:LLMGenerated` | Triples produced or ranked by an LLM |
274	
275	### 3.2 Named graphs catalogue
276	
277	| Named graph | Producing script | Inference method |
278	|---|---|---|
279	| `urn:goethe-faust:graph/transform` | `transform_edm_to_mocho.py` | `gf:Deterministic` |
280	| `urn:goethe-faust:graph/gnd-agents` | `link_gnd_agents.py` | `gf:Heuristic` |
281	| `urn:goethe-faust:graph/gnd-works` | `link_gnd_works.py` | `gf:Heuristic` |
282	| `urn:goethe-faust:graph/ner` | NER script (TBD) | `gf:NER` |
283	| `urn:goethe-faust:graph/llm` | LLM enrichment script (TBD) | `gf:LLMGenerated` |
284	| `urn:goethe-faust:graph/prov` | all scripts (self-referential) | `gf:Deterministic` |
285	
286	### 3.3 Triple mapping
287	
288	Each script run writes the following triples into `<urn:goethe-faust:graph/prov>`.
289	
290	#### 3.3.1 Named graph node (`urn:goethe-faust:graph/<name>`)
291	
292	| Triple | Source | Value type |
293	|---|---|---|
294	| `rdf:type` | — | `prov:Entity` |
295	| `prov:wasGeneratedBy` | runtime | run IRI |
296	| `gf:inferenceMethod` | script config | `gf:` vocab term |
297	
298	#### 3.3.2 Run node (`urn:goethe-faust:run/<script-stem>/<timestamp>`)
299	
300	| Triple | Source | Value type |
301	|---|---|---|
302	| `rdf:type` | — | `prov:Activity` |
303	| `prov:startedAtTime` | runtime | xsd:dateTime |
304	| `prov:endedAtTime` | runtime | xsd:dateTime |
305	| `prov:wasAssociatedWith` | script config | script agent IRI |
306	| `prov:used` | script config | input graph IRI(s) |
307	| `rdfs:comment` | optional | free-text note |
308	
309	#### 3.3.3 Script agent (`urn:goethe-faust:agent/<script-stem>`)
310	
311	| Triple | Source | Value type |
312	|---|---|---|
313	| `rdf:type` | — | `prov:SoftwareAgent` |
314	| `rdfs:label` | script header | filename string |
315	| `dcterms:hasVersion` | script header or git tag | string literal |
316	
317	For LLM agents, add:
318	
319	| Triple | Source | Value type |
320	|---|---|---|
321	| `rdf:type` | — | `prov:SoftwareAgent` |
322	| `rdfs:label` | config | model name string |
323	| `dcterms:hasVersion` | config | model version / API version |
324	| `gf:modelProvider` | config | string literal (e.g. `"Anthropic"`) |
325	
326	### 3.4 Turtle example
327	
328	One run of `transform_edm_to_mocho.py` and one run of `link_gnd_agents.py`,
329	stored in the prov graph.
330	
331	```turtle
332	@prefix prov:    <http://www.w3.org/ns/prov#> .
333	@prefix gf:      <urn:goethe-faust:vocab/> .
334	@prefix dcterms: <http://purl.org/dc/terms/> .
335	@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
336	@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
337	
338	# ── Named graph entities ──────────────────────────────────────────────────────
339	
340	<urn:goethe-faust:graph/transform>
341	    a prov:Entity ;
342	    prov:wasGeneratedBy <urn:goethe-faust:run/transform_edm_to_mocho/2026-05-03T09:14:22Z> ;
343	    gf:inferenceMethod  gf:Deterministic .
344	
345	<urn:goethe-faust:graph/gnd-agents>
346	    a prov:Entity ;
347	    prov:wasGeneratedBy <urn:goethe-faust:run/link_gnd_agents/2026-05-03T10:02:47Z> ;
348	    gf:inferenceMethod  gf:Heuristic .
349	
350	# ── Run: transform ────────────────────────────────────────────────────────────
351	
352	<urn:goethe-faust:run/transform_edm_to_mocho/2026-05-03T09:14:22Z>
353	    a prov:Activity ;
354	    prov:startedAtTime    "2026-05-03T09:14:22Z"^^xsd:dateTime ;
355	    prov:endedAtTime      "2026-05-03T09:31:05Z"^^xsd:dateTime ;
356	    prov:wasAssociatedWith <urn:goethe-faust:agent/transform_edm_to_mocho> ;
357	    prov:used             <urn:goethe-faust:graph/raw-json> .
358	
359	<urn:goethe-faust:agent/transform_edm_to_mocho>
360	    a prov:SoftwareAgent ;
361	    rdfs:label         "transform_edm_to_mocho.py" ;
362	    dcterms:hasVersion "0.9.1" .
363	
364	# ── Run: GND agent linking ────────────────────────────────────────────────────
365	
366	<urn:goethe-faust:run/link_gnd_agents/2026-05-03T10:02:47Z>
367	    a prov:Activity ;
368	    prov:startedAtTime    "2026-05-03T10:02:47Z"^^xsd:dateTime ;
369	    prov:endedAtTime      "2026-05-03T10:44:19Z"^^xsd:dateTime ;
370	    prov:wasAssociatedWith <urn:goethe-faust:agent/link_gnd_agents> ;
371	    prov:used             <urn:goethe-faust:graph/transform> ;
372	    rdfs:comment          "lobid-gnd API; confidence threshold 0.85" .
373	
374	<urn:goethe-faust:agent/link_gnd_agents>
375	    a prov:SoftwareAgent ;
376	    rdfs:label         "link_gnd_agents.py" ;
377	    dcterms:hasVersion "0.3.0" .
378	
379	# ── Example: LLM enrichment run (when applicable) ────────────────────────────
380	
381	<urn:goethe-faust:graph/llm>
382	    a prov:Entity ;
383	    prov:wasGeneratedBy <urn:goethe-faust:run/llm_enrich/2026-05-03T11:00:00Z> ;
384	    gf:inferenceMethod  gf:LLMGenerated .
385	
386	<urn:goethe-faust:run/llm_enrich/2026-05-03T11:00:00Z>
387	    a prov:Activity ;
388	    prov:startedAtTime    "2026-05-03T11:00:00Z"^^xsd:dateTime ;
389	    prov:endedAtTime      "2026-05-03T11:28:33Z"^^xsd:dateTime ;
390	    prov:wasAssociatedWith <urn:goethe-faust:agent/claude-sonnet-4-6> ;
391	    prov:used             <urn:goethe-faust:graph/transform> .
392	
393	<urn:goethe-faust:agent/claude-sonnet-4-6>
394	    a prov:SoftwareAgent ;
395	    rdfs:label         "claude-sonnet-4-6" ;
396	    dcterms:hasVersion "claude-sonnet-4-6" ;
397	    gf:modelProvider   "Anthropic" .
398	```
399	
400	---
401	
402	## 4. Prefix declarations
403	
404	| Prefix | URI |
405	|---|---|
406	| `prov:` | `http://www.w3.org/ns/prov#` |
407	| `gf:` | `urn:goethe-faust:vocab/` |
408	| `ddb:` | `http://www.deutsche-digitale-bibliothek.de/` |
409	| `ddb-api:` | `https://api.deutsche-digitale-bibliothek.de/2/` |
410	| `dcat:` | `http://www.w3.org/ns/dcat#` |
411	| `dc:` | `http://purl.org/dc/elements/1.1/` |
412	| `dcterms:` | `http://purl.org/dc/terms/` |
413	| `foaf:` | `http://xmlns.com/foaf/0.1/` |
414	| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` |
415	| `schema:` | `https://schema.org/` |
416	| `mocho:` | `https://ise-fizkarlsruhe.github.io/ddbkg/mocho#` |
417	| `xsd:` | `http://www.w3.org/2001/XMLSchema#` |
418	
```

---

### Assistant *(2026-05-13T12:35:55.330Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "offset": 1,
  "limit": 60
}
```

---

### User *(2026-05-13T12:35:55.341Z)*

**Tool result**
```
1	# ADR: transform_edm_to_mocho.py — Implementation Decisions
2	
3	**Date**: 2026-04-14  
4	**Status**: Accepted  
5	**Related**: `transform-adr.md` (D0 — design), `transform-props-mapping-adr.md` (property decisions — D6/D7/D8 moved there), `mocho/notes/alignment-ddbedm-mocho-adr.md`
6	
7	---
8	
9	## Context
10	
11	This document records implementation decisions for `transform_edm_to_mocho.py`,
12	the reference DDB-EDM JSONL → mocho RDF transform. Dispatch architecture and
13	signal priority are decided in `transform-adr.md` (D0); the decisions here
14	govern how those design choices are realised in code.
15	
16	---
17	
18	## Decision 1: Use JSONL as input, not the NT file
19	
20	**Decision**: Stream `items-all-goethe-faust.json` (JSONL, one JSON object per
21	line). The NT file `ddbedm-goethe-faust.nt` is not used.
22	
23	**Alternatives considered**:
24	- *NT file*: Load triples from the pre-generated NT and align by predicate IRI.
25	  Rejected because: (a) the NT was generated from the same JSONL and carries no
26	  additional information; (b) the alignment table is keyed by `(entity_type,
27	  json_key)` matching the JSON structure, not by IRI, so NT input would require
28	  a reverse IRI→json_key lookup that is neither defined nor stable.
29	
30	**Rationale**: JSONL streams with constant memory, preserves the `(entity_type,
31	json_key)` lookup key structure, and requires only stdlib `json`. No NT indexing
32	phase needed.
33	
34	---
35	
36	## Decision 2: stdlib only — no rdflib in the transform script
37	
38	**Decision**: The transform script uses only Python stdlib (`json`, `csv`, `re`,
39	`collections`, `argparse`, `pathlib`). rdflib is not imported.
40	
41	**Rationale**: The transform is a data pipeline step, not an ontology processing
42	step. N-Triples output can be constructed by string formatting. rdflib adds a
43	non-stdlib dependency and significant startup overhead for a script that runs
44	over 115k records.
45	
46	**Scope**: This applies only to `transform_edm_to_mocho.py`. Upstream scripts
47	that parse OWL or Turtle (`align_ddbedm_to_mocho.py`, `gen_htype_doco_mapping.py`)
48	continue to use rdflib.
49	
50	---
51	
52	## Decision 3: Dispatch signal field paths and htype lookup key
53	
54	**Decision**: The four dispatch signals are read from the following JSONL paths:
55	
56	| Signal | JSONL path | Value example | Notes |
57	|---|---|---|---|
58	| sector | `provider-info.domains[0]` | `http://ddb.vocnet.org/sparte/sparte001` | Vocnet sparte IRI; `domains[0]` is always the primary sector |
59	| mediatype | `edm.RDF.WebResource[0].type.resource` | `http://ddb.vocnet.org/medientyp/mt002` | Vocnet medientyp IRI; taken from first WebResource |
60	| htype | `edm.RDF.ProvidedCHO.hierarchyType` | `"htype_030"` | Literal `htype_code` string; absent if record has no hierarchy type |
```

---

### Assistant *(2026-05-13T12:36:18.041Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep \"^## Decision\" /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md | tail -5",
  "description": "Find last decision number in transform-script-adr.md"
}
```

---

### User *(2026-05-13T12:36:18.092Z)*

**Tool result**
```
## Decision 25: LIDO contributor predicate dispatch
## Decision 26: Work-level GND Werk staging output
## Decision 27: Bare-ID URI minting for malformed `about` values
## Decision 28: Post-processing NQ split → per-graph NT files
## Decision 14: Manual curation over automated schema alignment
```

---

### Assistant *(2026-05-13T12:36:41.415Z)*

I have a complete picture now. Here's the plan — no implementation until you say so.

---

## Plan: deduplicate shared PROV-O node triples

### What's redundant

Four nodes in `emit_prov_triples` have stable URIs that recur across records. Their descriptive triples are re-emitted identically for every record:

| Node | URI | # triples duplicated | Scope |
|---|---|---|---|
| DDB Agent | `DDB_BASE` (fixed) | 3 | entire run |
| XSLT SoftwareAgent | `urn:…:mapping-version:<ver>` | 3 | all records with same `mapping-version` |
| Dataset | `urn:…:dataset-id:<id>` | 3–5 | all records in same dataset |
| Provider Agent | `urn:…:provider-ddb-id:<id>` | 4–5 | all records from same provider |

The per-CHO linking triples (`prov:wasAttributedTo`, `prov:wasDerivedFrom`, etc.) are unique per record and must NOT be deduplicated.

---

### DuckDB — not needed

The run is a single-process, single-pass stream. An in-memory `set[str]` of already-emitted URIs is sufficient — O(1) lookup, zero dependencies. DuckDB would only be needed for cross-worker or cross-run deduplication, neither of which applies here. The existing DuckDB in `__main__.py` is write-only werk_staging and is unrelated.

---

### Code changes (3 files)

**`emitters.py`** — `emit_prov_triples` gets a new optional `emitted: set[str] | None = None` parameter. Each of the four shared-node blocks is wrapped:

```python
if emitted is not None and uri in emitted:
    pass  # skip descriptive triples; linking triples from CHO already emitted above
else:
    if emitted is not None:
        emitted.add(uri)
    # ... descriptive triple lines ...
```

**`transform.py`** — `transform_record` gets `emitted_prov: set[str] | None = None`, passes it through to `emit_prov_triples(record, ddb_uri, GRAPH_PROV, emitted=emitted_prov)`.

**`__main__.py`** — one line before the record loop: `emitted_prov: set[str] = set()`. Passed into every `transform_record(...)` call.

---

### Notes changes (2 files)

**`ddbedm-prov-o-plan.md` §2.1** — add a "Shared node deduplication" note after the five-node table: shared nodes (DDB Agent, XSLT, Dataset, Provider) emit descriptive triples only on first encounter per run; the CHO linking triples are always emitted.

**`transform-script-adr.md`** — add **Decision 29**: in-memory `set` for shared PROV-O node deduplication. Document: (a) which four nodes are guarded, (b) why not DuckDB (single-pass, single-process), (c) `emitted` is `None`-safe so callers that don't pass it get the current re-emit behavior.

---

Ready to implement?

---

### User *(2026-05-13T12:37:19.682Z)*

duckdb is needed, because i will be running this script repeatedly on different inputs

---

### Assistant *(2026-05-13T12:37:55.682Z)*

Good correction. Since you run the transform on separate sector files (s1, s2, … s7) that get merged, the DDB Agent and XSLT agent triples would otherwise appear in every sector's output. The deduplication needs to survive across runs.

Updated plan:

---

## Plan (revised): DuckDB-backed cross-run PROV-O deduplication

### Mechanism

A shared, persistent DuckDB file (separate from the per-run `werk-staging.duckdb`) stores a single table of already-emitted shared-node URIs. Each run:
1. opens the file and loads existing URIs into memory as `set[str]` (the number of unique providers/datasets/XSLT versions is small — tens to hundreds)
2. uses that set during processing to suppress redundant descriptive triples
3. writes newly-emitted URIs back to DuckDB at the end of the run via `INSERT OR IGNORE`

### Schema (one table, fixed path)
```sql
CREATE TABLE IF NOT EXISTS emitted_prov_uris (uri VARCHAR PRIMARY KEY)
```

### Code changes (3 files)

**`emitters.py`** — same as before: `emit_prov_triples` gets `emitted: set[str] | None = None`; each of the four shared-node blocks is guarded by `if emitted is None or uri not in emitted`; new URIs are `emitted.add(uri)` on first emit. `None` falls back to re-emit every time (safe default).

**`transform.py`** — `transform_record` gets `emitted_prov: set[str] | None = None`, threads it into `emit_prov_triples`.

**`__main__.py`** — three additions:
- New CLI arg: `--prov-db PATH` — path to the shared dedup DuckDB; optional; if omitted, fresh in-memory set is used (within-run dedup only, no persistence)
- At startup (after the existing DuckDB `conn` setup): open `--prov-db`, create table if absent, load all rows into `emitted_prov: set[str]`
- After the record loop closes (before `conn.close()`): `INSERT OR IGNORE INTO emitted_prov_uris` for all URIs in `emitted_prov`

### Notes changes (2 files)

**`ddbedm-prov-o-plan.md` §2.1** — add "Shared node deduplication" paragraph after the five-node table.

**`transform-script-adr.md`** — add **Decision 29**: DuckDB-backed cross-run dedup for shared PROV-O nodes. Document: which four nodes are guarded, why DuckDB (multi-run, separate sector files), why load-into-memory rather than per-record DB lookup (provider/dataset count is small; avoids DB round-trip per record), `None`-safe fallback.

---

Proceed?

---

### User *(2026-05-13T13:45:57.334Z)*

CREATE TABLE IF NOT EXISTS emitted_prov_uris (uri VARCHAR PRIMARY KEY)

There be a lookup: xslt version number is the key.

this duckdb should also be used for other entities:
1. edm:Agent
2. edm:Place

---

### User *(2026-05-13T13:45:59.046Z)*

[Request interrupted by user]

---

### User *(2026-05-13T13:46:20.200Z)*

CREATE TABLE IF NOT EXISTS emitted_prov_uris (uri VARCHAR PRIMARY KEY)

There be a lookup: xslt version number is the key.

this duckdb should also be used for other entities:
1. edm:Agent
2. edm:Place
3. skos:Concept (from db:Subject, dcterms:Subject).

What else?

---

### Assistant *(2026-05-13T13:47:06.781Z)*

Good extension. Let me think through the complete set of shared entities worth deduplicating, then flag the XSLT key question.

**Entities you listed + what else fits the same pattern** (stable URI, descriptive triples, high repetition across records):

| Entity | Source in JSON | Repetition driver |
|---|---|---|
| PROV: XSLT SoftwareAgent | `properties.mapping-version` | same version across entire sector file |
| PROV: DDB Agent | fixed | appears in every record |
| PROV: Provider Agent | `provider-info.provider-ddb-id` | all records from same institution |
| PROV: Dataset | `properties.dataset-id` | all records in same delivery batch |
| `edm:Agent` | `edm.RDF.Agent[].about` | GND agent URIs shared across many records |
| `edm:Place` | `edm.RDF.Place[].about` | GND place URIs shared across many records |
| `skos:Concept` | subjects via `dc:subject`, `dcterms:subject` | shared vocabulary terms |
| **`edm:TimeSpan`** | `edm.RDF.TimeSpan[].about` | century/period URIs repeat heavily |
| **rights/license URIs** | `edm:rights`, `dcterms:rights` | very few distinct values (~10–20) across all 115k records |

**On the XSLT key:** the version string (`"6.18"`) is the natural lookup key since the URI is fully derived from it (`urn:ddbedm:properties:mapping-version:6.18`). This argues for a separate `emitted_xslt` table with `version VARCHAR PRIMARY KEY` rather than folding it into a generic URI table — or at minimum noting that the lookup is by version, not URI, for that one case.

**What else?** The only remaining candidates I see:

- **`edm:WebResource`** — thumbnail and source URLs. These are mostly record-unique, so low dedup value. Probably not worth it.
- **`edm:PhysicalThing`** — same, mostly unique per record.
- **`htype` IRIs** (`edm:hasType`) — small fixed set (~30 values), could be deduplicated, but the triples are minimal (just a type assertion), so the gain is marginal.

So the meaningful set is: 4 PROV-O shared nodes + `edm:Agent`, `edm:Place`, `skos:Concept`, `edm:TimeSpan`, rights URIs.

**Table design question for you:** one table with a `entity_type` column, or one table per type? One table is simpler to manage; separate tables allow per-type statistics and cleaner schema. Which do you prefer before I update the plan?

---

### User *(2026-05-13T13:48:21.372Z)*

one table is better

---

### Assistant *(2026-05-13T13:48:56.189Z)*

Final plan before implementation:

---

## Plan (final): shared-entity deduplication via DuckDB

### Schema — one table, shared DuckDB file

```sql
CREATE TABLE IF NOT EXISTS emitted_entities (
    uri         VARCHAR PRIMARY KEY,
    entity_type VARCHAR NOT NULL
)
```

`entity_type` values: `prov_xslt`, `prov_ddb`, `prov_provider`, `prov_dataset`, `edm_agent`, `edm_place`, `skos_concept`, `edm_timespan`, `rights`

**XSLT note**: the lookup key in code is `xslt_uri` derived from `map_ver` (`urn:ddbedm:properties:mapping-version:{ver}`). The version number is what's in the JSON; the URI is computed from it — so "version number is the key" holds at the code level; the table stores the derived URI as with all other entries.

### Runtime pattern per run

- Load all existing `uri` values into a `dict[str, str]` (`uri → entity_type`) at startup — doubles as O(1) lookup and write-back source
- Pass this dict into every `transform_record()` call
- At end: `INSERT OR IGNORE INTO emitted_entities SELECT * FROM VALUES (?, ?)` for all entries in the dict — idempotent, handles pre-existing entries safely

---

### Code changes (3 files)

**`emitters.py`**
- `emit_prov_triples(record, ddb_cho_uri, graph_iri, emitted=None)` — guard XSLT, DDB Agent, Provider Agent, Dataset blocks: skip descriptive triples if URI already in `emitted`; add `(uri, entity_type)` on first emit
- `emit_ddbedm_triples(rdf, graph_iri, lang_coll=None, emitted=None)` — guard descriptive triple blocks for `edm:Agent`, `edm:Place`, `skos:Concept`, `edm:TimeSpan`, and rights URIs similarly

**`transform.py`**
- `transform_record(..., emitted_entities=None)` — pass through to both emitters

**`__main__.py`**
- New CLI arg: `--entities-db PATH` (optional; if omitted, fresh in-memory dict, within-run dedup only)
- Startup: open DuckDB at `--entities-db`, `CREATE TABLE IF NOT EXISTS`, load rows into `emitted_entities: dict[str, str]`
- Record loop: pass `emitted_entities` to every `transform_record()`
- After loop: batch `INSERT OR IGNORE` all entries back to DuckDB; close connection

---

### Notes changes (2 files)

**`ddbedm-prov-o-plan.md` §2.1** — add "Shared node deduplication" note after the five-node table covering: which nodes are guarded, that dedup is cross-run via DuckDB, XSLT key derivation

**`transform-script-adr.md` — Decision 29**: DuckDB-backed shared-entity dedup. Cover: which 9 entity types, one-table design rationale, `dict[str, str]` as both lookup and write-back, `--entities-db` optional flag, `None`-safe fallback

---

Proceed?

---

### User *(2026-05-13T13:56:08.267Z)*

also update /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md

---

### Assistant *(2026-05-13T13:56:14.445Z)*

Let me read `transform-implementation-actual.md` before starting.

---

### Assistant *(2026-05-13T13:56:14.739Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md"
}
```

---

### User *(2026-05-13T13:56:15.370Z)*

**Tool result**
```
1	# Transform implementation — as-built
2	
3	**Date**: 2026-05-06
4	**Status**: Implemented and verified on full goethe-faust corpus (115,432 records)
5	**Package**: `scripts/transform/` (invoked as `python -m transform` from `scripts/`)
6	
7	Reference for the original design intent: `notes/transform-implementation-plan.md`.
8	Validation findings: `notes/transform-validation.md`.
9	Full-corpus run planning: `notes/transform-dryrun-plan.md`.
10	
11	---
12	
13	## 1. Package structure
14	
15	The original plan targeted a monolithic rewrite of `scripts/transform_edm_to_mocho.py`. The actual implementation refactored into a Python package:
16	
17	| Module | Contents |
18	|---|---|
19	| `constants.py` | IRIs, prefix table (`_PREFIXES`), dispatch tables, path defaults, type aliases |
20	| `utils.py` | N-Quads formatting, URI minting, IRI sanitisation, value normalisation |
21	| `loaders.py` | CSV/JSON config loaders |
22	| `emitters.py` | Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, werk_staging |
23	| `transform.py` | `transform_record` — per-record orchestration |
24	| `__main__.py` | CLI entry point |
25	
26	---
27	
28	## 2. Deviations from the plan
29	
30	### 2.1 No in-process multiprocessing
31	
32	The plan (§8) included `--workers N` and `--batch-size N` for a `ProcessPoolExecutor` approach. This was dropped in favour of **Option C parallel** (`transform-dryrun-plan.md §5.2`): export per-sector JSONL files from SQLite once, then run one `python -m transform` worker per sector as separate OS processes. No code changes required in the transform itself.
33	
34	Rationale: per-UID SQLite random lookups are slower than sequential JSONL reads at 18.5M scale; sector split is the natural parallelism boundary; transform output is already sharded by sector. See `transform-dryrun-plan.md §5` for the full trade-off table.
35	
36	### 2.2 CLI flags — additions and removals
37	
38	**Planned but not implemented:**
39	- `--workers N`, `--batch-size N` — dropped (Option C)
40	- `--out` — output is always `<outdir>/goethe-faust.nq`; no free-choice path flag
41	- `--werk-staging` — DuckDB path is always `<outdir>/goethe-faust-werk-staging.duckdb`
42	
43	**Added (not in plan):**
44	- `--total N` — expected total records; enables ETA in progress log
45	- `--log-interval N` — log a progress line every N records (default: 100,000)
46	- SIGINT/SIGTERM signal handler — graceful exit after current record; partial stats and errors written
47	
48	**Output directory:** auto-timestamped `output/transform/YYYYMMDD_HHMMSS/` rather than fixed paths. Override with `--outdir`.
49	
50	### 2.3 Stats expansion
51	
52	The plan's `--stats` levels were implemented as designed. Additionally, during development the following were added at `dispatch` level (all from emitter Counters — no post-hoc N-Quad scanning):
53	
54	- `records.by_mediatype` — mediatype distribution (short codes: `mt001`–`mt007`)
55	- `records.by_htype` — htype distribution (short codes: `ht021`, etc.)
56	- `records.uri_sanitized` — IRIs percent-encoded due to illegal characters (RFC 3987)
57	- `records.uri_split` — individual URIs extracted from multi-URI `resource` fields
58	- `records.uri_about_split` — extra `owl:sameAs` triples for multi-URI `about` fields
59	- `ddbedm_classes` — entity class instance counts in the ddbedm graph
60	- `ddbedm_vocab.properties_all` — predicate counts for the ddbedm stream
61	- `mocho_vocab.properties_all` / `properties_new` — predicate counts for the mocho stream
62	
63	`full` level now aliases `dispatch` (reserved for future additions; the former regex-based predicate extraction was removed).
64	
65	Schema and field rationale: `notes/transform-stats-plan.md`.
66	
67	### 2.4 URI sanitisation and multi-URI data quality fixes
68	
69	Not in the original plan. Added to `utils.py`:
70	
71	**`_sanitize_iri(iri)`** — percent-encodes characters illegal in N-Triples IRI references (`[\x00-\x20<>"{}|\\^\x7f]`). Ported from `gemea/scripts/py/export_ddb.py`. Applied inside `value_to_nt_obj` for every `{"resource": ...}` value.
72	
73	**Multi-URI `resource` fields** — 1,250 fields in the goethe-faust corpus contain multiple space-separated URIs in a single `resource` value (e.g. `"http://www.geonames.org/2856883 http://vocab.getty.edu/tgn/7005252"`). `value_to_nt_obj` splits on whitespace and emits each URI as a separate triple.
74	
75	**Multi-URI `about` fields** — 1,178 entities (`Place`, `WebResource`, `Agent`) have multiple space-separated URIs in `about`. `emit_ddbedm_triples` uses the first URI as the RDF subject and emits `owl:sameAs` for each additional URI (+1,309 triples in the goethe-faust corpus).
76	
77	---
78	
79	## 3. Actual CLI
80	
81	Run from `scripts/` directory:
82	
83	```bash
84	python -m transform [OPTIONS]
85	```
86	
87	### I/O
88	
89	| Flag | Default | Description |
90	|---|---|---|
91	| `--jsonl FILE` | `data/items-all-goethe-faust.json` | JSONL input (one DDB-EDM JSON object per line) |
92	| `--ids FILE\|-` | _(none)_ | ID allowlist file, or `-` for stdin; omit to process all |
93	| `--outdir DIR` | `output/transform/YYYYMMDD_HHMMSS` | Output directory; auto-timestamped if omitted |
94	
95	### Config
96	
97	| Flag | Default |
98	|---|---|
99	| `--alignment FILE` | `output/config/lookup_class_prop_alignment.csv` |
100	| `--lido FILE` | `output/config/lido_event_types.csv` |
101	| `--htype FILE` | `output/config/lookup_htype_doco_rico.csv` |
102	| `--mediatype FILE` | `output/config/lookup_mediatype_class.csv` |
103	| `--audio FILE` | `output/config/audio_type2class.json` |
104	
105	### Run control
106	
107	| Flag | Default | Description |
108	|---|---|---|
109	| `--stats none\|basic\|dispatch\|full` | `basic` | Stats verbosity in `transform_stats.json` |
110	| `--log-level DEBUG\|INFO\|WARNING\|ERROR` | `INFO` | Log verbosity |
111	| `--limit N` | _(none)_ | Stop after N records (smoke-testing) |
112	| `--total N` | _(none)_ | Expected total records — enables ETA in progress log |
113	| `--log-interval N` | `100000` | Progress log line every N records |
114	| `--debug` | — | Shorthand for `--log-level DEBUG` |
115	
116	---
117	
118	## 4. Output files
119	
120	Each invocation derives the output filename stem from the input: for SQLite input `s2.sqlite` with `--offset N` the stem is `s2-N`; for JSONL input `foo.json` the stem is `foo`. Override with `--stem`.
121	
122	Single-worker output:
123	```
124	<outdir>/
125	  <stem>.nq                   N-Quads, all named graphs
126	  <stem>-werk-staging.duckdb  W-slot staging rows
127	  <stem>-stats.json           run statistics
128	  <stem>-errors.jsonl         per-record errors (written live)
129	  <stem>.log                  run log
130	```
131	
132	In the production parallel-sector run (`run-transform-sector.sh`), all workers for one sector share a single `nq/` shard directory; merged outputs land one level up named by sector:
133	```
134	<version>/
135	  nq/
136	    s2-0.nq  s2-0-stats.json  s2-0.log  ...   ← worker shards (deleted after merge)
137	    s2-38400.nq  ...
138	    ...
139	  s2.nq                    merged N-Quads (--merge-all only)
140	  s2-werk-staging.duckdb   merged werk_staging
141	  s2-stats.json            merged stats
142	  s2-errors.jsonl          merged errors
143	  s2.log                   merged log
144	```
145	
146	Running sectors sequentially into the same `<version>/` dir produces non-colliding `s1-*` and `s2-*` files.
147	
148	Named graphs:
149	
150	| Graph IRI | Content |
151	|---|---|
152	| `https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm` | Verbatim EDM passthrough (always, including mt007) |
153	| `https://gemea.ise.fiz-karlsruhe.de/graph/mocho` | mocho-aligned triples (skipped for mt007) |
154	| `https://gemea.ise.fiz-karlsruhe.de/graph/prov` | PROV-O Layer 1 (always) |
155	| `https://gemea.ise.fiz-karlsruhe.de/graph/lang-title` | `dcterms:language` provenance triples for normalized lang codes (emitted only when a record carries at least one invalid BCP 47 code) |
156	
157	---
158	
159	## 5. POC run — goethe-faust reference corpus (2026-05-06)
160	
161	| Metric | Value |
162	|---|---|
163	| Records processed | 115,432 |
164	| Triples total | 14,713,376 |
165	| ddbedm / mocho / prov | 8,957,262 / 1,898,754 / 3,857,360 |
166	| werk_staging rows | 15 (`rdac:C10001` only) |
167	| Errors (parse + transform) | 0 |
168	| fallback_d9 | 0 |
169	| uri_split | 4,188 |
170	| uri_about_split | 1,309 |
171	| uri_sanitized | 29 |
172	
173	Dispatch sum check: 25,644 (htype) + 47,428 (mediatype) + 0 (fallback) + 42,360 (mt007) = 115,432 ✓
174	
175	---
176	
177	## 6. Open issues from validation
178	
179	From `notes/transform-validation.md`:
180	
181	### 6.1 `mocho:ImageWork` missing from werk_staging
182	
183	`_W_SLOT_CLASSES` triggers on `rdac:C10001` and `mo:MusicalWork` only. `transform-revised-plan.md §1.1` marks `mocho:ImageWork` as a GND-Werk target (ht015 Illustration, ht019 Karte, sparte005 mt002). No `mocho:ImageWork` records in the goethe-faust corpus, so no current impact. **Fix before running on a broader corpus.**
184	
185	### 6.2 `ec:EditorialWork` werk_staging scope
186	
187	Adding `ec:EditorialWork` would produce 88 additional staging rows (mt005 Video). `transform-revised-plan.md §1.1` has no "GND Werk" column entry for mt005/EditorialWork. Video productions do not have GND Werk authority records. Left out intentionally; revisit when GND linking scope is finalised.
188	
189	---
190	
191	## 7. Emitter safety audit (2026-05-07)
192	
193	### 7.1 Issue categories
194	
195	Three systemic gaps (A–C) and one feature addition (D):
196	
197	| # | Category | Root cause / motivation | Emitters affected |
198	|---|---|---|---|
199	| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags; the unescaped tag appears verbatim in the N-Quad literal | Any emitter that calls `_escape_literal` on a field containing `<br …>` |
200	| B | Multi-URI `resource` not split | Emitters that manually extract `val.get("resource")` treat space-separated URIs as one string, producing a malformed IRI | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs` |
201	| C | Bare IDs not expanded in special emitters | Same emitters bypass `expand_obj_nt`; also `emit_prov_triples` passes `provider_isil` without `_sanitize_iri` | `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`, `emit_prov_triples` |
202	| D | `edm:currentLocation` — IRI-with-label-stub | Currently emitted via generic loop (no label stub). Should follow the same "IRI-with-label-stub" pattern as `edm:hasType`: URI values get a `rdfs:label` stub from the matching `edm:Place`; literal values pass through unchanged | New `emit_current_location_triples`; `"currentLocation"` added to `_MOCHO_SKIP` |
203	
204	Note: `value_to_nt_obj` (used by the generic loops in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are exclusively in special-case emitters that extract `resource` manually.
205	
206	Corpus evidence (from `data/items-all-goethe-faust.json`):
207	- **B/D** — `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF`: `ProvidedCHO.currentLocation.resource = "http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745"` and matching `Place.about`
208	- **A** — `223GMAWUHPGI76OQUKSL54XVOCHHXDWD`: description field contains `"...1749, +22. März 1832<br />Eduard Lassen..."` 
209	- **C** — `222NZKK63TNRLC2VETRV722VKBDSUVGL`: `ProvidedCHO.hasType[0].resource = "DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6"` (bare 32-char ID)
210	
211	### 7.2 Design — `resource_uris()` utility
212	
213	Rather than patching each emitter individually, one utility in `utils.py` encapsulates the three sub-steps every manual `resource` extraction must perform:
214	
215	```python
216	def resource_uris(
217	    resource_raw: str,
218	    bare_id_to_uri: dict[str, str] | None = None,
219	    entity_class: str = "Agent",
220	) -> list[str]:
221	    """Expand, sanitize, and split all URIs from a (possibly multi-value) resource string.
222	
223	    Steps: (1) split on whitespace; (2) expand bare IDs via index or mint_bare_id fallback;
224	    (3) percent-encode unsafe characters. Returns [] for empty input.
225	    """
226	```
227	
228	Callers pass `(val.get("resource") or "").strip()`, the per-record `bare_id_to_uri` index, and the entity class for bare-ID minting. Returns a list of safe, full URI strings ready for `f"<{uri}>"` wrapping.
229	
230	**Primary-URI rule**: emitters that need the raw first URI before expansion (e.g. `event_participant_index` lookup in `emit_contributor_triples`, `resolve_agent` in `emit_creator_triples`) extract `resource_raw.split()[0]` before calling `resource_uris()`.
231	
232	### 7.3 Change inventory
233	
234	**`utils.py`**
235	
236	| Change | Detail |
237	|---|---|
238	| Add `_BR_RE` | `re.compile(r'<br\s*/?\s*>', re.IGNORECASE)` |
239	| Update `_escape_literal` | Prepend `s = _BR_RE.sub('\n', s)` before the escape chain |
240	| Add `resource_uris()` | New utility; imported by `emitters.py` |
241	
242	**`emitters.py`**
243	
244	| Emitter | Change |
245	|---|---|
246	| `emit_subject_triples` | Replace single-URI `resource` branch with `resource_uris(resource_raw, _bare, "Concept")` loop |
247	| `emit_hastype_triples` | Same pattern |
248	| `emit_creator_triples` | Add `bare_id_to_uri=None` param; Track 1: `resource_uris()` loop; Track 2: `resource_raw.split()[0]` for `resolve_agent`; apply `_sanitize_iri(agent_uri)` |
249	| `emit_contributor_triples` | Add `bare_id_to_uri=None` param; `resource_raw.split()[0]` for `event_participant_index` lookup; `resource_uris()` loop for triples |
250	| `emit_prov_triples` | Apply `_sanitize_iri(provider_isil)` |
251	| `emit_place_stubs` | Split `raw_about`; pass only first part to `mint_bare_id` with `_sanitize_iri` |
252	| `emit_aggregation_triples` | Inline split+sanitize loop for `isShownAt.resource`, `dataProvider.resource`, `object.resource` (no bare ID expansion — aggregation URIs are always full) |
253	| `emit_mocho_triples` | Pass `bare_id_to_uri` to `emit_creator_triples` and `emit_contributor_triples` |
254	
255	**`emitters.py` — imports**: add `resource_uris` to `from .utils import`.
256	
257	### 7.4 Fixture-based integration tests
258	
259	Three real corpus records are saved to `scripts/transform/tests/fixtures/` as minimal inspection targets. Each record is stored as `<id>.json` (single-record JSON, not JSONL).
260	
261	| File | Record ID | Pattern |
262	|---|---|---|
263	| `fixtures/multi_uri.json` | `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF` | Multi-URI in `Place.about` and `currentLocation.resource` |
264	| `fixtures/br_tag.json` | `223GMAWUHPGI76OQUKSL54XVOCHHXDWD` | `<br />` in description literal |
265	| `fixtures/bare_id.json` | `222NZKK63TNRLC2VETRV722VKBDSUVGL` | Bare 32-char ID in `hasType.resource` |
266	
267	After fixes are applied, a fixture script `tests/make_fixtures.py` runs the full transform on all three records and writes `fixtures/<id>.nq` — the complete N-Quads output for human inspection.
268	
269	Integration tests in `test_transform.py` (new `TestFixtures` class) load each `.json`, call `transform_record()`, and make targeted assertions:
270	
271	| Test | Assertion |
272	|---|---|
273	| `test_multi_uri_place_splits` | Two separate `Place` subject IRIs emitted; no IRI containing a space |
274	| `test_multi_uri_current_location_splits` | Two separate triples for `currentLocation` |
275	| `test_br_tag_normalized` | `\\n` appears in the relevant literal; no `<br` substring in any triple |
276	| `test_bare_id_hastype_expanded` | `urn:ddbedm:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |
277	
278	### 7.5 Unit test additions
279	
280	| Class / function | Covers |
281	|---|---|
282	| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\n` |
283	| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id` (`urn:ddbedm:<id>`) |
284	| `TestEmitSubjectTriplesMultiUri` | `"URI1 URI2"` → two `dcterms:subject` triples |
285	| `TestEmitHastypeTriplesMultiUri` | Same for `edm:hasType` |
286	| `TestEmitCreatorTriplesMultiUri` | Two URIs → two Track-1 triples |
287	| `TestEmitCreatorTriplesBareId` | Bare ID expanded; `agent_uri` sanitized |
288	| `TestEmitContributorTriplesMultiUri` | Two URIs → two `(cho, prop, uri)` triples |
289	| `TestEmitContributorTriplesBareId` | Bare ID expanded via param |
290	| `TestEmitProvTriplesIsil` | `provider_isil` with unsafe chars → sanitized in `MOCHO_ISIL` triple |
291	| `TestEmitPlaceStubsSplitAbout` | Space-separated `about` → only first part used as subject |
292	| `TestEmitAggregationSplitUri` | `isShownAt.resource = "URI1 URI2"` → two `dcterms:source` triples |
293	
294	### 7.6 Validation run — goethe-faust corpus (2026-05-07)
295	
296	Full run on `data/items-all-goethe-faust.json` (115,432 records) after all audit fixes. Output: `output/transform/20260507_190805/`.
297	
298	| Metric | POC (2026-05-06) | Post-audit (2026-05-07) | Delta |
299	|---|---|---|---|
300	| Records processed | 115,432 | 115,432 | — |
301	| Triples total | 14,713,376 | 14,764,352 | +50,976 |
302	| ddbedm | 8,957,262 | 8,957,734 | +472 |
303	| **mocho** | **1,898,754** | **1,950,504** | **+51,750** |
304	| prov | 3,857,360 | 3,856,114 | −1,246 |
305	| Errors | 0 | 0 | — |
306	| fallback_d9 | 0 | 0 | — |
307	| uri_sanitized | 29 | 29 | — |
308	| uri_split | 4,188 | 2,685 | −1,503 |
309	| uri_about_split | 1,309 | 1,309 | — |
310	
311	**mocho +51,750** breaks down as:
312	- `edm:currentLocation` — 31,837 new triples (property moved from generic loop to `emit_current_location_triples`; IRI-with-label-stub pattern)
313	- Creator/contributor bare-ID expansions, multi-URI splits, and subject/hasType label stubs now handled correctly in special emitters account for the remainder
314	
315	**uri_split −1,503**: some multi-URI splits previously counted via the generic loop (`value_to_nt_obj`) are now handled in special emitters via `resource_uris()` and tracked separately; the net split count is lower because `currentLocation` URIs (many multi-value) are no longer double-counted.
316	
317	**prov −1,246**: minor change due to PROV provider node deduplication; no logic change — variance from record ordering in input.
318	
319	---
320	
321	## 8. Agent label stub fixes (2026-05-08)
322	
323	Two bugs in `emitters.py` prevented `rdfs:label` from being emitted on agent stubs in the mocho graph. Both deviate from the spec in `transform-props-mapping-plan.md §4–5` ("Label sourced from `edm:Agent.prefLabel[].$` (first value). Applies to both creator and contributor URI resolutions.").
324	
325	### 8.1 Bug 1 — `emit_creator_triples`: `isinstance(pref, str)` always False
326	
327	Track 2 of `emit_creator_triples` emits `dcterms:creator <agent.about>` + `mocho:Agent` type when `resolve_agent` finds a matching `edm:Agent`. It also should emit `rdfs:label` sourced from `agent.prefLabel[].$`. The pre-fix code:
328	
329	```python
330	pref = agent.get("prefLabel") or label
331	if pref and isinstance(pref, str):          # always False — prefLabel is a list
332	    lines.append(make_nq(agent_nt, RDFS_LABEL, f'"{_escape_literal(pref)}"', graph_iri))
333	```
334	
335	`agent.get("prefLabel")` returns a list (e.g. `[{"$": "Goethe, …", "lang": "de"}]`). `isinstance(list, str)` is always `False`, so no `rdfs:label` was ever emitted from the agent's own prefLabel. When the list was empty, the fallback `or label` set `pref` to the literal string from the creator field — which did pass `isinstance(str)` — but that path is rare and emits without lang-tag.
336	
337	**Fix**: replace with `coerce_list(agent.get("prefLabel"))` + `value_to_nt_obj` iteration (same pattern as `emit_hastype_triples`); fall back to the `label` string only when prefLabel is empty.
338	
339	### 8.2 Bug 2 — `emit_contributor_triples`: no `agents_index`, label from `val.get("$")`
340	
341	`emit_contributor_triples` had no `agents_index` parameter, so:
342	
343	1. **URI case**: `rdfs:label` was sourced from `val.get("$")` — the literal annotation on the contributor field — not from the matching `edm:Agent.prefLabel`.
344	2. **Literal case**: no `resolve_agent` call at all. Contributor literals that matched a DDB/GND agent by label were emitted as plain `dc:contributor "literal"@lang` instead of an agent stub.
345	
346	**Fix**: add `agents_index: dict[str, AgentDict] | None = None` parameter.
347	- **URI case**: `resolve_agent("", primary_resource, _agents)` → use `prefLabel` from agent; fall back to `val.get("$")` if not found.
348	- **Literal case**: `resolve_agent(label, "", _agents)` → if DDB/GND match, emit `<cho> <target_prop> <agent.about>` + `mocho:Agent` + `rdfs:label`; else emit plain literal.
349	
350	Update `emit_mocho_triples` call site to pass `agents_index`.
351	
352	### 8.3 Test additions
353	
354	Eight new tests in `scripts/transform/tests/test_transform.py`:
355	
356	| Class | Test | Covers |
357	|---|---|---|
358	| `TestEmitCreatorTriplesPrefLabel` | `test_preflabel_list_dict_emitted` | prefLabel list-of-dicts → label emitted |
359	| | `test_preflabel_lang_tagged` | lang tag preserved (`"Schiller, Friedrich"@de`) |
360	| | `test_preflabel_empty_list_falls_back_to_label` | empty prefLabel → fallback to literal |
361	| | `test_uri_track2_uses_agents_index_preflabel` | URI path also uses agents_index prefLabel |
362	| `TestEmitContributorTriplesAgentLabel` | `test_uri_case_uses_agents_index_preflabel` | agents_index prefLabel wins over `val["$"]` |
363	| | `test_uri_case_fallback_to_literal_label_when_no_index` | no agents_index → `val["$"]` used |
364	| | `test_literal_match_emits_agent_stub` | literal matching DDB/GND agent → stub emitted |
365	| | `test_literal_no_match_emits_plain_literal` | unmatched literal → plain `dc:contributor` |
366	
367	Total: 114 tests (106 post-audit + 8 new).
368	
369	### 8.4 Validation run — goethe-faust corpus (2026-05-08)
370	
371	Full run on `data/items-all-goethe-faust.json` (115,432 records) after agent label fixes. Output: `output/transform/20260507_232804/`.
372	
373	| Metric | Pre-fix (20260507_190805) | Post-fix (20260507_232804) | Δ |
374	|---|---|---|---|
375	| Records processed | 115,432 | 115,432 | — |
376	| Triples total | 14,764,352 | 14,782,653 | **+18,301** |
377	| ddbedm | 8,957,734 | 8,957,734 | 0 |
378	| **mocho** | **1,950,504** | **1,968,805** | **+18,301** |
379	| prov | 3,856,114 | 3,856,114 | 0 |
380	| `rdfs:label` (mocho) | 302,578 | 320,754 | **+18,176** |
381	| `rdf:type` (mocho) | 162,807 | 162,932 | **+125** |
382	| `dcterms:creator` | 53,453 | 53,453 | 0 |
383	| `dc:contributor` | 36,773 | 36,773 | 0 |
384	
385	18,176 + 125 = 18,301 — all new mocho triples accounted for by the two fixes.
386	
387	**Attribution:**
388	- **+18,176 `rdfs:label`** — Bug 1. Creator Track 2 now correctly iterates `agent.prefLabel[]` via `value_to_nt_obj`; all previously silenced agent labels are emitted. The contributor literal-match branch contributes its `rdfs:label` half here as well.
389	- **+125 `rdf:type mocho:Agent`** — Bug 2 (literal-match path). Contributor literals that previously fell through as plain `dc:contributor "…"@lang` now resolve to DDB/GND agents and emit `mocho:Agent` type stubs.
390	- `dcterms:creator` and `dc:contributor` counts unchanged — the fixes add stubs for existing agent resolutions, not new CHO-level predicates.
391	
392	---
393	
394	## 9. `hierarchyType` URI fixes (2026-05-12)
395	
396	Two bugs in `retype_entities` (`emitters.py`) in the handling of `ProvidedCHO.hierarchyType`.
397	
398	Corpus evidence: object `LH3LUU63TUKZJHMQEILGTP3HZXZP5IFT` (`s2.sqlite`) has `"hierarchyType": "htype_007 htype_020"`.
399	
400	### 9.1 Bug 1 — wrong vocnet URI form
401	
402	Raw values use the form `htype_NNN` (e.g. `htype_007`). The correct vocnet IRI suffix is `htNNN` (e.g. `ht007`). The emitter was appending the raw code directly to `_HTYPE_PREFIX`, producing the invalid IRI `http://ddb.vocnet.org/hierarchietyp/htype_007`.
403	
404	**Fix** (`emitters.py` lines 277–283): apply `.replace("htype_", "ht")` to each code before constructing the IRI.
405	
406	### 9.2 Bug 2 — space-separated multi-value treated as single code
407	
408	`hierarchyType` can contain multiple space-separated codes. The emitter passed the raw string as one unit, producing a single IRI with an embedded space: `<…/htype_007 htype_020>`. The dispatch lookup (`htype_map.get(htype_code)`) also silently failed for any multi-value record.
409	
410	**Fix** (`emitters.py`):
411	- **Dispatch** (layer 1): `htype_map.get(htype_code.split()[0])` — first code only, consistent with "most specific class" intent.
412	- **URI emission**: iterate `htype_code.split()`; emit one `ddbedm:hierarchyType` triple per code with the corrected IRI.
413	
414	### 9.3 Test additions
415	
416	Three new tests in `TestRetypeEntities` (`test_transform.py`):
417	
418	| Test | Assertion |
419	|---|---|
420	| `test_multi_htype_emits_two_triples` | `"htype_007 htype_020"` → exactly 2 `ddbedm:hierarchyType` triples, IRIs `ht007` and `ht020` |
421	| `test_multi_htype_no_space_in_iri` | No object token in any `ddbedm:hierarchyType` triple contains a space |
422	| `test_multi_htype_dispatch_uses_first` | `flags["htype_used"] is True` and `flags["fallback"] is False` — first code resolves a class |
423	
424	Two existing tests updated: `test_sparte001_mt003_htype021` and `test_htype_emitted_as_iri` now assert `ht021`/`ht042` (not `htype_021`/`htype_042`) in the emitted IRI.
425	
426	Total: 140 tests.
427	
428	---
429	
430	## 10. BCP 47 language tag normalization (2026-05-12)
431	
432	QLever validates RDF language tags against BCP 47 and terminates indexing on the first invalid tag. DDB source records carry ISO 639-2 collective codes (e.g. `wen`, `gem`) and malformed codes (e.g. `gerger`) in the `lang` field of cortex JSON. Neither is a valid BCP 47 individual-language subtag.
433	
434	Design record: `gemea/notes/ingest/transform-language-tag.md`.
435	
436	### 10.1 Validation approach
437	
438	`langcodes` (v3.5.1, added to `requirements.txt`) is used rather than a hand-curated dict. Two failure classes must be caught:
439	
440	1. **Malformed codes** (e.g. `gerger`) — `langcodes.tag_is_valid()` returns `False`.
441	2. **IANA collection subtags** (e.g. `wen`, `gem`) — `langcodes.tag_is_valid()` returns `True` (they are in the IANA registry), but QLever rejects them. Detected by membership in `_IANA_COLLECTION_CODES`, a `frozenset` parsed at import time from the IANA registry bundled with `langcodes` (`data/language-subtag-registry.txt`, `Scope: collection` entries). 116 codes in the current registry.
442	
443	Both → normalized to `"und"` (BCP 47 "undetermined"). Original code retained via provenance triple.
444	
445	### 10.2 Code changes
446	
447	**`utils.py`**
448	
449	| Change | Detail |
450	|---|---|
451	| `_build_iana_collection_codes()` | Parses bundled IANA registry line-by-line; returns `frozenset` of all `Scope: collection` subtags. Falls back to empty set on error. |
452	| `_IANA_COLLECTION_CODES` | Module-level `frozenset` built at import. |
453	| `_invalid_bcp47(lang)` | `@lru_cache(maxsize=512)`. `True` if `not tag_is_valid(lang) or lang in _IANA_COLLECTION_CODES`. |
454	| `value_to_nt_obj()` | Added `lang_coll: set[str] \| None = None` parameter. Strips `lang` before validation; guards `lang_coll.add()` against values containing internal spaces (see §10.3). |
455	
456	**`emitters.py`**
457	
458	`lang_coll: set[str] | None = None` added to `emit_ddbedm_triples()` and `emit_mocho_triples()`; passed to every `value_to_nt_obj()` call that processes CHO fields (title, generic property loop). Secondary emitters (`emit_subject_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_hastype_triples`, `emit_current_location_triples`) are unchanged — corpus analysis (`analyse_lang_tags_by_entity.py`) confirmed no collective codes on non-CHO entities.
459	
460	**`transform.py`**
461	
462	`lang_coll: set[str] = set()` created in `transform_record()`; passed to both emitters (mutated in place). After emitters complete, one `dcterms:language <http://id.loc.gov/vocabulary/iso639-2/{orig_lang}>` provenance triple per unique original code is emitted to `GRAPH_LANG_TITLE`. Subject is `ddb_uri` (not `cho_uri`).
463	
464	**`constants.py`**
465	
466	`GRAPH_LANG_TITLE = "https://gemea.ise.fiz-karlsruhe.de/graph/lang-title"` added.
467	
468	### 10.3 Whitespace-in-lang bug
469	
470	`lang = "en en"` appears on record `LH3LUU63TUKZJHMQEILGTP3HZXZP5IFT` (`s2.sqlite`) on `ProvidedCHO.dcType` and `Concept[1].prefLabel`. Root cause: `Concept[1].about` contains two space-joined URIs (`"http://ddb.vocnet.org/hierarchietyp/ht007 http://ddb.vocnet.org/hierarchietyp/ht020"`); the DDB XML-to-JSON converter applied the same join to the `lang` attributes of the repeated element, concatenating `"en"` + `" "` + `"en"`.
471	
472	Without the guard, `lang_coll.add("en en")` would produce `<http://id.loc.gov/vocabulary/iso639-2/en en>` — an invalid N-Quads IRI. Fix in `value_to_nt_obj()`:
473	
474	```python
475	lang = val.get("lang")
476	if lang:
477	    lang = str(lang).strip()
478	if lang and _invalid_bcp47(lang):
479	    if lang_coll is not None and " " not in lang:
480	        lang_coll.add(lang)
481	    lang = "und"
482	```
483	
484	`.strip()` handles leading/trailing whitespace. `" " not in lang` prevents any space-containing value from entering `lang_coll` (it still normalizes to `"und"`, so the literal output is correct).
485	
486	### 10.4 Test additions
487	
488	Three new test classes in `test_transform.py`:
489	
490	| Class | Tests | Covers |
491	|---|---|---|
492	| `TestIanaCollectionCodes` | 3 | Registry loaded (>0 codes); known collectives (`wen`, `gem`) present; valid individuals (`ger`, `eng`) absent |
493	| `TestInvalidBcp47` | 4 | Collective → `True`; malformed → `True`; valid codes → `False`; `und` itself → `False` |
494	| `TestValueToNtObjLangNorm` | 10 | `wen`/`gem`/`gerger` → `@und`; valid lang unchanged; `lang_coll` populated for collective/malformed, empty for valid; `"en en"` → `@und` and not added to `lang_coll`; leading/trailing whitespace stripped |
495	
496	Total: 137 tests (135 passing; 2 pre-existing failures in `TestRetypeEntities` — see §9.3).
497	
498	---
499	
500	## 12. Full-corpus run plan
501	
502	The production orchestrator is `scripts/run-transform-sector.sh`. It splits the SQLite table into `--workers` chunks, launches one `python -m transform` OS process per chunk, waits for all to finish, then merges.
503	
504	```bash
505	# one sector, all defaults (50 workers, merge stats only):
506	bash scripts/run-transform-sector.sh --merge --sector s2
507	
508	# merge including .nq:
509	bash scripts/run-transform-sector.sh --merge-all --sector s2
510	
511	# custom worker count:
512	bash scripts/run-transform-sector.sh --merge --sector s2 --workers 20
513	```
514	
515	Key defaults: `--sqlite-dir /data/gemea/sqlite`, `--scripts-dir /home/ann/goethe-faust/scripts`, `--output-dir /data/gemea/www/downloads/gemea/YYYYMMDD` (today's date).
516	
517	**Merge output naming**: `merge.py` receives `--stem "$SECTOR"`, so all merged files are named `<sector>-stats.json`, `<sector>.log`, etc. (not the version-date directory name). Multiple sectors run sequentially into the same version dir produce non-colliding outputs.
518	
519	**`--merge` vs `--merge-all`**: `--merge` passes `--skip-nq` to `merge.py` — merges stats, werk_staging, errors, and logs only; `.nq` shards are retained for later concatenation. `--merge-all` also concatenates `.nq` shards into `<sector>.nq`.
520	
521	Config files (`--alignment`, `--lido`, `--htype`, `--mediatype`, `--audio`) default to `output/config/` relative to the goethe-faust root derived from `--scripts-dir`.
522	
523	Estimated wall time at 18.5M records: ~1–1.5 h (7 parallel workers).
524	
```

---

### Assistant *(2026-05-13T13:56:19.499Z)*

Now let me read the rest of emitters.py to understand the ddbedm entity emission structure.

---

### Assistant *(2026-05-13T13:56:20.135Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 180
}
```

---

### User *(2026-05-13T13:56:20.486Z)*

**Tool result**
```
180	        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
181	        for binary in coerce_list((record.get("binaries") or {}).get("binary")):
182	            if not isinstance(binary, dict):
183	                continue
184	            ref   = (binary.get("ref")            or "").strip()
185	            name  = (binary.get("name")           or "").strip()
186	            name2 = (binary.get("name2")          or "").strip()
187	            kind  = (binary.get("kind")           or "").strip()
188	            lpath = (binary.get("local_pathname") or "").strip()
189	            if ref:
190	                lines.append(make_nq(src_nt, f"<{DC_ID}>",
191	                                     f'"{_escape_literal(ref)}"', graph_iri))
192	            if name:
193	                lines.append(make_nq(src_nt, f"<{DC_TITLE}>",
194	                                     f'"{_escape_literal(name)}"@de', graph_iri))
195	            desc = (name2 + " | " + name) if name2 and name else (name2 or name)
196	            if desc:
197	                lines.append(make_nq(src_nt, f"<{DC_DESCRIPTION}>",
198	                                     f'"{_escape_literal(desc)}"@de', graph_iri))
199	            if kind:
200	                lines.append(make_nq(src_nt, f"<{DCTERMS_RIGHTS}>", f"<{kind}>", graph_iri))
201	            if lpath and lpath.startswith("http"):
202	                lines.append(make_nq(src_nt, f"<{DCTERMS_SOURCE}>", f"<{lpath}>", graph_iri))
203	
204	    return lines
205	
206	
207	def retype_entities(
208	    sector: str,
209	    mediatype: str,
210	    htype_code: str | None,
211	    dctype_vals: list,
212	    cho_nt: str,
213	    mediatype_class_map: dict,
214	    htype_map: dict,
215	    audio_type2class: dict,
216	    graph_iri: str,
217	) -> tuple[NQList, str, str, dict]:
218	    """Dispatch rdf:type triples for a ProvidedCHO (§6.4, transform-revised-plan.md §1.1).
219	
220	    Returns (lines, target_class_full_iri, wemi, dispatch_flags).
221	    target_class is used for property alignment lookup; wemi for contributor column selection.
222	    dispatch_flags: {"htype_used": bool, "fallback": bool}
223	    """
224	    lines: NQList = []
225	    row = (
226	        mediatype_class_map.get((sector, mediatype))
227	        or mediatype_class_map.get(("any", "any"))
228	        or {}
229	    )
230	    use_htype  = row.get("use_htype", False)
231	    rdf_type_w = row.get("rdf_type_w", "")
232	    rdf_type_m = row.get("rdf_type_m", "")
233	
234	    primary_class = ""
235	    htype_used    = False
236	
237	    # Layer 1: htype-derived class (for htype-first strata)
238	    # hierarchyType may be space-separated (e.g. "htype_007 htype_020"); use first for dispatch
239	    if use_htype and htype_code:
240	        entry = htype_map.get(htype_code.split()[0])
241	        if entry:
242	            type_iris, rst_iris = entry
243	            for t in type_iris:
244	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{t}>", graph_iri))
245	            for r in rst_iris:
246	                lines.append(make_nq(cho_nt, f"<{RICO_HAS_RST}>", f"<{r}>", graph_iri))
247	            primary_class = type_iris[0]  # first = most specific
248	            htype_used    = True
249	
250	    # Layer 2: fixed mediatype class (always emit if set; added on top of layer 1)
251	    if rdf_type_w:
252	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_w}>", graph_iri))
253	        if not primary_class:
254	            primary_class = rdf_type_w
255	    if rdf_type_m:
256	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_m}>", graph_iri))
257	        if not primary_class:
258	            primary_class = rdf_type_m
259	
260	    # Audio group dispatch: dc:type → mo:MusicalManifestation (Group A) (§2.3)
261	    _aco_audio = "https://w3id.org/ac-ontology/aco#AudioManifestation"
262	    _mo_mani   = "http://purl.org/ontology/mo/MusicalManifestation"
263	    if rdf_type_m == _aco_audio and dctype_vals and not use_htype:
264	        for dct in dctype_vals:
265	            dc_text = (dct.get("$") or "").strip() if isinstance(dct, dict) else ""
266	            if audio_type2class.get((sector, dc_text)) == "A":
267	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{_mo_mani}>", graph_iri))
268	                primary_class = _mo_mani
269	                break
270	
271	    # D9 fallback — no class resolved
272	    is_fallback = not primary_class
273	    if is_fallback:
274	        fallback = MOCHO_NS + "Manifestation"
275	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{fallback}>", graph_iri))
276	        primary_class = fallback
277	
278	    # hierarchyType may be space-separated; emit one triple per code with correct URI form
279	    # (raw: "htype_007" → vocnet: "ht007")
280	    if htype_code:
281	        for _code in htype_code.split():
282	            _uri_code = _code.replace("htype_", "ht")
283	            lines.append(make_nq(cho_nt, f"<{DDB_HIERARCHY_TYPE}>",
284	                                 f"<{_HTYPE_PREFIX}{_uri_code}>", graph_iri))
285	
286	    wemi = _CLASS_WEMI.get(primary_class, "M")
287	    return lines, primary_class, wemi, {"htype_used": htype_used, "fallback": is_fallback}
288	
289	
290	def emit_subject_triples(
291	    cho_nt: str,
292	    subject_vals: list,
293	    concepts_index: dict[str, dict],
294	    graph_iri: str,
295	    bare_id_to_uri: dict[str, str] | None = None,
296	) -> NQList:
297	    """Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended)."""
298	    lines: NQList = []
299	    seen: set[str] = set()
300	    _bare = bare_id_to_uri or {}
301	    for val in subject_vals:
302	        if not isinstance(val, dict):
303	            continue
304	        resource_raw = (val.get("resource") or "").strip()
305	        label        = (val.get("$")        or "").strip()
306	        lang         = (val.get("lang")     or "").strip()
307	        if resource_raw:
308	            for uri in resource_uris(resource_raw, _bare, "Concept"):
309	                if uri in seen:
310	                    continue
311	                seen.add(uri)
312	                lines.append(make_nq(cho_nt, f"<{DCTERMS_SUBJECT}>", f"<{uri}>", graph_iri))
313	                concept = concepts_index.get(resource_raw) or concepts_index.get(uri)
314	                if concept:
315	                    for pl in coerce_list(concept.get("prefLabel")):
316	                        for obj_nt in value_to_nt_obj(pl):
317	                            lines.append(make_nq(f"<{uri}>", f"<{RDFS_LABEL}>",
318	                                                 obj_nt, graph_iri))
319	        elif label:
320	            key = f"lit:{label}"
321	            if key in seen:
322	                continue
323	            seen.add(key)
324	            escaped = _escape_literal(label)
325	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
326	            lines.append(make_nq(cho_nt, f"<{DC_SUBJECT}>", obj_nt, graph_iri))
327	    return lines
328	
329	
330	def emit_hastype_triples(
331	    cho_nt: str,
332	    hastype_vals: list,
333	    concepts_index: dict[str, dict],
334	    graph_iri: str,
335	    bare_id_to_uri: dict[str, str] | None = None,
336	) -> NQList:
337	    """Emit edm:hasType + rdfs:label stub for each IRI-valued hasType entry.
338	
339	    Bare 32-char IDs are expanded via the per-record index (fallback: mint as Concept URN).
340	    Literal-only values (no resource) are silently skipped — edm:hasType range is skos:Concept.
341	    """
342	    lines: NQList = []
343	    seen: set[str] = set()
344	    _bare = bare_id_to_uri or {}
345	    for val in coerce_list(hastype_vals):
346	        if not isinstance(val, dict):
347	            continue
348	        resource_raw = (val.get("resource") or "").strip()
349	        if not resource_raw:
350	            continue
351	        for uri in resource_uris(resource_raw, _bare, "Concept"):
352	            if uri in seen:
353	                continue
354	            seen.add(uri)
355	            lines.append(make_nq(cho_nt, f"<{EDM_HAS_TYPE}>", f"<{uri}>", graph_iri))
356	            concept = concepts_index.get(resource_raw) or concepts_index.get(uri)
357	            if concept:
358	                for pl in coerce_list(concept.get("prefLabel")):
359	                    for obj_nt in value_to_nt_obj(pl):
360	                        lines.append(make_nq(f"<{uri}>", f"<{RDFS_LABEL}>",
361	                                             obj_nt, graph_iri))
362	    return lines
363	
364	
365	def emit_current_location_triples(
366	    cho_nt: str,
367	    currentloc_vals: object,
368	    places_index: dict[str, dict],
369	    graph_iri: str,
370	    bare_id_to_uri: dict[str, str] | None = None,
371	) -> NQList:
372	    """Emit edm:currentLocation triples with optional rdfs:label stub from matching edm:Place.
373	
374	    URI values: emit <cho> edm:currentLocation <uri> + <uri> rdfs:label <prefLabel> if found.
375	    Literal values: emit <cho> edm:currentLocation "literal" (pass-through, no stub).
376	    Multi-URI resource fields are split; bare IDs are expanded. Deduplicates URIs per record.
377	    No rdf:type emitted for Place stubs in mocho graph (D17).
378	    """
379	    edm_current_location = EDM_NS + "currentLocation"
380	    lines: NQList = []
381	    seen: set[str] = set()
382	    _bare = bare_id_to_uri or {}
383	
384	    for val in coerce_list(currentloc_vals):
385	        if not isinstance(val, dict):
386	            continue
387	        resource_raw = (val.get("resource") or "").strip()
388	        label        = (val.get("$")        or "").strip()
389	        lang         = (val.get("lang")     or "").strip()
390	
391	        if resource_raw:
392	            for uri in resource_uris(resource_raw, _bare, "Place"):
393	                if uri in seen:
394	                    continue
395	                seen.add(uri)
396	                lines.append(make_nq(cho_nt, f"<{edm_current_location}>",
397	                                     f"<{uri}>", graph_iri))
398	                place = places_index.get(resource_raw) or places_index.get(uri)
399	                if place:
400	                    for pl in coerce_list(place.get("prefLabel")):
401	                        for obj_nt in value_to_nt_obj(pl):
402	                            lines.append(make_nq(f"<{uri}>", f"<{RDFS_LABEL}>",
403	                                                 obj_nt, graph_iri))
404	        elif label:
405	            escaped = _escape_literal(label)
406	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
407	            lines.append(make_nq(cho_nt, f"<{edm_current_location}>", obj_nt, graph_iri))
408	    return lines
409	
410	
411	def emit_creator_triples(
412	    cho_nt: str,
413	    creator_vals: list,
414	    agents_index: dict[str, AgentDict],
415	    target_class: str,
416	    class_prop_align: PropAlign,
417	    graph_iri: str,
418	    bare_id_to_uri: dict[str, str] | None = None,
419	) -> NQList:
420	    """Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).
421	
422	    Both tracks run independently for each creator value (D2 / props-mapping §4).
423	    """
424	    lines: NQList = []
425	    dc_creator_iri = "http://purl.org/dc/elements/1.1/creator"
426	    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), "")
427	
428	    for val in coerce_list(creator_vals):
429	        if not isinstance(val, dict):
430	            continue
431	        resource_raw = (val.get("resource") or "").strip()
432	        label        = (val.get("$")        or "").strip()
433	        lang         = (val.get("lang")     or "").strip()
434	        primary_resource = resource_raw.split()[0] if resource_raw else ""
435	
436	        # Track 1: class-specific predicate (always runs when target_prop is known)
437	        if track1_prop:
438	            if resource_raw:
439	                for uri in resource_uris(resource_raw, bare_id_to_uri, "Agent"):
440	                    lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{uri}>", graph_iri))
441	            elif label:
442	                escaped = _escape_literal(label)
443	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
444	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", obj_nt, graph_iri))
445	
446	        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)
447	        agent = resolve_agent(label, primary_resource, agents_index)
448	        if agent:
449	            agent_uri = _sanitize_iri((agent.get("about") or "").strip())
450	            if agent_uri and is_ddb_or_gnd(agent_uri):
451	                lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>",
452	                                     f"<{agent_uri}>", graph_iri))
453	                agent_nt = f"<{agent_uri}>"
454	                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
455	                pref_list = coerce_list(agent.get("prefLabel"))
456	                if pref_list:
457	                    for pl in pref_list:
458	                        for obj_nt in value_to_nt_obj(pl):
459	                            lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
460	                elif label:
461	                    escaped = _escape_literal(label)
462	                    obj_nt = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
463	                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
464	    return lines
465	
466	
467	def emit_contributor_triples(
468	    cho_nt: str,
469	    contributor_vals: list,
470	    event_participant_index: dict[str, str],
471	    lido_dispatch: dict[str, dict],
472	    target_class: str,
473	    wemi: str,
474	    graph_iri: str,
475	    bare_id_to_uri: dict[str, str] | None = None,
476	    agents_index: dict[str, AgentDict] | None = None,
477	) -> NQList:
478	    """Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5)."""
479	    lines: NQList = []
480	    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), "dc_agent_fallback")
481	    _agents  = agents_index or {}
482	
483	    for val in coerce_list(contributor_vals):
484	        if not isinstance(val, dict):
485	            continue
486	        resource_raw     = (val.get("resource") or "").strip()
487	        label            = (val.get("$")        or "").strip()
488	        lang             = (val.get("lang")     or "").strip()
489	        primary_resource = resource_raw.split()[0] if resource_raw else ""
490	
491	        lido_type   = event_participant_index.get(primary_resource) if primary_resource else None
492	        lido_row    = lido_dispatch.get(lido_type) if lido_type else None
493	        target_prop = (
494	            (lido_row.get(prop_col) or lido_row.get("dc_agent_fallback") or DC_CONTRIBUTOR)
495	            if lido_row else DC_CONTRIBUTOR
496	        )
497	
498	        if resource_raw:
499	            agent     = resolve_agent("", primary_resource, _agents)
500	            pref_list = coerce_list(agent.get("prefLabel")) if agent else []
501	            for uri in resource_uris(resource_raw, bare_id_to_uri, "Agent"):
502	                lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{uri}>", graph_iri))
503	                agent_nt = f"<{uri}>"
504	                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
505	                if pref_list:
506	                    for pl in pref_list:
507	                        for obj_nt in value_to_nt_obj(pl):
508	                            lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
509	                elif label:
510	                    escaped = _escape_literal(label)
511	                    obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
512	                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
513	        elif label:
514	            agent = resolve_agent(label, "", _agents)
515	            if agent:
516	                agent_uri = _sanitize_iri((agent.get("about") or "").strip())
517	                if agent_uri and is_ddb_or_gnd(agent_uri):
518	                    lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{agent_uri}>", graph_iri))
519	                    agent_nt  = f"<{agent_uri}>"
520	                    lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
521	                    pref_list = coerce_list(agent.get("prefLabel"))
522	                    if pref_list:
523	                        for pl in pref_list:
524	                            for obj_nt in value_to_nt_obj(pl):
525	                                lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
526	                    else:
527	                        escaped = _escape_literal(label)
528	                        obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
529	                        lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
530	                    continue
531	            escaped = _escape_literal(label)
532	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
533	            lines.append(make_nq(cho_nt, f"<{DC_CONTRIBUTOR}>", obj_nt, graph_iri))
534	    return lines
535	
536	
537	def emit_aggregation_triples(agg: dict, cho_nt: str, graph_iri: str) -> NQList:
538	    """Emit mocho triples derived from the Aggregation block (D23)."""
539	    lines: NQList = []
540	    _edm_dp     = EDM_NS + "dataProvider"
541	    _org_prefix = "http://www.deutsche-digitale-bibliothek.de/organization/"
542	
543	    is_shown = agg.get("isShownAt") or {}
544	    if isinstance(is_shown, dict):
545	        for uri in (is_shown.get("resource") or "").strip().split():
546	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SOURCE}>",
547	                                 f"<{_sanitize_iri(uri)}>", graph_iri))
548	
549	    for dp in coerce_list(agg.get("dataProvider")):
550	        if not isinstance(dp, dict):
551	            continue
552	        for uri in (dp.get("resource") or "").strip().split():
553	            if uri.startswith(_org_prefix):
554	                lines.append(make_nq(cho_nt, f"<{_edm_dp}>",
555	                                     f"<{_sanitize_iri(uri)}>", graph_iri))
556	
557	    for obj in coerce_list(agg.get("object")):
558	        if not isinstance(obj, dict):
559	            continue
560	        for uri in (obj.get("resource") or "").strip().split():
561	            lines.append(make_nq(cho_nt, f"<{FOAF_THUMBNAIL}>",
562	                                 f"<{_sanitize_iri(uri)}>", graph_iri))
563	
564	    return lines
565	
566	
567	def emit_place_stubs(places: object, graph_iri: str) -> NQList:
568	    """Emit rdfs:label stubs for each Place entity referenced by the record (D24)."""
569	    lines: NQList = []
570	    for place in coerce_list(places):
571	        if not isinstance(place, dict):
572	            continue
573	        raw_about = (place.get("about") or "").strip()
574	        if not raw_about:
575	            continue
576	        place_uri = mint_bare_id("Place", _sanitize_iri(raw_about.split()[0]))
577	        place_nt  = f"<{place_uri}>"
578	        for lbl in coerce_list(place.get("prefLabel")):
579	            for obj_nt in value_to_nt_obj(lbl):
580	                lines.append(make_nq(place_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
581	    return lines
582	
583	
584	def werk_staging_row(cho_uri: str, cho: dict, target_class: str) -> dict | None:
585	    """Build a werk_staging dict if target_class is a W-slot class (D26). Else None."""
586	    if target_class not in _W_SLOT_CLASSES:
587	        return None
588	
589	    title = ""
590	    tv = cho.get("title")
591	    if isinstance(tv, dict):
592	        title = (tv.get("$") or "").strip()
593	    elif isinstance(tv, list) and tv:
594	        first = tv[0]
595	        title = (first.get("$") or "").strip() if isinstance(first, dict) else ""
596	
597	    dc_alt: list[str] = []
598	    for v in coerce_list(cho.get("alternative")):
599	        t = (v.get("$") or "").strip() if isinstance(v, dict) else ""
600	        if t:
601	            dc_alt.append(t)
602	
603	    dc_created = ""
604	    for v in coerce_list(cho.get("date")):
605	        t = (v if isinstance(v, str) else "").strip()
606	        if t:
607	            dc_created = t
608	            break
609	
610	    creator_uris: list[str] = []
611	    creator_lits: list[str] = []
612	    for v in coerce_list(cho.get("creator")):
613	        if not isinstance(v, dict):
614	            continue
615	        uri = (v.get("resource") or "").strip()
616	        lit = (v.get("$")        or "").strip()
617	        if uri:
618	            creator_uris.append(uri)
619	        elif lit:
620	            creator_lits.append(lit)
621	
622	    obj_id = cho_uri.rsplit("/", 1)[-1]
623	    return {
624	        "ddb_obj_id":       obj_id,
625	        "cho_uri":          cho_uri,
626	        "target_class":     target_class,
627	        "dc_title":         title,
628	        "dc_alternative":   dc_alt,
629	        "dc_created":       dc_created,
630	        "creator_uris":     creator_uris,
631	        "creator_literals": creator_lits,
632	    }
633	
634	
635	def emit_mocho_triples(
636	    rdf: dict,
637	    cho_uri: str,
638	    ddb_uri: str,
639	    sector: str,
640	    mediatype: str,
641	    mediatype_class_map: dict,
642	    htype_map: dict,
643	    audio_type2class: dict,
644	    class_prop_align: PropAlign,
645	    lido_dispatch: dict,
646	    graph_iri: str,
647	    lang_coll: set[str] | None = None,
648	) -> tuple[NQList, str, str, dict]:
649	    """Emit all mocho-graph triples for one record (§6.3). Returns (lines, target_class, wemi, dispatch_flags).
650	
651	    dispatch_flags includes "preds_all" and "preds_new" Counters (CURIEs) built during emission.
652	    """
653	    lines:     NQList  = []
654	    preds_all: Counter = Counter()
655	    preds_new: Counter = Counter()
656	    sani_ctr:  Counter = Counter()
657	    bare_id_to_uri = build_bare_id_index(rdf)
658	
659	    def _track(pred_iri: str) -> None:
660	        curie = _to_curie(pred_iri)
661	        preds_all[curie] += 1
662	        if any(pred_iri.startswith(ns) for ns in _NEW_NS):
663	            preds_new[curie] += 1
664	
665	    def _track_nqlist(nqlist: NQList) -> None:
666	        for nq in nqlist:
667	            try:
668	                _track(nq.split("> <", 1)[1].split(">", 1)[0])
669	            except IndexError:
670	                pass
671	
672	    cho: dict = rdf.get("ProvidedCHO") or {}
673	    if isinstance(cho, list):
674	        cho = cho[0] if cho else {}
675	
676	    cho_nt      = f"<{cho_uri}>"
677	    htype       = (cho.get("hierarchyType") or "").strip() or None
678	    dctype_vals = coerce_list(cho.get("dcType"))
679	
680	    # ── Class dispatch ────────────────────────────────────────────────────────
681	    type_lines, target_class, wemi, dispatch_flags = retype_entities(
682	        sector, mediatype, htype, dctype_vals,
683	        cho_nt, mediatype_class_map, htype_map, audio_type2class, graph_iri,
684	    )
685	    lines.extend(type_lines)
686	    _track_nqlist(type_lines)
687	
688	    # owl:sameAs link to original DDB URI (D22)
689	    lines.append(make_nq(cho_nt, f"<{OWL_SAMEAS}>", f"<{ddb_uri}>", graph_iri))
690	    _track(OWL_SAMEAS)
691	
692	    # mocho:mediaType and mocho:sector as vocnet IRIs
693	    if mediatype != "any":
694	        lines.append(make_nq(cho_nt, f"<{MOCHO_NS}mediaType>", f"<{mediatype}>", graph_iri))
695	        _track(MOCHO_NS + "mediaType")
696	    if sector != "any":
697	        lines.append(make_nq(cho_nt, f"<{MOCHO_NS}sector>", f"<{sector}>", graph_iri))
698	        _track(MOCHO_NS + "sector")
699	
700	    # ── Build per-record indexes ───────────────────────────────────────────────
701	    agents_index: dict[str, AgentDict] = {}
702	    for agent in coerce_list(rdf.get("Agent")):
703	        if not isinstance(agent, dict):
704	            continue
705	        about = (agent.get("about") or "").strip()
706	        if about:
707	            agents_index[mint_bare_id("Agent", about)] = agent
708	        for pl in coerce_list(agent.get("prefLabel")):
709	            t = (pl.get("$") or "").strip() if isinstance(pl, dict) else ""
710	            if t:
711	                agents_index.setdefault(t, agent)
712	
713	    event_participant_index: dict[str, str] = {}
714	    for event in coerce_list(rdf.get("Event")):
715	        if not isinstance(event, dict):
716	            continue
717	        ht = event.get("hasType") or {}
718	        if isinstance(ht, list):
719	            ht = ht[0] if ht else {}
720	        lido_type_uri = (ht.get("resource") or "").strip() if isinstance(ht, dict) else ""
721	        for p in coerce_list(event.get("P11_had_participant")):
722	            puri = (p.get("resource") or "").strip() if isinstance(p, dict) else ""
723	            if puri and lido_type_uri:
724	                event_participant_index[puri] = lido_type_uri
725	
726	    concepts_index: dict[str, dict] = {}
727	    for concept in coerce_list(rdf.get("Concept")):
728	        if not isinstance(concept, dict):
729	            continue
730	        about = (concept.get("about") or "").strip()
731	        if about:
732	            concepts_index[about] = concept
733	
734	    places_index: dict[str, dict] = {}
735	    for place in coerce_list(rdf.get("Place")):
736	        if not isinstance(place, dict):
737	            continue
738	        about = (place.get("about") or "").strip()
739	        if about:
740	            places_index[about.split()[0]] = place
741	
742	    # ── dc:title — dual-emit (props-mapping D4) ───────────────────────────────
743	    dc_title_iri = "http://purl.org/dc/elements/1.1/title"
744	    title_prop   = class_prop_align.get((target_class, dc_title_iri), "")
745	    for obj_nt in value_to_nt_obj(cho.get("title"), sani_ctr, lang_coll):
746	        lines.append(make_nq(cho_nt, f"<{dc_title_iri}>", obj_nt, graph_iri))
747	        _track(dc_title_iri)
748	        if title_prop and title_prop != dc_title_iri:
749	            lines.append(make_nq(cho_nt, f"<{title_prop}>", obj_nt, graph_iri))
750	            _track(title_prop)
751	
752	    # ── Generic property loop ─────────────────────────────────────────────────
753	    dc_date_iri   = "http://purl.org/dc/elements/1.1/date"
754	    dcterms_iss   = "http://purl.org/dc/terms/issued"
755	    dcterms_ipart = "http://purl.org/dc/terms/isPartOf"
756	    _special_keys = frozenset({"creator", "contributor", "title"}) | SUBJECT_KEYS | _MOCHO_SKIP
757	
758	    subject_vals: list = []
759	    for skey in SUBJECT_KEYS:
760	        subject_vals.extend(coerce_list(cho.get(skey)))
761	    hastype_vals: list = coerce_list(cho.get("hasType"))
762	
763	    for prop, val in cho.items():
764	        if prop in _special_keys:
765	            continue
766	        prop_iri = _DDBEDM_PROP.get(prop)
767	        if not prop_iri:
768	            continue
769	        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
770	        if not target_prop:
771	            continue
772	
773	        if prop_iri in (dc_date_iri, dcterms_iss):
774	            # Date normalisation (D15 / props-mapping §3.1)
775	            for v in coerce_list(val):
776	                raw = (v if isinstance(v, str) else
777	                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
778	                for normed in normalize_date(raw):
779	                    if normed:
780	                        lines.append(make_nq(cho_nt, f"<{target_prop}>",
781	                                             f'"{_escape_literal(normed)}"', graph_iri))
782	                        _track(target_prop)
783	            continue
784	
785	        if prop_iri == dcterms_ipart:
786	            # isPartOf URI sanitisation (props-mapping §3.1)
787	            for obj_nt in value_to_nt_obj(val, sani_ctr):
788	                if not obj_nt.startswith("<"):
789	                    continue  # literal isPartOf skipped in mocho graph
790	                uri = obj_nt[1:-1]
791	                if not uri.startswith("http"):
792	                    if len(uri) == 32:
793	                        uri = DDB_ITEM_BASE + uri
794	                    else:
795	                        continue
796	                lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{uri}>", graph_iri))
797	                _track(target_prop)
798	            continue
799	
800	        for obj_nt in value_to_nt_obj(val, sani_ctr, lang_coll):
801	            lines.append(make_nq(cho_nt, f"<{target_prop}>",
802	                                 expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))
803	            _track(target_prop)
804	
805	    # ── Special handlers ──────────────────────────────────────────────────────
806	    _creator_lines = emit_creator_triples(
807	        cho_nt, cho.get("creator"), agents_index, target_class, class_prop_align, graph_iri,
808	        bare_id_to_uri,
809	    )
810	    lines.extend(_creator_lines)
811	    _track_nqlist(_creator_lines)
812	
813	    _contrib_lines = emit_contributor_triples(
814	        cho_nt, cho.get("contributor"),
815	        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,
816	        bare_id_to_uri, agents_index,
817	    )
818	    lines.extend(_contrib_lines)
819	    _track_nqlist(_contrib_lines)
820	
821	    if subject_vals:
822	        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri,
823	                                              bare_id_to_uri)
824	        lines.extend(_subject_lines)
825	        _track_nqlist(_subject_lines)
826	
827	    if hastype_vals:
828	        _hastype_lines = emit_hastype_triples(cho_nt, hastype_vals, concepts_index, graph_iri,
829	                                              bare_id_to_uri)
830	        lines.extend(_hastype_lines)
831	        _track_nqlist(_hastype_lines)
832	
833	    currentloc_vals = coerce_list(cho.get("currentLocation"))
834	    if currentloc_vals:
835	        _curloc_lines = emit_current_location_triples(
836	            cho_nt, currentloc_vals, places_index, graph_iri, bare_id_to_uri,
837	        )
838	        lines.extend(_curloc_lines)
839	        _track_nqlist(_curloc_lines)
840	
841	    # ── Aggregation & Place ───────────────────────────────────────────────────
842	    agg = rdf.get("Aggregation") or {}
843	    if isinstance(agg, list):
844	        agg = agg[0] if agg else {}
845	    _agg_lines = emit_aggregation_triples(agg, cho_nt, graph_iri)
846	    lines.extend(_agg_lines)
847	    _track_nqlist(_agg_lines)
848	
849	    _place_lines = emit_place_stubs(rdf.get("Place"), graph_iri)
850	    lines.extend(_place_lines)
851	    _track_nqlist(_place_lines)
852	
853	    dispatch_flags["preds_all"]     = preds_all
854	    dispatch_flags["preds_new"]     = preds_new
855	    dispatch_flags["uri_sanitized"] = sani_ctr["uri_sanitized"]
856	    dispatch_flags["uri_split"]     = sani_ctr["uri_split"]
857	    return lines, target_class, wemi, dispatch_flags
858	
```

---

### Assistant *(2026-05-13T13:59:01.200Z)*

Good. Now I have everything I need. Let me implement all changes across the 3 code files and 3 notes files.

---

### Assistant *(2026-05-13T13:59:01.201Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "offset": 1,
  "limit": 20
}
```

---

### User *(2026-05-13T13:59:01.219Z)*

**Tool result**
```
1	# ADR: transform_edm_to_mocho.py — Implementation Decisions
2	
3	**Date**: 2026-04-14  
4	**Status**: Accepted  
5	**Related**: `transform-adr.md` (D0 — design), `transform-props-mapping-adr.md` (property decisions — D6/D7/D8 moved there), `mocho/notes/alignment-ddbedm-mocho-adr.md`
6	
7	---
8	
9	## Context
10	
11	This document records implementation decisions for `transform_edm_to_mocho.py`,
12	the reference DDB-EDM JSONL → mocho RDF transform. Dispatch architecture and
13	signal priority are decided in `transform-adr.md` (D0); the decisions here
14	govern how those design choices are realised in code.
15	
16	---
17	
18	## Decision 1: Use JSONL as input, not the NT file
19	
20	**Decision**: Stream `items-all-goethe-faust.json` (JSONL, one JSON object per
```

---

### Assistant *(2026-05-13T13:59:05.898Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"^## Decision 28\" /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "description": "Find Decision 28 line number"
}
```

---

### User *(2026-05-13T13:59:05.985Z)*

**Tool result**
```
607:## Decision 28: Post-processing NQ split → per-graph NT files
```

---

### Assistant *(2026-05-13T13:59:08.453Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "offset": 607
}
```

---

### User *(2026-05-13T13:59:08.460Z)*

**Tool result**
```
607	## Decision 28: Post-processing NQ split → per-graph NT files
608	
609	**Decision**: The transform emits `.nq` output unchanged (D22). Immediately after the transform, a post-processing step (`scripts/split_nq.py`) splits each `.nq` file into one `.nt` file per named graph. The `.nt` files are the working intermediates for sanitization, validation, and debugging. NQ wrapping is deferred to QLever load time.
610	
611	File naming: the output `.nt` slug matches the graph name (e.g. `ddbedm.nt`, `mocho.nt`, `prov.nt`); the load-time wrapper derives the full graph IRI mechanically (`…/graph/<slug>`).
612	
613	**Rationale**:
614	1. **NT is simpler to sanitize**: no graph column; grep/awk/sed operate directly on `<subject> <predicate> <object> .` lines without stripping the fourth element first.
615	2. **Late-binding graph IRI**: renaming a named graph (e.g. schema-breaking release, IRI migration) requires changing only the load-time wrapper — not the `.nt` files.
616	3. **No generator change**: the transform already routes triples to per-graph output streams (D20, D22). Post-processing the `.nq` output is a small script; the generator is not touched.
617	
618	**Post-processing script** (`scripts/split_nq.py`):
619	
620	```python
621	from collections import defaultdict
622	from pathlib import Path
623	
624	def split_nq(nq_path: Path, out_dir: Path):
625	    graphs: dict[str, list[str]] = defaultdict(list)
626	    with open(nq_path) as f:
627	        for line in f:
628	            parts = line.rstrip(" .\n").rsplit(" ", 1)
629	            graphs[parts[1]].append(parts[0] + " .\n")
630	    for graph_iri, triples in graphs.items():
631	        slug = graph_iri.strip("<>").split("/")[-1]
632	        (out_dir / f"{slug}.nt").write_text("".join(triples))
633	```
634	
635	**Amends D22** on the file format question only: D22 governs the generator (NQ output, graph IRI on every emitted line). This decision governs what happens to the `.nq` files after generation; D22 remains in effect for the transform itself.
636	
637	---
638	
639	## Decision 14: Manual curation over automated schema alignment
640	
641	**Decision**: The alignment table (`alignment_ddbedm_mocho.csv`) and all dispatch
642	logic (htype lookup, dc:type × sector dispatch, sparte × mediatype class
643	assignment) were produced by manual curation and explicit decision records (D1–D13),
644	not by automated schema-matching algorithms [Rahm & Bernstein 2001; Shvaiko &
645	Euzenat 2013].
646	
647	**Alternatives considered**:
648	
649	- *LLM-assisted alignment* [Hertling & Paulheim 2023; Giglou et al. 2023]: Feed
650	  source JSON keys + sample values + target ontology namespace documentation to an
651	  LLM and generate `(entity_type, json_key) → predicate IRI` candidate mappings.
652	  Would have covered approximately 60–70% of the 1:1 property mappings in
653	  `alignment_ddbedm_mocho.csv` automatically — cases with clear semantic
654	  correspondences (`prefLabel → skos:prefLabel`, `lat → geo:lat`, `begin →
655	  schema:startDate`). Cannot produce the conditional class dispatch logic (htype ×
656	  sparte × mediatype → rdf:type) without domain knowledge of DDB's institutional
657	  structure and the mocho WEMI model. Useful for bootstrap; insufficient for the
658	  semantically significant part of the alignment.
659	
660	- *Instance-based statistical alignment* [Doan et al. 2002; Madhavan et al. 2001]:
661	  Analyze value distributions per JSON key — IRI vs literal, date format patterns,
662	  language tags, value overlap with target ontology IRIs — to narrow predicate
663	  candidates automatically. Good at datatype inference and distinguishing
664	  IRI-valued from literal-valued properties. Cannot distinguish semantically close
665	  predicates that share the same datatype (e.g. `rdaa:P50067` date-of-birth vs
666	  `rdaa:P50068` date-of-death both accept date literals; `rdaw:P10088` vs
667	  `rico:includesOrIncluded` both accept IRI objects). Requires a human to resolve
668	  ambiguities among ranked candidates.
669	
670	- *Rule induction over labeled examples* [Quinlan 1993; Völker & Niepert 2011]:
671	  Treat the lookup tables as labeled training data and learn the dispatch rules
672	  (e.g. sparte002 × mt003 × htype → `rdac:C10001 + rdac:C10007`) via a decision
673	  tree or rule-induction algorithm. Could rediscover the rules already encoded in
674	  `lookup_htype_doco_rico.csv`, and might surface
675	  coverage gaps or inconsistencies not noticed during manual construction. Not
676	  applicable before the tables exist; the tables are the training data. Value is
677	  in post-hoc validation, not in generating the alignment.
678	
679	**Rationale**: All three automated approaches share a structural precondition
680	that does not hold here: they assume the target ontology is fixed and complete
681	before alignment begins [Euzenat & Shvaiko 2013, ch. 2]. mocho is being
682	co-developed alongside the transformation. New classes (`mocho:ImageWork`,
683	`mocho:ImmovableWork`, `mocho:ImageObject`) and new properties (`mocho:facsimile`)
684	were introduced *in response to* patterns discovered in the DDB corpus during
685	alignment work — the data drives ontology design, not the reverse. An automated
686	aligner given an incomplete mocho would produce mappings against a moving target,
687	with no mechanism to signal when the ontology gap itself is the correct resolution
688	(rather than a nearest-available substitute).
689	
690	Beyond this precondition failure, the alignment problem has two sub-problems with
691	different automation profiles even in a stable-ontology scenario. For 1:1 property
692	mapping (JSON key → predicate IRI), automated approaches are viable and would have
693	reduced manual effort for the whitelist tables. For conditional class dispatch
694	(multi-signal decision trees over sector, mediatype, htype, and dc:type), the
695	rules encode institutional domain knowledge — what it means for a DDB Library
696	record with htype ht021 (`Monografie`) to be a `rdac:C10001 Work` — that cannot
697	be derived from schema or ontology definitions alone. The semantically significant
698	decisions (D9–D13) all fall in this second category. Automated alignment would
699	have covered the straightforward cases and left the hard ones unsolved.
700	
701	**Consequence**: The alignment table and dispatch tables are authoritative
702	artifacts, not derived files. Any re-run of the upstream alignment script
703	(`align_ddbedm_to_mocho.py`) must not overwrite manual decisions. Patches are
704	applied via `patch_alignment_inmocho.py` (see §5.1 of `transform-revised-plan.md`)
705	and tracked in this ADR.
706	
707	
708	**References** *(verify before citing in paper)*:
709	
710	| Key | Details | Confidence |
711	|---|---|---|
712	| Rahm & Bernstein 2001 | E. Rahm, P.A. Bernstein. "A survey of approaches to automatic schema matching." *VLDB Journal* 10(4):334–350. | High |
713	| Shvaiko & Euzenat 2013 | P. Shvaiko, J. Euzenat. "Ontology matching: State of the art and future challenges." *IEEE TKDE* 25(1):158–176. | High |
714	| Euzenat & Shvaiko 2013 | J. Euzenat, P. Shvaiko. *Ontology Matching* (2nd ed.). Springer. | High — cite ch. 2 for the fixed-target assumption |
715	| Hertling & Paulheim 2023 | S. Hertling, H. Paulheim. "Olala: Ontology Matching with Large Language Models." *Proc. K-CAP 2023*. | Medium — verify venue and title |
716	| Giglou et al. 2023 | H.B. Giglou, J. D'Souza, S. Auer. "LLMs4OL: Large Language Models for Ontology Learning." *ISWC 2023*. | Medium — covers ontology learning, not matching directly; verify fit |
717	| Doan et al. 2002 | A. Doan, J. Madhavan, P. Domingos, A. Halevy. "Learning to map between ontologies on the Semantic Web." *WWW 2002*. | High — instance-based learning for ontology mapping |
718	| Madhavan et al. 2001 | J. Madhavan, P.A. Bernstein, E. Rahm. "Generic schema matching with Cupid." *VLDB 2001*. | High — statistical/structural schema matching |
719	| Quinlan 1993 | J.R. Quinlan. *C4.5: Programs for Machine Learning*. Morgan Kaufmann. | High — decision tree rule induction |
720	| Völker & Niepert 2011 | J. Völker, M. Niepert. "Statistical schema induction." *ESWC 2011*. | Medium — verify this covers ontology rule learning specifically |
721	
```

---

### Assistant *(2026-05-13T14:00:12.816Z)*

Now I have everything. Implementing all changes across 6 files.

---

### Assistant *(2026-05-13T14:00:12.827Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "\"\"\"Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, and werk_staging.\"\"\"",
  "new_string": "\"\"\"Triple emitters: ddbedm passthrough, mocho alignment, PROV-O, werk_staging, and cross-run shared-entity deduplication.\"\"\""
}
```

---

### User *(2026-05-13T14:08:32.458Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.
```

---

### User *(2026-05-13T14:08:32.460Z)*

[Request interrupted by user for tool use]

---

### User *(2026-05-13T14:08:46.092Z)*

did you also plan the test and fixtures?

---

### Assistant *(2026-05-13T14:09:14.605Z)*

No, tests and fixtures were not in the plan. They should be. Based on the pattern from §7–§10 of `transform-implementation-actual.md`, here's what's needed:

---

## Test additions to add to the plan

### Unit tests — `test_transform.py`

**`TestEmitProvTriplesDedup`**

| Test | Assertion |
|---|---|
| `test_xslt_skipped_when_emitted` | `xslt_uri` already in `emitted` → 0 XSLT descriptive triples (`rdf:type`, `dcterms:hasVersion`, `prov:actedOnBehalfOf`) emitted |
| `test_ddb_agent_skipped_when_emitted` | `DDB_BASE` already in `emitted` → 0 DDB Agent triples emitted |
| `test_provider_skipped_when_emitted` | `prov_uri` already in `emitted` → 0 Provider descriptive triples emitted |
| `test_dataset_skipped_when_emitted` | `ds_uri` already in `emitted` → 0 Dataset descriptive triples emitted |
| `test_cho_linking_always_emitted` | All four in `emitted` → per-CHO triples (`prov:wasAttributedTo`, `prov:wasDerivedFrom`, `prov:generatedAtTime`) still present |
| `test_emitted_none_emits_all` | `emitted=None` → all shared-node triples present (backward-compatible) |
| `test_emitted_dict_populated` | Fresh `emitted={}` → after call, dict contains `xslt_uri`, `DDB_BASE`, `prov_uri`, `ds_uri` with correct `entity_type` values |

**`TestEmitDdbedmTriplesDedup`**

| Test | Assertion |
|---|---|
| `test_agent_skipped_when_emitted` | Agent `about` URI already in `emitted` → no triples for that agent URI |
| `test_place_skipped_when_emitted` | Same for `edm:Place` |
| `test_concept_skipped_when_emitted` | Same for `skos:Concept` |
| `test_timespan_skipped_when_emitted` | Same for `edm:TimeSpan` |
| `test_providedcho_never_skipped` | `ProvidedCHO` about URI in `emitted` → CHO triples still emitted (not in `_DEDUP_ENTITY_TYPES`) |
| `test_second_record_shares_agent` | Two records with same agent URI, shared `emitted` dict → agent triples appear exactly once across both calls |
| `test_emitted_dict_populated_with_type` | After call, agent URI in dict with `entity_type == "edm_agent"` |

### Fixtures

No new corpus fixture files needed. The unit tests can use minimal synthetic dicts (same pattern as existing `TestEmitCreatorTriples*` tests). The `second_record_shares_agent` test constructs two minimal `rdf` dicts with the same `Agent.about` value.

---

Should I add this to the plan and proceed with implementation?

---

### User *(2026-05-13T14:09:25.652Z)*

yes

---

### Assistant *(2026-05-13T14:10:21.336Z)*

Implementing all changes now — code first, then notes, then tests.

---

### Assistant *(2026-05-13T14:10:23.445Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "from .utils import (\n    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,\n    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,\n    build_bare_id_index, expand_obj_nt, resource_uris,\n)\n\n\ndef emit_ddbedm_triples(",
  "new_string": "from .utils import (\n    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,\n    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,\n    build_bare_id_index, expand_obj_nt, resource_uris,\n)\n\n# Entity types whose descriptive triples are deduplicated across records/runs via the\n# emitted dict (uri → entity_type).  ProvidedCHO, Aggregation, WebResource are excluded\n# — they are unique per record.\n_DEDUP_ENTITY_TYPES: dict[str, str] = {\n    \"Agent\":    \"edm_agent\",\n    \"Place\":    \"edm_place\",\n    \"Concept\":  \"skos_concept\",\n    \"TimeSpan\": \"edm_timespan\",\n}\n\n\ndef emit_ddbedm_triples("
}
```

---

### User *(2026-05-13T14:10:28.295Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:10:33.135Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "def emit_ddbedm_triples(\n    rdf: dict,\n    graph_iri: str,\n    lang_coll: set[str] | None = None,\n) -> tuple[NQList, Counter, Counter, Counter]:",
  "new_string": "def emit_ddbedm_triples(\n    rdf: dict,\n    graph_iri: str,\n    lang_coll: set[str] | None = None,\n    emitted: dict[str, str] | None = None,\n) -> tuple[NQList, Counter, Counter, Counter]:"
}
```

---

### User *(2026-05-13T14:10:40.305Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:10:45.738Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))\n        subj_nt  = f\"<{subj_uri}>\"\n        if len(about_parts) > 1:",
  "new_string": "        subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))\n        subj_nt  = f\"<{subj_uri}>\"\n        if emitted is not None and entity_type in _DEDUP_ENTITY_TYPES:\n            if subj_uri in emitted:\n                continue\n            emitted[subj_uri] = _DEDUP_ENTITY_TYPES[entity_type]\n        if len(about_parts) > 1:"
}
```

---

### User *(2026-05-13T14:10:45.739Z)*

**Tool result** *(error)*
```
<tool_use_error>String to replace not found in file.
String:         subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
        subj_nt  = f"<{subj_uri}>"
        if len(about_parts) > 1:</tool_use_error>
```

---

### Assistant *(2026-05-13T14:10:48.527Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 68,
  "limit": 15
}
```

---

### User *(2026-05-13T14:10:48.537Z)*

**Tool result**
```
68	            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
69	            subj_nt  = f"<{subj_uri}>"
70	            if len(about_parts) > 1:
71	                sani_ctr["uri_about_split"] += len(about_parts) - 1
72	                for alt in about_parts[1:]:
73	                    lines.append(make_nq(subj_nt, f"<{OWL_SAMEAS}>",
74	                                         f"<{_sanitize_iri(alt)}>", graph_iri))
75	            if edm_class:
76	                lines.append(make_nq(subj_nt, f"<{RDF_TYPE}>", f"<{edm_class}>", graph_iri))
77	                class_ctr[_to_curie(edm_class)] += 1
78	            for key, val in entity.items():
79	                if key in _skip:
80	                    continue
81	                pred_iri = _DDBEDM_PROP.get(key)
82	                if not pred_iri:
```

---

### Assistant *(2026-05-13T14:10:52.399Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))\n            subj_nt  = f\"<{subj_uri}>\"\n            if len(about_parts) > 1:",
  "new_string": "            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))\n            subj_nt  = f\"<{subj_uri}>\"\n            if emitted is not None and entity_type in _DEDUP_ENTITY_TYPES:\n                if subj_uri in emitted:\n                    continue\n                emitted[subj_uri] = _DEDUP_ENTITY_TYPES[entity_type]\n            if len(about_parts) > 1:"
}
```

---

### User *(2026-05-13T14:11:19.494Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:11:23.207Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:",
  "new_string": "def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str, emitted: dict[str, str] | None = None) -> NQList:"
}
```

---

### User *(2026-05-13T14:11:26.541Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:11:30.521Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    # ── Dataset node ──────────────────────────────────────────────────────────────\n    if ds_uri:\n        ds_nt = f\"<{ds_uri}>\"",
  "new_string": "    # ── Dataset node ──────────────────────────────────────────────────────────────\n    if ds_uri and (emitted is None or ds_uri not in emitted):\n        if emitted is not None:\n            emitted[ds_uri] = \"prov_dataset\"\n        ds_nt = f\"<{ds_uri}>\""
}
```

---

### User *(2026-05-13T14:11:30.522Z)*

**Tool result** *(error)*
```
<tool_use_error>String to replace not found in file.
String:     # ── Dataset node ──────────────────────────────────────────────────────────────
    if ds_uri:
        ds_nt = f"<{ds_uri}>"
(note: Edit also tried swapping \uXXXX escapes and their characters; neither form matched, so the mismatch is likely elsewhere in old_string. Re-read the file and copy the exact surrounding text.)</tool_use_error>
```

---

### Assistant *(2026-05-13T14:11:33.252Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 138,
  "limit": 20
}
```

---

### User *(2026-05-13T14:11:33.260Z)*

**Tool result**
```
138	                             f'"{_escape_literal(revision)}"', graph_iri))
139	    if ref_val:
140	        lines.append(make_nq(cho_nt, f"<{DCTERMS_REF}>",
141	                             f'"ddb:{_escape_literal(ref_val)}"', graph_iri))
142	
143	    # ── Dataset node ──────────────────────────────────────────────────────────
144	    if ds_uri:
145	        ds_nt = f"<{ds_uri}>"
146	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{DCAT_DATASET}>", graph_iri))
147	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
148	        lines.append(make_nq(ds_nt, f"<{DCTERMS_ID}>",
149	                             f'"{_escape_literal(dataset_id)}"', graph_iri))
150	        if dataset_label:
151	            lines.append(make_nq(ds_nt, f"<{RDFS_LABEL}>",
152	                                 f'"{_escape_literal(dataset_label)}"@de', graph_iri))
153	        if rec_type:
154	            lines.append(make_nq(ds_nt, f"<{DCTERMS_TYPE}>", f"<{rec_type}>", graph_iri))
155	        if prov_uri:
156	            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
157	                                 f"<{prov_uri}>", graph_iri))
```

---

### Assistant *(2026-05-13T14:11:37.505Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    # ── Dataset node ──────────────────────────────────────────────────────────\n    if ds_uri:\n        ds_nt = f\"<{ds_uri}>\"",
  "new_string": "    # ── Dataset node ──────────────────────────────────────────────────────────\n    if ds_uri and (emitted is None or ds_uri not in emitted):\n        if emitted is not None:\n            emitted[ds_uri] = \"prov_dataset\"\n        ds_nt = f\"<{ds_uri}>\""
}
```

---

### User *(2026-05-13T14:12:12.331Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:12:14.638Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 158,
  "limit": 20
}
```

---

### User *(2026-05-13T14:12:14.645Z)*

**Tool result**
```
158	            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
159	                                 f"<{prov_uri}>", graph_iri))
160	
161	    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────
162	    if xslt_uri:
163	        xslt_nt = f"<{xslt_uri}>"
164	        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
165	        lines.append(make_nq(xslt_nt, f"<{DCTERMS_HAS_VER}>",
166	                             f'"{_escape_literal(map_ver)}"', graph_iri))
167	        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
168	
169	    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────
170	    ddb_nt = f"<{DDB_BASE}>"
171	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
172	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
173	    lines.append(make_nq(ddb_nt, f"<{FOAF_NAME}>",
174	                         '"Deutsche Digitale Bibliothek"', graph_iri))
175	
176	    # ── Provider Agent node ───────────────────────────────────────────────────
177	    if prov_uri:
```

---

### Assistant *(2026-05-13T14:12:23.251Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────\n    if xslt_uri:\n        xslt_nt = f\"<{xslt_uri}>\"\n        lines.append(make_nq(xslt_nt, f\"<{RDF_TYPE}>\", f\"<{PROV_SW_AGENT}>\", graph_iri))\n        lines.append(make_nq(xslt_nt, f\"<{DCTERMS_HAS_VER}>\",\n                             f'\"{_escape_literal(map_ver)}\"', graph_iri))\n        lines.append(make_nq(xslt_nt, f\"<{PROV_ON_BEHALF}>\", f\"<{DDB_BASE}>\", graph_iri))\n\n    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────\n    ddb_nt = f\"<{DDB_BASE}>\"\n    lines.append(make_nq(ddb_nt, f\"<{RDF_TYPE}>\", f\"<{PROV_AGENT}>\", graph_iri))\n    lines.append(make_nq(ddb_nt, f\"<{RDF_TYPE}>\", f\"<{FOAF_ORG}>\",   graph_iri))\n    lines.append(make_nq(ddb_nt, f\"<{FOAF_NAME}>\",\n                         '\"Deutsche Digitale Bibliothek\"', graph_iri))\n\n    # ── Provider Agent node ───────────────────────────────────────────────────\n    if prov_uri:",
  "new_string": "    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────\n    if xslt_uri and (emitted is None or xslt_uri not in emitted):\n        if emitted is not None:\n            emitted[xslt_uri] = \"prov_xslt\"\n        xslt_nt = f\"<{xslt_uri}>\"\n        lines.append(make_nq(xslt_nt, f\"<{RDF_TYPE}>\", f\"<{PROV_SW_AGENT}>\", graph_iri))\n        lines.append(make_nq(xslt_nt, f\"<{DCTERMS_HAS_VER}>\",\n                             f'\"{_escape_literal(map_ver)}\"', graph_iri))\n        lines.append(make_nq(xslt_nt, f\"<{PROV_ON_BEHALF}>\", f\"<{DDB_BASE}>\", graph_iri))\n\n    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────\n    if emitted is None or DDB_BASE not in emitted:\n        if emitted is not None:\n            emitted[DDB_BASE] = \"prov_ddb\"\n        ddb_nt = f\"<{DDB_BASE}>\"\n        lines.append(make_nq(ddb_nt, f\"<{RDF_TYPE}>\", f\"<{PROV_AGENT}>\", graph_iri))\n        lines.append(make_nq(ddb_nt, f\"<{RDF_TYPE}>\", f\"<{FOAF_ORG}>\",   graph_iri))\n        lines.append(make_nq(ddb_nt, f\"<{FOAF_NAME}>\",\n                             '\"Deutsche Digitale Bibliothek\"', graph_iri))\n\n    # ── Provider Agent node ───────────────────────────────────────────────────\n    if prov_uri and (emitted is None or prov_uri not in emitted):"
}
```

---

### User *(2026-05-13T14:12:27.056Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:12:33.530Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 185,
  "limit": 15
}
```

---

### User *(2026-05-13T14:12:33.535Z)*

**Tool result**
```
185	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
186	        if provider_name:
187	            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
188	                                 f'"{_escape_literal(provider_name)}"', graph_iri))
189	        if provider_uri:
190	            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
191	        if provider_id:
192	            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
193	                                 f'"{_escape_literal(provider_id)}"', graph_iri))
194	        if provider_isil:
195	            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>",
196	                                 f"<{_sanitize_iri(provider_isil)}>", graph_iri))
197	
198	    # ── SourceRecord node (one per binary entry under same URI) ───────────────
199	    if src_href:
```

---

### Assistant *(2026-05-13T14:12:36.198Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "offset": 179,
  "limit": 8
}
```

---

### User *(2026-05-13T14:12:36.206Z)*

**Tool result**
```
179	                             '"Deutsche Digitale Bibliothek"', graph_iri))
180	
181	    # ── Provider Agent node ───────────────────────────────────────────────────
182	    if prov_uri and (emitted is None or prov_uri not in emitted):
183	        prov_nt = f"<{prov_uri}>"
184	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
185	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
186	        if provider_name:
```

---

### Assistant *(2026-05-13T14:12:39.606Z)*

I need to add the `emitted[prov_uri] = "prov_provider"` guard inside the provider block:

---

### Assistant *(2026-05-13T14:12:41.176Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    # ── Provider Agent node ───────────────────────────────────────────────────\n    if prov_uri and (emitted is None or prov_uri not in emitted):\n        prov_nt = f\"<{prov_uri}>\"",
  "new_string": "    # ── Provider Agent node ───────────────────────────────────────────────────\n    if prov_uri and (emitted is None or prov_uri not in emitted):\n        if emitted is not None:\n            emitted[prov_uri] = \"prov_provider\"\n        prov_nt = f\"<{prov_uri}>\""
}
```

---

### User *(2026-05-13T14:12:43.976Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:12:46.423Z)*

Now `transform.py`:

---

### Assistant *(2026-05-13T14:12:49.828Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py",
  "old_string": "def transform_record(\n    record: dict,\n    ids_set: set[str] | None,\n    mediatype_class_map: dict,\n    htype_map: dict,\n    audio_type2class: dict,\n    class_prop_align: PropAlign,\n    lido_dispatch: dict,\n) -> tuple[dict[str, NQList], dict | None, dict, dict]:",
  "new_string": "def transform_record(\n    record: dict,\n    ids_set: set[str] | None,\n    mediatype_class_map: dict,\n    htype_map: dict,\n    audio_type2class: dict,\n    class_prop_align: PropAlign,\n    lido_dispatch: dict,\n    emitted_entities: dict[str, str] | None = None,\n) -> tuple[dict[str, NQList], dict | None, dict, dict]:"
}
```

---

### User *(2026-05-13T14:12:52.775Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:12:58.309Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py",
  "old_string": "    ddbedm_lines, ddbedm_classes, ddbedm_preds, ddbedm_sani = emit_ddbedm_triples(\n        rdf, GRAPH_DDBEDM, lang_coll,\n    )\n    streams[\"ddbedm\"] = ddbedm_lines\n    streams[\"prov\"]   = emit_prov_triples(record, ddb_uri, GRAPH_PROV)",
  "new_string": "    ddbedm_lines, ddbedm_classes, ddbedm_preds, ddbedm_sani = emit_ddbedm_triples(\n        rdf, GRAPH_DDBEDM, lang_coll, emitted=emitted_entities,\n    )\n    streams[\"ddbedm\"] = ddbedm_lines\n    streams[\"prov\"]   = emit_prov_triples(record, ddb_uri, GRAPH_PROV, emitted=emitted_entities)"
}
```

---

### User *(2026-05-13T14:13:49.737Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:13:55.685Z)*

Now `__main__.py` — four sequential edits:

---

### Assistant *(2026-05-13T14:14:00.219Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py",
  "old_string": "    io.add_argument(\"--stem\", type=str, default=None,\n                    help=\"Output filename stem (overrides the input filename); \"\n                         \"e.g. --stem items-all-goethe-faust → items-all-goethe-faust.nq, etc.\")",
  "new_string": "    io.add_argument(\"--stem\", type=str, default=None,\n                    help=\"Output filename stem (overrides the input filename); \"\n                         \"e.g. --stem items-all-goethe-faust → items-all-goethe-faust.nq, etc.\")\n    io.add_argument(\"--entities-db\", type=Path, default=None,\n                    dest=\"entities_db\",\n                    help=\"Shared cross-run entity-dedup DuckDB; created if absent. \"\n                         \"Stores URIs of already-emitted shared nodes (PROV-O, \"\n                         \"edm:Agent, edm:Place, skos:Concept, edm:TimeSpan). \"\n                         \"Omit for within-run dedup only (no persistence).\")"
}
```

---

### User *(2026-05-13T14:14:12.912Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:14:18.851Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py",
  "old_string": "    stats_level = args.stats",
  "new_string": "    emitted_entities: dict[str, str] = {}\n    entities_conn = None\n    if args.entities_db:\n        try:\n            import duckdb as _ddb_ent\n            entities_conn = _ddb_ent.connect(str(args.entities_db))\n            entities_conn.execute(\"\"\"\n                CREATE TABLE IF NOT EXISTS emitted_entities (\n                    uri         VARCHAR PRIMARY KEY,\n                    entity_type VARCHAR NOT NULL\n                )\n            \"\"\")\n            rows = entities_conn.execute(\n                \"SELECT uri, entity_type FROM emitted_entities\"\n            ).fetchall()\n            emitted_entities = {uri: etype for uri, etype in rows}\n            log.info(\"Loaded %d emitted entities from %s\",\n                     len(emitted_entities), args.entities_db)\n        except ImportError:\n            log.warning(\"duckdb not available — --entities-db ignored\")\n        except Exception as exc:\n            log.warning(\"Could not open --entities-db %s: %s\", args.entities_db, exc)\n\n    stats_level = args.stats"
}
```

---

### User *(2026-05-13T14:14:22.863Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:14:28.768Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py",
  "old_string": "                streams, werk_row, dispatch_info, pred_info = transform_record(\n                    record, ids_set,\n                    mediatype_class_map, htype_map, audio_type2class,\n                    class_prop_align, lido_dispatch,\n                )",
  "new_string": "                streams, werk_row, dispatch_info, pred_info = transform_record(\n                    record, ids_set,\n                    mediatype_class_map, htype_map, audio_type2class,\n                    class_prop_align, lido_dispatch,\n                    emitted_entities=emitted_entities,\n                )"
}
```

---

### User *(2026-05-13T14:17:50.333Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:17:55.865Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py",
  "old_string": "    if conn is not None:\n        conn.close()",
  "new_string": "    if entities_conn is not None:\n        entities_conn.executemany(\n            \"INSERT OR IGNORE INTO emitted_entities VALUES (?, ?)\",\n            list(emitted_entities.items()),\n        )\n        entities_conn.close()\n        log.info(\"Wrote %d entities to %s\", len(emitted_entities), args.entities_db)\n\n    if conn is not None:\n        conn.close()"
}
```

---

### User *(2026-05-13T14:17:59.726Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:18:02.442Z)*

Now the three notes files in parallel:

---

### Assistant *(2026-05-13T14:18:09.495Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "old_string": "**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key\nchain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without\nrequiring a dereferenceable endpoint.",
  "new_string": "**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key\nchain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without\nrequiring a dereferenceable endpoint.\n\n**Shared node deduplication**: The four shared nodes (Dataset, XSLT, DDB Agent, Provider) have stable URIs that recur across records and sector files. Their descriptive triples are emitted only on first encounter per run via an `emitted: dict[str, str]` guard in `emit_prov_triples`. With `--entities-db`, the dict is persisted to DuckDB across runs; without it, deduplication is within-run only. The per-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted. The XSLT URI is derived from the version number (`urn:ddbedm:properties:mapping-version:{ver}`), so the version number is the effective lookup key at the code level."
}
```

---

### User *(2026-05-13T14:21:13.119Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:21:30.396Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "old_string": "## Decision 14: Manual curation over automated schema alignment",
  "new_string": "## Decision 29: DuckDB-backed cross-run shared-entity deduplication\n\n**Decision**: Descriptive triples for shared named entities are emitted at most once per URI across all transform runs, tracked via a persistent DuckDB table (`emitted_entities`).\n\n**Entity types deduplicated**:\n\n| entity_type value | Source | Scope of sharing |\n|---|---|---|\n| `prov_xslt` | `properties.mapping-version` → XSLT URI | All records with same mapping version |\n| `prov_ddb` | `DDB_BASE` (fixed) | Every record in every run |\n| `prov_provider` | `provider-info.provider-ddb-id` → Provider URI | All records from same institution |\n| `prov_dataset` | `properties.dataset-id` → Dataset URI | All records in same delivery batch |\n| `edm_agent` | `edm.RDF.Agent[].about` | GND agent URIs shared across records |\n| `edm_place` | `edm.RDF.Place[].about` | GND place URIs shared across records |\n| `skos_concept` | `edm.RDF.Concept[].about` | Subject concept URIs shared across records |\n| `edm_timespan` | `edm.RDF.TimeSpan[].about` | Time period URIs shared across records |\n\n**Schema** (single shared DuckDB file, not per-run):\n```sql\nCREATE TABLE IF NOT EXISTS emitted_entities (\n    uri         VARCHAR PRIMARY KEY,\n    entity_type VARCHAR NOT NULL\n)\n```\n\n**Runtime pattern**: at startup, load all rows into an in-memory `dict[str, str]` (`uri → entity_type`); check membership during processing; after the loop, `INSERT OR IGNORE` all entries back (idempotent, handles pre-existing rows).\n\n**Why not a per-record DuckDB lookup**: the number of unique shared-entity URIs is small (tens to low thousands). Loading into memory at startup is O(1) per record; a DuckDB round-trip per record would add I/O overhead at 18.5M scale.\n\n**Why not in-memory set only**: the transform is run once per sector file (s1–s7) as separate OS processes. An in-memory set resets between runs, so DDB Agent and XSLT triples would be re-emitted in every sector's output. The DuckDB file survives across runs.\n\n**`--entities-db` is optional**: if omitted, a fresh empty `dict` is used — within-run dedup only, no persistence. The `emitted` parameter defaults to `None` in both `emit_prov_triples` and `emit_ddbedm_triples`, which falls back to always-emit (backward-compatible for tests and other callers).\n\n**Per-CHO triples are never deduplicated**: linking triples from the CHO to shared nodes (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are unique per record and emitted unconditionally.\n\n---\n\n## Decision 14: Manual curation over automated schema alignment"
}
```

---

### User *(2026-05-13T14:24:19.874Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T14:24:22.737Z)*

Now the tests. Let me check the existing test file structure first:

---

### Assistant *(2026-05-13T14:24:23.888Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"^class Test\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py | tail -20",
  "description": "List test classes to find where to append new ones"
}
```

---

### User *(2026-05-13T14:24:23.985Z)*

**Tool result**
```
600:class TestEmitHastypeTriples:
651:class TestEscapeLiteralBr:
673:class TestResourceUris:
713:class TestEmitSubjectTriplesMultiUri:
739:class TestEmitHastypeTriplesMultiUri:
757:class TestEmitCreatorTriplesMultiUri:
770:class TestEmitCreatorTriplesBareId:
800:class TestEmitContributorTriplesMultiUri:
810:class TestEmitContributorTriplesBareId:
825:class TestEmitCreatorTriplesPrefLabel:
866:class TestEmitContributorTriplesAgentLabel:
914:class TestEmitProvTriplesIsil:
932:class TestEmitPlaceStubsSplitAbout:
953:class TestEmitAggregationSplitUri:
981:class TestEmitCurrentLocationTriples:
1060:class TestFixtures:
1097:class TestEmitMochoMediaTypeSector:
1136:class TestIanaCollectionCodes:
1148:class TestInvalidBcp47:
1161:class TestValueToNtObjLangNorm:
```

---

### Assistant *(2026-05-13T14:24:24.131Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "description": "Get total line count of test file"
}
```

---

### User *(2026-05-13T14:24:24.190Z)*

**Tool result**
```
    1208 /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py
```

---

### Assistant *(2026-05-13T14:24:26.810Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 1195,
  "limit": 15
}
```

---

### User *(2026-05-13T14:24:26.826Z)*

**Tool result**
```
1195	
1196	    def test_spaced_lang_normalized_to_und(self):
1197	        # "en en" is a DDB data-quality artifact (two URIs in about → two lang attrs joined)
1198	        result = value_to_nt_obj({"$": "Multivolume work Volume", "lang": "en en"})
1199	        assert result == ['"Multivolume work Volume"@und']
1200	
1201	    def test_spaced_lang_not_added_to_lang_coll(self):
1202	        coll: set[str] = set()
1203	        value_to_nt_obj({"$": "Multivolume work Volume", "lang": "en en"}, lang_coll=coll)
1204	        assert coll == set()
1205	
1206	    def test_leading_trailing_whitespace_stripped(self):
1207	        result = value_to_nt_obj({"$": "Faust", "lang": " ger "})
1208	        assert result == ['"Faust"@ger']
1209	
```

---

### Assistant *(2026-05-13T14:24:27.374Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 1,
  "limit": 30
}
```

---

### User *(2026-05-13T14:24:27.382Z)*

**Tool result**
```
1	"""
2	Purpose:    Unit tests for the transform package.
3	Usage:      pytest scripts/transform/tests/ -q
4	Deps:       pytest
5	Assumes:    Run from project root (goethe-faust/).
6	"""
7	
8	from __future__ import annotations
9	
10	import sys
11	from pathlib import Path
12	
13	import pytest
14	
15	# ── Package import ────────────────────────────────────────────────────────────
16	sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # adds scripts/ to sys.path
17	
18	from transform.constants import GRAPH_MOCHO, MOCHO_NS, PROJECT_DIR
19	from transform.utils import (
20	    coerce_list,
21	    make_nq,
22	    mint_bare_id,
23	    mint_cho_uri,
24	    normalize_date,
25	    value_to_nt_obj,
26	    _escape_literal,
27	    get_object_id,
28	    build_bare_id_index,
29	    expand_obj_nt,
30	    resource_uris,
```

---

### Assistant *(2026-05-13T14:24:30.055Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 30,
  "limit": 25
}
```

---

### User *(2026-05-13T14:24:30.062Z)*

**Tool result**
```
30	    resource_uris,
31	)
32	from transform.emitters import (
33	    retype_entities,
34	    emit_creator_triples,
35	    emit_contributor_triples,
36	    emit_subject_triples,
37	    emit_hastype_triples,
38	    emit_current_location_triples,
39	    emit_aggregation_triples,
40	    emit_place_stubs,
41	    werk_staging_row,
42	    emit_ddbedm_triples,
43	    emit_mocho_triples,
44	)
45	from transform.constants import (
46	    _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE, EDM_NS,
47	)
48	from transform.transform import transform_record
49	from transform.loaders import load_mediatype_class, load_htype_map
50	
51	# Config table paths
52	_CONFIG = PROJECT_DIR / "output" / "config"
53	
54	
```

---

### Assistant *(2026-05-13T14:25:16.024Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"def mint_bare_id\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py",
  "description": "Find mint_bare_id definition"
}
```

---

### User *(2026-05-13T14:25:16.073Z)*

**Tool result**
```
65:def mint_bare_id(entity_class: str, raw_id: str) -> str:
```

---

### Assistant *(2026-05-13T14:25:19.773Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py",
  "offset": 65,
  "limit": 20
}
```

---

### User *(2026-05-13T14:25:19.781Z)*

**Tool result**
```
65	def mint_bare_id(entity_class: str, raw_id: str) -> str:
66	    """Expand a bare 32-char ID to a full URI (D27).
67	
68	    ProvidedCHO bare IDs → DDB item URI.
69	    All other entity types → urn:ddbedm:<id>.
70	    Full URIs and URNs are returned unchanged.
71	    """
72	    if raw_id.startswith(("http", "urn")):
73	        return raw_id
74	    if entity_class == "ProvidedCHO":
75	        return DDB_ITEM_BASE + raw_id
76	    return f"urn:ddbedm:{raw_id}"
77	
78	
79	def _escape_literal(s: str) -> str:
80	    """Escape characters illegal in N-Triples/N-Quads literal content."""
81	    s = _BR_RE.sub('\n', s)
82	    return (s.replace("\\", "\\\\")
83	             .replace('"', '\\"')
84	             .replace("\n", "\\n")
```

---

### Assistant *(2026-05-13T14:25:26.326Z)*

Good — full URIs pass through unchanged. Now I can write the tests precisely. I need to add `emit_prov_triples` and `DDB_BASE` to imports, then append the two test classes:

---

### Assistant *(2026-05-13T14:25:27.890Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_hastype_triples,\n    emit_current_location_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n    emit_mocho_triples,\n)",
  "new_string": "from transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_hastype_triples,\n    emit_current_location_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n    emit_mocho_triples,\n    emit_prov_triples,\n)"
}
```

---

### User *(2026-05-13T16:29:11.857Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:29:18.072Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.constants import (\n    _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE, EDM_NS,\n)",
  "new_string": "from transform.constants import (\n    _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE, EDM_NS, DDB_BASE,\n)"
}
```

---

### User *(2026-05-13T16:30:02.545Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:30:32.738Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "    def test_leading_trailing_whitespace_stripped(self):\n        result = value_to_nt_obj({\"$\": \"Faust\", \"lang\": \" ger \"})\n        assert result == ['\"Faust\"@ger']",
  "new_string": "    def test_leading_trailing_whitespace_stripped(self):\n        result = value_to_nt_obj({\"$\": \"Faust\", \"lang\": \" ger \"})\n        assert result == ['\"Faust\"@ger']\n\n\nclass TestEmitProvTriplesDedup:\n    _RECORD = {\n        \"properties\": {\n            \"item-id\":         \"TESTITEMID00000000000000000000000\",\n            \"dataset-id\":      \"testdataset123\",\n            \"dataset-label\":   \"Test Dataset\",\n            \"revision-id\":     \"1\",\n            \"ingest-date\":     \"2026-01-01T00:00:00+0000\",\n            \"mapping-version\": \"6.18\",\n        },\n        \"provider-info\": {\n            \"provider-ddb-id\": \"PROVIDERID00000000000000000000000\",\n            \"provider-name\":   \"Test Provider\",\n        },\n    }\n    _CHO_URI  = \"http://www.deutsche-digitale-bibliothek.de/item/TESTITEMID00000000000000000000000\"\n    _GRAPH    = \"http://test.example/graph/prov\"\n    _XSLT_URI = \"urn:ddbedm:properties:mapping-version:6.18\"\n    _DS_URI   = \"urn:ddbedm:properties:dataset-id:testdataset123\"\n    _PROV_URI = \"urn:ddbedm:provider-info:provider-ddb-id:PROVIDERID00000000000000000000000\"\n\n    def _subjects(self, lines):\n        return [nq.split(\" \", 1)[0] for nq in lines]\n\n    def test_emitted_none_emits_all(self):\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH, emitted=None)\n        subjs = set(self._subjects(lines))\n        assert f\"<{self._XSLT_URI}>\" in subjs\n        assert f\"<{DDB_BASE}>\"       in subjs\n        assert f\"<{self._DS_URI}>\"   in subjs\n        assert f\"<{self._PROV_URI}>\" in subjs\n\n    def test_emitted_dict_populated(self):\n        emitted: dict[str, str] = {}\n        emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH, emitted=emitted)\n        assert emitted.get(self._XSLT_URI) == \"prov_xslt\"\n        assert emitted.get(DDB_BASE)       == \"prov_ddb\"\n        assert emitted.get(self._DS_URI)   == \"prov_dataset\"\n        assert emitted.get(self._PROV_URI) == \"prov_provider\"\n\n    def test_xslt_skipped_when_emitted(self):\n        lines = emit_prov_triples(\n            self._RECORD, self._CHO_URI, self._GRAPH,\n            emitted={self._XSLT_URI: \"prov_xslt\"},\n        )\n        assert f\"<{self._XSLT_URI}>\" not in self._subjects(lines)\n\n    def test_ddb_agent_skipped_when_emitted(self):\n        lines = emit_prov_triples(\n            self._RECORD, self._CHO_URI, self._GRAPH,\n            emitted={DDB_BASE: \"prov_ddb\"},\n        )\n        assert f\"<{DDB_BASE}>\" not in self._subjects(lines)\n\n    def test_provider_skipped_when_emitted(self):\n        lines = emit_prov_triples(\n            self._RECORD, self._CHO_URI, self._GRAPH,\n            emitted={self._PROV_URI: \"prov_provider\"},\n        )\n        assert f\"<{self._PROV_URI}>\" not in self._subjects(lines)\n\n    def test_dataset_skipped_when_emitted(self):\n        lines = emit_prov_triples(\n            self._RECORD, self._CHO_URI, self._GRAPH,\n            emitted={self._DS_URI: \"prov_dataset\"},\n        )\n        assert f\"<{self._DS_URI}>\" not in self._subjects(lines)\n\n    def test_cho_linking_always_emitted(self):\n        emitted = {\n            self._XSLT_URI: \"prov_xslt\",\n            DDB_BASE:        \"prov_ddb\",\n            self._PROV_URI:  \"prov_provider\",\n            self._DS_URI:    \"prov_dataset\",\n        }\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH, emitted=emitted)\n        cho_nt    = f\"<{self._CHO_URI}>\"\n        cho_lines = [nq for nq in lines if nq.startswith(cho_nt)]\n        predicates = {\n            nq.split(\"> <\", 1)[1].split(\">\", 1)[0]\n            for nq in cho_lines if \"> <\" in nq\n        }\n        assert \"http://www.w3.org/ns/prov#wasDerivedFrom\"  in predicates\n        assert \"http://www.w3.org/ns/prov#wasAttributedTo\" in predicates\n        assert \"http://www.w3.org/ns/prov#generatedAtTime\" in predicates\n\n\nclass TestEmitDdbedmTriplesDedup:\n    _GRAPH = \"http://test.example/graph/ddbedm\"\n\n    def _rdf_with(self, entity_type: str, about: str) -> dict:\n        return {entity_type: {\"about\": about, \"prefLabel\": [{\"$\": \"Test Label\", \"lang\": \"de\"}]}}\n\n    def test_agent_skipped_when_emitted(self):\n        uri     = \"http://d-nb.info/gnd/118540238\"\n        lines, *_ = emit_ddbedm_triples(\n            self._rdf_with(\"Agent\", uri), self._GRAPH,\n            emitted={uri: \"edm_agent\"},\n        )\n        assert not any(f\"<{uri}>\" in nq for nq in lines)\n\n    def test_place_skipped_when_emitted(self):\n        uri     = \"http://d-nb.info/gnd/4044283-4\"\n        lines, *_ = emit_ddbedm_triples(\n            self._rdf_with(\"Place\", uri), self._GRAPH,\n            emitted={uri: \"edm_place\"},\n        )\n        assert not any(f\"<{uri}>\" in nq for nq in lines)\n\n    def test_concept_skipped_when_emitted(self):\n        uri     = \"http://d-nb.info/gnd/4020531-9\"\n        lines, *_ = emit_ddbedm_triples(\n            self._rdf_with(\"Concept\", uri), self._GRAPH,\n            emitted={uri: \"skos_concept\"},\n        )\n        assert not any(f\"<{uri}>\" in nq for nq in lines)\n\n    def test_timespan_skipped_when_emitted(self):\n        uri     = \"http://d-nb.info/gnd/4806547-9\"\n        lines, *_ = emit_ddbedm_triples(\n            self._rdf_with(\"TimeSpan\", uri), self._GRAPH,\n            emitted={uri: \"edm_timespan\"},\n        )\n        assert not any(f\"<{uri}>\" in nq for nq in lines)\n\n    def test_provided_cho_never_skipped(self):\n        cho_uri = \"http://www.deutsche-digitale-bibliothek.de/item/ABCABC\"\n        lines, *_ = emit_ddbedm_triples(\n            {\"ProvidedCHO\": {\"about\": cho_uri}}, self._GRAPH,\n            emitted={cho_uri: \"edm_agent\"},  # present in dict but not a dedup type\n        )\n        assert any(f\"<{cho_uri}>\" in nq for nq in lines)\n\n    def test_emitted_none_emits_all(self):\n        uri     = \"http://d-nb.info/gnd/118540238\"\n        lines, *_ = emit_ddbedm_triples(\n            self._rdf_with(\"Agent\", uri), self._GRAPH, emitted=None,\n        )\n        assert any(f\"<{uri}>\" in nq for nq in lines)\n\n    def test_second_record_shares_agent(self):\n        uri     = \"http://d-nb.info/gnd/118540238\"\n        emitted: dict[str, str] = {}\n        rdf = self._rdf_with(\"Agent\", uri)\n        lines1, *_ = emit_ddbedm_triples(rdf, self._GRAPH, emitted=emitted)\n        lines2, *_ = emit_ddbedm_triples(rdf, self._GRAPH, emitted=emitted)\n        assert len([nq for nq in lines1 if f\"<{uri}>\" in nq]) > 0\n        assert len([nq for nq in lines2 if f\"<{uri}>\" in nq]) == 0\n\n    def test_emitted_dict_populated_with_type(self):\n        uri     = \"http://d-nb.info/gnd/118540238\"\n        emitted: dict[str, str] = {}\n        emit_ddbedm_triples(self._rdf_with(\"Agent\", uri), self._GRAPH, emitted=emitted)\n        assert emitted.get(uri) == \"edm_agent\""
}
```

---

### User *(2026-05-13T16:31:03.530Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:31:06.178Z)*

Now run the tests to verify:

---

### Assistant *(2026-05-13T16:31:09.649Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && python -m pytest scripts/transform/tests/test_transform.py -q --tb=short 2>&1 | tail -30",
  "description": "Run all tests and show results"
}
```

---

### User *(2026-05-13T16:31:10.869Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python: No module named pytest
```

---

### Assistant *(2026-05-13T16:31:14.295Z)*

**Tool call:** `Bash`
```json
{
  "command": "python -m pytest scripts/transform/tests/test_transform.py -q --tb=short 2>&1 | tail -30",
  "description": "Run tests from goethe-faust directory",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-13T16:31:15.348Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python: No module named pytest
```

---

### Assistant *(2026-05-13T16:31:20.716Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust/scripts && python -m pytest transform/tests/test_transform.py -q --tb=short 2>&1 | tail -35",
  "description": "Run tests from scripts directory",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-13T16:31:21.688Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python: No module named pytest
```

---

### Assistant *(2026-05-13T16:31:26.111Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/goethe-faust -name \"*.venv\" -o -name \".venv\" -type d 2>/dev/null | head -5; find /Users/mta -name \"pytest\" -type f 2>/dev/null | head -5",
  "description": "Find project venv and pytest",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-13T16:31:36.364Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/.venv
```

---

### Assistant *(2026-05-13T16:31:39.435Z)*

**Tool call:** `Bash`
```json
{
  "command": "/Users/mta/Documents/claude/goethe-faust/.venv/bin/python -m pytest transform/tests/test_transform.py -q --tb=short 2>&1 | tail -35",
  "description": "Run tests with project venv",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-13T16:31:42.208Z)*

**Tool result**
```
........................................................................ [ 46%]
........................................................................ [ 92%]
...........                                                              [100%]
155 passed in 0.28s
```

---

### Assistant *(2026-05-13T16:31:47.460Z)*

All 155 tests pass (140 prior + 15 new). Now the last notes file:

---

### Assistant *(2026-05-13T16:32:07.185Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "old_string": "## 12. Full-corpus run plan",
  "new_string": "## 11. Shared-entity deduplication (2026-05-13)\n\nDescriptive triples for shared named entities are emitted at most once per URI across all transform runs. Without this, every sector run re-emits identical triples for the DDB Agent, XSLT SoftwareAgent, provider institutions, datasets, and all GND agents/places/concepts/timespans that appear in multiple records.\n\n### 11.1 Mechanism\n\nAn `emitted: dict[str, str]` (`uri → entity_type`) is passed into both `emit_prov_triples` and `emit_ddbedm_triples`. Each shared-node block checks membership before emitting and registers the URI on first emission. The dict is initialized in `__main__.py` before the record loop (empty = within-run dedup only). With `--entities-db PATH`, it is loaded from DuckDB at startup and written back with `INSERT OR IGNORE` after the loop, enabling cross-run dedup across sector files.\n\n**Entity types tracked**:\n\n| entity_type | Source |\n|---|---|\n| `prov_xslt` | `properties.mapping-version` → XSLT SoftwareAgent URI |\n| `prov_ddb` | Fixed `DDB_BASE` URI |\n| `prov_provider` | `provider-info.provider-ddb-id` → Provider Agent URI |\n| `prov_dataset` | `properties.dataset-id` → Dataset URI |\n| `edm_agent` | `edm.RDF.Agent[].about` |\n| `edm_place` | `edm.RDF.Place[].about` |\n| `skos_concept` | `edm.RDF.Concept[].about` |\n| `edm_timespan` | `edm.RDF.TimeSpan[].about` |\n\nPer-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted unconditionally.\n\n### 11.2 DuckDB schema\n\n```sql\nCREATE TABLE IF NOT EXISTS emitted_entities (\n    uri         VARCHAR PRIMARY KEY,\n    entity_type VARCHAR NOT NULL\n)\n```\n\nSeparate file from `werk-staging.duckdb`; shared across all sector runs in a production campaign. Managed by the caller — not auto-created in the run output directory.\n\n### 11.3 New CLI flag\n\n| Flag | Default | Description |\n|---|---|---|\n| `--entities-db PATH` | _(none)_ | Shared cross-run entity-dedup DuckDB. Omit for within-run dedup only. |\n\n### 11.4 Code changes\n\n| File | Change |\n|---|---|\n| `emitters.py` | Add `_DEDUP_ENTITY_TYPES` dict; add `emitted` param to `emit_ddbedm_triples` and `emit_prov_triples`; guard 4 PROV-O shared-node blocks + entity loop in `emit_ddbedm_triples` |\n| `transform.py` | Add `emitted_entities` param to `transform_record`; thread through to both emitters |\n| `__main__.py` | Add `--entities-db` CLI arg; DuckDB setup/load at startup; pass `emitted_entities` to `transform_record`; batch write-back after loop |\n\n### 11.5 Test additions\n\n15 new tests across 2 new classes (total: 155).\n\n**`TestEmitProvTriplesDedup`** (7 tests): `emitted=None` emits all; dict populated with correct `entity_type` values; each of the 4 shared nodes skipped when URI already in `emitted`; per-CHO linking triples always present even when all shared nodes are pre-emitted.\n\n**`TestEmitDdbedmTriplesDedup`** (8 tests): Agent/Place/Concept/TimeSpan skipped when URI already in `emitted`; `ProvidedCHO` never skipped (not in `_DEDUP_ENTITY_TYPES`); `emitted=None` emits all; second call with same `emitted` dict emits 0 agent triples; dict populated with correct `entity_type` after first call.\n\n---\n\n## 12. Full-corpus run plan"
}
```

---

### User *(2026-05-13T16:32:11.493Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:32:18.351Z)*

All done. Here's a summary of what changed:

**Code (3 files):**
- [emitters.py](goethe-faust/scripts/transform/emitters.py) — `_DEDUP_ENTITY_TYPES` dict; `emitted` param on `emit_ddbedm_triples` (guards Agent/Place/Concept/TimeSpan entity blocks) and `emit_prov_triples` (guards Dataset/XSLT/DDB Agent/Provider blocks)
- [transform.py](goethe-faust/scripts/transform/transform.py) — `emitted_entities` param threaded through to both emitters
- [__main__.py](goethe-faust/scripts/transform/__main__.py) — `--entities-db` CLI arg; DuckDB load at startup; pass to `transform_record`; batch `INSERT OR IGNORE` write-back after loop

**Tests (1 file):** [test_transform.py](goethe-faust/scripts/transform/tests/test_transform.py) — 15 new tests in `TestEmitProvTriplesDedup` and `TestEmitDdbedmTriplesDedup`; all 155 pass

**Notes (3 files):** [ddbedm-prov-o-plan.md](goethe-faust/notes/ddbedm-prov-o-plan.md) §2.1, [transform-script-adr.md](goethe-faust/notes/transform-script-adr.md) Decision 29, [transform-implementation-actual.md](goethe-faust/notes/transform-implementation-actual.md) §11

---

### User *(2026-05-13T16:33:50.482Z)*

what field/value do you use to deduct agent, place, concept, timespan?

---

### User *(2026-05-13T16:33:58.420Z)*

[Request interrupted by user]

---

### User *(2026-05-13T16:34:41.859Z)*

For software agent, you use version number to check duplicate SoftwareAgent. what field/value do you use to deduct agent, place, concept, timespan?

---

### User *(2026-05-13T16:34:48.843Z)*

[Request interrupted by user]

---

### User *(2026-05-13T16:34:52.167Z)*

For software agent, you use version number to check duplicate SoftwareAgent. what field/value do you use to dedup agent, place, concept, timespan?

---

### Assistant *(2026-05-13T16:35:10.115Z)*

The dedup key for those four types is `subj_uri`, derived from the entity's **`about`** field in the EDM RDF block:

```python
about_parts = raw_about.split()  # raw_about = entity.get("about")
subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
# → e.g. "http://d-nb.info/gnd/118540238"
```

So for Agent/Place/Concept/TimeSpan the key is the **`about` URI** (typically a GND URI). Contrast with XSLT, where the field is `properties.mapping-version` (a version string) and the URI is derived from it — the version number is the semantic key, not the URI. For Agent/Place/etc., the `about` URI is already the semantic identifier, so it doubles as both.

To draw the parallel explicitly:

| Entity | JSON field used | Key stored in `emitted` |
|---|---|---|
| XSLT SoftwareAgent | `properties.mapping-version` | `urn:ddbedm:properties:mapping-version:{ver}` |
| DDB Agent | fixed | `http://www.deutsche-digitale-bibliothek.de` |
| Provider | `provider-info.provider-ddb-id` | `urn:ddbedm:provider-info:provider-ddb-id:{id}` |
| Dataset | `properties.dataset-id` | `urn:ddbedm:properties:dataset-id:{id}` |
| edm:Agent | `edm.RDF.Agent[].about` | GND/DDB URI directly |
| edm:Place | `edm.RDF.Place[].about` | GND/DDB URI directly |
| skos:Concept | `edm.RDF.Concept[].about` | GND/DDB URI directly |
| edm:TimeSpan | `edm.RDF.TimeSpan[].about` | GND/DDB URI directly |

---

### User *(2026-05-13T16:36:44.674Z)*

I just instructed another session to use urn:ddbedm:<object-id> for all generated urns. how come you still have the property chain names in the urn?

---

### Assistant *(2026-05-13T16:37:08.341Z)*

I don't have visibility into what was decided in that other session. The current code uses the verbose property-chain convention from `ddbedm-prov-o-plan.md §2.1` (`urn:ddbedm:<block>:<key>:<value>`), which was the design at the time.

Before I change it: can you point me to the note or decision from that session? I need to know the exact format — specifically whether it's `urn:ddbedm:{value}` for all cases, or something more specific, and whether there's a disambiguation strategy (since a raw version number like `6.18` and a dataset ID like `76409877634279609sQOu` in the same `urn:ddbedm:` namespace could collide with each other or with bare DDB object IDs).

---

### User *(2026-05-13T16:40:51.771Z)*

i would still like it to be urn:ddbedm:<some id> how do we prevent collision?

---

### User *(2026-05-13T16:41:05.490Z)*

[Request interrupted by user]

---

### User *(2026-05-13T16:42:59.320Z)*

i would still like it to be urn:ddbedm:<some id> how do we prevent collision? check the schema /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv how we could get the provider ID. Here is sample data /Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json

---

### Assistant *(2026-05-13T16:43:03.432Z)*

Let me check both files for the relevant ID fields.

---

### Assistant *(2026-05-13T16:43:04.582Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -i \"provider\\|dataset\\|mapping\\|version\\|xslt\\|revision\" /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv | head -40",
  "description": "Find provider, dataset, version fields in schema CSV"
}
```

---

### User *(2026-05-13T16:43:04.662Z)*

**Tool result**
```
ddbObject.objectViewDataprovider,Literals(string)
ddbObject.providerInfo,Literals(string)
edm.RDF.Aggregation.dataProvider,
edm.RDF.Aggregation.dataProvider[].$,Literals(string)
edm.RDF.Aggregation.dataProvider[].lang,Literals(string)
edm.RDF.Aggregation.dataProvider[].resource,Literals(string)|URI
edm.RDF.Aggregation.provider,Literals(string)
properties.dataset-id,Literals(string)
properties.dataset-label,Literals(string)
properties.mapping-version,Literals(string)
properties.revision-id,Literals(string)
provider-info,
provider-info.domains[],Literals(string)|URI
provider-info.provider-collection,Literals(string)
provider-info.provider-ddb-id,Literals(string)
provider-info.provider-email,Literals(string)
provider-info.provider-europeana-name,Literals(string)
provider-info.provider-facebook,Literals(string)|URI
provider-info.provider-id,Literals(string)
provider-info.provider-isil,Literals(string)|URI
provider-info.provider-item-id,Literals(string)|URI
provider-info.provider-item-id-type,Literals(string)
provider-info.provider-latitude,Literals(string)
provider-info.provider-logo,Literals(string)|URI
provider-info.provider-longitude,Literals(string)
provider-info.provider-name,Literals(string)
provider-info.provider-parent-id,Literals(string)
provider-info.provider-parents,
provider-info.provider-parents.parents,Literals(string)
provider-info.provider-parents.parents[].aggregator,Literals(string)
provider-info.provider-parents.parents[].domains[],Literals(string)|URI
provider-info.provider-parents.parents[].provider-collection,Literals(string)
provider-info.provider-parents.parents[].provider-ddb-id,Literals(string)
provider-info.provider-parents.parents[].provider-email,Literals(string)
provider-info.provider-parents.parents[].provider-id,Literals(string)
provider-info.provider-parents.parents[].provider-item-id-type,Literals(string)
provider-info.provider-parents.parents[].provider-latitude,Literals(string)
provider-info.provider-parents.parents[].provider-logo,Literals(string)|URI
provider-info.provider-parents.parents[].provider-longitude,Literals(string)
provider-info.provider-parents.parents[].provider-name,Literals(string)
```

---

### Assistant *(2026-05-13T16:43:06.451Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json\nwith open('/Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json') as f:\n    rec = json.loads(f.readline())\nfor block in ['properties', 'provider-info']:\n    print(f'--- {block} ---')\n    print(json.dumps(rec.get(block, {}), indent=2))\n\"",
  "description": "Print properties and provider-info blocks from first record"
}
```

---

### User *(2026-05-13T16:43:08.334Z)*

**Tool result** *(error)*
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 4, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 2)
```

---

### Assistant *(2026-05-13T16:43:11.964Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json\nwith open('/Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json') as f:\n    for line in f:\n        line = line.strip()\n        if line:\n            rec = json.loads(line)\n            break\nfor block in ['properties', 'provider-info']:\n    print(f'--- {block} ---')\n    print(json.dumps(rec.get(block, {}), indent=2))\n\"",
  "description": "Print properties and provider-info from first non-empty JSONL line"
}
```

---

### User *(2026-05-13T16:43:13.431Z)*

**Tool result** *(error)*
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 7, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)
```

---

### Assistant *(2026-05-13T16:43:17.359Z)*

**Tool call:** `Bash`
```json
{
  "command": "file /Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json && head -c 200 /Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json | xxd | head -5",
  "description": "Check file encoding and first bytes"
}
```

---

### User *(2026-05-13T16:43:19.478Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json: Unicode text, UTF-8 text
00000000: 5b0a 2020 7b0a 2020 2020 2270 726f 7065  [.  {.    "prope
00000010: 7274 6965 7322 3a20 7b0a 2020 2020 2020  rties": {.      
00000020: 2269 7465 6d2d 6964 223a 2022 3232 324e  "item-id": "222N
00000030: 5a4b 4b36 3354 4e52 4c43 3256 4554 5256  ZKK63TNRLC2VETRV
00000040: 3732 3256 4b42 4453 5556 474c 222c 0a20  722VKBDSUVGL",.
```

---

### Assistant *(2026-05-13T16:43:24.352Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json\nwith open('/Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json') as f:\n    data = json.load(f)\nrec = data[0]\nfor block in ['properties', 'provider-info']:\n    print(f'--- {block} ---')\n    print(json.dumps(rec.get(block, {}), indent=2))\n\"",
  "description": "Load as JSON array and print first record's key blocks"
}
```

---

### User *(2026-05-13T16:43:27.835Z)*

**Tool result**
```
--- properties ---
{
  "item-id": "222NZKK63TNRLC2VETRV722VKBDSUVGL",
  "dataset-id": "76409877634279609sQOu",
  "dataset-label": "Gesamtlieferung: Deutsche Fotothek - LIDO",
  "revision-id": "43",
  "ingest-date": "2026-01-07T15:40:43+0100",
  "cortex-type": "Kultur",
  "mapping-version": "6.18",
  "automatically-translated": false
}
--- provider-info ---
{
  "domains": [
    "http://ddb.vocnet.org/sparte/sparte005",
    "",
    ""
  ],
  "provider-name": "Deutsche Fotothek",
  "provider-europeana-name": "",
  "provider-parent-id": "00014072",
  "provider-facebook": "",
  "provider-twitter": "https://twitter.com/Fotothek",
  "provider-uri": "http://www.deutschefotothek.de",
  "provider-email": "Deutsche.Fotothek@slub-dresden.de",
  "provider-collection": "",
  "provider-item-id": "DE-2396_90106124_df_pos-2018-a_0000067_000_f",
  "provider-item-id-type": "",
  "provider-id": "99900890",
  "provider-ddb-id": "CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI",
  "provider-isil": "http://ld.zdb-services.de/resource/organisations/DE-2396",
  "provider-logo": "https://registrierung.deutsche-digitale-bibliothek.de/logos/99900890.jpg",
  "provider-longitude": "13.73593",
  "provider-latitude": "51.02874",
  "provider-state": "Sachsen",
  "provider-parents": {
    "parents": [
      {
        "provider-name": "S\u00e4chsische Landesbibliothek - Staats- und Universit\u00e4tsbibliothek Dresden",
        "domains": [
          "http://ddb.vocnet.org/sparte/sparte002",
          "",
          ""
        ],
        "provider-parent-id": "",
        "provider-uri": "http://www.slub-dresden.de",
        "provider-email": "",
        "provider-collection": "",
        "provider-item-id-type": "",
        "provider-id": "00014072",
        "provider-ddb-id": "265BI7NE7QBS4NQMZCCGIVLFR73OCOSL",
        "provider-logo": "https://registrierung.deutsche-digitale-bibliothek.de/logos/00014072.jpg",
        "provider-longitude": "13.73593",
        "provider-latitude": "51.02874",
        "aggregator": false
      }
    ]
  }
}
```

---

### Assistant *(2026-05-13T16:44:02.620Z)*

The collision risk is real: `provider-ddb-id` (`CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI`) is a 32-char DDB ID — same format as `item-id`. Without disambiguation, `urn:ddbedm:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI` is indistinguishable from an item URI. `dataset-id` (`76409877634279609sQOu`) and `mapping-version` (`6.18`) add more clash surface.

Three options:

**A — Short type prefix (recommended)**
```
urn:ddbedm:provider:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI   ← provider-ddb-id
urn:ddbedm:dataset:76409877634279609sQOu                  ← dataset-id
urn:ddbedm:xslt:6.18                                      ← mapping-version
```
Minimal addition, human-readable, no lookup needed to understand what the URN identifies.

**B — Hash of (type + value)**
```
urn:ddbedm:SHA1(provider:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI)
```
Collision-proof but opaque — you can't tell what entity it refers to without a registry.

**C — Separate URN namespace per type**
```
urn:ddb-provider:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI
urn:ddb-dataset:76409877634279609sQOu
```
Cleaner namespace separation but requires registering multiple NID prefixes.

**Recommendation: A.** The short prefix (`provider:`, `dataset:`, `xslt:`) is the natural discriminator — it mirrors what the ID *is*, keeps the actual identifier readable, and avoids the verbosity of the current property-chain form. The current `urn:ddbedm:properties:dataset-id:76409877634279609sQOu` becomes `urn:ddbedm:dataset:76409877634279609sQOu`.

Which do you prefer?

---

### User *(2026-05-13T16:48:18.428Z)*

i also remove the urn affix from agent, place, concept, timespan, this might also cause some form of collision.

---

### Assistant *(2026-05-13T16:48:59.133Z)*

So the full collision picture is:

- **PROV-O nodes**: want `urn:ddbedm:{id}` — provider-ddb-id, dataset-id, mapping-version are all short opaque strings
- **Agent/Place/Concept/TimeSpan bare IDs**: also `urn:ddbedm:{32-char-DDB-ID}` — same namespace, same format

A provider-ddb-id like `CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI` is a 32-char DDB ID — identical format to an agent or concept bare ID. Without a discriminator, `urn:ddbedm:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI` is ambiguous.

The short-prefix approach from Option A still solves this cleanly, **and the prefixes can't collide with bare DDB IDs** because DDB IDs are 32-char alphanumeric — they never start with `provider:`, `dataset:`, or `xslt:`:

```
urn:ddbedm:provider:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI  ← PROV-O Provider Agent
urn:ddbedm:dataset:76409877634279609sQOu                 ← PROV-O Dataset
urn:ddbedm:xslt:6.18                                     ← PROV-O XSLT SoftwareAgent
urn:ddbedm:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI            ← bare-ID Agent/Place/Concept/TimeSpan
```

No collision possible: the colon after the type word is the discriminator, and DDB IDs never contain colons. `mapping-version` values like `6.18` also contain a dot, not a colon, so no clash with `xslt:6.18`.

One remaining edge case: **dataset-id** (`76409877634279609sQOu`) — is this format distinct from bare DDB entity IDs? Bare entity IDs are always exactly 32 uppercase alphanumeric chars. Dataset IDs appear to be variable-length mixed-case strings. Let me verify:

---

### Assistant *(2026-05-13T16:49:02.580Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json\ndataset_ids = set()\nprovider_ids = set()\nwith open('/Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json') as f:\n    for rec in json.load(f):\n        props = rec.get('properties') or {}\n        pinfo = rec.get('provider-info') or {}\n        if props.get('dataset-id'):\n            dataset_ids.add(props['dataset-id'])\n        if pinfo.get('provider-ddb-id'):\n            provider_ids.add(pinfo['provider-ddb-id'])\nprint('dataset-id samples:', sorted(dataset_ids)[:10])\nprint('dataset-id lengths:', sorted({len(x) for x in dataset_ids}))\nprint()\nprint('provider-ddb-id samples:', sorted(provider_ids)[:5])\nprint('provider-ddb-id lengths:', sorted({len(x) for x in provider_ids}))\n\"",
  "description": "Check dataset-id and provider-ddb-id formats in sample data"
}
```

---

### User *(2026-05-13T16:53:48.580Z)*

**Tool result**
```
dataset-id samples: ['05729beeedc53aab338dd27ecaf32592ba981e07', '10354060393776970lpbP', '10540007514917601kIEX', '10644659166684776mVSD', '11738804782467846aMHW', '1188751977287471Akxq', '1296634308338877eyck', '1296799422070261UOgo', '12972523807685130ztzU', '12972779337265781Ogyb']
dataset-id lengths: [19, 20, 21, 40]

provider-ddb-id samples: ['2232YVSIZTZYDAZIBI25LW3TZUY6DZVH', '265BI7NE7QBS4NQMZCCGIVLFR73OCOSL', '2MSI2HDGRMB3T24CE4QKIMI2OON3ZILN', '2Q37XY5KXJNJE5MV6SWP3UKKZ6RSBLK5', '352XKS2HXYFRLY24AF5Q3N74AEAEAR4X']
provider-ddb-id lengths: [32]
```

---

### Assistant *(2026-05-13T16:54:03.390Z)*

Good data. `dataset-id` is variable-length (19–40 chars) mixed case — not 32-char uppercase like DDB entity IDs, but the longer 40-char hex ones (`05729bee…`) could theoretically overlap. `provider-ddb-id` is exactly 32-char uppercase — **identical format to bare entity IDs**, confirmed collision without a prefix.

Short-prefix approach is validated and safe:

| URI | Key |
|---|---|
| `urn:ddbedm:provider:{provider-ddb-id}` | 32-char DDB ID — would collide bare |
| `urn:ddbedm:dataset:{dataset-id}` | variable-length — 40-char hex could collide bare |
| `urn:ddbedm:xslt:{mapping-version}` | `6.18` — safe bare but prefix keeps it consistent |
| `urn:ddbedm:{bare-DDB-id}` | Agent/Place/Concept/TimeSpan — no prefix needed |

The colon after the type word is the unambiguous discriminator since DDB IDs are purely alphanumeric. No bare entity ID can ever start with `provider:`, `dataset:`, or `xslt:`.

Shall I update the code and notes to use this scheme — replacing the current property-chain URNs (`urn:ddbedm:properties:dataset-id:…`, etc.) with the short-prefix form?

---

### User *(2026-05-13T16:55:23.240Z)*

yes, add test cases and update notes: /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md

---

### User *(2026-05-13T16:55:25.929Z)*

[Request interrupted by user]

---

### User *(2026-05-13T16:55:49.068Z)*

yes, add test cases and update notes: /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md. Check which other note to update based on prov

---

### Assistant *(2026-05-13T16:56:04.705Z)*

Let me find all places that reference the old URN patterns.

---

### Assistant *(2026-05-13T16:56:05.600Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -rn \"urn:ddbedm:properties\\|urn:ddbedm:provider-info\" /Users/mta/Documents/claude/goethe-faust/scripts/ /Users/mta/Documents/claude/goethe-faust/notes/ 2>/dev/null",
  "description": "Find all old-style URN patterns in code and notes"
}
```

---

### User *(2026-05-13T16:56:05.883Z)*

**Tool result**
```
<persisted-output>
Output too large (338.5KB). Full output saved to: /Users/mta/.claude/projects/-Users-mta-Documents-claude/0de9cbbf-84af-4e5a-9d27-80f146854276/tool-results/bqceo6ci6.txt

Preview (first 2KB):
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:169:98:    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:170:99:    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:171:100:    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:530:98	    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:531:99	    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:532:100	    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:1296:316:| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-there-are-bugs-in-the-transform-scripts-20260507-111958.md:1297:317:| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
...
</persisted-output>
```

---

### Assistant *(2026-05-13T16:56:09.403Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -rn \"urn:ddbedm:properties\\|urn:ddbedm:provider-info\" \\\n  /Users/mta/Documents/claude/goethe-faust/scripts/transform/ \\\n  /Users/mta/Documents/claude/goethe-faust/notes/ \\\n  --include=\"*.py\" --include=\"*.md\" 2>/dev/null",
  "description": "Find old URN patterns only in transform scripts and notes (not transcripts)"
}
```

---

### User *(2026-05-13T16:56:09.466Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:121:    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:122:    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py:123:    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py:1229:    _XSLT_URI = "urn:ddbedm:properties:mapping-version:6.18"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py:1230:    _DS_URI   = "urn:ddbedm:properties:dataset-id:testdataset123"
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py:1231:    _PROV_URI = "urn:ddbedm:provider-info:provider-ddb-id:PROVIDERID00000000000000000000000"
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md:148:| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md:149:| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md:150:| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `provider-info.provider-ddb-id` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:316:| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:317:| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:318:| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `provider-info.provider-ddb-id` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:338:        <urn:ddbedm:properties:dataset-id:76409877634279609sQOu> ;  # properties.dataset-id
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:340:        <urn:ddbedm:properties:mapping-version:6.18> ;              # properties.mapping-version
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:347:<urn:ddbedm:properties:dataset-id:76409877634279609sQOu>
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:353:        <urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:357:<urn:ddbedm:properties:mapping-version:6.18>
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:370:<urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:390:**Dataset** (`urn:ddbedm:properties:dataset-id:<value>`):
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:399:**XSLT** (`urn:ddbedm:properties:mapping-version:<value>`):
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md:406:**Provider** (`urn:ddbedm:provider-info:provider-ddb-id:<value>`):
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:47:| Dataset | `dcat:Dataset`, `prov:Entity` | `urn:ddbedm:properties:dataset-id:<id>` |
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:48:| XSLT | `prov:SoftwareAgent` | `urn:ddbedm:properties:mapping-version:<ver>` |
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:49:| Provider | `prov:Agent`, `foaf:Organization` | `urn:ddbedm:provider-info:provider-ddb-id:<id>` |
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:56:**Shared node deduplication**: The four shared nodes (Dataset, XSLT, DDB Agent, Provider) have stable URIs that recur across records and sector files. Their descriptive triples are emitted only on first encounter per run via an `emitted: dict[str, str]` guard in `emit_prov_triples`. With `--entities-db`, the dict is persisted to DuckDB across runs; without it, deduplication is within-run only. The per-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted. The XSLT URI is derived from the version number (`urn:ddbedm:properties:mapping-version:{ver}`), so the version number is the effective lookup key at the code level.
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:117:#### 2.2.3 Dataset (`urn:ddbedm:properties:dataset-id:<value>`)
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:127:#### 2.2.4 XSLT (`urn:ddbedm:properties:mapping-version:<value>`)
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:142:#### 2.2.6 Provider (`urn:ddbedm:provider-info:provider-ddb-id:<value>`)
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:187:        <urn:ddbedm:properties:dataset-id:76409877634279609sQOu> ;
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:189:        <urn:ddbedm:properties:mapping-version:6.18> ;
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:196:<urn:ddbedm:properties:dataset-id:76409877634279609sQOu>
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:202:        <urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:206:<urn:ddbedm:properties:mapping-version:6.18>
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md:219:<urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
```

---

### Assistant *(2026-05-13T16:56:18.146Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"urn:ddbedm\" /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "description": "Check transform-script-adr and transform-implementation-actual for old URNs"
}
```

---

### User *(2026-05-13T16:56:18.198Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md:276:| `test_bare_id_hastype_expanded` | `urn:ddbedm:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md:283:| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id` (`urn:ddbedm:<id>`) |
/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md:480:**Rationale**: `ddbedm` is consistent with the `urn:ddbedm:` URN convention used throughout the PROV-O graph (D12). The `ddbedm` graph is emitted as priority #1 — a faithful baseline from which `mocho` and `work` graphs can be re-derived or verified. Separating raw EDM from aligned mocho triples allows independent re-runs of the alignment step without re-ingesting source data.
/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md:597:| All others (`Aggregation`, `Agent`, `Event`, `Place`, `WebResource`, …) | `urn:ddbedm:<ClassName>:<id>` | `urn:ddbedm:Agent:O5XUSBA7IPKSXYUTN6EQNWK62BQRF7GN` |
/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md:603:**Rationale**: `ProvidedCHO` bare IDs are DDB item identifiers — the canonical DDB item URI scheme (`…/item/<id>`) is the correct dereferenceable form and aligns with the `owl:sameAs` link emitted in the mocho graph. All other entity types have no canonical HTTP URI, so the `urn:ddbedm:` scheme encodes both the namespace and the entity class, making the source unambiguous without requiring a dereferenceable endpoint. Consistent with `export-s2-plan.md §4.3`.
```

---

### Assistant *(2026-05-13T16:56:54.597Z)*

Four files need updating in notes: `ddbedm-prov-o-plan.md`, `transform-adr.md`, `transform-implementation-plan.md`, and `transform-script-adr.md` (D27 bare-entity URI table is also stale). Plus code and tests. Let me do everything now.

---

### Assistant *(2026-05-13T16:56:55.970Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    ds_uri   = f\"urn:ddbedm:properties:dataset-id:{dataset_id}\"      if dataset_id      else \"\"\n    xslt_uri = f\"urn:ddbedm:properties:mapping-version:{map_ver}\"    if map_ver         else \"\"\n    prov_uri = f\"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}\" \\\n               if provider_ddb_id else \"\"",
  "new_string": "    ds_uri   = f\"urn:ddbedm:dataset:{dataset_id}\"       if dataset_id      else \"\"\n    xslt_uri = f\"urn:ddbedm:xslt:{map_ver}\"             if map_ver         else \"\"\n    prov_uri = f\"urn:ddbedm:provider:{provider_ddb_id}\" if provider_ddb_id else \"\""
}
```

---

### User *(2026-05-13T16:57:07.164Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:57:12.838Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "    _XSLT_URI = \"urn:ddbedm:properties:mapping-version:6.18\"\n    _DS_URI   = \"urn:ddbedm:properties:dataset-id:testdataset123\"\n    _PROV_URI = \"urn:ddbedm:provider-info:provider-ddb-id:PROVIDERID00000000000000000000000\"",
  "new_string": "    _XSLT_URI = \"urn:ddbedm:xslt:6.18\"\n    _DS_URI   = \"urn:ddbedm:dataset:testdataset123\"\n    _PROV_URI = \"urn:ddbedm:provider:PROVIDERID00000000000000000000000\""
}
```

---

### User *(2026-05-13T16:58:01.010Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:58:04.501Z)*

Now add the new URN-format tests at the end of `TestEmitProvTriplesDedup`:

---

### Assistant *(2026-05-13T16:58:16.593Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "    def test_cho_linking_always_emitted(self):\n        emitted = {\n            self._XSLT_URI: \"prov_xslt\",\n            DDB_BASE:        \"prov_ddb\",\n            self._PROV_URI:  \"prov_provider\",\n            self._DS_URI:    \"prov_dataset\",\n        }\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH, emitted=emitted)\n        cho_nt    = f\"<{self._CHO_URI}>\"\n        cho_lines = [nq for nq in lines if nq.startswith(cho_nt)]\n        predicates = {\n            nq.split(\"> <\", 1)[1].split(\">\", 1)[0]\n            for nq in cho_lines if \"> <\" in nq\n        }\n        assert \"http://www.w3.org/ns/prov#wasDerivedFrom\"  in predicates\n        assert \"http://www.w3.org/ns/prov#wasAttributedTo\" in predicates\n        assert \"http://www.w3.org/ns/prov#generatedAtTime\" in predicates",
  "new_string": "    def test_cho_linking_always_emitted(self):\n        emitted = {\n            self._XSLT_URI: \"prov_xslt\",\n            DDB_BASE:        \"prov_ddb\",\n            self._PROV_URI:  \"prov_provider\",\n            self._DS_URI:    \"prov_dataset\",\n        }\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH, emitted=emitted)\n        cho_nt    = f\"<{self._CHO_URI}>\"\n        cho_lines = [nq for nq in lines if nq.startswith(cho_nt)]\n        predicates = {\n            nq.split(\"> <\", 1)[1].split(\">\", 1)[0]\n            for nq in cho_lines if \"> <\" in nq\n        }\n        assert \"http://www.w3.org/ns/prov#wasDerivedFrom\"  in predicates\n        assert \"http://www.w3.org/ns/prov#wasAttributedTo\" in predicates\n        assert \"http://www.w3.org/ns/prov#generatedAtTime\" in predicates\n\n    # ── URN format tests ──────────────────────────────────────────────────────\n\n    def test_xslt_uri_short_prefix(self):\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH)\n        assert any(\"urn:ddbedm:xslt:6.18\" in nq for nq in lines)\n        assert not any(\"urn:ddbedm:properties:mapping-version\" in nq for nq in lines)\n\n    def test_dataset_uri_short_prefix(self):\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH)\n        assert any(\"urn:ddbedm:dataset:testdataset123\" in nq for nq in lines)\n        assert not any(\"urn:ddbedm:properties:dataset-id\" in nq for nq in lines)\n\n    def test_provider_uri_short_prefix(self):\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH)\n        assert any(\"urn:ddbedm:provider:PROVIDERID00000000000000000000000\" in nq for nq in lines)\n        assert not any(\"urn:ddbedm:provider-info:provider-ddb-id\" in nq for nq in lines)\n\n    def test_prov_uris_no_collision_with_entity_bare_id(self):\n        # DDB bare IDs are 32-char alphanumeric — prov URNs use typed prefixes with colons\n        # so urn:ddbedm:provider:X and urn:ddbedm:X are distinct\n        lines = emit_prov_triples(self._RECORD, self._CHO_URI, self._GRAPH)\n        prov_subjects = {nq.split(\" \", 1)[0] for nq in lines\n                         if nq.startswith(\"<urn:ddbedm:\")}\n        for s in prov_subjects:\n            # every prov URN must carry a type segment (provider:, dataset:, xslt:)\n            inner = s[len(\"<urn:ddbedm:\"):-1]\n            assert \":\" in inner, f\"prov URN missing type prefix: {s}\""
}
```

---

### User *(2026-05-13T16:58:26.065Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:58:30.454Z)*

Run tests:

---

### Assistant *(2026-05-13T16:58:30.600Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust/scripts && /Users/mta/Documents/claude/goethe-faust/.venv/bin/python -m pytest transform/tests/test_transform.py -q --tb=short 2>&1 | tail -10",
  "description": "Run tests to verify URN format changes",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-13T16:58:33.002Z)*

**Tool result**
```
........................................................................ [ 45%]
........................................................................ [ 90%]
...............                                                          [100%]
159 passed in 0.27s
```

---

### Assistant *(2026-05-13T16:58:36.601Z)*

159 pass. Now update all four notes files in parallel:

---

### Assistant *(2026-05-13T16:58:37.735Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "old_string": "urn:ddbedm:properties:dataset-id:",
  "new_string": "urn:ddbedm:dataset:"
}
```

---

### Assistant *(2026-05-13T16:58:38.659Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md",
  "old_string": "urn:ddbedm:properties:dataset-id:",
  "new_string": "urn:ddbedm:dataset:"
}
```

---

### User *(2026-05-13T16:58:40.593Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T16:58:40.596Z)*

**Tool result** *(error)*
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

---

### Assistant *(2026-05-13T16:58:43.972Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md",
  "offset": 310,
  "limit": 100
}
```

---

### User *(2026-05-13T16:58:43.986Z)*

**Tool result**
```
310	
311	### URI scheme
312	
313	| Node | URI pattern | JSON source |
314	|---|---|---|
315	| CHO | `ddb:item/<id>` | `properties.item-id` |
316	| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
317	| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
318	| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `provider-info.provider-ddb-id` |
319	| DDB | `<http://www.deutsche-digitale-bibliothek.de>` | fixed |
320	
321	### Turtle pattern
322	
323	```turtle
324	@prefix prov:     <http://www.w3.org/ns/prov#> .
325	@prefix ddb:      <http://www.deutsche-digitale-bibliothek.de/> .
326	@prefix dcat:     <http://www.w3.org/ns/dcat#> .
327	@prefix dcterms:  <http://purl.org/dc/terms/> .
328	@prefix foaf:     <http://xmlns.com/foaf/0.1/> .
329	@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .
330	@prefix schema:   <https://schema.org/> .
331	@prefix lov:      <http://www.w3.org/ns/iana/media-types/> .
332	
333	# ── CHO ──────────────────────────────────────────────────────────────────────
334	
335	ddb:item/222NZKK63TNRLC2VETRV722VKBDSUVGL          # properties.item-id
336	    a prov:Entity ;
337	    prov:wasDerivedFrom
338	        <urn:ddbedm:properties:dataset-id:76409877634279609sQOu> ;  # properties.dataset-id
339	    prov:wasAttributedTo
340	        <urn:ddbedm:properties:mapping-version:6.18> ;              # properties.mapping-version
341	    prov:generatedAtTime "2026-01-07T15:40:43+0100" ;               # properties.ingest-date
342	    dcterms:hasVersion   "43" ;                                      # properties.revision-id
343	    dcterms:references   "ddb:222NZKK63TNRLC2VETRV722VKBDSUVGL" .  # source.description.record.ref
344	
345	# ── Dataset ───────────────────────────────────────────────────────────────────
346	
347	<urn:ddbedm:properties:dataset-id:76409877634279609sQOu>
348	    a dcat:Dataset, prov:Entity ;
349	    dcterms:identifier "76409877634279609sQOu" ;                     # properties.dataset-id
350	    rdfs:label         "Gesamtlieferung: Deutsche Fotothek - LIDO"@de ;  # properties.dataset-label
351	    dcterms:type       <http://www.lido-schema.org/> ;               # source.description.record.type
352	    prov:wasAttributedTo
353	        <urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .
354	
355	# ── XSLT SoftwareAgent ────────────────────────────────────────────────────────
356	
357	<urn:ddbedm:properties:mapping-version:6.18>
358	    a prov:SoftwareAgent ;
359	    dcterms:hasVersion "6.18" ;                                      # properties.mapping-version
360	    prov:actedOnBehalfOf <http://www.deutsche-digitale-bibliothek.de> .
361	
362	# ── DDB Agent ─────────────────────────────────────────────────────────────────
363	
364	<http://www.deutsche-digitale-bibliothek.de>
365	    a prov:Agent, foaf:Organization ;
366	    foaf:name "Deutsche Digitale Bibliothek" .
367	
368	# ── Provider Agent ────────────────────────────────────────────────────────────
369	
370	<urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
371	    a prov:Agent, foaf:Organization ;
372	    foaf:name        "Deutsche Fotothek" ;                           # provider-info.provider-name
373	    schema:url       <http://www.deutschefotothek.de> ;              # provider-info.provider-uri
374	    dcterms:identifier "99900890" ;                                  # provider-info.provider-id
375	    lov:isil         <http://ld.zdb-services.de/resource/organisations/DE-2396> .  # provider-info.provider-isil
376	```
377	
378	### Field mapping table
379	
380	**CHO** (`ddb:item/<properties.item-id>`):
381	
382	| Triple | JSON path | Value type |
383	|---|---|---|
384	| `prov:wasDerivedFrom` | `properties.dataset-id` → Dataset URN | URN |
385	| `prov:wasAttributedTo` | `properties.mapping-version` → XSLT URN | URN |
386	| `prov:generatedAtTime` | `properties.ingest-date` | xsd:dateTime literal |
387	| `dcterms:hasVersion` | `properties.revision-id` | string literal |
388	| `dcterms:references` | `source.description.record.ref` | `"ddb:<ref>"` literal |
389	
390	**Dataset** (`urn:ddbedm:properties:dataset-id:<value>`):
391	
392	| Triple | JSON path | Value type |
393	|---|---|---|
394	| `dcterms:identifier` | `properties.dataset-id` | string literal |
395	| `rdfs:label` | `properties.dataset-label` | `@de` literal |
396	| `dcterms:type` | `source.description.record.type` | URI |
397	| `prov:wasAttributedTo` | `provider-info.provider-ddb-id` → Provider URN | URN |
398	
399	**XSLT** (`urn:ddbedm:properties:mapping-version:<value>`):
400	
401	| Triple | JSON path | Value type |
402	|---|---|---|
403	| `dcterms:hasVersion` | `properties.mapping-version` | string literal |
404	| `prov:actedOnBehalfOf` | fixed: `<http://www.deutsche-digitale-bibliothek.de>` | URI |
405	
406	**Provider** (`urn:ddbedm:provider-info:provider-ddb-id:<value>`):
407	
408	| Triple | JSON path | Value type |
409	|---|---|---|
```

---

### Assistant *(2026-05-13T16:58:44.439Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "offset": 145,
  "limit": 10
}
```

---

### User *(2026-05-13T16:58:44.449Z)*

**Tool result**
```
145	| Node | URI pattern | Source fields |
146	|---|---|---|
147	| CHO | `ddb:item/<item-id>` | `properties.item-id` |
148	| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
149	| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
150	| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `provider-info.provider-ddb-id` |
151	| DDB | `http://www.deutsche-digitale-bibliothek.de` | fixed |
152	| SourceRecord | `ddb-api:items/<id>/source/record` | `binaries.binary[]` (one block per entry) |
153	
154	### §6.3 `emit_mocho_triples(...)` — stream [2] orchestrator
```

---

### Assistant *(2026-05-13T16:58:48.448Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md",
  "old_string": "urn:ddbedm:properties:dataset-id:",
  "new_string": "urn:ddbedm:dataset:"
}
```

---

### Assistant *(2026-05-13T16:58:49.352Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "old_string": "urn:ddbedm:properties:dataset-id:",
  "new_string": "urn:ddbedm:dataset:"
}
```

---

### User *(2026-05-13T16:58:50.427Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T16:58:52.440Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:58:56.373Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "old_string": "urn:ddbedm:properties:mapping-version:",
  "new_string": "urn:ddbedm:xslt:"
}
```

---

### Assistant *(2026-05-13T16:58:57.604Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md",
  "old_string": "urn:ddbedm:properties:mapping-version:",
  "new_string": "urn:ddbedm:xslt:"
}
```

---

### Assistant *(2026-05-13T16:58:57.905Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "old_string": "urn:ddbedm:properties:mapping-version:",
  "new_string": "urn:ddbedm:xslt:"
}
```

---

### User *(2026-05-13T16:58:58.321Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T16:59:00.271Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T16:59:02.202Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:59:10.698Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "old_string": "urn:ddbedm:provider-info:provider-ddb-id:",
  "new_string": "urn:ddbedm:provider:"
}
```

---

### Assistant *(2026-05-13T16:59:10.941Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md",
  "old_string": "urn:ddbedm:provider-info:provider-ddb-id:",
  "new_string": "urn:ddbedm:provider:"
}
```

---

### Assistant *(2026-05-13T16:59:11.395Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "old_string": "urn:ddbedm:provider-info:provider-ddb-id:",
  "new_string": "urn:ddbedm:provider:"
}
```

---

### User *(2026-05-13T16:59:12.771Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T16:59:14.740Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T16:59:16.740Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md has been updated. All occurrences were successfully replaced. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T16:59:21.894Z)*

Now fix the section headers and URN convention paragraph in `ddbedm-prov-o-plan.md`, update the stale entity URI entry in `transform-script-adr.md`, and update the URN convention note in §2.1:

---

### Assistant *(2026-05-13T16:59:23.181Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": true,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "old_string": "#### 2.2.3 Dataset (`urn:ddbedm:properties:dataset-id:<value>`)",
  "new_string": "#### 2.2.3 Dataset (`urn:ddbedm:dataset:<value>`)"
}
```

---

### User *(2026-05-13T16:59:23.184Z)*

**Tool result** *(error)*
```
<tool_use_error>String to replace not found in file.
String: #### 2.2.3 Dataset (`urn:ddbedm:properties:dataset-id:<value>`)</tool_use_error>
```

---

### User *(2026-05-13T17:01:29.483Z)*

This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. Primary Request and Intent:
   The conversation covers a multi-part feature addition to the goethe-faust DDB-EDM transform scripts (`/Users/mta/Documents/claude/goethe-faust/scripts/transform/`):
   - **Part 1**: Identify which part of the transform scripts emits PROV-O provenance triples
   - **Part 2**: Add cross-run shared-entity deduplication: avoid re-emitting identical descriptive triples for shared named entities (PROV-O nodes + edm:Agent/Place/Concept/TimeSpan) across multiple sector-file runs
   - **Part 3**: Use a persistent DuckDB table (`emitted_entities`) for cross-run state (user runs the script on s1–s7 sector files as separate OS processes)
   - **Part 4**: Change the PROV-O URN scheme from verbose property-chain form (`urn:ddbedm:properties:dataset-id:…`) to a short-prefix form (`urn:ddbedm:dataset:…`, `urn:ddbedm:xslt:…`, `urn:ddbedm:provider:…`) to prevent collision with bare entity IDs that use `urn:ddbedm:{id}` (no type prefix)
   - **Throughout**: Add tests and update all relevant notes files

2. Key Technical Concepts:
   - PROV-O Layer 1 (Without-Activity pattern) — 5 node types per CHO record
   - Cross-run deduplication via DuckDB persistent table
   - URN collision prevention with typed short prefixes — DDB bare IDs are 32-char alphanumeric (no colons), so `urn:ddbedm:provider:X` vs `urn:ddbedm:X` are unambiguous
   - `dict[str, str]` (`uri → entity_type`) used as both O(1) lookup and write-back source
   - `INSERT OR IGNORE` for idempotent DuckDB writes
   - `None`-safe fallback: `emitted=None` → always emit (backward-compatible for tests)
   - Per-CHO linking triples always emitted; only shared-node descriptive triples are deduplicated
   - Named graph: `https://gemea.ise.fiz-karlsruhe.de/graph/prov`

3. Files and Code Sections:

   - **`scripts/transform/emitters.py`** — Core emitter file with all PROV-O triple generation
     - Added `_DEDUP_ENTITY_TYPES` dict after imports:
       ```python
       _DEDUP_ENTITY_TYPES: dict[str, str] = {
           "Agent":    "edm_agent",
           "Place":    "edm_place",
           "Concept":  "skos_concept",
           "TimeSpan": "edm_timespan",
       }
       ```
     - Updated `emit_ddbedm_triples` signature: added `emitted: dict[str, str] | None = None`
     - Added dedup check in entity loop (after computing `subj_uri`):
       ```python
       if emitted is not None and entity_type in _DEDUP_ENTITY_TYPES:
           if subj_uri in emitted:
               continue
           emitted[subj_uri] = _DEDUP_ENTITY_TYPES[entity_type]
       ```
     - Updated `emit_prov_triples` signature: added `emitted: dict[str, str] | None = None`
     - Changed URN construction from verbose to short-prefix form:
       ```python
       ds_uri   = f"urn:ddbedm:dataset:{dataset_id}"       if dataset_id      else ""
       xslt_uri = f"urn:ddbedm:xslt:{map_ver}"             if map_ver         else ""
       prov_uri = f"urn:ddbedm:provider:{provider_ddb_id}" if provider_ddb_id else ""
       ```
     - Guarded 4 shared-node blocks (Dataset, XSLT, DDB Agent, Provider):
       ```python
       # Dataset example:
       if ds_uri and (emitted is None or ds_uri not in emitted):
           if emitted is not None:
               emitted[ds_uri] = "prov_dataset"
           ds_nt = f"<{ds_uri}>"
           # ... emit triples ...
       
       # DDB Agent (fixed URI):
       if emitted is None or DDB_BASE not in emitted:
           if emitted is not None:
               emitted[DDB_BASE] = "prov_ddb"
           ddb_nt = f"<{DDB_BASE}>"
           # ... emit triples ...
       ```

   - **`scripts/transform/transform.py`** — Per-record orchestration
     - Added `emitted_entities: dict[str, str] | None = None` to `transform_record` signature
     - Updated both emitter calls:
       ```python
       ddbedm_lines, ddbedm_classes, ddbedm_preds, ddbedm_sani = emit_ddbedm_triples(
           rdf, GRAPH_DDBEDM, lang_coll, emitted=emitted_entities,
       )
       streams["prov"] = emit_prov_triples(record, ddb_uri, GRAPH_PROV, emitted=emitted_entities)
       ```

   - **`scripts/transform/__main__.py`** — CLI entry point
     - Added `--entities-db` CLI arg in io group:
       ```python
       io.add_argument("--entities-db", type=Path, default=None, dest="entities_db",
                       help="Shared cross-run entity-dedup DuckDB; created if absent...")
       ```
     - Added entities DuckDB setup before main loop:
       ```python
       emitted_entities: dict[str, str] = {}
       entities_conn = None
       if args.entities_db:
           try:
               import duckdb as _ddb_ent
               entities_conn = _ddb_ent.connect(str(args.entities_db))
               entities_conn.execute("""
                   CREATE TABLE IF NOT EXISTS emitted_entities (
                       uri         VARCHAR PRIMARY KEY,
                       entity_type VARCHAR NOT NULL
                   )
               """)
               rows = entities_conn.execute(
                   "SELECT uri, entity_type FROM emitted_entities"
               ).fetchall()
               emitted_entities = {uri: etype for uri, etype in rows}
               log.info("Loaded %d emitted entities from %s", len(emitted_entities), args.entities_db)
           except ImportError:
               log.warning("duckdb not available — --entities-db ignored")
           except Exception as exc:
               log.warning("Could not open --entities-db %s: %s", args.entities_db, exc)
       ```
     - Updated `transform_record` call: `emitted_entities=emitted_entities`
     - Added write-back after loop (before `conn.close()`):
       ```python
       if entities_conn is not None:
           entities_conn.executemany(
               "INSERT OR IGNORE INTO emitted_entities VALUES (?, ?)",
               list(emitted_entities.items()),
           )
           entities_conn.close()
           log.info("Wrote %d entities to %s", len(emitted_entities), args.entities_db)
       ```

   - **`scripts/transform/tests/test_transform.py`** — Test file
     - Added `emit_prov_triples` to imports from `transform.emitters`
     - Added `DDB_BASE` to imports from `transform.constants`
     - Added `TestEmitProvTriplesDedup` class (11 tests including 4 URN-format tests):
       - `_RECORD` with `properties.mapping-version: "6.18"`, `properties.dataset-id: "testdataset123"`, `provider-info.provider-ddb-id: "PROVIDERID00000000000000000000000"`
       - `_XSLT_URI = "urn:ddbedm:xslt:6.18"`
       - `_DS_URI = "urn:ddbedm:dataset:testdataset123"`
       - `_PROV_URI = "urn:ddbedm:provider:PROVIDERID00000000000000000000000"`
       - Tests: `test_emitted_none_emits_all`, `test_emitted_dict_populated`, `test_xslt_skipped_when_emitted`, `test_ddb_agent_skipped_when_emitted`, `test_provider_skipped_when_emitted`, `test_dataset_skipped_when_emitted`, `test_cho_linking_always_emitted`
       - URN format tests: `test_xslt_uri_short_prefix`, `test_dataset_uri_short_prefix`, `test_provider_uri_short_prefix`, `test_prov_uris_no_collision_with_entity_bare_id`
     - Added `TestEmitDdbedmTriplesDedup` class (8 tests):
       - `test_agent_skipped_when_emitted`, `test_place_skipped_when_emitted`, `test_concept_skipped_when_emitted`, `test_timespan_skipped_when_emitted`, `test_provided_cho_never_skipped`, `test_emitted_none_emits_all`, `test_second_record_shares_agent`, `test_emitted_dict_populated_with_type`
     - All 159 tests pass

   - **`notes/ddbedm-prov-o-plan.md`** — PROV-O design document
     - Updated URN patterns in node table (§2.1), dedup note, section headers §2.2.3/4/6, and Turtle example (§2.3)
     - All occurrences of old URN patterns replaced via `replace_all`
     - **Pending**: URN convention paragraph still describes old property-chain form

   - **`notes/transform-adr.md`** — Transform architecture decisions
     - Updated URI scheme table, Turtle pattern, and field mapping section headers
     - All occurrences replaced via `replace_all`

   - **`notes/transform-implementation-plan.md`** — Implementation plan
     - Updated node URI table
     - All occurrences replaced via `replace_all`

   - **`notes/transform-script-adr.md`** — Script-level implementation decisions
     - Added Decision 29 (DuckDB-backed cross-run shared-entity dedup)
     - **Pending**: D27 line 597 has stale entity URI scheme (`urn:ddbedm:<ClassName>:<id>` — note says this but code already uses `urn:ddbedm:<id>` without class name)
     - **Pending**: Decision 29 should document the new URN format

   - **`notes/transform-implementation-actual.md`** — As-built documentation
     - Added §11 "Shared-entity deduplication (2026-05-13)" covering mechanism, entity types, DuckDB schema, new CLI flag, code changes, test additions
     - **Pending**: Should add note about URN scheme change

4. Errors and fixes:
   - **`replace_all` then targeted Edit conflict**: After using `replace_all` to replace `urn:ddbedm:properties:dataset-id:` in `ddbedm-prov-o-plan.md`, attempted to also run a targeted edit on the section header `#### 2.2.3 Dataset (urn:ddbedm:properties:dataset-id:<value>)` — got "String to replace not found" because the `replace_all` had already changed it. The section headers are correct (already updated by `replace_all`).
   - **Edit tool old_string indentation mismatch**: First attempt at adding dedup check in `emit_ddbedm_triples` used 8-space indentation (from file display) but actual code used different indentation. Fixed by re-reading the file to get exact indentation (12 spaces) and using `            subj_uri = ...`.
   - **JSON parsing error**: Sample data file `items-excerpt-1000.json` is a JSON array, not JSONL. Fixed by using `json.load()` instead of per-line `json.loads()`.
   - **`transform-adr.md` read required before edit**: First `replace_all` attempt on `transform-adr.md` failed with "File has not been read yet." Fixed by reading the file first.

5. Problem Solving:
   - **Cross-run deduplication**: Solved by a persistent DuckDB table (`emitted_entities`) loaded at startup into an in-memory `dict[str, str]`, used for O(1) lookups during processing, written back with `INSERT OR IGNORE` after the loop.
   - **URN collision prevention**: Solved by using short typed prefixes (`provider:`, `dataset:`, `xslt:`) for PROV-O nodes, while bare entity IDs (Agent/Place/Concept/TimeSpan) use `urn:ddbedm:{id}` without prefix. DDB IDs are purely alphanumeric (no colons), so the colon in the type prefix is an unambiguous discriminator.
   - **Backward compatibility**: `emitted=None` default means all callers (tests, other code) that don't pass the dict get the original always-emit behavior.

6. All user messages:
   - "which part of the transform scripts /Users/mta/Documents/claude/goethe-faust/scripts/transform is responsible for emitting provenance triples?"
   - "check out this script if there is mention of prov" [re: xml2json-recursive.py]
   - "there is also a portion in this script which keeps tracks of the software agent. if the software agent triple has already been emitted, there is no need to emit the descriptive triples repeatedly. can you check?"
   - "plan first what to change, also (there needs to be a duckdb lookup to make this happen, right)? finally, update corresponding notes."
   - "duckdb is needed, because i will be running this script repeatedly on different inputs"
   - "CREATE TABLE IF NOT EXISTS emitted_prov_uris (uri VARCHAR PRIMARY KEY)\n\nThere be a lookup: xslt version number is the key.\n\nthis duckdb should also be used for other entities:\n1. edm:Agent\n2. edm:Place\n3. skos:Concept (from db:Subject, dcterms:Subject).\n\nWhat else?"
   - "one table is better"
   - "also update /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md"
   - "did you also plan the test and fixtures?"
   - "yes" [approving the test plan]
   - "what field/value do you use to dedup agent, place, concept, timespan?" [asking about the dedup key for ddbedm entities; answer: `about` URI from entity block]
   - "I just instructed another session to use urn:ddbedm:<object-id> for all generated urns. how come you still have the property chain names in the urn?"
   - "i would still like it to be urn:ddbedm:<some id> how do we prevent collision? check the schema /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv how we could get the provider ID. Here is sample data /Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json"
   - "i also remove the urn affix from agent, place, concept, timespan, this might also cause some form of collision."
   - "yes, add test cases and update notes: /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md. Check which other note to update based on prov"

7. Pending Tasks:
   - Update URN convention paragraph in `ddbedm-prov-o-plan.md` §2.1 (still describes old property-chain form: "URNs trace the identifier back to its JSON key chain (`urn:ddbedm:<block>:<key>:<value>`)") — needs to describe new short-prefix scheme and collision-prevention rationale
   - Update Decision 29 in `transform-script-adr.md` to document the new URN format (currently says "URI" generically without the new `urn:ddbedm:provider:`, `urn:ddbedm:dataset:`, `urn:ddbedm:xslt:` specifics)
   - Update D27 in `transform-script-adr.md` (line 597): still says `urn:ddbedm:<ClassName>:<id>` but code already uses `urn:ddbedm:<id>` — stale note from before another session removed the class name
   - Update `transform-implementation-actual.md` §11 to mention the URN scheme change

8. Current Work:
   Immediately before the summary request, the session was in the middle of updating notes for the URN scheme change. The bulk `replace_all` operations on `ddbedm-prov-o-plan.md`, `transform-adr.md`, and `transform-implementation-plan.md` successfully replaced all three old URN patterns with new short-prefix forms. The last action attempted was a targeted Edit on the section header `#### 2.2.3 Dataset (urn:ddbedm:properties:dataset-id:<value>)` in `ddbedm-prov-o-plan.md` which returned "String to replace not found" — because the `replace_all` had already updated it. The section headers in `ddbedm-prov-o-plan.md` are already correct.

   The remaining notes updates not yet done:
   - URN convention paragraph in `ddbedm-prov-o-plan.md` §2.1
   - D27 entity URI table in `transform-script-adr.md` (line 597)
   - Decision 29 URN format specifics in `transform-script-adr.md`
   - §11 URN note in `transform-implementation-actual.md`

9. Optional Next Step:
   Continue the notes updates that were in progress. From the user's request: "yes, add test cases and update notes: /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md. Check which other note to update based on prov"

   The identified notes to update were `ddbedm-prov-o-plan.md`, `transform-adr.md`, `transform-implementation-plan.md`, `transform-script-adr.md`, and `transform-implementation-actual.md`. The bulk text replacements for `transform-adr.md` and `transform-implementation-plan.md` are complete. The remaining work is:
   1. Update the URN convention paragraph in `ddbedm-prov-o-plan.md` §2.1 (currently says `urn:ddbedm:<block>:<key>:<value>`, should describe short-prefix scheme and collision rationale)
   2. Update D27 in `transform-script-adr.md` (line 597: `urn:ddbedm:<ClassName>:<id>` → `urn:ddbedm:<id>`)
   3. Add URN format note to Decision 29 in `transform-script-adr.md`
   4. Add URN scheme change note to `transform-implementation-actual.md` §11

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: /Users/mta/.claude/projects/-Users-mta-Documents-claude/0de9cbbf-84af-4e5a-9d27-80f146854276.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.

---

### Assistant *(2026-05-13T17:01:33.643Z)*

Reading the relevant sections of the three files that still need updates.

---

### Assistant *(2026-05-13T17:01:34.075Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"urn:ddbedm\" /Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md | head -40",
  "description": "Find URN occurrences in ddbedm-prov-o-plan.md"
}
```

---

### User *(2026-05-13T17:01:34.159Z)*

**Tool result**
```
47:| Dataset | `dcat:Dataset`, `prov:Entity` | `urn:ddbedm:dataset:<id>` |
48:| XSLT | `prov:SoftwareAgent` | `urn:ddbedm:xslt:<ver>` |
49:| Provider | `prov:Agent`, `foaf:Organization` | `urn:ddbedm:provider:<id>` |
52:**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key
53:chain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without
56:**Shared node deduplication**: The four shared nodes (Dataset, XSLT, DDB Agent, Provider) have stable URIs that recur across records and sector files. Their descriptive triples are emitted only on first encounter per run via an `emitted: dict[str, str]` guard in `emit_prov_triples`. With `--entities-db`, the dict is persisted to DuckDB across runs; without it, deduplication is within-run only. The per-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted. The XSLT URI is derived from the version number (`urn:ddbedm:xslt:{ver}`), so the version number is the effective lookup key at the code level.
117:#### 2.2.3 Dataset (`urn:ddbedm:dataset:<value>`)
127:#### 2.2.4 XSLT (`urn:ddbedm:xslt:<value>`)
142:#### 2.2.6 Provider (`urn:ddbedm:provider:<value>`)
187:        <urn:ddbedm:dataset:76409877634279609sQOu> ;
189:        <urn:ddbedm:xslt:6.18> ;
196:<urn:ddbedm:dataset:76409877634279609sQOu>
202:        <urn:ddbedm:provider:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .
206:<urn:ddbedm:xslt:6.18>
219:<urn:ddbedm:provider:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
```

---

### Assistant *(2026-05-13T17:01:35.245Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"urn:ddbedm\\|D27\\|Decision 27\\|Decision 29\\|ClassName\" /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md | head -40",
  "description": "Find URN and decision occurrences in transform-script-adr.md"
}
```

---

### User *(2026-05-13T17:01:35.305Z)*

**Tool result**
```
480:**Rationale**: `ddbedm` is consistent with the `urn:ddbedm:` URN convention used throughout the PROV-O graph (D12). The `ddbedm` graph is emitted as priority #1 — a faithful baseline from which `mocho` and `work` graphs can be re-derived or verified. Separating raw EDM from aligned mocho triples allows independent re-runs of the alignment step without re-ingesting source data.
588:## Decision 27: Bare-ID URI minting for malformed `about` values
597:| All others (`Aggregation`, `Agent`, `Event`, `Place`, `WebResource`, …) | `urn:ddbedm:<ClassName>:<id>` | `urn:ddbedm:Agent:O5XUSBA7IPKSXYUTN6EQNWK62BQRF7GN` |
603:**Rationale**: `ProvidedCHO` bare IDs are DDB item identifiers — the canonical DDB item URI scheme (`…/item/<id>`) is the correct dereferenceable form and aligns with the `owl:sameAs` link emitted in the mocho graph. All other entity types have no canonical HTTP URI, so the `urn:ddbedm:` scheme encodes both the namespace and the entity class, making the source unambiguous without requiring a dereferenceable endpoint. Consistent with `export-s2-plan.md §4.3`.
639:## Decision 29: DuckDB-backed cross-run shared-entity deduplication
```

---

### Assistant *(2026-05-13T17:01:35.847Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"urn:ddbedm\\|URN\\|§11\\|scheme\" /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md | head -30",
  "description": "Find URN and §11 occurrences in transform-implementation-actual.md"
}
```

---

### User *(2026-05-13T17:01:35.909Z)*

**Tool result**
```
276:| `test_bare_id_hastype_expanded` | `urn:ddbedm:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |
283:| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id` (`urn:ddbedm:<id>`) |
```

---

### Assistant *(2026-05-13T17:01:38.371Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "offset": 50,
  "limit": 10
}
```

---

### User *(2026-05-13T17:01:38.385Z)*

**Tool result**
```
50	| DDB | `prov:Agent`, `foaf:Organization` | `<http://www.deutsche-digitale-bibliothek.de>` (fixed) |
51	
52	**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key
53	chain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without
54	requiring a dereferenceable endpoint.
55	
56	**Shared node deduplication**: The four shared nodes (Dataset, XSLT, DDB Agent, Provider) have stable URIs that recur across records and sector files. Their descriptive triples are emitted only on first encounter per run via an `emitted: dict[str, str]` guard in `emit_prov_triples`. With `--entities-db`, the dict is persisted to DuckDB across runs; without it, deduplication is within-run only. The per-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted. The XSLT URI is derived from the version number (`urn:ddbedm:xslt:{ver}`), so the version number is the effective lookup key at the code level.
57	
58	### 2.2 JSON field → triple mapping
59	
```

---

### Assistant *(2026-05-13T17:01:39.311Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "offset": 585,
  "limit": 70
}
```

---

### User *(2026-05-13T17:01:39.318Z)*

**Tool result**
```
585	
586	---
587	
588	## Decision 27: Bare-ID URI minting for malformed `about` values
589	
590	**Context**: Some `edm.RDF.*.about` values (and `.resource` cross-references) contain only the bare 32-character DDB internal ID rather than a full HTTP URI. `px.NamedNode()` rejects bare strings — minting is required before any triple can be emitted.
591	
592	**Decision**: Apply the same scheme used in `export_ddb.py §4.3`:
593	
594	| Entity type | Minting rule | Example |
595	|---|---|---|
596	| `ProvidedCHO` | `http://www.deutsche-digitale-bibliothek.de/item/<id>` | `…/item/225LOCJZSZLTA4DCUBFIHG72SPN7JTQZ` |
597	| All others (`Aggregation`, `Agent`, `Event`, `Place`, `WebResource`, …) | `urn:ddbedm:<ClassName>:<id>` | `urn:ddbedm:Agent:O5XUSBA7IPKSXYUTN6EQNWK62BQRF7GN` |
598	
599	Detection: value does not start with `http` or `urn`.
600	
601	For `.resource` cross-references, the target entity type is resolved from a per-record lookup of all `about` values built before traversal begins.
602	
603	**Rationale**: `ProvidedCHO` bare IDs are DDB item identifiers — the canonical DDB item URI scheme (`…/item/<id>`) is the correct dereferenceable form and aligns with the `owl:sameAs` link emitted in the mocho graph. All other entity types have no canonical HTTP URI, so the `urn:ddbedm:` scheme encodes both the namespace and the entity class, making the source unambiguous without requiring a dereferenceable endpoint. Consistent with `export-s2-plan.md §4.3`.
604	
605	---
606	
607	## Decision 28: Post-processing NQ split → per-graph NT files
608	
609	**Decision**: The transform emits `.nq` output unchanged (D22). Immediately after the transform, a post-processing step (`scripts/split_nq.py`) splits each `.nq` file into one `.nt` file per named graph. The `.nt` files are the working intermediates for sanitization, validation, and debugging. NQ wrapping is deferred to QLever load time.
610	
611	File naming: the output `.nt` slug matches the graph name (e.g. `ddbedm.nt`, `mocho.nt`, `prov.nt`); the load-time wrapper derives the full graph IRI mechanically (`…/graph/<slug>`).
612	
613	**Rationale**:
614	1. **NT is simpler to sanitize**: no graph column; grep/awk/sed operate directly on `<subject> <predicate> <object> .` lines without stripping the fourth element first.
615	2. **Late-binding graph IRI**: renaming a named graph (e.g. schema-breaking release, IRI migration) requires changing only the load-time wrapper — not the `.nt` files.
616	3. **No generator change**: the transform already routes triples to per-graph output streams (D20, D22). Post-processing the `.nq` output is a small script; the generator is not touched.
617	
618	**Post-processing script** (`scripts/split_nq.py`):
619	
620	```python
621	from collections import defaultdict
622	from pathlib import Path
623	
624	def split_nq(nq_path: Path, out_dir: Path):
625	    graphs: dict[str, list[str]] = defaultdict(list)
626	    with open(nq_path) as f:
627	        for line in f:
628	            parts = line.rstrip(" .\n").rsplit(" ", 1)
629	            graphs[parts[1]].append(parts[0] + " .\n")
630	    for graph_iri, triples in graphs.items():
631	        slug = graph_iri.strip("<>").split("/")[-1]
632	        (out_dir / f"{slug}.nt").write_text("".join(triples))
633	```
634	
635	**Amends D22** on the file format question only: D22 governs the generator (NQ output, graph IRI on every emitted line). This decision governs what happens to the `.nq` files after generation; D22 remains in effect for the transform itself.
636	
637	---
638	
639	## Decision 29: DuckDB-backed cross-run shared-entity deduplication
640	
641	**Decision**: Descriptive triples for shared named entities are emitted at most once per URI across all transform runs, tracked via a persistent DuckDB table (`emitted_entities`).
642	
643	**Entity types deduplicated**:
644	
645	| entity_type value | Source | Scope of sharing |
646	|---|---|---|
647	| `prov_xslt` | `properties.mapping-version` → XSLT URI | All records with same mapping version |
648	| `prov_ddb` | `DDB_BASE` (fixed) | Every record in every run |
649	| `prov_provider` | `provider-info.provider-ddb-id` → Provider URI | All records from same institution |
650	| `prov_dataset` | `properties.dataset-id` → Dataset URI | All records in same delivery batch |
651	| `edm_agent` | `edm.RDF.Agent[].about` | GND agent URIs shared across records |
652	| `edm_place` | `edm.RDF.Place[].about` | GND place URIs shared across records |
653	| `skos_concept` | `edm.RDF.Concept[].about` | Subject concept URIs shared across records |
654	| `edm_timespan` | `edm.RDF.TimeSpan[].about` | Time period URIs shared across records |
```

---

### Assistant *(2026-05-13T17:01:39.441Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "offset": 270,
  "limit": 50
}
```

---

### User *(2026-05-13T17:01:39.449Z)*

**Tool result**
```
270	
271	| Test | Assertion |
272	|---|---|
273	| `test_multi_uri_place_splits` | Two separate `Place` subject IRIs emitted; no IRI containing a space |
274	| `test_multi_uri_current_location_splits` | Two separate triples for `currentLocation` |
275	| `test_br_tag_normalized` | `\\n` appears in the relevant literal; no `<br` substring in any triple |
276	| `test_bare_id_hastype_expanded` | `urn:ddbedm:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |
277	
278	### 7.5 Unit test additions
279	
280	| Class / function | Covers |
281	|---|---|
282	| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\n` |
283	| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id` (`urn:ddbedm:<id>`) |
284	| `TestEmitSubjectTriplesMultiUri` | `"URI1 URI2"` → two `dcterms:subject` triples |
285	| `TestEmitHastypeTriplesMultiUri` | Same for `edm:hasType` |
286	| `TestEmitCreatorTriplesMultiUri` | Two URIs → two Track-1 triples |
287	| `TestEmitCreatorTriplesBareId` | Bare ID expanded; `agent_uri` sanitized |
288	| `TestEmitContributorTriplesMultiUri` | Two URIs → two `(cho, prop, uri)` triples |
289	| `TestEmitContributorTriplesBareId` | Bare ID expanded via param |
290	| `TestEmitProvTriplesIsil` | `provider_isil` with unsafe chars → sanitized in `MOCHO_ISIL` triple |
291	| `TestEmitPlaceStubsSplitAbout` | Space-separated `about` → only first part used as subject |
292	| `TestEmitAggregationSplitUri` | `isShownAt.resource = "URI1 URI2"` → two `dcterms:source` triples |
293	
294	### 7.6 Validation run — goethe-faust corpus (2026-05-07)
295	
296	Full run on `data/items-all-goethe-faust.json` (115,432 records) after all audit fixes. Output: `output/transform/20260507_190805/`.
297	
298	| Metric | POC (2026-05-06) | Post-audit (2026-05-07) | Delta |
299	|---|---|---|---|
300	| Records processed | 115,432 | 115,432 | — |
301	| Triples total | 14,713,376 | 14,764,352 | +50,976 |
302	| ddbedm | 8,957,262 | 8,957,734 | +472 |
303	| **mocho** | **1,898,754** | **1,950,504** | **+51,750** |
304	| prov | 3,857,360 | 3,856,114 | −1,246 |
305	| Errors | 0 | 0 | — |
306	| fallback_d9 | 0 | 0 | — |
307	| uri_sanitized | 29 | 29 | — |
308	| uri_split | 4,188 | 2,685 | −1,503 |
309	| uri_about_split | 1,309 | 1,309 | — |
310	
311	**mocho +51,750** breaks down as:
312	- `edm:currentLocation` — 31,837 new triples (property moved from generic loop to `emit_current_location_triples`; IRI-with-label-stub pattern)
313	- Creator/contributor bare-ID expansions, multi-URI splits, and subject/hasType label stubs now handled correctly in special emitters account for the remainder
314	
315	**uri_split −1,503**: some multi-URI splits previously counted via the generic loop (`value_to_nt_obj`) are now handled in special emitters via `resource_uris()` and tracked separately; the net split count is lower because `currentLocation` URIs (many multi-value) are no longer double-counted.
316	
317	**prov −1,246**: minor change due to PROV provider node deduplication; no logic change — variance from record ordering in input.
318	
319	---
```

---

### Assistant *(2026-05-13T17:01:49.323Z)*

Let me read the rest of D29 and the end of §11 in `transform-implementation-actual.md`.

---

### Assistant *(2026-05-13T17:01:49.585Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "offset": 654,
  "limit": 50
}
```

---

### User *(2026-05-13T17:01:49.592Z)*

**Tool result**
```
654	| `edm_timespan` | `edm.RDF.TimeSpan[].about` | Time period URIs shared across records |
655	
656	**Schema** (single shared DuckDB file, not per-run):
657	```sql
658	CREATE TABLE IF NOT EXISTS emitted_entities (
659	    uri         VARCHAR PRIMARY KEY,
660	    entity_type VARCHAR NOT NULL
661	)
662	```
663	
664	**Runtime pattern**: at startup, load all rows into an in-memory `dict[str, str]` (`uri → entity_type`); check membership during processing; after the loop, `INSERT OR IGNORE` all entries back (idempotent, handles pre-existing rows).
665	
666	**Why not a per-record DuckDB lookup**: the number of unique shared-entity URIs is small (tens to low thousands). Loading into memory at startup is O(1) per record; a DuckDB round-trip per record would add I/O overhead at 18.5M scale.
667	
668	**Why not in-memory set only**: the transform is run once per sector file (s1–s7) as separate OS processes. An in-memory set resets between runs, so DDB Agent and XSLT triples would be re-emitted in every sector's output. The DuckDB file survives across runs.
669	
670	**`--entities-db` is optional**: if omitted, a fresh empty `dict` is used — within-run dedup only, no persistence. The `emitted` parameter defaults to `None` in both `emit_prov_triples` and `emit_ddbedm_triples`, which falls back to always-emit (backward-compatible for tests and other callers).
671	
672	**Per-CHO triples are never deduplicated**: linking triples from the CHO to shared nodes (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are unique per record and emitted unconditionally.
673	
674	---
675	
676	## Decision 14: Manual curation over automated schema alignment
677	
678	**Decision**: The alignment table (`alignment_ddbedm_mocho.csv`) and all dispatch
679	logic (htype lookup, dc:type × sector dispatch, sparte × mediatype class
680	assignment) were produced by manual curation and explicit decision records (D1–D13),
681	not by automated schema-matching algorithms [Rahm & Bernstein 2001; Shvaiko &
682	Euzenat 2013].
683	
684	**Alternatives considered**:
685	
686	- *LLM-assisted alignment* [Hertling & Paulheim 2023; Giglou et al. 2023]: Feed
687	  source JSON keys + sample values + target ontology namespace documentation to an
688	  LLM and generate `(entity_type, json_key) → predicate IRI` candidate mappings.
689	  Would have covered approximately 60–70% of the 1:1 property mappings in
690	  `alignment_ddbedm_mocho.csv` automatically — cases with clear semantic
691	  correspondences (`prefLabel → skos:prefLabel`, `lat → geo:lat`, `begin →
692	  schema:startDate`). Cannot produce the conditional class dispatch logic (htype ×
693	  sparte × mediatype → rdf:type) without domain knowledge of DDB's institutional
694	  structure and the mocho WEMI model. Useful for bootstrap; insufficient for the
695	  semantically significant part of the alignment.
696	
697	- *Instance-based statistical alignment* [Doan et al. 2002; Madhavan et al. 2001]:
698	  Analyze value distributions per JSON key — IRI vs literal, date format patterns,
699	  language tags, value overlap with target ontology IRIs — to narrow predicate
700	  candidates automatically. Good at datatype inference and distinguishing
701	  IRI-valued from literal-valued properties. Cannot distinguish semantically close
702	  predicates that share the same datatype (e.g. `rdaa:P50067` date-of-birth vs
703	  `rdaa:P50068` date-of-death both accept date literals; `rdaw:P10088` vs
```

---

### Assistant *(2026-05-13T17:01:50.262Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"^## \\|^### \\|^#### \" /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md | tail -20",
  "description": "Find section headers in transform-implementation-actual.md"
}
```

---

### User *(2026-05-13T17:01:50.325Z)*

**Tool result**
```
325:### 8.1 Bug 1 — `emit_creator_triples`: `isinstance(pref, str)` always False
339:### 8.2 Bug 2 — `emit_contributor_triples`: no `agents_index`, label from `val.get("$")`
352:### 8.3 Test additions
369:### 8.4 Validation run — goethe-faust corpus (2026-05-08)
394:## 9. `hierarchyType` URI fixes (2026-05-12)
400:### 9.1 Bug 1 — wrong vocnet URI form
406:### 9.2 Bug 2 — space-separated multi-value treated as single code
414:### 9.3 Test additions
430:## 10. BCP 47 language tag normalization (2026-05-12)
436:### 10.1 Validation approach
445:### 10.2 Code changes
468:### 10.3 Whitespace-in-lang bug
486:### 10.4 Test additions
500:## 11. Shared-entity deduplication (2026-05-13)
504:### 11.1 Mechanism
523:### 11.2 DuckDB schema
534:### 11.3 New CLI flag
540:### 11.4 Code changes
548:### 11.5 Test additions
558:## 12. Full-corpus run plan
```

---

### Assistant *(2026-05-13T17:01:52.455Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "offset": 500,
  "limit": 65
}
```

---

### User *(2026-05-13T17:01:52.459Z)*

**Tool result**
```
500	## 11. Shared-entity deduplication (2026-05-13)
501	
502	Descriptive triples for shared named entities are emitted at most once per URI across all transform runs. Without this, every sector run re-emits identical triples for the DDB Agent, XSLT SoftwareAgent, provider institutions, datasets, and all GND agents/places/concepts/timespans that appear in multiple records.
503	
504	### 11.1 Mechanism
505	
506	An `emitted: dict[str, str]` (`uri → entity_type`) is passed into both `emit_prov_triples` and `emit_ddbedm_triples`. Each shared-node block checks membership before emitting and registers the URI on first emission. The dict is initialized in `__main__.py` before the record loop (empty = within-run dedup only). With `--entities-db PATH`, it is loaded from DuckDB at startup and written back with `INSERT OR IGNORE` after the loop, enabling cross-run dedup across sector files.
507	
508	**Entity types tracked**:
509	
510	| entity_type | Source |
511	|---|---|
512	| `prov_xslt` | `properties.mapping-version` → XSLT SoftwareAgent URI |
513	| `prov_ddb` | Fixed `DDB_BASE` URI |
514	| `prov_provider` | `provider-info.provider-ddb-id` → Provider Agent URI |
515	| `prov_dataset` | `properties.dataset-id` → Dataset URI |
516	| `edm_agent` | `edm.RDF.Agent[].about` |
517	| `edm_place` | `edm.RDF.Place[].about` |
518	| `skos_concept` | `edm.RDF.Concept[].about` |
519	| `edm_timespan` | `edm.RDF.TimeSpan[].about` |
520	
521	Per-CHO linking triples (`prov:wasDerivedFrom`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `dcterms:hasVersion`, `dcterms:references`) are always emitted unconditionally.
522	
523	### 11.2 DuckDB schema
524	
525	```sql
526	CREATE TABLE IF NOT EXISTS emitted_entities (
527	    uri         VARCHAR PRIMARY KEY,
528	    entity_type VARCHAR NOT NULL
529	)
530	```
531	
532	Separate file from `werk-staging.duckdb`; shared across all sector runs in a production campaign. Managed by the caller — not auto-created in the run output directory.
533	
534	### 11.3 New CLI flag
535	
536	| Flag | Default | Description |
537	|---|---|---|
538	| `--entities-db PATH` | _(none)_ | Shared cross-run entity-dedup DuckDB. Omit for within-run dedup only. |
539	
540	### 11.4 Code changes
541	
542	| File | Change |
543	|---|---|
544	| `emitters.py` | Add `_DEDUP_ENTITY_TYPES` dict; add `emitted` param to `emit_ddbedm_triples` and `emit_prov_triples`; guard 4 PROV-O shared-node blocks + entity loop in `emit_ddbedm_triples` |
545	| `transform.py` | Add `emitted_entities` param to `transform_record`; thread through to both emitters |
546	| `__main__.py` | Add `--entities-db` CLI arg; DuckDB setup/load at startup; pass `emitted_entities` to `transform_record`; batch write-back after loop |
547	
548	### 11.5 Test additions
549	
550	15 new tests across 2 new classes (total: 155).
551	
552	**`TestEmitProvTriplesDedup`** (7 tests): `emitted=None` emits all; dict populated with correct `entity_type` values; each of the 4 shared nodes skipped when URI already in `emitted`; per-CHO linking triples always present even when all shared nodes are pre-emitted.
553	
554	**`TestEmitDdbedmTriplesDedup`** (8 tests): Agent/Place/Concept/TimeSpan skipped when URI already in `emitted`; `ProvidedCHO` never skipped (not in `_DEDUP_ENTITY_TYPES`); `emitted=None` emits all; second call with same `emitted` dict emits 0 agent triples; dict populated with correct `entity_type` after first call.
555	
556	---
557	
558	## 12. Full-corpus run plan
559	
560	The production orchestrator is `scripts/run-transform-sector.sh`. It splits the SQLite table into `--workers` chunks, launches one `python -m transform` OS process per chunk, waits for all to finish, then merges.
561	
562	```bash
563	# one sector, all defaults (50 workers, merge stats only):
564	bash scripts/run-transform-sector.sh --merge --sector s2
```

---

### Assistant *(2026-05-13T17:02:02.822Z)*

Now I have all the context. Making all four remaining updates in parallel.

---

### Assistant *(2026-05-13T17:02:06.886Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md",
  "old_string": "**URI convention**: `urn:ddbedm:` URNs trace the identifier back to its JSON key\nchain (`urn:ddbedm:<block>:<key>:<value>`), making the source unambiguous without\nrequiring a dereferenceable endpoint.",
  "new_string": "**URI convention**: PROV-O shared nodes use short typed-prefix URNs — `urn:ddbedm:dataset:<id>`, `urn:ddbedm:xslt:<ver>`, `urn:ddbedm:provider:<id>` — rather than a property-chain form. The type prefix (`dataset:`, `xslt:`, `provider:`) is a collision guard: bare DDB entity IDs (Agent, Place, Concept, TimeSpan) are minted as `urn:ddbedm:<id>` without a class name, and DDB IDs are 32-character alphanumeric strings (no colons), so the colon after the type prefix is an unambiguous discriminator. None of these URNs are dereferenceable endpoints; they are stable, opaque identifiers scoped to the `urn:ddbedm:` namespace."
}
```

---

### Assistant *(2026-05-13T17:02:10.108Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "old_string": "| All others (`Aggregation`, `Agent`, `Event`, `Place`, `WebResource`, …) | `urn:ddbedm:<ClassName>:<id>` | `urn:ddbedm:Agent:O5XUSBA7IPKSXYUTN6EQNWK62BQRF7GN` |",
  "new_string": "| All others (`Aggregation`, `Agent`, `Event`, `Place`, `WebResource`, …) | `urn:ddbedm:<id>` | `urn:ddbedm:O5XUSBA7IPKSXYUTN6EQNWK62BQRF7GN` |"
}
```

---

### User *(2026-05-13T17:13:56.957Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### User *(2026-05-13T17:18:14.230Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T17:18:17.901Z)*

Now update the D27 rationale paragraph and add URN format specifics to D29:

---

### Assistant *(2026-05-13T17:18:23.085Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "old_string": "**Rationale**: `ProvidedCHO` bare IDs are DDB item identifiers — the canonical DDB item URI scheme (`…/item/<id>`) is the correct dereferenceable form and aligns with the `owl:sameAs` link emitted in the mocho graph. All other entity types have no canonical HTTP URI, so the `urn:ddbedm:` scheme encodes both the namespace and the entity class, making the source unambiguous without requiring a dereferenceable endpoint. Consistent with `export-s2-plan.md §4.3`.",
  "new_string": "**Rationale**: `ProvidedCHO` bare IDs are DDB item identifiers — the canonical DDB item URI scheme (`…/item/<id>`) is the correct dereferenceable form and aligns with the `owl:sameAs` link emitted in the mocho graph. All other entity types have no canonical HTTP URI; the `urn:ddbedm:` prefix scopes them to the namespace without encoding a class name. PROV-O shared nodes (Dataset, XSLT, Provider) use a typed-prefix form (`urn:ddbedm:dataset:<id>`, `urn:ddbedm:xslt:<ver>`, `urn:ddbedm:provider:<id>`) as a collision guard — since DDB IDs are purely alphanumeric (no colons), the colon after the type prefix is an unambiguous discriminator. Consistent with `export-s2-plan.md §4.3` and D29."
}
```

---

### User *(2026-05-13T17:19:12.013Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T17:19:19.028Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md",
  "old_string": "**Schema** (single shared DuckDB file, not per-run):",
  "new_string": "**PROV-O node URI scheme**: shared PROV-O nodes use typed-prefix URNs to prevent collision with bare entity IDs (`urn:ddbedm:<id>`):\n\n| Node | URI |\n|---|---|\n| Dataset | `urn:ddbedm:dataset:<properties.dataset-id>` |\n| XSLT | `urn:ddbedm:xslt:<properties.mapping-version>` |\n| Provider | `urn:ddbedm:provider:<provider-info.provider-ddb-id>` |\n| DDB Agent | `<http://www.deutsche-digitale-bibliothek.de>` (fixed HTTP URI, not URN) |\n\nDDB IDs are 32-character alphanumeric strings (no colons). The colon after the type prefix (`dataset:`, `xslt:`, `provider:`) is therefore an unambiguous discriminator between PROV-O nodes and bare entity URIs.\n\n**Schema** (single shared DuckDB file, not per-run):"
}
```

---

### User *(2026-05-13T17:22:52.824Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T17:22:56.982Z)*

Now add the URN scheme subsection to `transform-implementation-actual.md` §11:

---

### Assistant *(2026-05-13T17:23:06.923Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "old_string": "### 11.5 Test additions\n\n15 new tests across 2 new classes (total: 155).\n\n**`TestEmitProvTriplesDedup`** (7 tests): `emitted=None` emits all; dict populated with correct `entity_type` values; each of the 4 shared nodes skipped when URI already in `emitted`; per-CHO linking triples always present even when all shared nodes are pre-emitted.\n\n**`TestEmitDdbedmTriplesDedup`** (8 tests): Agent/Place/Concept/TimeSpan skipped when URI already in `emitted`; `ProvidedCHO` never skipped (not in `_DEDUP_ENTITY_TYPES`); `emitted=None` emits all; second call with same `emitted` dict emits 0 agent triples; dict populated with correct `entity_type` after first call.",
  "new_string": "### 11.5 PROV-O URN scheme change\n\nPROV-O shared nodes switched from a verbose property-chain URN form to short typed-prefix URNs:\n\n| Node | Old form | New form |\n|---|---|---|\n| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `urn:ddbedm:dataset:<id>` |\n| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `urn:ddbedm:xslt:<ver>` |\n| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `urn:ddbedm:provider:<id>` |\n\n**Collision guard**: bare DDB entity IDs (Agent, Place, Concept, TimeSpan) are minted as `urn:ddbedm:<id>` without a class name. DDB IDs are 32-character alphanumeric strings (no colons), so `urn:ddbedm:dataset:X` vs `urn:ddbedm:X` are unambiguous — the colon after the type segment is the discriminator.\n\n### 11.6 Test additions\n\n19 new tests across 2 new classes (total: 159).\n\n**`TestEmitProvTriplesDedup`** (11 tests): `emitted=None` emits all; dict populated with correct `entity_type` values; each of the 4 shared nodes skipped when URI already in `emitted`; per-CHO linking triples always present even when all shared nodes are pre-emitted; 4 URN-format tests asserting the new short-prefix form and no collision between PROV-O nodes and bare entity IDs.\n\n**`TestEmitDdbedmTriplesDedup`** (8 tests): Agent/Place/Concept/TimeSpan skipped when URI already in `emitted`; `ProvidedCHO` never skipped (not in `_DEDUP_ENTITY_TYPES`); `emitted=None` emits all; second call with same `emitted` dict emits 0 agent triples; dict populated with correct `entity_type` after first call."
}
```

---

### User *(2026-05-13T21:29:10.617Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

### Assistant *(2026-05-13T21:29:17.529Z)*

All four pending notes updates are done:

- **`ddbedm-prov-o-plan.md` §2.1**: URN convention paragraph now describes the short-prefix scheme and the alphanumeric-ID collision guard, replacing the old property-chain description.
- **`transform-script-adr.md` D27**: Entity URI table row updated to `urn:ddbedm:<id>` (no class name); rationale paragraph updated to match and cross-references D29.
- **`transform-script-adr.md` D29**: New "PROV-O node URI scheme" block added before the schema, listing the three typed-prefix URNs and the collision-guard rationale.
- **`transform-implementation-actual.md` §11**: New §11.5 documents the old → new URN form for all three PROV-O nodes, the collision guard, and the test count was corrected to 159 (19 new tests across 2 classes, split 11+8).

---
