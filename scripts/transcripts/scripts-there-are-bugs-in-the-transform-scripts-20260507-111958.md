# Transcript: ef8b247d-8555-42ed-bcfa-d0e1dab38211

**Project:** /Users/mta/Documents/claude/goethe-faust/scripts  
**Messages:** 516

---

### User *(2026-05-07T11:19:58.078Z)*

There are bugs in the transform scripts:

1. the urn:fix did not seem to be carried over

`<http://www.deutsche-digitale-bibliothek.de/item/34TALB4SALQ5PPR3O5FG42GEZP3CA6IB> <http://purl.org/dc/terms/subject> <JJPUNJH2HPP22XUFLUGAQ37K3E4JN6C6>`

2. why does gemea resource emit `edm:hasMet`?

`<https://gemea.ise.fiz-karlsruhe.de/mocho/VLI2NURFSVBOMIRUFKQWNZYYCNA3444C> <http://www.europeana.eu/schemas/edm/hasMet> <TXOBF6SB26VQ4CP5HZ6VTDUJFBW2SH3V> .`

---

### Assistant *(2026-05-07T11:20:04.940Z)*

Let me look at the transform scripts to find both issues.

---

### Assistant *(2026-05-07T11:20:05.908Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude -path \"*/transform*\" -name \"*.py\" | head -20",
  "description": "Find transform Python scripts"
}
```

---

### User *(2026-05-07T11:20:06.151Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/sqlite_export.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/loaders.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__init__.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/__init__.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/optimization_tf.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/modeling_outputs.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/configuration_utils.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/modeling_flash_attention_utils.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/image_processing_utils_fast.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/image_utils.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/tokenization_utils.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/convert_graph_to_onnx.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/modeling_rope_utils.py
/Users/mta/Documents/claude/.venv/lib/python3.9/site-packages/transformers/convert_tf_hub_seq_to_seq_bert_to_pytorch.py
```

---

### Assistant *(2026-05-07T11:20:06.273Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude -path \"*/scripts/transform*\" | head -20",
  "description": "Find transform script directory"
}
```

---

### User *(2026-05-07T11:20:06.510Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform
/Users/mta/Documents/claude/goethe-faust/scripts/transform/sqlite_export.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/loaders.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__init__.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/README.md
/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py
/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/__init__.py
```

---

### Assistant *(2026-05-07T11:20:10.279Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"urn\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py | head -30",
  "description": "Search for URN handling in utils.py"
}
```

---

### User *(2026-05-07T11:20:10.326Z)*

**Tool result**
```
20:    return _IRI_UNSAFE_RE.sub(lambda m: f"%{ord(m.group()):02X}", iri)
24:    """Return one N-Quads line."""
25:    return f"{s_nt} {p_nt} {o_nt} <{graph_iri}> ."
31:        return []
33:        return [val]
35:        return val
36:    return []
43:            return base + curie[len(prefix) + 1:]
44:    return curie
48:    """Collapse a full IRI to a CURIE using _PREFIXES; return IRI unchanged if no match."""
51:            return f"{prefix}:{iri[len(base):]}"
52:    return iri
56:    """Return the minted GeMeA mocho CHO URI for a 32-char DDB object ID (D22)."""
57:    return GEMEA_BASE + obj_id
64:    All other entity types → urn:ddbedm:<ClassName>:<id>.
65:    Full URIs and URNs are returned unchanged.
67:    if raw_id.startswith(("http", "urn")):
68:        return raw_id
70:        return DDB_ITEM_BASE + raw_id
71:    return f"urn:ddbedm:{entity_class}:{raw_id}"
76:    return (s.replace("\\", "\\\\")
98:        return []
100:        return [f'"{_escape_literal(val)}"'] if val else []
105:        return result
118:            return result
121:            return []
125:            return [f'"{escaped}"@{lang}']
126:        return [f'"{escaped}"']
127:    return []
135:    All other values returned unchanged.
```

---

### Assistant *(2026-05-07T11:20:11.604Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"hasMet\\|edm:hasMet\\|subject\\|urn\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py | head -40",
  "description": "Search for hasMet and URN in emitters.py"
}
```

---

### User *(2026-05-07T11:20:11.647Z)*

**Tool result**
```
33:    Returns (lines, class_ctr, pred_ctr, sani_ctr) where sani_ctr tracks
71:    return lines, class_ctr, pred_ctr, sani_ctr
98:    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
99:    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
100:    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
195:    return lines
211:    Returns (lines, target_class_full_iri, wemi, dispatch_flags).
269:    return lines, primary_class, wemi, {"htype_used": htype_used, "fallback": is_fallback}
272:def emit_subject_triples(
274:    subject_vals: list,
278:    """Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended)."""
281:    for val in subject_vals:
306:    return lines
354:    return lines
396:    return lines
425:    return lines
442:    return lines
448:        return None
484:    return {
509:    """Emit all mocho-graph triples for one record (§6.3). Returns (lines, target_class, wemi, dispatch_flags).
601:    subject_vals: list = []
603:        subject_vals.extend(coerce_list(cho.get(skey)))
660:    if subject_vals:
661:        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri)
662:        lines.extend(_subject_lines)
663:        _track_nqlist(_subject_lines)
681:    return lines, target_class, wemi, dispatch_flags
```

---

### Assistant *(2026-05-07T11:20:14.160Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py"
}
```

---

### User *(2026-05-07T11:20:14.210Z)*

**Tool result**
```
1	"""Utility functions: N-Quads formatting, URI minting, value normalisation."""
2	
3	from __future__ import annotations
4	
5	import re
6	from collections import Counter
7	
8	from .constants import (
9	    AgentDict, NQuad, NQList,
10	    GEMEA_BASE, DDB_ITEM_BASE,
11	    _PREFIXES, _MEDIATYPE_PREFIX, _SECTOR_PREFIX,
12	)
13	
14	# Characters forbidden inside N-Triples IRI references (RFC 3987 + NT spec)
15	_IRI_UNSAFE_RE = re.compile(r'[\x00-\x20<>"{}|\\^`\x7f]')
16	
17	
18	def _sanitize_iri(iri: str) -> str:
19	    """Percent-encode characters illegal inside NT IRI references."""
20	    return _IRI_UNSAFE_RE.sub(lambda m: f"%{ord(m.group()):02X}", iri)
21	
22	
23	def make_nq(s_nt: str, p_nt: str, o_nt: str, graph_iri: str) -> NQuad:
24	    """Return one N-Quads line."""
25	    return f"{s_nt} {p_nt} {o_nt} <{graph_iri}> ."
26	
27	
28	def coerce_list(val: object) -> list:
29	    """Normalise None/dict/list to a list."""
30	    if val is None:
31	        return []
32	    if isinstance(val, dict):
33	        return [val]
34	    if isinstance(val, list):
35	        return val
36	    return []
37	
38	
39	def _expand_prefix(curie: str) -> str:
40	    """Expand a CURIE (e.g. 'rdam:P30134') to a full IRI."""
41	    for prefix, base in _PREFIXES.items():
42	        if curie.startswith(prefix + ":"):
43	            return base + curie[len(prefix) + 1:]
44	    return curie
45	
46	
47	def _to_curie(iri: str) -> str:
48	    """Collapse a full IRI to a CURIE using _PREFIXES; return IRI unchanged if no match."""
49	    for prefix, base in _PREFIXES.items():
50	        if iri.startswith(base):
51	            return f"{prefix}:{iri[len(base):]}"
52	    return iri
53	
54	
55	def mint_cho_uri(obj_id: str) -> str:
56	    """Return the minted GeMeA mocho CHO URI for a 32-char DDB object ID (D22)."""
57	    return GEMEA_BASE + obj_id
58	
59	
60	def mint_bare_id(entity_class: str, raw_id: str) -> str:
61	    """Expand a bare 32-char ID to a full URI (D27).
62	
63	    ProvidedCHO bare IDs → DDB item URI.
64	    All other entity types → urn:ddbedm:<ClassName>:<id>.
65	    Full URIs and URNs are returned unchanged.
66	    """
67	    if raw_id.startswith(("http", "urn")):
68	        return raw_id
69	    if entity_class == "ProvidedCHO":
70	        return DDB_ITEM_BASE + raw_id
71	    return f"urn:ddbedm:{entity_class}:{raw_id}"
72	
73	
74	def _escape_literal(s: str) -> str:
75	    """Escape characters illegal in N-Triples/N-Quads literal content."""
76	    return (s.replace("\\", "\\\\")
77	             .replace('"', '\\"')
78	             .replace("\n", "\\n")
79	             .replace("\r", "\\r")
80	             .replace("\t", "\\t"))
81	
82	
83	def value_to_nt_obj(val: object, sani_ctr: Counter | None = None) -> list[str]:
84	    """Convert a JSONL field value to a list of N-Triples object strings.
85	
86	    Handles all value shapes produced by the DDB EDM JSONL:
87	      None / ""                    → []
88	      str (non-empty)              → ['"escaped"']
89	      list                         → recurse and flatten
90	      {"resource": IRI}            → ["<IRI>"] (IRI percent-encoded if unsafe chars present)
91	      {"lang": L, "$": T}          → ['"T"@L']
92	      {"lang": null, "$": T}       → ['"T"']
93	      {"resource": null, "$": ""}  → []
94	
95	    sani_ctr: if provided, incremented once per IRI that required sanitisation.
96	    """
97	    if val is None:
98	        return []
99	    if isinstance(val, str):
100	        return [f'"{_escape_literal(val)}"'] if val else []
101	    if isinstance(val, list):
102	        result = []
103	        for item in val:
104	            result.extend(value_to_nt_obj(item, sani_ctr))
105	        return result
106	    if isinstance(val, dict):
107	        resource = val.get("resource")
108	        if resource:
109	            parts = resource.split()  # split handles multi-URI values (DDB data quality issue)
110	            result = []
111	            for uri in parts:
112	                sanitized = _sanitize_iri(uri)
113	                if sani_ctr is not None and sanitized != uri:
114	                    sani_ctr["uri_sanitized"] += 1
115	                result.append(f"<{sanitized}>")
116	            if sani_ctr is not None and len(parts) > 1:
117	                sani_ctr["uri_split"] += len(parts)
118	            return result
119	        text = val.get("$", "")
120	        if not text:
121	            return []
122	        escaped = _escape_literal(str(text))
123	        lang = val.get("lang")
124	        if lang:
125	            return [f'"{escaped}"@{lang}']
126	        return [f'"{escaped}"']
127	    return []
128	
129	
130	def normalize_date(s: str) -> list[str]:
131	    """Normalise a dc:date string to ISO 8601.
132	
133	    8-digit compact YYYYMMDD → YYYY-MM-DD.
134	    ISO interval begin/end → [begin, end].
135	    All other values returned unchanged.
136	    """
137	    s = s.strip()
138	    if "/" in s:
139	        parts = s.split("/", 1)
140	        return [normalize_date(p)[0] for p in parts]
141	    if len(s) == 8 and s.isdigit():
142	        return [f"{s[:4]}-{s[4:6]}-{s[6:]}"]
143	    return [s]
144	
145	
146	def is_ddb_or_gnd(uri: str) -> bool:
147	    """True if URI is a DDB organization or GND authority URI."""
148	    return uri.startswith((
149	        "http://www.deutsche-digitale-bibliothek.de/organization/",
150	        "http://d-nb.info/gnd/",
151	        "https://d-nb.info/gnd/",
152	    ))
153	
154	
155	def resolve_agent(
156	    label: str,
157	    resource: str,
158	    agents_index: dict[str, AgentDict],
159	) -> AgentDict | None:
160	    """Resolve a creator/contributor to an Agent dict.
161	
162	    URI match preferred; label match fallback.
163	    Returns None if no match found.
164	    """
165	    if resource and resource in agents_index:
166	        return agents_index[resource]
167	    if label and label in agents_index:
168	        return agents_index[label]
169	    return None
170	
171	
172	def _extract_mediatype_sector(concepts: object) -> tuple[str, str]:
173	    """Return (mediatype_iri, sector_iri) from the record's Concept list."""
174	    mediatype = "any"
175	    sector    = "any"
176	    for c in coerce_list(concepts):
177	        if not isinstance(c, dict):
178	            continue
179	        about = c.get("about") or ""
180	        if about.startswith(_MEDIATYPE_PREFIX):
181	            mediatype = about
182	        elif about.startswith(_SECTOR_PREFIX):
183	            sector = about
184	    return mediatype, sector
185	
186	
187	def get_object_id(record: dict) -> str | None:
188	    """Extract 32-char object ID from ProvidedCHO.about URI. Returns None on failure."""
189	    try:
190	        about = record["edm"]["RDF"]["ProvidedCHO"]["about"]
191	    except (KeyError, TypeError):
192	        return None
193	    if not about:
194	        return None
195	    # Bare 32-char ID (D27)
196	    if len(about) == 32 and not about.startswith("http"):
197	        return about
198	    obj_id = about.rstrip("/").rsplit("/", 1)[-1]
199	    return obj_id if len(obj_id) == 32 else None
200	
```

---

### Assistant *(2026-05-07T11:20:14.607Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 100
}
```

---

### User *(2026-05-07T11:20:14.619Z)*

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
18	    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, EDM_NS,
19	    _EDM_ENTITY_TYPES, _DDBEDM_PROP, _MOCHO_SKIP, _NEW_NS,
20	    _CLASS_WEMI, _CONTRIBUTOR_COL, _W_SLOT_CLASSES, SUBJECT_KEYS,
21	)
22	from .utils import (
23	    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,
24	    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,
25	)
26	
27	
28	def emit_ddbedm_triples(rdf: dict, graph_iri: str) -> tuple[NQList, Counter, Counter, Counter]:
29	    """Emit verbatim EDM passthrough triples for all entity types in rdf (§6.1).
30	
31	    Subject: first URI in entity['about']; owl:sameAs emitted for any additional URIs.
32	    Includes mt007 records.
33	    Returns (lines, class_ctr, pred_ctr, sani_ctr) where sani_ctr tracks
34	    uri_sanitized, uri_split, and uri_about_split counts.
35	    """
36	    lines:     NQList  = []
37	    class_ctr: Counter = Counter()
38	    pred_ctr:  Counter = Counter()
39	    sani_ctr:  Counter = Counter()
40	    _skip = frozenset({"about"})
41	    for entity_type, entities in rdf.items():
42	        edm_class = _EDM_ENTITY_TYPES.get(entity_type)
43	        for entity in coerce_list(entities):
44	            if not isinstance(entity, dict):
45	                continue
46	            raw_about = (entity.get("about") or "").strip()
47	            if not raw_about:
48	                continue
49	            about_parts = raw_about.split()
50	            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
51	            subj_nt  = f"<{subj_uri}>"
52	            if len(about_parts) > 1:
53	                sani_ctr["uri_about_split"] += len(about_parts) - 1
54	                for alt in about_parts[1:]:
55	                    lines.append(make_nq(subj_nt, f"<{OWL_SAMEAS}>",
56	                                         f"<{_sanitize_iri(alt)}>", graph_iri))
57	            if edm_class:
58	                lines.append(make_nq(subj_nt, f"<{RDF_TYPE}>", f"<{edm_class}>", graph_iri))
59	                class_ctr[_to_curie(edm_class)] += 1
60	            for key, val in entity.items():
61	                if key in _skip:
62	                    continue
63	                pred_iri = _DDBEDM_PROP.get(key)
64	                if not pred_iri:
65	                    continue
66	                pred_nt = f"<{pred_iri}>"
67	                curie   = _to_curie(pred_iri)
68	                for obj_nt in value_to_nt_obj(val, sani_ctr):
69	                    lines.append(make_nq(subj_nt, pred_nt, obj_nt, graph_iri))
70	                    pred_ctr[curie] += 1
71	    return lines, class_ctr, pred_ctr, sani_ctr
72	
73	
74	def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
75	    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
76	    lines: NQList = []
77	    props = record.get("properties") or {}
78	    prov  = record.get("provider-info") or {}
79	
80	    item_id         = (props.get("item-id")         or "").strip()
81	    dataset_id      = (props.get("dataset-id")      or "").strip()
82	    dataset_label   = (props.get("dataset-label")   or "").strip()
83	    revision        = (props.get("revision-id")     or "").strip()
84	    ingest_dt       = (props.get("ingest-date")     or "").strip()
85	    map_ver         = (props.get("mapping-version") or "").strip()
86	    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
87	    provider_name   = (prov.get("provider-name")    or "").strip()
88	    provider_uri    = (prov.get("provider-uri")     or "").strip()
89	    provider_id     = (prov.get("provider-id")      or "").strip()
90	    provider_isil   = (prov.get("provider-isil")    or "").strip()
91	
92	    src_desc  = (record.get("source") or {}).get("description") or {}
93	    src_ref   = (src_desc.get("record") or {}) if isinstance(src_desc, dict) else {}
94	    ref_val   = (src_ref.get("ref",  "") or "").strip() if isinstance(src_ref, dict) else ""
95	    src_href  = (src_ref.get("href", "") or "").strip() if isinstance(src_ref, dict) else ""
96	    rec_type  = (src_ref.get("type", "") or "").strip() if isinstance(src_ref, dict) else ""
97	
98	    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
99	    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
100	    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
```

---

### Assistant *(2026-05-07T11:20:18.265Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 150,
  "offset": 270
}
```

---

### User *(2026-05-07T11:20:18.272Z)*

**Tool result**
```
270	
271	
272	def emit_subject_triples(
273	    cho_nt: str,
274	    subject_vals: list,
275	    concepts_index: dict[str, dict],
276	    graph_iri: str,
277	) -> NQList:
278	    """Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended)."""
279	    lines: NQList = []
280	    seen: set[str] = set()
281	    for val in subject_vals:
282	        if not isinstance(val, dict):
283	            continue
284	        resource = (val.get("resource") or "").strip()
285	        label    = (val.get("$")        or "").strip()
286	        lang     = (val.get("lang")     or "").strip()
287	        if resource:
288	            if resource in seen:
289	                continue
290	            seen.add(resource)
291	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SUBJECT}>", f"<{_sanitize_iri(resource)}>", graph_iri))
292	            concept = concepts_index.get(resource)
293	            if concept:
294	                for pl in coerce_list(concept.get("prefLabel")):
295	                    for obj_nt in value_to_nt_obj(pl):
296	                        lines.append(make_nq(f"<{_sanitize_iri(resource)}>", f"<{RDFS_LABEL}>",
297	                                             obj_nt, graph_iri))
298	        elif label:
299	            key = f"lit:{label}"
300	            if key in seen:
301	                continue
302	            seen.add(key)
303	            escaped = _escape_literal(label)
304	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
305	            lines.append(make_nq(cho_nt, f"<{DC_SUBJECT}>", obj_nt, graph_iri))
306	    return lines
307	
308	
309	def emit_creator_triples(
310	    cho_nt: str,
311	    creator_vals: list,
312	    agents_index: dict[str, AgentDict],
313	    target_class: str,
314	    class_prop_align: PropAlign,
315	    graph_iri: str,
316	) -> NQList:
317	    """Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).
318	
319	    Both tracks run independently for each creator value (D2 / props-mapping §4).
320	    """
321	    lines: NQList = []
322	    dc_creator_iri = "http://purl.org/dc/elements/1.1/creator"
323	    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), "")
324	
325	    for val in coerce_list(creator_vals):
326	        if not isinstance(val, dict):
327	            continue
328	        resource = (val.get("resource") or "").strip()
329	        label    = (val.get("$")        or "").strip()
330	        lang     = (val.get("lang")     or "").strip()
331	
332	        # Track 1: class-specific predicate (always runs when target_prop is known)
333	        if track1_prop:
334	            if resource:
335	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
336	            elif label:
337	                escaped = _escape_literal(label)
338	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
339	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", obj_nt, graph_iri))
340	
341	        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)
342	        agent = resolve_agent(label, resource, agents_index)
343	        if agent:
344	            agent_uri = (agent.get("about") or "").strip()
345	            if agent_uri and is_ddb_or_gnd(agent_uri):
346	                lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>",
347	                                     f"<{agent_uri}>", graph_iri))
348	                agent_nt = f"<{agent_uri}>"
349	                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
350	                pref = agent.get("prefLabel") or label
351	                if pref and isinstance(pref, str):
352	                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>",
353	                                         f'"{_escape_literal(pref)}"', graph_iri))
354	    return lines
355	
356	
357	def emit_contributor_triples(
358	    cho_nt: str,
359	    contributor_vals: list,
360	    event_participant_index: dict[str, str],
361	    lido_dispatch: dict[str, dict],
362	    target_class: str,
363	    wemi: str,
364	    graph_iri: str,
365	) -> NQList:
366	    """Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5)."""
367	    lines: NQList = []
368	    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), "dc_agent_fallback")
369	
370	    for val in coerce_list(contributor_vals):
371	        if not isinstance(val, dict):
372	            continue
373	        resource = (val.get("resource") or "").strip()
374	        label    = (val.get("$")        or "").strip()
375	        lang     = (val.get("lang")     or "").strip()
376	
377	        lido_type   = event_participant_index.get(resource) if resource else None
378	        lido_row    = lido_dispatch.get(lido_type) if lido_type else None
379	        target_prop = (
380	            (lido_row.get(prop_col) or lido_row.get("dc_agent_fallback") or DC_CONTRIBUTOR)
381	            if lido_row else DC_CONTRIBUTOR
382	        )
383	
384	        if resource:
385	            lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
386	            agent_nt = f"<{_sanitize_iri(resource)}>"
387	            lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
388	            if label:
389	                escaped = _escape_literal(label)
390	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
391	                lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
392	        elif label:
393	            escaped = _escape_literal(label)
394	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
395	            lines.append(make_nq(cho_nt, f"<{DC_CONTRIBUTOR}>", obj_nt, graph_iri))
396	    return lines
397	
398	
399	def emit_aggregation_triples(agg: dict, cho_nt: str, graph_iri: str) -> NQList:
400	    """Emit mocho triples derived from the Aggregation block (D23)."""
401	    lines: NQList = []
402	    _edm_dp     = EDM_NS + "dataProvider"
403	    _org_prefix = "http://www.deutsche-digitale-bibliothek.de/organization/"
404	
405	    is_shown = agg.get("isShownAt") or {}
406	    if isinstance(is_shown, dict):
407	        uri = (is_shown.get("resource") or "").strip()
408	        if uri:
409	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SOURCE}>", f"<{_sanitize_iri(uri)}>", graph_iri))
410	
411	    for dp in coerce_list(agg.get("dataProvider")):
412	        if not isinstance(dp, dict):
413	            continue
414	        uri = (dp.get("resource") or "").strip()
415	        if uri and uri.startswith(_org_prefix):
416	            lines.append(make_nq(cho_nt, f"<{_edm_dp}>", f"<{_sanitize_iri(uri)}>", graph_iri))
417	
418	    for obj in coerce_list(agg.get("object")):
419	        if not isinstance(obj, dict):
```

---

### Assistant *(2026-05-07T11:20:19.705Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"hasMet\\|edm:hasMet\\|EDM_HAS_MET\\|has_met\\|hasMet\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "description": "Search for hasMet in transform files"
}
```

---

### User *(2026-05-07T11:20:19.754Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:251:    "hasMet":              EDM_NS + "hasMet",
```

---

### Assistant *(2026-05-07T11:20:39.745Z)*

Let me look at the rest of emitters.py and constants.py to understand both bugs.

---

### Assistant *(2026-05-07T11:20:40.312Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 200,
  "offset": 420
}
```

---

### User *(2026-05-07T11:20:40.321Z)*

**Tool result**
```
420	            continue
421	        uri = (obj.get("resource") or "").strip()
422	        if uri:
423	            lines.append(make_nq(cho_nt, f"<{FOAF_THUMBNAIL}>", f"<{_sanitize_iri(uri)}>", graph_iri))
424	
425	    return lines
426	
427	
428	def emit_place_stubs(places: object, graph_iri: str) -> NQList:
429	    """Emit rdfs:label stubs for each Place entity referenced by the record (D24)."""
430	    lines: NQList = []
431	    for place in coerce_list(places):
432	        if not isinstance(place, dict):
433	            continue
434	        raw_about = (place.get("about") or "").strip()
435	        if not raw_about:
436	            continue
437	        place_uri = mint_bare_id("Place", raw_about)
438	        place_nt  = f"<{place_uri}>"
439	        for lbl in coerce_list(place.get("prefLabel")):
440	            for obj_nt in value_to_nt_obj(lbl):
441	                lines.append(make_nq(place_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
442	    return lines
443	
444	
445	def werk_staging_row(cho_uri: str, cho: dict, target_class: str) -> dict | None:
446	    """Build a werk_staging dict if target_class is a W-slot class (D26). Else None."""
447	    if target_class not in _W_SLOT_CLASSES:
448	        return None
449	
450	    title = ""
451	    tv = cho.get("title")
452	    if isinstance(tv, dict):
453	        title = (tv.get("$") or "").strip()
454	    elif isinstance(tv, list) and tv:
455	        first = tv[0]
456	        title = (first.get("$") or "").strip() if isinstance(first, dict) else ""
457	
458	    dc_alt: list[str] = []
459	    for v in coerce_list(cho.get("alternative")):
460	        t = (v.get("$") or "").strip() if isinstance(v, dict) else ""
461	        if t:
462	            dc_alt.append(t)
463	
464	    dc_created = ""
465	    for v in coerce_list(cho.get("date")):
466	        t = (v if isinstance(v, str) else "").strip()
467	        if t:
468	            dc_created = t
469	            break
470	
471	    creator_uris: list[str] = []
472	    creator_lits: list[str] = []
473	    for v in coerce_list(cho.get("creator")):
474	        if not isinstance(v, dict):
475	            continue
476	        uri = (v.get("resource") or "").strip()
477	        lit = (v.get("$")        or "").strip()
478	        if uri:
479	            creator_uris.append(uri)
480	        elif lit:
481	            creator_lits.append(lit)
482	
483	    obj_id = cho_uri.rsplit("/", 1)[-1]
484	    return {
485	        "ddb_obj_id":       obj_id,
486	        "cho_uri":          cho_uri,
487	        "target_class":     target_class,
488	        "dc_title":         title,
489	        "dc_alternative":   dc_alt,
490	        "dc_created":       dc_created,
491	        "creator_uris":     creator_uris,
492	        "creator_literals": creator_lits,
493	    }
494	
495	
496	def emit_mocho_triples(
497	    rdf: dict,
498	    cho_uri: str,
499	    ddb_uri: str,
500	    sector: str,
501	    mediatype: str,
502	    mediatype_class_map: dict,
503	    htype_map: dict,
504	    audio_type2class: dict,
505	    class_prop_align: PropAlign,
506	    lido_dispatch: dict,
507	    graph_iri: str,
508	) -> tuple[NQList, str, str, dict]:
509	    """Emit all mocho-graph triples for one record (§6.3). Returns (lines, target_class, wemi, dispatch_flags).
510	
511	    dispatch_flags includes "preds_all" and "preds_new" Counters (CURIEs) built during emission.
512	    """
513	    lines:     NQList  = []
514	    preds_all: Counter = Counter()
515	    preds_new: Counter = Counter()
516	    sani_ctr:  Counter = Counter()
517	
518	    def _track(pred_iri: str) -> None:
519	        curie = _to_curie(pred_iri)
520	        preds_all[curie] += 1
521	        if any(pred_iri.startswith(ns) for ns in _NEW_NS):
522	            preds_new[curie] += 1
523	
524	    def _track_nqlist(nqlist: NQList) -> None:
525	        for nq in nqlist:
526	            try:
527	                _track(nq.split("> <", 1)[1].split(">", 1)[0])
528	            except IndexError:
529	                pass
530	
531	    cho: dict = rdf.get("ProvidedCHO") or {}
532	    if isinstance(cho, list):
533	        cho = cho[0] if cho else {}
534	
535	    cho_nt      = f"<{cho_uri}>"
536	    htype       = (cho.get("hierarchyType") or "").strip() or None
537	    dctype_vals = coerce_list(cho.get("dcType"))
538	
539	    # ── Class dispatch ────────────────────────────────────────────────────────
540	    type_lines, target_class, wemi, dispatch_flags = retype_entities(
541	        sector, mediatype, htype, dctype_vals,
542	        cho_nt, mediatype_class_map, htype_map, audio_type2class, graph_iri,
543	    )
544	    lines.extend(type_lines)
545	    _track_nqlist(type_lines)
546	
547	    # owl:sameAs link to original DDB URI (D22)
548	    lines.append(make_nq(cho_nt, f"<{OWL_SAMEAS}>", f"<{ddb_uri}>", graph_iri))
549	    _track(OWL_SAMEAS)
550	
551	    # ── Build per-record indexes ───────────────────────────────────────────────
552	    agents_index: dict[str, AgentDict] = {}
553	    for agent in coerce_list(rdf.get("Agent")):
554	        if not isinstance(agent, dict):
555	            continue
556	        about = (agent.get("about") or "").strip()
557	        if about:
558	            agents_index[mint_bare_id("Agent", about)] = agent
559	        for pl in coerce_list(agent.get("prefLabel")):
560	            t = (pl.get("$") or "").strip() if isinstance(pl, dict) else ""
561	            if t:
562	                agents_index.setdefault(t, agent)
563	
564	    event_participant_index: dict[str, str] = {}
565	    for event in coerce_list(rdf.get("Event")):
566	        if not isinstance(event, dict):
567	            continue
568	        ht = event.get("hasType") or {}
569	        if isinstance(ht, list):
570	            ht = ht[0] if ht else {}
571	        lido_type_uri = (ht.get("resource") or "").strip() if isinstance(ht, dict) else ""
572	        for p in coerce_list(event.get("P11_had_participant")):
573	            puri = (p.get("resource") or "").strip() if isinstance(p, dict) else ""
574	            if puri and lido_type_uri:
575	                event_participant_index[puri] = lido_type_uri
576	
577	    concepts_index: dict[str, dict] = {}
578	    for concept in coerce_list(rdf.get("Concept")):
579	        if not isinstance(concept, dict):
580	            continue
581	        about = (concept.get("about") or "").strip()
582	        if about:
583	            concepts_index[about] = concept
584	
585	    # ── dc:title — dual-emit (props-mapping D4) ───────────────────────────────
586	    dc_title_iri = "http://purl.org/dc/elements/1.1/title"
587	    title_prop   = class_prop_align.get((target_class, dc_title_iri), "")
588	    for obj_nt in value_to_nt_obj(cho.get("title"), sani_ctr):
589	        lines.append(make_nq(cho_nt, f"<{dc_title_iri}>", obj_nt, graph_iri))
590	        _track(dc_title_iri)
591	        if title_prop and title_prop != dc_title_iri:
592	            lines.append(make_nq(cho_nt, f"<{title_prop}>", obj_nt, graph_iri))
593	            _track(title_prop)
594	
595	    # ── Generic property loop ─────────────────────────────────────────────────
596	    dc_date_iri   = "http://purl.org/dc/elements/1.1/date"
597	    dcterms_iss   = "http://purl.org/dc/terms/issued"
598	    dcterms_ipart = "http://purl.org/dc/terms/isPartOf"
599	    _special_keys = frozenset({"creator", "contributor", "title"}) | SUBJECT_KEYS | _MOCHO_SKIP
600	
601	    subject_vals: list = []
602	    for skey in SUBJECT_KEYS:
603	        subject_vals.extend(coerce_list(cho.get(skey)))
604	
605	    for prop, val in cho.items():
606	        if prop in _special_keys:
607	            continue
608	        prop_iri = _DDBEDM_PROP.get(prop)
609	        if not prop_iri:
610	            continue
611	        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
612	        if not target_prop:
613	            continue
614	
615	        if prop_iri in (dc_date_iri, dcterms_iss):
616	            # Date normalisation (D15 / props-mapping §3.1)
617	            for v in coerce_list(val):
618	                raw = (v if isinstance(v, str) else
619	                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
```

---

### Assistant *(2026-05-07T11:20:40.368Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py"
}
```

---

### User *(2026-05-07T11:20:40.377Z)*

**Tool result**
```
1	"""Constants: IRIs, prefix tables, dispatch tables, path defaults, and type aliases."""
2	
3	from __future__ import annotations
4	
5	from pathlib import Path
6	from typing import Dict, List, Tuple
7	
8	# ─── Paths ────────────────────────────────────────────────────────────────────
9	
10	SCRIPT_DIR  = Path(__file__).resolve().parent
11	PROJECT_DIR = SCRIPT_DIR.parents[1]   # scripts/transform/ → scripts/ → project root
12	
13	DEFAULT_JSONL        = PROJECT_DIR / "data"   / "items-all-goethe-faust.json"
14	DEFAULT_IDS          = PROJECT_DIR / "data"   / "ids-all-goethe-faust.txt"
15	DEFAULT_ALIGNMENT    = PROJECT_DIR / "output" / "config" / "lookup_class_prop_alignment.csv"
16	DEFAULT_LIDO         = PROJECT_DIR / "output" / "config" / "lido_event_types.csv"
17	DEFAULT_HTYPE        = PROJECT_DIR / "output" / "config" / "lookup_htype_doco_rico.csv"
18	DEFAULT_MEDIATYPE    = PROJECT_DIR / "output" / "config" / "lookup_mediatype_class.csv"
19	DEFAULT_AUDIO        = PROJECT_DIR / "output" / "config" / "audio_type2class.json"
20	DEFAULT_OUTPUT_BASE  = PROJECT_DIR / "output" / "transform"
21	
22	# ─── Type aliases ─────────────────────────────────────────────────────────────
23	
24	NQuad     = str
25	NQList    = List[NQuad]
26	PropAlign = Dict[Tuple[str, str], str]   # (target_class, edm_prop) → target_prop_iri
27	AgentDict = Dict[str, object]
28	
29	# ─── Named graphs ─────────────────────────────────────────────────────────────
30	
31	GRAPH_DDBEDM = "https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm"
32	GRAPH_MOCHO  = "https://gemea.ise.fiz-karlsruhe.de/graph/mocho"
33	GRAPH_PROV   = "https://gemea.ise.fiz-karlsruhe.de/graph/prov"
34	
35	# ─── URI bases ────────────────────────────────────────────────────────────────
36	
37	GEMEA_BASE    = "https://gemea.ise.fiz-karlsruhe.de/mocho/"
38	DDB_ITEM_BASE = "http://www.deutsche-digitale-bibliothek.de/item/"
39	DDB_BASE      = "http://www.deutsche-digitale-bibliothek.de"
40	DDB_API_BASE  = "https://api.deutsche-digitale-bibliothek.de/2/"
41	
42	# ─── Vocab prefixes ───────────────────────────────────────────────────────────
43	
44	_MEDIATYPE_PREFIX = "http://ddb.vocnet.org/medientyp/"
45	_SECTOR_PREFIX    = "http://ddb.vocnet.org/sparte/"
46	MT007_IRI         = "http://ddb.vocnet.org/medientyp/mt007"
47	
48	# ─── Ontology namespaces ──────────────────────────────────────────────────────
49	
50	EDM_NS   = "http://www.europeana.eu/schemas/edm/"
51	GNDO_NS  = "https://d-nb.info/standards/elementset/gnd#"
52	CIDOC_NS = "http://www.cidoc-crm.org/cidoc-crm/"
53	MOCHO_NS = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#"
54	
55	# ─── Ontology IRIs ────────────────────────────────────────────────────────────
56	
57	RDF_TYPE        = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
58	RDFS_LABEL      = "http://www.w3.org/2000/01/rdf-schema#label"
59	OWL_SAMEAS      = "http://www.w3.org/2002/07/owl#sameAs"
60	SKOS_PREF_LABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
61	SKOS_CONCEPT    = "http://www.w3.org/2004/02/skos/core#Concept"
62	DCTERMS_SOURCE  = "http://purl.org/dc/terms/source"
63	FOAF_THUMBNAIL  = "http://xmlns.com/foaf/0.1/thumbnail"
64	FOAF_ORG        = "http://xmlns.com/foaf/0.1/Organization"
65	FOAF_NAME       = "http://xmlns.com/foaf/0.1/name"
66	EDM_DATA_PROVIDER = EDM_NS + "dataProvider"
67	SCHEMA_URL      = "https://schema.org/url"
68	MOCHO_ISIL      = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#isil"
69	MOCHO_AGENT     = MOCHO_NS + "Agent"
70	RICO_HAS_RST    = "http://www.ica.org/standards/RiC/ontology#hasRecordSetType"
71	
72	PROV_ENTITY     = "http://www.w3.org/ns/prov#Entity"
73	PROV_AGENT      = "http://www.w3.org/ns/prov#Agent"
74	PROV_SW_AGENT   = "http://www.w3.org/ns/prov#SoftwareAgent"
75	PROV_DERIVED    = "http://www.w3.org/ns/prov#wasDerivedFrom"
76	PROV_ATTRIBUTED = "http://www.w3.org/ns/prov#wasAttributedTo"
77	PROV_GEN_TIME   = "http://www.w3.org/ns/prov#generatedAtTime"
78	PROV_ON_BEHALF  = "http://www.w3.org/ns/prov#actedOnBehalfOf"
79	DCAT_DATASET    = "http://www.w3.org/ns/dcat#Dataset"
80	DCTERMS_ID      = "http://purl.org/dc/terms/identifier"
81	DCTERMS_TYPE    = "http://purl.org/dc/terms/type"
82	DCTERMS_HAS_VER = "http://purl.org/dc/terms/hasVersion"
83	DCTERMS_REF     = "http://purl.org/dc/terms/references"
84	DCTERMS_RIGHTS  = "http://purl.org/dc/terms/rights"
85	DC_ID           = "http://purl.org/dc/elements/1.1/identifier"
86	DC_TITLE        = "http://purl.org/dc/elements/1.1/title"
87	DC_DESCRIPTION  = "http://purl.org/dc/elements/1.1/description"
88	
89	DCTERMS_CREATOR = "http://purl.org/dc/terms/creator"
90	DC_CONTRIBUTOR  = "http://purl.org/dc/elements/1.1/contributor"
91	DC_SUBJECT      = "http://purl.org/dc/elements/1.1/subject"
92	DCTERMS_SUBJECT = "http://purl.org/dc/terms/subject"
93	XSD_DATETIME    = "http://www.w3.org/2001/XMLSchema#dateTime"
94	
95	# ─── Property skip sets ───────────────────────────────────────────────────────
96	
97	SUBJECT_KEYS = frozenset({"dcSubject", "dcTermsSubject", "dcTermSubject"})
98	
99	_MOCHO_SKIP = frozenset({
100	    "about", "hierarchyType",
101	    "creator", "contributor",
102	    "dcSubject", "dcTermsSubject", "dcTermSubject",
103	    "dcType",
104	    "aggregationEntity", "hierarchyPosition",
105	})
106	
107	# ─── Prefix expansion table ───────────────────────────────────────────────────
108	
109	_PREFIXES = {
110	    "rdam":    "http://rdaregistry.info/Elements/m/",
111	    "rdaw":    "http://rdaregistry.info/Elements/w/",
112	    "rdae":    "http://rdaregistry.info/Elements/e/",
113	    "rdac":    "http://rdaregistry.info/Elements/c/",
114	    "rdact":   "http://rdaregistry.info/termList/RDACarrierType/",
115	    "dc":      "http://purl.org/dc/elements/1.1/",
116	    "dcterms": "http://purl.org/dc/terms/",
117	    "vra":     "http://purl.org/vra/",
118	    "rico":    "http://www.ica.org/standards/RiC/ontology#",
119	    "ric-rst": "http://www.ica.org/standards/RiC/vocabularies/recordSetTypes#",
120	    "skos":    "http://www.w3.org/2004/02/skos/core#",
121	    "owl":     "http://www.w3.org/2002/07/owl#",
122	    "rdfs":    "http://www.w3.org/2000/01/rdf-schema#",
123	    "foaf":    "http://xmlns.com/foaf/0.1/",
124	    "edm":     EDM_NS,
125	    "mo":      "http://purl.org/ontology/mo/",
126	    "aco":     "https://w3id.org/ac-ontology/aco#",
127	    "ec":      "http://www.ebu.ch/metadata/ontologies/ebucoreplus#",
128	    "doco":    "http://purl.org/spar/doco/",
129	    "mocho":   MOCHO_NS,
130	    "gndo":    GNDO_NS,
131	    "ddb":     "http://www.deutsche-digitale-bibliothek.de/",
132	    "ore":     "http://www.openarchives.org/ore/terms/",
133	}
134	
135	# ─── EDM entity type map ──────────────────────────────────────────────────────
136	
137	_EDM_ENTITY_TYPES = {
138	    "ProvidedCHO":  EDM_NS + "ProvidedCHO",
139	    "Agent":        EDM_NS + "Agent",
140	    "Place":        EDM_NS + "Place",
141	    "TimeSpan":     EDM_NS + "TimeSpan",
142	    "WebResource":  EDM_NS + "WebResource",
143	    "Aggregation":  "http://www.openarchives.org/ore/terms/Aggregation",
144	    "Concept":      "http://www.w3.org/2004/02/skos/core#Concept",
145	    "PhysicalThing": EDM_NS + "PhysicalThing",
146	    "Event":        EDM_NS + "Event",
147	}
148	
149	# ─── Namespace tuple (used for mocho_vocab properties_new tracking) ─────────
150	
151	_NEW_NS: tuple[str, ...] = (
152	    "http://rdaregistry.info/Elements/",
153	    "http://www.ica.org/standards/RiC/",
154	    MOCHO_NS,
155	    "http://purl.org/vra/",
156	    "http://purl.org/ontology/mo/",
157	    "https://w3id.org/ac-ontology/",
158	    "http://www.ebu.ch/metadata/ontologies/ebucoreplus#",
159	    "http://purl.org/spar/doco/",
160	)
161	
162	# ─── W-slot classes (trigger werk_staging row) ────────────────────────────────
163	
164	_W_SLOT_CLASSES: frozenset[str] = frozenset({
165	    "http://rdaregistry.info/Elements/c/C10001",  # rdac:C10001 Work
166	    "http://purl.org/ontology/mo/MusicalWork",    # mo:MusicalWork
167	})
168	
169	# ─── Primary WEMI level per class ─────────────────────────────────────────────
170	
171	_CLASS_WEMI: dict[str, str] = {
172	    # W — Work
173	    "http://rdaregistry.info/Elements/c/C10001":                       "W",
174	    MOCHO_NS + "ImmovableWork":                                        "W",
175	    MOCHO_NS + "ImageWork":                                            "W",
176	    "http://purl.org/ontology/mo/MusicalWork":                         "W",
177	    "http://purl.org/vra/Work":                                        "W",
178	    "http://www.ebu.ch/metadata/ontologies/ebucoreplus#EditorialWork":  "W",
179	    # M — Manifestation
180	    "http://rdaregistry.info/Elements/c/C10007":                       "M",
181	    MOCHO_NS + "Manifestation":                                        "M",
182	    MOCHO_NS + "ImageManifestation":                                   "M",
183	    "https://w3id.org/ac-ontology/aco#AudioManifestation":             "M",
184	    "http://purl.org/ontology/mo/MusicalManifestation":                "M",
185	    "http://www.ebu.ch/metadata/ontologies/ebucoreplus#MediaResource":  "M",
186	    "http://purl.org/vra/Image":                                       "M",
187	    # doco fragment types (Manifestation-level document parts)
188	    "http://purl.org/spar/doco/Section":         "M",
189	    "http://purl.org/spar/doco/Appendix":        "M",
190	    "http://purl.org/spar/doco/Part":            "M",
191	    "http://purl.org/spar/doco/Chapter":         "M",
192	    "http://purl.org/spar/doco/Figure":          "M",
193	    "http://purl.org/spar/doco/Index":           "M",
194	    "http://purl.org/spar/doco/TableOfContents": "M",
195	    "http://purl.org/spar/doco/TextChunk":       "M",
196	    "http://purl.org/spar/doco/Stanza":          "M",
197	    "http://purl.org/spar/doco/Preface":         "M",
198	    # RiC — no WEMI slot
199	    "http://www.ica.org/standards/RiC/ontology#RecordSet":  "",
200	    "http://www.ica.org/standards/RiC/ontology#Record":     "",
201	    "http://www.ica.org/standards/RiC/ontology#RecordPart": "",
202	}
203	
204	# ─── Contributor column selection: (wemi, target_class) → lido_event_types col ─
205	
206	_CONTRIBUTOR_COL: dict[tuple[str, str], str] = {
207	    ("M", "http://rdaregistry.info/Elements/c/C10007"):        "rdam_agent_prop",
208	    ("M", MOCHO_NS + "Manifestation"):                         "rdam_agent_prop",
209	    ("W", "http://rdaregistry.info/Elements/c/C10001"):        "rdaw_agent_prop",
210	    ("M", "http://purl.org/vra/Image"):                        "vra_image_agent_prop",
211	    ("W", "http://purl.org/vra/Work"):                         "vra_work_agent_prop",
212	    ("",  "http://www.ica.org/standards/RiC/ontology#RecordSet"):  "rico_agent_prop",
213	    ("",  "http://www.ica.org/standards/RiC/ontology#Record"):     "rico_agent_prop",
214	    ("",  "http://www.ica.org/standards/RiC/ontology#RecordPart"): "rico_agent_prop",
215	}
216	
217	# ─── JSON key → predicate IRI (ddbedm passthrough and mocho alignment lookup) ─
218	
219	_DDBEDM_PROP: dict[str, str] = {
220	    # DC elements 1.1
221	    "title":               "http://purl.org/dc/elements/1.1/title",
222	    "creator":             "http://purl.org/dc/elements/1.1/creator",
223	    "contributor":         "http://purl.org/dc/elements/1.1/contributor",
224	    "date":                "http://purl.org/dc/elements/1.1/date",
225	    "description":         "http://purl.org/dc/elements/1.1/description",
226	    "format":              "http://purl.org/dc/elements/1.1/format",
227	    "identifier":          "http://purl.org/dc/elements/1.1/identifier",
228	    "language":            "http://purl.org/dc/elements/1.1/language",
229	    "publisher":           "http://purl.org/dc/elements/1.1/publisher",
230	    "relation":            "http://purl.org/dc/elements/1.1/relation",
231	    "rights":              "http://purl.org/dc/elements/1.1/rights",
232	    "source":              "http://purl.org/dc/elements/1.1/source",
233	    "coverage":            "http://purl.org/dc/elements/1.1/coverage",
234	    "dcSubject":           "http://purl.org/dc/elements/1.1/subject",
235	    "dcType":              "http://purl.org/dc/elements/1.1/type",
236	    # DC terms
237	    "alternative":         "http://purl.org/dc/terms/alternative",
238	    "dcTermsSubject":      "http://purl.org/dc/terms/subject",
239	    "dcTermSubject":       "http://purl.org/dc/terms/subject",  # corpus typo variant
240	    "dcTermsLanguage":     "http://purl.org/dc/terms/language",
241	    "isPartOf":            "http://purl.org/dc/terms/isPartOf",
242	    "issued":              "http://purl.org/dc/terms/issued",
243	    "extent":              "http://purl.org/dc/terms/extent",
244	    "medium":              "http://purl.org/dc/terms/medium",
245	    "tableOfContents":     "http://purl.org/dc/terms/tableOfContents",
246	    "hasPart":             "http://purl.org/dc/terms/hasPart",
247	    "spatial":             "http://purl.org/dc/terms/spatial",
248	    "dcTermsRights":       "http://purl.org/dc/terms/rights",
249	    # EDM
250	    "currentLocation":     EDM_NS + "currentLocation",
251	    "hasMet":              EDM_NS + "hasMet",
252	    "hasType":             EDM_NS + "hasType",
253	    "isNextInSequence":    EDM_NS + "isNextInSequence",
254	    "isShownAt":           EDM_NS + "isShownAt",
255	    "isShownBy":           EDM_NS + "isShownBy",
256	    "wasPresentAt":        EDM_NS + "wasPresentAt",
257	    "isRelatedTo":         EDM_NS + "isRelatedTo",
258	    "edmType":             EDM_NS + "type",
259	    "object":              EDM_NS + "object",
260	    "aggregatedCHO":       EDM_NS + "aggregatedCHO",
261	    "aggregator":          EDM_NS + "aggregator",
262	    "dataProvider":        EDM_NS + "dataProvider",
263	    "edmRights":           EDM_NS + "rights",
264	    "provider":            EDM_NS + "provider",
265	    "hasView":             EDM_NS + "hasView",
266	    "begin":               EDM_NS + "begin",
267	    "end":                 EDM_NS + "end",
268	    "occurredAt":          EDM_NS + "occurredAt",
269	    "occuredAt":           EDM_NS + "occurredAt",  # typo variant in corpus
270	    "happenedAt":          EDM_NS + "happenedAt",
271	    # SKOS
272	    "prefLabel":           "http://www.w3.org/2004/02/skos/core#prefLabel",
273	    "altLabel":            "http://www.w3.org/2004/02/skos/core#altLabel",
274	    "note":                "http://www.w3.org/2004/02/skos/core#note",
275	    "notation":            "http://www.w3.org/2004/02/skos/core#notation",
276	    # RDF / OWL
277	    "type":                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
278	    "sameAs":              "http://www.w3.org/2002/07/owl#sameAs",
279	    # FOAF
280	    "name":                "http://xmlns.com/foaf/0.1/name",
281	    # GND
282	    "biographicalInformation": GNDO_NS + "biographicalInformation",
283	    "dateOfBirth":             GNDO_NS + "dateOfBirth",
284	    "dateOfDeath":             GNDO_NS + "dateOfDeath",
285	    "dateOfEstablishment":     GNDO_NS + "dateOfEstablishment",
286	    "dateOfTermination":       GNDO_NS + "dateOfTermination",
287	    "gender":                  GNDO_NS + "gender",
288	    "placeOfBirth":            GNDO_NS + "placeOfBirth",
289	    "placeOfDeath":            GNDO_NS + "placeOfDeath",
290	    "professionOrOccupation":  GNDO_NS + "professionOrOccupation",
291	    # CIDOC-CRM (LIDO events)
292	    "P11_had_participant": CIDOC_NS + "P11_had_participant",
293	    # DDB-internal structural fields (preserved in ddbedm, skipped in mocho)
294	    "hierarchyType":      "http://www.deutsche-digitale-bibliothek.de/hierarchyType",
295	    "hierarchyPosition":  "http://www.deutsche-digitale-bibliothek.de/hierarchyPosition",
296	    "aggregationEntity":  "http://www.deutsche-digitale-bibliothek.de/aggregationEntity",
297	}
298	
```

---

### Assistant *(2026-05-07T11:21:40.690Z)*

Let me check the ADR and transform notes for context on the urn:fix.

---

### Assistant *(2026-05-07T11:21:42.479Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"urn\\|bare\\|subject\\|hasMet\\|concept\" /Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md | head -60",
  "description": "Search ADR for URN and subject handling decisions"
}
```

---

### User *(2026-05-07T11:21:42.587Z)*

**Tool result**
```
308:follow a `urn:ddbedm:` convention that traces each identifier back to its JSON key
316:| Dataset | `urn:ddbedm:properties:dataset-id:<id>` | `properties.dataset-id` |
317:| XSLT | `urn:ddbedm:properties:mapping-version:<ver>` | `properties.mapping-version` |
318:| Provider | `urn:ddbedm:provider-info:provider-ddb-id:<id>` | `provider-info.provider-ddb-id` |
338:        <urn:ddbedm:properties:dataset-id:76409877634279609sQOu> ;  # properties.dataset-id
340:        <urn:ddbedm:properties:mapping-version:6.18> ;              # properties.mapping-version
347:<urn:ddbedm:properties:dataset-id:76409877634279609sQOu>
353:        <urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI> .
357:<urn:ddbedm:properties:mapping-version:6.18>
370:<urn:ddbedm:provider-info:provider-ddb-id:CJY7MSLPOPB7FTPC7JM5K2GGM5PBGLYI>
390:**Dataset** (`urn:ddbedm:properties:dataset-id:<value>`):
399:**XSLT** (`urn:ddbedm:properties:mapping-version:<value>`):
406:**Provider** (`urn:ddbedm:provider-info:provider-ddb-id:<value>`):
446:Emit `mocho:mimeType` as a DataProperty triple on the WebResource subject:
458:- `mocho:mediaType` → vocnet-mtype concept IRI (`vocnet-mtype:mt002`) — semantic category
492:- Minting a GeMeA URI for the CHO separates the enriched mocho view from the raw DDB-EDM view. The `ddbedm` graph retains the original DDB URI as subject; the `mocho` graph uses the minted URI. `owl:sameAs` bridges the two.
495:**Implementation**: `get_object_id()` already extracts the 32-char object ID. The minted URI is constructed as `GEMEA_BASE + object_id`. All mocho-graph triples for the CHO use the minted URI as subject.
531:*Use `owl:sameAs` instead of `skos:exactMatch`*: `owl:sameAs` asserts full identity — all properties of `<gnd-uri>` are inherited by `<gemea-work-uri>` and vice versa under OWL semantics. This is too strong: GND's `gndo:MusicalWork` type and its bibliographic properties would be inferred on the GeMeA Work entity. `skos:exactMatch` expresses "the same concept in a different vocabulary" without triggering OWL identity closure.
```

---

### Assistant *(2026-05-07T11:21:43.179Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 100,
  "offset": 600
}
```

---

### User *(2026-05-07T11:21:43.189Z)*

**Tool result**
```
600	
601	    subject_vals: list = []
602	    for skey in SUBJECT_KEYS:
603	        subject_vals.extend(coerce_list(cho.get(skey)))
604	
605	    for prop, val in cho.items():
606	        if prop in _special_keys:
607	            continue
608	        prop_iri = _DDBEDM_PROP.get(prop)
609	        if not prop_iri:
610	            continue
611	        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
612	        if not target_prop:
613	            continue
614	
615	        if prop_iri in (dc_date_iri, dcterms_iss):
616	            # Date normalisation (D15 / props-mapping §3.1)
617	            for v in coerce_list(val):
618	                raw = (v if isinstance(v, str) else
619	                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
620	                for normed in normalize_date(raw):
621	                    if normed:
622	                        lines.append(make_nq(cho_nt, f"<{target_prop}>",
623	                                             f'"{_escape_literal(normed)}"', graph_iri))
624	                        _track(target_prop)
625	            continue
626	
627	        if prop_iri == dcterms_ipart:
628	            # isPartOf URI sanitisation (props-mapping §3.1)
629	            for obj_nt in value_to_nt_obj(val, sani_ctr):
630	                if not obj_nt.startswith("<"):
631	                    continue  # literal isPartOf skipped in mocho graph
632	                uri = obj_nt[1:-1]
633	                if not uri.startswith("http"):
634	                    if len(uri) == 32:
635	                        uri = DDB_ITEM_BASE + uri
636	                    else:
637	                        continue
638	                lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{uri}>", graph_iri))
639	                _track(target_prop)
640	            continue
641	
642	        for obj_nt in value_to_nt_obj(val, sani_ctr):
643	            lines.append(make_nq(cho_nt, f"<{target_prop}>", obj_nt, graph_iri))
644	            _track(target_prop)
645	
646	    # ── Special handlers ──────────────────────────────────────────────────────
647	    _creator_lines = emit_creator_triples(
648	        cho_nt, cho.get("creator"), agents_index, target_class, class_prop_align, graph_iri,
649	    )
650	    lines.extend(_creator_lines)
651	    _track_nqlist(_creator_lines)
652	
653	    _contrib_lines = emit_contributor_triples(
654	        cho_nt, cho.get("contributor"),
655	        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,
656	    )
657	    lines.extend(_contrib_lines)
658	    _track_nqlist(_contrib_lines)
659	
660	    if subject_vals:
661	        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri)
662	        lines.extend(_subject_lines)
663	        _track_nqlist(_subject_lines)
664	
665	    # ── Aggregation & Place ───────────────────────────────────────────────────
666	    agg = rdf.get("Aggregation") or {}
667	    if isinstance(agg, list):
668	        agg = agg[0] if agg else {}
669	    _agg_lines = emit_aggregation_triples(agg, cho_nt, graph_iri)
670	    lines.extend(_agg_lines)
671	    _track_nqlist(_agg_lines)
672	
673	    _place_lines = emit_place_stubs(rdf.get("Place"), graph_iri)
674	    lines.extend(_place_lines)
675	    _track_nqlist(_place_lines)
676	
677	    dispatch_flags["preds_all"]     = preds_all
678	    dispatch_flags["preds_new"]     = preds_new
679	    dispatch_flags["uri_sanitized"] = sani_ctr["uri_sanitized"]
680	    dispatch_flags["uri_split"]     = sani_ctr["uri_split"]
681	    return lines, target_class, wemi, dispatch_flags
682	
```

---

### Assistant *(2026-05-07T11:25:13.634Z)*

Now I have a clear picture of both bugs. Let me also check the `emit_mocho_triples` generic loop for the hasMet path and the rest of emitters.py.

---

### Assistant *(2026-05-07T11:25:14.793Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 30,
  "offset": 595
}
```

---

### User *(2026-05-07T11:25:14.812Z)*

**Tool result**
```
595	    # ── Generic property loop ─────────────────────────────────────────────────
596	    dc_date_iri   = "http://purl.org/dc/elements/1.1/date"
597	    dcterms_iss   = "http://purl.org/dc/terms/issued"
598	    dcterms_ipart = "http://purl.org/dc/terms/isPartOf"
599	    _special_keys = frozenset({"creator", "contributor", "title"}) | SUBJECT_KEYS | _MOCHO_SKIP
600	
601	    subject_vals: list = []
602	    for skey in SUBJECT_KEYS:
603	        subject_vals.extend(coerce_list(cho.get(skey)))
604	
605	    for prop, val in cho.items():
606	        if prop in _special_keys:
607	            continue
608	        prop_iri = _DDBEDM_PROP.get(prop)
609	        if not prop_iri:
610	            continue
611	        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
612	        if not target_prop:
613	            continue
614	
615	        if prop_iri in (dc_date_iri, dcterms_iss):
616	            # Date normalisation (D15 / props-mapping §3.1)
617	            for v in coerce_list(val):
618	                raw = (v if isinstance(v, str) else
619	                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
620	                for normed in normalize_date(raw):
621	                    if normed:
622	                        lines.append(make_nq(cho_nt, f"<{target_prop}>",
623	                                             f'"{_escape_literal(normed)}"', graph_iri))
624	                        _track(target_prop)
```

---

### Assistant *(2026-05-07T11:25:21.620Z)*

I have the full picture now. Both bugs:

1. **Bare ID not expanded**: `value_to_nt_obj` wraps resource values in `<...>` without calling `mint_bare_id`. The `isPartOf` fix (lines 627–640) is the pattern — it wasn't generalized. Affects both graphs, and `emit_subject_triples` too.

2. **`edm:hasMet` on gemea CHO**: `hasMet` is in `_DDBEDM_PROP` but not in `_MOCHO_SKIP`, so the generic property loop in `emit_mocho_triples` emits it on the minted gemea URI. It's an EDM Event property with no mocho alignment.

Three-part fix: add `build_bare_id_index`/`expand_obj_nt` to `utils.py`, wire them into `emit_ddbedm_triples` and the generic loop + subject emitter in `emit_mocho_triples`, and add `hasMet` to `_MOCHO_SKIP`.

---

### Assistant *(2026-05-07T11:25:22.437Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 10,
  "offset": 60
}
```

---

### User *(2026-05-07T11:25:22.441Z)*

**Tool result**
```
60	            for key, val in entity.items():
61	                if key in _skip:
62	                    continue
63	                pred_iri = _DDBEDM_PROP.get(key)
64	                if not pred_iri:
65	                    continue
66	                pred_nt = f"<{pred_iri}>"
67	                curie   = _to_curie(pred_iri)
68	                for obj_nt in value_to_nt_obj(val, sani_ctr):
69	                    lines.append(make_nq(subj_nt, pred_nt, obj_nt, graph_iri))
```

---

### Assistant *(2026-05-07T11:25:24.476Z)*

Now applying all three fixes:

---

### Assistant *(2026-05-07T11:25:31.960Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py",
  "old_string": "def is_ddb_or_gnd(uri: str) -> bool:",
  "new_string": "def build_bare_id_index(rdf: dict) -> dict[str, str]:\n    \"\"\"Map bare about IDs → expanded URIs for every entity in the record (D27).\"\"\"\n    index: dict[str, str] = {}\n    for entity_type, entities in rdf.items():\n        for entity in coerce_list(entities):\n            if not isinstance(entity, dict):\n                continue\n            raw_about = (entity.get(\"about\") or \"\").strip()\n            for part in raw_about.split():\n                if part and not part.startswith((\"http\", \"urn\")):\n                    index[part] = mint_bare_id(entity_type, _sanitize_iri(part))\n    return index\n\n\ndef expand_obj_nt(obj_nt: str, bare_id_to_uri: dict[str, str]) -> str:\n    \"\"\"Resolve a bare-ID IRI object <ID> via the index; return unchanged otherwise.\"\"\"\n    if obj_nt.startswith(\"<\") and obj_nt.endswith(\">\"):\n        inner = obj_nt[1:-1]\n        if not inner.startswith((\"http\", \"urn\")):\n            resolved = bare_id_to_uri.get(inner)\n            if resolved:\n                return f\"<{resolved}>\"\n    return obj_nt\n\n\ndef is_ddb_or_gnd(uri: str) -> bool:"
}
```

---

### User *(2026-05-07T11:33:21.885Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:33:27.715Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "from .utils import (\n    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,\n    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,\n)",
  "new_string": "from .utils import (\n    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,\n    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,\n    build_bare_id_index, expand_obj_nt,\n)"
}
```

---

### User *(2026-05-07T11:33:29.110Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:33:32.242Z)*

Now apply the bare ID expansion in `emit_ddbedm_triples`:

---

### Assistant *(2026-05-07T11:33:35.277Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    lines:     NQList  = []\n    class_ctr: Counter = Counter()\n    pred_ctr:  Counter = Counter()\n    sani_ctr:  Counter = Counter()\n    _skip = frozenset({\"about\"})\n    for entity_type, entities in rdf.items():",
  "new_string": "    lines:     NQList  = []\n    class_ctr: Counter = Counter()\n    pred_ctr:  Counter = Counter()\n    sani_ctr:  Counter = Counter()\n    _skip = frozenset({\"about\"})\n    bare_id_to_uri = build_bare_id_index(rdf)\n    for entity_type, entities in rdf.items():"
}
```

---

### User *(2026-05-07T11:33:36.910Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:33:42.508Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "                for obj_nt in value_to_nt_obj(val, sani_ctr):\n                    lines.append(make_nq(subj_nt, pred_nt, obj_nt, graph_iri))\n                    pred_ctr[curie] += 1\n    return lines, class_ctr, pred_ctr, sani_ctr",
  "new_string": "                for obj_nt in value_to_nt_obj(val, sani_ctr):\n                    lines.append(make_nq(subj_nt, pred_nt,\n                                         expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))\n                    pred_ctr[curie] += 1\n    return lines, class_ctr, pred_ctr, sani_ctr"
}
```

---

### User *(2026-05-07T11:33:53.353Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:33:56.336Z)*

Now fix `emit_subject_triples` to expand bare resource IDs:

---

### Assistant *(2026-05-07T11:34:09.519Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "def emit_subject_triples(\n    cho_nt: str,\n    subject_vals: list,\n    concepts_index: dict[str, dict],\n    graph_iri: str,\n) -> NQList:\n    \"\"\"Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended).\"\"\"\n    lines: NQList = []\n    seen: set[str] = set()\n    for val in subject_vals:\n        if not isinstance(val, dict):\n            continue\n        resource = (val.get(\"resource\") or \"\").strip()\n        label    = (val.get(\"$\")        or \"\").strip()\n        lang     = (val.get(\"lang\")     or \"\").strip()\n        if resource:\n            if resource in seen:\n                continue\n            seen.add(resource)\n            lines.append(make_nq(cho_nt, f\"<{DCTERMS_SUBJECT}>\", f\"<{_sanitize_iri(resource)}>\", graph_iri))\n            concept = concepts_index.get(resource)\n            if concept:\n                for pl in coerce_list(concept.get(\"prefLabel\")):\n                    for obj_nt in value_to_nt_obj(pl):\n                        lines.append(make_nq(f\"<{_sanitize_iri(resource)}>\", f\"<{RDFS_LABEL}>\",\n                                             obj_nt, graph_iri))",
  "new_string": "def emit_subject_triples(\n    cho_nt: str,\n    subject_vals: list,\n    concepts_index: dict[str, dict],\n    graph_iri: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n) -> NQList:\n    \"\"\"Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended).\"\"\"\n    lines: NQList = []\n    seen: set[str] = set()\n    _bare = bare_id_to_uri or {}\n    for val in subject_vals:\n        if not isinstance(val, dict):\n            continue\n        resource = (val.get(\"resource\") or \"\").strip()\n        label    = (val.get(\"$\")        or \"\").strip()\n        lang     = (val.get(\"lang\")     or \"\").strip()\n        if resource:\n            # Expand bare IDs: look up in the per-record index, fall back to Concept mint\n            if not resource.startswith((\"http\", \"urn\")):\n                expanded = _bare.get(resource) or mint_bare_id(\"Concept\", resource)\n            else:\n                expanded = resource\n            expanded_safe = _sanitize_iri(expanded)\n            if expanded_safe in seen:\n                continue\n            seen.add(expanded_safe)\n            lines.append(make_nq(cho_nt, f\"<{DCTERMS_SUBJECT}>\", f\"<{expanded_safe}>\", graph_iri))\n            concept = concepts_index.get(resource) or concepts_index.get(expanded)\n            if concept:\n                for pl in coerce_list(concept.get(\"prefLabel\")):\n                    for obj_nt in value_to_nt_obj(pl):\n                        lines.append(make_nq(f\"<{expanded_safe}>\", f\"<{RDFS_LABEL}>\",\n                                             obj_nt, graph_iri))"
}
```

---

### User *(2026-05-07T11:34:15.070Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:34:18.490Z)*

Now wire up the bare_id_to_uri in `emit_mocho_triples` — build the index, use it in the generic loop, and pass it to `emit_subject_triples`:

---

### Assistant *(2026-05-07T11:34:21.665Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    lines:     NQList  = []\n    preds_all: Counter = Counter()\n    preds_new: Counter = Counter()\n    sani_ctr:  Counter = Counter()\n\n    def _track(pred_iri: str) -> None:",
  "new_string": "    lines:     NQList  = []\n    preds_all: Counter = Counter()\n    preds_new: Counter = Counter()\n    sani_ctr:  Counter = Counter()\n    bare_id_to_uri = build_bare_id_index(rdf)\n\n    def _track(pred_iri: str) -> None:"
}
```

---

### User *(2026-05-07T11:34:23.323Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:34:28.545Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        for obj_nt in value_to_nt_obj(val, sani_ctr):\n            lines.append(make_nq(cho_nt, f\"<{target_prop}>\", obj_nt, graph_iri))\n            _track(target_prop)",
  "new_string": "        for obj_nt in value_to_nt_obj(val, sani_ctr):\n            lines.append(make_nq(cho_nt, f\"<{target_prop}>\",\n                                 expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))\n            _track(target_prop)"
}
```

---

### User *(2026-05-07T11:34:30.224Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:34:34.579Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    if subject_vals:\n        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri)",
  "new_string": "    if subject_vals:\n        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri,\n                                              bare_id_to_uri)"
}
```

---

### User *(2026-05-07T11:34:36.175Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:34:42.321Z)*

Now add `hasMet` to `_MOCHO_SKIP`:

---

### Assistant *(2026-05-07T11:34:45.764Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "_MOCHO_SKIP = frozenset({\n    \"about\", \"hierarchyType\",\n    \"creator\", \"contributor\",\n    \"dcSubject\", \"dcTermsSubject\", \"dcTermSubject\",\n    \"dcType\",\n    \"aggregationEntity\", \"hierarchyPosition\",\n})",
  "new_string": "_MOCHO_SKIP = frozenset({\n    \"about\", \"hierarchyType\",\n    \"creator\", \"contributor\",\n    \"dcSubject\", \"dcTermsSubject\", \"dcTermSubject\",\n    \"dcType\",\n    \"aggregationEntity\", \"hierarchyPosition\",\n    \"hasMet\",   # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph\n})"
}
```

---

### User *(2026-05-07T11:35:02.127Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:35:04.956Z)*

Let me verify the changes look correct, then add a test.

---

### Assistant *(2026-05-07T11:35:06.017Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && python -c \"from scripts.transform import emitters, utils, constants; print('imports OK')\"",
  "description": "Verify imports work after changes"
}
```

---

### Assistant *(2026-05-07T11:35:06.629Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "limit": 80
}
```

---

### User *(2026-05-07T11:35:07.755Z)*

**Tool result**
```
imports OK
```

---

### User *(2026-05-07T11:35:07.775Z)*

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
28	)
29	from transform.emitters import (
30	    retype_entities,
31	    emit_creator_triples,
32	    emit_contributor_triples,
33	    emit_subject_triples,
34	    emit_aggregation_triples,
35	    emit_place_stubs,
36	    werk_staging_row,
37	)
38	from transform.loaders import load_mediatype_class, load_htype_map
39	
40	# Config table paths
41	_CONFIG = PROJECT_DIR / "output" / "config"
42	
43	
44	# ── Helpers ───────────────────────────────────────────────────────────────────
45	
46	def _rdf_types(lines: list[str]) -> set[str]:
47	    """Extract the object IRIs from all rdf:type triples in a list of N-Quads lines."""
48	    rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
49	    result: set[str] = set()
50	    for line in lines:
51	        parts = line.split()
52	        if len(parts) >= 4 and f"<{rdf_type}>" in parts[1]:
53	            obj = parts[2].strip("<>")
54	            result.add(obj)
55	    return result
56	
57	
58	def _predicates(lines: list[str]) -> set[str]:
59	    result: set[str] = set()
60	    for line in lines:
61	        parts = line.split()
62	        if len(parts) >= 4:
63	            result.add(parts[1].strip("<>"))
64	    return result
65	
66	
67	def _load_configs():
68	    mc_map = load_mediatype_class(_CONFIG / "lookup_mediatype_class.csv")
69	    ht_map = load_htype_map(_CONFIG / "lookup_htype_doco_rico.csv")
70	    return mc_map, ht_map
71	
72	
73	# ── normalize_date ────────────────────────────────────────────────────────────
74	
75	class TestNormalizeDate:
76	    def test_compact_yyyymmdd(self):
77	        assert normalize_date("19870315") == ["1987-03-15"]
78	
79	    def test_iso_interval(self):
80	        result = normalize_date("1900/1950")
```

---

### Assistant *(2026-05-07T11:35:10.114Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "limit": 50,
  "offset": 80
}
```

---

### User *(2026-05-07T11:35:10.116Z)*

**Tool result**
```
80	        result = normalize_date("1900/1950")
81	        assert result == ["1900", "1950"]
82	
83	    def test_passthrough(self):
84	        assert normalize_date("ca. 1900") == ["ca. 1900"]
85	
86	    def test_iso_already(self):
87	        assert normalize_date("2026-05-01") == ["2026-05-01"]
88	
89	
90	# ── mint_bare_id ──────────────────────────────────────────────────────────────
91	
92	class TestMintBareId:
93	    _id = "A" * 32
94	
95	    def test_providedcho_bare_id(self):
96	        result = mint_bare_id("ProvidedCHO", self._id)
97	        assert result == f"http://www.deutsche-digitale-bibliothek.de/item/{self._id}"
98	
99	    def test_other_entity_bare_id(self):
100	        result = mint_bare_id("Agent", self._id)
101	        assert result == f"urn:ddbedm:Agent:{self._id}"
102	
103	    def test_full_uri_passthrough(self):
104	        uri = "http://d-nb.info/gnd/1234567"
105	        assert mint_bare_id("Agent", uri) == uri
106	
107	    def test_urn_passthrough(self):
108	        urn = "urn:ddbedm:Agent:12345"
109	        assert mint_bare_id("Agent", urn) == urn
110	
111	
112	# ── value_to_nt_obj ───────────────────────────────────────────────────────────
113	
114	class TestValueToNtObj:
115	    def test_string(self):
116	        assert value_to_nt_obj("hello") == ['"hello"']
117	
118	    def test_empty_string(self):
119	        assert value_to_nt_obj("") == []
120	
121	    def test_none(self):
122	        assert value_to_nt_obj(None) == []
123	
124	    def test_resource_dict(self):
125	        assert value_to_nt_obj({"resource": "http://example.org/"}) == ["<http://example.org/>"]
126	
127	    def test_lang_dict(self):
128	        result = value_to_nt_obj({"$": "Faust", "lang": "de"})
129	        assert result == ['"Faust"@de']
```

---

### Assistant *(2026-05-07T11:35:13.058Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "limit": 100,
  "offset": 130
}
```

---

### User *(2026-05-07T11:35:13.063Z)*

**Tool result**
```
130	
131	    def test_no_lang_dict(self):
132	        result = value_to_nt_obj({"$": "Faust", "lang": None})
133	        assert result == ['"Faust"']
134	
135	    def test_list_flattened(self):
136	        result = value_to_nt_obj([{"$": "A", "lang": "de"}, {"$": "B", "lang": "en"}])
137	        assert '"A"@de' in result and '"B"@en' in result
138	
139	    def test_escape_quotes(self):
140	        result = value_to_nt_obj('say "hi"')
141	        assert result == ['"say \\"hi\\""']
142	
143	    def test_escape_newlines(self):
144	        result = value_to_nt_obj("line1\nline2\r\nline3")
145	        assert result == ['"line1\\nline2\\r\\nline3"']
146	
147	
148	# ── get_object_id ─────────────────────────────────────────────────────────────
149	
150	class TestGetObjectId:
151	    _id = "B" * 32
152	
153	    def test_full_url(self):
154	        record = {"edm": {"RDF": {"ProvidedCHO": {"about": f"http://www.deutsche-digitale-bibliothek.de/item/{self._id}"}}}}
155	        assert get_object_id(record) == self._id
156	
157	    def test_bare_id(self):
158	        record = {"edm": {"RDF": {"ProvidedCHO": {"about": self._id}}}}
159	        assert get_object_id(record) == self._id
160	
161	    def test_missing_about(self):
162	        record = {"edm": {"RDF": {"ProvidedCHO": {}}}}
163	        assert get_object_id(record) is None
164	
165	    def test_missing_cho(self):
166	        record = {"edm": {"RDF": {}}}
167	        assert get_object_id(record) is None
168	
169	
170	# ── retype_entities ───────────────────────────────────────────────────────────
171	
172	@pytest.fixture(scope="module")
173	def configs():
174	    return _load_configs()
175	
176	
177	_SPARTE001 = "http://ddb.vocnet.org/sparte/sparte001"
178	_SPARTE002 = "http://ddb.vocnet.org/sparte/sparte002"
179	_SPARTE003 = "http://ddb.vocnet.org/sparte/sparte003"
180	_MT001     = "http://ddb.vocnet.org/medientyp/mt001"
181	_MT002     = "http://ddb.vocnet.org/medientyp/mt002"
182	_MT003     = "http://ddb.vocnet.org/medientyp/mt003"
183	_MT007     = "http://ddb.vocnet.org/medientyp/mt007"
184	
185	
186	class TestRetypeEntities:
187	    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "C" * 32 + ">"
188	
189	    def _call(self, sector, mediatype, htype, configs, dctype_vals=None):
190	        mc_map, ht_map = configs
191	        return retype_entities(
192	            sector, mediatype, htype, dctype_vals or [],
193	            self._cho_nt, mc_map, ht_map, {}, GRAPH_MOCHO,
194	        )
195	
196	    def test_sparte004_mt003_no_htype_fallback(self, configs):
197	        """sparte004/mt003 use_htype=True; no htype → fixed M class rdac:C10007."""
198	        _SPARTE004 = "http://ddb.vocnet.org/sparte/sparte004"
199	        lines, target_class, wemi, _flags = self._call(_SPARTE004, _MT003, None, configs)
200	        types = _rdf_types(lines)
201	        assert "http://rdaregistry.info/Elements/c/C10007" in types
202	        assert wemi == "M"
203	
204	    def test_sparte001_mt003_htype021(self, configs):
205	        """sparte001/mt003 use_htype=True; htype_021 → rdac:C10001+C10007 from htype, mocho:Manifestation added."""
206	        lines, target_class, wemi, _flags = self._call(_SPARTE001, _MT003, "htype_021", configs)
207	        types = _rdf_types(lines)
208	        assert "http://rdaregistry.info/Elements/c/C10001" in types
209	        assert "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation" in types
210	        assert wemi == "W"
211	
212	    def test_sparte003_mt001_fixed(self, configs):
213	        """sparte003/mt001 use_htype=False → mocho:ImmovableWork (W) + aco:AudioManifestation (M)."""
214	        lines, target_class, wemi, _flags = self._call(_SPARTE003, _MT001, None, configs)
215	        types = _rdf_types(lines)
216	        assert MOCHO_NS + "ImmovableWork" in types
217	        assert "https://w3id.org/ac-ontology/aco#AudioManifestation" in types
218	
219	    def test_mt007_guard_does_not_add_types_here(self, configs):
220	        """retype_entities itself doesn't know about mt007; caller guards. Falls back to mocho:Manifestation."""
221	        lines, target_class, wemi, _flags = self._call(_SPARTE001, _MT007, None, configs)
222	        assert target_class != ""  # always returns something
223	
224	    def test_unknown_sector_mediatype_fallback(self, configs):
225	        """Unknown (sector, mediatype) → ('any','any') D9 fallback mocho:Manifestation."""
226	        lines, target_class, wemi, _flags = self._call("any", "any", None, configs)
227	        types = _rdf_types(lines)
228	        assert MOCHO_NS + "Manifestation" in types
229	        assert target_class == MOCHO_NS + "Manifestation"
```

---

### Assistant *(2026-05-07T11:35:15.928Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "limit": 100,
  "offset": 229
}
```

---

### User *(2026-05-07T11:35:15.931Z)*

**Tool result**
```
229	        assert target_class == MOCHO_NS + "Manifestation"
230	
231	
232	# ── emit_creator_triples ──────────────────────────────────────────────────────
233	
234	class TestEmitCreatorTriples:
235	    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "D" * 32 + ">"
236	    _agent_uri = "http://d-nb.info/gnd/118540238"
237	    _rdac_c10007 = "http://rdaregistry.info/Elements/c/C10007"
238	    _rdam_P30329 = "http://rdaregistry.info/Elements/m/P30329"
239	
240	    def _agents_index(self):
241	        return {
242	            self._agent_uri: {
243	                "about":     self._agent_uri,
244	                "prefLabel": "Goethe, Johann Wolfgang von",
245	            }
246	        }
247	
248	    def _align(self):
249	        """Minimal class_prop_align for rdac:C10007/dc:creator → rdam:P30329."""
250	        dc_creator = "http://purl.org/dc/elements/1.1/creator"
251	        return {(self._rdac_c10007, dc_creator): self._rdam_P30329}
252	
253	    def test_track1_iri(self):
254	        vals = [{"resource": self._agent_uri, "$": "", "lang": ""}]
255	        lines = emit_creator_triples(
256	            self._cho_nt, vals, {}, self._rdac_c10007, self._align(), GRAPH_MOCHO,
257	        )
258	        preds = _predicates(lines)
259	        assert self._rdam_P30329 in preds
260	
261	    def test_track2_agent_stub(self):
262	        vals = [{"resource": self._agent_uri, "$": "Goethe", "lang": ""}]
263	        lines = emit_creator_triples(
264	            self._cho_nt, vals, self._agents_index(), self._rdac_c10007,
265	            self._align(), GRAPH_MOCHO,
266	        )
267	        preds = _predicates(lines)
268	        assert "http://purl.org/dc/terms/creator" in preds
269	        assert "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in preds
270	
271	    def test_label_only_no_track2(self):
272	        """Label-only creator: Track 2 is silent (no dcterms:creator without URI)."""
273	        vals = [{"resource": "", "$": "Unbekannt", "lang": "de"}]
274	        lines = emit_creator_triples(
275	            self._cho_nt, vals, {}, self._rdac_c10007, self._align(), GRAPH_MOCHO,
276	        )
277	        assert "http://purl.org/dc/terms/creator" not in _predicates(lines)
278	        assert self._rdam_P30329 in _predicates(lines)
279	
280	    def test_no_match_no_crash(self):
281	        lines = emit_creator_triples(
282	            self._cho_nt, [], {}, self._rdac_c10007, {}, GRAPH_MOCHO,
283	        )
284	        assert lines == []
285	
286	
287	# ── emit_contributor_triples ──────────────────────────────────────────────────
288	
289	class TestEmitContributorTriples:
290	    _cho_nt   = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "E" * 32 + ">"
291	    _agent_uri = "http://d-nb.info/gnd/987654321"
292	    _lido_creation = "http://terminology.lido-schema.org/lido00012"
293	    _rdac_c10007   = "http://rdaregistry.info/Elements/c/C10007"
294	
295	    def test_lido_dispatch_matched(self):
296	        event_idx = {self._agent_uri: self._lido_creation}
297	        lido_row = {
298	            "rdam_agent_prop": "http://rdaregistry.info/Elements/m/P30329",
299	            "dc_agent_fallback": "http://purl.org/dc/elements/1.1/contributor",
300	        }
301	        lido_dispatch = {self._lido_creation: lido_row}
302	        vals = [{"resource": self._agent_uri, "$": "Schiller", "lang": ""}]
303	        lines = emit_contributor_triples(
304	            self._cho_nt, vals, event_idx, lido_dispatch,
305	            self._rdac_c10007, "M", GRAPH_MOCHO,
306	        )
307	        preds = _predicates(lines)
308	        assert "http://rdaregistry.info/Elements/m/P30329" in preds
309	
310	    def test_no_event_fallback_dc_contributor(self):
311	        vals = [{"resource": self._agent_uri, "$": "X", "lang": ""}]
312	        lines = emit_contributor_triples(
313	            self._cho_nt, vals, {}, {}, self._rdac_c10007, "M", GRAPH_MOCHO,
314	        )
315	        preds = _predicates(lines)
316	        assert "http://purl.org/dc/elements/1.1/contributor" in preds
317	
318	    def test_label_only_literal_fallback(self):
319	        vals = [{"resource": "", "$": "Anonym", "lang": "de"}]
320	        lines = emit_contributor_triples(
321	            self._cho_nt, vals, {}, {}, self._rdac_c10007, "M", GRAPH_MOCHO,
322	        )
323	        preds = _predicates(lines)
324	        assert "http://purl.org/dc/elements/1.1/contributor" in preds
325	        assert any('"Anonym"@de' in nq for nq in lines)
326	
327	
328	# ── emit_subject_triples ──────────────────────────────────────────────────────
```

---

### Assistant *(2026-05-07T11:35:19.221Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "limit": 100,
  "offset": 328
}
```

---

### User *(2026-05-07T11:35:19.226Z)*

**Tool result**
```
328	# ── emit_subject_triples ──────────────────────────────────────────────────────
329	
330	class TestEmitSubjectTriples:
331	    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "F" * 32 + ">"
332	
333	    def test_iri_subject(self):
334	        vals = [{"resource": "http://d-nb.info/gnd/4018197-4", "$": "Faust", "lang": "de"}]
335	        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
336	        preds = _predicates(lines)
337	        assert "http://purl.org/dc/terms/subject" in preds
338	
339	    def test_literal_subject(self):
340	        vals = [{"resource": "", "$": "Goethe", "lang": "de"}]
341	        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
342	        preds = _predicates(lines)
343	        assert "http://purl.org/dc/elements/1.1/subject" in preds
344	
345	    def test_dedup(self):
346	        uri = "http://d-nb.info/gnd/4018197-4"
347	        vals = [
348	            {"resource": uri, "$": "Faust", "lang": "de"},
349	            {"resource": uri, "$": "Faust", "lang": "de"},
350	        ]
351	        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
352	        dcterms_sub_lines = [l for l in lines if "terms/subject" in l]
353	        assert len(dcterms_sub_lines) == 1
354	
355	
356	# ── emit_place_stubs ──────────────────────────────────────────────────────────
357	
358	class TestEmitPlaceStubs:
359	    def test_emits_label(self):
360	        places = [{"about": "http://example.org/place/1",
361	                   "prefLabel": [{"$": "Weimar", "lang": "de"}]}]
362	        lines = emit_place_stubs(places, GRAPH_MOCHO)
363	        assert any('"Weimar"@de' in nq for nq in lines)
364	
365	    def test_no_about_skipped(self):
366	        places = [{"prefLabel": [{"$": "Weimar", "lang": "de"}]}]
367	        lines = emit_place_stubs(places, GRAPH_MOCHO)
368	        assert lines == []
369	
370	    def test_none_input(self):
371	        assert emit_place_stubs(None, GRAPH_MOCHO) == []
372	
373	
374	# ── werk_staging_row ──────────────────────────────────────────────────────────
375	
376	class TestWerkStagingRow:
377	    _cho_uri = "https://gemea.ise.fiz-karlsruhe.de/mocho/" + "G" * 32
378	    _rdac_c10001 = "http://rdaregistry.info/Elements/c/C10001"
379	    _rdac_c10007 = "http://rdaregistry.info/Elements/c/C10007"
380	
381	    def test_w_slot_returns_row(self):
382	        cho = {"title": {"$": "Faust", "lang": "de"},
383	               "creator": [{"resource": "http://d-nb.info/gnd/118540238", "$": "Goethe"}]}
384	        row = werk_staging_row(self._cho_uri, cho, self._rdac_c10001)
385	        assert row is not None
386	        assert row["dc_title"] == "Faust"
387	        assert "http://d-nb.info/gnd/118540238" in row["creator_uris"]
388	
389	    def test_m_slot_returns_none(self):
390	        cho = {"title": {"$": "Faust"}}
391	        row = werk_staging_row(self._cho_uri, cho, self._rdac_c10007)
392	        assert row is None
393	
394	    def test_obj_id_extracted(self):
395	        cho = {}
396	        row = werk_staging_row(self._cho_uri, cho, self._rdac_c10001)
397	        assert row["ddb_obj_id"] == "G" * 32
398	
399	
400	# ── make_nq ───────────────────────────────────────────────────────────────────
401	
402	def test_make_nq_format():
403	    line = make_nq("<http://s>", "<http://p>", '"o"', "https://graph/g")
404	    assert line == '<http://s> <http://p> "o" <https://graph/g> .'
405	
```

---

### Assistant *(2026-05-07T11:35:29.240Z)*

Now I'll add tests. I need to import the new utils and `emit_ddbedm_triples`, and add test classes for both bugs.

---

### Assistant *(2026-05-07T11:35:33.997Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.utils import (\n    coerce_list,\n    make_nq,\n    mint_bare_id,\n    mint_cho_uri,\n    normalize_date,\n    value_to_nt_obj,\n    _escape_literal,\n    get_object_id,\n)\nfrom transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n)",
  "new_string": "from transform.utils import (\n    coerce_list,\n    make_nq,\n    mint_bare_id,\n    mint_cho_uri,\n    normalize_date,\n    value_to_nt_obj,\n    _escape_literal,\n    get_object_id,\n    build_bare_id_index,\n    expand_obj_nt,\n)\nfrom transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n)\nfrom transform.constants import _MOCHO_SKIP"
}
```

---

### User *(2026-05-07T11:35:39.443Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:35:42.005Z)*

Now add the new test classes at the end of the file:

---

### Assistant *(2026-05-07T11:36:12.362Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "def test_make_nq_format():\n    line = make_nq(\"<http://s>\", \"<http://p>\", '\"o\"', \"https://graph/g\")\n    assert line == '<http://s> <http://p> \"o\" <https://graph/g> .'",
  "new_string": "def test_make_nq_format():\n    line = make_nq(\"<http://s>\", \"<http://p>\", '\"o\"', \"https://graph/g\")\n    assert line == '<http://s> <http://p> \"o\" <https://graph/g> .'\n\n\n# ── build_bare_id_index / expand_obj_nt ──────────────────────────────────────\n\n_BARE_CONCEPT = \"J\" * 32\n_BARE_PLACE   = \"K\" * 32\n_BARE_AGENT   = \"L\" * 32\n\nclass TestBuildBareIdIndex:\n    def _rdf(self):\n        return {\n            \"Concept\": [{\"about\": _BARE_CONCEPT, \"prefLabel\": [{\"$\": \"Test\", \"lang\": \"de\"}]}],\n            \"Place\":   [{\"about\": _BARE_PLACE,   \"prefLabel\": [{\"$\": \"Berlin\", \"lang\": \"de\"}]}],\n            \"Agent\":   [{\"about\": f\"http://d-nb.info/gnd/99999\", \"prefLabel\": \"Name\"}],\n        }\n\n    def test_bare_concept_indexed(self):\n        idx = build_bare_id_index(self._rdf())\n        assert _BARE_CONCEPT in idx\n        assert idx[_BARE_CONCEPT] == f\"urn:ddbedm:Concept:{_BARE_CONCEPT}\"\n\n    def test_bare_place_indexed(self):\n        idx = build_bare_id_index(self._rdf())\n        assert idx[_BARE_PLACE] == f\"urn:ddbedm:Place:{_BARE_PLACE}\"\n\n    def test_full_uri_not_indexed(self):\n        idx = build_bare_id_index(self._rdf())\n        assert \"http://d-nb.info/gnd/99999\" not in idx\n\n    def test_empty_rdf(self):\n        assert build_bare_id_index({}) == {}\n\n\nclass TestExpandObjNt:\n    _idx = {_BARE_CONCEPT: f\"urn:ddbedm:Concept:{_BARE_CONCEPT}\"}\n\n    def test_bare_id_resolved(self):\n        result = expand_obj_nt(f\"<{_BARE_CONCEPT}>\", self._idx)\n        assert result == f\"<urn:ddbedm:Concept:{_BARE_CONCEPT}>\"\n\n    def test_full_uri_unchanged(self):\n        result = expand_obj_nt(\"<http://example.org/foo>\", self._idx)\n        assert result == \"<http://example.org/foo>\"\n\n    def test_urn_unchanged(self):\n        result = expand_obj_nt(\"<urn:ddbedm:Concept:XXXX>\", self._idx)\n        assert result == \"<urn:ddbedm:Concept:XXXX>\"\n\n    def test_literal_unchanged(self):\n        result = expand_obj_nt('\"hello\"@de', self._idx)\n        assert result == '\"hello\"@de'\n\n    def test_unknown_bare_id_unchanged(self):\n        result = expand_obj_nt(f\"<{'Z' * 32}>\", self._idx)\n        assert result == f\"<{'Z' * 32}>\"\n\n\n# ── emit_ddbedm_triples: bare-ID expansion in property objects ─────────────────\n\n_DDB_ITEM = \"http://www.deutsche-digitale-bibliothek.de/item/\"\n_BARE_CHO  = \"M\" * 32\n_BARE_CONC = \"N\" * 32\n\nclass TestEmitDdbedmBareIds:\n    \"\"\"Bare IDs in property-object positions must be expanded to match entity subjects.\"\"\"\n\n    def _rdf(self):\n        return {\n            \"ProvidedCHO\": [{\n                \"about\":          _BARE_CHO,\n                \"dcTermsSubject\": {\"resource\": _BARE_CONC},\n            }],\n            \"Concept\": [{\"about\": _BARE_CONC}],\n        }\n\n    def test_subject_object_expanded(self):\n        lines, _, _, _ = emit_ddbedm_triples(self._rdf(), \"https://test/graph\")\n        subj_line = next(\n            (l for l in lines if \"terms/subject\" in l), None\n        )\n        assert subj_line is not None, \"dcterms:subject triple not emitted\"\n        assert f\"urn:ddbedm:Concept:{_BARE_CONC}\" in subj_line, (\n            f\"bare ID not expanded; got: {subj_line}\"\n        )\n\n    def test_cho_subject_expanded(self):\n        lines, _, _, _ = emit_ddbedm_triples(self._rdf(), \"https://test/graph\")\n        cho_uri = _DDB_ITEM + _BARE_CHO\n        assert any(cho_uri in l for l in lines), \"CHO subject URI not expanded\"\n\n    def test_no_bare_id_iri_in_output(self):\n        lines, _, _, _ = emit_ddbedm_triples(self._rdf(), \"https://test/graph\")\n        for line in lines:\n            parts = line.split()\n            for part in parts:\n                if part.startswith(\"<\") and part.endswith(\">\"):\n                    inner = part[1:-1]\n                    assert inner.startswith((\"http\", \"urn\")), (\n                        f\"bare IRI in output: {part}\\n  line: {line}\"\n                    )\n\n\n# ── emit_subject_triples: bare-ID expansion ───────────────────────────────────\n\nclass TestEmitSubjectTriplesBareId:\n    _cho_nt = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"P\" * 32 + \">\"\n    _bare   = \"Q\" * 32\n\n    def test_bare_id_expanded_via_index(self):\n        bare_id_to_uri = {self._bare: f\"urn:ddbedm:Concept:{self._bare}\"}\n        vals = [{\"resource\": self._bare, \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, bare_id_to_uri)\n        assert any(f\"urn:ddbedm:Concept:{self._bare}\" in l for l in lines)\n\n    def test_bare_id_fallback_concept_mint(self):\n        \"\"\"No index entry → mint as Concept URN as fallback.\"\"\"\n        vals = [{\"resource\": self._bare, \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, {})\n        assert any(f\"urn:ddbedm:Concept:{self._bare}\" in l for l in lines)\n\n    def test_full_uri_unchanged(self):\n        uri = \"http://d-nb.info/gnd/4018197-4\"\n        vals = [{\"resource\": uri, \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_subject_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, {})\n        assert any(uri in l for l in lines)\n\n    def test_label_stub_uses_expanded_uri(self):\n        bare_id_to_uri = {self._bare: f\"urn:ddbedm:Concept:{self._bare}\"}\n        concept = {\"about\": self._bare, \"prefLabel\": [{\"$\": \"Faust\", \"lang\": \"de\"}]}\n        vals = [{\"resource\": self._bare, \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_subject_triples(\n            self._cho_nt, vals, {self._bare: concept}, GRAPH_MOCHO, bare_id_to_uri\n        )\n        label_line = next((l for l in lines if '\"Faust\"@de' in l), None)\n        assert label_line is not None\n        assert f\"urn:ddbedm:Concept:{self._bare}\" in label_line\n\n\n# ── _MOCHO_SKIP: hasMet excluded from mocho graph ────────────────────────────\n\ndef test_hasmet_in_mocho_skip():\n    assert \"hasMet\" in _MOCHO_SKIP, \"hasMet must be in _MOCHO_SKIP to prevent edm:hasMet on gemea CHOs\""
}
```

---

### User *(2026-05-07T11:36:25.848Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:36:29.525Z)*

**Tool call:** `Bash`
```json
{
  "command": "python -m pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -30",
  "description": "Run tests to verify all pass"
}
```

---

### User *(2026-05-07T11:36:31.612Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python: No module named pytest
```

---

### Assistant *(2026-05-07T11:36:33.944Z)*

**Tool call:** `Bash`
```json
{
  "command": "python -m pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -40",
  "description": "Run tests from project root"
}
```

---

### User *(2026-05-07T11:36:35.202Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python: No module named pytest
```

---

### Assistant *(2026-05-07T11:36:37.406Z)*

**Tool call:** `Bash`
```json
{
  "command": "python -m pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -40",
  "description": "Run tests from goethe-faust directory"
}
```

---

### User *(2026-05-07T11:36:38.470Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python: No module named pytest
```

---

### Assistant *(2026-05-07T11:36:40.702Z)*

**Tool call:** `Bash`
```json
{
  "command": "which python3 && python3 -m pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -40",
  "description": "Run tests with python3",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T11:36:41.840Z)*

**Tool result**
```
/Users/mta/Documents/claude/gemea/.venv/bin/python3
/Users/mta/Documents/claude/gemea/.venv/bin/python3: No module named pytest
```

---

### Assistant *(2026-05-07T11:36:44.985Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/goethe-faust/.venv/bin/ 2>/dev/null || find /Users/mta/Documents/claude/goethe-faust -name \"pytest\" 2>/dev/null | head -5",
  "description": "Find pytest in goethe-faust venv",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T11:36:46.864Z)*

**Tool result**
```
Activate.ps1
activate
activate.csh
activate.fish
f2py
numpy-config
pip
pip3
pip3.9
py.test
pygmentize
pytest
python
python3
python3.9
```

---

### Assistant *(2026-05-07T11:36:50.157Z)*

**Tool call:** `Bash`
```json
{
  "command": ".venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -40",
  "description": "Run tests with goethe-faust venv pytest",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T11:36:53.124Z)*

**Tool result**
```
............................................................             [100%]
60 passed in 0.09s
```

---

### Assistant *(2026-05-07T11:37:03.381Z)*

All 60 tests pass (including 16 new ones). Now addressing your question about where `_MOCHO_SKIP` values came from.

---

**Re: where did `_MOCHO_SKIP` values come from?**

Looking at [constants.py:99–106](goethe-faust/scripts/transform/constants.py):

```python
_MOCHO_SKIP = frozenset({
    "about", "hierarchyType",
    "creator", "contributor",
    "dcSubject", "dcTermsSubject", "dcTermSubject",
    "dcType",
    "aggregationEntity", "hierarchyPosition",
})
```

Each entry was added for a distinct reason:

| Key | Why skipped in mocho graph |
|---|---|
| `about` | It's the entity subject, not a property |
| `hierarchyType` | DDB-internal structural field (D27); handled separately by `retype_entities` |
| `creator`, `contributor` | Handled by dedicated emitters (`emit_creator_triples`, `emit_contributor_triples`) with LIDO dispatch |
| `dcSubject`, `dcTermsSubject`, `dcTermSubject` | Handled by `emit_subject_triples` with Concept lookup |
| `dcType` | Consumed by `retype_entities` for class dispatch; not re-emitted |
| `aggregationEntity`, `hierarchyPosition` | DDB-internal structural fields with no mocho mapping |

`hasMet` I just added: it's in `_DDBEDM_PROP` (so it passes through to the ddbedm graph correctly), but it has no mocho alignment — so without the skip, the generic loop emitted it raw as `edm:hasMet` on the gemea CHO URI.

---

### User *(2026-05-07T11:41:33.965Z)*

update retype_entities to also emit ddb:hierarchyType in the mocho graph.

---

### Assistant *(2026-05-07T11:41:36.978Z)*

Let me read the `retype_entities` function and the relevant constants.

---

### Assistant *(2026-05-07T11:41:37.946Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 80,
  "offset": 196
}
```

---

### User *(2026-05-07T11:41:37.968Z)*

**Tool result**
```
196	                lines.append(make_nq(src_nt, f"<{DCTERMS_SOURCE}>", f"<{lpath}>", graph_iri))
197	
198	    return lines
199	
200	
201	def retype_entities(
202	    sector: str,
203	    mediatype: str,
204	    htype_code: str | None,
205	    dctype_vals: list,
206	    cho_nt: str,
207	    mediatype_class_map: dict,
208	    htype_map: dict,
209	    audio_type2class: dict,
210	    graph_iri: str,
211	) -> tuple[NQList, str, str, dict]:
212	    """Dispatch rdf:type triples for a ProvidedCHO (§6.4, transform-revised-plan.md §1.1).
213	
214	    Returns (lines, target_class_full_iri, wemi, dispatch_flags).
215	    target_class is used for property alignment lookup; wemi for contributor column selection.
216	    dispatch_flags: {"htype_used": bool, "fallback": bool}
217	    """
218	    lines: NQList = []
219	    row = (
220	        mediatype_class_map.get((sector, mediatype))
221	        or mediatype_class_map.get(("any", "any"))
222	        or {}
223	    )
224	    use_htype  = row.get("use_htype", False)
225	    rdf_type_w = row.get("rdf_type_w", "")
226	    rdf_type_m = row.get("rdf_type_m", "")
227	
228	    primary_class = ""
229	    htype_used    = False
230	
231	    # Layer 1: htype-derived class (for htype-first strata)
232	    if use_htype and htype_code:
233	        entry = htype_map.get(htype_code)
234	        if entry:
235	            type_iris, rst_iris = entry
236	            for t in type_iris:
237	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{t}>", graph_iri))
238	            for r in rst_iris:
239	                lines.append(make_nq(cho_nt, f"<{RICO_HAS_RST}>", f"<{r}>", graph_iri))
240	            primary_class = type_iris[0]  # first = most specific
241	            htype_used    = True
242	
243	    # Layer 2: fixed mediatype class (always emit if set; added on top of layer 1)
244	    if rdf_type_w:
245	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_w}>", graph_iri))
246	        if not primary_class:
247	            primary_class = rdf_type_w
248	    if rdf_type_m:
249	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_m}>", graph_iri))
250	        if not primary_class:
251	            primary_class = rdf_type_m
252	
253	    # Audio group dispatch: dc:type → mo:MusicalManifestation (Group A) (§2.3)
254	    _aco_audio = "https://w3id.org/ac-ontology/aco#AudioManifestation"
255	    _mo_mani   = "http://purl.org/ontology/mo/MusicalManifestation"
256	    if rdf_type_m == _aco_audio and dctype_vals and not use_htype:
257	        for dct in dctype_vals:
258	            dc_text = (dct.get("$") or "").strip() if isinstance(dct, dict) else ""
259	            if audio_type2class.get((sector, dc_text)) == "A":
260	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{_mo_mani}>", graph_iri))
261	                primary_class = _mo_mani
262	                break
263	
264	    # D9 fallback — no class resolved
265	    is_fallback = not primary_class
266	    if is_fallback:
267	        fallback = MOCHO_NS + "Manifestation"
268	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{fallback}>", graph_iri))
269	        primary_class = fallback
270	
271	    wemi = _CLASS_WEMI.get(primary_class, "M")
272	    return lines, primary_class, wemi, {"htype_used": htype_used, "fallback": is_fallback}
273	
274	
275	def emit_subject_triples(
```

---

### Assistant *(2026-05-07T11:41:38.888Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"hierarchyType\\|ddb:\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "description": "Find hierarchyType and ddb: IRI in constants"
}
```

---

### User *(2026-05-07T11:41:38.942Z)*

**Tool result**
```
100:    "about", "hierarchyType",
295:    "hierarchyType":      "http://www.deutsche-digitale-bibliothek.de/hierarchyType",
```

---

### Assistant *(2026-05-07T11:42:03.306Z)*

The predicate IRI is already in `_DDBEDM_PROP` as `DDB_BASE + "/hierarchyType"`. The change is: add a named constant for it, then emit it as a literal triple in `retype_entities` when `htype_code` is set.

---

### Assistant *(2026-05-07T11:42:05.296Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "DDB_BASE      = \"http://www.deutsche-digitale-bibliothek.de\"",
  "new_string": "DDB_BASE           = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_HIERARCHY_TYPE = DDB_BASE + \"/hierarchyType\""
}
```

---

### User *(2026-05-07T11:42:38.875Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). The user provided the following reason for the rejection:  DDB_BASE is http://www.deutsche-digitale-bibliothek.de/edm/
```

---

### Assistant *(2026-05-07T11:43:03.480Z)*

I'll define the constant directly rather than deriving from `DDB_BASE`:

---

### Assistant *(2026-05-07T11:43:03.481Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "limit": 10,
  "offset": 36
}
```

---

### User *(2026-05-07T11:43:03.491Z)*

**Tool result**
```
36	
37	GEMEA_BASE    = "https://gemea.ise.fiz-karlsruhe.de/mocho/"
38	DDB_ITEM_BASE = "http://www.deutsche-digitale-bibliothek.de/item/"
39	DDB_BASE      = "http://www.deutsche-digitale-bibliothek.de"
40	DDB_API_BASE  = "https://api.deutsche-digitale-bibliothek.de/2/"
41	
42	# ─── Vocab prefixes ───────────────────────────────────────────────────────────
43	
44	_MEDIATYPE_PREFIX = "http://ddb.vocnet.org/medientyp/"
45	_SECTOR_PREFIX    = "http://ddb.vocnet.org/sparte/"
```

---

### Assistant *(2026-05-07T11:43:30.987Z)*

Got it — I'll define it as a standalone literal rather than deriving from `DDB_BASE`. What's the correct IRI? Is it `http://www.deutsche-digitale-bibliothek.de/hierarchyType` (as in `_DDBEDM_PROP` line 294) or `http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType`?

---

### User *(2026-05-07T11:43:41.705Z)*

2nd

---

### Assistant *(2026-05-07T11:43:47.137Z)*

That also means the existing `_DDBEDM_PROP` entry is wrong. I'll fix both together.

---

### Assistant *(2026-05-07T11:43:48.918Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "DDB_BASE      = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_API_BASE  = \"https://api.deutsche-digitale-bibliothek.de/2/\"",
  "new_string": "DDB_BASE           = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_API_BASE       = \"https://api.deutsche-digitale-bibliothek.de/2/\"\nDDB_HIERARCHY_TYPE = \"http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType\""
}
```

---

### User *(2026-05-07T11:44:12.261Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). The user provided the following reason for the rejection:  maybe it should be called ddbedm:hierarchyType?
```

---

### Assistant *(2026-05-07T11:44:27.294Z)*

Yes — if we're adding `http://www.deutsche-digitale-bibliothek.de/edm/` as a namespace, it makes sense to add `ddbedm:` to `_PREFIXES` too (so `_to_curie` produces clean CURIEs in the stats output). Then the constant derives from that base.

---

### Assistant *(2026-05-07T11:44:27.375Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "limit": 30,
  "offset": 107
}
```

---

### User *(2026-05-07T11:44:27.382Z)*

**Tool result**
```
107	
108	# ─── Prefix expansion table ───────────────────────────────────────────────────
109	
110	_PREFIXES = {
111	    "rdam":    "http://rdaregistry.info/Elements/m/",
112	    "rdaw":    "http://rdaregistry.info/Elements/w/",
113	    "rdae":    "http://rdaregistry.info/Elements/e/",
114	    "rdac":    "http://rdaregistry.info/Elements/c/",
115	    "rdact":   "http://rdaregistry.info/termList/RDACarrierType/",
116	    "dc":      "http://purl.org/dc/elements/1.1/",
117	    "dcterms": "http://purl.org/dc/terms/",
118	    "vra":     "http://purl.org/vra/",
119	    "rico":    "http://www.ica.org/standards/RiC/ontology#",
120	    "ric-rst": "http://www.ica.org/standards/RiC/vocabularies/recordSetTypes#",
121	    "skos":    "http://www.w3.org/2004/02/skos/core#",
122	    "owl":     "http://www.w3.org/2002/07/owl#",
123	    "rdfs":    "http://www.w3.org/2000/01/rdf-schema#",
124	    "foaf":    "http://xmlns.com/foaf/0.1/",
125	    "edm":     EDM_NS,
126	    "mo":      "http://purl.org/ontology/mo/",
127	    "aco":     "https://w3id.org/ac-ontology/aco#",
128	    "ec":      "http://www.ebu.ch/metadata/ontologies/ebucoreplus#",
129	    "doco":    "http://purl.org/spar/doco/",
130	    "mocho":   MOCHO_NS,
131	    "gndo":    GNDO_NS,
132	    "ddb":     "http://www.deutsche-digitale-bibliothek.de/",
133	    "ore":     "http://www.openarchives.org/ore/terms/",
134	}
135	
136	# ─── EDM entity type map ──────────────────────────────────────────────────────
```

---

### Assistant *(2026-05-07T11:44:30.105Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "limit": 12,
  "offset": 290
}
```

---

### User *(2026-05-07T11:44:30.108Z)*

**Tool result**
```
290	    "placeOfDeath":            GNDO_NS + "placeOfDeath",
291	    "professionOrOccupation":  GNDO_NS + "professionOrOccupation",
292	    # CIDOC-CRM (LIDO events)
293	    "P11_had_participant": CIDOC_NS + "P11_had_participant",
294	    # DDB-internal structural fields (preserved in ddbedm, skipped in mocho)
295	    "hierarchyType":      "http://www.deutsche-digitale-bibliothek.de/hierarchyType",
296	    "hierarchyPosition":  "http://www.deutsche-digitale-bibliothek.de/hierarchyPosition",
297	    "aggregationEntity":  "http://www.deutsche-digitale-bibliothek.de/aggregationEntity",
298	}
299	
```

---

### Assistant *(2026-05-07T11:44:48.280Z)*

Three changes at once: add `DDBEDM_NS` + `DDB_HIERARCHY_TYPE`, register `ddbedm:` in `_PREFIXES`, and fix the wrong IRI in `_DDBEDM_PROP`.

---

### Assistant *(2026-05-07T11:44:49.593Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "DDB_BASE           = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_API_BASE       = \"https://api.deutsche-digitale-bibliothek.de/2/\"",
  "new_string": "DDB_BASE           = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_API_BASE       = \"https://api.deutsche-digitale-bibliothek.de/2/\"\nDDBEDM_NS          = \"http://www.deutsche-digitale-bibliothek.de/edm/\"\nDDB_HIERARCHY_TYPE = DDBEDM_NS + \"hierarchyType\""
}
```

---

### User *(2026-05-07T11:44:49.596Z)*

**Tool result** *(error)*
```
<tool_use_error>String to replace not found in file.
String: DDB_BASE           = "http://www.deutsche-digitale-bibliothek.de"
DDB_API_BASE       = "https://api.deutsche-digitale-bibliothek.de/2/"</tool_use_error>
```

---

### Assistant *(2026-05-07T11:44:53.765Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "DDB_BASE      = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_API_BASE  = \"https://api.deutsche-digitale-bibliothek.de/2/\"",
  "new_string": "DDB_BASE           = \"http://www.deutsche-digitale-bibliothek.de\"\nDDB_API_BASE       = \"https://api.deutsche-digitale-bibliothek.de/2/\"\nDDBEDM_NS          = \"http://www.deutsche-digitale-bibliothek.de/edm/\"\nDDB_HIERARCHY_TYPE = DDBEDM_NS + \"hierarchyType\""
}
```

---

### User *(2026-05-07T11:45:01.930Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:45:10.868Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "    \"ddb\":     \"http://www.deutsche-digitale-bibliothek.de/\",\n    \"ore\":     \"http://www.openarchives.org/ore/terms/\",",
  "new_string": "    \"ddb\":    \"http://www.deutsche-digitale-bibliothek.de/\",\n    \"ddbedm\": DDBEDM_NS,\n    \"ore\":    \"http://www.openarchives.org/ore/terms/\","
}
```

---

### User *(2026-05-07T11:45:12.492Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:45:16.457Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "    \"hierarchyType\":      \"http://www.deutsche-digitale-bibliothek.de/hierarchyType\",",
  "new_string": "    \"hierarchyType\":      DDBEDM_NS + \"hierarchyType\","
}
```

---

### User *(2026-05-07T11:45:17.696Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:45:22.964Z)*

Now import `DDB_HIERARCHY_TYPE` in `emitters.py` and emit it in `retype_entities`:

---

### Assistant *(2026-05-07T11:45:25.154Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    DCAT_DATASET, XSD_DATETIME,\n    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, EDM_NS,",
  "new_string": "    DCAT_DATASET, XSD_DATETIME,\n    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, DDB_HIERARCHY_TYPE, EDM_NS,"
}
```

---

### User *(2026-05-07T11:45:26.526Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:45:29.836Z)*

Now emit it in `retype_entities` — after all the class triples are resolved, before the return:

---

### Assistant *(2026-05-07T11:45:33.873Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    wemi = _CLASS_WEMI.get(primary_class, \"M\")\n    return lines, primary_class, wemi, {\"htype_used\": htype_used, \"fallback\": is_fallback}",
  "new_string": "    if htype_code:\n        lines.append(make_nq(cho_nt, f\"<{DDB_HIERARCHY_TYPE}>\",\n                             f'\"{_escape_literal(htype_code)}\"', graph_iri))\n\n    wemi = _CLASS_WEMI.get(primary_class, \"M\")\n    return lines, primary_class, wemi, {\"htype_used\": htype_used, \"fallback\": is_fallback}"
}
```

---

### User *(2026-05-07T11:45:35.522Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:45:39.115Z)*

Now add a test and update the existing one that uses `htype_021` to also check for the property:

---

### Assistant *(2026-05-07T11:45:40.169Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.constants import _MOCHO_SKIP",
  "new_string": "from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE"
}
```

---

### User *(2026-05-07T11:45:48.973Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:46:01.695Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "    def test_sparte001_mt003_htype021(self, configs):\n        \"\"\"sparte001/mt003 use_htype=True; htype_021 → rdac:C10001+C10007 from htype, mocho:Manifestation added.\"\"\"\n        lines, target_class, wemi, _flags = self._call(_SPARTE001, _MT003, \"htype_021\", configs)\n        types = _rdf_types(lines)\n        assert \"http://rdaregistry.info/Elements/c/C10001\" in types\n        assert \"https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation\" in types\n        assert wemi == \"W\"",
  "new_string": "    def test_sparte001_mt003_htype021(self, configs):\n        \"\"\"sparte001/mt003 use_htype=True; htype_021 → rdac:C10001+C10007 from htype, mocho:Manifestation added.\"\"\"\n        lines, target_class, wemi, _flags = self._call(_SPARTE001, _MT003, \"htype_021\", configs)\n        types = _rdf_types(lines)\n        assert \"http://rdaregistry.info/Elements/c/C10001\" in types\n        assert \"https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation\" in types\n        assert wemi == \"W\"\n        assert any(DDB_HIERARCHY_TYPE in l and '\"htype_021\"' in l for l in lines)\n\n    def test_htype_emitted_as_literal(self, configs):\n        \"\"\"htype_code is always emitted as ddbedm:hierarchyType literal when set.\"\"\"\n        lines, _, _, _ = self._call(_SPARTE001, _MT003, \"htype_042\", configs)\n        assert any(DDB_HIERARCHY_TYPE in l and '\"htype_042\"' in l for l in lines)\n\n    def test_no_htype_no_hierarchy_type_triple(self, configs):\n        \"\"\"No htype_code → ddbedm:hierarchyType triple must not appear.\"\"\"\n        lines, _, _, _ = self._call(_SPARTE001, _MT003, None, configs)\n        assert not any(DDB_HIERARCHY_TYPE in l for l in lines)"
}
```

---

### User *(2026-05-07T11:52:56.707Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:53:00.565Z)*

**Tool call:** `Bash`
```json
{
  "command": ".venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -15",
  "description": "Run tests",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T11:53:04.347Z)*

**Tool result**
```
ERROR: file or directory not found: scripts/transform/tests/test_transform.py


no tests ran in 0.00s
```

---

### Assistant *(2026-05-07T11:53:06.705Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && .venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -15",
  "description": "Run tests from project root",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T11:53:08.887Z)*

**Tool result**
```
..............................................................           [100%]
62 passed in 0.07s
```

---

### Assistant *(2026-05-07T11:53:13.731Z)*

All 62 tests pass. Summary of changes:

- **`constants.py`**: Added `DDBEDM_NS = "http://www.deutsche-digitale-bibliothek.de/edm/"` and `DDB_HIERARCHY_TYPE = DDBEDM_NS + "hierarchyType"`; registered `ddbedm:` in `_PREFIXES`; corrected the wrong IRI in `_DDBEDM_PROP["hierarchyType"]` from `.../hierarchyType` → `.../edm/hierarchyType`
- **`emitters.py`**: `retype_entities` now appends `<ddbedm:hierarchyType> "htype_XXX"` when `htype_code` is set

---

### User *(2026-05-07T11:53:54.584Z)*

the value should vocnet-htype:ht0xx

---

### Assistant *(2026-05-07T11:54:04.021Z)*

Let me find the vocnet-htype IRI base.

---

### Assistant *(2026-05-07T11:54:05.168Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -r \"vocnet.*htype\\|hierarchie\\|htype\" /Users/mta/Documents/claude/goethe-faust/output/config/ /Users/mta/Documents/claude/goethe-faust/notes/ 2>/dev/null | grep -v \".pyc\" | head -20",
  "description": "Find vocnet htype IRI in configs and notes"
}
```

---

### User *(2026-05-07T11:54:05.299Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_code,label_de,label_en,domain,rdf_type,has_record_set_type,target_vocab,notes
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_001,Abschnitt,Section,library,"doco:Section, rdac:C10007",,doco rdac,
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_002,Anhang,Appendix,library,"doco:Appendix, rdac:C10007",,doco rdac,
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_003,Beigefügtes oder enthaltenes Werk,Contained Work,library,"rdac:C10001, rdac:C10007",,rdac,Contained work; W+M; GND Werk
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_004,Annotation,Annotation,library,rdac:C10007,,rdac,
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_005,Anrede,Address,library,rdac:C10007,,rdac,Dedicatory address or prefatory speech
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_006,Aufsatz,Article,library,"rdac:C10001, rdac:C10007",,rdac,Publication type (journal/serial article); W+M; GND Werk
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_007,Band,Volume,library,"doco:Part, rdac:C10007",,doco rdac,Volume as a Part of a multivolume set
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_008,Beilage,Additional,library,rdac:C10007,,rdac,Supplementary insert
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_009,Einleitung,Introduction,library,"doco:Section, rdac:C10007",,doco rdac,Introduction section
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_010,Eintrag,Entry,library,rdac:C10007,,rdac,Dictionary or encyclopaedia entry
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_011,Faszikel,Fascicle,library,"doco:Part, rdac:C10007",,doco rdac,Fascicle = installment / separately published part
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_012,Fragment,Fragment,library,"doco:TextChunk, rdac:C10007",,doco rdac,Partial text or manuscript fragment
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_013,Handschrift,Manuscript,library,"rdac:C10001, rdac:C10007",,rdac,Publication type (handwritten document); W+M; GND Werk
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_014,Heft,Issue,library,rdac:C10007,,rdac,Periodical issue
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_015,Illustration,Illustration,library,"doco:Figure, rdac:C10007, mocho:ImageWork",,doco rdac mocho,W+M; GND Werk
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_016,Index,Index,library,"doco:Index, rdac:C10007",,doco rdac,
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_017,Inhaltsverzeichnis,Table of Contents,library,"doco:TableOfContents, rdac:C10007",,doco rdac,
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_018,Kapitel,Chapter,library,"doco:Chapter, rdac:C10007",,doco rdac,
/Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv:htype_019,Karte,Map,library,"doco:Figure, rdac:C10007, mocho:ImageWork",,doco rdac mocho,Map; W+M; GND Werk
```

---

### User *(2026-05-07T11:54:06.293Z)*

**Tool result**
```
htype_code,label_de,label_en,domain,rdf_type,has_record_set_type,target_vocab,notes
htype_001,Abschnitt,Section,library,"doco:Section, rdac:C10007",,doco rdac,
htype_002,Anhang,Appendix,library,"doco:Appendix, rdac:C10007",,doco rdac,
htype_003,Beigefügtes oder enthaltenes Werk,Contained Work,library,"rdac:C10001, rdac:C10007",,rdac,Contained work; W+M; GND Werk
htype_004,Annotation,Annotation,library,rdac:C10007,,rdac,
```

---

### Assistant *(2026-05-07T11:54:06.259Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -5 /Users/mta/Documents/claude/goethe-faust/output/config/lookup_htype_doco_rico.csv",
  "description": "Check htype lookup CSV for IRI pattern"
}
```

---

### Assistant *(2026-05-07T11:54:14.001Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"vocnet\\|htype\\|hierarchie\" /Users/mta/Documents/claude/mocho/notes/mocho-gatherer-plan.md | head -20",
  "description": "Check mocho-gatherer-plan for vocnet-htype IRI"
}
```

---

### User *(2026-05-07T11:54:14.047Z)*

**Tool result**
```
10:Both sector and mediatype are resolved by the transform (Mode B — see ADR §7.2). The transform reads `edm.RDF.Concept[].about`, identifies the vocnet IRI, emits two bridge triples on the CHO, and directly asserts the domain class `rdf:type` (D9, per R1). Pattern 1 `SubClassOf` axioms route to the mocho WEMI pivot via pre-materialisation.
15:  → assert <cho> mocho:sector    vocnet-sparte:sparte002
16:  → assert <cho> mocho:mediaType vocnet-mtype:mt003
23:  → assert <cho> mocho:sector    vocnet-sparte:sparte006
24:  → assert <cho> mocho:mediaType vocnet-mtype:mt002
39:Prefix(vocnet-sparte:=<http://ddb.vocnet.org/sparte/>)
40:Prefix(vocnet-mtype:=<http://ddb.vocnet.org/medientyp/>)
50:Declaration(NamedIndividual(vocnet-sparte:sparte001))
51:Declaration(NamedIndividual(vocnet-sparte:sparte002))
52:Declaration(NamedIndividual(vocnet-sparte:sparte005))
53:Declaration(NamedIndividual(vocnet-sparte:sparte006))
54:Declaration(NamedIndividual(vocnet-mtype:mt001))
55:Declaration(NamedIndividual(vocnet-mtype:mt002))
56:Declaration(NamedIndividual(vocnet-mtype:mt005))
76:AnnotationAssertion(rdfs:comment <https://ise-fizkarlsruhe.github.io/ddbkg/mocho#mediatype> "Links a DDB ProvidedCHO to its mediatype (medientyp) skos:Concept. ProvidedCHO.edmType (edm:type) carries one of five uppercase literals (IMAGE, SOUND, TEXT, VIDEO, 3D) — a simple hardcoded lookup resolves these to the vocnet IRI. The transform currently reads from edm.RDF.Concept[].about instead. The mocho:mediaType bridge triple makes the IRI directly queryable on the CHO."@en)
106:| New prefixes (`vocnet-sparte:`, `vocnet-mtype:`, `vocnet-htype:`) | ADD | 3 |
110:| New declarations (2 ObjectProperties + 13 sparte/mt + 7 htype NamedIndividuals) | ADD | 22 |
111:| ClassAssertion + bilingual labels for 7 vocnet-htype individuals | ADD | 21 axioms |
163:Prefix(vocnet-sparte:=<http://ddb.vocnet.org/sparte/>)
164:Prefix(vocnet-mtype:=<http://ddb.vocnet.org/medientyp/>)
```

---

### Assistant *(2026-05-07T11:54:15.184Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -rn \"vocnet.org.*htype\\|vocnet.org.*hierarch\" /Users/mta/Documents/claude/ --include=\"*.md\" --include=\"*.py\" --include=\"*.csv\" 2>/dev/null | grep -v \".venv\" | head -20",
  "description": "Search for vocnet htype IRI across project"
}
```

---

### User *(2026-05-07T11:54:23.985Z)*

**Tool result**
```
<persisted-output>
Output too large (40.6KB). Full output saved to: /Users/mta/.claude/projects/-Users-mta-Documents-claude/ef8b247d-8555-42ed-bcfa-d0e1dab38211/tool-results/b0wrg5pvw.txt

Preview (first 2KB):
/Users/mta/Documents/claude/transcripts/claude-claude-was-forced-quit-how-to-recover-pr-20260420-115640.md:6221:  "old_string": "## The inference chain\n\n```\ndc:subject <http://ddb.vocnet.org/sparte/sparte002>\n  → (ObjectHasValue restriction)\n  → mocho:LibraryCHO\n  → (SubClassOf rda:C10007)\n  → satisfies mocho:Manifestation union\n  → (SubClassOf mocho:Manifestation)\n  → mocho:Manifestation\n```\n\nYou only need the sector/mediatype skos:Concept individual on the `edm:ProvidedCHO` via `dc:subject`; no `dc:type` or `htype` required.",
/Users/mta/Documents/claude/transcripts/claude-claude-was-forced-quit-how-to-recover-pr-20260420-115640.md:6222:  "new_string": "## The inference chain\n\n<!-- INCORRECT — commented out. Sector is on Organization (not directly on CHO via dc:subject).\n```\ndc:subject <http://ddb.vocnet.org/sparte/sparte002>\n  → (ObjectHasValue restriction)\n  → mocho:LibraryCHO\n  → (SubClassOf rda:C10007)\n  → satisfies mocho:Manifestation union\n  → (SubClassOf mocho:Manifestation)\n  → mocho:Manifestation\n```\n\nYou only need the sector/mediatype skos:Concept individual on the `edm:ProvidedCHO` via `dc:subject`; no `dc:type` or `htype` required.\n-->"
/Users/mta/Documents/claude/transcripts/claude-claude-was-forced-quit-how-to-recover-pr-20260420-115640.md:7095:46	Prefix: `vocnet-htype: <http://ddb.vocnet.org/hierarchietyp/>`
/Users/mta/Documents/claude/transcripts/claude-claude-was-forced-quit-how-to-recover-pr-20260420-115640.md:7112:63	@prefix vocnet-htype: <http://ddb.vocnet.org/hierarchietyp/> .
/Users/mta/Documents/claude/transcripts/claude-claude-was-forced-quit-how-to-recover-pr-20260420-115640.md:7667:163-Prefix(vocnet-htype:=<http://ddb.vocnet.org/hierarchietyp/>)
...
</persisted-output>
```

---

### Assistant *(2026-05-07T11:54:33.365Z)*

The IRI base is `http://ddb.vocnet.org/hierarchietyp/`. Now I'll add the constant + prefix entry, then change the emission from a literal to an IRI.

---

### Assistant *(2026-05-07T11:54:35.541Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "_MEDIATYPE_PREFIX = \"http://ddb.vocnet.org/medientyp/\"\n_SECTOR_PREFIX    = \"http://ddb.vocnet.org/sparte/\"",
  "new_string": "_MEDIATYPE_PREFIX = \"http://ddb.vocnet.org/medientyp/\"\n_SECTOR_PREFIX    = \"http://ddb.vocnet.org/sparte/\"\n_HTYPE_PREFIX     = \"http://ddb.vocnet.org/hierarchietyp/\""
}
```

---

### User *(2026-05-07T11:54:43.768Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:54:49.095Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "    \"ddb\":    \"http://www.deutsche-digitale-bibliothek.de/\",\n    \"ddbedm\": DDBEDM_NS,\n    \"ore\":    \"http://www.openarchives.org/ore/terms/\",",
  "new_string": "    \"ddb\":         \"http://www.deutsche-digitale-bibliothek.de/\",\n    \"ddbedm\":      DDBEDM_NS,\n    \"vocnet-htype\": _HTYPE_PREFIX,\n    \"ore\":         \"http://www.openarchives.org/ore/terms/\","
}
```

---

### User *(2026-05-07T11:54:50.183Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:54:52.782Z)*

Now update the import and the emission in `emitters.py`:

---

### Assistant *(2026-05-07T11:54:55.386Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    DCAT_DATASET, XSD_DATETIME,\n    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, DDB_HIERARCHY_TYPE, EDM_NS,",
  "new_string": "    DCAT_DATASET, XSD_DATETIME,\n    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, DDB_HIERARCHY_TYPE, EDM_NS,\n    _HTYPE_PREFIX,"
}
```

---

### User *(2026-05-07T11:57:35.784Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:57:41.822Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    if htype_code:\n        lines.append(make_nq(cho_nt, f\"<{DDB_HIERARCHY_TYPE}>\",\n                             f'\"{_escape_literal(htype_code)}\"', graph_iri))",
  "new_string": "    if htype_code:\n        lines.append(make_nq(cho_nt, f\"<{DDB_HIERARCHY_TYPE}>\",\n                             f\"<{_HTYPE_PREFIX}{htype_code}>\", graph_iri))"
}
```

---

### User *(2026-05-07T11:57:58.772Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:58:02.031Z)*

Update the tests to expect an IRI object instead of a literal:

---

### Assistant *(2026-05-07T11:58:03.427Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE",
  "new_string": "from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX"
}
```

---

### User *(2026-05-07T11:58:04.859Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:58:12.422Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "        assert any(DDB_HIERARCHY_TYPE in l and '\"htype_021\"' in l for l in lines)\n\n    def test_htype_emitted_as_literal(self, configs):\n        \"\"\"htype_code is always emitted as ddbedm:hierarchyType literal when set.\"\"\"\n        lines, _, _, _ = self._call(_SPARTE001, _MT003, \"htype_042\", configs)\n        assert any(DDB_HIERARCHY_TYPE in l and '\"htype_042\"' in l for l in lines)",
  "new_string": "        assert any(DDB_HIERARCHY_TYPE in l and f\"{_HTYPE_PREFIX}htype_021\" in l for l in lines)\n\n    def test_htype_emitted_as_iri(self, configs):\n        \"\"\"htype_code is emitted as a vocnet-htype: IRI object.\"\"\"\n        lines, _, _, _ = self._call(_SPARTE001, _MT003, \"htype_042\", configs)\n        assert any(DDB_HIERARCHY_TYPE in l and f\"{_HTYPE_PREFIX}htype_042\" in l for l in lines)"
}
```

---

### User *(2026-05-07T11:58:13.803Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T11:58:17.398Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && .venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -10",
  "description": "Run tests",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T11:58:19.211Z)*

**Tool result**
```
..............................................................           [100%]
62 passed in 0.07s
```

---

### Assistant *(2026-05-07T11:58:22.517Z)*

All 62 pass. The triple now emits:

```
<gemea-cho> <ddbedm:hierarchyType> <vocnet-htype:htype_021> .
```

with `vocnet-htype:` → `http://ddb.vocnet.org/hierarchietyp/` registered in `_PREFIXES` so stats output uses the short form.

---

### User *(2026-05-07T11:59:43.000Z)*

update transform-props-mapping.md to document handling of hasMet and ddbedm:hierarchyTyp

---

### Assistant *(2026-05-07T11:59:46.368Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping.md"
}
```

---

### User *(2026-05-07T11:59:46.379Z)*

**Tool result** *(error)*
```
File does not exist. Note: your current working directory is /Users/mta/Documents/claude.
```

---

### Assistant *(2026-05-07T11:59:53.415Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/goethe-faust/notes -name \"*props*\" -o -name \"*mapping*\" | head -10",
  "description": "Find props-mapping file"
}
```

---

### User *(2026-05-07T11:59:53.472Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/audio-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/video-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/image-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/entity-property-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/entity-property-mapping-plan.md
```

---

### Assistant *(2026-05-07T11:59:55.473Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md"
}
```

---

### User *(2026-05-07T11:59:55.491Z)*

**Tool result**
```
1	# ADR: EDM → mocho Property Mapping Decisions
2	
3	**Date**: 2026-05-02
4	**Status**: In progress
5	**Related**: `transform-adr.md` (class dispatch), `transform-script-adr.md` (implementation), `transform-props-mapping-plan.md` (full property mapping catalogue)
6	
7	---
8	
9	## Context
10	
11	This document records decisions about **which predicate to emit** for each EDM/DC property in `transform_edm_to_mocho.py`. Class-assignment decisions (rdf:type dispatch, htype lookup, mediatype dispatch) are in `transform-adr.md` and `transform-script-adr.md`. The decisions here govern property-level choices: which RDA/RiC-O/VRA/vocab predicate replaces or accompanies the source DC/EDM predicate, and when the source predicate is kept or skipped.
12	
13	All ProvidedCHOs are typed as `mocho:Manifestation` (D9, `transform-script-adr.md`). Target predicates for Manifestation-level properties use `rdam:` where a Manifestation-specific RDA property exists. For Work-level nodes produced by W+M dispatch, `rdaw:` properties are used.
14	
15	---
16	
17	## Decision 1: Subject keys — IRI correction and value-type dispatch
18	
19	*(Moved from `transform-script-adr.md` D6)*
20	
21	**Decision**: Three JSON keys carry subject data: `dcSubject`, `dcTermsSubject`, `dcTermSubject`. These are handled by a dedicated `emit_subject_triples()` function, not the generic alignment loop.
22	
23	**Background**: Corpus inspection revealed that `dcTermsSubject` was incorrectly mapped to `dc:subject` (`http://purl.org/dc/elements/1.1/subject`) in `alignment_ddbedm_mocho.csv`. The correct IRI is `dcterms:subject` (`http://purl.org/dc/terms/subject`). This was a derivation error in the alignment script's IRI resolution step; `dcTermSubject` (note: missing `s`) was correctly resolved to `dcterms:subject` via an explicit `OVERRIDES` entry in `align_ddbedm_to_mocho.py`. The fix was applied directly to the CSV (42 rows: `edm_prefix` `dc→dcterms`, `edm_iri` corrected).
24	
25	**Dispatch logic**:
26	- Literal value (string or lang-tagged text) → `dc:subject "string"@lang` — uncontrolled annotation; no concept node minted.
27	- IRI value (`{"resource": ..., "$": label}`) → two triples:
28	  1. `<cho> dcterms:subject <concept-uri>`
29	  2. `<concept-uri> rdfs:label "label"@lang` — concept stub (label from `$` field; language from `@language` if present)
30	
31	**Deduplication**: `emit_subject_triples()` collects values from all three keys and deduplicates `(pred_nt, obj_nt)` pairs in a per-record set before writing. This prevents duplicate triples when the same value appears under multiple keys (occurs in ~60% of records). Concept stubs (`rdfs:label`) are also deduplicated per record — one label triple per URI.
32	
33	**Rationale**: The IRI + label stub pattern is strictly better for SPARQL retrieval than a literal-only approach:
34	- URI equality tests are index lookups; string matching is a scan with normalization risk.
35	- One `rdfs:label` triple per concept URI allows cross-record deduplication for faceting: `GROUP BY ?c ?label COUNT(?cho)` without string normalization.
36	- Future enrichment (`skos:broader`, `skos:altLabel`, `owl:sameAs` to GND/LCSH) attaches to the concept node without touching CHO triples.
37	
38	`dc:subject` is kept for literal-only values as a fallback annotation, signalling "unresolved, no authority URI". This keeps literal subjects queryable without mixing literal and IRI objects under `dcterms:subject`.
39	
40	---
41	
42	## Decision 2: Creator → rdam:P30329 "has creator agent of manifestation"
43	
44	*(Moved from `transform-script-adr.md` D7; IRI corrected from P30263 → P30329)*
45	
46	**Decision**: `dc:creator` (json_key: `creator`) is mapped to `rdam:P30329` "has creator agent of manifestation" (`http://rdaregistry.info/Elements/m/P30329`). The alignment table's 464 Work-level candidates are bypassed.
47	
48	**IRI correction**: The earlier decision (D7 in `transform-script-adr.md`) incorrectly cited `rdam:P30263`. The RDA properties CSV (`mocho/output/rda_properties_rda-5.4.9.csv`) confirms `P30263` is "has reduction ratio designation" — unrelated to creator. The correct Manifestation-level generic creator property is `rdam:P30329` "has creator agent of manifestation". This correction must also be applied in `transform_edm_to_mocho.py`.
49	
50	**Background**: The alignment table produces 464 candidates for `creator`, all at the Work WEMI level — including highly specific properties such as "has production company", "has plaintiff corporate body". These are correct sub-properties of Work-level creator properties but wrong for a generic `dc:creator` value where the role is unknown. The WEMI level is determined by D9 (`transform-script-adr.md`): all ProvidedCHOs are `mocho:Manifestation` → creator property must be Manifestation-level.
51	
52	**Typed subproperties** (Phase 1b): `rdam:P30363` (person), `rdam:P30392` (collective agent), `rdam:P30421` (corporate body), `rdam:P30450` (family) are the typed subproperties of `rdam:P30329`. These are the Phase 1b resolution path once GND agent type is resolved by `link_gnd_agents.py`.
53	
54	**Alternatives considered**:
55	- *Emit all 464*: Semantically noisy; a Goethe letter would assert "has plaintiff corporate body" for the author. Rejected.
56	- *Use rdaw:P10065 has creator agent of work*: Work-level; inconsistent with D9. Rejected.
57	- *Mediatype dispatch*: Correct role remains unknown even with mediatype. Rejected for POC.
58	
59	**Open**: D7 does not specify whether a GND URI in `resource` should cause an `edm:Agent` node to be minted and linked, or whether a plain literal is emitted. Phase 1b GND enrichment is the intended resolution path.
60	
61	---
62	
63	## Decision 3: Contributor — LIDO event type dispatch
64	
65	*(Supersedes earlier draft: "keep dc:contributor". Prior rationale: no generic RDA contributor property exists; alignment table candidates were all role-specific or wrong WEMI level.)*
66	
67	**Decision**: The specific predicate emitted for a `dc:contributor` value is determined by the LIDO event type of the `edm:Event` in which the contributor's Agent URI participates. Resolution chain:
68	
69	```
70	ProvidedCHO.hasMet[].resource  →  edm:Event.about
71	edm:Event.hasType.resource     →  LIDO event type URI
72	edm:Event.P11_had_participant[].resource  ==  contributor[].resource
73	→  emit <cho> <target_prop> <contributor.resource>
74	```
75	
76	If no matching Event is found (contributor URI absent from any Event.P11_had_participant, or contributor is label-only), fall back to `dc:contributor`.
77	
78	**Corpus evidence** (`data/items-excerpt-1000.json`, 519 contributor values):
79	- URI match → DDB org / GND: 325 (62.6%) — reliable join key
80	- Label match → DDB org / GND: 174 (33.5%) — lower than creator; label is not a reliable fallback
81	
82	See `notes/corpus-analysis.md §1b` and `data/analysis/contributor_agent_coverage.csv`.
83	
84	**LIDO event type → target predicate dispatch** (`output/config/lido_event_types.csv`):
85	
86	| LIDO event type | label | rdam_prop (M) | rdaw_prop (W) | vra_image | vra_work | rico_prop |
87	|---|---|---|---|---|---|---|
88	| lido00012, eventType/creation | creation | `rdam:P30329` | `rdaw:P10065` | `vra:creator` | `vra:creator` | `rico:hasCreator` |
89	| lido00228, eventType/publication | publication | `rdam:P30083` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `rico:hasPublisher` |
90	| lido00007 | production | `rdam:P30081` | `dc:contributor` | `vra:producer` | `vra:producer` | `dc:contributor` |
91	| lido01127 | photography | `rdam:P30329` | `rdaw:P10056` | `vra:photographer` | `vra:photographer` | `dc:contributor` |
92	| lido00224 | designing | `dc:contributor` | `rdaw:P10051` | `vra:designer` | `vra:designer` | `dc:contributor` |
93	| lido00226 | commissioning | `dc:contributor` | `rdaw:P10287` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
94	| lido00003 | unknown_event | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
95	| all others | — | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
96	
97	For aco, mo, doco, ec, and mocho subclasses: `dc:contributor` in all rows (no role-specific property in those vocabularies).
98	
99	**RDA property notes**:
100	- `rdam:P30329` "has creator agent of manifestation" — used for photography as well as creation: no Manifestation-level photographer property exists in RDA; the photographer is the creator agent of the photographic manifestation.
101	- `rdam:P30081` "has producer agent of unpublished manifestation" — covers fabricated/inscribed artifacts (manuscripts, prints, artworks); no W-level RDA production-agent property exists, hence `dc:contributor` fallback for `rdaw_prop`.
102	- `rdam:P30083` "has publisher agent" — publication is inherently Manifestation-level in RDA; no W-level equivalent, hence `dc:contributor` fallback.
103	- `rdaw:P10051` "has designer agent", `rdaw:P10287` "has commissioning agent" — W-level only; no M-level equivalents, hence `dc:contributor` for `rdam_prop`.
104	- `rdaw:P10056` "has photographer agent of work" — W-level specific property for photography.
105	
106	**Source**: `output/config/lido_event_types.csv`; RDA labels verified from `mocho/output/rda_properties_rda-5.4.9.csv`; VRA properties from `mocho/output/mapping_vra_to_rda.csv`; RiC-O properties from `mocho/output/mapping_rico_to_rda.csv`.
107	
108	---
109	
110	## Decision 4: dc:title — dual-emit with class-specific title predicate
111	
112	**Decision**: For every `dc:title` value, two triples are emitted: `dc:title` (universal cross-WEMI handle) and a class-specific title predicate determined by the target class of the node. The class-specific predicate is looked up from `output/config/lookup_class_prop_alignment.csv` (columns: `edm_class, target_class, wemi, edm_prop, target_prop`). When `target_prop == edm_prop`, only `dc:title` is emitted.
113	
114	**Class-specific predicates for dc:title**:
115	
116	| target_class | wemi | target_prop | Notes |
117	|---|---|---|---|
118	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30134` "has title of manifestation" | rdac classes only |
119	| `rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`, `ec:EditorialWork` | W | `rdaw:P10088` "has title of work" | rdac-derived mocho classes |
120	| `vra:Image`, `vra:Work` | M/W | `vra:title` | VRA Core has its own title property |
121	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadTitle` | RiC-O; WEMI not applicable |
122	| `aco:AudioManifestation`, `mocho:ImageManifestation`, `mo:Musical*`, `ec:MediaResource`, `doco:*` | M | `dc:title` | No vocab-specific title property; dc:title only |
123	
124	**Rationale**: `dc:title` is declared `rdfs:subPropertyOf dct:title` in mocho's RDA→DCT map (`mapRDA2DCT.ttl`), and `rdam:P30134` / `rdaw:P10088` are declared `rdfs:subPropertyOf dct:title` in the same file. QLever has no OWL reasoner, so the entailment is not materialized from subPropertyOf chains — dual-emit at ingest time is the practical approach. `dc:title` serves as the cross-WEMI query handle; the class-specific property serves WEMI-aware consumers.
125	
126	**W+M nodes**: For W+M assignments (e.g. `rdac:C10001` + `rdac:C10007` from sparte002 Library htype dispatch), `dc:title` + `rdaw:P10088` goes on the Work node; `dc:title` + `rdam:P30134` goes on the Manifestation node — both derived from the same source `dc:title` value.
127	
128	**Source**: `output/config/lookup_class_prop_alignment.csv` — currently populated for `dc:title`; extended as other properties are decided.
129	
130	---
131	
132	## Decision 5: Five predicate remappings — DC/EDM → RDA Manifestation-level
133	
134	**Decision**: The following five source predicates are replaced by their Manifestation-level RDA equivalents. Source rationale: `mocho/output/mapping_dct_to_rda.csv` provides the DC → RDA sub-property mapping; Manifestation-level (`rdam:`) properties are selected per D9.
135	
136	| json_key | Source predicate | Target predicate | Label |
137	|---|---|---|---|
138	| `title` | `dc:title` | `rdam:P30134` | "has title of manifestation" |
139	| `description` | `dc:description` | `rdam:P30137` | "has note on manifestation" |
140	| `date` | `dc:date` | `rdam:P30278` | "has date of manifestation" |
141	| `issued` | `dc:issued` | `rdam:P30278` | "has date of manifestation" (same as `date`) |
142	| `isPartOf` | `dcterms:isPartOf` | `rdam:P30020` | "is part of manifestation" |
143	
144	Note: `dc:title` dual-emit is governed by D4. For `description`, `date`, `issued`, `isPartOf` the source predicate is replaced, not dual-emitted — these do not have the cross-WEMI querying motivation that title has.
145	
146	---
147	
148	## Decision 8: dcterms:alternative — class-specific variant title dispatch
149	
150	**Decision**: `dcterms:alternative` is mapped per target class:
151	
152	| target_class | wemi | target_prop |
153	|---|---|---|
154	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30128` "has variant title of manifestation" |
155	| `rdac:C10001` | W | `rdaw:P10086` "has variant title of work" |
156	| all others | — | `dcterms:alternative` (keep as-is) |
157	
158	**Rationale**: `rdam:P30128` is the correct Manifestation-level variant title property; `rdam:P30131` "has abbreviated title" is too narrow — it implies a formally abbreviated form (e.g. acronym), not a generic alternative title. `rdaw:P10086` is the Work-level parallel. No equivalent found in VRA, RiC-O, MO, or ACO; those classes keep the source predicate. RiC-O uses `rico:hasOrHadTitle` for all title types distinguished by `rico:hasTitleType`, but emitting the same predicate for both main title and alternative would conflate them without type context — keeping `dcterms:alternative` is the safer fallback.
159	
160	**Closes open question from D5.**
161	
162	**Source**: `output/config/lookup_class_prop_alignment.csv` (dcterms:alternative rows).
163	
164	---
165	
166	## Decision 9: dc:date and dc:issued — class-specific date predicate dispatch
167	
168	**Decision**: `dc:date` and `dc:issued` are mapped per target class via `output/config/lookup_class_prop_alignment.csv`. The mapping is:
169	
170	| target_class | wemi | dc:date | dc:issued |
171	|---|---|---|---|
172	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30278` "has date of manifestation" | `rdam:P30011` "has date of publication" |
173	| `mocho:ImageManifestation`, `mocho:ImmovableWork`, `mocho:ImageWork` | M/W | `dc:date` | `dc:issued` |
174	| `rdac:C10001` | W | `rdaw:P10219` "has date of work" | N/A |
175	| `aco:AudioManifestation`, `mo:MusicalManifestation`, `mo:MusicalWork` | M/W | `dc:date` | `dc:issued` |
176	| `doco:*`, `ec:MediaResource`, `ec:EditorialWork` | M/W | `dc:date` | `dc:issued` |
177	| `vra:Image` | M | `vra:dateCreated` | `dc:issued` |
178	| `vra:Work` | W | `vra:dateCreated` | N/A |
179	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:creationDate` | `rico:publicationDate` |
180	
181	**N/A** rows are not emitted — no meaningful publication date applies at Work level in RDA or VRA.
182	
183	**Rationale**:
184	- `rdam:P30278` and `rdam:P30011` are the correct Manifestation-level RDA properties. `dc:date` is a generic date; `dc:issued` specifically denotes publication — `rdam:P30011` "has date of publication" captures this distinction.
185	- `rdac:C10001` Work nodes receive `rdaw:P10219` "has date of work" for `dc:date`; `dc:issued` is not applicable at Work level.
186	- VRA classes use `vra:dateCreated` (approximate to `rdaw:P10219`; confirmed in `mapping_vra_to_rda.csv`).
187	- RiC-O classes use `rico:creationDate` / `rico:publicationDate` — native archival date properties with no RDA equivalent (confirmed "no match" in `mapping_rico_to_rda.csv`).
188	- All other classes (aco, mo, doco, ec, mocho subclasses) keep the source predicate — no date property exists in their respective vocabularies.
189	
190	**Closes open question from D5.**
191	
192	**Source**: `output/config/lookup_class_prop_alignment.csv` (dc:date and dc:issued rows).
193	
194	---
195	
196	## Decision 7: Creator URI resolution — emit dcterms:creator when Agent is DDB org or GND
197	
198	**Decision**: When a `ProvidedCHO.creator` value resolves to an `edm:Agent` whose
199	`about` URI is a DDB organization URI (`http://www.deutsche-digitale-bibliothek.de/organization/…`)
200	or a GND URI (`http://d-nb.info/gnd/…`), emit:
201	
202	```turtle
203	<cho> dcterms:creator <agent.about> .
204	```
205	
206	Resolution is attempted in two steps, in priority order:
207	
208	1. **URI match**: `creator[].resource` == `agent[].about` — direct IRI equality.
209	2. **Label match**: `creator[].$` matched against any `agent[].prefLabel[].$` after
210	   comma-order normalization (`"Lastname, Firstname"` ↔ `"Firstname Lastname"`).
211	   Applied only when step 1 fails or `creator[].resource` is absent.
212	
213	If neither step resolves, fall back to the `rdam:P30329` plain-literal path (D2).
214	
215	**Corpus evidence** (`data/items-excerpt-1000.json`, 488 creator values):
216	- URI match → DDB org / GND: 301 (61.7%)
217	- Label match → DDB org / GND (after normalization): 269 (55.1%)
218	
219	See `notes/corpus-analysis.md §1` and `data/analysis/creator_agent_coverage.csv`.
220	
221	**Rationale**: An IRI-valued `dcterms:creator` provides a stable node for GND/VIAF/Wikidata `owl:sameAs` alignment and a target for Phase 1b `rdaa:` property attachment (`link_gnd_agents.py`), without requiring a separate reconciliation step. `dcterms:creator` is used for the IRI triple (agent as entity); `rdam:P30329` is reserved for the Manifestation-scoped plain-literal fallback (D2).
222	
223	**Closes open question from D2.**
224	
225	---
226	
227	## Decision 10: dc:description — class-specific note predicate dispatch
228	
229	**Decision**: `dc:description` is mapped per target class via `output/config/lookup_class_prop_alignment.csv`:
230	
231	| target_class | wemi | target_prop |
232	|---|---|---|
233	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30137` "has note on manifestation" |
234	| `rdac:C10001` | W | `rdaw:P10330` "has note on work" |
235	| `vra:Image`, `vra:Work` | M/W | `vra:description` |
236	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:note` |
237	| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dc:description` |
238	
239	**Rationale**:
240	- `rdam:P30137` is the most generic Manifestation-level note property in `mapping_dct_to_rda.csv`; no narrower property (e.g. `rdaw:P10109` "has summary") is warranted without knowing whether the source value is a summary, a content note, or a scope note.
241	- `rdaw:P10330` is the Work-level parallel for `rdac:C10001` W nodes.
242	- VRA classes use `vra:description` — a free-text description field with no structural RDA equivalent (confirmed "no match" in `mapping_vra_to_rda.csv`).
243	- RiC-O classes use `rico:note` — native archival note property with no RDA equivalent (confirmed "no match" in `mapping_rico_to_rda.csv`).
244	- All other classes (aco, mo, doco, ec, mocho subclasses) have no description property in their respective vocabularies; the source predicate `dc:description` is retained.
245	
246	**Source**: `mapping_dct_to_rda.csv`, `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`.
247	
248	---
249	
250	## Decision 12: dcterms:isPartOf — class-specific part-relation dispatch
251	
252	**Decision**: `dcterms:isPartOf` is mapped per target class via `output/config/lookup_class_prop_alignment.csv`:
253	
254	| target_class | wemi | target_prop |
255	|---|---|---|
256	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30020` "is part of manifestation" |
257	| `rdac:C10001` | W | `rdaw:P10019` "is part of work" |
258	| `vra:Image`, `vra:Work` | M/W | `vra:partOf` |
259	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `dcterms:isPartOf` |
260	| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dcterms:isPartOf` |
261	
262	**Corpus range** (full corpus, 70,311 values, `data/analysis/ispartof_coverage.csv`):
263	
264	| Kind | n | % |
265	|---|---|---|
266	| Full DDB item URL (`http://…/item/<UUID>`) | 43,814 | 62.3% |
267	| Bare 32-char UUID | 22,265 | 31.7% |
268	| Label-only (no resource) | 4,232 | 6.0% |
269	
270	**IRI sanitisation**: bare 32-char UUIDs must be prefixed with `http://www.deutsche-digitale-bibliothek.de/item/` before emitting. Full DDB URLs are used as-is.
271	
272	**Rationale**:
273	- `rdam:P30020` "is part of manifestation" and `rdaw:P10019` "is part of work" are the direct RDA equivalents at M and W level respectively (confirmed in `mapping_dct_to_rda.csv`).
274	- VRA uses `vra:partOf` — maps to `rdaw:P10019` per `mapping_vra_to_rda.csv`; applies to both `vra:Image` and `vra:Work`.
275	- RiC-O: `rico:isOrWasComponentOf` domain is restricted to `rico:Instantiation`, not `rico:RecordResource` — no clean native equivalent for the Record hierarchy. `dcterms:isPartOf` is kept as a valid queryable fallback.
276	- All other classes have no part-relation property in their vocabularies; `dcterms:isPartOf` is kept.
277	- Label-only values carry no resolvable IRI — emitting a literal object for a property whose range is an IRI would violate the graph model; graph/ddbedm passthrough preserves them without loss.
278	
279	**Source**: `mapping_dct_to_rda.csv`, `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `scripts/analyse_ispartof.py`.
280	
281	---
282	
283	## Decision 11: dcterms:language — re-cast LOC URI as rico:Language for RiC-O classes
284	
285	**Decision**: For RiC-O target classes (`rico:RecordSet`, `rico:Record`, `rico:RecordPart`), `dcterms:language` is emitted using `rico:hasOrHadLanguage`. The LOC ISO 639-2 URI (e.g. `http://id.loc.gov/vocabulary/iso639-2/ger`) is additionally typed as `rico:Language` via a stub triple.
286	
287	**Emitted triples** (RiC-O classes only):
288	```turtle
289	<cho>     rico:hasOrHadLanguage <http://id.loc.gov/vocabulary/iso639-2/ger> .
290	<loc-uri> a rico:Language .
291	```
292	
293	For all non-RiC-O classes, `dcterms:language <LOC-URI>` is kept as-is (range `dcterms:LinguisticSystem`).
294	
295	**Rationale**: The LOC ISO 639-2 URIs are authoritative language identifiers. Asserting `rico:Language` on them is a projection into mocho's class space, consistent with how GND URIs are asserted as `mocho:Agent` stubs. The LOC MADS/RDF definition (`madsrdf:Language`) does not prevent additional typing. This enables well-typed `rico:hasOrHadLanguage` triples without minting new URIs.
296	
297	**dc:language** (literal): kept as `dc:language` for all classes including RiC-O. `rico:hasOrHadLanguage` expects a `rico:Language` instance (a URI), not a literal — the literal form has no direct RiC-O equivalent. The literal is retained as a cross-WEMI query handle.
298	
299	**WEMI mismatch note**: Both `dc:language` and `dcterms:language` are Expression-level in RDA (`rdae:P20006` "has language of expression"); no `rdam:` equivalent exists. Language triples are emitted on the Manifestation node as a pragmatic shortcut until Expression nodes are minted. See `transform-future-plan.md §2`.
300	
301	---
302	
303	## Decision 13: edm:Agent — property mapping to mocho:Agent stub
304	
305	**Decision**: All `edm:Agent` nodes are typed as `mocho:Agent` (Phase 0 stub). Properties are mapped per `output/config/lookup_class_prop_alignment.csv` (rows 549–572), generated by `scripts/gen_agent_alignment_rows.py`.
306	
307	**Source namespace note**: DDB uses `gndo:` directly for agent-demographic properties (`gndo:dateOfBirth`, `gndo:dateOfDeath`, `gndo:dateOfEstablishment`, `gndo:dateOfTermination`, `gndo:gender`, `gndo:placeOfBirth`, `gndo:placeOfDeath`, `gndo:professionOrOccupation`, `gndo:biographicalOrHistoricalInformation`). These are passthrough — `edm_prop == target_prop`. The `align_ddbedm_to_mocho.py` script incorrectly resolved these as `edm:` (fallback for properties absent from `ddbedm_1.0.ttl`); the correct namespace is confirmed from `~/Documents/claude/mocho/ontology/gnd_20251218.ttl`.
308	
309	**Non-trivial remappings**:
310	
311	| edm_prop | target_prop | Reason |
312	|---|---|---|
313	| `dc:identifier` | `gndo:gndIdentifier` | GND number literal → GND-native identifier property |
314	| `edm:altLabel` | `skos:altLabel` | `edm:altLabel rdfs:subPropertyOf skos:altLabel`; promote to superclass |
315	| `edm:sameAs` | `owl:sameAs` | EDM declares these equivalent |
316	
317	**Passthrough properties** (no transformation): `gndo:dateOfBirth`, `gndo:dateOfDeath`, `gndo:dateOfEstablishment`, `gndo:dateOfTermination`, `gndo:gender`, `gndo:placeOfBirth`, `gndo:placeOfDeath`, `gndo:professionOrOccupation`, `gndo:biographicalOrHistoricalInformation`, `skos:prefLabel`, `skos:note`, `foaf:name`, `dc:date`, `dc:type`, `dct:hasPart`, `dct:isPartOf`, `edm:begin`, `edm:end`, `edm:hasMet`, `edm:isRelatedTo`, `edm:wasPresentAt`.
318	
319	**Domain mismatches deferred**: `gndo:dateOfEstablishment` / `gndo:dateOfTermination` apply to `gndo:CorporateBody` and `gndo:ConferenceOrEvent`, not `gndo:DifferentiatedPerson`. `edm:begin` / `edm:end` are generic temporals that map to type-specific gndo date properties. Both are emitted as-is under `mocho:Agent` until agent type is resolved. See `transform-future-plan.md §10`.
320	
321	**Source**: `~/Documents/claude/mocho/ontology/gnd_20251218.ttl` (property domain analysis); `output/config/lookup_class_prop_alignment.csv`.
322	
323	---
324	
325	## Decision 6: aggregationEntity and hierarchyPosition — skip, no triple emitted
326	
327	**Decision**: `ddb:aggregationEntity` (boolean string `"true"`/`"false"`) and `ddb:hierarchyPosition` (zero-padded sort key, e.g. `"000000000014848"`) are not emitted as triples.
328	
329	**Rationale**: Both are DDB-internal fields with no mocho/RDA equivalent. `aggregationEntity` is a grouping flag used by the DDB portal UI. `hierarchyPosition` is a sort key for the display hierarchy. Neither carries semantic content useful to downstream graph consumers.
330	
```

---

### Assistant *(2026-05-07T12:00:30.073Z)*

Now I have the full picture. I'll append two decisions at the end: D14 for `hasMet` skip on ProvidedCHO, and D15 for `ddbedm:hierarchyType` emission.

---

### Assistant *(2026-05-07T12:00:31.456Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md",
  "limit": 5,
  "offset": 325
}
```

---

### User *(2026-05-07T12:00:31.466Z)*

**Tool result**
```
325	## Decision 6: aggregationEntity and hierarchyPosition — skip, no triple emitted
326	
327	**Decision**: `ddb:aggregationEntity` (boolean string `"true"`/`"false"`) and `ddb:hierarchyPosition` (zero-padded sort key, e.g. `"000000000014848"`) are not emitted as triples.
328	
329	**Rationale**: Both are DDB-internal fields with no mocho/RDA equivalent. `aggregationEntity` is a grouping flag used by the DDB portal UI. `hierarchyPosition` is a sort key for the display hierarchy. Neither carries semantic content useful to downstream graph consumers.
```

---

### Assistant *(2026-05-07T12:00:52.025Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md",
  "old_string": "**Rationale**: Both are DDB-internal fields with no mocho/RDA equivalent. `aggregationEntity` is a grouping flag used by the DDB portal UI. `hierarchyPosition` is a sort key for the display hierarchy. Neither carries semantic content useful to downstream graph consumers.",
  "new_string": "**Rationale**: Both are DDB-internal fields with no mocho/RDA equivalent. `aggregationEntity` is a grouping flag used by the DDB portal UI. `hierarchyPosition` is a sort key for the display hierarchy. Neither carries semantic content useful to downstream graph consumers.\n\n---\n\n## Decision 14: edm:hasMet on ProvidedCHO — skip in mocho graph, passthrough in ddbedm\n\n**Decision**: The `hasMet` JSON key on `ProvidedCHO` is excluded from the mocho graph via `_MOCHO_SKIP`. It is retained verbatim in the ddbedm passthrough graph as `ddbedm:hasMet` (`http://www.deutsche-digitale-bibliothek.de/edm/hasMet`).\n\n**Background**: `edm:hasMet` on a ProvidedCHO links the object to related events, places, or concepts encountered by the object (or its creator). In the mocho graph there is no RDA/mocho alignment for this relationship at the CHO level. The property also appears in the LIDO contributor resolution chain (D3), where `ProvidedCHO.hasMet[].resource` is used to navigate to the `edm:Event` node — but the `hasMet` triple itself is not emitted on the mocho CHO.\n\n**Note**: `edm:hasMet` on `edm:Agent` stubs is passthrough per D13 — the skip applies only to ProvidedCHO in the mocho graph.\n\n**Implementation**: `\"hasMet\"` added to `_MOCHO_SKIP` in `constants.py`. `emit_ddbedm_triples` continues to emit it unchanged on the ddbedm graph subject.\n\n---\n\n## Decision 15: ddbedm:hierarchyType — emit as vocnet-htype: IRI in mocho graph\n\n**Decision**: When `ProvidedCHO.hierarchyType` is present, `retype_entities()` emits one additional triple in the mocho graph:\n\n```turtle\n<cho> ddbedm:hierarchyType vocnet-htype:htype_021 .\n```\n\nwhere:\n- `ddbedm:hierarchyType` = `http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType`\n- `vocnet-htype:` = `http://ddb.vocnet.org/hierarchietyp/`\n\nThe htype code (e.g. `\"htype_021\"`) is the local name of the vocnet-htype individual. This triple is emitted for every record with a non-empty `hierarchyType` value, regardless of whether the code drove the rdf:type dispatch (i.e. whether `use_htype=True` for the record's sector/mediatype row). The rdf:type dispatch outcome is independent — a record may receive a htype-derived class (layer 1 in `retype_entities`) and still always receive the `ddbedm:hierarchyType` triple.\n\n**Rationale**: The htype code identifies the DDB document hierarchy position type (e.g. volume, chapter, article) and is the primary facet for hierarchical navigation in GeMeA. Emitting it as an IRI (not a literal) enables direct join to the vocnet-htype individuals in QLever without string normalization. The property IRI `ddbedm:hierarchyType` (in the DDB EDM extension namespace) is also used in the ddbedm passthrough graph, ensuring the predicate is consistent across both graphs.\n\n**IRI correction**: The earlier `_DDBEDM_PROP` entry used `http://www.deutsche-digitale-bibliothek.de/hierarchyType` (no `/edm/`). This was corrected to `http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType` as part of this decision. `DDBEDM_NS = \"http://www.deutsche-digitale-bibliothek.de/edm/\"` is defined as a named constant and `ddbedm:` added to `_PREFIXES`.\n\n**Scope**: `hierarchyType` is in `_MOCHO_SKIP` — the generic property loop does not emit it. The triple is emitted exclusively by `retype_entities`. `hierarchyPosition` and `aggregationEntity` remain skipped per D6."
}
```

---

### User *(2026-05-07T12:00:54.752Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md has been updated successfully.
```

---

### Assistant *(2026-05-07T12:01:00.048Z)*

Done. Two decisions added at the end of [transform-props-mapping-adr.md](goethe-faust/notes/transform-props-mapping-adr.md):

- **D14**: `edm:hasMet` on ProvidedCHO — skipped in mocho (via `_MOCHO_SKIP`), passthrough in ddbedm; distinguishes from Agent-level `hasMet` (D13 passthrough) and the D3 navigation use.
- **D15**: `ddbedm:hierarchyType` — always emitted from `retype_entities` as a `vocnet-htype:` IRI; documents the IRI correction, the `DDBEDM_NS` constant, and the separation from class dispatch.

---

### User *(2026-05-07T12:01:55.490Z)*

are all the properties stated in the props-mapping as "deferred" added to the MOCHO skip?

---

### Assistant *(2026-05-07T12:01:59.014Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-plan.md"
}
```

---

### User *(2026-05-07T12:01:59.442Z)*

**Tool result**
```
1	# ProvidedCHO Property Mapping Plan
2	
3	**Date**: 2026-05-01
4	**Status**: In progress
5	**Related**: `transform-adr.md`, `entity-property-mapping-plan.md`, `entity-property-mapping.md`, `output/alignment_ddbedm_mocho.csv`, `references/ddbedm-cho-properties.csv`
6	
7	---
8	
9	## §-1 Insights on GAI
10	
11	When using LLMs to assist with EDM property mapping, the indirect paths from CHO to TimeSpan and Place are a recurring failure point. The pattern is:
12	
13	```
14	CHO → edm:hasMet → Event → edm:occurredAt  → TimeSpan
15	                          → edm:happenedAt → Place
16	```
17	
18	LLMs consistently collapse this to a direct CHO → TimeSpan / CHO → Place link, skipping Event. The root cause is **ambiguous property usage intent**: `edm:occurredAt` (temporal) and `edm:happenedAt` (spatial) are semantically distinct but structurally parallel, and neither name makes the intermediate Event node salient. The LLM infers the connection by property name semantics ("occurred at" → time, "happened at" → place) without attending to the Event node in between.
19	
20	The same failure does not occur for the direct paths (`dc:date`, `dc:issued`, `edm:currentLocation`, `dc:spatial` on CHO directly), because those properties appear inline on the CHO without any intermediate node.
21	
22	A second, related failure: even when the Event node is retained structurally, LLMs miss that it carries **LIDO type** — the event type that distinguishes agent roles (author vs. photographer vs. publisher) and date semantics (creation date vs. publication date). Without LIDO type, all contributors flatten to `dc:contributor` and all dates flatten to `rdam:P30278` "has date of manifestation", losing the typed dispatch that gives the KG its query value.
23	
24	Both failures share a root cause: LLMs attend to property names as semantic clues and skip structural nodes that appear to be mere connectors, even when those nodes carry discriminating attributes.
25	
26	---
27	
28	## §0 Context
29	
30	All ProvidedCHOs are typed as `mocho:Manifestation` (ADR D9). Target predicates must therefore be at the Manifestation WEMI level (`rdam:`) where a Manifestation-level RDA property exists. The alignment CSV (`output/alignment_ddbedm_mocho.csv`) provides candidates for each json_key but fans out across all WEMI levels without selecting one — this plan selects one target per property and documents the rationale.
31	
32	Candidate predicates were drawn from `mocho/output/mapping_dct_to_rda.csv`. For properties with no RDA mapping, the source DC/EDM predicate is retained.
33	
34	For object-range properties (range is a class, not a literal), this plan names the connected class and points to `entity-property-mapping.md` for the properties of that class.
35	
36	`creator` (D7) and `contributor` (D8) are already decided in `transform-adr.md`; their sections below summarise those decisions and add open questions.
37	
38	---
39	
40	## §0.2 Property mapping workflow
41	
42	For each EDM/DC property on a `ProvidedCHO`, the target predicate is resolved in three steps:
43	
44	1. **Look up the RDA equivalent** in `mocho/output/mapping_dct_to_rda.csv` — this gives the RDA property (rdam:, rdaw:, rdae:) that corresponds to the source DC/DCTerms predicate. The WEMI level of the RDA property is constrained by the target class (all ProvidedCHOs are Manifestation-level per D9, so rdam: is preferred where it exists).
45	
46	2. **Look up the vocabulary-specific equivalent** in the parallel mapping files — `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `mapping_mo_to_rda.csv`, `mapping_aco_to_rda.csv` — to find the native property for non-RDA target classes (vra:, rico:, mo:, aco:). Where no match is found, the source DC predicate is kept.
47	
48	3. **Record the decision** in `output/config/lookup_class_prop_alignment.csv` — one row per `(target_class, edm_prop)` pair with the resolved `target_prop`. This table is the runtime dispatch table consumed by `emit_triples()` in `transform_edm_to_mocho.py`.
49	
50	4. **For object-valued properties** (range is a URI): always emit an additional label triple alongside the main predicate triple:
51	
52	   ```
53	   <cho>  <target_prop>  <URI> .
54	   <URI>  rdfs:label     "..."@lang .
55	   ```
56	
57	   The label source depends on the URI type:
58	
59	   | URI type | Label source in source record |
60	   |---|---|
61	   | `edm:Agent` (creator, contributor) | `edm.RDF.Agent[].prefLabel[].$` + `.lang` |
62	   | `edm:Place` (currentLocation, spatial) | `edm.RDF.Place[].prefLabel[].$` + `.lang` |
63	   | `skos:Concept` (dcType URI, dcTermsSubject, hasType) | `edm.RDF.Concept[].prefLabel[].$` + `.lang` |
64	   | vocnet controlled vocab (mocho:mediaType, ddb:hierarchyType) | `lookup_vocnet.csv` `label_en` → `@en`, `label_de` → `@de` |
65	   | `dcterms:LinguisticSystem` (dcTermsLanguage) | LOC ISO 639-2 label — deferred; emit URI only for now |
66	   | parent `edm:ProvidedCHO` (isPartOf) | `dc:title` of parent record if available |
67	
68	   This rule applies to all URI-valued properties throughout the mapping. Where no label is available in the source record, the triple is omitted (no blank label).
69	
70	---
71	
72	## §0.1 Property mapping status
73	
74	| Domain | Property | §  | Status |
75	|---|---|---|---|
76	| `edm:ProvidedCHO` | [about](#1-about) | §1 | ⏭ subject IRI, not a predicate |
77	| `edm:ProvidedCHO` | [title](#2-title) | §2 | ✅ done |
78	| `edm:ProvidedCHO` | [alternative](#3-alternative) | §3 | ✅ done |
79	| `edm:ProvidedCHO` | [creator](#4-creator) | §4 | ✅ done |
80	| `edm:ProvidedCHO` | [contributor](#5-contributor) | §5 | ✅ done |
81	| `edm:ProvidedCHO` | [date](#6-date) | §6 | ✅ done |
82	| `edm:ProvidedCHO` | [issued](#7-issued) | §7 | ✅ done |
83	| `edm:ProvidedCHO` | [description](#8-description) | §8 | ✅ done |
84	| `edm:ProvidedCHO` | [dcSubject](#9-dcsubject) | §9 | ✅ done |
85	| `edm:ProvidedCHO` | [dcTermsSubject / dcTermSubject](#10-dctermssubject--dctermsubject) | §10 | ✅ done |
86	| `edm:ProvidedCHO` | [isPartOf](#11-ispartof) | §11 | ✅ done |
87	| `edm:ProvidedCHO` | [identifier](#12-identifier) | §12 | ✅ done |
88	| `edm:ProvidedCHO` | [language](#13-language) | §13 | ✅ done |
89	| `edm:ProvidedCHO` | [dcTermsLanguage](#14-dctermslanguage) | §14 | ✅ done |
90	| `edm:ProvidedCHO` | [dcType](#15-dctype) | §15 | ✅ done |
91	| `edm:ProvidedCHO` | [spatial](#16-spatial) | §16 | ✅ done |
92	| `edm:ProvidedCHO` | [currentLocation](#17-currentlocation) | §17 | ✅ done |
93	| `edm:ProvidedCHO` | [format](#18-format) | §18 | ✅ done |
94	| `edm:ProvidedCHO` | [extent](#19-extent) | §19 | ✅ done |
95	| `edm:ProvidedCHO` | [edmType](#20-edmtype) | §20 | ✅ done |
96	| `edm:ProvidedCHO` | [aggregationEntity](#21-aggregationentity) | §21 | ✅ done |
97	| `edm:ProvidedCHO` | [hierarchyPosition](#22-hierarchyposition) | §22 | ✅ done |
98	| `edm:ProvidedCHO` | [hierarchyType](#23-hierarchytype) | §23 | ✅ done |
99	| `edm:ProvidedCHO` | [hasType](#24-hastype) | §24 | ⏭ skip — covered by `<cho> mocho:mimetype vocnet-mtype:mtXXX` |
100	| `edm:ProvidedCHO` | [hasMet](#25-hasmet) | §25 | ⏭ skip — EDM event-centric link; `edm:Event` modeling deferred |
101	
102	---
103	
104	## §1 about
105	
106	| Field | Value |
107	|---|---|
108	| EDM IRI | — |
109	| Range | `xsd:anyURI` |
110	| Target | **not a predicate** — subject IRI of the CHO node |
111	
112	The `about` key is the `@subject` of the CHO resource, not a property to be emitted. IRI form: `http://www.deutsche-digitale-bibliothek.de/item/<id>`.
113	
114	---
115	
116	## §2 title
117	
118	| Property | EDM IRI | Target predicates | Notes |
119	|---|---|---|---|
120	| `title` (Manifestation node) | `dc:title` | `dc:title` + `rdam:P30134` "has title of manifestation" | Dual-emit: `dc:title` as cross-WEMI query handle; `rdam:P30134` as WEMI-specific predicate |
121	| `title` (Work node, when W+M) | `dc:title` | `dc:title` + `rdaw:P10088` "has title of work" | Dual-emit on the `rdac:C10001` Work node when htype/dc:type produces a W+M assignment |
122	
123	Range: `rdfs:Literal` (lang-tagged string)
124	
125	`dc:title` is always emitted. When `target_prop != edm_prop`, the class-specific property is dual-emitted alongside it. When `target_prop == edm_prop`, only `dc:title` is emitted (no vocab-specific equivalent exists for that class).
126	
127	**Alignment table**: `output/config/lookup_class_prop_alignment.csv` — columns: `edm_class, target_class, wemi, edm_prop, target_prop`. Populated for `dc:title`; extended as other properties are decided.
128	
129	Notable cases:
130	- `rdac:C10007`, `mocho:Manifestation` → `rdam:P30134` (dual-emit; rdac classes only)
131	- `rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`, `ec:EditorialWork` → `rdaw:P10088` (dual-emit)
132	- `vra:Image`, `vra:Work` → `vra:title` (dual-emit; VRA Core has its own title property)
133	- `rico:Record*` → `rico:hasOrHadTitle` (dual-emit; RiC-O; WEMI not applicable)
134	- `aco:AudioManifestation`, `mocho:ImageManifestation`, `mo:Musical*`, `ec:MediaResource`, `doco:*`, `frbr:Manifestation` → `dc:title` only (no vocab-specific title property)
135	
136	---
137	
138	## §3 alternative
139	
140	| Property | EDM IRI | Target predicate | Notes |
141	|---|---|---|---|
142	| Property | EDM IRI | Target predicate | Notes |
143	|---|---|---|---|
144	| `alternative` (M classes) | `dcterms:alternative` | `rdam:P30128` "has variant title of manifestation" | `rdac:C10007`, `mocho:Manifestation` |
145	| `alternative` (W classes) | `dcterms:alternative` | `rdaw:P10086` "has variant title of work" | `rdac:C10001` |
146	
147	Range: `rdfs:Literal` (lang-tagged string)
148	
149	No equivalent found in VRA, RiC-O, MO, or ACO (`mapping_*_to_rda.csv`). RiC-O and all other non-RDA classes keep `dcterms:alternative` as-is.
150	
151	---
152	
153	## §4 creator
154	
155	Range: `edm:Agent` (may carry GND URI in `resource` + role-annotated literal in `$`)
156	
157	**Connected class**: `edm:Agent` → `rdaa:` properties (`prefLabel`, `altLabel`, `dateOfBirth`, `sameAs`, …). See `entity-property-mapping.md §1`.
158	
159	Two independent dispatch tracks run for every `creator` value:
160	
161	**Track 1 — class dispatch** (always runs): predicate is determined by the CHO's target class, looked up from `output/config/lookup_class_prop_alignment.csv` (creator rows to be populated). The `dc:creator` source predicate is the `edm_prop` key; the table provides `target_prop` per class.
162	
163	**Track 2 — Agent URI resolution** (conditional): If the creator label matches an `edm:Agent` in the record whose `about` is a DDB organization URI (`http://www.deutsche-digitale-bibliothek.de/organization/…`) or GND URI (`http://d-nb.info/gnd/…`), emit:
164	
165	```turtle
166	<cho> dcterms:creator <agent.about> .
167	```
168	
169	If no matching Agent URI is found, do nothing (no literal fallback). See `transform-props-mapping-adr.md D7`.
170	
171	**Agent node** (when URI resolves): also emit a stub node for the agent:
172	
173	```turtle
174	<agent.about> a mocho:Agent ;
175	              rdfs:label "Lastname, Firstname" .
176	```
177	
178	Label sourced from `edm:Agent.prefLabel[].$` (first value). Applies to both creator and contributor URI resolutions.
179	
180	### §2.1 RDA creator properties
181	
182	Generic properties only; typed subproperties (by agent type) are deferred — see `transform-future-plan.md §1`.
183	
184	| WEMI | Property | label_full |
185	|---|---|---|
186	| M | `rdam:P30329` | "has creator agent of manifestation" |
187	| W | `rdaw:P10065` | "has creator agent of work" |
188	| E | `rdae:P20053` | "has creator agent of expression" |
189	
190	---
191	
192	## §5 contributor
193	
194	Range: `edm:Agent` (most values are literals with role annotation in parentheses; ~62.6% carry a URI resolvable to DDB org or GND)
195	
196	**Connected class**: `edm:Agent` (when URI present). See `entity-property-mapping.md §1`.
197	
198	The target predicate depends on the LIDO event type of the `edm:Event` in which the contributor participates:
199	
200	```
201	ProvidedCHO.hasMet[].resource  →  edm:Event.about
202	edm:Event.hasType.resource     →  LIDO event type URI
203	edm:Event.P11_had_participant[].resource  ==  contributor[].resource
204	→  emit <cho> <target_prop> <contributor.resource>
205	```
206	
207	Fallback when no matching Event is found (URI absent or label-only): `dc:contributor`.
208	
209	**LIDO event type → target predicate** (from `output/config/lido_event_types.csv`):
210	
211	| LIDO event type | rdam: (M) | rdaw: (W) | vra:Image | vra:Work | rico: |
212	|---|---|---|---|---|---|
213	| lido00012 creation | `rdam:P30329` | `rdaw:P10065` | `vra:creator` | `vra:creator` | `rico:hasCreator` |
214	| lido00228 publication | `rdam:P30083` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `rico:hasPublisher` |
215	| lido00007 production | `rdam:P30081` | `dc:contributor` | `vra:producer` | `vra:producer` | `dc:contributor` |
216	| lido01127 photography | `rdam:P30329` | `rdaw:P10056` | `vra:photographer` | `vra:photographer` | `dc:contributor` |
217	| lido00224 designing | `dc:contributor` | `rdaw:P10051` | `vra:designer` | `vra:designer` | `dc:contributor` |
218	| lido00226 commissioning | `dc:contributor` | `rdaw:P10287` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
219	| all others | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
220	
221	For `aco:`, `mo:`, `doco:`, `ec:`, `mocho:` subclasses: `dc:contributor` in all rows.
222	
223	**Agent node** (when contributor URI resolves): same stub as creator — see §4:
224	
225	```turtle
226	<contributor.resource> a mocho:Agent ;
227	                       rdfs:label "Lastname, Firstname" .
228	```
229	
230	See `transform-props-mapping-adr.md D3`.
231	
232	---
233	
234	## §6 date
235	
236	| Property | EDM IRI | Target predicate | Notes |
237	|---|---|---|---|
238	| `date` | `dc:date` | `rdam:P30278` "has date of manifestation" | Manifestation-level from `mapping_dct_to_rda.csv`; format varies: `"2018 (role)"`, `"18300213"` |
239	| `created` | `dc:created` | — (lookup only) | Work-level creation date; not emitted as a mocho triple; written to GND Werk lookup table (see `transform-revised-plan.md §1.2`) |
240	
241	Range: `rdfs:Literal`
242	
243	**Normalization** (corpus analysis `notes/corpus-analysis.md §2`):
244	
245	- **Compact date YYYYMMDD → ISO 8601** (now): `"18300213"` → `"1830-02-13"`. Decided in `transform-script-adr.md`.
246	- **Range split** (now): ISO interval `"begin/end"` split on `/`; emit two `rdam:P30278` triples. `"1915-01-01/1920-12-31"` → `rdam:P30278 "1915-01-01"` + `rdam:P30278 "1920-12-31"` (16.7% of records). Decided in `transform-script-adr.md`.
247	- **Role annotation** (future): `"2018 (Fotografische Aufnahme)"` — do not strip; consider linking role string to other fields (e.g. `edm:Event.hasType`). Deferred.
248	
249	---
250	
251	## §7 issued
252	
253	| Property | EDM IRI | Target predicate | Notes |
254	|---|---|---|---|
255	| `issued` | `dc:issued` | `rdam:P30278` "has date of manifestation" | Non-standard DC term; publication year collapses to same predicate as `date` (§6) |
256	
257	Range: `rdfs:Literal` (lang-tagged literal year string)
258	
259	**Deferred**: `dc:issued` maps to `rdam:P30278` for now. The correct resolution is LIDO event type dispatch via `CHO → edm:hasMet → Event → edm:occurredAt → TimeSpan` — the event type (e.g. lido00228 publication) would select `rdam:P30011` "has date of publication" over `rdam:P30278`. This is the same deferred path as `transform-revised-plan.md §3.2` item 3 and §5.2; `dc:issued` is a stopgap until that traversal is implemented.
260	
261	---
262	
263	## §25 hasMet
264	
265	| Property | EDM IRI | Target predicate | Notes |
266	|---|---|---|---|
267	| `hasMet` | `edm:hasMet` | keep `edm:hasMet` | No mocho/RDA equivalent; EDM structural link |
268	
269	Range: `edm:Event`
270	
271	**Connected class**: `edm:Event` — all four Event properties (`hasType`, `happenedAt`, `occuredAt`, `P11_had_participant`) are deferred pending CRM import. See `entity-property-mapping.md §8`.
272	
273	---
274	
275	## §12 identifier
276	
277	Range: `rdfs:Literal` (string or array; values often include role annotation in parentheses, e.g. `"GSA 28/752"`, `"urn:nbn:…"`, `"http://d-nb.info/…"`)
278	
279	**Step 1 (RDA)**: No entry for `dc:identifier` in `mapping_dct_to_rda.csv`. Closest RDA property is `rdam:P30004` "has identifier for manifestation" — not imported into mocho; deferred (see `transform-future-plan.md`).
280	
281	**Step 2 (vocab-specific)**: RiC-O has `rico:hasOrHadIdentifier` (domain: `rico:Thing`, range: `rico:Identifier`). No identifier property in `mapping_vra_to_rda.csv`, `mapping_mo_to_rda.csv`, or ACO.
282	
283	**Step 3 (lookup table)**: All non-RiC-O classes → `dc:identifier`; RiC-O classes → `rico:hasOrHadIdentifier`.
284	
285	| target_class | wemi | target_prop | Notes |
286	|---|---|---|---|
287	| `rdac:C10007`, `mocho:Manifestation` | M | `dc:identifier` | No RDA mapping available |
288	| `rdac:C10001` | W | `dc:identifier` | No RDA mapping available |
289	| all non-RDA M/W classes | M/W | `dc:identifier` | Source predicate kept |
290	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadIdentifier` | Native RiC-O identifier property |
291	
292	**Step 4**: `dc:identifier` values are literals — no agent stub applies.
293	
294	---
295	
296	## §24 hasType
297	
298	| Property | EDM IRI | Target predicate | Notes |
299	|---|---|---|---|
300	| `hasType` | `edm:hasType` | keep `edm:hasType` | No mocho/RDA equivalent |
301	
302	Range: `skos:Concept` (resource refs — DDB internal IDs or GND/LIDO concept URIs)
303	
304	**Connected class**: `skos:Concept` → `skos:prefLabel`, `skos:notation`. See `entity-property-mapping.md §7`.
305	
306	---
307	
308	## §23 hierarchyType
309	
310	Range: `rdfs:Literal` controlled codes (e.g. `htype_030`, `htype_034`). Resolved against `lookup_vocnet.csv` (category `hierarchyType`) to a vocnet IRI.
311	
312	**Step 1–2**: No RDA, VRA, MO, or ACO equivalent. `ddb:hierarchyType` source namespace preserved. `retype_entities()` also consumes this value to produce `rdf:type` triples (ADR D3) — the triple below is emitted in addition, not instead.
313	
314	**Step 3 (lookup table)**: All classes → `ddb:hierarchyType`.
315	
316	**Step 4**: URI-valued; vocnet IRI is the object. Re-emitted as `<cho> ddb:hierarchyType <http://ddb.vocnet.org/hierarchietyp/htXXX>` in the mocho subgraph.
317	
318	---
319	
320	## §15 dcType
321	
322	Range: mixed — `rdfs:Literal` (72.4% label-only) or URI (27.6%: GND 55.9%, Getty AAT 32.2%, Wikidata 11.9%). See `corpus-analysis.md §2`.
323	
324	Value-type dispatch runs before class dispatch, mirroring the `dc:subject` / `dcterms:subject` split:
325	- **Literal** (no `resource`): emit `<cho> dc:type "label"@lang` — all classes
326	- **URI** (`resource` present): emit `<cho> dcterms:type <uri>` + class-specific predicate (dual-emit for RDA/VRA classes) + Concept stub
327	
328	**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdam:P30335` "has category of manifestation" (M) and `rdaw:P10004` "has category of work" (W). Both expect controlled vocabulary objects — URI path only.
329	
330	**Step 2 (vocab-specific)**: RiC-O → `rico:hasOrHadType` (domain: `rico:Thing`, range: `rico:Type`) for URI path; `rico:type` (range: `rdfs:Literal`) for literal path. VRA Core 4 → `vra:worktype` (native property; not yet in `mapping_vra_to_rda.csv` — see `mocho/notes/mocho-gatherer-plan.md §Pending`). MO and ACO have no native type property in their mapping files.
331	
332	**Step 3 (lookup table)** — URI path (when `dcType.resource` present):
333	
334	| target_class | wemi | target_prop | Notes |
335	|---|---|---|---|
336	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30335` | dual-emit: also `dcterms:type <uri>` |
337	| `rdac:C10001` | W | `rdaw:P10004` | dual-emit: also `dcterms:type <uri>` |
338	| `vra:Image` | M | `vra:worktype` | dual-emit: also `dcterms:type <uri>` |
339	| `vra:Work` | W | `vra:worktype` | dual-emit: also `dcterms:type <uri>` |
340	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadType` | `<uri> a rico:Type` stub; no `dcterms:type` |
341	| all others (mo:, aco:, doco:, ec:, mocho:Image*, mocho:Immovable*) | M/W | `dcterms:type` | no class-specific predicate |
342	
343	Literal path: all classes → `dc:type`.
344	
345	**Step 4 (Concept stub)**: When `dcType.resource` is present, also emit a concept stub sourced from the in-record `Concept[]` node (URI match 99.9% for GND; see `corpus-analysis.md §2.2`):
346	- Non-RiC-O: `<concept-uri> a skos:Concept ; skos:prefLabel "..."@lang`
347	- RiC-O: `<concept-uri> a rico:Type` (same re-cast pattern as ADR D11)
348	
349	---
350	
351	## §8 description
352	
353	Range: `rdfs:Literal` (lang-tagged string)
354	
355	Class-specific dispatch via `output/config/lookup_class_prop_alignment.csv`:
356	
357	| target_class | wemi | target_prop | Notes |
358	|---|---|---|---|
359	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30137` "has note on manifestation" | RDA Manifestation-level generic note |
360	| `rdac:C10001` | W | `rdaw:P10330` "has note on work" | RDA Work-level generic note |
361	| `vra:Image`, `vra:Work` | M/W | `vra:description` | VRA Core has its own free-text description property; no RDA match in `mapping_vra_to_rda.csv` |
362	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:note` | Native archival note property; no RDA match in `mapping_rico_to_rda.csv` |
363	| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dc:description` | No vocab-specific description property; source predicate kept |
364	
365	Source: `mapping_dct_to_rda.csv` for RDA candidates; `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv` for vocab equivalents.
366	
367	---
368	
369	## §21 aggregationEntity
370	
371	Range: `rdfs:Literal` (`"true"` / `"false"`). DDB-internal grouping flag indicating whether the record is an aggregation container rather than a leaf item.
372	
373	**Step 1–2**: No RDA, VRA, RiC-O, MO, or ACO equivalent. Source namespace `ddb:` preserved.
374	
375	**Step 3 (lookup table)**: All classes → `ddb:aggregationEntity`.
376	
377	**Step 4**: Literal-valued; no stub. Re-emitted as `<cho> ddb:aggregationEntity "true"/"false"` in the mocho subgraph.
378	
379	---
380	
381	## §19 extent
382	
383	Range: `rdfs:Literal` (lang-tagged; physical dimensions or pagination, e.g. `"V, 244 S."`, `"8,5 x 12 x 2,2 cm"`). 95,808 values; 47.6% pagination, 29.1% dimensions, 23.2% other (see `corpus-analysis.md §4`).
384	
385	**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `dcterms:extent` → `rdam:P30182` "has extent of manifestation" (M-level). Values are free-text literals — not normalised to RDA-controlled extent vocabulary. WEMI mismatch is absent (M-level exists), but structured parse is required before dispatch → keep `dc:extent`.
386	
387	**Step 2 (vocab-specific)**: VRA Core 4 → `vra:measurementsSet` (structured typed measurement — height/width/depth with unit fields); no plain-literal form available. RiC-O → `rico:hasExtent` (expects `rico:Extent` instance, not a literal). MO/ACO → no extent property. All require structured values → keep `dc:extent` for all classes.
388	
389	**Step 3 (lookup table)**: All classes → `dc:extent`. See `transform-future-plan.md §8` for deferred structured-parse dispatch.
390	
391	**Step 4**: Literal-valued; no stub.
392	
393	---
394	
395	## §20 edmType
396	
397	Range: uppercase controlled string (`IMAGE`, `TEXT`, `SOUND`, `VIDEO`, `3D`). Resolved against `lookup_vocnet.csv` (category `mediaType`) to a vocnet IRI.
398	
399	**Step 1–2**: No RDA, VRA, RiC-O, MO, or ACO equivalent. `mocho:mediaType` is the mocho-native property (ObjectProperty, domain `edm:ProvidedCHO`, range `skos:Concept`; defined in `mocho-edit.owl`). The mediatype dispatch also consumes this value to produce `rdf:type` triples (ADR D11/D12) — the triple below is emitted in addition.
400	
401	**Step 3 (lookup table)**: All classes → `mocho:mediaType`.
402	
403	**Step 4**: URI-valued; vocnet IRI is the object. Emitted as `<cho> mocho:mediaType <http://ddb.vocnet.org/medientyp/mtXXX>` in the mocho subgraph.
404	
405	---
406	
407	## §13 language
408	
409	Range: `rdfs:Literal` (ISO 639-2 string, e.g. `"ger"`). Always co-occurs with `dcterms:language` (§14) — 62.1% of records have both, 37.9% have neither. `dc:language` carries the primary language only; `dcterms:language` is multi-valued (see `corpus-analysis.md §2`).
410	
411	**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdae:P20006` "has language of expression" (E-level); `rdaw:P10353` "has language of representative expression" (W-level). No `rdam:` equivalent. WEMI mismatch for M-level nodes → keep `dc:language`.
412	
413	**Step 2 (vocab-specific)**: VRA and MO have no language property. RiC-O has `rico:hasOrHadLanguage`, but its range is `rico:Language` (a URI-valued class), not a literal — `dc:language` is a plain ISO code string. No viable RiC-O mapping for the literal form → keep `dc:language` for all classes.
414	
415	**Step 3 (lookup table)**: All classes → `dc:language`.
416	
417	**Step 4**: Literal-valued; no stub.
418	
419	---
420	
421	## §14 dcTermsLanguage
422	
423	Range: `dcterms:LinguisticSystem` (resource URI, e.g. `http://id.loc.gov/vocabulary/iso639-2/ger`). Same WEMI mismatch as §13 (see ADR D11).
424	
425	**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdae:P20006` "has language of expression" (E-level); no `rdam:` equivalent. WEMI mismatch for M-level nodes → keep `dcterms:language`.
426	
427	**Step 2 (vocab-specific)**: RiC-O has `rico:hasOrHadLanguage` (domain: `rico:Record*`, range: `rico:Language`). The LOC URI is re-cast as `rico:Language` per ADR D11. All other vocabularies have no language property → keep `dcterms:language`.
428	
429	**Step 3 (lookup table)**:
430	
431	| target_class | wemi | target_prop | Notes |
432	|---|---|---|---|
433	| `rdac:C10007`, `mocho:Manifestation`, all M non-RDA | M | `dcterms:language` | No rdam: equivalent; kept as-is |
434	| `rdac:C10001`, all W non-RDA | W | `dcterms:language` | WEMI mismatch; kept as-is |
435	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadLanguage` | LOC URI re-typed as `rico:Language` (ADR D11) |
436	
437	**Step 4 (URI stub)**: For RiC-O classes, also emit `<LOC-URI> a rico:Language`. This is distinct from agent stubs — no `rdfs:label` is added (authority label resides at the LOC endpoint). See ADR D11.
438	
439	---
440	
441	## §9 dcSubject
442	
443	| Property | EDM IRI | Target predicate | Notes |
444	|---|---|---|---|
445	| `dcSubject` | `dc:subject` | via `emit_subject_triples()` (ADR D1) | Literal → `dc:subject`; IRI → promoted to `dcterms:subject` path |
446	
447	Range: `rdfs:Literal` (literal-primary; some records carry GND URI in `resource` field)
448	
449	Subject describes intellectual content — a Work-level concern. **`dc:subject` is only emitted for Work-level target classes** (`rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`). Manifestation-level classes receive `N/A` in `lookup_class_prop_alignment.csv` — no triple emitted. Domain-specific Work classes (`vra:Work`, `mo:MusicalWork`, `ec:EditorialWork`, `rico:*`) are `TBD`.
450	
451	See `transform-props-mapping-adr.md D1` for full dispatch and deduplication logic.
452	
453	---
454	
455	## §10 dcTermsSubject / dcTermSubject
456	
457	| Property | EDM IRI | Target predicate | Notes |
458	|---|---|---|---|
459	| `dcTermsSubject` / `dcTermSubject` | `dcterms:subject` | `rdaw:P10256` "has subject" (Work-level only) | Two keys, same predicate (D1); dedup by `(pred_nt, obj_nt)` per record |
460	
461	Range: `skos:Concept` (resource refs — DDB internal IDs or GND URIs)
462	
463	No Manifestation-level "has subject" exists in RDA — subject relationships describe intellectual content, not physical carrier. `rdaw:P10256` (Work-level) is therefore only emitted for Work-level target classes (`rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`). All Manifestation-level classes receive `N/A` in `lookup_class_prop_alignment.csv`. Domain-specific Work classes (`vra:Work`, `mo:MusicalWork`, `ec:EditorialWork`, `rico:*`) are `TBD`.
464	
465	**Connected class**: `skos:Concept` → `skos:prefLabel`, `skos:notation`. See `entity-property-mapping.md §7`.
466	
467	---
468	
469	## §11 isPartOf
470	
471	**Step 1 (RDA)**: `mapping_dct_to_rda.csv` → `rdam:P30020` "is part of manifestation" (M), `rdaw:P10019` "is part of work" (W).
472	
473	**Step 2 (vocab-specific)**: `vra:partOf` for VRA classes (per `mapping_vra_to_rda.csv`). No equivalent in RiC-O, MO, ACO.
474	
475	**Step 3**: Class dispatch via `output/config/lookup_class_prop_alignment.csv`:
476	
477	| target_class | wemi | target_prop | Notes |
478	|---|---|---|---|
479	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30020` "is part of manifestation" | |
480	| `rdac:C10001` | W | `rdaw:P10019` "is part of work" | |
481	| `vra:Image`, `vra:Work` | M/W | `vra:partOf` | |
482	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `dcterms:isPartOf` | `rico:isOrWasComponentOf` domain restricted to `rico:Instantiation` |
483	| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dcterms:isPartOf` | |
484	
485	**Step 4**: Object-valued (IRI). IRI sanitisation required before emit — see corpus finding.
486	
487	**Corpus finding** (`data/analysis/ispartof_coverage.csv`, 70,311 values across 67,539 records):
488	
489	| Kind | n | % |
490	|---|---|---|
491	| Full DDB item URL (`http://…/item/<UUID>`) | 43,814 | 62.3% |
492	| Bare 32-char UUID | 22,265 | 31.7% |
493	| Label-only (no resource) | 4,232 | 6.0% |
494	
495	**IRI sanitisation**: bare 32-char UUIDs must be prefixed with `http://www.deutsche-digitale-bibliothek.de/item/` before emitting. Full DDB URLs are used as-is. Label-only values have no resource to emit.
496	
497	**Connected class**: parent `ProvidedCHO` → same class dispatch applies recursively.
498	
499	---
500	
501	## §22 hierarchyPosition
502	
503	Range: `rdfs:Literal` (zero-padded numeric string, e.g. `"000000000014848"`). DDB-internal sort key encoding the record's position within its hierarchy tree.
504	
505	**Step 1–2**: No RDA, VRA, RiC-O, MO, or ACO equivalent. Source namespace `ddb:` preserved.
506	
507	**Step 3 (lookup table)**: All classes → `ddb:hierarchyPosition`.
508	
509	**Step 4**: Literal-valued; no stub. Re-emitted as `<cho> ddb:hierarchyPosition "000000000014848"` in the mocho subgraph.
510	
511	---
512	
513	## §17 currentLocation
514	
515	Range: `edm:Place` (resource URI — DDB internal Place ID or GND place URI).
516	
517	**Step 1 (RDA)**: `edm:currentLocation` is an EDM property, not in `mapping_dct_to_rda.csv`. No RDA equivalent.
518	
519	**Step 2 (vocab-specific)**: Not in `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `mapping_mo_to_rda.csv`, or `mapping_aco_to_rda.csv`. No vocab-specific equivalent.
520	
521	**Step 3**: All classes → keep `edm:currentLocation`.
522	
523	**Step 4 (Place stub)**: Re-emit the matching `edm.RDF.Place[]` node in the mocho subgraph — sourced from `Place[].about == currentLocation.resource`. Emit all available properties: `geo:lat`, `geo:long`, `geo:alt`, `skos:prefLabel`, `skos:altLabel`, `owl:sameAs`. See `entity-property-mapping.md §3`.
524	
525	---
526	
527	## §18 format
528	
529	Range: `rdfs:Literal` (lang-tagged free-text; technique/medium descriptions, e.g. "Kohlezeichnung (?) (Technik)", "Negativ in color, quer").
530	
531	**Step 1 (RDA)**: `mapping_dct_to_rda.csv` maps `dc:format` to carrier/media/material properties (`rdam:P30001` "has carrier type", `rdam:P30002` "has media type", `rdam:P30208` "has base material of manifestation", and 50+ others). **All expect controlled vocabulary objects** — none are applicable to free-text strings. No clean RDA mapping.
532	
533	**Step 2 (vocab-specific)**: `vra:material` → `rdam:P30208` (VRA mapping file). No equivalent in RiC-O, MO, or ACO mapping files. **All vocab-specific candidates also expect controlled vocabulary or structured values.**
534	
535	**Step 3**: All classes → keep `dc:format`.
536	
537	**Step 4**: Literal-valued; no stub.
538	
539	KB linking and controlled-vocab dispatch deferred. See `transform-future-plan.md §7`.
540	
541	---
542	
543	## §16 spatial
544	
545	**Step 1 (RDA)**: `dc:spatial` not in `mapping_dct_to_rda.csv`. No RDA equivalent.
546	
547	**Step 2 (vocab-specific)**: Not in `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `mapping_mo_to_rda.csv`, or `mapping_aco_to_rda.csv`. No vocab-specific equivalent.
548	
549	**Step 3**: All classes → keep `dc:spatial`.
550	
551	**Step 4**: Object-valued (URI). Range is `edm:Place` — use resource URI directly as object: `<cho> dc:spatial <URI>`. No agent stub. 99.5% of spatial resource URIs equal the record's `Event.happenedAt` URIs — no event traversal needed (see `data/analysis/spatial_event_overlap.csv`).
552	
553	---
554	
555	## Summary: transform actions
556	
557	| json_key | Current predicate | Change to | Status |
558	|---|---|---|---|
559	| `title` (Manifestation) | `dc:title` | `dc:title` + `rdam:P30134` | ☐ update |
560	| `title` (Work, W+M nodes) | `dc:title` | `dc:title` + `rdaw:P10088` | ☐ update |
561	| `description` | `dc:description` | `rdam:P30137` | ☐ update |
562	| `date` | `dc:date` | `rdam:P30278` | ☐ update |
563	| `issued` | `dc:issued` | `rdam:P30278` | ☐ update |
564	| `isPartOf` | `dcterms:isPartOf` | `rdam:P30020` | ☐ update |
565	| `alternative` (M) | `dcterms:alternative` | `rdam:P30128` | ✅ props-mapping D8 |
566	| `alternative` (W) | `dcterms:alternative` | `rdaw:P10086` | ✅ props-mapping D8 |
567	| `hierarchyType` | `ddb:hierarchyType` | no triple (dispatch) | ✅ implemented (D3) |
568	| `edmType` | `edm:type` | no triple (dispatch) | ✅ implemented (D11/D12) |
569	| `aggregationEntity` | `ddb:aggregationEntity` | skip | ☐ add skip |
570	| `hierarchyPosition` | `ddb:hierarchyPosition` | skip | ☐ add skip |
571	| `creator` (Agent resolved) | `dc:creator` | `dcterms:creator <URI>` | ✅ props-mapping D7 |
572	| `creator` (fallback literal) | `dc:creator` | `rdam:P30329` | ✅ D2 (IRI corrected from P30263) |
573	| `contributor` | `dc:contributor` | keep as-is | ✅ D8 |
574	| all others | — | keep as-is | ✅ no change |
575	
576	---
577	
578	## Files to update
579	
580	| File | Action |
581	|---|---|
582	| `scripts/transform_edm_to_mocho.py` | Update 5 predicate strings (title, description, date, issued, isPartOf); add skip for aggregationEntity and hierarchyPosition |
583	| `notes/transform-adr.md` | New decisions D13–D17 for the 5 changed predicates |
584	
585	
```

---

### Assistant *(2026-05-07T12:02:41.264Z)*

Comparing the "⏭ skip" entries in §0.1 against `_MOCHO_SKIP`:

From the status table there are two explicit skips:
- `hasMet` (§25) — ✅ in `_MOCHO_SKIP` (just added)
- `hasType` (§24) — ❌ **not** in `_MOCHO_SKIP`

`hasType` maps to `EDM_NS + "hasType"` in `_DDBEDM_PROP` and is not excluded, so it's currently emitted on mocho CHO subjects. The plan also has an internal contradiction — §24 body says "keep `edm:hasType`" while the status table says "⏭ skip". Which is right?

---

### User *(2026-05-07T12:10:17.692Z)*

we need special handling for hasType. this is equivalent to edm:hasType. special handling here. when the value is a proper URI, keep as is. then look for corresponding skos:Concept where it matches "about", then emit 2 triples:
1. value is a valid Triple
<cho> edm:hasType <valid URI> ;
<valid URI> rdfs:label <the skos:prefLabel value of matching skos:Concept> .

2. value is a 32-character internal DDB uuuid
<cho> edm:hasType <urn:Concept:<id>> ;
<urn:Concept:<id>> rdfs:label <the skos:prefLabel value of matching skos:Concept> .

---

### Assistant *(2026-05-07T12:11:12.305Z)*

Same pattern as `emit_subject_triples` — add `"hasType"` to `_MOCHO_SKIP`, add a dedicated emitter, wire it into `emit_mocho_triples`. Let me implement all three.

---

### Assistant *(2026-05-07T12:11:12.893Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "limit": 8,
  "offset": 63
}
```

---

### User *(2026-05-07T12:11:12.925Z)*

**Tool result**
```
63	SKOS_PREF_LABEL = "http://www.w3.org/2004/02/skos/core#prefLabel"
64	SKOS_CONCEPT    = "http://www.w3.org/2004/02/skos/core#Concept"
65	DCTERMS_SOURCE  = "http://purl.org/dc/terms/source"
66	FOAF_THUMBNAIL  = "http://xmlns.com/foaf/0.1/thumbnail"
67	FOAF_ORG        = "http://xmlns.com/foaf/0.1/Organization"
68	FOAF_NAME       = "http://xmlns.com/foaf/0.1/name"
69	EDM_DATA_PROVIDER = EDM_NS + "dataProvider"
70	SCHEMA_URL      = "https://schema.org/url"
```

---

### Assistant *(2026-05-07T12:11:17.101Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "EDM_DATA_PROVIDER = EDM_NS + \"dataProvider\"",
  "new_string": "EDM_DATA_PROVIDER = EDM_NS + \"dataProvider\"\nEDM_HAS_TYPE      = EDM_NS + \"hasType\""
}
```

---

### User *(2026-05-07T12:13:05.087Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:13:11.888Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "    \"hasMet\",   # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph",
  "new_string": "    \"hasMet\",     # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph\n    \"hasType\",    # handled by emit_hastype_triples(); needs bare-ID expansion + label stub"
}
```

---

### User *(2026-05-07T12:13:14.363Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:13:17.650Z)*

Now add the import and the emitter function. First the import:

---

### Assistant *(2026-05-07T12:13:20.266Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    DCAT_DATASET, XSD_DATETIME,\n    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, DDB_HIERARCHY_TYPE, EDM_NS,\n    _HTYPE_PREFIX,",
  "new_string": "    DCAT_DATASET, XSD_DATETIME,\n    DDB_BASE, DDB_ITEM_BASE, DDB_API_BASE, DDB_HIERARCHY_TYPE, EDM_NS, EDM_HAS_TYPE,\n    _HTYPE_PREFIX,"
}
```

---

### User *(2026-05-07T12:13:24.846Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:13:27.924Z)*

Now add `emit_hastype_triples` right after `emit_subject_triples`:

---

### Assistant *(2026-05-07T12:13:28.522Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 5,
  "offset": 315
}
```

---

### User *(2026-05-07T12:13:28.525Z)*

**Tool result**
```
315	            key = f"lit:{label}"
316	            if key in seen:
317	                continue
318	            seen.add(key)
319	            escaped = _escape_literal(label)
```

---

### Assistant *(2026-05-07T12:13:31.465Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 8,
  "offset": 320
}
```

---

### User *(2026-05-07T12:13:31.467Z)*

**Tool result**
```
320	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
321	            lines.append(make_nq(cho_nt, f"<{DC_SUBJECT}>", obj_nt, graph_iri))
322	    return lines
323	
324	
325	def emit_creator_triples(
326	    cho_nt: str,
327	    creator_vals: list,
```

---

### Assistant *(2026-05-07T12:13:43.245Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "            obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n            lines.append(make_nq(cho_nt, f\"<{DC_SUBJECT}>\", obj_nt, graph_iri))\n    return lines\n\n\ndef emit_creator_triples(",
  "new_string": "            obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n            lines.append(make_nq(cho_nt, f\"<{DC_SUBJECT}>\", obj_nt, graph_iri))\n    return lines\n\n\ndef emit_hastype_triples(\n    cho_nt: str,\n    hastype_vals: list,\n    concepts_index: dict[str, dict],\n    graph_iri: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n) -> NQList:\n    \"\"\"Emit edm:hasType + rdfs:label stub for each IRI-valued hasType entry.\n\n    Bare 32-char IDs are expanded via the per-record index (fallback: mint as Concept URN).\n    Literal-only values (no resource) are silently skipped — edm:hasType range is skos:Concept.\n    \"\"\"\n    lines: NQList = []\n    seen: set[str] = set()\n    _bare = bare_id_to_uri or {}\n    for val in coerce_list(hastype_vals):\n        if not isinstance(val, dict):\n            continue\n        resource = (val.get(\"resource\") or \"\").strip()\n        if not resource:\n            continue\n        if not resource.startswith((\"http\", \"urn\")):\n            expanded = _bare.get(resource) or mint_bare_id(\"Concept\", resource)\n        else:\n            expanded = resource\n        expanded_safe = _sanitize_iri(expanded)\n        if expanded_safe in seen:\n            continue\n        seen.add(expanded_safe)\n        lines.append(make_nq(cho_nt, f\"<{EDM_HAS_TYPE}>\", f\"<{expanded_safe}>\", graph_iri))\n        concept = concepts_index.get(resource) or concepts_index.get(expanded)\n        if concept:\n            for pl in coerce_list(concept.get(\"prefLabel\")):\n                for obj_nt in value_to_nt_obj(pl):\n                    lines.append(make_nq(f\"<{expanded_safe}>\", f\"<{RDFS_LABEL}>\",\n                                         obj_nt, graph_iri))\n    return lines\n\n\ndef emit_creator_triples("
}
```

---

### User *(2026-05-07T12:13:44.850Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:13:49.483Z)*

Now wire it into `emit_mocho_triples` — collect the vals and call the emitter alongside subjects:

---

### Assistant *(2026-05-07T12:13:51.527Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    subject_vals: list = []\n    for skey in SUBJECT_KEYS:\n        subject_vals.extend(coerce_list(cho.get(skey)))",
  "new_string": "    subject_vals: list = []\n    for skey in SUBJECT_KEYS:\n        subject_vals.extend(coerce_list(cho.get(skey)))\n    hastype_vals: list = coerce_list(cho.get(\"hasType\"))"
}
```

---

### User *(2026-05-07T12:13:54.067Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:14:00.063Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    if subject_vals:\n        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri,\n                                              bare_id_to_uri)\n        lines.extend(_subject_lines)\n        _track_nqlist(_subject_lines)",
  "new_string": "    if subject_vals:\n        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri,\n                                              bare_id_to_uri)\n        lines.extend(_subject_lines)\n        _track_nqlist(_subject_lines)\n\n    if hastype_vals:\n        _hastype_lines = emit_hastype_triples(cho_nt, hastype_vals, concepts_index, graph_iri,\n                                              bare_id_to_uri)\n        lines.extend(_hastype_lines)\n        _track_nqlist(_hastype_lines)"
}
```

---

### User *(2026-05-07T12:14:01.207Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:14:04.292Z)*

Now add tests:

---

### Assistant *(2026-05-07T12:14:07.268Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n)",
  "new_string": "from transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_hastype_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n)"
}
```

---

### User *(2026-05-07T12:14:08.348Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:14:12.627Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX",
  "new_string": "from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE"
}
```

---

### User *(2026-05-07T12:14:14.918Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:14:32.438Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "def test_hasmet_in_mocho_skip():\n    assert \"hasMet\" in _MOCHO_SKIP, \"hasMet must be in _MOCHO_SKIP to prevent edm:hasMet on gemea CHOs\"",
  "new_string": "def test_hasmet_in_mocho_skip():\n    assert \"hasMet\" in _MOCHO_SKIP, \"hasMet must be in _MOCHO_SKIP to prevent edm:hasMet on gemea CHOs\"\n\n\n# ── emit_hastype_triples ──────────────────────────────────────────────────────\n\n_BARE_HT = \"R\" * 32\n\nclass TestEmitHastypeTriples:\n    _cho_nt = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"S\" * 32 + \">\"\n\n    def test_full_uri_emitted(self):\n        uri = \"http://ddb.vocnet.org/medientyp/mt003\"\n        vals = [{\"resource\": uri, \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)\n        assert any(EDM_HAS_TYPE in l and uri in l for l in lines)\n\n    def test_bare_id_expanded_via_index(self):\n        bare_id_to_uri = {_BARE_HT: f\"urn:ddbedm:Concept:{_BARE_HT}\"}\n        vals = [{\"resource\": _BARE_HT}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, bare_id_to_uri)\n        assert any(f\"urn:ddbedm:Concept:{_BARE_HT}\" in l for l in lines)\n\n    def test_bare_id_fallback_concept_mint(self):\n        vals = [{\"resource\": _BARE_HT}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, {})\n        assert any(f\"urn:ddbedm:Concept:{_BARE_HT}\" in l for l in lines)\n\n    def test_label_stub_from_concept(self):\n        uri = \"http://ddb.vocnet.org/thema/th001\"\n        concept = {\"about\": uri, \"prefLabel\": [{\"$\": \"Musik\", \"lang\": \"de\"}]}\n        vals = [{\"resource\": uri}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {uri: concept}, GRAPH_MOCHO)\n        label_line = next((l for l in lines if '\"Musik\"@de' in l), None)\n        assert label_line is not None\n        assert uri in label_line\n\n    def test_literal_only_skipped(self):\n        vals = [{\"resource\": \"\", \"$\": \"Foto\", \"lang\": \"de\"}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)\n        assert lines == []\n\n    def test_dedup(self):\n        uri = \"http://ddb.vocnet.org/medientyp/mt003\"\n        vals = [{\"resource\": uri}, {\"resource\": uri}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)\n        assert len([l for l in lines if EDM_HAS_TYPE in l]) == 1\n\n    def test_hastype_in_mocho_skip():\n        assert \"hasType\" in _MOCHO_SKIP"
}
```

---

### User *(2026-05-07T12:14:33.955Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:14:37.745Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && .venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -15",
  "description": "Run tests",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T12:14:40.942Z)*

**Tool result**
```
    @hookimpl(trylast=True)
    def pytest_pyfunc_call(pyfuncitem: Function) -> object | None:
        testfunction = pyfuncitem.obj
        if is_async_function(testfunction):
            async_fail(pyfuncitem.nodeid)
        funcargs = pyfuncitem.funcargs
        testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
>       result = testfunction(**testargs)
E       TypeError: test_hastype_in_mocho_skip() takes 0 positional arguments but 1 was given

.venv/lib/python3.9/site-packages/_pytest/python.py:157: TypeError
=========================== short test summary info ============================
FAILED scripts/transform/tests/test_transform.py::TestEmitHastypeTriples::test_hastype_in_mocho_skip
1 failed, 68 passed in 0.16s
```

---

### Assistant *(2026-05-07T12:14:42.979Z)*

That test was accidentally indented inside the class — it doesn't need `self`. Fix:

---

### Assistant *(2026-05-07T12:14:46.390Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "    def test_dedup(self):\n        uri = \"http://ddb.vocnet.org/medientyp/mt003\"\n        vals = [{\"resource\": uri}, {\"resource\": uri}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)\n        assert len([l for l in lines if EDM_HAS_TYPE in l]) == 1\n\n    def test_hastype_in_mocho_skip():\n        assert \"hasType\" in _MOCHO_SKIP",
  "new_string": "    def test_dedup(self):\n        uri = \"http://ddb.vocnet.org/medientyp/mt003\"\n        vals = [{\"resource\": uri}, {\"resource\": uri}]\n        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)\n        assert len([l for l in lines if EDM_HAS_TYPE in l]) == 1\n\n\ndef test_hastype_in_mocho_skip():\n    assert \"hasType\" in _MOCHO_SKIP"
}
```

---

### User *(2026-05-07T12:14:48.401Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:14:52.047Z)*

**Tool call:** `Bash`
```json
{
  "command": ".venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -5",
  "description": "Run tests",
  "dangerouslyDisableSandbox": true
}
```

---

### User *(2026-05-07T12:14:54.334Z)*

**Tool result**
```
.....................................................................    [100%]
69 passed in 0.07s
```

---

### Assistant *(2026-05-07T12:14:59.558Z)*

All 69 pass. Summary of changes:

- **`constants.py`**: Added `EDM_HAS_TYPE = EDM_NS + "hasType"`; added `"hasType"` to `_MOCHO_SKIP`
- **`emitters.py`**: New `emit_hastype_triples()` — IRI-only dispatch (literals silently skipped), bare-ID expansion via index with Concept fallback, `rdfs:label` stub from matching `concepts_index` entry, deduplication
- **`emit_mocho_triples()`**: Collects `hasType` vals and calls the new emitter alongside subjects, using the same `bare_id_to_uri` index and `concepts_index` already built for the record

---

### User *(2026-05-07T12:16:56.817Z)*

please check all emitters that URIs are checked:

1. literals are proper 
- escaped properly, '\n' will not cause carriage return in .nt/.nq)
- <br> are handled.

2. uris are correct
- when multiple https:blah blah http:// bleh bleh in one value are split. emit 2 triples (s, p, https1) and (s, p, http)

---

### Assistant *(2026-05-07T12:17:02.413Z)*

Let me read all the relevant code carefully before drawing any conclusions.

---

### Assistant *(2026-05-07T12:17:02.884Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py"
}
```

---

### User *(2026-05-07T12:17:02.897Z)*

**Tool result**
```
1	"""Utility functions: N-Quads formatting, URI minting, value normalisation."""
2	
3	from __future__ import annotations
4	
5	import re
6	from collections import Counter
7	
8	from .constants import (
9	    AgentDict, NQuad, NQList,
10	    GEMEA_BASE, DDB_ITEM_BASE,
11	    _PREFIXES, _MEDIATYPE_PREFIX, _SECTOR_PREFIX,
12	)
13	
14	# Characters forbidden inside N-Triples IRI references (RFC 3987 + NT spec)
15	_IRI_UNSAFE_RE = re.compile(r'[\x00-\x20<>"{}|\\^`\x7f]')
16	
17	
18	def _sanitize_iri(iri: str) -> str:
19	    """Percent-encode characters illegal inside NT IRI references."""
20	    return _IRI_UNSAFE_RE.sub(lambda m: f"%{ord(m.group()):02X}", iri)
21	
22	
23	def make_nq(s_nt: str, p_nt: str, o_nt: str, graph_iri: str) -> NQuad:
24	    """Return one N-Quads line."""
25	    return f"{s_nt} {p_nt} {o_nt} <{graph_iri}> ."
26	
27	
28	def coerce_list(val: object) -> list:
29	    """Normalise None/dict/list to a list."""
30	    if val is None:
31	        return []
32	    if isinstance(val, dict):
33	        return [val]
34	    if isinstance(val, list):
35	        return val
36	    return []
37	
38	
39	def _expand_prefix(curie: str) -> str:
40	    """Expand a CURIE (e.g. 'rdam:P30134') to a full IRI."""
41	    for prefix, base in _PREFIXES.items():
42	        if curie.startswith(prefix + ":"):
43	            return base + curie[len(prefix) + 1:]
44	    return curie
45	
46	
47	def _to_curie(iri: str) -> str:
48	    """Collapse a full IRI to a CURIE using _PREFIXES; return IRI unchanged if no match."""
49	    for prefix, base in _PREFIXES.items():
50	        if iri.startswith(base):
51	            return f"{prefix}:{iri[len(base):]}"
52	    return iri
53	
54	
55	def mint_cho_uri(obj_id: str) -> str:
56	    """Return the minted GeMeA mocho CHO URI for a 32-char DDB object ID (D22)."""
57	    return GEMEA_BASE + obj_id
58	
59	
60	def mint_bare_id(entity_class: str, raw_id: str) -> str:
61	    """Expand a bare 32-char ID to a full URI (D27).
62	
63	    ProvidedCHO bare IDs → DDB item URI.
64	    All other entity types → urn:ddbedm:<ClassName>:<id>.
65	    Full URIs and URNs are returned unchanged.
66	    """
67	    if raw_id.startswith(("http", "urn")):
68	        return raw_id
69	    if entity_class == "ProvidedCHO":
70	        return DDB_ITEM_BASE + raw_id
71	    return f"urn:ddbedm:{entity_class}:{raw_id}"
72	
73	
74	def _escape_literal(s: str) -> str:
75	    """Escape characters illegal in N-Triples/N-Quads literal content."""
76	    return (s.replace("\\", "\\\\")
77	             .replace('"', '\\"')
78	             .replace("\n", "\\n")
79	             .replace("\r", "\\r")
80	             .replace("\t", "\\t"))
81	
82	
83	def value_to_nt_obj(val: object, sani_ctr: Counter | None = None) -> list[str]:
84	    """Convert a JSONL field value to a list of N-Triples object strings.
85	
86	    Handles all value shapes produced by the DDB EDM JSONL:
87	      None / ""                    → []
88	      str (non-empty)              → ['"escaped"']
89	      list                         → recurse and flatten
90	      {"resource": IRI}            → ["<IRI>"] (IRI percent-encoded if unsafe chars present)
91	      {"lang": L, "$": T}          → ['"T"@L']
92	      {"lang": null, "$": T}       → ['"T"']
93	      {"resource": null, "$": ""}  → []
94	
95	    sani_ctr: if provided, incremented once per IRI that required sanitisation.
96	    """
97	    if val is None:
98	        return []
99	    if isinstance(val, str):
100	        return [f'"{_escape_literal(val)}"'] if val else []
101	    if isinstance(val, list):
102	        result = []
103	        for item in val:
104	            result.extend(value_to_nt_obj(item, sani_ctr))
105	        return result
106	    if isinstance(val, dict):
107	        resource = val.get("resource")
108	        if resource:
109	            parts = resource.split()  # split handles multi-URI values (DDB data quality issue)
110	            result = []
111	            for uri in parts:
112	                sanitized = _sanitize_iri(uri)
113	                if sani_ctr is not None and sanitized != uri:
114	                    sani_ctr["uri_sanitized"] += 1
115	                result.append(f"<{sanitized}>")
116	            if sani_ctr is not None and len(parts) > 1:
117	                sani_ctr["uri_split"] += len(parts)
118	            return result
119	        text = val.get("$", "")
120	        if not text:
121	            return []
122	        escaped = _escape_literal(str(text))
123	        lang = val.get("lang")
124	        if lang:
125	            return [f'"{escaped}"@{lang}']
126	        return [f'"{escaped}"']
127	    return []
128	
129	
130	def normalize_date(s: str) -> list[str]:
131	    """Normalise a dc:date string to ISO 8601.
132	
133	    8-digit compact YYYYMMDD → YYYY-MM-DD.
134	    ISO interval begin/end → [begin, end].
135	    All other values returned unchanged.
136	    """
137	    s = s.strip()
138	    if "/" in s:
139	        parts = s.split("/", 1)
140	        return [normalize_date(p)[0] for p in parts]
141	    if len(s) == 8 and s.isdigit():
142	        return [f"{s[:4]}-{s[4:6]}-{s[6:]}"]
143	    return [s]
144	
145	
146	def build_bare_id_index(rdf: dict) -> dict[str, str]:
147	    """Map bare about IDs → expanded URIs for every entity in the record (D27)."""
148	    index: dict[str, str] = {}
149	    for entity_type, entities in rdf.items():
150	        for entity in coerce_list(entities):
151	            if not isinstance(entity, dict):
152	                continue
153	            raw_about = (entity.get("about") or "").strip()
154	            for part in raw_about.split():
155	                if part and not part.startswith(("http", "urn")):
156	                    index[part] = mint_bare_id(entity_type, _sanitize_iri(part))
157	    return index
158	
159	
160	def expand_obj_nt(obj_nt: str, bare_id_to_uri: dict[str, str]) -> str:
161	    """Resolve a bare-ID IRI object <ID> via the index; return unchanged otherwise."""
162	    if obj_nt.startswith("<") and obj_nt.endswith(">"):
163	        inner = obj_nt[1:-1]
164	        if not inner.startswith(("http", "urn")):
165	            resolved = bare_id_to_uri.get(inner)
166	            if resolved:
167	                return f"<{resolved}>"
168	    return obj_nt
169	
170	
171	def is_ddb_or_gnd(uri: str) -> bool:
172	    """True if URI is a DDB organization or GND authority URI."""
173	    return uri.startswith((
174	        "http://www.deutsche-digitale-bibliothek.de/organization/",
175	        "http://d-nb.info/gnd/",
176	        "https://d-nb.info/gnd/",
177	    ))
178	
179	
180	def resolve_agent(
181	    label: str,
182	    resource: str,
183	    agents_index: dict[str, AgentDict],
184	) -> AgentDict | None:
185	    """Resolve a creator/contributor to an Agent dict.
186	
187	    URI match preferred; label match fallback.
188	    Returns None if no match found.
189	    """
190	    if resource and resource in agents_index:
191	        return agents_index[resource]
192	    if label and label in agents_index:
193	        return agents_index[label]
194	    return None
195	
196	
197	def _extract_mediatype_sector(concepts: object) -> tuple[str, str]:
198	    """Return (mediatype_iri, sector_iri) from the record's Concept list."""
199	    mediatype = "any"
200	    sector    = "any"
201	    for c in coerce_list(concepts):
202	        if not isinstance(c, dict):
203	            continue
204	        about = c.get("about") or ""
205	        if about.startswith(_MEDIATYPE_PREFIX):
206	            mediatype = about
207	        elif about.startswith(_SECTOR_PREFIX):
208	            sector = about
209	    return mediatype, sector
210	
211	
212	def get_object_id(record: dict) -> str | None:
213	    """Extract 32-char object ID from ProvidedCHO.about URI. Returns None on failure."""
214	    try:
215	        about = record["edm"]["RDF"]["ProvidedCHO"]["about"]
216	    except (KeyError, TypeError):
217	        return None
218	    if not about:
219	        return None
220	    # Bare 32-char ID (D27)
221	    if len(about) == 32 and not about.startswith("http"):
222	        return about
223	    obj_id = about.rstrip("/").rsplit("/", 1)[-1]
224	    return obj_id if len(obj_id) == 32 else None
225	
```

---

### Assistant *(2026-05-07T12:17:02.942Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py"
}
```

---

### User *(2026-05-07T12:17:03.487Z)*

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
26	    build_bare_id_index, expand_obj_nt,
27	)
28	
29	
30	def emit_ddbedm_triples(rdf: dict, graph_iri: str) -> tuple[NQList, Counter, Counter, Counter]:
31	    """Emit verbatim EDM passthrough triples for all entity types in rdf (§6.1).
32	
33	    Subject: first URI in entity['about']; owl:sameAs emitted for any additional URIs.
34	    Includes mt007 records.
35	    Returns (lines, class_ctr, pred_ctr, sani_ctr) where sani_ctr tracks
36	    uri_sanitized, uri_split, and uri_about_split counts.
37	    """
38	    lines:     NQList  = []
39	    class_ctr: Counter = Counter()
40	    pred_ctr:  Counter = Counter()
41	    sani_ctr:  Counter = Counter()
42	    _skip = frozenset({"about"})
43	    bare_id_to_uri = build_bare_id_index(rdf)
44	    for entity_type, entities in rdf.items():
45	        edm_class = _EDM_ENTITY_TYPES.get(entity_type)
46	        for entity in coerce_list(entities):
47	            if not isinstance(entity, dict):
48	                continue
49	            raw_about = (entity.get("about") or "").strip()
50	            if not raw_about:
51	                continue
52	            about_parts = raw_about.split()
53	            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
54	            subj_nt  = f"<{subj_uri}>"
55	            if len(about_parts) > 1:
56	                sani_ctr["uri_about_split"] += len(about_parts) - 1
57	                for alt in about_parts[1:]:
58	                    lines.append(make_nq(subj_nt, f"<{OWL_SAMEAS}>",
59	                                         f"<{_sanitize_iri(alt)}>", graph_iri))
60	            if edm_class:
61	                lines.append(make_nq(subj_nt, f"<{RDF_TYPE}>", f"<{edm_class}>", graph_iri))
62	                class_ctr[_to_curie(edm_class)] += 1
63	            for key, val in entity.items():
64	                if key in _skip:
65	                    continue
66	                pred_iri = _DDBEDM_PROP.get(key)
67	                if not pred_iri:
68	                    continue
69	                pred_nt = f"<{pred_iri}>"
70	                curie   = _to_curie(pred_iri)
71	                for obj_nt in value_to_nt_obj(val, sani_ctr):
72	                    lines.append(make_nq(subj_nt, pred_nt,
73	                                         expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))
74	                    pred_ctr[curie] += 1
75	    return lines, class_ctr, pred_ctr, sani_ctr
76	
77	
78	def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
79	    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
80	    lines: NQList = []
81	    props = record.get("properties") or {}
82	    prov  = record.get("provider-info") or {}
83	
84	    item_id         = (props.get("item-id")         or "").strip()
85	    dataset_id      = (props.get("dataset-id")      or "").strip()
86	    dataset_label   = (props.get("dataset-label")   or "").strip()
87	    revision        = (props.get("revision-id")     or "").strip()
88	    ingest_dt       = (props.get("ingest-date")     or "").strip()
89	    map_ver         = (props.get("mapping-version") or "").strip()
90	    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
91	    provider_name   = (prov.get("provider-name")    or "").strip()
92	    provider_uri    = (prov.get("provider-uri")     or "").strip()
93	    provider_id     = (prov.get("provider-id")      or "").strip()
94	    provider_isil   = (prov.get("provider-isil")    or "").strip()
95	
96	    src_desc  = (record.get("source") or {}).get("description") or {}
97	    src_ref   = (src_desc.get("record") or {}) if isinstance(src_desc, dict) else {}
98	    ref_val   = (src_ref.get("ref",  "") or "").strip() if isinstance(src_ref, dict) else ""
99	    src_href  = (src_ref.get("href", "") or "").strip() if isinstance(src_ref, dict) else ""
100	    rec_type  = (src_ref.get("type", "") or "").strip() if isinstance(src_ref, dict) else ""
101	
102	    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
103	    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
104	    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
105	               if provider_ddb_id else ""
106	
107	    # ── CHO node ──────────────────────────────────────────────────────────────
108	    cho_nt = f"<{ddb_cho_uri}>"
109	    lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
110	    if ds_uri:
111	        lines.append(make_nq(cho_nt, f"<{PROV_DERIVED}>",   f"<{ds_uri}>",   graph_iri))
112	    if xslt_uri:
113	        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
114	    if ingest_dt:
115	        lines.append(make_nq(cho_nt, f"<{PROV_GEN_TIME}>",
116	                             f'"{_escape_literal(ingest_dt)}"^^<{XSD_DATETIME}>', graph_iri))
117	    if revision:
118	        lines.append(make_nq(cho_nt, f"<{DCTERMS_HAS_VER}>",
119	                             f'"{_escape_literal(revision)}"', graph_iri))
120	    if ref_val:
121	        lines.append(make_nq(cho_nt, f"<{DCTERMS_REF}>",
122	                             f'"ddb:{_escape_literal(ref_val)}"', graph_iri))
123	
124	    # ── Dataset node ──────────────────────────────────────────────────────────
125	    if ds_uri:
126	        ds_nt = f"<{ds_uri}>"
127	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{DCAT_DATASET}>", graph_iri))
128	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
129	        lines.append(make_nq(ds_nt, f"<{DCTERMS_ID}>",
130	                             f'"{_escape_literal(dataset_id)}"', graph_iri))
131	        if dataset_label:
132	            lines.append(make_nq(ds_nt, f"<{RDFS_LABEL}>",
133	                                 f'"{_escape_literal(dataset_label)}"@de', graph_iri))
134	        if rec_type:
135	            lines.append(make_nq(ds_nt, f"<{DCTERMS_TYPE}>", f"<{rec_type}>", graph_iri))
136	        if prov_uri:
137	            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
138	                                 f"<{prov_uri}>", graph_iri))
139	
140	    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────
141	    if xslt_uri:
142	        xslt_nt = f"<{xslt_uri}>"
143	        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
144	        lines.append(make_nq(xslt_nt, f"<{DCTERMS_HAS_VER}>",
145	                             f'"{_escape_literal(map_ver)}"', graph_iri))
146	        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
147	
148	    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────
149	    ddb_nt = f"<{DDB_BASE}>"
150	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
151	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
152	    lines.append(make_nq(ddb_nt, f"<{FOAF_NAME}>",
153	                         '"Deutsche Digitale Bibliothek"', graph_iri))
154	
155	    # ── Provider Agent node ───────────────────────────────────────────────────
156	    if prov_uri:
157	        prov_nt = f"<{prov_uri}>"
158	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
159	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
160	        if provider_name:
161	            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
162	                                 f'"{_escape_literal(provider_name)}"', graph_iri))
163	        if provider_uri:
164	            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
165	        if provider_id:
166	            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
167	                                 f'"{_escape_literal(provider_id)}"', graph_iri))
168	        if provider_isil:
169	            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>", f"<{provider_isil}>", graph_iri))
170	
171	    # ── SourceRecord node (one per binary entry under same URI) ───────────────
172	    if src_href:
173	        src_rec_uri = DDB_API_BASE + src_href.lstrip("/")
174	        src_nt      = f"<{src_rec_uri}>"
175	        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
176	        for binary in coerce_list((record.get("binaries") or {}).get("binary")):
177	            if not isinstance(binary, dict):
178	                continue
179	            ref   = (binary.get("ref")            or "").strip()
180	            name  = (binary.get("name")           or "").strip()
181	            name2 = (binary.get("name2")          or "").strip()
182	            kind  = (binary.get("kind")           or "").strip()
183	            lpath = (binary.get("local_pathname") or "").strip()
184	            if ref:
185	                lines.append(make_nq(src_nt, f"<{DC_ID}>",
186	                                     f'"{_escape_literal(ref)}"', graph_iri))
187	            if name:
188	                lines.append(make_nq(src_nt, f"<{DC_TITLE}>",
189	                                     f'"{_escape_literal(name)}"@de', graph_iri))
190	            desc = (name2 + " | " + name) if name2 and name else (name2 or name)
191	            if desc:
192	                lines.append(make_nq(src_nt, f"<{DC_DESCRIPTION}>",
193	                                     f'"{_escape_literal(desc)}"@de', graph_iri))
194	            if kind:
195	                lines.append(make_nq(src_nt, f"<{DCTERMS_RIGHTS}>", f"<{kind}>", graph_iri))
196	            if lpath and lpath.startswith("http"):
197	                lines.append(make_nq(src_nt, f"<{DCTERMS_SOURCE}>", f"<{lpath}>", graph_iri))
198	
199	    return lines
200	
201	
202	def retype_entities(
203	    sector: str,
204	    mediatype: str,
205	    htype_code: str | None,
206	    dctype_vals: list,
207	    cho_nt: str,
208	    mediatype_class_map: dict,
209	    htype_map: dict,
210	    audio_type2class: dict,
211	    graph_iri: str,
212	) -> tuple[NQList, str, str, dict]:
213	    """Dispatch rdf:type triples for a ProvidedCHO (§6.4, transform-revised-plan.md §1.1).
214	
215	    Returns (lines, target_class_full_iri, wemi, dispatch_flags).
216	    target_class is used for property alignment lookup; wemi for contributor column selection.
217	    dispatch_flags: {"htype_used": bool, "fallback": bool}
218	    """
219	    lines: NQList = []
220	    row = (
221	        mediatype_class_map.get((sector, mediatype))
222	        or mediatype_class_map.get(("any", "any"))
223	        or {}
224	    )
225	    use_htype  = row.get("use_htype", False)
226	    rdf_type_w = row.get("rdf_type_w", "")
227	    rdf_type_m = row.get("rdf_type_m", "")
228	
229	    primary_class = ""
230	    htype_used    = False
231	
232	    # Layer 1: htype-derived class (for htype-first strata)
233	    if use_htype and htype_code:
234	        entry = htype_map.get(htype_code)
235	        if entry:
236	            type_iris, rst_iris = entry
237	            for t in type_iris:
238	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{t}>", graph_iri))
239	            for r in rst_iris:
240	                lines.append(make_nq(cho_nt, f"<{RICO_HAS_RST}>", f"<{r}>", graph_iri))
241	            primary_class = type_iris[0]  # first = most specific
242	            htype_used    = True
243	
244	    # Layer 2: fixed mediatype class (always emit if set; added on top of layer 1)
245	    if rdf_type_w:
246	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_w}>", graph_iri))
247	        if not primary_class:
248	            primary_class = rdf_type_w
249	    if rdf_type_m:
250	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_m}>", graph_iri))
251	        if not primary_class:
252	            primary_class = rdf_type_m
253	
254	    # Audio group dispatch: dc:type → mo:MusicalManifestation (Group A) (§2.3)
255	    _aco_audio = "https://w3id.org/ac-ontology/aco#AudioManifestation"
256	    _mo_mani   = "http://purl.org/ontology/mo/MusicalManifestation"
257	    if rdf_type_m == _aco_audio and dctype_vals and not use_htype:
258	        for dct in dctype_vals:
259	            dc_text = (dct.get("$") or "").strip() if isinstance(dct, dict) else ""
260	            if audio_type2class.get((sector, dc_text)) == "A":
261	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{_mo_mani}>", graph_iri))
262	                primary_class = _mo_mani
263	                break
264	
265	    # D9 fallback — no class resolved
266	    is_fallback = not primary_class
267	    if is_fallback:
268	        fallback = MOCHO_NS + "Manifestation"
269	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{fallback}>", graph_iri))
270	        primary_class = fallback
271	
272	    if htype_code:
273	        lines.append(make_nq(cho_nt, f"<{DDB_HIERARCHY_TYPE}>",
274	                             f"<{_HTYPE_PREFIX}{htype_code}>", graph_iri))
275	
276	    wemi = _CLASS_WEMI.get(primary_class, "M")
277	    return lines, primary_class, wemi, {"htype_used": htype_used, "fallback": is_fallback}
278	
279	
280	def emit_subject_triples(
281	    cho_nt: str,
282	    subject_vals: list,
283	    concepts_index: dict[str, dict],
284	    graph_iri: str,
285	    bare_id_to_uri: dict[str, str] | None = None,
286	) -> NQList:
287	    """Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended)."""
288	    lines: NQList = []
289	    seen: set[str] = set()
290	    _bare = bare_id_to_uri or {}
291	    for val in subject_vals:
292	        if not isinstance(val, dict):
293	            continue
294	        resource = (val.get("resource") or "").strip()
295	        label    = (val.get("$")        or "").strip()
296	        lang     = (val.get("lang")     or "").strip()
297	        if resource:
298	            # Expand bare IDs: look up in the per-record index, fall back to Concept mint
299	            if not resource.startswith(("http", "urn")):
300	                expanded = _bare.get(resource) or mint_bare_id("Concept", resource)
301	            else:
302	                expanded = resource
303	            expanded_safe = _sanitize_iri(expanded)
304	            if expanded_safe in seen:
305	                continue
306	            seen.add(expanded_safe)
307	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SUBJECT}>", f"<{expanded_safe}>", graph_iri))
308	            concept = concepts_index.get(resource) or concepts_index.get(expanded)
309	            if concept:
310	                for pl in coerce_list(concept.get("prefLabel")):
311	                    for obj_nt in value_to_nt_obj(pl):
312	                        lines.append(make_nq(f"<{expanded_safe}>", f"<{RDFS_LABEL}>",
313	                                             obj_nt, graph_iri))
314	        elif label:
315	            key = f"lit:{label}"
316	            if key in seen:
317	                continue
318	            seen.add(key)
319	            escaped = _escape_literal(label)
320	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
321	            lines.append(make_nq(cho_nt, f"<{DC_SUBJECT}>", obj_nt, graph_iri))
322	    return lines
323	
324	
325	def emit_hastype_triples(
326	    cho_nt: str,
327	    hastype_vals: list,
328	    concepts_index: dict[str, dict],
329	    graph_iri: str,
330	    bare_id_to_uri: dict[str, str] | None = None,
331	) -> NQList:
332	    """Emit edm:hasType + rdfs:label stub for each IRI-valued hasType entry.
333	
334	    Bare 32-char IDs are expanded via the per-record index (fallback: mint as Concept URN).
335	    Literal-only values (no resource) are silently skipped — edm:hasType range is skos:Concept.
336	    """
337	    lines: NQList = []
338	    seen: set[str] = set()
339	    _bare = bare_id_to_uri or {}
340	    for val in coerce_list(hastype_vals):
341	        if not isinstance(val, dict):
342	            continue
343	        resource = (val.get("resource") or "").strip()
344	        if not resource:
345	            continue
346	        if not resource.startswith(("http", "urn")):
347	            expanded = _bare.get(resource) or mint_bare_id("Concept", resource)
348	        else:
349	            expanded = resource
350	        expanded_safe = _sanitize_iri(expanded)
351	        if expanded_safe in seen:
352	            continue
353	        seen.add(expanded_safe)
354	        lines.append(make_nq(cho_nt, f"<{EDM_HAS_TYPE}>", f"<{expanded_safe}>", graph_iri))
355	        concept = concepts_index.get(resource) or concepts_index.get(expanded)
356	        if concept:
357	            for pl in coerce_list(concept.get("prefLabel")):
358	                for obj_nt in value_to_nt_obj(pl):
359	                    lines.append(make_nq(f"<{expanded_safe}>", f"<{RDFS_LABEL}>",
360	                                         obj_nt, graph_iri))
361	    return lines
362	
363	
364	def emit_creator_triples(
365	    cho_nt: str,
366	    creator_vals: list,
367	    agents_index: dict[str, AgentDict],
368	    target_class: str,
369	    class_prop_align: PropAlign,
370	    graph_iri: str,
371	) -> NQList:
372	    """Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).
373	
374	    Both tracks run independently for each creator value (D2 / props-mapping §4).
375	    """
376	    lines: NQList = []
377	    dc_creator_iri = "http://purl.org/dc/elements/1.1/creator"
378	    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), "")
379	
380	    for val in coerce_list(creator_vals):
381	        if not isinstance(val, dict):
382	            continue
383	        resource = (val.get("resource") or "").strip()
384	        label    = (val.get("$")        or "").strip()
385	        lang     = (val.get("lang")     or "").strip()
386	
387	        # Track 1: class-specific predicate (always runs when target_prop is known)
388	        if track1_prop:
389	            if resource:
390	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
391	            elif label:
392	                escaped = _escape_literal(label)
393	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
394	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", obj_nt, graph_iri))
395	
396	        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)
397	        agent = resolve_agent(label, resource, agents_index)
398	        if agent:
399	            agent_uri = (agent.get("about") or "").strip()
400	            if agent_uri and is_ddb_or_gnd(agent_uri):
401	                lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>",
402	                                     f"<{agent_uri}>", graph_iri))
403	                agent_nt = f"<{agent_uri}>"
404	                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
405	                pref = agent.get("prefLabel") or label
406	                if pref and isinstance(pref, str):
407	                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>",
408	                                         f'"{_escape_literal(pref)}"', graph_iri))
409	    return lines
410	
411	
412	def emit_contributor_triples(
413	    cho_nt: str,
414	    contributor_vals: list,
415	    event_participant_index: dict[str, str],
416	    lido_dispatch: dict[str, dict],
417	    target_class: str,
418	    wemi: str,
419	    graph_iri: str,
420	) -> NQList:
421	    """Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5)."""
422	    lines: NQList = []
423	    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), "dc_agent_fallback")
424	
425	    for val in coerce_list(contributor_vals):
426	        if not isinstance(val, dict):
427	            continue
428	        resource = (val.get("resource") or "").strip()
429	        label    = (val.get("$")        or "").strip()
430	        lang     = (val.get("lang")     or "").strip()
431	
432	        lido_type   = event_participant_index.get(resource) if resource else None
433	        lido_row    = lido_dispatch.get(lido_type) if lido_type else None
434	        target_prop = (
435	            (lido_row.get(prop_col) or lido_row.get("dc_agent_fallback") or DC_CONTRIBUTOR)
436	            if lido_row else DC_CONTRIBUTOR
437	        )
438	
439	        if resource:
440	            lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
441	            agent_nt = f"<{_sanitize_iri(resource)}>"
442	            lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
443	            if label:
444	                escaped = _escape_literal(label)
445	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
446	                lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
447	        elif label:
448	            escaped = _escape_literal(label)
449	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
450	            lines.append(make_nq(cho_nt, f"<{DC_CONTRIBUTOR}>", obj_nt, graph_iri))
451	    return lines
452	
453	
454	def emit_aggregation_triples(agg: dict, cho_nt: str, graph_iri: str) -> NQList:
455	    """Emit mocho triples derived from the Aggregation block (D23)."""
456	    lines: NQList = []
457	    _edm_dp     = EDM_NS + "dataProvider"
458	    _org_prefix = "http://www.deutsche-digitale-bibliothek.de/organization/"
459	
460	    is_shown = agg.get("isShownAt") or {}
461	    if isinstance(is_shown, dict):
462	        uri = (is_shown.get("resource") or "").strip()
463	        if uri:
464	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SOURCE}>", f"<{_sanitize_iri(uri)}>", graph_iri))
465	
466	    for dp in coerce_list(agg.get("dataProvider")):
467	        if not isinstance(dp, dict):
468	            continue
469	        uri = (dp.get("resource") or "").strip()
470	        if uri and uri.startswith(_org_prefix):
471	            lines.append(make_nq(cho_nt, f"<{_edm_dp}>", f"<{_sanitize_iri(uri)}>", graph_iri))
472	
473	    for obj in coerce_list(agg.get("object")):
474	        if not isinstance(obj, dict):
475	            continue
476	        uri = (obj.get("resource") or "").strip()
477	        if uri:
478	            lines.append(make_nq(cho_nt, f"<{FOAF_THUMBNAIL}>", f"<{_sanitize_iri(uri)}>", graph_iri))
479	
480	    return lines
481	
482	
483	def emit_place_stubs(places: object, graph_iri: str) -> NQList:
484	    """Emit rdfs:label stubs for each Place entity referenced by the record (D24)."""
485	    lines: NQList = []
486	    for place in coerce_list(places):
487	        if not isinstance(place, dict):
488	            continue
489	        raw_about = (place.get("about") or "").strip()
490	        if not raw_about:
491	            continue
492	        place_uri = mint_bare_id("Place", raw_about)
493	        place_nt  = f"<{place_uri}>"
494	        for lbl in coerce_list(place.get("prefLabel")):
495	            for obj_nt in value_to_nt_obj(lbl):
496	                lines.append(make_nq(place_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
497	    return lines
498	
499	
500	def werk_staging_row(cho_uri: str, cho: dict, target_class: str) -> dict | None:
501	    """Build a werk_staging dict if target_class is a W-slot class (D26). Else None."""
502	    if target_class not in _W_SLOT_CLASSES:
503	        return None
504	
505	    title = ""
506	    tv = cho.get("title")
507	    if isinstance(tv, dict):
508	        title = (tv.get("$") or "").strip()
509	    elif isinstance(tv, list) and tv:
510	        first = tv[0]
511	        title = (first.get("$") or "").strip() if isinstance(first, dict) else ""
512	
513	    dc_alt: list[str] = []
514	    for v in coerce_list(cho.get("alternative")):
515	        t = (v.get("$") or "").strip() if isinstance(v, dict) else ""
516	        if t:
517	            dc_alt.append(t)
518	
519	    dc_created = ""
520	    for v in coerce_list(cho.get("date")):
521	        t = (v if isinstance(v, str) else "").strip()
522	        if t:
523	            dc_created = t
524	            break
525	
526	    creator_uris: list[str] = []
527	    creator_lits: list[str] = []
528	    for v in coerce_list(cho.get("creator")):
529	        if not isinstance(v, dict):
530	            continue
531	        uri = (v.get("resource") or "").strip()
532	        lit = (v.get("$")        or "").strip()
533	        if uri:
534	            creator_uris.append(uri)
535	        elif lit:
536	            creator_lits.append(lit)
537	
538	    obj_id = cho_uri.rsplit("/", 1)[-1]
539	    return {
540	        "ddb_obj_id":       obj_id,
541	        "cho_uri":          cho_uri,
542	        "target_class":     target_class,
543	        "dc_title":         title,
544	        "dc_alternative":   dc_alt,
545	        "dc_created":       dc_created,
546	        "creator_uris":     creator_uris,
547	        "creator_literals": creator_lits,
548	    }
549	
550	
551	def emit_mocho_triples(
552	    rdf: dict,
553	    cho_uri: str,
554	    ddb_uri: str,
555	    sector: str,
556	    mediatype: str,
557	    mediatype_class_map: dict,
558	    htype_map: dict,
559	    audio_type2class: dict,
560	    class_prop_align: PropAlign,
561	    lido_dispatch: dict,
562	    graph_iri: str,
563	) -> tuple[NQList, str, str, dict]:
564	    """Emit all mocho-graph triples for one record (§6.3). Returns (lines, target_class, wemi, dispatch_flags).
565	
566	    dispatch_flags includes "preds_all" and "preds_new" Counters (CURIEs) built during emission.
567	    """
568	    lines:     NQList  = []
569	    preds_all: Counter = Counter()
570	    preds_new: Counter = Counter()
571	    sani_ctr:  Counter = Counter()
572	    bare_id_to_uri = build_bare_id_index(rdf)
573	
574	    def _track(pred_iri: str) -> None:
575	        curie = _to_curie(pred_iri)
576	        preds_all[curie] += 1
577	        if any(pred_iri.startswith(ns) for ns in _NEW_NS):
578	            preds_new[curie] += 1
579	
580	    def _track_nqlist(nqlist: NQList) -> None:
581	        for nq in nqlist:
582	            try:
583	                _track(nq.split("> <", 1)[1].split(">", 1)[0])
584	            except IndexError:
585	                pass
586	
587	    cho: dict = rdf.get("ProvidedCHO") or {}
588	    if isinstance(cho, list):
589	        cho = cho[0] if cho else {}
590	
591	    cho_nt      = f"<{cho_uri}>"
592	    htype       = (cho.get("hierarchyType") or "").strip() or None
593	    dctype_vals = coerce_list(cho.get("dcType"))
594	
595	    # ── Class dispatch ────────────────────────────────────────────────────────
596	    type_lines, target_class, wemi, dispatch_flags = retype_entities(
597	        sector, mediatype, htype, dctype_vals,
598	        cho_nt, mediatype_class_map, htype_map, audio_type2class, graph_iri,
599	    )
600	    lines.extend(type_lines)
601	    _track_nqlist(type_lines)
602	
603	    # owl:sameAs link to original DDB URI (D22)
604	    lines.append(make_nq(cho_nt, f"<{OWL_SAMEAS}>", f"<{ddb_uri}>", graph_iri))
605	    _track(OWL_SAMEAS)
606	
607	    # ── Build per-record indexes ───────────────────────────────────────────────
608	    agents_index: dict[str, AgentDict] = {}
609	    for agent in coerce_list(rdf.get("Agent")):
610	        if not isinstance(agent, dict):
611	            continue
612	        about = (agent.get("about") or "").strip()
613	        if about:
614	            agents_index[mint_bare_id("Agent", about)] = agent
615	        for pl in coerce_list(agent.get("prefLabel")):
616	            t = (pl.get("$") or "").strip() if isinstance(pl, dict) else ""
617	            if t:
618	                agents_index.setdefault(t, agent)
619	
620	    event_participant_index: dict[str, str] = {}
621	    for event in coerce_list(rdf.get("Event")):
622	        if not isinstance(event, dict):
623	            continue
624	        ht = event.get("hasType") or {}
625	        if isinstance(ht, list):
626	            ht = ht[0] if ht else {}
627	        lido_type_uri = (ht.get("resource") or "").strip() if isinstance(ht, dict) else ""
628	        for p in coerce_list(event.get("P11_had_participant")):
629	            puri = (p.get("resource") or "").strip() if isinstance(p, dict) else ""
630	            if puri and lido_type_uri:
631	                event_participant_index[puri] = lido_type_uri
632	
633	    concepts_index: dict[str, dict] = {}
634	    for concept in coerce_list(rdf.get("Concept")):
635	        if not isinstance(concept, dict):
636	            continue
637	        about = (concept.get("about") or "").strip()
638	        if about:
639	            concepts_index[about] = concept
640	
641	    # ── dc:title — dual-emit (props-mapping D4) ───────────────────────────────
642	    dc_title_iri = "http://purl.org/dc/elements/1.1/title"
643	    title_prop   = class_prop_align.get((target_class, dc_title_iri), "")
644	    for obj_nt in value_to_nt_obj(cho.get("title"), sani_ctr):
645	        lines.append(make_nq(cho_nt, f"<{dc_title_iri}>", obj_nt, graph_iri))
646	        _track(dc_title_iri)
647	        if title_prop and title_prop != dc_title_iri:
648	            lines.append(make_nq(cho_nt, f"<{title_prop}>", obj_nt, graph_iri))
649	            _track(title_prop)
650	
651	    # ── Generic property loop ─────────────────────────────────────────────────
652	    dc_date_iri   = "http://purl.org/dc/elements/1.1/date"
653	    dcterms_iss   = "http://purl.org/dc/terms/issued"
654	    dcterms_ipart = "http://purl.org/dc/terms/isPartOf"
655	    _special_keys = frozenset({"creator", "contributor", "title"}) | SUBJECT_KEYS | _MOCHO_SKIP
656	
657	    subject_vals: list = []
658	    for skey in SUBJECT_KEYS:
659	        subject_vals.extend(coerce_list(cho.get(skey)))
660	    hastype_vals: list = coerce_list(cho.get("hasType"))
661	
662	    for prop, val in cho.items():
663	        if prop in _special_keys:
664	            continue
665	        prop_iri = _DDBEDM_PROP.get(prop)
666	        if not prop_iri:
667	            continue
668	        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
669	        if not target_prop:
670	            continue
671	
672	        if prop_iri in (dc_date_iri, dcterms_iss):
673	            # Date normalisation (D15 / props-mapping §3.1)
674	            for v in coerce_list(val):
675	                raw = (v if isinstance(v, str) else
676	                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
677	                for normed in normalize_date(raw):
678	                    if normed:
679	                        lines.append(make_nq(cho_nt, f"<{target_prop}>",
680	                                             f'"{_escape_literal(normed)}"', graph_iri))
681	                        _track(target_prop)
682	            continue
683	
684	        if prop_iri == dcterms_ipart:
685	            # isPartOf URI sanitisation (props-mapping §3.1)
686	            for obj_nt in value_to_nt_obj(val, sani_ctr):
687	                if not obj_nt.startswith("<"):
688	                    continue  # literal isPartOf skipped in mocho graph
689	                uri = obj_nt[1:-1]
690	                if not uri.startswith("http"):
691	                    if len(uri) == 32:
692	                        uri = DDB_ITEM_BASE + uri
693	                    else:
694	                        continue
695	                lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{uri}>", graph_iri))
696	                _track(target_prop)
697	            continue
698	
699	        for obj_nt in value_to_nt_obj(val, sani_ctr):
700	            lines.append(make_nq(cho_nt, f"<{target_prop}>",
701	                                 expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))
702	            _track(target_prop)
703	
704	    # ── Special handlers ──────────────────────────────────────────────────────
705	    _creator_lines = emit_creator_triples(
706	        cho_nt, cho.get("creator"), agents_index, target_class, class_prop_align, graph_iri,
707	    )
708	    lines.extend(_creator_lines)
709	    _track_nqlist(_creator_lines)
710	
711	    _contrib_lines = emit_contributor_triples(
712	        cho_nt, cho.get("contributor"),
713	        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,
714	    )
715	    lines.extend(_contrib_lines)
716	    _track_nqlist(_contrib_lines)
717	
718	    if subject_vals:
719	        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri,
720	                                              bare_id_to_uri)
721	        lines.extend(_subject_lines)
722	        _track_nqlist(_subject_lines)
723	
724	    if hastype_vals:
725	        _hastype_lines = emit_hastype_triples(cho_nt, hastype_vals, concepts_index, graph_iri,
726	                                              bare_id_to_uri)
727	        lines.extend(_hastype_lines)
728	        _track_nqlist(_hastype_lines)
729	
730	    # ── Aggregation & Place ───────────────────────────────────────────────────
731	    agg = rdf.get("Aggregation") or {}
732	    if isinstance(agg, list):
733	        agg = agg[0] if agg else {}
734	    _agg_lines = emit_aggregation_triples(agg, cho_nt, graph_iri)
735	    lines.extend(_agg_lines)
736	    _track_nqlist(_agg_lines)
737	
738	    _place_lines = emit_place_stubs(rdf.get("Place"), graph_iri)
739	    lines.extend(_place_lines)
740	    _track_nqlist(_place_lines)
741	
742	    dispatch_flags["preds_all"]     = preds_all
743	    dispatch_flags["preds_new"]     = preds_new
744	    dispatch_flags["uri_sanitized"] = sani_ctr["uri_sanitized"]
745	    dispatch_flags["uri_split"]     = sani_ctr["uri_split"]
746	    return lines, target_class, wemi, dispatch_flags
747	
```

---

### User *(2026-05-07T12:17:19.107Z)*

[Request interrupted by user]

---

### User *(2026-05-07T12:17:49.874Z)*

please check all emitters that URIs are checked:

1. literals are proper 
- escaped properly, '\n' will not cause carriage return in .nt/.nq)
- <br> are handled.

2. uris are correct
- when multiple https:blah blah http:// bleh bleh in one value are split. emit 2 triples (s, p, https1) and (s, p, http)

3. bare DDB ids are changed into urn:<json key>:ID

---

### Assistant *(2026-05-07T12:21:19.789Z)*

Let me read the full files before making changes.

---

### Assistant *(2026-05-07T12:21:19.791Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "limit": 80,
  "offset": 380
}
```

---

### User *(2026-05-07T12:21:19.811Z)*

**Tool result**
```
380	    for val in coerce_list(creator_vals):
381	        if not isinstance(val, dict):
382	            continue
383	        resource = (val.get("resource") or "").strip()
384	        label    = (val.get("$")        or "").strip()
385	        lang     = (val.get("lang")     or "").strip()
386	
387	        # Track 1: class-specific predicate (always runs when target_prop is known)
388	        if track1_prop:
389	            if resource:
390	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
391	            elif label:
392	                escaped = _escape_literal(label)
393	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
394	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", obj_nt, graph_iri))
395	
396	        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)
397	        agent = resolve_agent(label, resource, agents_index)
398	        if agent:
399	            agent_uri = (agent.get("about") or "").strip()
400	            if agent_uri and is_ddb_or_gnd(agent_uri):
401	                lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>",
402	                                     f"<{agent_uri}>", graph_iri))
403	                agent_nt = f"<{agent_uri}>"
404	                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
405	                pref = agent.get("prefLabel") or label
406	                if pref and isinstance(pref, str):
407	                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>",
408	                                         f'"{_escape_literal(pref)}"', graph_iri))
409	    return lines
410	
411	
412	def emit_contributor_triples(
413	    cho_nt: str,
414	    contributor_vals: list,
415	    event_participant_index: dict[str, str],
416	    lido_dispatch: dict[str, dict],
417	    target_class: str,
418	    wemi: str,
419	    graph_iri: str,
420	) -> NQList:
421	    """Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5)."""
422	    lines: NQList = []
423	    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), "dc_agent_fallback")
424	
425	    for val in coerce_list(contributor_vals):
426	        if not isinstance(val, dict):
427	            continue
428	        resource = (val.get("resource") or "").strip()
429	        label    = (val.get("$")        or "").strip()
430	        lang     = (val.get("lang")     or "").strip()
431	
432	        lido_type   = event_participant_index.get(resource) if resource else None
433	        lido_row    = lido_dispatch.get(lido_type) if lido_type else None
434	        target_prop = (
435	            (lido_row.get(prop_col) or lido_row.get("dc_agent_fallback") or DC_CONTRIBUTOR)
436	            if lido_row else DC_CONTRIBUTOR
437	        )
438	
439	        if resource:
440	            lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
441	            agent_nt = f"<{_sanitize_iri(resource)}>"
442	            lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
443	            if label:
444	                escaped = _escape_literal(label)
445	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
446	                lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
447	        elif label:
448	            escaped = _escape_literal(label)
449	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
450	            lines.append(make_nq(cho_nt, f"<{DC_CONTRIBUTOR}>", obj_nt, graph_iri))
451	    return lines
452	
453	
454	def emit_aggregation_triples(agg: dict, cho_nt: str, graph_iri: str) -> NQList:
455	    """Emit mocho triples derived from the Aggregation block (D23)."""
456	    lines: NQList = []
457	    _edm_dp     = EDM_NS + "dataProvider"
458	    _org_prefix = "http://www.deutsche-digitale-bibliothek.de/organization/"
459	
```

---

### User *(2026-05-07T12:23:22.577Z)*

This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. Primary Request and Intent:

The session covers a series of bug fixes, features, and documentation updates to the `goethe-faust/scripts/transform/` package (the EDM→mocho N-Quads transform pipeline for the GeMeA project). The final (interrupted) request is a comprehensive emitter audit for three categories of issues:

1. **Literal safety**: `<br>` tags not normalized; `\n` must be escaped to `\\n` in N-Triples
2. **Multi-URI splitting**: space-separated URIs in a single `resource` field must produce separate triples
3. **Bare DDB ID expansion**: bare 32-char IDs in property object positions must be expanded to proper URNs

---

2. Key Technical Concepts:

- **N-Quads / N-Triples format**: literals must have `\n`, `\r`, `\t`, `"`, `\\` escaped; IRIs must not contain spaces or control characters
- **DDB EDM JSONL**: source format; entity fields use `{"resource": "URI", "$": "label", "lang": "de"}` shape; `resource` field can contain multiple space-separated URIs (data quality issue)
- **Bare 32-char DDB IDs**: appear in `about` and resource fields when DDB omits the base URI prefix; must be expanded via `mint_bare_id(entity_class, id)`
- **`_MOCHO_SKIP`**: frozenset of JSON keys excluded from `emit_mocho_triples` generic property loop (handled specially or dropped)
- **`build_bare_id_index(rdf)`**: builds per-record `{bare_id → expanded_uri}` map from all entity `about` fields
- **`expand_obj_nt(obj_nt, bare_id_to_uri)`**: post-processes IRI-wrapped bare IDs in object position
- **`value_to_nt_obj`**: central utility; already does `.split()` on resource values for multi-URI; already calls `_escape_literal`; does NOT handle `<br>` tags
- **`_escape_literal`**: escapes `\\`, `"`, `\n`, `\r`, `\t`; does NOT handle `<br>` HTML tags
- **`emit_subject_triples`**, **`emit_hastype_triples`**: special-case emitters that extract `resource` manually (bypassing `value_to_nt_obj`) — currently missing multi-URI split and bare-ID expansion
- **`emit_creator_triples`**, **`emit_contributor_triples`**: also extract `resource` manually — same gaps
- **`vocnet-htype:`**: `http://ddb.vocnet.org/hierarchietyp/` — namespace for htype IRI objects
- **`ddbedm:`**: `http://www.deutsche-digitale-bibliothek.de/edm/` — namespace for DDB EDM extension properties

---

3. Files and Code Sections:

**`goethe-faust/scripts/transform/utils.py`**
- Added `build_bare_id_index` and `expand_obj_nt`
- `_escape_literal` currently handles `\\`, `"`, `\n`, `\r`, `\t` but NOT `<br>` tags (pending fix)
- `value_to_nt_obj` already splits multi-URI via `.split()` in the `{"resource": ...}` dict branch

Current `_escape_literal`:
```python
def _escape_literal(s: str) -> str:
    return (s.replace("\\", "\\\\")
             .replace('"', '\\"')
             .replace("\n", "\\n")
             .replace("\r", "\\r")
             .replace("\t", "\\t"))
```
Missing: `<br>` → `\n` normalization before the chain.

**`goethe-faust/scripts/transform/constants.py`**
- Added `DDBEDM_NS = "http://www.deutsche-digitale-bibliothek.de/edm/"`
- Added `DDB_HIERARCHY_TYPE = DDBEDM_NS + "hierarchyType"`
- Added `_HTYPE_PREFIX = "http://ddb.vocnet.org/hierarchietyp/"`
- Added `EDM_HAS_TYPE = EDM_NS + "hasType"`
- Fixed `_DDBEDM_PROP["hierarchyType"]` from wrong `"http://www.deutsche-digitale-bibliothek.de/hierarchyType"` to `DDBEDM_NS + "hierarchyType"`
- Added `"ddbedm": DDBEDM_NS` and `"vocnet-htype": _HTYPE_PREFIX` to `_PREFIXES`
- Current `_MOCHO_SKIP`:
```python
_MOCHO_SKIP = frozenset({
    "about", "hierarchyType",
    "creator", "contributor",
    "dcSubject", "dcTermsSubject", "dcTermSubject",
    "dcType",
    "aggregationEntity", "hierarchyPosition",
    "hasMet",     # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph
    "hasType",    # handled by emit_hastype_triples(); needs bare-ID expansion + label stub
})
```

**`goethe-faust/scripts/transform/emitters.py`**

Key issues identified in audit (not yet fixed):

`emit_subject_triples` — resource not split:
```python
resource = (val.get("resource") or "").strip()
# BUG: if resource = "URI1 URI2", treated as one URI
if resource:
    expanded = _bare.get(resource) or mint_bare_id("Concept", resource)
    ...
    lines.append(make_nq(cho_nt, f"<{DCTERMS_SUBJECT}>", f"<{expanded_safe}>", graph_iri))
```

`emit_hastype_triples` — same pattern, same bug.

`emit_creator_triples` — no split, no bare ID expansion, `agent_uri` not sanitized:
```python
resource = (val.get("resource") or "").strip()
if track1_prop:
    if resource:
        # BUG: no split, no bare ID expansion
        lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
# Track 2: agent_uri not sanitized
agent_uri = (agent.get("about") or "").strip()
if agent_uri and is_ddb_or_gnd(agent_uri):
    lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>", f"<{agent_uri}>", graph_iri))  # BUG: no _sanitize_iri
```

`emit_contributor_triples` — no split, no bare ID expansion:
```python
resource = (val.get("resource") or "").strip()
lido_type = event_participant_index.get(resource) if resource else None
# BUG: no split; lido_type lookup uses full unsplit string
if resource:
    lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
    # BUG: no split; resource may be "URI1 URI2"
```

`emit_prov_triples` — `provider_isil` not sanitized:
```python
if provider_isil:
    lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>", f"<{provider_isil}>", graph_iri))
    # BUG: missing _sanitize_iri(provider_isil)
```

`emit_place_stubs` — `raw_about` not split (space-separated would produce malformed URN):
```python
raw_about = (place.get("about") or "").strip()
place_uri = mint_bare_id("Place", raw_about)  # BUG: raw_about.split()[0] should be used
```

**`goethe-faust/scripts/transform/tests/test_transform.py`**
69 tests currently passing. Added test classes: `TestBuildBareIdIndex`, `TestExpandObjNt`, `TestEmitDdbedmBareIds`, `TestEmitSubjectTriplesBareId`, `TestEmitHastypeTriples`. Also `test_hasmet_in_mocho_skip`, `test_hastype_in_mocho_skip`.

**`goethe-faust/notes/transform-props-mapping-adr.md`**
Added D14 (hasMet skip) and D15 (ddbedm:hierarchyType emission).

---

4. Errors and fixes:

- **`test_hastype_in_mocho_skip` indentation bug**: function was accidentally indented inside `TestEmitHastypeTriples` class, causing pytest to inject `self` arg. Fixed by dedenting to module level.

- **`DDB_HIERARCHY_TYPE` derivation rejected**: First attempt used `DDB_BASE + "/hierarchyType"`. User rejected: "DDB_BASE is http://www.deutsche-digitale-bibliothek.de/edm/". Fixed by adding standalone `DDBEDM_NS` constant and deriving from it.

- **`hierarchyType` emitted as literal**: First attempt emitted `"htype_021"` as a string literal. User said "value should be vocnet-htype:ht0xx". Fixed by looking up base IRI `http://ddb.vocnet.org/hierarchietyp/` and emitting `<vocnet-htype:htype_021>` as an IRI object.

- **Edit not found error**: Attempted edit on `DDB_BASE           = ...` with extra spaces that didn't match the file. Fixed by using the actual spacing in the file.

---

5. Problem Solving:

- **Bare ID expansion**: Solved globally via `build_bare_id_index` + `expand_obj_nt` for the generic property loops; solved via `mint_bare_id("Concept", resource)` fallback for the special emitters (`emit_subject_triples`, `emit_hastype_triples`). Pending: apply to `emit_creator_triples`, `emit_contributor_triples`.

- **hasMet on mocho CHO**: Solved by adding to `_MOCHO_SKIP`.

- **hasType special handling**: Implemented `emit_hastype_triples` with IRI-only dispatch, bare-ID expansion, label stub from `concepts_index`, deduplication.

- **Pending audit**: Multi-URI split and `<br>` handling not yet fixed in the special emitters.

---

6. All user messages:

- "There are bugs in the transform scripts: 1. the urn:fix did not seem to be carried over [subject bare ID example] 2. why does gemea resource emit `edm:hasMet`? [hasMet example]"
- "the malformed URI exists everywhere: values of properties and 'about' or IDs of resources."
- "add a test for this."
- "where did the values of _MOCHO_SKIP_ come from?"
- "update retype_entities to also emit ddb:hierarchyType in the mocho graph."
- "[rejected edit] DDB_BASE is http://www.deutsche-digitale-bibliothek.de/edm/"
- "[rejected edit] maybe it should be called ddbedm:hierarchyType?"
- "2nd" (confirming IRI should be `http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType`)
- "[selected 'vocnet-htype:'] the value should vocnet-htype:ht0xx"
- "update transform-props-mapping.md to document handling of hasMet and ddbedm:hierarchyTyp"
- "are all the properties stated in the props-mapping as 'deferred' added to the MOCHO skip?"
- "[selected 'hasType'] we need special handling for hasType. this is equivalent to edm:hasType. special handling here. when the value is a proper URI, keep as is. then look for corresponding skos:Concept where it matches 'about', then emit 2 triples: 1. value is a valid Triple: `<cho> edm:hasType <valid URI>` + `<valid URI> rdfs:label <skos:prefLabel>`. 2. value is a 32-character internal DDB uuid: `<cho> edm:hasType <urn:Concept:<id>>` + label"
- "please check all emitters that URIs are checked: 1. literals are proper - escaped properly, '\n' will not cause carriage return in .nt/.nq) - <br> are handled. 2. uris are correct - when multiple https:blah blah http:// bleh bleh in one value are split. emit 2 triples (s, p, https1) and (s, p, http) 3. bare DDB ids are changed into urn:<json key>:ID"

---

7. Pending Tasks:

**Primary pending task** — Audit and fix all emitters for:

1. **`<br>` in literals** — add to `_escape_literal` in `utils.py`:
   - Add `_BR_RE = re.compile(r'<br\s*/?\s*>', re.IGNORECASE)`
   - Prepend `s = _BR_RE.sub('\n', s)` before the escape chain

2. **Multi-URI splitting** — fix in emitters that manually extract `resource`:
   - `emit_subject_triples`: loop over `resource.split()`, emit each part separately
   - `emit_hastype_triples`: same
   - `emit_creator_triples`: split resource for Track 1; use first part for Track 2 agent lookup
   - `emit_contributor_triples`: split resource; use first part for LIDO event lookup

3. **Bare ID expansion** — apply in emitters that bypass `expand_obj_nt`:
   - `emit_creator_triples`: add `bare_id_to_uri` param; expand each URI part
   - `emit_contributor_triples`: add `bare_id_to_uri` param; expand each URI part
   - `emit_mocho_triples`: pass `bare_id_to_uri` to both
   - `agent_uri` in Track 2 of `emit_creator_triples`: apply `_sanitize_iri`
   - `emit_place_stubs`: use `raw_about.split()[0]` instead of full `raw_about`
   - `emit_prov_triples`: apply `_sanitize_iri(provider_isil)`

4. **Add tests** for all new behaviors.

---

8. Current Work:

The conversation was interrupted mid-task. The user's request was:

> "please check all emitters that URIs are checked:
> 1. literals are proper - escaped properly, '\n' will not cause carriage return in .nt/.nq) - <br> are handled.
> 2. uris are correct - when multiple https:blah blah http:// bleh bleh in one value are split. emit 2 triples (s, p, https1) and (s, p, http)
> 3. bare DDB ids are changed into urn:<json key>:ID"

The assistant had just finished reading the full `utils.py` and `emitters.py` files (all 747 lines) to conduct the audit, and was about to begin making fixes. The reading revealed all the gaps listed in Pending Tasks above. No code changes had been made yet for this audit.

---

9. Optional Next Step:

The next step is to implement all fixes identified in the audit across `utils.py` and `emitters.py`, then update tests. Start with `_escape_literal` in `utils.py` (adding `<br>` normalization), then update `emit_subject_triples` and `emit_hastype_triples` to split `resource` on whitespace, then update `emit_creator_triples` and `emit_contributor_triples` to add `bare_id_to_uri` param and split `resource`.

Direct quote from the most recent user request establishing the task:
> "please check all emitters that URIs are checked: 1. literals are proper - escaped properly, '\n' will not cause carriage return in .nt/.nq) - <br> are handled. 2. uris are correct - when multiple https:blah blah http:// bleh bleh in one value are split. emit 2 triples (s, p, https1) and (s, p, http) 3. bare DDB ids are changed into urn:<json key>:ID"

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: /Users/mta/.claude/projects/-Users-mta-Documents-claude/ef8b247d-8555-42ed-bcfa-d0e1dab38211.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.

---

### Assistant *(2026-05-07T12:23:25.804Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py"
}
```

---

### User *(2026-05-07T12:23:25.807Z)*

**Tool result**
```
File unchanged since last read. The content from the earlier Read tool_result in this conversation is still current — refer to that instead of re-reading.
```

---

### Assistant *(2026-05-07T12:23:26.018Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py"
}
```

---

### User *(2026-05-07T12:23:26.308Z)*

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
26	    build_bare_id_index, expand_obj_nt,
27	)
28	
29	
30	def emit_ddbedm_triples(rdf: dict, graph_iri: str) -> tuple[NQList, Counter, Counter, Counter]:
31	    """Emit verbatim EDM passthrough triples for all entity types in rdf (§6.1).
32	
33	    Subject: first URI in entity['about']; owl:sameAs emitted for any additional URIs.
34	    Includes mt007 records.
35	    Returns (lines, class_ctr, pred_ctr, sani_ctr) where sani_ctr tracks
36	    uri_sanitized, uri_split, and uri_about_split counts.
37	    """
38	    lines:     NQList  = []
39	    class_ctr: Counter = Counter()
40	    pred_ctr:  Counter = Counter()
41	    sani_ctr:  Counter = Counter()
42	    _skip = frozenset({"about"})
43	    bare_id_to_uri = build_bare_id_index(rdf)
44	    for entity_type, entities in rdf.items():
45	        edm_class = _EDM_ENTITY_TYPES.get(entity_type)
46	        for entity in coerce_list(entities):
47	            if not isinstance(entity, dict):
48	                continue
49	            raw_about = (entity.get("about") or "").strip()
50	            if not raw_about:
51	                continue
52	            about_parts = raw_about.split()
53	            subj_uri = mint_bare_id(entity_type, _sanitize_iri(about_parts[0]))
54	            subj_nt  = f"<{subj_uri}>"
55	            if len(about_parts) > 1:
56	                sani_ctr["uri_about_split"] += len(about_parts) - 1
57	                for alt in about_parts[1:]:
58	                    lines.append(make_nq(subj_nt, f"<{OWL_SAMEAS}>",
59	                                         f"<{_sanitize_iri(alt)}>", graph_iri))
60	            if edm_class:
61	                lines.append(make_nq(subj_nt, f"<{RDF_TYPE}>", f"<{edm_class}>", graph_iri))
62	                class_ctr[_to_curie(edm_class)] += 1
63	            for key, val in entity.items():
64	                if key in _skip:
65	                    continue
66	                pred_iri = _DDBEDM_PROP.get(key)
67	                if not pred_iri:
68	                    continue
69	                pred_nt = f"<{pred_iri}>"
70	                curie   = _to_curie(pred_iri)
71	                for obj_nt in value_to_nt_obj(val, sani_ctr):
72	                    lines.append(make_nq(subj_nt, pred_nt,
73	                                         expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))
74	                    pred_ctr[curie] += 1
75	    return lines, class_ctr, pred_ctr, sani_ctr
76	
77	
78	def emit_prov_triples(record: dict, ddb_cho_uri: str, graph_iri: str) -> NQList:
79	    """Emit PROV-O Layer 1 (Without-Activity) for one record (§6.2, ddbedm-prov-o-plan.md §2)."""
80	    lines: NQList = []
81	    props = record.get("properties") or {}
82	    prov  = record.get("provider-info") or {}
83	
84	    item_id         = (props.get("item-id")         or "").strip()
85	    dataset_id      = (props.get("dataset-id")      or "").strip()
86	    dataset_label   = (props.get("dataset-label")   or "").strip()
87	    revision        = (props.get("revision-id")     or "").strip()
88	    ingest_dt       = (props.get("ingest-date")     or "").strip()
89	    map_ver         = (props.get("mapping-version") or "").strip()
90	    provider_ddb_id = (prov.get("provider-ddb-id")  or "").strip()
91	    provider_name   = (prov.get("provider-name")    or "").strip()
92	    provider_uri    = (prov.get("provider-uri")     or "").strip()
93	    provider_id     = (prov.get("provider-id")      or "").strip()
94	    provider_isil   = (prov.get("provider-isil")    or "").strip()
95	
96	    src_desc  = (record.get("source") or {}).get("description") or {}
97	    src_ref   = (src_desc.get("record") or {}) if isinstance(src_desc, dict) else {}
98	    ref_val   = (src_ref.get("ref",  "") or "").strip() if isinstance(src_ref, dict) else ""
99	    src_href  = (src_ref.get("href", "") or "").strip() if isinstance(src_ref, dict) else ""
100	    rec_type  = (src_ref.get("type", "") or "").strip() if isinstance(src_ref, dict) else ""
101	
102	    ds_uri   = f"urn:ddbedm:properties:dataset-id:{dataset_id}"      if dataset_id      else ""
103	    xslt_uri = f"urn:ddbedm:properties:mapping-version:{map_ver}"    if map_ver         else ""
104	    prov_uri = f"urn:ddbedm:provider-info:provider-ddb-id:{provider_ddb_id}" \
105	               if provider_ddb_id else ""
106	
107	    # ── CHO node ──────────────────────────────────────────────────────────────
108	    cho_nt = f"<{ddb_cho_uri}>"
109	    lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
110	    if ds_uri:
111	        lines.append(make_nq(cho_nt, f"<{PROV_DERIVED}>",   f"<{ds_uri}>",   graph_iri))
112	    if xslt_uri:
113	        lines.append(make_nq(cho_nt, f"<{PROV_ATTRIBUTED}>", f"<{xslt_uri}>", graph_iri))
114	    if ingest_dt:
115	        lines.append(make_nq(cho_nt, f"<{PROV_GEN_TIME}>",
116	                             f'"{_escape_literal(ingest_dt)}"^^<{XSD_DATETIME}>', graph_iri))
117	    if revision:
118	        lines.append(make_nq(cho_nt, f"<{DCTERMS_HAS_VER}>",
119	                             f'"{_escape_literal(revision)}"', graph_iri))
120	    if ref_val:
121	        lines.append(make_nq(cho_nt, f"<{DCTERMS_REF}>",
122	                             f'"ddb:{_escape_literal(ref_val)}"', graph_iri))
123	
124	    # ── Dataset node ──────────────────────────────────────────────────────────
125	    if ds_uri:
126	        ds_nt = f"<{ds_uri}>"
127	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{DCAT_DATASET}>", graph_iri))
128	        lines.append(make_nq(ds_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>",  graph_iri))
129	        lines.append(make_nq(ds_nt, f"<{DCTERMS_ID}>",
130	                             f'"{_escape_literal(dataset_id)}"', graph_iri))
131	        if dataset_label:
132	            lines.append(make_nq(ds_nt, f"<{RDFS_LABEL}>",
133	                                 f'"{_escape_literal(dataset_label)}"@de', graph_iri))
134	        if rec_type:
135	            lines.append(make_nq(ds_nt, f"<{DCTERMS_TYPE}>", f"<{rec_type}>", graph_iri))
136	        if prov_uri:
137	            lines.append(make_nq(ds_nt, f"<{PROV_ATTRIBUTED}>",
138	                                 f"<{prov_uri}>", graph_iri))
139	
140	    # ── XSLT SoftwareAgent node ───────────────────────────────────────────────
141	    if xslt_uri:
142	        xslt_nt = f"<{xslt_uri}>"
143	        lines.append(make_nq(xslt_nt, f"<{RDF_TYPE}>", f"<{PROV_SW_AGENT}>", graph_iri))
144	        lines.append(make_nq(xslt_nt, f"<{DCTERMS_HAS_VER}>",
145	                             f'"{_escape_literal(map_ver)}"', graph_iri))
146	        lines.append(make_nq(xslt_nt, f"<{PROV_ON_BEHALF}>", f"<{DDB_BASE}>", graph_iri))
147	
148	    # ── DDB Agent node (fixed URI) ────────────────────────────────────────────
149	    ddb_nt = f"<{DDB_BASE}>"
150	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
151	    lines.append(make_nq(ddb_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
152	    lines.append(make_nq(ddb_nt, f"<{FOAF_NAME}>",
153	                         '"Deutsche Digitale Bibliothek"', graph_iri))
154	
155	    # ── Provider Agent node ───────────────────────────────────────────────────
156	    if prov_uri:
157	        prov_nt = f"<{prov_uri}>"
158	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{PROV_AGENT}>", graph_iri))
159	        lines.append(make_nq(prov_nt, f"<{RDF_TYPE}>", f"<{FOAF_ORG}>",   graph_iri))
160	        if provider_name:
161	            lines.append(make_nq(prov_nt, f"<{FOAF_NAME}>",
162	                                 f'"{_escape_literal(provider_name)}"', graph_iri))
163	        if provider_uri:
164	            lines.append(make_nq(prov_nt, f"<{SCHEMA_URL}>", f"<{provider_uri}>", graph_iri))
165	        if provider_id:
166	            lines.append(make_nq(prov_nt, f"<{DCTERMS_ID}>",
167	                                 f'"{_escape_literal(provider_id)}"', graph_iri))
168	        if provider_isil:
169	            lines.append(make_nq(prov_nt, f"<{MOCHO_ISIL}>", f"<{provider_isil}>", graph_iri))
170	
171	    # ── SourceRecord node (one per binary entry under same URI) ───────────────
172	    if src_href:
173	        src_rec_uri = DDB_API_BASE + src_href.lstrip("/")
174	        src_nt      = f"<{src_rec_uri}>"
175	        lines.append(make_nq(src_nt, f"<{RDF_TYPE}>", f"<{PROV_ENTITY}>", graph_iri))
176	        for binary in coerce_list((record.get("binaries") or {}).get("binary")):
177	            if not isinstance(binary, dict):
178	                continue
179	            ref   = (binary.get("ref")            or "").strip()
180	            name  = (binary.get("name")           or "").strip()
181	            name2 = (binary.get("name2")          or "").strip()
182	            kind  = (binary.get("kind")           or "").strip()
183	            lpath = (binary.get("local_pathname") or "").strip()
184	            if ref:
185	                lines.append(make_nq(src_nt, f"<{DC_ID}>",
186	                                     f'"{_escape_literal(ref)}"', graph_iri))
187	            if name:
188	                lines.append(make_nq(src_nt, f"<{DC_TITLE}>",
189	                                     f'"{_escape_literal(name)}"@de', graph_iri))
190	            desc = (name2 + " | " + name) if name2 and name else (name2 or name)
191	            if desc:
192	                lines.append(make_nq(src_nt, f"<{DC_DESCRIPTION}>",
193	                                     f'"{_escape_literal(desc)}"@de', graph_iri))
194	            if kind:
195	                lines.append(make_nq(src_nt, f"<{DCTERMS_RIGHTS}>", f"<{kind}>", graph_iri))
196	            if lpath and lpath.startswith("http"):
197	                lines.append(make_nq(src_nt, f"<{DCTERMS_SOURCE}>", f"<{lpath}>", graph_iri))
198	
199	    return lines
200	
201	
202	def retype_entities(
203	    sector: str,
204	    mediatype: str,
205	    htype_code: str | None,
206	    dctype_vals: list,
207	    cho_nt: str,
208	    mediatype_class_map: dict,
209	    htype_map: dict,
210	    audio_type2class: dict,
211	    graph_iri: str,
212	) -> tuple[NQList, str, str, dict]:
213	    """Dispatch rdf:type triples for a ProvidedCHO (§6.4, transform-revised-plan.md §1.1).
214	
215	    Returns (lines, target_class_full_iri, wemi, dispatch_flags).
216	    target_class is used for property alignment lookup; wemi for contributor column selection.
217	    dispatch_flags: {"htype_used": bool, "fallback": bool}
218	    """
219	    lines: NQList = []
220	    row = (
221	        mediatype_class_map.get((sector, mediatype))
222	        or mediatype_class_map.get(("any", "any"))
223	        or {}
224	    )
225	    use_htype  = row.get("use_htype", False)
226	    rdf_type_w = row.get("rdf_type_w", "")
227	    rdf_type_m = row.get("rdf_type_m", "")
228	
229	    primary_class = ""
230	    htype_used    = False
231	
232	    # Layer 1: htype-derived class (for htype-first strata)
233	    if use_htype and htype_code:
234	        entry = htype_map.get(htype_code)
235	        if entry:
236	            type_iris, rst_iris = entry
237	            for t in type_iris:
238	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{t}>", graph_iri))
239	            for r in rst_iris:
240	                lines.append(make_nq(cho_nt, f"<{RICO_HAS_RST}>", f"<{r}>", graph_iri))
241	            primary_class = type_iris[0]  # first = most specific
242	            htype_used    = True
243	
244	    # Layer 2: fixed mediatype class (always emit if set; added on top of layer 1)
245	    if rdf_type_w:
246	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_w}>", graph_iri))
247	        if not primary_class:
248	            primary_class = rdf_type_w
249	    if rdf_type_m:
250	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{rdf_type_m}>", graph_iri))
251	        if not primary_class:
252	            primary_class = rdf_type_m
253	
254	    # Audio group dispatch: dc:type → mo:MusicalManifestation (Group A) (§2.3)
255	    _aco_audio = "https://w3id.org/ac-ontology/aco#AudioManifestation"
256	    _mo_mani   = "http://purl.org/ontology/mo/MusicalManifestation"
257	    if rdf_type_m == _aco_audio and dctype_vals and not use_htype:
258	        for dct in dctype_vals:
259	            dc_text = (dct.get("$") or "").strip() if isinstance(dct, dict) else ""
260	            if audio_type2class.get((sector, dc_text)) == "A":
261	                lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{_mo_mani}>", graph_iri))
262	                primary_class = _mo_mani
263	                break
264	
265	    # D9 fallback — no class resolved
266	    is_fallback = not primary_class
267	    if is_fallback:
268	        fallback = MOCHO_NS + "Manifestation"
269	        lines.append(make_nq(cho_nt, f"<{RDF_TYPE}>", f"<{fallback}>", graph_iri))
270	        primary_class = fallback
271	
272	    if htype_code:
273	        lines.append(make_nq(cho_nt, f"<{DDB_HIERARCHY_TYPE}>",
274	                             f"<{_HTYPE_PREFIX}{htype_code}>", graph_iri))
275	
276	    wemi = _CLASS_WEMI.get(primary_class, "M")
277	    return lines, primary_class, wemi, {"htype_used": htype_used, "fallback": is_fallback}
278	
279	
280	def emit_subject_triples(
281	    cho_nt: str,
282	    subject_vals: list,
283	    concepts_index: dict[str, dict],
284	    graph_iri: str,
285	    bare_id_to_uri: dict[str, str] | None = None,
286	) -> NQList:
287	    """Emit dcterms:subject (IRI path) or dc:subject (literal path) per value (D1 amended)."""
288	    lines: NQList = []
289	    seen: set[str] = set()
290	    _bare = bare_id_to_uri or {}
291	    for val in subject_vals:
292	        if not isinstance(val, dict):
293	            continue
294	        resource = (val.get("resource") or "").strip()
295	        label    = (val.get("$")        or "").strip()
296	        lang     = (val.get("lang")     or "").strip()
297	        if resource:
298	            # Expand bare IDs: look up in the per-record index, fall back to Concept mint
299	            if not resource.startswith(("http", "urn")):
300	                expanded = _bare.get(resource) or mint_bare_id("Concept", resource)
301	            else:
302	                expanded = resource
303	            expanded_safe = _sanitize_iri(expanded)
304	            if expanded_safe in seen:
305	                continue
306	            seen.add(expanded_safe)
307	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SUBJECT}>", f"<{expanded_safe}>", graph_iri))
308	            concept = concepts_index.get(resource) or concepts_index.get(expanded)
309	            if concept:
310	                for pl in coerce_list(concept.get("prefLabel")):
311	                    for obj_nt in value_to_nt_obj(pl):
312	                        lines.append(make_nq(f"<{expanded_safe}>", f"<{RDFS_LABEL}>",
313	                                             obj_nt, graph_iri))
314	        elif label:
315	            key = f"lit:{label}"
316	            if key in seen:
317	                continue
318	            seen.add(key)
319	            escaped = _escape_literal(label)
320	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
321	            lines.append(make_nq(cho_nt, f"<{DC_SUBJECT}>", obj_nt, graph_iri))
322	    return lines
323	
324	
325	def emit_hastype_triples(
326	    cho_nt: str,
327	    hastype_vals: list,
328	    concepts_index: dict[str, dict],
329	    graph_iri: str,
330	    bare_id_to_uri: dict[str, str] | None = None,
331	) -> NQList:
332	    """Emit edm:hasType + rdfs:label stub for each IRI-valued hasType entry.
333	
334	    Bare 32-char IDs are expanded via the per-record index (fallback: mint as Concept URN).
335	    Literal-only values (no resource) are silently skipped — edm:hasType range is skos:Concept.
336	    """
337	    lines: NQList = []
338	    seen: set[str] = set()
339	    _bare = bare_id_to_uri or {}
340	    for val in coerce_list(hastype_vals):
341	        if not isinstance(val, dict):
342	            continue
343	        resource = (val.get("resource") or "").strip()
344	        if not resource:
345	            continue
346	        if not resource.startswith(("http", "urn")):
347	            expanded = _bare.get(resource) or mint_bare_id("Concept", resource)
348	        else:
349	            expanded = resource
350	        expanded_safe = _sanitize_iri(expanded)
351	        if expanded_safe in seen:
352	            continue
353	        seen.add(expanded_safe)
354	        lines.append(make_nq(cho_nt, f"<{EDM_HAS_TYPE}>", f"<{expanded_safe}>", graph_iri))
355	        concept = concepts_index.get(resource) or concepts_index.get(expanded)
356	        if concept:
357	            for pl in coerce_list(concept.get("prefLabel")):
358	                for obj_nt in value_to_nt_obj(pl):
359	                    lines.append(make_nq(f"<{expanded_safe}>", f"<{RDFS_LABEL}>",
360	                                         obj_nt, graph_iri))
361	    return lines
362	
363	
364	def emit_creator_triples(
365	    cho_nt: str,
366	    creator_vals: list,
367	    agents_index: dict[str, AgentDict],
368	    target_class: str,
369	    class_prop_align: PropAlign,
370	    graph_iri: str,
371	) -> NQList:
372	    """Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).
373	
374	    Both tracks run independently for each creator value (D2 / props-mapping §4).
375	    """
376	    lines: NQList = []
377	    dc_creator_iri = "http://purl.org/dc/elements/1.1/creator"
378	    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), "")
379	
380	    for val in coerce_list(creator_vals):
381	        if not isinstance(val, dict):
382	            continue
383	        resource = (val.get("resource") or "").strip()
384	        label    = (val.get("$")        or "").strip()
385	        lang     = (val.get("lang")     or "").strip()
386	
387	        # Track 1: class-specific predicate (always runs when target_prop is known)
388	        if track1_prop:
389	            if resource:
390	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
391	            elif label:
392	                escaped = _escape_literal(label)
393	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
394	                lines.append(make_nq(cho_nt, f"<{track1_prop}>", obj_nt, graph_iri))
395	
396	        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)
397	        agent = resolve_agent(label, resource, agents_index)
398	        if agent:
399	            agent_uri = (agent.get("about") or "").strip()
400	            if agent_uri and is_ddb_or_gnd(agent_uri):
401	                lines.append(make_nq(cho_nt, f"<{DCTERMS_CREATOR}>",
402	                                     f"<{agent_uri}>", graph_iri))
403	                agent_nt = f"<{agent_uri}>"
404	                lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
405	                pref = agent.get("prefLabel") or label
406	                if pref and isinstance(pref, str):
407	                    lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>",
408	                                         f'"{_escape_literal(pref)}"', graph_iri))
409	    return lines
410	
411	
412	def emit_contributor_triples(
413	    cho_nt: str,
414	    contributor_vals: list,
415	    event_participant_index: dict[str, str],
416	    lido_dispatch: dict[str, dict],
417	    target_class: str,
418	    wemi: str,
419	    graph_iri: str,
420	) -> NQList:
421	    """Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5)."""
422	    lines: NQList = []
423	    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), "dc_agent_fallback")
424	
425	    for val in coerce_list(contributor_vals):
426	        if not isinstance(val, dict):
427	            continue
428	        resource = (val.get("resource") or "").strip()
429	        label    = (val.get("$")        or "").strip()
430	        lang     = (val.get("lang")     or "").strip()
431	
432	        lido_type   = event_participant_index.get(resource) if resource else None
433	        lido_row    = lido_dispatch.get(lido_type) if lido_type else None
434	        target_prop = (
435	            (lido_row.get(prop_col) or lido_row.get("dc_agent_fallback") or DC_CONTRIBUTOR)
436	            if lido_row else DC_CONTRIBUTOR
437	        )
438	
439	        if resource:
440	            lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{_sanitize_iri(resource)}>", graph_iri))
441	            agent_nt = f"<{_sanitize_iri(resource)}>"
442	            lines.append(make_nq(agent_nt, f"<{RDF_TYPE}>", f"<{MOCHO_AGENT}>", graph_iri))
443	            if label:
444	                escaped = _escape_literal(label)
445	                obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
446	                lines.append(make_nq(agent_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
447	        elif label:
448	            escaped = _escape_literal(label)
449	            obj_nt  = f'"{escaped}"@{lang}' if lang else f'"{escaped}"'
450	            lines.append(make_nq(cho_nt, f"<{DC_CONTRIBUTOR}>", obj_nt, graph_iri))
451	    return lines
452	
453	
454	def emit_aggregation_triples(agg: dict, cho_nt: str, graph_iri: str) -> NQList:
455	    """Emit mocho triples derived from the Aggregation block (D23)."""
456	    lines: NQList = []
457	    _edm_dp     = EDM_NS + "dataProvider"
458	    _org_prefix = "http://www.deutsche-digitale-bibliothek.de/organization/"
459	
460	    is_shown = agg.get("isShownAt") or {}
461	    if isinstance(is_shown, dict):
462	        uri = (is_shown.get("resource") or "").strip()
463	        if uri:
464	            lines.append(make_nq(cho_nt, f"<{DCTERMS_SOURCE}>", f"<{_sanitize_iri(uri)}>", graph_iri))
465	
466	    for dp in coerce_list(agg.get("dataProvider")):
467	        if not isinstance(dp, dict):
468	            continue
469	        uri = (dp.get("resource") or "").strip()
470	        if uri and uri.startswith(_org_prefix):
471	            lines.append(make_nq(cho_nt, f"<{_edm_dp}>", f"<{_sanitize_iri(uri)}>", graph_iri))
472	
473	    for obj in coerce_list(agg.get("object")):
474	        if not isinstance(obj, dict):
475	            continue
476	        uri = (obj.get("resource") or "").strip()
477	        if uri:
478	            lines.append(make_nq(cho_nt, f"<{FOAF_THUMBNAIL}>", f"<{_sanitize_iri(uri)}>", graph_iri))
479	
480	    return lines
481	
482	
483	def emit_place_stubs(places: object, graph_iri: str) -> NQList:
484	    """Emit rdfs:label stubs for each Place entity referenced by the record (D24)."""
485	    lines: NQList = []
486	    for place in coerce_list(places):
487	        if not isinstance(place, dict):
488	            continue
489	        raw_about = (place.get("about") or "").strip()
490	        if not raw_about:
491	            continue
492	        place_uri = mint_bare_id("Place", raw_about)
493	        place_nt  = f"<{place_uri}>"
494	        for lbl in coerce_list(place.get("prefLabel")):
495	            for obj_nt in value_to_nt_obj(lbl):
496	                lines.append(make_nq(place_nt, f"<{RDFS_LABEL}>", obj_nt, graph_iri))
497	    return lines
498	
499	
500	def werk_staging_row(cho_uri: str, cho: dict, target_class: str) -> dict | None:
501	    """Build a werk_staging dict if target_class is a W-slot class (D26). Else None."""
502	    if target_class not in _W_SLOT_CLASSES:
503	        return None
504	
505	    title = ""
506	    tv = cho.get("title")
507	    if isinstance(tv, dict):
508	        title = (tv.get("$") or "").strip()
509	    elif isinstance(tv, list) and tv:
510	        first = tv[0]
511	        title = (first.get("$") or "").strip() if isinstance(first, dict) else ""
512	
513	    dc_alt: list[str] = []
514	    for v in coerce_list(cho.get("alternative")):
515	        t = (v.get("$") or "").strip() if isinstance(v, dict) else ""
516	        if t:
517	            dc_alt.append(t)
518	
519	    dc_created = ""
520	    for v in coerce_list(cho.get("date")):
521	        t = (v if isinstance(v, str) else "").strip()
522	        if t:
523	            dc_created = t
524	            break
525	
526	    creator_uris: list[str] = []
527	    creator_lits: list[str] = []
528	    for v in coerce_list(cho.get("creator")):
529	        if not isinstance(v, dict):
530	            continue
531	        uri = (v.get("resource") or "").strip()
532	        lit = (v.get("$")        or "").strip()
533	        if uri:
534	            creator_uris.append(uri)
535	        elif lit:
536	            creator_lits.append(lit)
537	
538	    obj_id = cho_uri.rsplit("/", 1)[-1]
539	    return {
540	        "ddb_obj_id":       obj_id,
541	        "cho_uri":          cho_uri,
542	        "target_class":     target_class,
543	        "dc_title":         title,
544	        "dc_alternative":   dc_alt,
545	        "dc_created":       dc_created,
546	        "creator_uris":     creator_uris,
547	        "creator_literals": creator_lits,
548	    }
549	
550	
551	def emit_mocho_triples(
552	    rdf: dict,
553	    cho_uri: str,
554	    ddb_uri: str,
555	    sector: str,
556	    mediatype: str,
557	    mediatype_class_map: dict,
558	    htype_map: dict,
559	    audio_type2class: dict,
560	    class_prop_align: PropAlign,
561	    lido_dispatch: dict,
562	    graph_iri: str,
563	) -> tuple[NQList, str, str, dict]:
564	    """Emit all mocho-graph triples for one record (§6.3). Returns (lines, target_class, wemi, dispatch_flags).
565	
566	    dispatch_flags includes "preds_all" and "preds_new" Counters (CURIEs) built during emission.
567	    """
568	    lines:     NQList  = []
569	    preds_all: Counter = Counter()
570	    preds_new: Counter = Counter()
571	    sani_ctr:  Counter = Counter()
572	    bare_id_to_uri = build_bare_id_index(rdf)
573	
574	    def _track(pred_iri: str) -> None:
575	        curie = _to_curie(pred_iri)
576	        preds_all[curie] += 1
577	        if any(pred_iri.startswith(ns) for ns in _NEW_NS):
578	            preds_new[curie] += 1
579	
580	    def _track_nqlist(nqlist: NQList) -> None:
581	        for nq in nqlist:
582	            try:
583	                _track(nq.split("> <", 1)[1].split(">", 1)[0])
584	            except IndexError:
585	                pass
586	
587	    cho: dict = rdf.get("ProvidedCHO") or {}
588	    if isinstance(cho, list):
589	        cho = cho[0] if cho else {}
590	
591	    cho_nt      = f"<{cho_uri}>"
592	    htype       = (cho.get("hierarchyType") or "").strip() or None
593	    dctype_vals = coerce_list(cho.get("dcType"))
594	
595	    # ── Class dispatch ────────────────────────────────────────────────────────
596	    type_lines, target_class, wemi, dispatch_flags = retype_entities(
597	        sector, mediatype, htype, dctype_vals,
598	        cho_nt, mediatype_class_map, htype_map, audio_type2class, graph_iri,
599	    )
600	    lines.extend(type_lines)
601	    _track_nqlist(type_lines)
602	
603	    # owl:sameAs link to original DDB URI (D22)
604	    lines.append(make_nq(cho_nt, f"<{OWL_SAMEAS}>", f"<{ddb_uri}>", graph_iri))
605	    _track(OWL_SAMEAS)
606	
607	    # ── Build per-record indexes ───────────────────────────────────────────────
608	    agents_index: dict[str, AgentDict] = {}
609	    for agent in coerce_list(rdf.get("Agent")):
610	        if not isinstance(agent, dict):
611	            continue
612	        about = (agent.get("about") or "").strip()
613	        if about:
614	            agents_index[mint_bare_id("Agent", about)] = agent
615	        for pl in coerce_list(agent.get("prefLabel")):
616	            t = (pl.get("$") or "").strip() if isinstance(pl, dict) else ""
617	            if t:
618	                agents_index.setdefault(t, agent)
619	
620	    event_participant_index: dict[str, str] = {}
621	    for event in coerce_list(rdf.get("Event")):
622	        if not isinstance(event, dict):
623	            continue
624	        ht = event.get("hasType") or {}
625	        if isinstance(ht, list):
626	            ht = ht[0] if ht else {}
627	        lido_type_uri = (ht.get("resource") or "").strip() if isinstance(ht, dict) else ""
628	        for p in coerce_list(event.get("P11_had_participant")):
629	            puri = (p.get("resource") or "").strip() if isinstance(p, dict) else ""
630	            if puri and lido_type_uri:
631	                event_participant_index[puri] = lido_type_uri
632	
633	    concepts_index: dict[str, dict] = {}
634	    for concept in coerce_list(rdf.get("Concept")):
635	        if not isinstance(concept, dict):
636	            continue
637	        about = (concept.get("about") or "").strip()
638	        if about:
639	            concepts_index[about] = concept
640	
641	    # ── dc:title — dual-emit (props-mapping D4) ───────────────────────────────
642	    dc_title_iri = "http://purl.org/dc/elements/1.1/title"
643	    title_prop   = class_prop_align.get((target_class, dc_title_iri), "")
644	    for obj_nt in value_to_nt_obj(cho.get("title"), sani_ctr):
645	        lines.append(make_nq(cho_nt, f"<{dc_title_iri}>", obj_nt, graph_iri))
646	        _track(dc_title_iri)
647	        if title_prop and title_prop != dc_title_iri:
648	            lines.append(make_nq(cho_nt, f"<{title_prop}>", obj_nt, graph_iri))
649	            _track(title_prop)
650	
651	    # ── Generic property loop ─────────────────────────────────────────────────
652	    dc_date_iri   = "http://purl.org/dc/elements/1.1/date"
653	    dcterms_iss   = "http://purl.org/dc/terms/issued"
654	    dcterms_ipart = "http://purl.org/dc/terms/isPartOf"
655	    _special_keys = frozenset({"creator", "contributor", "title"}) | SUBJECT_KEYS | _MOCHO_SKIP
656	
657	    subject_vals: list = []
658	    for skey in SUBJECT_KEYS:
659	        subject_vals.extend(coerce_list(cho.get(skey)))
660	    hastype_vals: list = coerce_list(cho.get("hasType"))
661	
662	    for prop, val in cho.items():
663	        if prop in _special_keys:
664	            continue
665	        prop_iri = _DDBEDM_PROP.get(prop)
666	        if not prop_iri:
667	            continue
668	        target_prop = class_prop_align.get((target_class, prop_iri), prop_iri)
669	        if not target_prop:
670	            continue
671	
672	        if prop_iri in (dc_date_iri, dcterms_iss):
673	            # Date normalisation (D15 / props-mapping §3.1)
674	            for v in coerce_list(val):
675	                raw = (v if isinstance(v, str) else
676	                       (v.get("$") or "") if isinstance(v, dict) else "").strip()
677	                for normed in normalize_date(raw):
678	                    if normed:
679	                        lines.append(make_nq(cho_nt, f"<{target_prop}>",
680	                                             f'"{_escape_literal(normed)}"', graph_iri))
681	                        _track(target_prop)
682	            continue
683	
684	        if prop_iri == dcterms_ipart:
685	            # isPartOf URI sanitisation (props-mapping §3.1)
686	            for obj_nt in value_to_nt_obj(val, sani_ctr):
687	                if not obj_nt.startswith("<"):
688	                    continue  # literal isPartOf skipped in mocho graph
689	                uri = obj_nt[1:-1]
690	                if not uri.startswith("http"):
691	                    if len(uri) == 32:
692	                        uri = DDB_ITEM_BASE + uri
693	                    else:
694	                        continue
695	                lines.append(make_nq(cho_nt, f"<{target_prop}>", f"<{uri}>", graph_iri))
696	                _track(target_prop)
697	            continue
698	
699	        for obj_nt in value_to_nt_obj(val, sani_ctr):
700	            lines.append(make_nq(cho_nt, f"<{target_prop}>",
701	                                 expand_obj_nt(obj_nt, bare_id_to_uri), graph_iri))
702	            _track(target_prop)
703	
704	    # ── Special handlers ──────────────────────────────────────────────────────
705	    _creator_lines = emit_creator_triples(
706	        cho_nt, cho.get("creator"), agents_index, target_class, class_prop_align, graph_iri,
707	    )
708	    lines.extend(_creator_lines)
709	    _track_nqlist(_creator_lines)
710	
711	    _contrib_lines = emit_contributor_triples(
712	        cho_nt, cho.get("contributor"),
713	        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,
714	    )
715	    lines.extend(_contrib_lines)
716	    _track_nqlist(_contrib_lines)
717	
718	    if subject_vals:
719	        _subject_lines = emit_subject_triples(cho_nt, subject_vals, concepts_index, graph_iri,
720	                                              bare_id_to_uri)
721	        lines.extend(_subject_lines)
722	        _track_nqlist(_subject_lines)
723	
724	    if hastype_vals:
725	        _hastype_lines = emit_hastype_triples(cho_nt, hastype_vals, concepts_index, graph_iri,
726	                                              bare_id_to_uri)
727	        lines.extend(_hastype_lines)
728	        _track_nqlist(_hastype_lines)
729	
730	    # ── Aggregation & Place ───────────────────────────────────────────────────
731	    agg = rdf.get("Aggregation") or {}
732	    if isinstance(agg, list):
733	        agg = agg[0] if agg else {}
734	    _agg_lines = emit_aggregation_triples(agg, cho_nt, graph_iri)
735	    lines.extend(_agg_lines)
736	    _track_nqlist(_agg_lines)
737	
738	    _place_lines = emit_place_stubs(rdf.get("Place"), graph_iri)
739	    lines.extend(_place_lines)
740	    _track_nqlist(_place_lines)
741	
742	    dispatch_flags["preds_all"]     = preds_all
743	    dispatch_flags["preds_new"]     = preds_new
744	    dispatch_flags["uri_sanitized"] = sani_ctr["uri_sanitized"]
745	    dispatch_flags["uri_split"]     = sani_ctr["uri_split"]
746	    return lines, target_class, wemi, dispatch_flags
747	
```

---

### Assistant *(2026-05-07T12:24:59.085Z)*

Now I have the full current state. Let me apply all the fixes systematically.

---

### Assistant *(2026-05-07T12:25:01.215Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py",
  "old_string": "_IRI_UNSAFE_RE = re.compile(r'[\\x00-\\x20<>\"{}|\\\\^`\\x7f]')",
  "new_string": "_IRI_UNSAFE_RE = re.compile(r'[\\x00-\\x20<>\"{}|\\\\^`\\x7f]')\n_BR_RE         = re.compile(r'<br\\s*/?\\s*>', re.IGNORECASE)"
}
```

---

### User *(2026-05-07T12:29:51.251Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:29:56.924Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py",
  "old_string": "def _escape_literal(s: str) -> str:\n    \"\"\"Escape characters illegal in N-Triples/N-Quads literal content.\"\"\"\n    return (s.replace(\"\\\\\", \"\\\\\\\\\")\n             .replace('\"', '\\\\\"')\n             .replace(\"\\n\", \"\\\\n\")\n             .replace(\"\\r\", \"\\\\r\")\n             .replace(\"\\t\", \"\\\\t\"))",
  "new_string": "def _escape_literal(s: str) -> str:\n    \"\"\"Escape characters illegal in N-Triples/N-Quads literal content.\"\"\"\n    s = _BR_RE.sub('\\n', s)\n    return (s.replace(\"\\\\\", \"\\\\\\\\\")\n             .replace('\"', '\\\\\"')\n             .replace(\"\\n\", \"\\\\n\")\n             .replace(\"\\r\", \"\\\\r\")\n             .replace(\"\\t\", \"\\\\t\"))"
}
```

---

### User *(2026-05-07T12:30:24.613Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py has been updated successfully.
```

---

### Assistant *(2026-05-07T12:30:29.264Z)*

Now fix `emit_subject_triples` to split `resource` on whitespace:

---

### Assistant *(2026-05-07T12:30:42.868Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        resource = (val.get(\"resource\") or \"\").strip()\n        label    = (val.get(\"$\")        or \"\").strip()\n        lang     = (val.get(\"lang\")     or \"\").strip()\n        if resource:\n            # Expand bare IDs: look up in the per-record index, fall back to Concept mint\n            if not resource.startswith((\"http\", \"urn\")):\n                expanded = _bare.get(resource) or mint_bare_id(\"Concept\", resource)\n            else:\n                expanded = resource\n            expanded_safe = _sanitize_iri(expanded)\n            if expanded_safe in seen:\n                continue\n            seen.add(expanded_safe)\n            lines.append(make_nq(cho_nt, f\"<{DCTERMS_SUBJECT}>\", f\"<{expanded_safe}>\", graph_iri))\n            concept = concepts_index.get(resource) or concepts_index.get(expanded)\n            if concept:\n                for pl in coerce_list(concept.get(\"prefLabel\")):\n                    for obj_nt in value_to_nt_obj(pl):\n                        lines.append(make_nq(f\"<{expanded_safe}>\", f\"<{RDFS_LABEL}>\",\n                                             obj_nt, graph_iri))\n        elif label:",
  "new_string": "        resource_raw = (val.get(\"resource\") or \"\").strip()\n        label        = (val.get(\"$\")        or \"\").strip()\n        lang         = (val.get(\"lang\")     or \"\").strip()\n        if resource_raw:\n            for resource in resource_raw.split():\n                # Expand bare IDs: look up in the per-record index, fall back to Concept mint\n                if not resource.startswith((\"http\", \"urn\")):\n                    expanded = _bare.get(resource) or mint_bare_id(\"Concept\", resource)\n                else:\n                    expanded = resource\n                expanded_safe = _sanitize_iri(expanded)\n                if expanded_safe in seen:\n                    continue\n                seen.add(expanded_safe)\n                lines.append(make_nq(cho_nt, f\"<{DCTERMS_SUBJECT}>\", f\"<{expanded_safe}>\", graph_iri))\n                concept = concepts_index.get(resource) or concepts_index.get(expanded)\n                if concept:\n                    for pl in coerce_list(concept.get(\"prefLabel\")):\n                        for obj_nt in value_to_nt_obj(pl):\n                            lines.append(make_nq(f\"<{expanded_safe}>\", f\"<{RDFS_LABEL}>\",\n                                                 obj_nt, graph_iri))\n        elif label:"
}
```

---

### User *(2026-05-07T12:31:23.924Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). The user provided the following reason for the rejection:  this is not just for subject. This is systemic. would it be better to place all these checks before all the emits start?
```

---

### Assistant *(2026-05-07T12:31:45.990Z)*

Good point. Rather than patching each emitter separately, a cleaner approach is to add one utility function in `utils.py` that encapsulates extract + split + expand + sanitize, then have every emitter call it. Something like:

```python
def resource_uris(
    val: dict,
    bare_id_to_uri: dict[str, str] | None = None,
    entity_class: str = "Agent",
) -> list[str]:
    """Return sanitized URI strings from a resource-bearing dict value.

    Splits space-separated URIs, expands bare IDs via index or mint,
    and percent-encodes any unsafe characters. Returns [] if no resource.
    """
    resource = (val.get("resource") or "").strip() if isinstance(val, dict) else ""
    if not resource:
        return []
    _bare = bare_id_to_uri or {}
    result = []
    for uri in resource.split():
        if not uri.startswith(("http", "urn")):
            uri = _bare.get(uri) or mint_bare_id(entity_class, uri)
        result.append(_sanitize_iri(uri))
    return result
```

Then every emitter that currently does manual `val.get("resource")` + single-URI treatment just calls `resource_uris(val, bare_id_to_uri, "Concept")` etc. instead.

The tradeoff vs a preprocessing step: preprocessing would need to know the entity_class per field (Agent vs Concept vs Place) and some emitters need the primary URI separately for LIDO event lookup — so the utility function approach is cleaner.

Should I implement it this way?

---

### User *(2026-05-07T12:39:39.843Z)*

plan this first before implementation, and also document in implementation-actual.md

---

### Assistant *(2026-05-07T12:39:45.344Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/goethe-faust -name \"implementation-actual.md\" 2>/dev/null; find /Users/mta/Documents/claude/goethe-faust/notes -name \"*.md\" | sort",
  "description": "Find implementation-actual.md and list notes"
}
```

---

### User *(2026-05-07T12:39:45.430Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-05-07T12:39:47.604Z)*

**Tool call:** `Bash`
```json
{
  "command": "find /Users/mta/Documents/claude/goethe-faust -name \"*.md\" | sort",
  "description": "Find all markdown files in goethe-faust"
}
```

---

### User *(2026-05-07T12:39:47.667Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/.claude/CLAUDE.md
/Users/mta/Documents/claude/goethe-faust/.pytest_cache/README.md
/Users/mta/Documents/claude/goethe-faust/.venv/lib/python3.9/site-packages/numpy/random/LICENSE.md
/Users/mta/Documents/claude/goethe-faust/.venv/lib/python3.9/site-packages/pip-26.0.1.dist-info/licenses/src/pip/_vendor/idna/LICENSE.md
/Users/mta/Documents/claude/goethe-faust/.venv/lib/python3.9/site-packages/pip/_vendor/idna/LICENSE.md
/Users/mta/Documents/claude/goethe-faust/README.md
/Users/mta/Documents/claude/goethe-faust/data/hf-cache/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf/README.md
/Users/mta/Documents/claude/goethe-faust/data/transcripts/claude-1-read-ddb-search-goethe-alljson-20260220-080350.md
/Users/mta/Documents/claude/goethe-faust/notes/adhoc-manifestation-types.md
/Users/mta/Documents/claude/goethe-faust/notes/audio-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/corpus-analysis.md
/Users/mta/Documents/claude/goethe-faust/notes/ddbedm-prov-o-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/entity-property-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/goethe-faust-gnd-linking-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/graph-views-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/how-claude-transcript.md
/Users/mta/Documents/claude/goethe-faust/notes/image-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/notes/infra-local-setup.md
/Users/mta/Documents/claude/goethe-faust/notes/inputs.md
/Users/mta/Documents/claude/goethe-faust/notes/isbd-title-analysis.md
/Users/mta/Documents/claude/goethe-faust/notes/memory-handover-20260414.md
/Users/mta/Documents/claude/goethe-faust/notes/ollama-qlever-mcp-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/openwebui-native-tool.md
/Users/mta/Documents/claude/goethe-faust/notes/openwebui-ollama-setup.md
/Users/mta/Documents/claude/goethe-faust/notes/outputs.md
/Users/mta/Documents/claude/goethe-faust/notes/plan-check-script.md
/Users/mta/Documents/claude/goethe-faust/notes/plan-configurable-setup.md
/Users/mta/Documents/claude/goethe-faust/notes/prov-lm-future-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/s4-dispatch-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/session-summary-final-dataset.md
/Users/mta/Documents/claude/goethe-faust/notes/tabularasa-mocho-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/tabularasa.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-cli-spec.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-dryrun-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-duckdb-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-future-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-lezdoit-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-revised-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-script-adr.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-script-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/entity-property-mapping-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/reorg-align-mocho-transform.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/transform-edm2mocho-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/transform-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/transform-revised-plan-s1.1-snapshot-20260502.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stale/transform-script-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-stats-plan.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-validation.md
/Users/mta/Documents/claude/goethe-faust/notes/transform-writeup.md
/Users/mta/Documents/claude/goethe-faust/notes/troubleshooting-mcpo.md
/Users/mta/Documents/claude/goethe-faust/notes/troubleshooting-openwebui-password.md
/Users/mta/Documents/claude/goethe-faust/notes/video-type-class-mapping.md
/Users/mta/Documents/claude/goethe-faust/output/transcripts/output-vscode-terminate-unexpectedly-i-lost-my-20260505-073332.md
/Users/mta/Documents/claude/goethe-faust/scripts/README.md
/Users/mta/Documents/claude/goethe-faust/scripts/transcripts/scripts-prepare-manual-validation-dataset-20260505-125836.md
/Users/mta/Documents/claude/goethe-faust/scripts/transform/README.md
/Users/mta/Documents/claude/goethe-faust/transcripts/claude-1-read-ddb-search-goethe-alljson-20260220-080350.md
/Users/mta/Documents/claude/goethe-faust/transcripts/claude-artificial-intelligence-engineering-rese-20260222-215730.md
/Users/mta/Documents/claude/goethe-faust/transcripts/claude-auto-save-transcripts-in-claudemd-20260222-103946.md
/Users/mta/Documents/claude/goethe-faust/transcripts/claude-does-teams-work-in-this-session-20260322-184807.md
/Users/mta/Documents/claude/goethe-faust/transcripts/claude-suggest-a-quick-access-solution-like-duc-20260223-170425.md
/Users/mta/Documents/claude/goethe-faust/transcripts/claude-update-usersmtaclaudeclaudemd-to-include-20260223-184928.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-btw-i-think-it-is-better-to-not-generate-20260506-091735.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-check-how-many-of-the-time-edmrdfprovide-20260502-191200.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-check-this-plan-i-have-some-qleverl-shma-20260506-090416.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-claude-was-forced-quit-how-to-recover-pr-20260420-115640.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-create-a-script-that-creates-nt-file-moc-20260416-164746.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-find-out-how-to-use-rml-to-convert-jsonl-20260416-203031.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-im-ready-to-run-on-the-full-corpus-is-th-20260506-070159.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-in-a-proper-software-development-project-20260505-204631.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-just-playing-the-devils-advocate-is-ther-20260430-080527.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-lets-plan-a-new-task-loading-usersmtadoc-20260413-110824.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-make-count-dctype-sparte004py-usable-for-20260501-085242.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-prepare-manual-validation-dataset-20260505-125836.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-project-mocho-goethe-faust-20260225-151004.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-read-memory-handover-from-the-previous-s-20260414-182906.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-there-are-bugs-in-the-transform-scripts-20260507-111958.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-vscode-terminate-unexpectedly-i-lost-my-20260505-073332.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-vscode-terminated-resume-from-transcript-20260505-073527.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-we-need-to-map-all-the-properties-attach-20260429-133226.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-what-is-the-best-practice-format-for-a-s-20260504-170202.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-what-kind-of-owl-axioms-i-should-define-20260420-122409.md
/Users/mta/Documents/claude/goethe-faust/transcripts/goethe-faust-which-script-counts-the-dctype-of-sparte-20260501-083607.md
/Users/mta/Documents/claude/goethe-faust/transcripts/transcript-goethe-faust-scraping.md
/Users/mta/Documents/claude/goethe-faust/transcripts/transcript-objecttype-fabio.md
```

---

### Assistant *(2026-05-07T12:39:51.107Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md"
}
```

---

### User *(2026-05-07T12:39:51.122Z)*

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
120	Each invocation creates a timestamped run directory. All output filenames are derived
121	from the input filename stem so that parallel sector runs in a shared directory are
122	unambiguous (e.g. `s2.jsonl` → `s2.nq`, `s2-stats.json`, …):
123	
124	```
125	output/transform/YYYYMMDD_HHMMSS/
126	  <stem>.nq                   N-Quads, all named graphs
127	  <stem>-werk-staging.duckdb  W-slot staging rows
128	  <stem>-stats.json           run statistics
129	  <stem>-errors.jsonl         per-record errors (written live)
130	  <stem>.log                  run log
131	```
132	
133	For the full GeMeA parallel run with `--outdir output/transform/gemea/s${n}`:
134	```
135	output/transform/gemea/
136	  s1/s1.nq  s1/s1-stats.json  s1/s1-errors.jsonl  s1/s1.log  ...
137	  s2/s2.nq  s2/s2-stats.json  s2/s2-errors.jsonl  s2/s2.log  ...
138	  ...
139	```
140	
141	Named graphs:
142	
143	| Graph IRI | Content |
144	|---|---|
145	| `https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm` | Verbatim EDM passthrough (always, including mt007) |
146	| `https://gemea.ise.fiz-karlsruhe.de/graph/mocho` | mocho-aligned triples (skipped for mt007) |
147	| `https://gemea.ise.fiz-karlsruhe.de/graph/prov` | PROV-O Layer 1 (always) |
148	
149	---
150	
151	## 5. POC run — goethe-faust reference corpus (2026-05-06)
152	
153	| Metric | Value |
154	|---|---|
155	| Records processed | 115,432 |
156	| Triples total | 14,713,376 |
157	| ddbedm / mocho / prov | 8,957,262 / 1,898,754 / 3,857,360 |
158	| werk_staging rows | 15 (`rdac:C10001` only) |
159	| Errors (parse + transform) | 0 |
160	| fallback_d9 | 0 |
161	| uri_split | 4,188 |
162	| uri_about_split | 1,309 |
163	| uri_sanitized | 29 |
164	
165	Dispatch sum check: 25,644 (htype) + 47,428 (mediatype) + 0 (fallback) + 42,360 (mt007) = 115,432 ✓
166	
167	---
168	
169	## 6. Open issues from validation
170	
171	From `notes/transform-validation.md`:
172	
173	### 6.1 `mocho:ImageWork` missing from werk_staging
174	
175	`_W_SLOT_CLASSES` triggers on `rdac:C10001` and `mo:MusicalWork` only. `transform-revised-plan.md §1.1` marks `mocho:ImageWork` as a GND-Werk target (ht015 Illustration, ht019 Karte, sparte005 mt002). No `mocho:ImageWork` records in the goethe-faust corpus, so no current impact. **Fix before running on a broader corpus.**
176	
177	### 6.2 `ec:EditorialWork` werk_staging scope
178	
179	Adding `ec:EditorialWork` would produce 88 additional staging rows (mt005 Video). `transform-revised-plan.md §1.1` has no "GND Werk" column entry for mt005/EditorialWork. Video productions do not have GND Werk authority records. Left out intentionally; revisit when GND linking scope is finalised.
180	
181	---
182	
183	## 7. Full-corpus run plan
184	
185	See `notes/transform-dryrun-plan.md §6` for the full pipeline:
186	
187	1. **Export** — `python -m transform.sqlite_export` per sector (`s1.sqlite`…`s7.sqlite`) → per-sector JSONL
188	2. **Transform** — one `python -m transform` worker per sector, all in parallel
189	3. **Merge** — `cat` N-Quads shards; DuckDB `INSERT OR REPLACE` across staging files
190	
191	Config files (`--alignment`, `--lido`, `--htype`, `--mediatype`, `--audio`) must be passed explicitly when running from outside the goethe-faust root. All live in `goethe-faust/output/config/`.
192	
193	Estimated wall time at 18.5M records: ~1–1.5 h (7 parallel workers).
194	
```

---

### Assistant *(2026-05-07T12:40:36.558Z)*

Now I have the full picture. Let me write the plan into `transform-implementation-actual.md` first.

---

### Assistant *(2026-05-07T12:40:37.418Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 1,
  "limit": 80
}
```

---

### User *(2026-05-07T12:40:37.434Z)*

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
30	)
31	from transform.emitters import (
32	    retype_entities,
33	    emit_creator_triples,
34	    emit_contributor_triples,
35	    emit_subject_triples,
36	    emit_hastype_triples,
37	    emit_aggregation_triples,
38	    emit_place_stubs,
39	    werk_staging_row,
40	    emit_ddbedm_triples,
41	)
42	from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE
43	from transform.loaders import load_mediatype_class, load_htype_map
44	
45	# Config table paths
46	_CONFIG = PROJECT_DIR / "output" / "config"
47	
48	
49	# ── Helpers ───────────────────────────────────────────────────────────────────
50	
51	def _rdf_types(lines: list[str]) -> set[str]:
52	    """Extract the object IRIs from all rdf:type triples in a list of N-Quads lines."""
53	    rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
54	    result: set[str] = set()
55	    for line in lines:
56	        parts = line.split()
57	        if len(parts) >= 4 and f"<{rdf_type}>" in parts[1]:
58	            obj = parts[2].strip("<>")
59	            result.add(obj)
60	    return result
61	
62	
63	def _predicates(lines: list[str]) -> set[str]:
64	    result: set[str] = set()
65	    for line in lines:
66	        parts = line.split()
67	        if len(parts) >= 4:
68	            result.add(parts[1].strip("<>"))
69	    return result
70	
71	
72	def _load_configs():
73	    mc_map = load_mediatype_class(_CONFIG / "lookup_mediatype_class.csv")
74	    ht_map = load_htype_map(_CONFIG / "lookup_htype_doco_rico.csv")
75	    return mc_map, ht_map
76	
77	
78	# ── normalize_date ────────────────────────────────────────────────────────────
79	
80	class TestNormalizeDate:
```

---

### Assistant *(2026-05-07T12:40:40.930Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "description": "Count test file lines"
}
```

---

### User *(2026-05-07T12:40:40.981Z)*

**Tool result**
```
     611 /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py
```

---

### Assistant *(2026-05-07T12:40:43.479Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 560,
  "limit": 52
}
```

---

### User *(2026-05-07T12:40:43.486Z)*

**Tool result**
```
560	
561	def test_hasmet_in_mocho_skip():
562	    assert "hasMet" in _MOCHO_SKIP, "hasMet must be in _MOCHO_SKIP to prevent edm:hasMet on gemea CHOs"
563	
564	
565	# ── emit_hastype_triples ──────────────────────────────────────────────────────
566	
567	_BARE_HT = "R" * 32
568	
569	class TestEmitHastypeTriples:
570	    _cho_nt = "<https://gemea.ise.fiz-karlsruhe.de/mocho/" + "S" * 32 + ">"
571	
572	    def test_full_uri_emitted(self):
573	        uri = "http://ddb.vocnet.org/medientyp/mt003"
574	        vals = [{"resource": uri, "$": "", "lang": ""}]
575	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
576	        assert any(EDM_HAS_TYPE in l and uri in l for l in lines)
577	
578	    def test_bare_id_expanded_via_index(self):
579	        bare_id_to_uri = {_BARE_HT: f"urn:ddbedm:Concept:{_BARE_HT}"}
580	        vals = [{"resource": _BARE_HT}]
581	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, bare_id_to_uri)
582	        assert any(f"urn:ddbedm:Concept:{_BARE_HT}" in l for l in lines)
583	
584	    def test_bare_id_fallback_concept_mint(self):
585	        vals = [{"resource": _BARE_HT}]
586	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO, {})
587	        assert any(f"urn:ddbedm:Concept:{_BARE_HT}" in l for l in lines)
588	
589	    def test_label_stub_from_concept(self):
590	        uri = "http://ddb.vocnet.org/thema/th001"
591	        concept = {"about": uri, "prefLabel": [{"$": "Musik", "lang": "de"}]}
592	        vals = [{"resource": uri}]
593	        lines = emit_hastype_triples(self._cho_nt, vals, {uri: concept}, GRAPH_MOCHO)
594	        label_line = next((l for l in lines if '"Musik"@de' in l), None)
595	        assert label_line is not None
596	        assert uri in label_line
597	
598	    def test_literal_only_skipped(self):
599	        vals = [{"resource": "", "$": "Foto", "lang": "de"}]
600	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
601	        assert lines == []
602	
603	    def test_dedup(self):
604	        uri = "http://ddb.vocnet.org/medientyp/mt003"
605	        vals = [{"resource": uri}, {"resource": uri}]
606	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
607	        assert len([l for l in lines if EDM_HAS_TYPE in l]) == 1
608	
609	
610	def test_hastype_in_mocho_skip():
611	    assert "hasType" in _MOCHO_SKIP
```

---

### Assistant *(2026-05-07T12:41:06.098Z)*

Now I have full context. Let me write the plan section into `transform-implementation-actual.md`.

---

### Assistant *(2026-05-07T12:41:35.400Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "old_string": "## 7. Full-corpus run plan",
  "new_string": "## 7. Emitter safety audit (2026-05-07)\n\n### 7.1 Issue categories\n\nThree systemic gaps identified by post-POC audit:\n\n| # | Category | Root cause | Scope |\n|---|---|---|---|\n| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags before escaping `\\n` | Any string value containing `<br>` produces a literal `\\n` escape sequence preceded by an unescaped `<br>` tag |\n| B | Multi-URI `resource` not split | Emitters that manually extract `val.get(\"resource\")` treat space-separated URIs as a single URI string (malformed IRI) | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples` |\n| C | Bare IDs not expanded | Same emitters bypass `expand_obj_nt` and thus miss expansion of 32-char bare DDB IDs | `emit_creator_triples`, `emit_contributor_triples`; also `emit_place_stubs` (bare ID in `about`) and `emit_prov_triples` (`provider_isil` not sanitized) |\n\nNote: `value_to_nt_obj` (used by the generic loop in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are in special-case emitters that extract `resource` manually.\n\n### 7.2 Design decision — `resource_uris()` utility\n\nRather than patching each emitter individually, a single utility function in `utils.py` encapsulates the three sub-steps that every manual `resource` extraction must perform:\n\n```python\ndef resource_uris(\n    resource_raw: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n    entity_class: str = \"Agent\",\n) -> list[str]:\n    \"\"\"Expand, sanitize, and split all URIs from a (possibly multi-value) resource string.\n\n    Steps: (1) split on whitespace; (2) expand bare IDs via index or mint_bare_id fallback;\n    (3) percent-encode unsafe characters. Returns [] for empty input.\n    \"\"\"\n```\n\nCallers pass the raw string from `val.get(\"resource\")`, the per-record `bare_id_to_uri` index (from `build_bare_id_index`), and the entity class for bare-ID minting. The function returns a list of safe, fully-qualified URI strings ready for `f\"<{uri}>\"` wrapping.\n\nFor emitters that also need the *raw first URI* before expansion (e.g. `event_participant_index` lookup in `emit_contributor_triples`, `resolve_agent` lookup in `emit_creator_triples`): callers extract the raw `resource_raw.split()[0]` before calling `resource_uris()`.\n\n### 7.3 Change inventory\n\n**`utils.py`**\n\n| Change | Detail |\n|---|---|\n| Add `_BR_RE` regex | `re.compile(r'<br\\s*/?\\s*>', re.IGNORECASE)` |\n| Update `_escape_literal` | Prepend `s = _BR_RE.sub('\\n', s)` — tag normalized before `\\n` escape step |\n| Add `resource_uris()` | New utility; imported by `emitters.py` |\n\n**`emitters.py`**\n\n| Emitter | Change |\n|---|---|\n| `emit_subject_triples` | Replace `resource = val.get(\"resource\")` + single-URI branch with `resource_raw` + `resource_uris(resource_raw, _bare, \"Concept\")` loop |\n| `emit_hastype_triples` | Same pattern as `emit_subject_triples` |\n| `emit_creator_triples` | Add `bare_id_to_uri=None` param; Track 1: `resource_uris()` loop; Track 2: use `resource_raw.split()[0]` for `resolve_agent`; apply `_sanitize_iri(agent_uri)` |\n| `emit_contributor_triples` | Add `bare_id_to_uri=None` param; use `resource_raw.split()[0]` for `event_participant_index` lookup; `resource_uris()` loop for triple emission |\n| `emit_prov_triples` | Apply `_sanitize_iri(provider_isil)` on line emitting `MOCHO_ISIL` triple |\n| `emit_place_stubs` | Split `raw_about`, use `raw_about.split()[0]` for `mint_bare_id`; apply `_sanitize_iri` |\n| `emit_aggregation_triples` | Inline split+sanitize for `isShownAt.resource`, `dataProvider.resource`, `object.resource` (no bare ID expansion — aggregation-level URIs are always full) |\n| `emit_mocho_triples` | Pass `bare_id_to_uri` as kwarg to `emit_creator_triples` and `emit_contributor_triples` |\n\n**`emitters.py` — import update**\n\nAdd `resource_uris` to the `from .utils import` block.\n\n### 7.4 Test inventory\n\nNew tests to add to `test_transform.py`:\n\n| Class / function | What it covers |\n|---|---|\n| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\\\n` in the output |\n| `TestResourceUris` | empty string → `[]`; single full URI → `[sanitized]`; two space-separated URIs → two entries; bare ID → expanded via index; bare ID fallback → `mint_bare_id`; entity_class forwarded correctly |\n| `TestEmitSubjectTriplesMultiUri` | `resource = \"URI1 URI2\"` → two `dcterms:subject` triples |\n| `TestEmitHastypeTriplesMultiUri` | Same for `edm:hasType` |\n| `TestEmitCreatorTriplesMultiUri` | Two URIs in resource → two Track-1 triples |\n| `TestEmitCreatorTriplesBareId` | Bare ID in resource expanded; `agent_uri` from agent dict sanitized |\n| `TestEmitContributorTriplesMultiUri` | Two URIs in resource → two `(cho, prop, uri)` triples |\n| `TestEmitContributorTriplesBareId` | Bare ID in resource expanded |\n| `TestEmitProvTriplesIsil` | `provider_isil` with space → sanitized in ISIL triple |\n| `TestEmitPlaceStubsSplitAbout` | Space-separated `about` → only first part used as subject |\n| `TestEmitAggregationSplitUri` | `isShownAt.resource = \"URI1 URI2\"` → two `dcterms:source` triples |\n\n---\n\n## 8. Full-corpus run plan"
}
```

---

### User *(2026-05-07T12:44:00.166Z)*

**Tool result** *(error)*
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). The user provided the following reason for the rejection:  also in the test, take subset of json file and their corresponding .nq triples for me to inspect
```

---

### Assistant *(2026-05-07T12:44:03.778Z)*

Let me check what test data is available before writing the plan.

---

### Assistant *(2026-05-07T12:44:04.860Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/ 2>/dev/null; ls /Users/mta/Documents/claude/goethe-faust/data/ 2>/dev/null | head -20",
  "description": "List transform tests directory and data directory"
}
```

---

### User *(2026-05-07T12:44:04.920Z)*

**Tool result**
```
__init__.py
test_transform.py
analysis
ddb-search-faust-all.json
ddb-search-faust-goethe-all.json
ddb-search-goethe-all.json
ddbedm
fabio-type2class.json
goethe-faust.json
hf-cache
ids-all-goethe-faust.txt
ids-faust.txt
ids-goethe.txt
ids-missing.txt
items-all-goethe-faust.json
items-all-goethe-faust.json.gz
items-excerpt-1000.json
logs
processed
qlever-index
schemas
search-ids-post.txt
```

---

### Assistant *(2026-05-07T12:44:18.391Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/analysis/ 2>/dev/null | head -20; ls /Users/mta/Documents/claude/goethe-faust/data/ddbedm/ 2>/dev/null | head -20",
  "description": "List analysis subdir and ddbedm data"
}
```

---

### User *(2026-05-07T12:44:18.438Z)*

**Tool result**
```
cortex.xml
ddbedm-htype.csv
json_schema_paths.csv
```

---

### Assistant *(2026-05-07T12:44:39.683Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -1 /Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json | python3 -c \"import json,sys; r=json.loads(sys.stdin.read()); print(json.dumps(list(r.keys())[:5]))\"",
  "description": "Inspect top-level structure of one excerpt record"
}
```

---

### User *(2026-05-07T12:45:10.106Z)*

**Tool result** *(error)*
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 2)
```

---

### Assistant *(2026-05-07T12:45:13.495Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -1 /Users/mta/Documents/claude/goethe-faust/data/items-excerpt-1000.json | python3 -c \"import json,sys; r=json.loads(sys.stdin.readline()); print(json.dumps(list(r.keys())[:8]))\"",
  "description": "Inspect keys of first JSONL record"
}
```

---

### Assistant *(2026-05-07T12:45:16.626Z)*

**Tool call:** `Bash`
```json
{
  "command": "# Search for records with multi-URI resource fields\npython3 -c \"\nimport json, re\nmulti_re = re.compile(r'https?://\\S+ https?://')\nbr_re = re.compile(r'<br\\s*/?\\s*>', re.IGNORECASE)\nmulti_ids, br_ids = [], []\nwith open('goethe-faust/data/items-excerpt-1000.json') as f:\n    for i, line in enumerate(f):\n        line = line.strip()\n        if not line: continue\n        if multi_re.search(line):\n            multi_ids.append(i)\n        if br_re.search(line):\n            br_ids.append(i)\nprint('multi-URI lines:', multi_ids[:5])\nprint('br lines:', br_ids[:5])\n\" 2>&1 | head -20",
  "description": "Find records with multi-URI and br patterns in excerpt"
}
```

---

### User *(2026-05-07T14:32:14.476Z)*

**Tool result** *(error)*
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 2)
```

---

### User *(2026-05-07T14:32:14.476Z)*

**Tool result** *(error)*
```
<tool_use_error>Cancelled: parallel tool call Bash(head -1 /Users/mta/Documents/claude/goet…) errored</tool_use_error>
```

---

### Assistant *(2026-05-07T14:32:20.220Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && python3 -c \"\nimport json\nwith open('data/items-excerpt-1000.json') as f:\n    content = f.read()\n# Try parsing as JSON array\ntry:\n    data = json.loads(content)\n    print(type(data), len(data) if isinstance(data, list) else 'dict')\nexcept:\n    # Try as newline-separated\n    lines = [l.strip() for l in content.splitlines() if l.strip()]\n    print('lines:', len(lines))\n    print('first 100 chars of line 1:', lines[0][:100])\n\"",
  "description": "Probe the format of items-excerpt-1000.json"
}
```

---

### User *(2026-05-07T15:21:26.933Z)*

**Tool result**
```
<class 'list'> 1000
```

---

### User *(2026-05-07T15:21:28.143Z)*

[Request interrupted by user]

---

### User *(2026-05-07T15:23:12.373Z)*

this is the schema /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv

---

### Assistant *(2026-05-07T15:23:16.714Z)*

**Tool call:** `Bash`
```json
{
  "command": "head -5 /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv && echo \"---\" && wc -l /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv",
  "description": "Preview schema CSV header and row count"
}
```

---

### User *(2026-05-07T15:23:16.945Z)*

**Tool result**
```
path,value_types
aggregator-info,Literals(string)
aggregator-info.aggregator-collection,Literals(string)
aggregator-info.aggregator-ddb-id,Literals(string)
aggregator-info.aggregator-domains,
---
     548 /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv
```

---

### Assistant *(2026-05-07T15:23:20.256Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && grep -E \"(resource|creator|contributor|subject|hasType|hierarchyType|about|prefLabel|place|provider-isil)\" data/ddbedm/json_schema_paths.csv | grep -v \"^\\s*#\" | head -60",
  "description": "Filter schema paths relevant to emitter audit"
}
```

---

### User *(2026-05-07T15:23:20.310Z)*

**Tool result**
```
ddbObject.category[].hierarchyType,Literals(string)
ddbObject.category[].standardised[].resource,Literals(string)
ddbObject.contributor[],
ddbObject.creator[],
ddbObject.identifier.hierarchyType,Literals(string)
ddbObject.identifier.objectID.resource,Literals(string)
ddbObject.mediaType.hierarchyType,Literals(string)
ddbObject.mediaType.literal[].resource,Literals(string)
ddbObject.subjectEvent[],
ddbObject.subjectWhat[],
ddbObject.subjectWhen[],
ddbObject.subjectWhere[],
ddbObject.subjectWho[],
ddbObject.subject[],
ddbObject.title[].resource,Literals(string)
edm.RDF.Agent.prefLabel,
edm.RDF.Agent[].about,Literals(string)|URI
edm.RDF.Agent[].isPartOf[].resource,URI
edm.RDF.Agent[].placeOfBirth,Literals(string)
edm.RDF.Agent[].placeOfDeath,Literals(string)
edm.RDF.Agent[].prefLabel[].$,Literals(string)
edm.RDF.Agent[].prefLabel[].lang,Literals(string)
edm.RDF.Agent[].type.resource,URI
edm.RDF.Agent[].wasPresentAt.resource,Literals(string)
edm.RDF.Aggregation.about,Literals(string)|URI
edm.RDF.Aggregation.aggregatedCHO.resource,URI
edm.RDF.Aggregation.aggregator.resource,URI
edm.RDF.Aggregation.dataProvider[].resource,Literals(string)|URI
edm.RDF.Aggregation.dcTermsRights.resource,URI
edm.RDF.Aggregation.edmRights.resource,URI
edm.RDF.Aggregation.hasView[].resource,Literals(string)|URI
edm.RDF.Aggregation.isShownAt.resource,Literals(string)|URI
edm.RDF.Aggregation.isShownBy.resource,Literals(string)|URI
edm.RDF.Aggregation.object.resource,Literals(string)|URI
edm.RDF.Concept.prefLabel,
edm.RDF.Concept[].about,Literals(string)|URI
edm.RDF.Concept[].prefLabel,Literals(string)
edm.RDF.Concept[].prefLabel.$,Literals(string)
edm.RDF.Concept[].prefLabel.lang,Literals(string)
edm.RDF.Concept[].prefLabel.resource,Literals(string)
edm.RDF.Event.hasType,
edm.RDF.Event[].P11_had_participant[].resource,Literals(string)|URI
edm.RDF.Event[].about,Literals(string)|URI
edm.RDF.Event[].happenedAt[].resource,Literals(string)|URI
edm.RDF.Event[].hasType,Literals(string)
edm.RDF.Event[].hasType.$,Literals(string)
edm.RDF.Event[].hasType.lang,Literals(string)
edm.RDF.Event[].hasType.resource,URI
edm.RDF.Event[].occuredAt[].resource,Literals(string)
edm.RDF.PhysicalThing[].about,Literals(string)
edm.RDF.PhysicalThing[].hierarchyType,Literals(string)
edm.RDF.PhysicalThing[].isPartOf[].resource,Literals(string)|URI
edm.RDF.PhysicalThing[].title.resource,Literals(string)
edm.RDF.Place.prefLabel,
edm.RDF.Place[].about,Literals(string)|URI
edm.RDF.Place[].prefLabel[].$,Literals(string)
edm.RDF.Place[].prefLabel[].lang,Literals(string)
edm.RDF.ProvidedCHO.about,URI
edm.RDF.ProvidedCHO.alternative[].resource,Literals(string)
edm.RDF.ProvidedCHO.contributor,
```

---

### Assistant *(2026-05-07T15:23:22.679Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep \"^edm.RDF.ProvidedCHO\" data/ddbedm/json_schema_paths.csv",
  "description": "All ProvidedCHO paths from schema"
}
```

---

### User *(2026-05-07T15:23:22.757Z)*

**Tool result**
```
edm.RDF.ProvidedCHO,
edm.RDF.ProvidedCHO.about,URI
edm.RDF.ProvidedCHO.aggregationEntity,Literals(string)
edm.RDF.ProvidedCHO.alternative,
edm.RDF.ProvidedCHO.alternative[].$,Literals(string)
edm.RDF.ProvidedCHO.alternative[].lang,Literals(string)
edm.RDF.ProvidedCHO.alternative[].resource,Literals(string)
edm.RDF.ProvidedCHO.contributor,
edm.RDF.ProvidedCHO.contributor[].$,Literals(string)
edm.RDF.ProvidedCHO.contributor[].lang,Literals(string)
edm.RDF.ProvidedCHO.contributor[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.creator,
edm.RDF.ProvidedCHO.creator[].$,Literals(string)
edm.RDF.ProvidedCHO.creator[].lang,Literals(string)
edm.RDF.ProvidedCHO.creator[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.currentLocation,
edm.RDF.ProvidedCHO.currentLocation.$,Literals(string)
edm.RDF.ProvidedCHO.currentLocation.lang,Literals(string)
edm.RDF.ProvidedCHO.currentLocation.resource,Literals(string)|URI
edm.RDF.ProvidedCHO.date[],Literals(string)
edm.RDF.ProvidedCHO.dcSubject,
edm.RDF.ProvidedCHO.dcSubject[].$,Literals(string)
edm.RDF.ProvidedCHO.dcSubject[].lang,Literals(string)
edm.RDF.ProvidedCHO.dcSubject[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.dcTermSubject,
edm.RDF.ProvidedCHO.dcTermSubject[].$,Literals(string)
edm.RDF.ProvidedCHO.dcTermSubject[].lang,Literals(string)
edm.RDF.ProvidedCHO.dcTermSubject[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.dcTermsLanguage,
edm.RDF.ProvidedCHO.dcTermsLanguage[].$,Literals(string)
edm.RDF.ProvidedCHO.dcTermsLanguage[].lang,Literals(string)
edm.RDF.ProvidedCHO.dcTermsLanguage[].resource,URI
edm.RDF.ProvidedCHO.dcTermsSubject,
edm.RDF.ProvidedCHO.dcTermsSubject[].$,Literals(string)
edm.RDF.ProvidedCHO.dcTermsSubject[].lang,Literals(string)
edm.RDF.ProvidedCHO.dcTermsSubject[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.dcType,
edm.RDF.ProvidedCHO.dcType.$,Literals(string)
edm.RDF.ProvidedCHO.dcType.lang,Literals(string)
edm.RDF.ProvidedCHO.dcType.resource,Literals(string)|URI
edm.RDF.ProvidedCHO.description,
edm.RDF.ProvidedCHO.description[].$,Literals(string)
edm.RDF.ProvidedCHO.description[].lang,Literals(string)
edm.RDF.ProvidedCHO.description[].resource,Literals(string)
edm.RDF.ProvidedCHO.edmType,Literals(string)
edm.RDF.ProvidedCHO.extent,
edm.RDF.ProvidedCHO.extent[].$,Literals(string)
edm.RDF.ProvidedCHO.extent[].lang,Literals(string)
edm.RDF.ProvidedCHO.extent[].resource,Literals(string)
edm.RDF.ProvidedCHO.format,
edm.RDF.ProvidedCHO.format.$,Literals(string)
edm.RDF.ProvidedCHO.format.lang,Literals(string)
edm.RDF.ProvidedCHO.format.resource,Literals(string)|URI
edm.RDF.ProvidedCHO.hasMet,
edm.RDF.ProvidedCHO.hasMet[].$,Literals(string)
edm.RDF.ProvidedCHO.hasMet[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.hasType,
edm.RDF.ProvidedCHO.hasType[].$,Literals(string)
edm.RDF.ProvidedCHO.hasType[].lang,Literals(string)
edm.RDF.ProvidedCHO.hasType[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.hierarchyPosition,Literals(string)
edm.RDF.ProvidedCHO.hierarchyType,Literals(string)
edm.RDF.ProvidedCHO.identifier[],Literals(string)|URI
edm.RDF.ProvidedCHO.isPartOf,
edm.RDF.ProvidedCHO.isPartOf[].$,Literals(string)
edm.RDF.ProvidedCHO.isPartOf[].lang,Literals(string)
edm.RDF.ProvidedCHO.isPartOf[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.issued,
edm.RDF.ProvidedCHO.issued[].$,Literals(string)
edm.RDF.ProvidedCHO.issued[].lang,Literals(string)
edm.RDF.ProvidedCHO.issued[].resource,Literals(string)
edm.RDF.ProvidedCHO.language,Literals(string)
edm.RDF.ProvidedCHO.spatial,
edm.RDF.ProvidedCHO.spatial[].$,Literals(string)
edm.RDF.ProvidedCHO.spatial[].lang,Literals(string)
edm.RDF.ProvidedCHO.spatial[].resource,Literals(string)|URI
edm.RDF.ProvidedCHO.title,
edm.RDF.ProvidedCHO.title.$,Literals(string)
edm.RDF.ProvidedCHO.title.lang,Literals(string)
edm.RDF.ProvidedCHO.title.resource,Literals(string)
```

---

### Assistant *(2026-05-07T15:23:29.255Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep \"^provider-info\" /Users/mta/Documents/claude/goethe-faust/data/ddbedm/json_schema_paths.csv",
  "description": "Provider-info paths from schema"
}
```

---

### User *(2026-05-07T15:23:29.325Z)*

**Tool result**
```
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
provider-info.provider-parents.parents[].provider-parent-id,Literals(string)
provider-info.provider-parents.parents[].provider-uri,URI
provider-info.provider-state,Literals(string)
provider-info.provider-twitter,Literals(string)|URI
provider-info.provider-uri,URI
```

---

### Assistant *(2026-05-07T15:23:39.328Z)*

Now let me find records demonstrating each issue pattern, including the provided example:

---

### Assistant *(2026-05-07T15:23:44.178Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json, re\n\nmulti_re  = re.compile(r'https?://\\S+ https?://')\nbr_re     = re.compile(r'<br\\s*/?\\s*>', re.IGNORECASE)\nbare_re   = re.compile(r'\\\"resource\\\":\\s*\\\"([A-Za-z0-9]{32})\\\"')\ntarget_id = '34TALB4SALQ5PPR3O5FG42GEZP3CA6IB'\n\nmulti_recs, br_recs, bare_recs, target_rec = [], [], [], None\n\nwith open('data/items-all-goethe-faust.json') as f:\n    for line in f:\n        line = line.strip()\n        if not line: continue\n        try: rec = json.loads(line)\n        except: continue\n        obj_id = None\n        try: obj_id = rec['edm']['RDF']['ProvidedCHO']['about'].rsplit('/',1)[-1]\n        except: pass\n\n        if obj_id == target_id:\n            target_rec = rec\n\n        raw = json.dumps(rec)\n        if not multi_recs and multi_re.search(raw):\n            multi_recs.append((obj_id, rec))\n        if not br_recs and br_re.search(raw):\n            br_recs.append((obj_id, rec))\n        if not bare_recs and bare_re.search(raw):\n            bare_recs.append((obj_id, rec))\n        if target_rec and multi_recs and br_recs and bare_recs:\n            break\n\nprint('target:', bool(target_rec))\nprint('multi:', [x[0] for x in multi_recs])\nprint('br:', [x[0] for x in br_recs])\nprint('bare:', [x[0] for x in bare_recs])\n\"\n",
  "description": "Find fixture records for each issue category plus the provided example"
}
```

---

### User *(2026-05-07T15:24:32.783Z)*

**Tool result**
```
target: False
multi: ['23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF']
br: ['223GMAWUHPGI76OQUKSL54XVOCHHXDWD']
bare: ['222NZKK63TNRLC2VETRV722VKBDSUVGL']
```

---

### Assistant *(2026-05-07T15:24:37.927Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json\nwith open('data/items-all-goethe-faust.json') as f:\n    for line in f:\n        line = line.strip()\n        if not line: continue\n        try: rec = json.loads(line)\n        except: continue\n        try: obj_id = rec['edm']['RDF']['ProvidedCHO']['about'].rsplit('/',1)[-1]\n        except: continue\n        if obj_id == '34TALB4SALQ5PPR3O5FG42GEZP3CA6IB':\n            print('FOUND'); break\n    else:\n        print('NOT IN FILE')\n# Also search the goethe-faust.json\nimport subprocess\nresult = subprocess.run(['grep', '-l', '34TALB4SALQ5PPR3O5FG42GEZP3CA6IB', \n    'data/items-all-goethe-faust.json', 'data/goethe-faust.json',\n    'data/items-excerpt-1000.json'], capture_output=True, text=True)\nprint(result.stdout, result.stderr)\n\"",
  "description": "Search for the provided example record ID across data files"
}
```

---

### User *(2026-05-07T15:25:47.941Z)*

**Tool result**
```
NOT IN FILE
```

---

### Assistant *(2026-05-07T15:25:51.145Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -l \"34TALB4SALQ5PPR3O5FG42GEZP3CA6IB\" data/*.json 2>/dev/null || echo \"not found in data/\"",
  "description": "Search for example ID in all JSON data files"
}
```

---

### User *(2026-05-07T15:25:51.798Z)*

**Tool result** *(error)*
```
Exit code 1
```

---

### Assistant *(2026-05-07T15:26:00.713Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json, re\nmulti_re = re.compile(r'https?://\\S+ https?://')\ntarget_ids = {\n    '23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF',\n    '223GMAWUHPGI76OQUKSL54XVOCHHXDWD',\n    '222NZKK63TNRLC2VETRV722VKBDSUVGL',\n}\nfound = {}\nwith open('data/items-all-goethe-faust.json') as f:\n    for line in f:\n        line = line.strip()\n        if not line: continue\n        try: rec = json.loads(line)\n        except: continue\n        try: obj_id = rec['edm']['RDF']['ProvidedCHO']['about'].rsplit('/',1)[-1]\n        except: continue\n        if obj_id in target_ids:\n            found[obj_id] = rec\n        if len(found) == len(target_ids):\n            break\n\nfor oid, rec in found.items():\n    raw = json.dumps(rec)\n    matches = multi_re.findall(raw)\n    cho = rec['edm']['RDF']['ProvidedCHO']\n    print(f'=== {oid} ===')\n    print('  multi-URI hits:', matches[:3])\n    if 'creator' in cho:\n        print('  creator:', json.dumps(cho['creator'])[:200])\n    if 'contributor' in cho:\n        print('  contributor:', str(cho['contributor'])[:200])\n    if 'dcSubject' in cho or 'dcTermsSubject' in cho:\n        print('  subject:', str(cho.get('dcSubject') or cho.get('dcTermsSubject'))[:200])\n    if 'hasType' in cho:\n        print('  hasType:', json.dumps(cho['hasType'])[:200])\n    print()\n\" 2>&1 | head -80",
  "description": "Inspect relevant fields of the three fixture records"
}
```

---

### User *(2026-05-07T15:29:45.854Z)*

**Tool result**
```
=== 222NZKK63TNRLC2VETRV722VKBDSUVGL ===
  multi-URI hits: []
  contributor: [{'resource': None, 'lang': 'zxx', '$': 'DDZ (Fotografische Aufnahme) (Atelier/Verlag)'}]
  subject: [{'resource': None, 'lang': 'ger', '$': 'Album'}, {'resource': None, 'lang': 'ger', '$': 'Einsteckalbum'}, {'resource': None, 'lang': 'ger', '$': 'Kalligraphie'}, {'resource': None, 'lang': 'ger', '$'
  hasType: [{"resource": "DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6", "lang": null, "$": ""}]

=== 223GMAWUHPGI76OQUKSL54XVOCHHXDWD ===
  multi-URI hits: []
  subject: [{'resource': None, 'lang': 'ger', '$': 'Faust I. und II.'}, {'resource': None, 'lang': 'ger', '$': 'Goethe, Johann Wolfgang von'}, {'resource': None, 'lang': 'ger', '$': 'Lassen, Eduard'}]
  hasType: [{"resource": "https://d-nb.info/gnd/4142968-0", "lang": null, "$": ""}]

=== 23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF ===
  multi-URI hits: ['http://d-nb.info/gnd/4044283-4 https://', 'http://d-nb.info/gnd/4044283-4 https://', 'http://d-nb.info/gnd/4044283-4 https://']
  hasType: [{"resource": "http://d-nb.info/gnd/4021791-7", "lang": null, "$": ""}, {"resource": "http://d-nb.info/gnd/7581172-8", "lang": null, "$": ""}]
```

---

### Assistant *(2026-05-07T15:29:54.846Z)*

**Tool call:** `Bash`
```json
{
  "command": "python3 -c \"\nimport json, re\nbr_re = re.compile(r'<br\\s*/?\\s*>', re.IGNORECASE)\nbare_re = re.compile(r'\\\"resource\\\":\\s*\\\"([A-Za-z0-9]{32})\\\"')\n\ntarget_ids = {\n    '23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF',\n    '223GMAWUHPGI76OQUKSL54XVOCHHXDWD',\n    '222NZKK63TNRLC2VETRV722VKBDSUVGL',\n}\nwith open('data/items-all-goethe-faust.json') as f:\n    for line in f:\n        line = line.strip()\n        if not line: continue\n        try: rec = json.loads(line)\n        except: continue\n        try: obj_id = rec['edm']['RDF']['ProvidedCHO']['about'].rsplit('/',1)[-1]\n        except: continue\n        if obj_id in target_ids:\n            raw = json.dumps(rec)\n            cho = rec['edm']['RDF']['ProvidedCHO']\n\n            if obj_id == '223GMAWUHPGI76OQUKSL54XVOCHHXDWD':\n                # find <br> field\n                m = br_re.search(raw)\n                print('br record context:', raw[max(0,m.start()-50):m.end()+80] if m else 'NOT FOUND')\n\n            if obj_id == '222NZKK63TNRLC2VETRV722VKBDSUVGL':\n                # find bare id\n                m = bare_re.search(raw)\n                print('bare record context:', raw[max(0,m.start()-80):m.end()+80] if m else 'NOT FOUND')\n                print('hasType:', json.dumps(cho.get('hasType')))\n\n            if obj_id == '23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF':\n                # find the multi-URI field\n                for key, val in rec['edm']['RDF'].items():\n                    for ent in ([val] if isinstance(val,dict) else val if isinstance(val,list) else []):\n                        if not isinstance(ent,dict): continue\n                        for k,v in ent.items():\n                            vl = json.dumps(v)\n                            if 'gnd/4044283' in vl:\n                                print(f'multi-URI field: {key}.{k} =', vl[:300])\n\" 2>&1",
  "description": "Find exact field locations of each pattern in the fixture records"
}
```

---

### User *(2026-05-07T15:30:11.536Z)*

**Tool result**
```
bare record context: fDeath": null, "professionOrOccupation": null, "sameAs": null, "wasPresentAt": {"resource": "PH5JJIYFIVCTJYPWZSMZCHQSJWATUON3", "$": ""}}], "PhysicalThing": null, "ProvidedCHO": {"about": "http://www.deutsc
hasType: [{"resource": "DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6", "lang": null, "$": ""}]
br record context: g von Goethe *28. August 1749, +22. M\u00e4rz 1832<br />Eduard Lassen *13 April 1830, +15 Januar 1904"}], "identifier": ["A Rep. 167 (No
multi-URI field: ProvidedCHO.currentLocation = {"resource": "http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745", "lang": null, "$": ""}
multi-URI field: Place.about = "http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745"
```

---

### Assistant *(2026-05-07T15:30:51.647Z)*

Now I have everything I need. Let me write the plan section:

---

### Assistant *(2026-05-07T15:31:29.225Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "old_string": "## 7. Full-corpus run plan",
  "new_string": "## 7. Emitter safety audit (2026-05-07)\n\n### 7.1 Issue categories\n\nThree systemic gaps identified by post-POC audit:\n\n| # | Category | Root cause | Emitters affected |\n|---|---|---|---|\n| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags; the unescaped tag appears verbatim in the N-Quad literal | Any emitter that calls `_escape_literal` on a field containing `<br …>` |\n| B | Multi-URI `resource` not split | Emitters that manually extract `val.get(\"resource\")` treat space-separated URIs as one string, producing a malformed IRI | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs` |\n| C | Bare IDs not expanded in special emitters | Same emitters bypass `expand_obj_nt`; also `emit_prov_triples` passes `provider_isil` without `_sanitize_iri` | `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`, `emit_prov_triples` |\n\nNote: `value_to_nt_obj` (used by the generic loops in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are exclusively in special-case emitters that extract `resource` manually.\n\nCorpus evidence (from `data/items-all-goethe-faust.json`):\n- **B** — `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF`: `ProvidedCHO.currentLocation.resource = \"http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745\"` and matching `Place.about`\n- **A** — `223GMAWUHPGI76OQUKSL54XVOCHHXDWD`: description field contains `\"...1749, +22. März 1832<br />Eduard Lassen...\"` \n- **C** — `222NZKK63TNRLC2VETRV722VKBDSUVGL`: `ProvidedCHO.hasType[0].resource = \"DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6\"` (bare 32-char ID)\n\n### 7.2 Design — `resource_uris()` utility\n\nRather than patching each emitter individually, one utility in `utils.py` encapsulates the three sub-steps every manual `resource` extraction must perform:\n\n```python\ndef resource_uris(\n    resource_raw: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n    entity_class: str = \"Agent\",\n) -> list[str]:\n    \"\"\"Expand, sanitize, and split all URIs from a (possibly multi-value) resource string.\n\n    Steps: (1) split on whitespace; (2) expand bare IDs via index or mint_bare_id fallback;\n    (3) percent-encode unsafe characters. Returns [] for empty input.\n    \"\"\"\n```\n\nCallers pass `(val.get(\"resource\") or \"\").strip()`, the per-record `bare_id_to_uri` index, and the entity class for bare-ID minting. Returns a list of safe, full URI strings ready for `f\"<{uri}>\"` wrapping.\n\n**Primary-URI rule**: emitters that need the raw first URI before expansion (e.g. `event_participant_index` lookup in `emit_contributor_triples`, `resolve_agent` in `emit_creator_triples`) extract `resource_raw.split()[0]` before calling `resource_uris()`.\n\n### 7.3 Change inventory\n\n**`utils.py`**\n\n| Change | Detail |\n|---|---|\n| Add `_BR_RE` | `re.compile(r'<br\\s*/?\\s*>', re.IGNORECASE)` |\n| Update `_escape_literal` | Prepend `s = _BR_RE.sub('\\n', s)` before the escape chain |\n| Add `resource_uris()` | New utility; imported by `emitters.py` |\n\n**`emitters.py`**\n\n| Emitter | Change |\n|---|---|\n| `emit_subject_triples` | Replace single-URI `resource` branch with `resource_uris(resource_raw, _bare, \"Concept\")` loop |\n| `emit_hastype_triples` | Same pattern |\n| `emit_creator_triples` | Add `bare_id_to_uri=None` param; Track 1: `resource_uris()` loop; Track 2: `resource_raw.split()[0]` for `resolve_agent`; apply `_sanitize_iri(agent_uri)` |\n| `emit_contributor_triples` | Add `bare_id_to_uri=None` param; `resource_raw.split()[0]` for `event_participant_index` lookup; `resource_uris()` loop for triples |\n| `emit_prov_triples` | Apply `_sanitize_iri(provider_isil)` |\n| `emit_place_stubs` | Split `raw_about`; pass only first part to `mint_bare_id` with `_sanitize_iri` |\n| `emit_aggregation_triples` | Inline split+sanitize loop for `isShownAt.resource`, `dataProvider.resource`, `object.resource` (no bare ID expansion — aggregation URIs are always full) |\n| `emit_mocho_triples` | Pass `bare_id_to_uri` to `emit_creator_triples` and `emit_contributor_triples` |\n\n**`emitters.py` — imports**: add `resource_uris` to `from .utils import`.\n\n### 7.4 Fixture-based integration tests\n\nThree real corpus records are saved to `scripts/transform/tests/fixtures/` as minimal inspection targets. Each record is stored as `<id>.json` (single-record JSON, not JSONL).\n\n| File | Record ID | Pattern |\n|---|---|---|\n| `fixtures/multi_uri.json` | `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF` | Multi-URI in `Place.about` and `currentLocation.resource` |\n| `fixtures/br_tag.json` | `223GMAWUHPGI76OQUKSL54XVOCHHXDWD` | `<br />` in description literal |\n| `fixtures/bare_id.json` | `222NZKK63TNRLC2VETRV722VKBDSUVGL` | Bare 32-char ID in `hasType.resource` |\n\nAfter fixes are applied, a fixture script `tests/make_fixtures.py` runs the full transform on all three records and writes `fixtures/<id>.nq` — the complete N-Quads output for human inspection.\n\nIntegration tests in `test_transform.py` (new `TestFixtures` class) load each `.json`, call `transform_record()`, and make targeted assertions:\n\n| Test | Assertion |\n|---|---|\n| `test_multi_uri_place_splits` | Two separate `Place` subject IRIs emitted; no IRI containing a space |\n| `test_multi_uri_current_location_splits` | Two separate triples for `currentLocation` |\n| `test_br_tag_normalized` | `\\\\n` appears in the relevant literal; no `<br` substring in any triple |\n| `test_bare_id_hastype_expanded` | `urn:ddbedm:Concept:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |\n\n### 7.5 Unit test additions\n\n| Class / function | Covers |\n|---|---|\n| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\\\n` |\n| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id`; entity_class forwarded |\n| `TestEmitSubjectTriplesMultiUri` | `\"URI1 URI2\"` → two `dcterms:subject` triples |\n| `TestEmitHastypeTriplesMultiUri` | Same for `edm:hasType` |\n| `TestEmitCreatorTriplesMultiUri` | Two URIs → two Track-1 triples |\n| `TestEmitCreatorTriplesBareId` | Bare ID expanded; `agent_uri` sanitized |\n| `TestEmitContributorTriplesMultiUri` | Two URIs → two `(cho, prop, uri)` triples |\n| `TestEmitContributorTriplesBareId` | Bare ID expanded via param |\n| `TestEmitProvTriplesIsil` | `provider_isil` with unsafe chars → sanitized in `MOCHO_ISIL` triple |\n| `TestEmitPlaceStubsSplitAbout` | Space-separated `about` → only first part used as subject |\n| `TestEmitAggregationSplitUri` | `isShownAt.resource = \"URI1 URI2\"` → two `dcterms:source` triples |\n\n---\n\n## 8. Full-corpus run plan"
}
```

---

### User *(2026-05-07T15:35:43.722Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md has been updated successfully.
```

---

### Assistant *(2026-05-07T15:35:50.518Z)*

Plan is written. Summary of what's documented in §7:

- **§7.1** — three issue categories (A: `<br>` in literals, B: multi-URI not split, C: bare IDs not expanded), with exact corpus records as evidence
- **§7.2** — `resource_uris(resource_raw, bare_id_to_uri, entity_class)` utility design; primary-URI rule for emitters that also need a raw first URI (LIDO lookup, agent resolution)
- **§7.3** — full change inventory: 3 in `utils.py`, 8 in `emitters.py`
- **§7.4** — three fixture records (`multi_uri.json`, `br_tag.json`, `bare_id.json`) + `make_fixtures.py` script that produces `.nq` for human inspection + 4 targeted integration test assertions
- **§7.5** — 11 unit test classes/extensions

Ready to implement when you confirm the plan looks right.

---

### User *(2026-05-07T15:41:34.280Z)*

what triple/s does edm:currentLocation property emit right now?

---

### Assistant *(2026-05-07T15:41:38.735Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"currentLocation\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "description": "Find currentLocation in constants and emitters"
}
```

---

### User *(2026-05-07T15:41:38.795Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py:258:    "currentLocation":     EDM_NS + "currentLocation",
```

---

### Assistant *(2026-05-07T15:41:43.951Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"currentLocation\\|_MOCHO_SKIP\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py | head -20",
  "description": "Check currentLocation in _MOCHO_SKIP and constants"
}
```

---

### User *(2026-05-07T15:41:44.011Z)*

**Tool result**
```
103:_MOCHO_SKIP = frozenset({
258:    "currentLocation":     EDM_NS + "currentLocation",
```

---

### Assistant *(2026-05-07T15:41:46.752Z)*

**Tool call:** `Bash`
```json
{
  "command": "sed -n '103,115p' /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "description": "Show _MOCHO_SKIP contents"
}
```

---

### User *(2026-05-07T15:41:46.796Z)*

**Tool result**
```
_MOCHO_SKIP = frozenset({
    "about", "hierarchyType",
    "creator", "contributor",
    "dcSubject", "dcTermsSubject", "dcTermSubject",
    "dcType",
    "aggregationEntity", "hierarchyPosition",
    "hasMet",     # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph
    "hasType",    # handled by emit_hastype_triples(); needs bare-ID expansion + label stub
})

# ─── Prefix expansion table ───────────────────────────────────────────────────

_PREFIXES = {
```

---

### Assistant *(2026-05-07T15:41:52.479Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep \"currentLocation\" /Users/mta/Documents/claude/goethe-faust/output/config/lookup_class_prop_alignment.csv | head -10",
  "description": "Check prop alignment for currentLocation"
}
```

---

### User *(2026-05-07T15:41:52.546Z)*

**Tool result**
```
edm:ProvidedCHO,rdac:C10007,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,mocho:Manifestation,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,aco:AudioManifestation,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,mocho:ImageManifestation,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,ec:MediaResource,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,mo:MusicalManifestation,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,vra:Image,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,doco:Section,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,doco:Appendix,M,edm:currentLocation,edm:currentLocation
edm:ProvidedCHO,doco:Part,M,edm:currentLocation,edm:currentLocation
```

---

### Assistant *(2026-05-07T15:42:01.596Z)*

`currentLocation` goes through the **generic loop** in both emitters — `_DDBEDM_PROP["currentLocation"] = edm:currentLocation`, not in `_MOCHO_SKIP`, prop alignment maps it 1:1 to `edm:currentLocation`.

So `value_to_nt_obj` handles it, which **already splits on whitespace**. For record `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF` with `"resource": "http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745"`, the current output is already:

```
<cho> <edm:currentLocation> <http://d-nb.info/gnd/4044283-4> <graph> .
<cho> <edm:currentLocation> <https://www.geonames.org/2855745> <graph> .
```

Two triples, correctly split — **no bug here**. The multi-URI gap from that record is in `Place.about`, which goes through `emit_place_stubs`, not through `value_to_nt_obj`.

The plan section §7.4 fixture description for `multi_uri.json` is slightly misleading — I should update it: the relevant pattern to test is `Place.about` splitting, not `currentLocation.resource`.

---

### User *(2026-05-07T15:51:38.973Z)*

add the same handling as edm:hasType. this should be added as a "category" of handing. That when the value is a Literal, emit the same triple. if it's a uri, sanitize and emit additional triple for each valid URI:

<cho> edm:currentLocation <geo> .
<geo> rdfs:label <the skos:prefLabel of the matching edm:Place> .

btw, what's the harm of changing from skos:prefLabel to rdfs:label?

---

### Assistant *(2026-05-07T15:52:46.240Z)*

`rdfs:label` is the right choice for stubs in the mocho graph. The only harm: a SPARQL query specifically filtering `skos:prefLabel` won't find these labels. But `skos:prefLabel rdfs:subPropertyOf rdfs:label` — so the implication only runs the other way (asserting `skos:prefLabel` entails `rdfs:label`, not vice versa). For stub convenience labels in the mocho graph, `rdfs:label` is what QLever text-indexes against, and these stubs aren't full SKOS concept descriptions anyway. No real harm.

Now let me update the plan to add the `currentLocation` pattern, then implement everything.

---

### Assistant *(2026-05-07T15:52:46.314Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "offset": 183,
  "limit": 110
}
```

---

### User *(2026-05-07T15:52:46.322Z)*

**Tool result**
```
183	## 7. Emitter safety audit (2026-05-07)
184	
185	### 7.1 Issue categories
186	
187	Three systemic gaps identified by post-POC audit:
188	
189	| # | Category | Root cause | Emitters affected |
190	|---|---|---|---|
191	| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags; the unescaped tag appears verbatim in the N-Quad literal | Any emitter that calls `_escape_literal` on a field containing `<br …>` |
192	| B | Multi-URI `resource` not split | Emitters that manually extract `val.get("resource")` treat space-separated URIs as one string, producing a malformed IRI | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs` |
193	| C | Bare IDs not expanded in special emitters | Same emitters bypass `expand_obj_nt`; also `emit_prov_triples` passes `provider_isil` without `_sanitize_iri` | `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`, `emit_prov_triples` |
194	
195	Note: `value_to_nt_obj` (used by the generic loops in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are exclusively in special-case emitters that extract `resource` manually.
196	
197	Corpus evidence (from `data/items-all-goethe-faust.json`):
198	- **B** — `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF`: `ProvidedCHO.currentLocation.resource = "http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745"` and matching `Place.about`
199	- **A** — `223GMAWUHPGI76OQUKSL54XVOCHHXDWD`: description field contains `"...1749, +22. März 1832<br />Eduard Lassen..."` 
200	- **C** — `222NZKK63TNRLC2VETRV722VKBDSUVGL`: `ProvidedCHO.hasType[0].resource = "DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6"` (bare 32-char ID)
201	
202	### 7.2 Design — `resource_uris()` utility
203	
204	Rather than patching each emitter individually, one utility in `utils.py` encapsulates the three sub-steps every manual `resource` extraction must perform:
205	
206	```python
207	def resource_uris(
208	    resource_raw: str,
209	    bare_id_to_uri: dict[str, str] | None = None,
210	    entity_class: str = "Agent",
211	) -> list[str]:
212	    """Expand, sanitize, and split all URIs from a (possibly multi-value) resource string.
213	
214	    Steps: (1) split on whitespace; (2) expand bare IDs via index or mint_bare_id fallback;
215	    (3) percent-encode unsafe characters. Returns [] for empty input.
216	    """
217	```
218	
219	Callers pass `(val.get("resource") or "").strip()`, the per-record `bare_id_to_uri` index, and the entity class for bare-ID minting. Returns a list of safe, full URI strings ready for `f"<{uri}>"` wrapping.
220	
221	**Primary-URI rule**: emitters that need the raw first URI before expansion (e.g. `event_participant_index` lookup in `emit_contributor_triples`, `resolve_agent` in `emit_creator_triples`) extract `resource_raw.split()[0]` before calling `resource_uris()`.
222	
223	### 7.3 Change inventory
224	
225	**`utils.py`**
226	
227	| Change | Detail |
228	|---|---|
229	| Add `_BR_RE` | `re.compile(r'<br\s*/?\s*>', re.IGNORECASE)` |
230	| Update `_escape_literal` | Prepend `s = _BR_RE.sub('\n', s)` before the escape chain |
231	| Add `resource_uris()` | New utility; imported by `emitters.py` |
232	
233	**`emitters.py`**
234	
235	| Emitter | Change |
236	|---|---|
237	| `emit_subject_triples` | Replace single-URI `resource` branch with `resource_uris(resource_raw, _bare, "Concept")` loop |
238	| `emit_hastype_triples` | Same pattern |
239	| `emit_creator_triples` | Add `bare_id_to_uri=None` param; Track 1: `resource_uris()` loop; Track 2: `resource_raw.split()[0]` for `resolve_agent`; apply `_sanitize_iri(agent_uri)` |
240	| `emit_contributor_triples` | Add `bare_id_to_uri=None` param; `resource_raw.split()[0]` for `event_participant_index` lookup; `resource_uris()` loop for triples |
241	| `emit_prov_triples` | Apply `_sanitize_iri(provider_isil)` |
242	| `emit_place_stubs` | Split `raw_about`; pass only first part to `mint_bare_id` with `_sanitize_iri` |
243	| `emit_aggregation_triples` | Inline split+sanitize loop for `isShownAt.resource`, `dataProvider.resource`, `object.resource` (no bare ID expansion — aggregation URIs are always full) |
244	| `emit_mocho_triples` | Pass `bare_id_to_uri` to `emit_creator_triples` and `emit_contributor_triples` |
245	
246	**`emitters.py` — imports**: add `resource_uris` to `from .utils import`.
247	
248	### 7.4 Fixture-based integration tests
249	
250	Three real corpus records are saved to `scripts/transform/tests/fixtures/` as minimal inspection targets. Each record is stored as `<id>.json` (single-record JSON, not JSONL).
251	
252	| File | Record ID | Pattern |
253	|---|---|---|
254	| `fixtures/multi_uri.json` | `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF` | Multi-URI in `Place.about` and `currentLocation.resource` |
255	| `fixtures/br_tag.json` | `223GMAWUHPGI76OQUKSL54XVOCHHXDWD` | `<br />` in description literal |
256	| `fixtures/bare_id.json` | `222NZKK63TNRLC2VETRV722VKBDSUVGL` | Bare 32-char ID in `hasType.resource` |
257	
258	After fixes are applied, a fixture script `tests/make_fixtures.py` runs the full transform on all three records and writes `fixtures/<id>.nq` — the complete N-Quads output for human inspection.
259	
260	Integration tests in `test_transform.py` (new `TestFixtures` class) load each `.json`, call `transform_record()`, and make targeted assertions:
261	
262	| Test | Assertion |
263	|---|---|
264	| `test_multi_uri_place_splits` | Two separate `Place` subject IRIs emitted; no IRI containing a space |
265	| `test_multi_uri_current_location_splits` | Two separate triples for `currentLocation` |
266	| `test_br_tag_normalized` | `\\n` appears in the relevant literal; no `<br` substring in any triple |
267	| `test_bare_id_hastype_expanded` | `urn:ddbedm:Concept:DJVX…` IRI in `edm:hasType` triple; no raw bare ID as IRI |
268	
269	### 7.5 Unit test additions
270	
271	| Class / function | Covers |
272	|---|---|
273	| `TestEscapeLiteral` (extend) | `<br>`, `<BR />`, `<br/>` all produce `\\n` |
274	| `TestResourceUris` | empty → `[]`; single full URI → `[sanitized]`; two space-separated → two entries; bare ID → index lookup; bare ID fallback → `mint_bare_id`; entity_class forwarded |
275	| `TestEmitSubjectTriplesMultiUri` | `"URI1 URI2"` → two `dcterms:subject` triples |
276	| `TestEmitHastypeTriplesMultiUri` | Same for `edm:hasType` |
277	| `TestEmitCreatorTriplesMultiUri` | Two URIs → two Track-1 triples |
278	| `TestEmitCreatorTriplesBareId` | Bare ID expanded; `agent_uri` sanitized |
279	| `TestEmitContributorTriplesMultiUri` | Two URIs → two `(cho, prop, uri)` triples |
280	| `TestEmitContributorTriplesBareId` | Bare ID expanded via param |
281	| `TestEmitProvTriplesIsil` | `provider_isil` with unsafe chars → sanitized in `MOCHO_ISIL` triple |
282	| `TestEmitPlaceStubsSplitAbout` | Space-separated `about` → only first part used as subject |
283	| `TestEmitAggregationSplitUri` | `isShownAt.resource = "URI1 URI2"` → two `dcterms:source` triples |
284	
285	---
286	
287	## 8. Full-corpus run plan
288	
289	See `notes/transform-dryrun-plan.md §6` for the full pipeline:
290	
291	1. **Export** — `python -m transform.sqlite_export` per sector (`s1.sqlite`…`s7.sqlite`) → per-sector JSONL
292	2. **Transform** — one `python -m transform` worker per sector, all in parallel
```

---

### Assistant *(2026-05-07T15:53:11.047Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md",
  "old_string": "### 7.1 Issue categories\n\nThree systemic gaps identified by post-POC audit:\n\n| # | Category | Root cause | Emitters affected |\n|---|---|---|---|\n| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags; the unescaped tag appears verbatim in the N-Quad literal | Any emitter that calls `_escape_literal` on a field containing `<br …>` |\n| B | Multi-URI `resource` not split | Emitters that manually extract `val.get(\"resource\")` treat space-separated URIs as one string, producing a malformed IRI | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs` |\n| C | Bare IDs not expanded in special emitters | Same emitters bypass `expand_obj_nt`; also `emit_prov_triples` passes `provider_isil` without `_sanitize_iri` | `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`, `emit_prov_triples` |\n\nNote: `value_to_nt_obj` (used by the generic loops in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are exclusively in special-case emitters that extract `resource` manually.\n\nCorpus evidence (from `data/items-all-goethe-faust.json`):\n- **B** — `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF`: `ProvidedCHO.currentLocation.resource = \"http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745\"` and matching `Place.about`\n- **A** — `223GMAWUHPGI76OQUKSL54XVOCHHXDWD`: description field contains `\"...1749, +22. März 1832<br />Eduard Lassen...\"` \n- **C** — `222NZKK63TNRLC2VETRV722VKBDSUVGL`: `ProvidedCHO.hasType[0].resource = \"DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6\"` (bare 32-char ID)",
  "new_string": "### 7.1 Issue categories\n\nThree systemic gaps (A–C) and one feature addition (D):\n\n| # | Category | Root cause / motivation | Emitters affected |\n|---|---|---|---|\n| A | `<br>` in literals | `_escape_literal` does not normalize HTML line-break tags; the unescaped tag appears verbatim in the N-Quad literal | Any emitter that calls `_escape_literal` on a field containing `<br …>` |\n| B | Multi-URI `resource` not split | Emitters that manually extract `val.get(\"resource\")` treat space-separated URIs as one string, producing a malformed IRI | `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_aggregation_triples`, `emit_place_stubs` |\n| C | Bare IDs not expanded in special emitters | Same emitters bypass `expand_obj_nt`; also `emit_prov_triples` passes `provider_isil` without `_sanitize_iri` | `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`, `emit_prov_triples` |\n| D | `edm:currentLocation` — IRI-with-label-stub | Currently emitted via generic loop (no label stub). Should follow the same \"IRI-with-label-stub\" pattern as `edm:hasType`: URI values get a `rdfs:label` stub from the matching `edm:Place`; literal values pass through unchanged | New `emit_current_location_triples`; `\"currentLocation\"` added to `_MOCHO_SKIP` |\n\nNote: `value_to_nt_obj` (used by the generic loops in `emit_ddbedm_triples` and `emit_mocho_triples`) already handles B and C correctly via `.split()` and `_sanitize_iri`. The gaps are exclusively in special-case emitters that extract `resource` manually.\n\nCorpus evidence (from `data/items-all-goethe-faust.json`):\n- **B/D** — `23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF`: `ProvidedCHO.currentLocation.resource = \"http://d-nb.info/gnd/4044283-4 https://www.geonames.org/2855745\"` and matching `Place.about`\n- **A** — `223GMAWUHPGI76OQUKSL54XVOCHHXDWD`: description field contains `\"...1749, +22. März 1832<br />Eduard Lassen...\"` \n- **C** — `222NZKK63TNRLC2VETRV722VKBDSUVGL`: `ProvidedCHO.hasType[0].resource = \"DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6\"` (bare 32-char ID)"
}
```

---

### User *(2026-05-07T15:54:28.664Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-actual.md has been updated successfully.
```

---

### User *(2026-05-07T15:54:34.950Z)*

[Request interrupted by user]

---

### User *(2026-05-07T15:55:04.718Z)*

hold on, also, do I need to type the new place URIs in the mocho graph? 

or would it suffice that it is already in edm?

---

### User *(2026-05-07T15:55:16.952Z)*

[Request interrupted by user]

---

### User *(2026-05-07T15:55:32.697Z)*

hold on, also, do I need to type the new place URIs in the mocho graph? 

or would it suffice that it is defined as edm:Place already in the ddbedm graph?

---

### Assistant *(2026-05-07T15:55:56.194Z)*

No need to type in the mocho graph. Two reasons:

1. **Precedent from `emit_hastype_triples`**: it emits `<concept> rdfs:label "…"` as a stub in mocho but never `<concept> rdf:type skos:Concept`. The same principle applies — the stub is just a display convenience, not a full entity description.

2. **The type is already authoritative in ddbedm**: `emit_ddbedm_triples` emits `<place> rdf:type edm:Place` for every `Place` entity. QLever queries against the default graph (union of all named graphs) will find it. If someone queries only the mocho graph, they lose the type — but that's the correct trade-off: the mocho graph is for mocho-aligned triples, not for re-asserting EDM entity types.

The only edge case: if `currentLocation` references a Place URI that is **not** in the same record (external GND/GeoNames URI), there's no `Place.about` entry to match, so no label stub is emitted anyway. The URI lands in the mocho graph typed as nothing — but that's fine; the URI itself (GND, GeoNames) is resolvable and its type is asserted in whatever enrichment graph we add later.

So the pattern stays lean: `<cho> edm:currentLocation <place>` + `<place> rdfs:label "…"` only when the Place is locally described. No type triple in mocho.

Ready to proceed with updating the plan section and then implementing?

---

### User *(2026-05-07T15:57:28.103Z)*

Add the decision about rdfs:label and skos:prefLabel in the transform-props-mapping-adr. and also the decision to forego typing of context description properties (agent, place, concept, timespan).

---

### Assistant *(2026-05-07T15:57:32.420Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md"
}
```

---

### User *(2026-05-07T15:57:32.929Z)*

**Tool result**
```
1	# ADR: EDM → mocho Property Mapping Decisions
2	
3	**Date**: 2026-05-02
4	**Status**: In progress
5	**Related**: `transform-adr.md` (class dispatch), `transform-script-adr.md` (implementation), `transform-props-mapping-plan.md` (full property mapping catalogue)
6	
7	---
8	
9	## Context
10	
11	This document records decisions about **which predicate to emit** for each EDM/DC property in `transform_edm_to_mocho.py`. Class-assignment decisions (rdf:type dispatch, htype lookup, mediatype dispatch) are in `transform-adr.md` and `transform-script-adr.md`. The decisions here govern property-level choices: which RDA/RiC-O/VRA/vocab predicate replaces or accompanies the source DC/EDM predicate, and when the source predicate is kept or skipped.
12	
13	All ProvidedCHOs are typed as `mocho:Manifestation` (D9, `transform-script-adr.md`). Target predicates for Manifestation-level properties use `rdam:` where a Manifestation-specific RDA property exists. For Work-level nodes produced by W+M dispatch, `rdaw:` properties are used.
14	
15	---
16	
17	## Decision 1: Subject keys — IRI correction and value-type dispatch
18	
19	*(Moved from `transform-script-adr.md` D6)*
20	
21	**Decision**: Three JSON keys carry subject data: `dcSubject`, `dcTermsSubject`, `dcTermSubject`. These are handled by a dedicated `emit_subject_triples()` function, not the generic alignment loop.
22	
23	**Background**: Corpus inspection revealed that `dcTermsSubject` was incorrectly mapped to `dc:subject` (`http://purl.org/dc/elements/1.1/subject`) in `alignment_ddbedm_mocho.csv`. The correct IRI is `dcterms:subject` (`http://purl.org/dc/terms/subject`). This was a derivation error in the alignment script's IRI resolution step; `dcTermSubject` (note: missing `s`) was correctly resolved to `dcterms:subject` via an explicit `OVERRIDES` entry in `align_ddbedm_to_mocho.py`. The fix was applied directly to the CSV (42 rows: `edm_prefix` `dc→dcterms`, `edm_iri` corrected).
24	
25	**Dispatch logic**:
26	- Literal value (string or lang-tagged text) → `dc:subject "string"@lang` — uncontrolled annotation; no concept node minted.
27	- IRI value (`{"resource": ..., "$": label}`) → two triples:
28	  1. `<cho> dcterms:subject <concept-uri>`
29	  2. `<concept-uri> rdfs:label "label"@lang` — concept stub (label from `$` field; language from `@language` if present)
30	
31	**Deduplication**: `emit_subject_triples()` collects values from all three keys and deduplicates `(pred_nt, obj_nt)` pairs in a per-record set before writing. This prevents duplicate triples when the same value appears under multiple keys (occurs in ~60% of records). Concept stubs (`rdfs:label`) are also deduplicated per record — one label triple per URI.
32	
33	**Rationale**: The IRI + label stub pattern is strictly better for SPARQL retrieval than a literal-only approach:
34	- URI equality tests are index lookups; string matching is a scan with normalization risk.
35	- One `rdfs:label` triple per concept URI allows cross-record deduplication for faceting: `GROUP BY ?c ?label COUNT(?cho)` without string normalization.
36	- Future enrichment (`skos:broader`, `skos:altLabel`, `owl:sameAs` to GND/LCSH) attaches to the concept node without touching CHO triples.
37	
38	`dc:subject` is kept for literal-only values as a fallback annotation, signalling "unresolved, no authority URI". This keeps literal subjects queryable without mixing literal and IRI objects under `dcterms:subject`.
39	
40	---
41	
42	## Decision 2: Creator → rdam:P30329 "has creator agent of manifestation"
43	
44	*(Moved from `transform-script-adr.md` D7; IRI corrected from P30263 → P30329)*
45	
46	**Decision**: `dc:creator` (json_key: `creator`) is mapped to `rdam:P30329` "has creator agent of manifestation" (`http://rdaregistry.info/Elements/m/P30329`). The alignment table's 464 Work-level candidates are bypassed.
47	
48	**IRI correction**: The earlier decision (D7 in `transform-script-adr.md`) incorrectly cited `rdam:P30263`. The RDA properties CSV (`mocho/output/rda_properties_rda-5.4.9.csv`) confirms `P30263` is "has reduction ratio designation" — unrelated to creator. The correct Manifestation-level generic creator property is `rdam:P30329` "has creator agent of manifestation". This correction must also be applied in `transform_edm_to_mocho.py`.
49	
50	**Background**: The alignment table produces 464 candidates for `creator`, all at the Work WEMI level — including highly specific properties such as "has production company", "has plaintiff corporate body". These are correct sub-properties of Work-level creator properties but wrong for a generic `dc:creator` value where the role is unknown. The WEMI level is determined by D9 (`transform-script-adr.md`): all ProvidedCHOs are `mocho:Manifestation` → creator property must be Manifestation-level.
51	
52	**Typed subproperties** (Phase 1b): `rdam:P30363` (person), `rdam:P30392` (collective agent), `rdam:P30421` (corporate body), `rdam:P30450` (family) are the typed subproperties of `rdam:P30329`. These are the Phase 1b resolution path once GND agent type is resolved by `link_gnd_agents.py`.
53	
54	**Alternatives considered**:
55	- *Emit all 464*: Semantically noisy; a Goethe letter would assert "has plaintiff corporate body" for the author. Rejected.
56	- *Use rdaw:P10065 has creator agent of work*: Work-level; inconsistent with D9. Rejected.
57	- *Mediatype dispatch*: Correct role remains unknown even with mediatype. Rejected for POC.
58	
59	**Open**: D7 does not specify whether a GND URI in `resource` should cause an `edm:Agent` node to be minted and linked, or whether a plain literal is emitted. Phase 1b GND enrichment is the intended resolution path.
60	
61	---
62	
63	## Decision 3: Contributor — LIDO event type dispatch
64	
65	*(Supersedes earlier draft: "keep dc:contributor". Prior rationale: no generic RDA contributor property exists; alignment table candidates were all role-specific or wrong WEMI level.)*
66	
67	**Decision**: The specific predicate emitted for a `dc:contributor` value is determined by the LIDO event type of the `edm:Event` in which the contributor's Agent URI participates. Resolution chain:
68	
69	```
70	ProvidedCHO.hasMet[].resource  →  edm:Event.about
71	edm:Event.hasType.resource     →  LIDO event type URI
72	edm:Event.P11_had_participant[].resource  ==  contributor[].resource
73	→  emit <cho> <target_prop> <contributor.resource>
74	```
75	
76	If no matching Event is found (contributor URI absent from any Event.P11_had_participant, or contributor is label-only), fall back to `dc:contributor`.
77	
78	**Corpus evidence** (`data/items-excerpt-1000.json`, 519 contributor values):
79	- URI match → DDB org / GND: 325 (62.6%) — reliable join key
80	- Label match → DDB org / GND: 174 (33.5%) — lower than creator; label is not a reliable fallback
81	
82	See `notes/corpus-analysis.md §1b` and `data/analysis/contributor_agent_coverage.csv`.
83	
84	**LIDO event type → target predicate dispatch** (`output/config/lido_event_types.csv`):
85	
86	| LIDO event type | label | rdam_prop (M) | rdaw_prop (W) | vra_image | vra_work | rico_prop |
87	|---|---|---|---|---|---|---|
88	| lido00012, eventType/creation | creation | `rdam:P30329` | `rdaw:P10065` | `vra:creator` | `vra:creator` | `rico:hasCreator` |
89	| lido00228, eventType/publication | publication | `rdam:P30083` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `rico:hasPublisher` |
90	| lido00007 | production | `rdam:P30081` | `dc:contributor` | `vra:producer` | `vra:producer` | `dc:contributor` |
91	| lido01127 | photography | `rdam:P30329` | `rdaw:P10056` | `vra:photographer` | `vra:photographer` | `dc:contributor` |
92	| lido00224 | designing | `dc:contributor` | `rdaw:P10051` | `vra:designer` | `vra:designer` | `dc:contributor` |
93	| lido00226 | commissioning | `dc:contributor` | `rdaw:P10287` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
94	| lido00003 | unknown_event | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
95	| all others | — | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` | `dc:contributor` |
96	
97	For aco, mo, doco, ec, and mocho subclasses: `dc:contributor` in all rows (no role-specific property in those vocabularies).
98	
99	**RDA property notes**:
100	- `rdam:P30329` "has creator agent of manifestation" — used for photography as well as creation: no Manifestation-level photographer property exists in RDA; the photographer is the creator agent of the photographic manifestation.
101	- `rdam:P30081` "has producer agent of unpublished manifestation" — covers fabricated/inscribed artifacts (manuscripts, prints, artworks); no W-level RDA production-agent property exists, hence `dc:contributor` fallback for `rdaw_prop`.
102	- `rdam:P30083` "has publisher agent" — publication is inherently Manifestation-level in RDA; no W-level equivalent, hence `dc:contributor` fallback.
103	- `rdaw:P10051` "has designer agent", `rdaw:P10287` "has commissioning agent" — W-level only; no M-level equivalents, hence `dc:contributor` for `rdam_prop`.
104	- `rdaw:P10056` "has photographer agent of work" — W-level specific property for photography.
105	
106	**Source**: `output/config/lido_event_types.csv`; RDA labels verified from `mocho/output/rda_properties_rda-5.4.9.csv`; VRA properties from `mocho/output/mapping_vra_to_rda.csv`; RiC-O properties from `mocho/output/mapping_rico_to_rda.csv`.
107	
108	---
109	
110	## Decision 4: dc:title — dual-emit with class-specific title predicate
111	
112	**Decision**: For every `dc:title` value, two triples are emitted: `dc:title` (universal cross-WEMI handle) and a class-specific title predicate determined by the target class of the node. The class-specific predicate is looked up from `output/config/lookup_class_prop_alignment.csv` (columns: `edm_class, target_class, wemi, edm_prop, target_prop`). When `target_prop == edm_prop`, only `dc:title` is emitted.
113	
114	**Class-specific predicates for dc:title**:
115	
116	| target_class | wemi | target_prop | Notes |
117	|---|---|---|---|
118	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30134` "has title of manifestation" | rdac classes only |
119	| `rdac:C10001`, `mocho:ImmovableWork`, `mocho:ImageWork`, `ec:EditorialWork` | W | `rdaw:P10088` "has title of work" | rdac-derived mocho classes |
120	| `vra:Image`, `vra:Work` | M/W | `vra:title` | VRA Core has its own title property |
121	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:hasOrHadTitle` | RiC-O; WEMI not applicable |
122	| `aco:AudioManifestation`, `mocho:ImageManifestation`, `mo:Musical*`, `ec:MediaResource`, `doco:*` | M | `dc:title` | No vocab-specific title property; dc:title only |
123	
124	**Rationale**: `dc:title` is declared `rdfs:subPropertyOf dct:title` in mocho's RDA→DCT map (`mapRDA2DCT.ttl`), and `rdam:P30134` / `rdaw:P10088` are declared `rdfs:subPropertyOf dct:title` in the same file. QLever has no OWL reasoner, so the entailment is not materialized from subPropertyOf chains — dual-emit at ingest time is the practical approach. `dc:title` serves as the cross-WEMI query handle; the class-specific property serves WEMI-aware consumers.
125	
126	**W+M nodes**: For W+M assignments (e.g. `rdac:C10001` + `rdac:C10007` from sparte002 Library htype dispatch), `dc:title` + `rdaw:P10088` goes on the Work node; `dc:title` + `rdam:P30134` goes on the Manifestation node — both derived from the same source `dc:title` value.
127	
128	**Source**: `output/config/lookup_class_prop_alignment.csv` — currently populated for `dc:title`; extended as other properties are decided.
129	
130	---
131	
132	## Decision 5: Five predicate remappings — DC/EDM → RDA Manifestation-level
133	
134	**Decision**: The following five source predicates are replaced by their Manifestation-level RDA equivalents. Source rationale: `mocho/output/mapping_dct_to_rda.csv` provides the DC → RDA sub-property mapping; Manifestation-level (`rdam:`) properties are selected per D9.
135	
136	| json_key | Source predicate | Target predicate | Label |
137	|---|---|---|---|
138	| `title` | `dc:title` | `rdam:P30134` | "has title of manifestation" |
139	| `description` | `dc:description` | `rdam:P30137` | "has note on manifestation" |
140	| `date` | `dc:date` | `rdam:P30278` | "has date of manifestation" |
141	| `issued` | `dc:issued` | `rdam:P30278` | "has date of manifestation" (same as `date`) |
142	| `isPartOf` | `dcterms:isPartOf` | `rdam:P30020` | "is part of manifestation" |
143	
144	Note: `dc:title` dual-emit is governed by D4. For `description`, `date`, `issued`, `isPartOf` the source predicate is replaced, not dual-emitted — these do not have the cross-WEMI querying motivation that title has.
145	
146	---
147	
148	## Decision 8: dcterms:alternative — class-specific variant title dispatch
149	
150	**Decision**: `dcterms:alternative` is mapped per target class:
151	
152	| target_class | wemi | target_prop |
153	|---|---|---|
154	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30128` "has variant title of manifestation" |
155	| `rdac:C10001` | W | `rdaw:P10086` "has variant title of work" |
156	| all others | — | `dcterms:alternative` (keep as-is) |
157	
158	**Rationale**: `rdam:P30128` is the correct Manifestation-level variant title property; `rdam:P30131` "has abbreviated title" is too narrow — it implies a formally abbreviated form (e.g. acronym), not a generic alternative title. `rdaw:P10086` is the Work-level parallel. No equivalent found in VRA, RiC-O, MO, or ACO; those classes keep the source predicate. RiC-O uses `rico:hasOrHadTitle` for all title types distinguished by `rico:hasTitleType`, but emitting the same predicate for both main title and alternative would conflate them without type context — keeping `dcterms:alternative` is the safer fallback.
159	
160	**Closes open question from D5.**
161	
162	**Source**: `output/config/lookup_class_prop_alignment.csv` (dcterms:alternative rows).
163	
164	---
165	
166	## Decision 9: dc:date and dc:issued — class-specific date predicate dispatch
167	
168	**Decision**: `dc:date` and `dc:issued` are mapped per target class via `output/config/lookup_class_prop_alignment.csv`. The mapping is:
169	
170	| target_class | wemi | dc:date | dc:issued |
171	|---|---|---|---|
172	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30278` "has date of manifestation" | `rdam:P30011` "has date of publication" |
173	| `mocho:ImageManifestation`, `mocho:ImmovableWork`, `mocho:ImageWork` | M/W | `dc:date` | `dc:issued` |
174	| `rdac:C10001` | W | `rdaw:P10219` "has date of work" | N/A |
175	| `aco:AudioManifestation`, `mo:MusicalManifestation`, `mo:MusicalWork` | M/W | `dc:date` | `dc:issued` |
176	| `doco:*`, `ec:MediaResource`, `ec:EditorialWork` | M/W | `dc:date` | `dc:issued` |
177	| `vra:Image` | M | `vra:dateCreated` | `dc:issued` |
178	| `vra:Work` | W | `vra:dateCreated` | N/A |
179	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:creationDate` | `rico:publicationDate` |
180	
181	**N/A** rows are not emitted — no meaningful publication date applies at Work level in RDA or VRA.
182	
183	**Rationale**:
184	- `rdam:P30278` and `rdam:P30011` are the correct Manifestation-level RDA properties. `dc:date` is a generic date; `dc:issued` specifically denotes publication — `rdam:P30011` "has date of publication" captures this distinction.
185	- `rdac:C10001` Work nodes receive `rdaw:P10219` "has date of work" for `dc:date`; `dc:issued` is not applicable at Work level.
186	- VRA classes use `vra:dateCreated` (approximate to `rdaw:P10219`; confirmed in `mapping_vra_to_rda.csv`).
187	- RiC-O classes use `rico:creationDate` / `rico:publicationDate` — native archival date properties with no RDA equivalent (confirmed "no match" in `mapping_rico_to_rda.csv`).
188	- All other classes (aco, mo, doco, ec, mocho subclasses) keep the source predicate — no date property exists in their respective vocabularies.
189	
190	**Closes open question from D5.**
191	
192	**Source**: `output/config/lookup_class_prop_alignment.csv` (dc:date and dc:issued rows).
193	
194	---
195	
196	## Decision 7: Creator URI resolution — emit dcterms:creator when Agent is DDB org or GND
197	
198	**Decision**: When a `ProvidedCHO.creator` value resolves to an `edm:Agent` whose
199	`about` URI is a DDB organization URI (`http://www.deutsche-digitale-bibliothek.de/organization/…`)
200	or a GND URI (`http://d-nb.info/gnd/…`), emit:
201	
202	```turtle
203	<cho> dcterms:creator <agent.about> .
204	```
205	
206	Resolution is attempted in two steps, in priority order:
207	
208	1. **URI match**: `creator[].resource` == `agent[].about` — direct IRI equality.
209	2. **Label match**: `creator[].$` matched against any `agent[].prefLabel[].$` after
210	   comma-order normalization (`"Lastname, Firstname"` ↔ `"Firstname Lastname"`).
211	   Applied only when step 1 fails or `creator[].resource` is absent.
212	
213	If neither step resolves, fall back to the `rdam:P30329` plain-literal path (D2).
214	
215	**Corpus evidence** (`data/items-excerpt-1000.json`, 488 creator values):
216	- URI match → DDB org / GND: 301 (61.7%)
217	- Label match → DDB org / GND (after normalization): 269 (55.1%)
218	
219	See `notes/corpus-analysis.md §1` and `data/analysis/creator_agent_coverage.csv`.
220	
221	**Rationale**: An IRI-valued `dcterms:creator` provides a stable node for GND/VIAF/Wikidata `owl:sameAs` alignment and a target for Phase 1b `rdaa:` property attachment (`link_gnd_agents.py`), without requiring a separate reconciliation step. `dcterms:creator` is used for the IRI triple (agent as entity); `rdam:P30329` is reserved for the Manifestation-scoped plain-literal fallback (D2).
222	
223	**Closes open question from D2.**
224	
225	---
226	
227	## Decision 10: dc:description — class-specific note predicate dispatch
228	
229	**Decision**: `dc:description` is mapped per target class via `output/config/lookup_class_prop_alignment.csv`:
230	
231	| target_class | wemi | target_prop |
232	|---|---|---|
233	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30137` "has note on manifestation" |
234	| `rdac:C10001` | W | `rdaw:P10330` "has note on work" |
235	| `vra:Image`, `vra:Work` | M/W | `vra:description` |
236	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `rico:note` |
237	| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dc:description` |
238	
239	**Rationale**:
240	- `rdam:P30137` is the most generic Manifestation-level note property in `mapping_dct_to_rda.csv`; no narrower property (e.g. `rdaw:P10109` "has summary") is warranted without knowing whether the source value is a summary, a content note, or a scope note.
241	- `rdaw:P10330` is the Work-level parallel for `rdac:C10001` W nodes.
242	- VRA classes use `vra:description` — a free-text description field with no structural RDA equivalent (confirmed "no match" in `mapping_vra_to_rda.csv`).
243	- RiC-O classes use `rico:note` — native archival note property with no RDA equivalent (confirmed "no match" in `mapping_rico_to_rda.csv`).
244	- All other classes (aco, mo, doco, ec, mocho subclasses) have no description property in their respective vocabularies; the source predicate `dc:description` is retained.
245	
246	**Source**: `mapping_dct_to_rda.csv`, `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`.
247	
248	---
249	
250	## Decision 12: dcterms:isPartOf — class-specific part-relation dispatch
251	
252	**Decision**: `dcterms:isPartOf` is mapped per target class via `output/config/lookup_class_prop_alignment.csv`:
253	
254	| target_class | wemi | target_prop |
255	|---|---|---|
256	| `rdac:C10007`, `mocho:Manifestation` | M | `rdam:P30020` "is part of manifestation" |
257	| `rdac:C10001` | W | `rdaw:P10019` "is part of work" |
258	| `vra:Image`, `vra:Work` | M/W | `vra:partOf` |
259	| `rico:RecordSet`, `rico:Record`, `rico:RecordPart` | — | `dcterms:isPartOf` |
260	| all others (aco, mo, doco, ec, mocho subclasses) | M/W | `dcterms:isPartOf` |
261	
262	**Corpus range** (full corpus, 70,311 values, `data/analysis/ispartof_coverage.csv`):
263	
264	| Kind | n | % |
265	|---|---|---|
266	| Full DDB item URL (`http://…/item/<UUID>`) | 43,814 | 62.3% |
267	| Bare 32-char UUID | 22,265 | 31.7% |
268	| Label-only (no resource) | 4,232 | 6.0% |
269	
270	**IRI sanitisation**: bare 32-char UUIDs must be prefixed with `http://www.deutsche-digitale-bibliothek.de/item/` before emitting. Full DDB URLs are used as-is.
271	
272	**Rationale**:
273	- `rdam:P30020` "is part of manifestation" and `rdaw:P10019` "is part of work" are the direct RDA equivalents at M and W level respectively (confirmed in `mapping_dct_to_rda.csv`).
274	- VRA uses `vra:partOf` — maps to `rdaw:P10019` per `mapping_vra_to_rda.csv`; applies to both `vra:Image` and `vra:Work`.
275	- RiC-O: `rico:isOrWasComponentOf` domain is restricted to `rico:Instantiation`, not `rico:RecordResource` — no clean native equivalent for the Record hierarchy. `dcterms:isPartOf` is kept as a valid queryable fallback.
276	- All other classes have no part-relation property in their vocabularies; `dcterms:isPartOf` is kept.
277	- Label-only values carry no resolvable IRI — emitting a literal object for a property whose range is an IRI would violate the graph model; graph/ddbedm passthrough preserves them without loss.
278	
279	**Source**: `mapping_dct_to_rda.csv`, `mapping_vra_to_rda.csv`, `mapping_rico_to_rda.csv`, `scripts/analyse_ispartof.py`.
280	
281	---
282	
283	## Decision 11: dcterms:language — re-cast LOC URI as rico:Language for RiC-O classes
284	
285	**Decision**: For RiC-O target classes (`rico:RecordSet`, `rico:Record`, `rico:RecordPart`), `dcterms:language` is emitted using `rico:hasOrHadLanguage`. The LOC ISO 639-2 URI (e.g. `http://id.loc.gov/vocabulary/iso639-2/ger`) is additionally typed as `rico:Language` via a stub triple.
286	
287	**Emitted triples** (RiC-O classes only):
288	```turtle
289	<cho>     rico:hasOrHadLanguage <http://id.loc.gov/vocabulary/iso639-2/ger> .
290	<loc-uri> a rico:Language .
291	```
292	
293	For all non-RiC-O classes, `dcterms:language <LOC-URI>` is kept as-is (range `dcterms:LinguisticSystem`).
294	
295	**Rationale**: The LOC ISO 639-2 URIs are authoritative language identifiers. Asserting `rico:Language` on them is a projection into mocho's class space, consistent with how GND URIs are asserted as `mocho:Agent` stubs. The LOC MADS/RDF definition (`madsrdf:Language`) does not prevent additional typing. This enables well-typed `rico:hasOrHadLanguage` triples without minting new URIs.
296	
297	**dc:language** (literal): kept as `dc:language` for all classes including RiC-O. `rico:hasOrHadLanguage` expects a `rico:Language` instance (a URI), not a literal — the literal form has no direct RiC-O equivalent. The literal is retained as a cross-WEMI query handle.
298	
299	**WEMI mismatch note**: Both `dc:language` and `dcterms:language` are Expression-level in RDA (`rdae:P20006` "has language of expression"); no `rdam:` equivalent exists. Language triples are emitted on the Manifestation node as a pragmatic shortcut until Expression nodes are minted. See `transform-future-plan.md §2`.
300	
301	---
302	
303	## Decision 13: edm:Agent — property mapping to mocho:Agent stub
304	
305	**Decision**: All `edm:Agent` nodes are typed as `mocho:Agent` (Phase 0 stub). Properties are mapped per `output/config/lookup_class_prop_alignment.csv` (rows 549–572), generated by `scripts/gen_agent_alignment_rows.py`.
306	
307	**Source namespace note**: DDB uses `gndo:` directly for agent-demographic properties (`gndo:dateOfBirth`, `gndo:dateOfDeath`, `gndo:dateOfEstablishment`, `gndo:dateOfTermination`, `gndo:gender`, `gndo:placeOfBirth`, `gndo:placeOfDeath`, `gndo:professionOrOccupation`, `gndo:biographicalOrHistoricalInformation`). These are passthrough — `edm_prop == target_prop`. The `align_ddbedm_to_mocho.py` script incorrectly resolved these as `edm:` (fallback for properties absent from `ddbedm_1.0.ttl`); the correct namespace is confirmed from `~/Documents/claude/mocho/ontology/gnd_20251218.ttl`.
308	
309	**Non-trivial remappings**:
310	
311	| edm_prop | target_prop | Reason |
312	|---|---|---|
313	| `dc:identifier` | `gndo:gndIdentifier` | GND number literal → GND-native identifier property |
314	| `edm:altLabel` | `skos:altLabel` | `edm:altLabel rdfs:subPropertyOf skos:altLabel`; promote to superclass |
315	| `edm:sameAs` | `owl:sameAs` | EDM declares these equivalent |
316	
317	**Passthrough properties** (no transformation): `gndo:dateOfBirth`, `gndo:dateOfDeath`, `gndo:dateOfEstablishment`, `gndo:dateOfTermination`, `gndo:gender`, `gndo:placeOfBirth`, `gndo:placeOfDeath`, `gndo:professionOrOccupation`, `gndo:biographicalOrHistoricalInformation`, `skos:prefLabel`, `skos:note`, `foaf:name`, `dc:date`, `dc:type`, `dct:hasPart`, `dct:isPartOf`, `edm:begin`, `edm:end`, `edm:hasMet`, `edm:isRelatedTo`, `edm:wasPresentAt`.
318	
319	**Domain mismatches deferred**: `gndo:dateOfEstablishment` / `gndo:dateOfTermination` apply to `gndo:CorporateBody` and `gndo:ConferenceOrEvent`, not `gndo:DifferentiatedPerson`. `edm:begin` / `edm:end` are generic temporals that map to type-specific gndo date properties. Both are emitted as-is under `mocho:Agent` until agent type is resolved. See `transform-future-plan.md §10`.
320	
321	**Source**: `~/Documents/claude/mocho/ontology/gnd_20251218.ttl` (property domain analysis); `output/config/lookup_class_prop_alignment.csv`.
322	
323	---
324	
325	## Decision 6: aggregationEntity and hierarchyPosition — skip, no triple emitted
326	
327	**Decision**: `ddb:aggregationEntity` (boolean string `"true"`/`"false"`) and `ddb:hierarchyPosition` (zero-padded sort key, e.g. `"000000000014848"`) are not emitted as triples.
328	
329	**Rationale**: Both are DDB-internal fields with no mocho/RDA equivalent. `aggregationEntity` is a grouping flag used by the DDB portal UI. `hierarchyPosition` is a sort key for the display hierarchy. Neither carries semantic content useful to downstream graph consumers.
330	
331	---
332	
333	## Decision 14: edm:hasMet on ProvidedCHO — skip in mocho graph, passthrough in ddbedm
334	
335	**Decision**: The `hasMet` JSON key on `ProvidedCHO` is excluded from the mocho graph via `_MOCHO_SKIP`. It is retained verbatim in the ddbedm passthrough graph as `ddbedm:hasMet` (`http://www.deutsche-digitale-bibliothek.de/edm/hasMet`).
336	
337	**Background**: `edm:hasMet` on a ProvidedCHO links the object to related events, places, or concepts encountered by the object (or its creator). In the mocho graph there is no RDA/mocho alignment for this relationship at the CHO level. The property also appears in the LIDO contributor resolution chain (D3), where `ProvidedCHO.hasMet[].resource` is used to navigate to the `edm:Event` node — but the `hasMet` triple itself is not emitted on the mocho CHO.
338	
339	**Note**: `edm:hasMet` on `edm:Agent` stubs is passthrough per D13 — the skip applies only to ProvidedCHO in the mocho graph.
340	
341	**Implementation**: `"hasMet"` added to `_MOCHO_SKIP` in `constants.py`. `emit_ddbedm_triples` continues to emit it unchanged on the ddbedm graph subject.
342	
343	---
344	
345	## Decision 15: ddbedm:hierarchyType — emit as vocnet-htype: IRI in mocho graph
346	
347	**Decision**: When `ProvidedCHO.hierarchyType` is present, `retype_entities()` emits one additional triple in the mocho graph:
348	
349	```turtle
350	<cho> ddbedm:hierarchyType vocnet-htype:htype_021 .
351	```
352	
353	where:
354	- `ddbedm:hierarchyType` = `http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType`
355	- `vocnet-htype:` = `http://ddb.vocnet.org/hierarchietyp/`
356	
357	The htype code (e.g. `"htype_021"`) is the local name of the vocnet-htype individual. This triple is emitted for every record with a non-empty `hierarchyType` value, regardless of whether the code drove the rdf:type dispatch (i.e. whether `use_htype=True` for the record's sector/mediatype row). The rdf:type dispatch outcome is independent — a record may receive a htype-derived class (layer 1 in `retype_entities`) and still always receive the `ddbedm:hierarchyType` triple.
358	
359	**Rationale**: The htype code identifies the DDB document hierarchy position type (e.g. volume, chapter, article) and is the primary facet for hierarchical navigation in GeMeA. Emitting it as an IRI (not a literal) enables direct join to the vocnet-htype individuals in QLever without string normalization. The property IRI `ddbedm:hierarchyType` (in the DDB EDM extension namespace) is also used in the ddbedm passthrough graph, ensuring the predicate is consistent across both graphs.
360	
361	**IRI correction**: The earlier `_DDBEDM_PROP` entry used `http://www.deutsche-digitale-bibliothek.de/hierarchyType` (no `/edm/`). This was corrected to `http://www.deutsche-digitale-bibliothek.de/edm/hierarchyType` as part of this decision. `DDBEDM_NS = "http://www.deutsche-digitale-bibliothek.de/edm/"` is defined as a named constant and `ddbedm:` added to `_PREFIXES`.
362	
363	**Scope**: `hierarchyType` is in `_MOCHO_SKIP` — the generic property loop does not emit it. The triple is emitted exclusively by `retype_entities`. `hierarchyPosition` and `aggregationEntity` remain skipped per D6.
364	
```

---

### Assistant *(2026-05-07T15:58:26.297Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md",
  "old_string": "**Scope**: `hierarchyType` is in `_MOCHO_SKIP` — the generic property loop does not emit it. The triple is emitted exclusively by `retype_entities`. `hierarchyPosition` and `aggregationEntity` remain skipped per D6.",
  "new_string": "**Scope**: `hierarchyType` is in `_MOCHO_SKIP` — the generic property loop does not emit it. The triple is emitted exclusively by `retype_entities`. `hierarchyPosition` and `aggregationEntity` remain skipped per D6.\n\n---\n\n## Decision 16: Stub label predicate — `rdfs:label` over `skos:prefLabel`\n\n**Decision**: Label stubs emitted in the mocho graph for referenced context entities (Agent, Place, Concept) use `rdfs:label`, not `skos:prefLabel`, even when the source JSON field is named `prefLabel`.\n\n**Affected emitters**: `emit_subject_triples`, `emit_hastype_triples`, `emit_current_location_triples`, `emit_creator_triples`, `emit_contributor_triples`, `emit_place_stubs`.\n\n**Rationale**:\n- The JSON `prefLabel` field name is a DDB EDM convention, not a SKOS assertion. The mocho graph does not copy the SKOS semantics implied by that field name.\n- These are convenience stubs for display and search — not full SKOS concept descriptions. Full `skos:prefLabel` triples will come from the GND enrichment graph (Phase 1b).\n- QLever text-indexes against `rdfs:label` by default. Using it directly ensures stubs are full-text-searchable without configuration changes.\n- QLever does not materialise RDFS/OWL entailments (`skos:prefLabel rdfs:subPropertyOf rdfs:label`), so asserting `skos:prefLabel` would not automatically make stubs retrievable via `rdfs:label` queries. Asserting `rdfs:label` is the pragmatic approach.\n\n**Harm of not using `skos:prefLabel`**: SPARQL queries filtering specifically on `skos:prefLabel` will not find mocho stub labels. This is acceptable: once the GND enrichment graph is loaded, proper `skos:prefLabel` triples from GND will be available there; the mocho stub is intentionally a weaker, provisional label.\n\n---\n\n## Decision 17: Context entity stubs — no `rdf:type` in mocho for Place, Concept, Timespan\n\n**Decision**: When the mocho graph emits stub triples for context entities referenced by a CHO (a label or property triple whose subject is not the CHO itself), the following typing policy applies:\n\n| Context entity | Type asserted in mocho | Reason |\n|---|---|---|\n| Agent (creator, contributor) | `mocho:Agent` | mocho-specific alignment type; uniform query handle across WEMI levels; distinct from `edm:Agent` / `foaf:Agent` in ddbedm |\n| Place (`edm:currentLocation`) | none | `edm:Place` already asserted in ddbedm; no mocho-specific Place type |\n| Concept (`dcterms:subject`, `edm:hasType`) | none | `skos:Concept` already asserted in ddbedm; no mocho-specific Concept type |\n| Timespan | none | not yet emitted as stubs; same policy will apply when introduced |\n\n**Rationale**:\n- QLever's default graph is the union of all named graphs. A query without a `GRAPH` filter will find `edm:Place` from ddbedm, `mocho:Agent` from mocho, and `skos:Concept` from ddbedm — cross-graph typing is transparent to consumers.\n- Agent stubs are an exception because `mocho:Agent` is a mocho-internal type with no counterpart in EDM or any source vocabulary. It is needed for uniform federated querying (`?x a mocho:Agent`) across records that use different Agent superclasses (`foaf:Agent`, GND entity classes). Re-asserting it from the ddbedm graph is not possible since ddbedm uses `edm:Agent`, not `mocho:Agent`.\n- Adding `edm:Place` or `skos:Concept` in mocho would be redundant cross-graph re-assertions with no query benefit. It would also inflate the mocho graph with triples whose authority belongs in ddbedm."
}
```

---

### User *(2026-05-07T15:58:30.524Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-props-mapping-adr.md has been updated successfully.
```

---

### Assistant *(2026-05-07T15:58:36.415Z)*

D16 and D17 added. Summary of each:

- **D16** — `rdfs:label` over `skos:prefLabel` for mocho stubs: the JSON `prefLabel` field name is a DDB convention, not a SKOS assertion; QLever text-indexes on `rdfs:label`; QLever doesn't materialise subPropertyOf entailments so using `skos:prefLabel` would silently break label queries. Full SKOS labels come from the GND enrichment graph (Phase 1b).

- **D17** — No `rdf:type` for Place/Concept/Timespan stubs in mocho: their type is already authoritative in ddbedm and visible via QLever's default (union) graph. Agent stubs are the only exception because `mocho:Agent` is a mocho-internal type that can't be inferred from ddbedm's `edm:Agent` — it exists specifically for uniform cross-WEMI querying.

---

### User *(2026-05-07T16:05:13.889Z)*

before you implement the changes, confirm that the named graphs are gemea.ise.fiz-karlsruhe.de/graph/<ddbedm, mocho, prov, work>

---

### Assistant *(2026-05-07T16:05:19.804Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"GRAPH\\|graph_iri\\|gemea\\|ise.fiz\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py | head -20",
  "description": "Check named graph IRIs in constants"
}
```

---

### User *(2026-05-07T16:05:19.862Z)*

**Tool result**
```
31:GRAPH_DDBEDM = "https://gemea.ise.fiz-karlsruhe.de/graph/ddbedm"
32:GRAPH_MOCHO  = "https://gemea.ise.fiz-karlsruhe.de/graph/mocho"
33:GRAPH_PROV   = "https://gemea.ise.fiz-karlsruhe.de/graph/prov"
37:GEMEA_BASE    = "https://gemea.ise.fiz-karlsruhe.de/mocho/"
56:MOCHO_NS = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#"
72:MOCHO_ISIL      = "https://ise-fizkarlsruhe.github.io/ddbkg/mocho#isil"
```

---

### Assistant *(2026-05-07T16:05:24.946Z)*

Three named graphs confirmed: `ddbedm`, `mocho`, `prov`. There is no `work` graph defined — `GRAPH_WORK` is absent from `constants.py`. Is `work` a fourth graph that needs to be added, or did you mean the three existing ones are correct as-is?

---

### User *(2026-05-07T16:06:53.854Z)*

work graph will be the destination of the werk staging dnb linking

---

### Assistant *(2026-05-07T16:06:58.893Z)*

Confirmed. Current three graphs are correct for the current implementation scope:

- `GRAPH_DDBEDM` — verbatim EDM passthrough
- `GRAPH_MOCHO` — mocho-aligned triples
- `GRAPH_PROV` — PROV-O Layer 1

`GRAPH_WORK` (`…/graph/work`) will be added when the werk-staging → DNB-linking pipeline (Phase 1b) is implemented. Nothing to add now.

Ready to proceed with implementation?

---

### User *(2026-05-07T16:07:42.091Z)*

where in the transform script is the parallelization happening?

---

### Assistant *(2026-05-07T16:07:46.461Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"parallel\\|worker\\|Process\\|Pool\\|thread\\|concurrent\\|multiprocess\" /Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py /Users/mta/Documents/claude/goethe-faust/scripts/transform/transform.py 2>/dev/null | head -20",
  "description": "Search for parallelization in transform scripts"
}
```

---

### User *(2026-05-07T16:07:46.525Z)*

**Tool result**
```
/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py:91:                    help="Skip first N rows in SQLite (for parallel workers; use with --db and --limit)")
```

---

### Assistant *(2026-05-07T16:07:52.387Z)*

It isn't. The transform script is single-threaded. Parallelization is done externally — you run one `python -m transform` process per sector JSONL file, as separate OS processes. The `--skip` flag in `__main__.py` is a residual hint for a SQLite-based parallel worker approach that was planned but dropped (see §2.1 of `transform-implementation-actual.md`).

The actual parallel execution pattern (from `transform-dryrun-plan.md §5.2`) is:

```bash
for n in 1 2 3 4 5 6 7; do
  python -m transform --jsonl s${n}.jsonl --outdir output/gemea/s${n}/ &
done
wait
```

One OS process per sector, no shared state, outputs go to separate directories.

---

### User *(2026-05-07T16:09:02.534Z)*

this is my problem, because then at the end, i have to collect all the files. where could parallelization be placed and how much change would it require?

---

### Assistant *(2026-05-07T16:09:21.720Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/__main__.py"
}
```

---

### User *(2026-05-07T16:09:21.737Z)*

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
79	    parser = argparse.ArgumentParser(
80	        description="Transform DDB-EDM JSONL to mocho N-Quads (§8)"
81	    )
82	
83	    io = parser.add_argument_group("I/O")
84	    io.add_argument("--jsonl",  type=Path, default=DEFAULT_JSONL,
85	                    help="JSONL input file (one DDB-EDM JSON object per line); "
86	                         "default: data/items-all-goethe-faust.json")
87	    io.add_argument("--db",     type=Path, default=None,
88	                    help="SQLite sector file — reads directly without intermediate JSONL export; "
89	                         "mutually exclusive with --jsonl")
90	    io.add_argument("--offset", type=int,  default=0,
91	                    help="Skip first N rows in SQLite (for parallel workers; use with --db and --limit)")
92	    io.add_argument("--ids",    type=str,  default=None,
93	                    help="Path to ID allowlist file (one 32-char DDB ID per line), "
94	                         "or '-' to read from stdin; omit to process all records")
95	    io.add_argument("--outdir", type=Path, default=None,
96	                    help="Output directory; auto-timestamped if omitted "
97	                         "(default: output/transform/YYYYMMDD_HHMMSS)")
98	
99	    cfg = parser.add_argument_group("Config")
100	    cfg.add_argument("--alignment", type=Path, default=DEFAULT_ALIGNMENT,
101	                     help="Property alignment lookup CSV "
102	                          "(target_class, edm_prop) → mocho property; "
103	                          "default: output/config/lookup_class_prop_alignment.csv")
104	    cfg.add_argument("--lido",      type=Path, default=DEFAULT_LIDO,
105	                     help="LIDO event type dispatch CSV "
106	                          "(event URI → agent predicates per WEMI level); "
107	                          "default: output/config/lido_event_types.csv")
108	    cfg.add_argument("--htype",     type=Path, default=DEFAULT_HTYPE,
109	                     help="htype → class lookup CSV "
110	                          "(htype_code → rdf:type IRIs for §1.1 dispatch); "
111	                          "default: output/config/lookup_htype_doco_rico.csv")
112	    cfg.add_argument("--mediatype", type=Path, default=DEFAULT_MEDIATYPE,
113	                     help="Mediatype × sector → class lookup CSV "
114	                          "(sector, mediatype → WEMI class IRIs); "
115	                          "default: output/config/lookup_mediatype_class.csv")
116	    cfg.add_argument("--audio",     type=Path, default=DEFAULT_AUDIO,
117	                     help="mt001 dc:type → audio group JSON "
118	                          "(dc:type value → A/B/C group for audio class dispatch); "
119	                          "default: output/config/audio_type2class.json")
120	
121	    run = parser.add_argument_group("Run control")
122	    run.add_argument("--stats",     choices=["none", "basic", "dispatch", "full"],
123	                     default="basic",
124	                     help="Stats verbosity written to transform_stats.json: "
125	                          "none=nothing written, basic=run/records/triples/werk_staging, "
126	                          "dispatch=basic+WEMI class counts (recommended for full-corpus runs), "
127	                          "full=dispatch+per-predicate mocho counts (slow — use with --limit); "
128	                          "default: basic")
129	    run.add_argument("--log-level", default="INFO",
130	                     choices=["DEBUG", "INFO", "WARNING", "ERROR"],
131	                     dest="log_level",
132	                     help="Console and file log verbosity; default: INFO")
133	    run.add_argument("--limit",        type=int, default=None,
134	                     help="Stop after N records — for smoke-testing and sampling")
135	    run.add_argument("--total",        type=int, default=None,
136	                     help="Expected total records — enables ETA in progress log")
137	    run.add_argument("--log-interval", type=int, default=100_000, dest="log_interval",
138	                     help="Log a progress line every N records (default: 100000)")
139	    run.add_argument("--debug",     action="store_true",
140	                     help="Enable DEBUG logging (shorthand for --log-level DEBUG)")
141	
142	    args = parser.parse_args()
143	    if args.debug:
144	        args.log_level = "DEBUG"
145	
146	    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
147	    outdir = args.outdir or (DEFAULT_OUTPUT_BASE / ts)
148	    outdir.mkdir(parents=True, exist_ok=True)
149	
150	    if args.db:
151	        stem = args.db.stem + (f"-{args.offset}" if args.offset else "")
152	    else:
153	        stem = Path(args.jsonl).stem
154	    out_path    = outdir / f"{stem}.nq"
155	    werk_path   = outdir / f"{stem}-werk-staging.duckdb"
156	    stats_path  = outdir / f"{stem}-stats.json"
157	    errors_path = outdir / f"{stem}-errors.jsonl"
158	    log_path    = outdir / f"{stem}.log"
159	
160	    logging.basicConfig(
161	        filename=str(log_path),
162	        level=getattr(logging, args.log_level),
163	        format="%(asctime)s %(levelname)s %(message)s",
164	    )
165	    log = logging.getLogger(__name__)
166	
167	    log.info("Loading config tables")
168	    class_prop_align    = load_class_prop_alignment(args.alignment)
169	    lido_dispatch       = load_lido_event_types(args.lido)
170	    htype_map           = load_htype_map(args.htype)
171	    mediatype_class_map = load_mediatype_class(args.mediatype)
172	    audio_type2class    = load_audio_type2class(args.audio)
173	
174	    ids_set: set[str] | None = None
175	    if args.ids == "-":
176	        ids_set = {line.strip() for line in sys.stdin if line.strip()}
177	    elif args.ids:
178	        ids_set = load_ids(Path(args.ids))
179	
180	    try:
181	        import duckdb
182	        conn = duckdb.connect(str(werk_path))
183	    except ImportError:
184	        log.warning("duckdb not available — werk_staging will not be written")
185	        conn = None
186	    if conn is not None:
187	        conn.execute("""
188	        CREATE TABLE IF NOT EXISTS werk_staging (
189	            ddb_obj_id       VARCHAR PRIMARY KEY,
190	            cho_uri          VARCHAR,
191	            target_class     VARCHAR,
192	            dc_title         VARCHAR,
193	            dc_alternative   VARCHAR[],
194	            dc_created       VARCHAR,
195	            creator_uris     VARCHAR[],
196	            creator_literals VARCHAR[]
197	        )
198	    """)
199	
200	    stats_level = args.stats
201	
202	    stats:  Counter = Counter()
203	
204	    class_counts: dict[str, Counter] = {"W": Counter(), "E": Counter(), "M": Counter(), "": Counter()}
205	    mt_dist:         Counter = Counter()
206	    ht_dist:         Counter = Counter()
207	    ddbedm_cls:      Counter = Counter()
208	    ddbedm_preds:    Counter = Counter()
209	    mocho_preds_all: Counter = Counter()
210	    mocho_preds_new: Counter = Counter()
211	    werk_by_class:   Counter = Counter()
212	
213	    start_time = time.monotonic()
214	    interrupted = False
215	
216	    def _iter_input():
217	        if args.db:
218	            import gzip
219	            import sqlite3 as _sqlite3
220	            conn = _sqlite3.connect(str(args.db))
221	            try:
222	                q = "SELECT uid, bufgz FROM objs"
223	                if args.offset:
224	                    q += f" LIMIT -1 OFFSET {args.offset}"
225	                for uid, buf in conn.execute(q):
226	                    try:
227	                        yield json.dumps(json.loads(gzip.decompress(buf)))
228	                    except Exception as exc:
229	                        log.warning("%s uid=%s: %s", args.db.name, uid, exc)
230	                        yield ""
231	            finally:
232	                conn.close()
233	        else:
234	            with open(args.jsonl, encoding="utf-8") as f:
235	                yield from f
236	
237	    with open(out_path, "w", encoding="utf-8") as out, \
238	         open(errors_path, "w", encoding="utf-8") as err_fh:
239	
240	        for line_no, raw in enumerate(_iter_input(), 1):
241	            if _stop:
242	                interrupted = True
243	                log.warning("Interrupted at line %d — writing partial output", line_no)
244	                break
245	
246	            raw = raw.strip()
247	            if not raw:
248	                continue
249	            if args.limit and line_no > args.limit:
250	                break
251	
252	            try:
253	                record = json.loads(raw)
254	            except json.JSONDecodeError as exc:
255	                entry = {"line": line_no, "issue": f"JSON parse error: {exc}"}
256	                err_fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
257	                stats["json_errors"] += 1
258	                continue
259	
260	            obj_id = get_object_id(record) or f"line:{line_no}"
261	            try:
262	                streams, werk_row, dispatch_info, pred_info = transform_record(
263	                    record, ids_set,
264	                    mediatype_class_map, htype_map, audio_type2class,
265	                    class_prop_align, lido_dispatch,
266	                )
267	            except Exception as exc:
268	                entry = {
269	                    "id":        obj_id,
270	                    "issue":     str(exc),
271	                    "traceback": traceback.format_exc(),
272	                }
273	                err_fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
274	                stats["record_errors"] += 1
275	                continue
276	
277	            if not streams:
278	                stats["filtered"] += 1
279	                continue
280	
281	            for graph_name, graph_lines in streams.items():
282	                for nq in graph_lines:
283	                    out.write(nq + "\n")
284	                    stats["triples_total"] += 1
285	                    stats[f"triples_{graph_name}"] += 1
286	
287	            stats["records_processed"]  += 1
288	            stats["uri_sanitized"]      += pred_info.get("uri_sanitized",   0)
289	            stats["uri_split"]          += pred_info.get("uri_split",       0)
290	            stats["uri_about_split"]    += pred_info.get("uri_about_split", 0)
291	
292	            if stats_level in ("dispatch", "full"):
293	                if dispatch_info.get("is_mt007"):
294	                    stats["skipped_mt007"] += 1
295	                elif dispatch_info.get("fallback"):
296	                    stats["dispatch_fallback"] += 1
297	                elif dispatch_info.get("htype_used"):
298	                    stats["dispatch_htype"] += 1
299	                else:
300	                    stats["dispatch_mediatype"] += 1
301	
302	                tc = dispatch_info.get("target_class", "")
303	                if tc:
304	                    wemi = dispatch_info.get("wemi", "M")
305	                    class_counts[wemi][_to_curie(tc)] += 1
306	
307	                mt = (dispatch_info.get("mediatype", "") or "").split("/")[-1]
308	                if mt:
309	                    mt_dist[mt] += 1
310	
311	                rdf_top = record["edm"]["RDF"]
312	                cho_raw = rdf_top.get("ProvidedCHO") or {}
313	                if isinstance(cho_raw, list):
314	                    cho_raw = cho_raw[0] if cho_raw else {}
315	                raw_ht = (cho_raw.get("hierarchyType") or "").strip()
316	                if raw_ht:
317	                    ht_dist[raw_ht.replace("htype_", "ht")] += 1
318	
319	                ddbedm_cls.update(pred_info["ddbedm_classes"])
320	                ddbedm_preds.update(pred_info["ddbedm_preds"])
321	                mocho_preds_all.update(pred_info["mocho_preds_all"])
322	                mocho_preds_new.update(pred_info["mocho_preds_new"])
323	
324	            if werk_row and conn is not None:
325	                conn.execute(
326	                    "INSERT OR REPLACE INTO werk_staging VALUES (?,?,?,?,?,?,?,?)",
327	                    [
328	                        werk_row["ddb_obj_id"],
329	                        werk_row["cho_uri"],
330	                        werk_row["target_class"],
331	                        werk_row["dc_title"],
332	                        werk_row["dc_alternative"],
333	                        werk_row["dc_created"],
334	                        werk_row["creator_uris"],
335	                        werk_row["creator_literals"],
336	                    ],
337	                )
338	                stats["werk_staging_rows"] += 1
339	                werk_by_class[_to_curie(werk_row["target_class"])] += 1
340	
341	            processed = stats["records_processed"]
342	            if args.log_interval and processed and processed % args.log_interval == 0:
343	                elapsed = time.monotonic() - start_time
344	                rate    = processed / elapsed if elapsed > 0 else 0
345	                errors  = stats["json_errors"] + stats["record_errors"]
346	                eta_str = ""
347	                if args.total and rate > 0:
348	                    remaining = (args.total - processed) / rate
349	                    eta_str   = f" | ETA {_fmt_duration(remaining)}"
350	                total_str = f"/{args.total:,}" if args.total else ""
351	                log.info(
352	                    "Progress: %s%s records | triples %d | errors %d"
353	                    " | %.0f rec/s | elapsed %s%s",
354	                    f"{processed:,}", total_str,
355	                    stats["triples_total"], errors,
356	                    rate, _fmt_duration(elapsed), eta_str,
357	                )
358	
359	    if conn is not None:
360	        conn.close()
361	
362	    elapsed_total = time.monotonic() - start_time
363	
364	    if stats_level != "none":
365	        stats_out: dict = {
366	            "run": {
367	                "timestamp":   ts,
368	                "input":       str(args.jsonl),
369	                "stats_level": stats_level,
370	                "elapsed_s":   round(elapsed_total, 1),
371	                "interrupted": interrupted,
372	            },
373	            "records": {
374	                "processed":          stats["records_processed"],
375	                "skipped_not_in_ids": stats["filtered"],
376	                "by_mediatype": dict(mt_dist.most_common()),
377	                "by_htype":     dict(ht_dist.most_common()),
378	                "uri_sanitized":   stats["uri_sanitized"],
379	                "uri_split":       stats["uri_split"],
380	                "uri_about_split": stats["uri_about_split"],
381	                "errors": {
382	                    "json_parse": stats["json_errors"],
383	                    "transform":  stats["record_errors"],
384	                },
385	            },
386	            "triples": {
387	                "total":    stats["triples_total"],
388	                "by_graph": {
389	                    "ddbedm": stats["triples_ddbedm"],
390	                    "mocho":  stats["triples_mocho"],
391	                    "prov":   stats["triples_prov"],
392	                },
393	            },
394	            "werk_staging": {
395	                "rows":     stats["werk_staging_rows"],
396	                "by_class": dict(werk_by_class.most_common()),
397	            },
398	        }
399	
400	        if stats_level in ("dispatch", "full"):
401	            stats_out["dispatch"] = {
402	                "htype_hits":            stats["dispatch_htype"],
403	                "mediatype_hits":        stats["dispatch_mediatype"],
404	                "fallback_d9":           stats["dispatch_fallback"],
405	                "skipped_mt007":         stats["skipped_mt007"],
406	                "work_classes":          dict(class_counts["W"].most_common()),
407	                "expression_classes":    dict(class_counts["E"].most_common()),
408	                "manifestation_classes": dict(class_counts["M"].most_common()),
409	                "rico_classes":          dict(class_counts[""].most_common()),
410	            }
411	            stats_out["ddbedm_classes"] = dict(ddbedm_cls.most_common())
412	            stats_out["ddbedm_vocab"]   = {"properties_all": dict(ddbedm_preds.most_common())}
413	            stats_out["mocho_vocab"]    = {
414	                "properties_all": dict(mocho_preds_all.most_common()),
415	                "properties_new": dict(mocho_preds_new.most_common()),
416	            }
417	
418	        with open(stats_path, "w", encoding="utf-8") as f:
419	            json.dump(stats_out, f, indent=2)
420	
421	    status = "Interrupted" if interrupted else "Done"
422	    log.info(
423	        "%s: %d records in %s (%.0f rec/s) | triples %d (mocho %d) | errors %d",
424	        status,
425	        stats["records_processed"],
426	        _fmt_duration(elapsed_total),
427	        stats["records_processed"] / elapsed_total if elapsed_total > 0 else 0,
428	        stats["triples_total"],
429	        stats["triples_mocho"],
430	        stats["record_errors"] + stats["json_errors"],
431	    )
432	
433	
434	if __name__ == "__main__":
435	    main()
436	
```

---

### Assistant *(2026-05-07T16:09:46.023Z)*

There's no parallelism in the script — it's a single sequential loop (line 240). `transform_record()` is called once per record, results are written directly to a single open file handle.

Two realistic options:

---

**Option A — `ProcessPoolExecutor` inside `__main__.py`**

`transform_record()` is already a pure function with no shared state, which makes this straightforward.

Structure:
1. Load config tables once in the main process (already done at lines 168–172)
2. Pass them to workers via `initializer` (copied once per worker at fork, not per record)
3. Replace the `for line_no, raw in enumerate(...)` loop with batch submission to the pool
4. Collect `(streams, werk_row, dispatch_info, pred_info)` tuples in the main process
5. Main process does all file writes and counter updates

The DuckDB connection and the stats `Counter` stay in the main process — workers return data, they don't write.

**Effort**: ~120 lines changed/added in `__main__.py` only. No changes to `transform.py`, `emitters.py`, or any other module. `transform_record()` is already the right interface.

**One wrinkle**: `_stop` (SIGINT handler) needs to cancel the pool via `executor.shutdown(cancel_futures=True)`. Manageable.

---

**Option B — add a `merge` subcommand, keep external parallelism as-is**

The transform script stays unchanged. A small `python -m transform merge --indir DIR --out combined.nq` script:
- `cat`s all `.nq` shards into one file
- Merges DuckDB staging tables (`INSERT INTO ... SELECT * FROM ...`)
- Sums stats JSONs into a combined report

**Effort**: ~60 lines, new file `merge.py`. Zero changes to existing code.

---

**Trade-off**:

| | Option A | Option B |
|---|---|---|
| Single invocation | yes | no (still two steps) |
| Code change | moderate (`__main__.py`) | minimal (new file only) |
| Debugging | harder (worker pickling errors, pool teardown) | easy |
| Scales to 18.5M records | yes, native | yes, same as current |
| Risk to existing code | low but nonzero | zero |

For a pipeline you'll run once or a few times on a known corpus, Option B is faster to add and harder to break. Option A makes sense if single-command operation matters for reproducibility or handoff to others.

---

### User *(2026-05-07T16:33:41.025Z)*

put this in future plan section inside transform-implementation-plan. put a date when this was brought up

---

### Assistant *(2026-05-07T16:33:45.250Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"^## \\|^### \\|future\\|parallel\\|worker\" /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md | head -30",
  "description": "Find section headings and future/parallel mentions in transform-implementation-plan"
}
```

---

### User *(2026-05-07T16:33:45.376Z)*

**Tool result**
```
3:## §0 Context
13:## §1 Critical files
29:## §2 New constants
67:## §3 Prefix table for CURIE expansion
92:## §4 New loaders
94:### §4.1 `load_class_prop_alignment(path)` → `dict[(target_class_curie, edm_prop_curie), target_prop_iri]`
97:### §4.2 `load_lido_event_types(path)` → `dict[lido_uri_str, dict[col_name, expanded_iri]]`
100:### §4.3 `load_mediatype_class(path)` → `dict[(sparte_iri, mediatype_iri), row_dict]`
103:### §4.4 `load_audio_type2class(path)` → `dict[(sector_iri, dc_type_de), group_char]`
108:## §5 New utility functions
110:### §5.1 `make_nq(s_nt, p_nt, o_nt, graph_iri)` → `str`
113:### §5.2 `coerce_list(val)` → `list`
116:### §5.3 `mint_cho_uri(obj_id)` → `str`
119:### §5.4 `mint_bare_id(entity_class, raw_id)` → `str`
122:### §5.5 `normalize_date(s)` → `list[str]`
125:### §5.6 `resolve_agent(label, resource, agents_index)` → `dict | None`
128:### §5.7 `is_ddb_or_gnd(uri)` → `bool`
133:## §6 Handler functions
137:### §6.1 `emit_ddbedm_triples(rdf, record, graph_iri)` — stream [1], D20
141:### §6.2 `emit_prov_triples(record, ddb_cho_uri, graph_iri)` — stream [4], D11/D12
154:### §6.3 `emit_mocho_triples(...)` — stream [2] orchestrator
163:### §6.4 `retype_entities()` — refactor of existing
171:### §6.5 `emit_subject_triples()` — update (D1 amended)
175:### §6.6 `emit_creator_triples(cho_nt, creator_values, agents_index, target_class, class_prop_align, graph_iri)` — D2 / props-mapping §4
181:### §6.7 `emit_contributor_triples(cho_nt, contributor_values, event_participant_index, lido_dispatch, target_class, wemi, graph_iri)` — D3/D25, props-mapping §5
201:### §6.8 `emit_aggregation_triples(agg, cho_nt, graph_iri)` — D23
209:### §6.9 `emit_place_stubs(places, graph_iri)` — D24
213:### §6.10 `werk_staging_row(cho_uri, cho_entity, target_class)` → `dict | None` — D26
219:## §7 Core transform restructure
221:### §7.1 `transform_record(record, ...)` → `tuple[dict[str, list[str]], dict|None]`
```

---

### Assistant *(2026-05-07T16:33:48.799Z)*

**Tool call:** `Bash`
```json
{
  "command": "tail -30 /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "description": "Read the end of transform-implementation-plan.md"
}
```

---

### User *(2026-05-07T16:33:48.872Z)*

**Tool result**
```
# 99.5% of dc:spatial URIs duplicate Event.happenedAt — no event traversal needed
```

### §13.2 Registry (dict of callables)

The main property loop in `emit_mocho_triples()` must branch for ~6 properties with special handling. An if/elif chain grows brittle as properties are added. Use a registry instead:

```python
SPECIAL_HANDLERS = {
    "creator":        emit_creator_triples,
    "contributor":    emit_contributor_triples,
    "dcSubject":      emit_subject_triples,
    "dcTermsSubject": emit_subject_triples,
    "dcTermSubject":  emit_subject_triples,
    "dcType":         emit_dctype_triples,
}

for prop, val in cho.items():
    handler = SPECIAL_HANDLERS.get(prop)
    if handler:
        lines += handler(cho_nt, val, ...)
    else:
        lines += emit_generic_triple(cho_nt, prop, val, class_prop_align, ...)
```

Adding a new special case = one entry in the registry + one new function. The generic path handles all remaining properties via `class_prop_align` lookup.

### §13.3 Pipeline

`transform_record()` calls independent stream emitters in sequence — `emit_ddbedm_triples`, `emit_mocho_triples`, `emit_prov_triples` — each returning a list of N-Quad lines. The four output streams are fully decoupled: mt007 guard applies only to mocho and werk_staging; ddbedm and prov always run. See `§7.1`.
```

---

### Assistant *(2026-05-07T16:33:51.441Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"^## §\" /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md | tail -10",
  "description": "Find the last section numbers"
}
```

---

### User *(2026-05-07T16:33:51.524Z)*

**Tool result**
```
133:## §6 Handler functions
219:## §7 Core transform restructure
246:## §8 CLI changes
261:## §9 Output file structure (POC)
272:## §9.1 DuckDB werk_staging table schema
291:## §10 Implementation order
306:## §11 Verification
344:## §12 Testing and validation style
394:## §13 Design patterns
404:## §14 Coding style
```

---

### Assistant *(2026-05-07T16:33:54.677Z)*

**Tool call:** `Bash`
```json
{
  "command": "grep -n \"^## §14\\|^## §15\\|future\" /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md | head -10",
  "description": "Check §14 and any existing future section"
}
```

---

### User *(2026-05-07T16:33:54.719Z)*

**Tool result**
```
404:## §14 Coding style
```

---

### Assistant *(2026-05-07T16:33:57.265Z)*

**Tool call:** `Bash`
```json
{
  "command": "tail -5 /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "description": "Read the last few lines of the plan"
}
```

---

### User *(2026-05-07T16:33:57.304Z)*

**Tool result**
```
Adding a new special case = one entry in the registry + one new function. The generic path handles all remaining properties via `class_prop_align` lookup.

### §13.3 Pipeline

`transform_record()` calls independent stream emitters in sequence — `emit_ddbedm_triples`, `emit_mocho_triples`, `emit_prov_triples` — each returning a list of N-Quad lines. The four output streams are fully decoupled: mt007 guard applies only to mocho and werk_staging; ddbedm and prov always run. See `§7.1`.
```

---

### Assistant *(2026-05-07T16:34:00.131Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "offset": 404,
  "limit": 20
}
```

---

### User *(2026-05-07T16:34:00.173Z)*

**Tool result**
```
404	## §14 Coding style
405	
406	Target audience: mid-level to senior programmers reading the script cold. Optimize for clarity first; micro-optimizations only where profiling shows a bottleneck.
407	
408	### §14.1 Type hints — everywhere
409	
410	All function signatures carry type hints. Use `type aliases` for recurring types:
411	
412	```python
413	NQuad     = str          # one N-Quads line
414	NQList    = list[NQuad]  # return type of all emit_* handlers
415	AgentDict = dict[str, Any]
416	PropAlign = dict[tuple[str, str], str]  # (target_class, edm_prop) → target_prop_iri
417	```
418	
419	```python
420	def emit_creator_triples(
421	    cho_nt: str,
422	    creator_values: list[dict],
423	    agents_index: dict[str, AgentDict],
```

---

### Assistant *(2026-05-07T16:34:03.444Z)*

**Tool call:** `Bash`
```json
{
  "command": "wc -l /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "description": "Get line count of plan file"
}
```

---

### User *(2026-05-07T16:34:03.483Z)*

**Tool result**
```
     517 /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md
```

---

### Assistant *(2026-05-07T16:34:06.919Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "offset": 510,
  "limit": 8
}
```

---

### User *(2026-05-07T16:34:06.926Z)*

**Tool result**
```
510	        lines += emit_generic_triple(cho_nt, prop, val, class_prop_align, ...)
511	```
512	
513	Adding a new special case = one entry in the registry + one new function. The generic path handles all remaining properties via `class_prop_align` lookup.
514	
515	### §13.3 Pipeline
516	
517	`transform_record()` calls independent stream emitters in sequence — `emit_ddbedm_triples`, `emit_mocho_triples`, `emit_prov_triples` — each returning a list of N-Quad lines. The four output streams are fully decoupled: mt007 guard applies only to mocho and werk_staging; ddbedm and prov always run. See `§7.1`.
```

---

### Assistant *(2026-05-07T16:34:23.235Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md",
  "old_string": "### §13.3 Pipeline\n\n`transform_record()` calls independent stream emitters in sequence — `emit_ddbedm_triples`, `emit_mocho_triples`, `emit_prov_triples` — each returning a list of N-Quad lines. The four output streams are fully decoupled: mt007 guard applies only to mocho and werk_staging; ddbedm and prov always run. See `§7.1`.",
  "new_string": "### §13.3 Pipeline\n\n`transform_record()` calls independent stream emitters in sequence — `emit_ddbedm_triples`, `emit_mocho_triples`, `emit_prov_triples` — each returning a list of N-Quad lines. The four output streams are fully decoupled: mt007 guard applies only to mocho and werk_staging; ddbedm and prov always run. See `§7.1`.\n\n---\n\n## §15 Future work\n\n### §15.1 In-process parallelisation (raised 2026-05-07)\n\nThe current implementation is single-threaded. The planned approach (§2.1 of `transform-implementation-actual.md`) is to run one OS process per sector JSONL file externally. The downside is a manual merge step after all workers finish.\n\nTwo options for moving parallelisation into the script itself:\n\n**Option A — `ProcessPoolExecutor` inside `__main__.py`**\n\n`transform_record()` is already a pure function with no shared state, which makes this the natural fit.\n\n- Load all config tables once in the main process (already done).\n- Pass them to workers via the pool `initializer` — copied once per worker at fork, not per record.\n- Replace the `for line_no, raw in enumerate(...)` loop with batch submission to the pool.\n- Workers return `(streams, werk_row, dispatch_info, pred_info)` tuples; the main process handles all file I/O and counter updates.\n- DuckDB connection and stats `Counter` stay in the main process.\n- SIGINT teardown: `executor.shutdown(cancel_futures=True)`.\n\n**Estimated effort**: ~120 lines changed/added in `__main__.py` only. No changes to `transform.py`, `emitters.py`, or any other module.\n\n**Option B — `python -m transform merge` subcommand**\n\nThe transform script stays single-threaded. A separate `merge.py` (~60 lines, new file) handles post-run collection:\n- Concatenates all `.nq` shards into one file.\n- Merges DuckDB staging tables (`INSERT INTO … SELECT * FROM …`).\n- Sums stats JSON files into a combined report.\n\n**Estimated effort**: ~60 lines, new file only. Zero changes to existing code.\n\n**Trade-off**:\n\n| | Option A | Option B |\n|---|---|---|\n| Single invocation | yes | no (still two steps) |\n| Code change | moderate (`__main__.py`) | minimal (new file only) |\n| Risk to existing code | low but nonzero | zero |\n| Scales to 18.5M records | yes, native | yes, same as current |\n\nFor a pipeline run on a known corpus, Option B is faster to add and harder to break. Option A makes sense if single-command operation matters for reproducibility or handoff."
}
```

---

### User *(2026-05-07T16:34:25.169Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/notes/transform-implementation-plan.md has been updated successfully.
```

---

### Assistant *(2026-05-07T16:34:28.913Z)*

Added as `§15.1` under a new `§15 Future work` section, dated 2026-05-07. Both options documented with effort estimates and the trade-off table.

---

### User *(2026-05-07T16:35:19.938Z)*

let's go back to §7 plan. do you still know what to do? there were 5 items

---

### Assistant *(2026-05-07T16:35:47.745Z)*

Yes. Two items in `utils.py` are already done (`_BR_RE` + `_escape_literal` update). The remaining work:

1. **`resource_uris()` utility** — new function in `utils.py`; split + bare-ID expand + sanitize in one place

2. **Fix existing emitters** — swap manual `resource` extraction for `resource_uris()` calls in: `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples` (+ `bare_id_to_uri` param + sanitize `agent_uri`), `emit_contributor_triples` (+ `bare_id_to_uri` param), `emit_prov_triples` (`provider_isil`), `emit_place_stubs` (split `about`), `emit_aggregation_triples` (inline split); update `emit_mocho_triples` to pass `bare_id_to_uri` downstream and build `places_index`

3. **New `emit_current_location_triples`** — IRI-with-label-stub pattern (D16/D17); literal pass-through; add `"currentLocation"` to `_MOCHO_SKIP`

4. **Fixture files** — extract 3 corpus records to `tests/fixtures/`, write `make_fixtures.py` to produce `.nq` output for inspection

5. **Tests** — unit tests for `resource_uris()`, `_escape_literal` `<br>` variants, multi-URI and bare-ID cases for each emitter; `TestFixtures` integration class

Shall I proceed?

---

### User *(2026-05-07T16:36:45.607Z)*

lezgo

---

### Assistant *(2026-05-07T16:36:49.592Z)*

**Tool call:** `ToolSearch`
```json
{
  "query": "select:TodoWrite",
  "max_results": 1
}
```

---

### User *(2026-05-07T16:36:49.593Z)*

**Tool result**
```

```

---

### Assistant *(2026-05-07T16:36:54.688Z)*

**Tool call:** `TodoWrite`
```json
{
  "todos": [
    {
      "content": "Add resource_uris() to utils.py",
      "activeForm": "Adding resource_uris() to utils.py",
      "status": "in_progress"
    },
    {
      "content": "Fix all existing emitters + constants (_MOCHO_SKIP)",
      "activeForm": "Fixing all existing emitters + constants",
      "status": "pending"
    },
    {
      "content": "Add emit_current_location_triples + places_index in emit_mocho_triples",
      "activeForm": "Adding emit_current_location_triples",
      "status": "pending"
    },
    {
      "content": "Extract fixture records + write make_fixtures.py",
      "activeForm": "Extracting fixture records",
      "status": "pending"
    },
    {
      "content": "Write unit tests + TestFixtures integration class",
      "activeForm": "Writing tests",
      "status": "pending"
    }
  ]
}
```

---

### User *(2026-05-07T16:36:54.689Z)*

**Tool result**
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

---

### Assistant *(2026-05-07T16:37:01.735Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py",
  "old_string": "def expand_obj_nt(obj_nt: str, bare_id_to_uri: dict[str, str]) -> str:",
  "new_string": "def resource_uris(\n    resource_raw: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n    entity_class: str = \"Agent\",\n) -> list[str]:\n    \"\"\"Expand, sanitize, and split all URIs from a (possibly multi-value) resource string.\n\n    Steps: (1) split on whitespace; (2) expand bare IDs via index or mint_bare_id fallback;\n    (3) percent-encode unsafe characters. Returns [] for empty input.\n    \"\"\"\n    if not resource_raw:\n        return []\n    _bare = bare_id_to_uri or {}\n    result = []\n    for uri in resource_raw.split():\n        if not uri.startswith((\"http\", \"urn\")):\n            uri = _bare.get(uri) or mint_bare_id(entity_class, uri)\n        result.append(_sanitize_iri(uri))\n    return result\n\n\ndef expand_obj_nt(obj_nt: str, bare_id_to_uri: dict[str, str]) -> str:"
}
```

---

### User *(2026-05-07T16:50:27.720Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/utils.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:50:32.507Z)*

**Tool call:** `TodoWrite`
```json
{
  "todos": [
    {
      "content": "Add resource_uris() to utils.py",
      "activeForm": "Adding resource_uris() to utils.py",
      "status": "completed"
    },
    {
      "content": "Fix all existing emitters + constants (_MOCHO_SKIP)",
      "activeForm": "Fixing all existing emitters + constants",
      "status": "in_progress"
    },
    {
      "content": "Add emit_current_location_triples + places_index in emit_mocho_triples",
      "activeForm": "Adding emit_current_location_triples",
      "status": "pending"
    },
    {
      "content": "Extract fixture records + write make_fixtures.py",
      "activeForm": "Extracting fixture records",
      "status": "pending"
    },
    {
      "content": "Write unit tests + TestFixtures integration class",
      "activeForm": "Writing tests",
      "status": "pending"
    }
  ]
}
```

---

### User *(2026-05-07T16:50:32.508Z)*

**Tool result**
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

---

### Assistant *(2026-05-07T16:50:34.969Z)*

Now fix the emitters. Starting with the imports, then each function:

---

### Assistant *(2026-05-07T16:50:37.749Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "from .utils import (\n    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,\n    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,\n    build_bare_id_index, expand_obj_nt,\n)",
  "new_string": "from .utils import (\n    make_nq, coerce_list, mint_bare_id, _escape_literal, _sanitize_iri,\n    value_to_nt_obj, normalize_date, is_ddb_or_gnd, resolve_agent, _to_curie,\n    build_bare_id_index, expand_obj_nt, resource_uris,\n)"
}
```

---

### User *(2026-05-07T16:50:40.125Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:50:44.480Z)*

`emit_prov_triples` — sanitize `provider_isil`:

---

### Assistant *(2026-05-07T16:50:46.322Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        if provider_isil:\n            lines.append(make_nq(prov_nt, f\"<{MOCHO_ISIL}>\", f\"<{provider_isil}>\", graph_iri))",
  "new_string": "        if provider_isil:\n            lines.append(make_nq(prov_nt, f\"<{MOCHO_ISIL}>\",\n                                 f\"<{_sanitize_iri(provider_isil)}>\", graph_iri))"
}
```

---

### User *(2026-05-07T16:50:47.424Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:50:51.433Z)*

`emit_subject_triples` — replace single-URI branch with `resource_uris()` loop:

---

### Assistant *(2026-05-07T16:50:57.983Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        resource = (val.get(\"resource\") or \"\").strip()\n        label    = (val.get(\"$\")        or \"\").strip()\n        lang     = (val.get(\"lang\")     or \"\").strip()\n        if resource:\n            # Expand bare IDs: look up in the per-record index, fall back to Concept mint\n            if not resource.startswith((\"http\", \"urn\")):\n                expanded = _bare.get(resource) or mint_bare_id(\"Concept\", resource)\n            else:\n                expanded = resource\n            expanded_safe = _sanitize_iri(expanded)\n            if expanded_safe in seen:\n                continue\n            seen.add(expanded_safe)\n            lines.append(make_nq(cho_nt, f\"<{DCTERMS_SUBJECT}>\", f\"<{expanded_safe}>\", graph_iri))\n            concept = concepts_index.get(resource) or concepts_index.get(expanded)\n            if concept:\n                for pl in coerce_list(concept.get(\"prefLabel\")):\n                    for obj_nt in value_to_nt_obj(pl):\n                        lines.append(make_nq(f\"<{expanded_safe}>\", f\"<{RDFS_LABEL}>\",\n                                             obj_nt, graph_iri))\n        elif label:",
  "new_string": "        resource_raw = (val.get(\"resource\") or \"\").strip()\n        label        = (val.get(\"$\")        or \"\").strip()\n        lang         = (val.get(\"lang\")     or \"\").strip()\n        if resource_raw:\n            for uri in resource_uris(resource_raw, _bare, \"Concept\"):\n                if uri in seen:\n                    continue\n                seen.add(uri)\n                lines.append(make_nq(cho_nt, f\"<{DCTERMS_SUBJECT}>\", f\"<{uri}>\", graph_iri))\n                concept = concepts_index.get(resource_raw) or concepts_index.get(uri)\n                if concept:\n                    for pl in coerce_list(concept.get(\"prefLabel\")):\n                        for obj_nt in value_to_nt_obj(pl):\n                            lines.append(make_nq(f\"<{uri}>\", f\"<{RDFS_LABEL}>\",\n                                                 obj_nt, graph_iri))\n        elif label:"
}
```

---

### User *(2026-05-07T16:51:30.529Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:51:34.258Z)*

`emit_hastype_triples` — same pattern:

---

### Assistant *(2026-05-07T16:51:38.048Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        resource = (val.get(\"resource\") or \"\").strip()\n        if not resource:\n            continue\n        if not resource.startswith((\"http\", \"urn\")):\n            expanded = _bare.get(resource) or mint_bare_id(\"Concept\", resource)\n        else:\n            expanded = resource\n        expanded_safe = _sanitize_iri(expanded)\n        if expanded_safe in seen:\n            continue\n        seen.add(expanded_safe)\n        lines.append(make_nq(cho_nt, f\"<{EDM_HAS_TYPE}>\", f\"<{expanded_safe}>\", graph_iri))\n        concept = concepts_index.get(resource) or concepts_index.get(expanded)\n        if concept:\n            for pl in coerce_list(concept.get(\"prefLabel\")):\n                for obj_nt in value_to_nt_obj(pl):\n                    lines.append(make_nq(f\"<{expanded_safe}>\", f\"<{RDFS_LABEL}>\",\n                                         obj_nt, graph_iri))",
  "new_string": "        resource_raw = (val.get(\"resource\") or \"\").strip()\n        if not resource_raw:\n            continue\n        for uri in resource_uris(resource_raw, _bare, \"Concept\"):\n            if uri in seen:\n                continue\n            seen.add(uri)\n            lines.append(make_nq(cho_nt, f\"<{EDM_HAS_TYPE}>\", f\"<{uri}>\", graph_iri))\n            concept = concepts_index.get(resource_raw) or concepts_index.get(uri)\n            if concept:\n                for pl in coerce_list(concept.get(\"prefLabel\")):\n                    for obj_nt in value_to_nt_obj(pl):\n                        lines.append(make_nq(f\"<{uri}>\", f\"<{RDFS_LABEL}>\",\n                                             obj_nt, graph_iri))"
}
```

---

### User *(2026-05-07T16:51:40.258Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:51:44.696Z)*

`emit_creator_triples` — add `bare_id_to_uri` param, split resource for Track 1, sanitize `agent_uri` for Track 2:

---

### Assistant *(2026-05-07T16:51:59.021Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "def emit_creator_triples(\n    cho_nt: str,\n    creator_vals: list,\n    agents_index: dict[str, AgentDict],\n    target_class: str,\n    class_prop_align: PropAlign,\n    graph_iri: str,\n) -> NQList:\n    \"\"\"Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).\n\n    Both tracks run independently for each creator value (D2 / props-mapping §4).\n    \"\"\"\n    lines: NQList = []\n    dc_creator_iri = \"http://purl.org/dc/elements/1.1/creator\"\n    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), \"\")\n\n    for val in coerce_list(creator_vals):\n        if not isinstance(val, dict):\n            continue\n        resource = (val.get(\"resource\") or \"\").strip()\n        label    = (val.get(\"$\")        or \"\").strip()\n        lang     = (val.get(\"lang\")     or \"\").strip()\n\n        # Track 1: class-specific predicate (always runs when target_prop is known)\n        if track1_prop:\n            if resource:\n                lines.append(make_nq(cho_nt, f\"<{track1_prop}>\", f\"<{_sanitize_iri(resource)}>\", graph_iri))\n            elif label:\n                escaped = _escape_literal(label)\n                obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n                lines.append(make_nq(cho_nt, f\"<{track1_prop}>\", obj_nt, graph_iri))\n\n        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)\n        agent = resolve_agent(label, resource, agents_index)\n        if agent:\n            agent_uri = (agent.get(\"about\") or \"\").strip()\n            if agent_uri and is_ddb_or_gnd(agent_uri):\n                lines.append(make_nq(cho_nt, f\"<{DCTERMS_CREATOR}>\",\n                                     f\"<{agent_uri}>\", graph_iri))\n                agent_nt = f\"<{agent_uri}>\"\n                lines.append(make_nq(agent_nt, f\"<{RDF_TYPE}>\", f\"<{MOCHO_AGENT}>\", graph_iri))\n                pref = agent.get(\"prefLabel\") or label\n                if pref and isinstance(pref, str):\n                    lines.append(make_nq(agent_nt, f\"<{RDFS_LABEL}>\",\n                                         f'\"{_escape_literal(pref)}\"', graph_iri))\n    return lines",
  "new_string": "def emit_creator_triples(\n    cho_nt: str,\n    creator_vals: list,\n    agents_index: dict[str, AgentDict],\n    target_class: str,\n    class_prop_align: PropAlign,\n    graph_iri: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n) -> NQList:\n    \"\"\"Emit class-specific creator predicate (Track 1) and dcterms:creator agent stub (Track 2).\n\n    Both tracks run independently for each creator value (D2 / props-mapping §4).\n    \"\"\"\n    lines: NQList = []\n    dc_creator_iri = \"http://purl.org/dc/elements/1.1/creator\"\n    track1_prop    = class_prop_align.get((target_class, dc_creator_iri), \"\")\n\n    for val in coerce_list(creator_vals):\n        if not isinstance(val, dict):\n            continue\n        resource_raw = (val.get(\"resource\") or \"\").strip()\n        label        = (val.get(\"$\")        or \"\").strip()\n        lang         = (val.get(\"lang\")     or \"\").strip()\n        primary_resource = resource_raw.split()[0] if resource_raw else \"\"\n\n        # Track 1: class-specific predicate (always runs when target_prop is known)\n        if track1_prop:\n            if resource_raw:\n                for uri in resource_uris(resource_raw, bare_id_to_uri, \"Agent\"):\n                    lines.append(make_nq(cho_nt, f\"<{track1_prop}>\", f\"<{uri}>\", graph_iri))\n            elif label:\n                escaped = _escape_literal(label)\n                obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n                lines.append(make_nq(cho_nt, f\"<{track1_prop}>\", obj_nt, graph_iri))\n\n        # Track 2: generic dcterms:creator + agent stub (D2 — both tracks always run)\n        agent = resolve_agent(label, primary_resource, agents_index)\n        if agent:\n            agent_uri = _sanitize_iri((agent.get(\"about\") or \"\").strip())\n            if agent_uri and is_ddb_or_gnd(agent_uri):\n                lines.append(make_nq(cho_nt, f\"<{DCTERMS_CREATOR}>\",\n                                     f\"<{agent_uri}>\", graph_iri))\n                agent_nt = f\"<{agent_uri}>\"\n                lines.append(make_nq(agent_nt, f\"<{RDF_TYPE}>\", f\"<{MOCHO_AGENT}>\", graph_iri))\n                pref = agent.get(\"prefLabel\") or label\n                if pref and isinstance(pref, str):\n                    lines.append(make_nq(agent_nt, f\"<{RDFS_LABEL}>\",\n                                         f'\"{_escape_literal(pref)}\"', graph_iri))\n    return lines"
}
```

---

### User *(2026-05-07T16:52:00.778Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:52:04.780Z)*

`emit_contributor_triples` — add `bare_id_to_uri` param, use first URI for LIDO lookup, `resource_uris()` loop:

---

### Assistant *(2026-05-07T16:52:15.388Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "def emit_contributor_triples(\n    cho_nt: str,\n    contributor_vals: list,\n    event_participant_index: dict[str, str],\n    lido_dispatch: dict[str, dict],\n    target_class: str,\n    wemi: str,\n    graph_iri: str,\n) -> NQList:\n    \"\"\"Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5).\"\"\"\n    lines: NQList = []\n    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), \"dc_agent_fallback\")\n\n    for val in coerce_list(contributor_vals):\n        if not isinstance(val, dict):\n            continue\n        resource = (val.get(\"resource\") or \"\").strip()\n        label    = (val.get(\"$\")        or \"\").strip()\n        lang     = (val.get(\"lang\")     or \"\").strip()\n\n        lido_type   = event_participant_index.get(resource) if resource else None\n        lido_row    = lido_dispatch.get(lido_type) if lido_type else None\n        target_prop = (\n            (lido_row.get(prop_col) or lido_row.get(\"dc_agent_fallback\") or DC_CONTRIBUTOR)\n            if lido_row else DC_CONTRIBUTOR\n        )\n\n        if resource:\n            lines.append(make_nq(cho_nt, f\"<{target_prop}>\", f\"<{_sanitize_iri(resource)}>\", graph_iri))\n            agent_nt = f\"<{_sanitize_iri(resource)}>\"\n            lines.append(make_nq(agent_nt, f\"<{RDF_TYPE}>\", f\"<{MOCHO_AGENT}>\", graph_iri))\n            if label:\n                escaped = _escape_literal(label)\n                obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n                lines.append(make_nq(agent_nt, f\"<{RDFS_LABEL}>\", obj_nt, graph_iri))\n        elif label:\n            escaped = _escape_literal(label)\n            obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n            lines.append(make_nq(cho_nt, f\"<{DC_CONTRIBUTOR}>\", obj_nt, graph_iri))\n    return lines",
  "new_string": "def emit_contributor_triples(\n    cho_nt: str,\n    contributor_vals: list,\n    event_participant_index: dict[str, str],\n    lido_dispatch: dict[str, dict],\n    target_class: str,\n    wemi: str,\n    graph_iri: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n) -> NQList:\n    \"\"\"Emit contributor triples using LIDO event-type dispatch (D3/D25, props-mapping §5).\"\"\"\n    lines: NQList = []\n    prop_col = _CONTRIBUTOR_COL.get((wemi, target_class), \"dc_agent_fallback\")\n\n    for val in coerce_list(contributor_vals):\n        if not isinstance(val, dict):\n            continue\n        resource_raw     = (val.get(\"resource\") or \"\").strip()\n        label            = (val.get(\"$\")        or \"\").strip()\n        lang             = (val.get(\"lang\")     or \"\").strip()\n        primary_resource = resource_raw.split()[0] if resource_raw else \"\"\n\n        lido_type   = event_participant_index.get(primary_resource) if primary_resource else None\n        lido_row    = lido_dispatch.get(lido_type) if lido_type else None\n        target_prop = (\n            (lido_row.get(prop_col) or lido_row.get(\"dc_agent_fallback\") or DC_CONTRIBUTOR)\n            if lido_row else DC_CONTRIBUTOR\n        )\n\n        if resource_raw:\n            for uri in resource_uris(resource_raw, bare_id_to_uri, \"Agent\"):\n                lines.append(make_nq(cho_nt, f\"<{target_prop}>\", f\"<{uri}>\", graph_iri))\n                agent_nt = f\"<{uri}>\"\n                lines.append(make_nq(agent_nt, f\"<{RDF_TYPE}>\", f\"<{MOCHO_AGENT}>\", graph_iri))\n                if label:\n                    escaped = _escape_literal(label)\n                    obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n                    lines.append(make_nq(agent_nt, f\"<{RDFS_LABEL}>\", obj_nt, graph_iri))\n        elif label:\n            escaped = _escape_literal(label)\n            obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n            lines.append(make_nq(cho_nt, f\"<{DC_CONTRIBUTOR}>\", obj_nt, graph_iri))\n    return lines"
}
```

---

### User *(2026-05-07T16:55:43.351Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:55:49.594Z)*

`emit_aggregation_triples` — inline split+sanitize for all three URI extractions:

---

### Assistant *(2026-05-07T16:55:55.907Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    is_shown = agg.get(\"isShownAt\") or {}\n    if isinstance(is_shown, dict):\n        uri = (is_shown.get(\"resource\") or \"\").strip()\n        if uri:\n            lines.append(make_nq(cho_nt, f\"<{DCTERMS_SOURCE}>\", f\"<{_sanitize_iri(uri)}>\", graph_iri))\n\n    for dp in coerce_list(agg.get(\"dataProvider\")):\n        if not isinstance(dp, dict):\n            continue\n        uri = (dp.get(\"resource\") or \"\").strip()\n        if uri and uri.startswith(_org_prefix):\n            lines.append(make_nq(cho_nt, f\"<{_edm_dp}>\", f\"<{_sanitize_iri(uri)}>\", graph_iri))\n\n    for obj in coerce_list(agg.get(\"object\")):\n        if not isinstance(obj, dict):\n            continue\n        uri = (obj.get(\"resource\") or \"\").strip()\n        if uri:\n            lines.append(make_nq(cho_nt, f\"<{FOAF_THUMBNAIL}>\", f\"<{_sanitize_iri(uri)}>\", graph_iri))",
  "new_string": "    is_shown = agg.get(\"isShownAt\") or {}\n    if isinstance(is_shown, dict):\n        for uri in (is_shown.get(\"resource\") or \"\").strip().split():\n            lines.append(make_nq(cho_nt, f\"<{DCTERMS_SOURCE}>\",\n                                 f\"<{_sanitize_iri(uri)}>\", graph_iri))\n\n    for dp in coerce_list(agg.get(\"dataProvider\")):\n        if not isinstance(dp, dict):\n            continue\n        for uri in (dp.get(\"resource\") or \"\").strip().split():\n            if uri.startswith(_org_prefix):\n                lines.append(make_nq(cho_nt, f\"<{_edm_dp}>\",\n                                     f\"<{_sanitize_iri(uri)}>\", graph_iri))\n\n    for obj in coerce_list(agg.get(\"object\")):\n        if not isinstance(obj, dict):\n            continue\n        for uri in (obj.get(\"resource\") or \"\").strip().split():\n            lines.append(make_nq(cho_nt, f\"<{FOAF_THUMBNAIL}>\",\n                                 f\"<{_sanitize_iri(uri)}>\", graph_iri))"
}
```

---

### User *(2026-05-07T16:56:00.663Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T16:56:04.416Z)*

`emit_place_stubs` — split `raw_about`, use first part:

---

### Assistant *(2026-05-07T16:56:05.841Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "        raw_about = (place.get(\"about\") or \"\").strip()\n        if not raw_about:\n            continue\n        place_uri = mint_bare_id(\"Place\", raw_about)",
  "new_string": "        raw_about = (place.get(\"about\") or \"\").strip()\n        if not raw_about:\n            continue\n        place_uri = mint_bare_id(\"Place\", _sanitize_iri(raw_about.split()[0]))"
}
```

---

### User *(2026-05-07T17:01:49.859Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:01:57.678Z)*

Now update `emit_mocho_triples` to pass `bare_id_to_uri` to creator/contributor:

---

### Assistant *(2026-05-07T17:02:01.969Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    _creator_lines = emit_creator_triples(\n        cho_nt, cho.get(\"creator\"), agents_index, target_class, class_prop_align, graph_iri,\n    )\n    lines.extend(_creator_lines)\n    _track_nqlist(_creator_lines)\n\n    _contrib_lines = emit_contributor_triples(\n        cho_nt, cho.get(\"contributor\"),\n        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,\n    )",
  "new_string": "    _creator_lines = emit_creator_triples(\n        cho_nt, cho.get(\"creator\"), agents_index, target_class, class_prop_align, graph_iri,\n        bare_id_to_uri,\n    )\n    lines.extend(_creator_lines)\n    _track_nqlist(_creator_lines)\n\n    _contrib_lines = emit_contributor_triples(\n        cho_nt, cho.get(\"contributor\"),\n        event_participant_index, lido_dispatch, target_class, wemi, graph_iri,\n        bare_id_to_uri,\n    )"
}
```

---

### User *(2026-05-07T17:02:05.741Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:02:09.703Z)*

Now add `"currentLocation"` to `_MOCHO_SKIP` in constants:

---

### Assistant *(2026-05-07T17:02:14.549Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "_MOCHO_SKIP = frozenset({\n    \"about\", \"hierarchyType\",\n    \"creator\", \"contributor\",\n    \"dcSubject\", \"dcTermsSubject\", \"dcTermSubject\",\n    \"dcType\",\n    \"aggregationEntity\", \"hierarchyPosition\",\n    \"hasMet\",     # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph\n    \"hasType\",    # handled by emit_hastype_triples(); needs bare-ID expansion + label stub\n})",
  "new_string": "_MOCHO_SKIP = frozenset({\n    \"about\", \"hierarchyType\",\n    \"creator\", \"contributor\",\n    \"dcSubject\", \"dcTermsSubject\", \"dcTermSubject\",\n    \"dcType\",\n    \"aggregationEntity\", \"hierarchyPosition\",\n    \"hasMet\",          # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph\n    \"hasType\",         # handled by emit_hastype_triples(); needs bare-ID expansion + label stub\n    \"currentLocation\", # handled by emit_current_location_triples(); IRI-with-label-stub (D16/D17)\n})"
}
```

---

### User *(2026-05-07T17:02:14.550Z)*

**Tool result** *(error)*
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

---

### Assistant *(2026-05-07T17:02:16.884Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "offset": 100,
  "limit": 18
}
```

---

### User *(2026-05-07T17:02:16.891Z)*

**Tool result**
```
100	
101	SUBJECT_KEYS = frozenset({"dcSubject", "dcTermsSubject", "dcTermSubject"})
102	
103	_MOCHO_SKIP = frozenset({
104	    "about", "hierarchyType",
105	    "creator", "contributor",
106	    "dcSubject", "dcTermsSubject", "dcTermSubject",
107	    "dcType",
108	    "aggregationEntity", "hierarchyPosition",
109	    "hasMet",     # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph
110	    "hasType",    # handled by emit_hastype_triples(); needs bare-ID expansion + label stub
111	})
112	
113	# ─── Prefix expansion table ───────────────────────────────────────────────────
114	
115	_PREFIXES = {
116	    "rdam":    "http://rdaregistry.info/Elements/m/",
117	    "rdaw":    "http://rdaregistry.info/Elements/w/",
```

---

### Assistant *(2026-05-07T17:02:21.770Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py",
  "old_string": "_MOCHO_SKIP = frozenset({\n    \"about\", \"hierarchyType\",\n    \"creator\", \"contributor\",\n    \"dcSubject\", \"dcTermsSubject\", \"dcTermSubject\",\n    \"dcType\",\n    \"aggregationEntity\", \"hierarchyPosition\",\n    \"hasMet\",     # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph\n    \"hasType\",    # handled by emit_hastype_triples(); needs bare-ID expansion + label stub\n})",
  "new_string": "_MOCHO_SKIP = frozenset({\n    \"about\", \"hierarchyType\",\n    \"creator\", \"contributor\",\n    \"dcSubject\", \"dcTermsSubject\", \"dcTermSubject\",\n    \"dcType\",\n    \"aggregationEntity\", \"hierarchyPosition\",\n    \"hasMet\",          # edm:hasMet is an EDM Event property; no mocho alignment, skip in mocho graph\n    \"hasType\",         # handled by emit_hastype_triples(); IRI-with-label-stub (D16/D17)\n    \"currentLocation\", # handled by emit_current_location_triples(); IRI-with-label-stub (D16/D17)\n})"
}
```

---

### User *(2026-05-07T17:02:41.415Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/constants.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:02:45.840Z)*

**Tool call:** `TodoWrite`
```json
{
  "todos": [
    {
      "content": "Add resource_uris() to utils.py",
      "activeForm": "Adding resource_uris() to utils.py",
      "status": "completed"
    },
    {
      "content": "Fix all existing emitters + constants (_MOCHO_SKIP)",
      "activeForm": "Fixing all existing emitters + constants",
      "status": "completed"
    },
    {
      "content": "Add emit_current_location_triples + places_index in emit_mocho_triples",
      "activeForm": "Adding emit_current_location_triples",
      "status": "in_progress"
    },
    {
      "content": "Extract fixture records + write make_fixtures.py",
      "activeForm": "Extracting fixture records",
      "status": "pending"
    },
    {
      "content": "Write unit tests + TestFixtures integration class",
      "activeForm": "Writing tests",
      "status": "pending"
    }
  ]
}
```

---

### User *(2026-05-07T17:02:45.841Z)*

**Tool result**
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

---

### Assistant *(2026-05-07T17:02:49.673Z)*

Now add `emit_current_location_triples` to `emitters.py`, and update `emit_mocho_triples` to build `places_index` and call it. First the new function, placed after `emit_hastype_triples`:

---

### Assistant *(2026-05-07T17:02:59.965Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "def emit_creator_triples(",
  "new_string": "def emit_current_location_triples(\n    cho_nt: str,\n    currentloc_vals: object,\n    places_index: dict[str, dict],\n    graph_iri: str,\n    bare_id_to_uri: dict[str, str] | None = None,\n) -> NQList:\n    \"\"\"Emit edm:currentLocation triples with optional rdfs:label stub from matching edm:Place.\n\n    URI values: emit <cho> edm:currentLocation <uri> + <uri> rdfs:label <prefLabel> if found.\n    Literal values: emit <cho> edm:currentLocation \"literal\" (pass-through, no stub).\n    Multi-URI resource fields are split; bare IDs are expanded. Deduplicates URIs per record.\n    No rdf:type emitted for Place stubs in mocho graph (D17).\n    \"\"\"\n    edm_current_location = EDM_NS + \"currentLocation\"\n    lines: NQList = []\n    seen: set[str] = set()\n    _bare = bare_id_to_uri or {}\n\n    for val in coerce_list(currentloc_vals):\n        if not isinstance(val, dict):\n            continue\n        resource_raw = (val.get(\"resource\") or \"\").strip()\n        label        = (val.get(\"$\")        or \"\").strip()\n        lang         = (val.get(\"lang\")     or \"\").strip()\n\n        if resource_raw:\n            for uri in resource_uris(resource_raw, _bare, \"Place\"):\n                if uri in seen:\n                    continue\n                seen.add(uri)\n                lines.append(make_nq(cho_nt, f\"<{edm_current_location}>\",\n                                     f\"<{uri}>\", graph_iri))\n                place = places_index.get(resource_raw) or places_index.get(uri)\n                if place:\n                    for pl in coerce_list(place.get(\"prefLabel\")):\n                        for obj_nt in value_to_nt_obj(pl):\n                            lines.append(make_nq(f\"<{uri}>\", f\"<{RDFS_LABEL}>\",\n                                                 obj_nt, graph_iri))\n        elif label:\n            escaped = _escape_literal(label)\n            obj_nt  = f'\"{escaped}\"@{lang}' if lang else f'\"{escaped}\"'\n            lines.append(make_nq(cho_nt, f\"<{edm_current_location}>\", obj_nt, graph_iri))\n    return lines\n\n\ndef emit_creator_triples("
}
```

---

### User *(2026-05-07T17:03:01.366Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:03:04.963Z)*

Now update `emit_mocho_triples` to build `places_index` and call `emit_current_location_triples`:

---

### Assistant *(2026-05-07T17:03:07.593Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    concepts_index: dict[str, dict] = {}\n    for concept in coerce_list(rdf.get(\"Concept\")):\n        if not isinstance(concept, dict):\n            continue\n        about = (concept.get(\"about\") or \"\").strip()\n        if about:\n            concepts_index[about] = concept",
  "new_string": "    concepts_index: dict[str, dict] = {}\n    for concept in coerce_list(rdf.get(\"Concept\")):\n        if not isinstance(concept, dict):\n            continue\n        about = (concept.get(\"about\") or \"\").strip()\n        if about:\n            concepts_index[about] = concept\n\n    places_index: dict[str, dict] = {}\n    for place in coerce_list(rdf.get(\"Place\")):\n        if not isinstance(place, dict):\n            continue\n        about = (place.get(\"about\") or \"\").strip()\n        if about:\n            places_index[about.split()[0]] = place"
}
```

---

### User *(2026-05-07T17:03:08.747Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:03:12.615Z)*

Now wire in the call to `emit_current_location_triples` alongside the other special handlers:

---

### Assistant *(2026-05-07T17:03:15.366Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py",
  "old_string": "    if hastype_vals:\n        _hastype_lines = emit_hastype_triples(cho_nt, hastype_vals, concepts_index, graph_iri,\n                                              bare_id_to_uri)\n        lines.extend(_hastype_lines)\n        _track_nqlist(_hastype_lines)",
  "new_string": "    if hastype_vals:\n        _hastype_lines = emit_hastype_triples(cho_nt, hastype_vals, concepts_index, graph_iri,\n                                              bare_id_to_uri)\n        lines.extend(_hastype_lines)\n        _track_nqlist(_hastype_lines)\n\n    currentloc_vals = coerce_list(cho.get(\"currentLocation\"))\n    if currentloc_vals:\n        _curloc_lines = emit_current_location_triples(\n            cho_nt, currentloc_vals, places_index, graph_iri, bare_id_to_uri,\n        )\n        lines.extend(_curloc_lines)\n        _track_nqlist(_curloc_lines)"
}
```

---

### User *(2026-05-07T17:03:16.588Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/emitters.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:03:19.881Z)*

Run the existing tests to confirm nothing is broken:

---

### Assistant *(2026-05-07T17:03:20.744Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && .venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -20",
  "description": "Run existing test suite"
}
```

---

### User *(2026-05-07T17:03:22.753Z)*

**Tool result**
```
.....................................................................    [100%]
69 passed in 0.06s
```

---

### Assistant *(2026-05-07T17:03:27.460Z)*

All 69 pass.

---

### Assistant *(2026-05-07T17:03:29.598Z)*

**Tool call:** `TodoWrite`
```json
{
  "todos": [
    {
      "content": "Add resource_uris() to utils.py",
      "activeForm": "Adding resource_uris() to utils.py",
      "status": "completed"
    },
    {
      "content": "Fix all existing emitters + constants (_MOCHO_SKIP)",
      "activeForm": "Fixing all existing emitters + constants",
      "status": "completed"
    },
    {
      "content": "Add emit_current_location_triples + places_index in emit_mocho_triples",
      "activeForm": "Adding emit_current_location_triples",
      "status": "completed"
    },
    {
      "content": "Extract fixture records + write make_fixtures.py",
      "activeForm": "Extracting fixture records",
      "status": "in_progress"
    },
    {
      "content": "Write unit tests + TestFixtures integration class",
      "activeForm": "Writing tests",
      "status": "pending"
    }
  ]
}
```

---

### User *(2026-05-07T17:03:29.598Z)*

**Tool result**
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

---

### Assistant *(2026-05-07T17:03:32.172Z)*

Now extract the three fixture records and write `make_fixtures.py`:

---

### Assistant *(2026-05-07T17:03:39.296Z)*

**Tool call:** `Bash`
```json
{
  "command": "mkdir -p /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/fixtures && python3 -c \"\nimport json\n\ntargets = {\n    '23MBRVVDUHBFZNDCTK4SQM7KROKGVGNF': 'multi_uri',\n    '223GMAWUHPGI76OQUKSL54XVOCHHXDWD': 'br_tag',\n    '222NZKK63TNRLC2VETRV722VKBDSUVGL': 'bare_id',\n}\nfound = {}\nwith open('data/items-all-goethe-faust.json') as f:\n    for line in f:\n        line = line.strip()\n        if not line: continue\n        try: rec = json.loads(line)\n        except: continue\n        try: obj_id = rec['edm']['RDF']['ProvidedCHO']['about'].rsplit('/',1)[-1]\n        except: continue\n        if obj_id in targets:\n            found[targets[obj_id]] = rec\n        if len(found) == len(targets):\n            break\n\nfor name, rec in found.items():\n    path = f'scripts/transform/tests/fixtures/{name}.json'\n    with open(path, 'w') as f:\n        json.dump(rec, f, indent=2, ensure_ascii=False)\n    print(f'wrote {path}')\nprint('done:', list(found.keys()))\n\"",
  "description": "Extract fixture records from corpus"
}
```

---

### User *(2026-05-07T17:03:41.213Z)*

**Tool result**
```
wrote scripts/transform/tests/fixtures/bare_id.json
wrote scripts/transform/tests/fixtures/br_tag.json
wrote scripts/transform/tests/fixtures/multi_uri.json
done: ['bare_id', 'br_tag', 'multi_uri']
```

---

### Assistant *(2026-05-07T17:03:44.116Z)*

Now write `make_fixtures.py`:

---

### Assistant *(2026-05-07T17:03:54.441Z)*

**Tool call:** `Write`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/make_fixtures.py",
  "content": "\"\"\"\nPurpose:    Run the full transform on the three fixture records and write .nq output files\n            for human inspection. One <id>.nq file per fixture in tests/fixtures/.\nUsage:      python -m transform.tests.make_fixtures\n            (run from scripts/ directory)\nInputs:     scripts/transform/tests/fixtures/{multi_uri,br_tag,bare_id}.json\n            output/config/  (all standard config files)\nOutputs:    scripts/transform/tests/fixtures/{multi_uri,br_tag,bare_id}.nq\nDeps:       transform package (stdlib only)\nAssumes:    Run from goethe-faust/scripts/\n\"\"\"\n\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # adds scripts/ to sys.path\n\nfrom transform.constants import PROJECT_DIR\nfrom transform.loaders import (\n    load_class_prop_alignment, load_lido_event_types,\n    load_htype_map, load_mediatype_class, load_audio_type2class,\n)\nfrom transform.transform import transform_record\n\n_FIXTURES = Path(__file__).parent / \"fixtures\"\n_CONFIG   = PROJECT_DIR / \"output\" / \"config\"\n\n_FIXTURE_NAMES = [\"multi_uri\", \"br_tag\", \"bare_id\"]\n\n\ndef main() -> None:\n    class_prop_align    = load_class_prop_alignment(_CONFIG / \"lookup_class_prop_alignment.csv\")\n    lido_dispatch       = load_lido_event_types(_CONFIG / \"lido_event_types.csv\")\n    htype_map           = load_htype_map(_CONFIG / \"lookup_htype_doco_rico.csv\")\n    mediatype_class_map = load_mediatype_class(_CONFIG / \"lookup_mediatype_class.csv\")\n    audio_type2class    = load_audio_type2class(_CONFIG / \"audio_type2class.json\")\n\n    for name in _FIXTURE_NAMES:\n        in_path  = _FIXTURES / f\"{name}.json\"\n        out_path = _FIXTURES / f\"{name}.nq\"\n\n        with open(in_path, encoding=\"utf-8\") as f:\n            record = json.load(f)\n\n        streams, _werk, _dispatch, _pred = transform_record(\n            record, None,\n            mediatype_class_map, htype_map, audio_type2class,\n            class_prop_align, lido_dispatch,\n        )\n\n        with open(out_path, \"w\", encoding=\"utf-8\") as f:\n            if streams:\n                for graph_lines in streams.values():\n                    for nq in graph_lines:\n                        f.write(nq + \"\\n\")\n\n        total = sum(len(v) for v in streams.values()) if streams else 0\n        print(f\"{name}: {total} triples → {out_path.name}\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
```

---

### User *(2026-05-07T17:03:56.055Z)*

**Tool result**
```
File created successfully at: /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/make_fixtures.py
```

---

### Assistant *(2026-05-07T17:04:00.542Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust/scripts && python -m transform.tests.make_fixtures 2>&1",
  "description": "Generate fixture .nq output files"
}
```

---

### User *(2026-05-07T17:04:01.858Z)*

**Tool result**
```
multi_uri: 117 triples → multi_uri.nq
br_tag: 69 triples → br_tag.nq
bare_id: 192 triples → bare_id.nq
```

---

### Assistant *(2026-05-07T17:04:05.830Z)*

**Tool call:** `TodoWrite`
```json
{
  "todos": [
    {
      "content": "Add resource_uris() to utils.py",
      "activeForm": "Adding resource_uris() to utils.py",
      "status": "completed"
    },
    {
      "content": "Fix all existing emitters + constants (_MOCHO_SKIP)",
      "activeForm": "Fixing all existing emitters + constants",
      "status": "completed"
    },
    {
      "content": "Add emit_current_location_triples + places_index in emit_mocho_triples",
      "activeForm": "Adding emit_current_location_triples",
      "status": "completed"
    },
    {
      "content": "Extract fixture records + write make_fixtures.py",
      "activeForm": "Extracting fixture records",
      "status": "completed"
    },
    {
      "content": "Write unit tests + TestFixtures integration class",
      "activeForm": "Writing tests",
      "status": "in_progress"
    }
  ]
}
```

---

### User *(2026-05-07T17:04:05.831Z)*

**Tool result**
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

---

### Assistant *(2026-05-07T17:04:09.186Z)*

Now write all the tests. Let me read the end of the test file first:

---

### Assistant *(2026-05-07T17:04:09.420Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 1,
  "limit": 45
}
```

---

### User *(2026-05-07T17:04:09.502Z)*

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
30	)
31	from transform.emitters import (
32	    retype_entities,
33	    emit_creator_triples,
34	    emit_contributor_triples,
35	    emit_subject_triples,
36	    emit_hastype_triples,
37	    emit_aggregation_triples,
38	    emit_place_stubs,
39	    werk_staging_row,
40	    emit_ddbedm_triples,
41	)
42	from transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE
43	from transform.loaders import load_mediatype_class, load_htype_map
44	
45	# Config table paths
```

---

### Assistant *(2026-05-07T17:04:15.168Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "from transform.utils import (\n    coerce_list,\n    make_nq,\n    mint_bare_id,\n    mint_cho_uri,\n    normalize_date,\n    value_to_nt_obj,\n    _escape_literal,\n    get_object_id,\n    build_bare_id_index,\n    expand_obj_nt,\n)\nfrom transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_hastype_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n)\nfrom transform.constants import _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE",
  "new_string": "from transform.utils import (\n    coerce_list,\n    make_nq,\n    mint_bare_id,\n    mint_cho_uri,\n    normalize_date,\n    value_to_nt_obj,\n    _escape_literal,\n    get_object_id,\n    build_bare_id_index,\n    expand_obj_nt,\n    resource_uris,\n)\nfrom transform.emitters import (\n    retype_entities,\n    emit_creator_triples,\n    emit_contributor_triples,\n    emit_subject_triples,\n    emit_hastype_triples,\n    emit_current_location_triples,\n    emit_aggregation_triples,\n    emit_place_stubs,\n    werk_staging_row,\n    emit_ddbedm_triples,\n)\nfrom transform.constants import (\n    _MOCHO_SKIP, DDB_HIERARCHY_TYPE, _HTYPE_PREFIX, EDM_HAS_TYPE, EDM_NS,\n)\nfrom transform.transform import transform_record"
}
```

---

### User *(2026-05-07T17:04:16.885Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:04:20.095Z)*

Now append all new tests:

---

### Assistant *(2026-05-07T17:04:20.669Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "offset": 605,
  "limit": 15
}
```

---

### User *(2026-05-07T17:04:20.673Z)*

**Tool result**
```
605	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
606	        assert lines == []
607	
608	    def test_dedup(self):
609	        uri = "http://ddb.vocnet.org/medientyp/mt003"
610	        vals = [{"resource": uri}, {"resource": uri}]
611	        lines = emit_hastype_triples(self._cho_nt, vals, {}, GRAPH_MOCHO)
612	        assert len([l for l in lines if EDM_HAS_TYPE in l]) == 1
613	
614	
615	def test_hastype_in_mocho_skip():
616	    assert "hasType" in _MOCHO_SKIP
617	
```

---

### Assistant *(2026-05-07T17:05:18.970Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "def test_hastype_in_mocho_skip():\n    assert \"hasType\" in _MOCHO_SKIP",
  "new_string": "def test_hastype_in_mocho_skip():\n    assert \"hasType\" in _MOCHO_SKIP\n\n\ndef test_currentlocation_in_mocho_skip():\n    assert \"currentLocation\" in _MOCHO_SKIP\n\n\n# ── _escape_literal — <br> normalization ─────────────────────────────────────\n\nclass TestEscapeLiteralBr:\n    def test_br_lowercase(self):\n        assert _escape_literal(\"a<br>b\") == r\"a\\nb\"\n\n    def test_br_uppercase(self):\n        assert _escape_literal(\"A<BR>B\") == r\"A\\nB\"\n\n    def test_br_self_closing(self):\n        assert _escape_literal(\"a<br/>b\") == r\"a\\nb\"\n\n    def test_br_xhtml(self):\n        assert _escape_literal(\"a<br />b\") == r\"a\\nb\"\n\n    def test_br_mixed_with_other_escapes(self):\n        result = _escape_literal('say \"hi\"<br/>next')\n        assert r'\\n' in result\n        assert r'\\\"' in result\n        assert \"<br\" not in result\n\n\n# ── resource_uris ─────────────────────────────────────────────────────────────\n\nclass TestResourceUris:\n    def test_empty_returns_empty(self):\n        assert resource_uris(\"\") == []\n\n    def test_single_full_uri(self):\n        uri = \"http://d-nb.info/gnd/118540238\"\n        assert resource_uris(uri) == [uri]\n\n    def test_two_space_separated(self):\n        raw = \"http://d-nb.info/gnd/123 https://www.geonames.org/456\"\n        result = resource_uris(raw)\n        assert len(result) == 2\n        assert \"http://d-nb.info/gnd/123\" in result\n        assert \"https://www.geonames.org/456\" in result\n\n    def test_bare_id_index_lookup(self):\n        bare = \"A\" * 32\n        index = {bare: f\"urn:ddbedm:Concept:{bare}\"}\n        result = resource_uris(bare, index, \"Concept\")\n        assert result == [f\"urn:ddbedm:Concept:{bare}\"]\n\n    def test_bare_id_fallback_mint(self):\n        bare = \"B\" * 32\n        result = resource_uris(bare, {}, \"Concept\")\n        assert result == [f\"urn:ddbedm:Concept:{bare}\"]\n\n    def test_entity_class_forwarded(self):\n        bare = \"C\" * 32\n        result = resource_uris(bare, {}, \"Place\")\n        assert result == [f\"urn:ddbedm:Place:{bare}\"]\n\n    def test_unsafe_chars_sanitized(self):\n        uri = \"http://example.org/item with space\"\n        result = resource_uris(uri)\n        assert \" \" not in result[0]\n        assert \"%20\" in result[0]\n\n\n# ── emit_subject_triples — multi-URI ─────────────────────────────────────────\n\nclass TestEmitSubjectTriplesMultiUri:\n    _cho = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"S\" * 32 + \">\"\n    _g   = GRAPH_MOCHO\n\n    def test_two_uris_produce_two_triples(self):\n        uri1 = \"http://d-nb.info/gnd/111\"\n        uri2 = \"http://d-nb.info/gnd/222\"\n        vals = [{\"resource\": f\"{uri1} {uri2}\", \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_subject_triples(self._cho, vals, {}, self._g)\n        subject_lines = [l for l in lines if \"dcterms/terms/subject\" in l or \"subject\" in l]\n        assert len([l for l in lines if uri1 in l and \"subject\" in l]) == 1\n        assert len([l for l in lines if uri2 in l and \"subject\" in l]) == 1\n\n    def test_no_space_in_any_iri(self):\n        raw = \"http://d-nb.info/gnd/111 http://d-nb.info/gnd/222\"\n        vals = [{\"resource\": raw}]\n        lines = emit_subject_triples(self._cho, vals, {}, self._g)\n        for line in lines:\n            parts = line.split()\n            for part in parts:\n                if part.startswith(\"<\") and part.endswith(\">\"):\n                    assert \" \" not in part[1:-1]\n\n\n# ── emit_hastype_triples — multi-URI ─────────────────────────────────────────\n\nclass TestEmitHastypeTriplesMultiUri:\n    _cho = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"T\" * 32 + \">\"\n\n    def test_two_uris_produce_two_hastype_triples(self):\n        uri1 = \"http://ddb.vocnet.org/medientyp/mt001\"\n        uri2 = \"http://ddb.vocnet.org/medientyp/mt003\"\n        vals = [{\"resource\": f\"{uri1} {uri2}\"}]\n        lines = emit_hastype_triples(self._cho, vals, {}, GRAPH_MOCHO)\n        hastype_lines = [l for l in lines if EDM_HAS_TYPE in l]\n        assert len(hastype_lines) == 2\n\n\n# ── emit_creator_triples — multi-URI + bare ID + agent_uri sanitize ───────────\n\n_CREATOR_CHO = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"X\" * 32 + \">\"\n_CREATOR_G   = GRAPH_MOCHO\n\n\nclass TestEmitCreatorTriplesMultiUri:\n    def test_two_uris_produce_two_track1_triples(self):\n        uri1 = \"http://d-nb.info/gnd/111\"\n        uri2 = \"http://d-nb.info/gnd/222\"\n        align = {(\"http://www.w3.org/2002/07/owl#Thing\",\n                  \"http://purl.org/dc/elements/1.1/creator\"): \"http://example.org/prop\"}\n        vals = [{\"resource\": f\"{uri1} {uri2}\", \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_creator_triples(_CREATOR_CHO, vals, {}, \"http://www.w3.org/2002/07/owl#Thing\",\n                                     align, _CREATOR_G)\n        prop_lines = [l for l in lines if \"example.org/prop\" in l]\n        assert len(prop_lines) == 2\n\n\nclass TestEmitCreatorTriplesBareId:\n    _bare = \"D\" * 32\n\n    def test_bare_id_expanded_via_param(self):\n        index = {self._bare: f\"urn:ddbedm:Agent:{self._bare}\"}\n        align = {(\"http://www.w3.org/2002/07/owl#Thing\",\n                  \"http://purl.org/dc/elements/1.1/creator\"): \"http://example.org/prop\"}\n        vals = [{\"resource\": self._bare}]\n        lines = emit_creator_triples(_CREATOR_CHO, vals, {}, \"http://www.w3.org/2002/07/owl#Thing\",\n                                     align, _CREATOR_G, index)\n        assert any(f\"urn:ddbedm:Agent:{self._bare}\" in l for l in lines)\n\n    def test_agent_uri_sanitized(self):\n        unsafe_uri = \"http://d-nb.info/gnd/118 540238\"  # space in URI\n        agent = {\"about\": unsafe_uri, \"prefLabel\": \"Goethe\"}\n        agents_index = {unsafe_uri: agent}\n        vals = [{\"resource\": \"\", \"$\": \"Goethe\", \"lang\": \"de\"}]\n        lines = emit_creator_triples(_CREATOR_CHO, vals, agents_index,\n                                     \"http://www.w3.org/2002/07/owl#Thing\", {}, _CREATOR_G)\n        for line in lines:\n            for part in line.split():\n                if part.startswith(\"<\") and part.endswith(\">\"):\n                    assert \" \" not in part[1:-1]\n\n\n# ── emit_contributor_triples — multi-URI + bare ID ────────────────────────────\n\n_CONTRIB_CHO = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"Y\" * 32 + \">\"\n\n\nclass TestEmitContributorTriplesMultiUri:\n    def test_two_uris_produce_two_cho_triples(self):\n        uri1 = \"http://d-nb.info/gnd/333\"\n        uri2 = \"http://d-nb.info/gnd/444\"\n        vals = [{\"resource\": f\"{uri1} {uri2}\", \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_contributor_triples(_CONTRIB_CHO, vals, {}, {}, \"\", \"M\", GRAPH_MOCHO)\n        cho_lines = [l for l in lines if _CONTRIB_CHO in l]\n        assert len(cho_lines) == 2\n\n\nclass TestEmitContributorTriplesBareId:\n    _bare = \"E\" * 32\n\n    def test_bare_id_expanded_via_param(self):\n        index = {self._bare: f\"urn:ddbedm:Agent:{self._bare}\"}\n        vals = [{\"resource\": self._bare}]\n        lines = emit_contributor_triples(_CONTRIB_CHO, vals, {}, {}, \"\", \"M\", GRAPH_MOCHO, index)\n        assert any(f\"urn:ddbedm:Agent:{self._bare}\" in l for l in lines)\n\n\n# ── emit_prov_triples — provider_isil sanitize ────────────────────────────────\n\nclass TestEmitProvTriplesIsil:\n    def test_isil_with_unsafe_chars_sanitized(self):\n        from transform.emitters import emit_prov_triples\n        from transform.constants import GRAPH_PROV\n        record = {\n            \"properties\": {\"item-id\": \"A\" * 32},\n            \"provider-info\": {\"provider-ddb-id\": \"org123\", \"provider-isil\": \"DE-<isil>\"},\n            \"source\": {},\n        }\n        lines = emit_prov_triples(record, f\"http://example.org/{'A'*32}\", GRAPH_PROV)\n        isil_lines = [l for l in lines if \"isil\" in l.lower() or \"mocho#isil\" in l]\n        for line in isil_lines:\n            assert \"<DE-<isil>\" not in line\n            assert \"%3C\" in line or \"%3E\" in line\n\n\n# ── emit_place_stubs — split about ───────────────────────────────────────────\n\nclass TestEmitPlaceStubsSplitAbout:\n    def test_space_separated_about_uses_first_only(self):\n        uri1 = \"http://d-nb.info/gnd/4044283-4\"\n        uri2 = \"https://www.geonames.org/2855745\"\n        places = [{\"about\": f\"{uri1} {uri2}\", \"prefLabel\": [{\"$\": \"Potsdam\", \"lang\": \"de\"}]}]\n        lines = emit_place_stubs(places, GRAPH_MOCHO)\n        subjects = {l.split()[0] for l in lines}\n        assert subjects == {f\"<{uri1}>\"}\n        assert not any(uri2 in l.split()[0] for l in lines)\n\n    def test_no_space_in_subject_iri(self):\n        places = [{\"about\": \"http://a.org/1 http://b.org/2\",\n                   \"prefLabel\": [{\"$\": \"X\", \"lang\": \"de\"}]}]\n        lines = emit_place_stubs(places, GRAPH_MOCHO)\n        for line in lines:\n            subj = line.split()[0]\n            assert \" \" not in subj[1:-1]\n\n\n# ── emit_aggregation_triples — split resource URIs ───────────────────────────\n\nclass TestEmitAggregationSplitUri:\n    _cho = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"Z\" * 32 + \">\"\n\n    def test_isshownat_two_uris(self):\n        agg = {\"isShownAt\": {\"resource\": \"http://a.org/1 http://b.org/2\"}}\n        lines = emit_aggregation_triples(agg, self._cho, GRAPH_MOCHO)\n        src_lines = [l for l in lines if \"source\" in l or \"DCTERMS\" in l or\n                     \"http://purl.org/dc/terms/source\" in l]\n        assert len(lines) == 2\n\n    def test_no_space_in_any_iri(self):\n        agg = {\n            \"isShownAt\":   {\"resource\": \"http://a.org/1 http://a.org/2\"},\n            \"object\":      [{\"resource\": \"http://b.org/1 http://b.org/2\"}],\n        }\n        lines = emit_aggregation_triples(agg, self._cho, GRAPH_MOCHO)\n        for line in lines:\n            for part in line.split():\n                if part.startswith(\"<\") and part.endswith(\">\"):\n                    assert \" \" not in part[1:-1]\n\n\n# ── emit_current_location_triples ─────────────────────────────────────────────\n\n_EDM_CURRENT_LOC = EDM_NS + \"currentLocation\"\n_CURLOC_CHO = \"<https://gemea.ise.fiz-karlsruhe.de/mocho/\" + \"L\" * 32 + \">\"\n\n\nclass TestEmitCurrentLocationTriples:\n    def test_single_uri_emitted(self):\n        uri = \"http://d-nb.info/gnd/4044283-4\"\n        vals = [{\"resource\": uri, \"$\": \"\", \"lang\": \"\"}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {}, GRAPH_MOCHO)\n        assert any(_EDM_CURRENT_LOC in l and uri in l for l in lines)\n\n    def test_literal_pass_through(self):\n        vals = [{\"resource\": \"\", \"$\": \"Stadtbibliothek\", \"lang\": \"de\"}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {}, GRAPH_MOCHO)\n        assert any(_EDM_CURRENT_LOC in l and '\"Stadtbibliothek\"@de' in l for l in lines)\n\n    def test_two_uris_produce_two_triples(self):\n        uri1 = \"http://d-nb.info/gnd/4044283-4\"\n        uri2 = \"https://www.geonames.org/2855745\"\n        vals = [{\"resource\": f\"{uri1} {uri2}\"}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {}, GRAPH_MOCHO)\n        assert len([l for l in lines if _EDM_CURRENT_LOC in l]) == 2\n\n    def test_label_stub_from_place(self):\n        uri = \"http://d-nb.info/gnd/4044283-4\"\n        place = {\"about\": uri, \"prefLabel\": [{\"$\": \"Potsdam\", \"lang\": \"de\"}]}\n        vals = [{\"resource\": uri}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {uri: place}, GRAPH_MOCHO)\n        assert any('\"Potsdam\"@de' in l and uri in l for l in lines)\n\n    def test_no_rdf_type_emitted(self):\n        uri = \"http://d-nb.info/gnd/4044283-4\"\n        place = {\"about\": uri, \"prefLabel\": [{\"$\": \"X\", \"lang\": \"de\"}]}\n        vals = [{\"resource\": uri}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {uri: place}, GRAPH_MOCHO)\n        rdf_type = \"http://www.w3.org/1999/02/22-rdf-syntax-ns#type\"\n        assert not any(rdf_type in l for l in lines)\n\n    def test_dedup(self):\n        uri = \"http://d-nb.info/gnd/4044283-4\"\n        vals = [{\"resource\": uri}, {\"resource\": uri}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {}, GRAPH_MOCHO)\n        assert len([l for l in lines if _EDM_CURRENT_LOC in l]) == 1\n\n    def test_bare_id_expanded(self):\n        bare = \"F\" * 32\n        index = {bare: f\"urn:ddbedm:Place:{bare}\"}\n        vals = [{\"resource\": bare}]\n        lines = emit_current_location_triples(_CURLOC_CHO, vals, {}, GRAPH_MOCHO, index)\n        assert any(f\"urn:ddbedm:Place:{bare}\" in l for l in lines)\n\n\n# ── TestFixtures — integration tests on real corpus records ───────────────────\n\n_FIXTURES = Path(__file__).parent / \"fixtures\"\n_CONFIG   = PROJECT_DIR / \"output\" / \"config\"\n\n\ndef _load_configs():\n    from transform.loaders import (\n        load_class_prop_alignment, load_lido_event_types,\n        load_htype_map, load_mediatype_class, load_audio_type2class,\n    )\n    return (\n        load_mediatype_class(_CONFIG / \"lookup_mediatype_class.csv\"),\n        load_htype_map(_CONFIG / \"lookup_htype_doco_rico.csv\"),\n        load_audio_type2class(_CONFIG / \"audio_type2class.json\"),\n        load_class_prop_alignment(_CONFIG / \"lookup_class_prop_alignment.csv\"),\n        load_lido_event_types(_CONFIG / \"lido_event_types.csv\"),\n    )\n\n\nimport json as _json\n\n\ndef _run_fixture(name: str) -> list[str]:\n    mc_map, ht_map, at_map, cpa, lido = _load_configs()\n    with open(_FIXTURES / f\"{name}.json\", encoding=\"utf-8\") as f:\n        rec = _json.load(f)\n    streams, *_ = transform_record(rec, None, mc_map, ht_map, at_map, cpa, lido)\n    return [nq for lines in (streams or {}).values() for nq in lines]\n\n\nclass TestFixtures:\n    def test_multi_uri_no_space_in_iri(self):\n        lines = _run_fixture(\"multi_uri\")\n        for line in lines:\n            for part in line.split():\n                if part.startswith(\"<\") and part.endswith(\">\"):\n                    assert \" \" not in part[1:-1], f\"Space in IRI: {part}\"\n\n    def test_multi_uri_place_split(self):\n        lines = _run_fixture(\"multi_uri\")\n        gnd_uri  = \"http://d-nb.info/gnd/4044283-4\"\n        geo_uri  = \"https://www.geonames.org/2855745\"\n        place_subjects = {l.split()[0] for l in lines if \"prefLabel\" in l or \"label\" in l.lower()}\n        assert any(gnd_uri in l for l in lines), \"GND place URI missing\"\n        assert not any(f\"{gnd_uri} {geo_uri}\" in l for l in lines), \"URIs not split\"\n\n    def test_br_tag_normalized(self):\n        lines = _run_fixture(\"br_tag\")\n        assert not any(\"<br\" in l.lower() for l in lines), \"<br> tag not normalized\"\n        assert any(r\"\\n\" in l for l in lines), r\"Expected \\n in output\"\n\n    def test_bare_id_hastype_expanded(self):\n        bare = \"DJVX2BT7X2HN24O6YRDOQM6T3CNZYYY6\"\n        lines = _run_fixture(\"bare_id\")\n        assert not any(f\"<{bare}>\" in l for l in lines), \"Bare ID not expanded\"\n        assert any(f\"urn:ddbedm:Concept:{bare}\" in l for l in lines), \"Expanded URN missing\""
}
```

---

### User *(2026-05-07T17:05:50.086Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:05:54.933Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust && .venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -30",
  "description": "Run full test suite"
}
```

---

### User *(2026-05-07T17:05:57.417Z)*

**Tool result**
```
configs = ({('any', 'any'): {'rdf_type_m': 'https://ise-fizkarlsruhe.github.io/ddbkg/mocho#Manifestation', 'rdf_type_w': '', 'us...://purl.org/dc/elements/1.1/contributor', 'rico_agent_prop': 'http://purl.org/dc/elements/1.1/contributor', ...}, ...})
dctype_vals = None

    def _call(self, sector, mediatype, htype, configs, dctype_vals=None):
>       mc_map, ht_map = configs
E       ValueError: too many values to unpack (expected 2)

scripts/transform/tests/test_transform.py:200: ValueError
_________________ TestResourceUris.test_unsafe_chars_sanitized _________________

self = <transform.tests.test_transform.TestResourceUris object at 0x1086c8700>

    def test_unsafe_chars_sanitized(self):
        uri = "http://example.org/item with space"
        result = resource_uris(uri)
        assert " " not in result[0]
>       assert "%20" in result[0]
E       AssertionError: assert '%20' in 'http://example.org/item'

scripts/transform/tests/test_transform.py:682: AssertionError
=========================== short test summary info ============================
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_sparte004_mt003_no_htype_fallback
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_sparte001_mt003_htype021
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_htype_emitted_as_iri
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_no_htype_no_hierarchy_type_triple
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_sparte003_mt001_fixed
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_mt007_guard_does_not_add_types_here
FAILED scripts/transform/tests/test_transform.py::TestRetypeEntities::test_unknown_sector_mediatype_fallback
FAILED scripts/transform/tests/test_transform.py::TestResourceUris::test_unsafe_chars_sanitized
8 failed, 98 passed in 0.25s
```

---

### Assistant *(2026-05-07T17:06:07.457Z)*

Two fixes needed: `_load_configs` name collision, and the space-in-URI test is wrong (spaces are URI separators, not sanitizable):

---

### Assistant *(2026-05-07T17:06:08.957Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "    def test_unsafe_chars_sanitized(self):\n        uri = \"http://example.org/item with space\"\n        result = resource_uris(uri)\n        assert \" \" not in result[0]\n        assert \"%20\" in result[0]",
  "new_string": "    def test_unsafe_chars_sanitized(self):\n        uri = \"http://example.org/item<foo>\"\n        result = resource_uris(uri)\n        assert len(result) == 1\n        assert \"%3C\" in result[0] and \"%3E\" in result[0]"
}
```

---

### User *(2026-05-07T17:06:10.502Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:06:19.649Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py",
  "old_string": "def _load_configs():\n    from transform.loaders import (\n        load_class_prop_alignment, load_lido_event_types,\n        load_htype_map, load_mediatype_class, load_audio_type2class,\n    )\n    return (\n        load_mediatype_class(_CONFIG / \"lookup_mediatype_class.csv\"),\n        load_htype_map(_CONFIG / \"lookup_htype_doco_rico.csv\"),\n        load_audio_type2class(_CONFIG / \"audio_type2class.json\"),\n        load_class_prop_alignment(_CONFIG / \"lookup_class_prop_alignment.csv\"),\n        load_lido_event_types(_CONFIG / \"lido_event_types.csv\"),\n    )\n\n\nimport json as _json\n\n\ndef _run_fixture(name: str) -> list[str]:\n    mc_map, ht_map, at_map, cpa, lido = _load_configs()",
  "new_string": "def _fixture_configs():\n    from transform.loaders import (\n        load_class_prop_alignment, load_lido_event_types,\n        load_htype_map, load_mediatype_class, load_audio_type2class,\n    )\n    return (\n        load_mediatype_class(_CONFIG / \"lookup_mediatype_class.csv\"),\n        load_htype_map(_CONFIG / \"lookup_htype_doco_rico.csv\"),\n        load_audio_type2class(_CONFIG / \"audio_type2class.json\"),\n        load_class_prop_alignment(_CONFIG / \"lookup_class_prop_alignment.csv\"),\n        load_lido_event_types(_CONFIG / \"lido_event_types.csv\"),\n    )\n\n\nimport json as _json\n\n\ndef _run_fixture(name: str) -> list[str]:\n    mc_map, ht_map, at_map, cpa, lido = _fixture_configs()"
}
```

---

### User *(2026-05-07T17:06:58.909Z)*

**Tool result**
```
The file /Users/mta/Documents/claude/goethe-faust/scripts/transform/tests/test_transform.py has been updated successfully.
```

---

### Assistant *(2026-05-07T17:07:02.930Z)*

**Tool call:** `Bash`
```json
{
  "command": ".venv/bin/pytest scripts/transform/tests/test_transform.py -q 2>&1 | tail -15",
  "description": "Run full test suite"
}
```

---

### User *(2026-05-07T17:07:06.304Z)*

**Tool result**
```
........................................................................ [ 67%]
..................................                                       [100%]
106 passed in 0.16s
```

---

### Assistant *(2026-05-07T17:07:08.676Z)*

All 106 pass.

---

### Assistant *(2026-05-07T17:07:09.911Z)*

**Tool call:** `TodoWrite`
```json
{
  "todos": [
    {
      "content": "Add resource_uris() to utils.py",
      "activeForm": "Adding resource_uris() to utils.py",
      "status": "completed"
    },
    {
      "content": "Fix all existing emitters + constants (_MOCHO_SKIP)",
      "activeForm": "Fixing all existing emitters + constants",
      "status": "completed"
    },
    {
      "content": "Add emit_current_location_triples + places_index in emit_mocho_triples",
      "activeForm": "Adding emit_current_location_triples",
      "status": "completed"
    },
    {
      "content": "Extract fixture records + write make_fixtures.py",
      "activeForm": "Extracting fixture records",
      "status": "completed"
    },
    {
      "content": "Write unit tests + TestFixtures integration class",
      "activeForm": "Writing tests",
      "status": "completed"
    }
  ]
}
```

---

### User *(2026-05-07T17:07:09.911Z)*

**Tool result**
```
Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable
```

---

### Assistant *(2026-05-07T17:07:22.166Z)*

All done. 106 tests pass (69 existing + 37 new). Summary of what was implemented:

1. **`resource_uris()`** — new utility in `utils.py`: split + bare-ID expand + sanitize in one place
2. **Emitter fixes** — `emit_subject_triples`, `emit_hastype_triples`, `emit_creator_triples` (+ `bare_id_to_uri` param + `agent_uri` sanitize), `emit_contributor_triples` (+ `bare_id_to_uri` param), `emit_prov_triples` (`provider_isil`), `emit_place_stubs` (first-part split), `emit_aggregation_triples` (inline split); `_MOCHO_SKIP` updated; `bare_id_to_uri` passed through `emit_mocho_triples`
3. **`emit_current_location_triples`** — IRI-with-label-stub, literal pass-through, no `rdf:type` (D17); `places_index` built in `emit_mocho_triples`
4. **Fixtures** — `tests/fixtures/{multi_uri,br_tag,bare_id}.{json,nq}` + `make_fixtures.py`
5. **Tests** — `TestEscapeLiteralBr`, `TestResourceUris`, multi-URI/bare-ID tests for each emitter, `TestEmitCurrentLocationTriples`, `TestFixtures` integration class

---

### User *(2026-05-07T17:07:50.816Z)*

run on /Users/mta/Documents/claude/goethe-faust/data/items-all-goethe-faust.json

---

### Assistant *(2026-05-07T17:07:55.338Z)*

**Tool call:** `Bash`
```json
{
  "command": "cd /Users/mta/Documents/claude/goethe-faust/scripts && python -m transform --jsonl ../data/items-all-goethe-faust.json --stats dispatch --total 115432 --log-interval 10000 2>&1 | tail -5",
  "description": "Run full transform on goethe-faust corpus",
  "timeout": 600000
}
```

---

### User *(2026-05-07T17:09:08.807Z)*

**Tool result**
```
(Bash completed with no output)
```

---

### Assistant *(2026-05-07T17:09:11.495Z)*

**Tool call:** `Bash`
```json
{
  "command": "ls -lt /Users/mta/Documents/claude/goethe-faust/output/transform/ | head -5",
  "description": "Find the latest run directory"
}
```

---

### User *(2026-05-07T17:09:11.552Z)*

**Tool result**
```
total 0
drwxr-xr-x@  6 mta  staff  192 May  7 19:09 20260507_190805
drwxr-xr-x   2 mta  staff   64 May  7 09:20 20260506_131842
drwxr-xr-x   7 mta  staff  224 May  6 15:46 20260506_154602
drwxr-xr-x@  4 mta  staff  128 May  6 15:41 20260506_131816
```

---

### Assistant *(2026-05-07T17:09:14.378Z)*

**Tool call:** `Bash`
```json
{
  "command": "cat /Users/mta/Documents/claude/goethe-faust/output/transform/20260507_190805/items-all-goethe-faust-stats.json",
  "description": "Show run stats"
}
```

---

### User *(2026-05-07T17:09:14.418Z)*

**Tool result**
```
{
  "run": {
    "timestamp": "20260507_190805",
    "input": "../data/items-all-goethe-faust.json",
    "stats_level": "dispatch",
    "elapsed_s": 63.3,
    "interrupted": false
  },
  "records": {
    "processed": 115432,
    "skipped_not_in_ids": 0,
    "by_mediatype": {
      "mt003": 52247,
      "mt007": 42360,
      "mt002": 20228,
      "mt001": 476,
      "mt005": 96,
      "any": 25
    },
    "by_htype": {
      "ht021": 24630,
      "ht034": 23183,
      "ht035": 19166,
      "ht007": 6644,
      "ht018": 6156,
      "ht006": 4638,
      "ht026": 3111,
      "ht001": 3076,
      "ht030": 985,
      "ht015": 450,
      "ht023": 155,
      "ht019": 133,
      "ht013": 120,
      "ht003": 101,
      "ht020": 77,
      "ht028": 66,
      "ht017": 62,
      "ht016": 52,
      "ht038": 49,
      "ht014": 39,
      "ht008": 19,
      "ht029": 10,
      "ht004": 9,
      "ht031": 9,
      "ht032": 9,
      "ht037": 5,
      "ht027": 2,
      "ht010": 1
    },
    "uri_sanitized": 29,
    "uri_split": 2685,
    "uri_about_split": 1309,
    "errors": {
      "json_parse": 0,
      "transform": 0
    }
  },
  "triples": {
    "total": 14764352,
    "by_graph": {
      "ddbedm": 8957734,
      "mocho": 1950504,
      "prov": 3856114
    }
  },
  "werk_staging": {
    "rows": 0,
    "by_class": {}
  },
  "dispatch": {
    "htype_hits": 25644,
    "mediatype_hits": 47428,
    "fallback_d9": 0,
    "skipped_mt007": 42360,
    "work_classes": {
      "vra:Work": 8972,
      "mocho:ImageWork": 3792,
      "mocho:ImmovableWork": 97,
      "ec:EditorialWork": 88,
      "rdac:C10001": 15
    },
    "expression_classes": {},
    "manifestation_classes": {
      "mocho:Manifestation": 28913,
      "mocho:ImageManifestation": 5100,
      "doco:TextChunk": 2993,
      "doco:Figure": 577,
      "aco:AudioManifestation": 466,
      "doco:Section": 162,
      "doco:Chapter": 91,
      "doco:Part": 2
    },
    "rico_classes": {
      "rico:RecordPart": 18648,
      "rico:Record": 3156
    }
  },
  "ddbedm_classes": {
    "skos:Concept": 717638,
    "edm:Agent": 422026,
    "edm:WebResource": 312538,
    "edm:Event": 158407,
    "edm:Place": 118088,
    "ore:Aggregation": 115432,
    "edm:ProvidedCHO": 115432,
    "edm:TimeSpan": 99930,
    "edm:PhysicalThing": 55771
  },
  "ddbedm_vocab": {
    "properties_all": {
      "skos:prefLabel": 829843,
      "dcterms:subject": 606086,
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": 427909,
      "skos:notation": 427909,
      "dcterms:rights": 353746,
      "dc:subject": 302946,
      "edm:hasType": 264585,
      "edm:rights": 257360,
      "edm:dataProvider": 230864,
      "dcterms:isPartOf": 178303,
      "dc:title": 171203,
      "edm:hasMet": 158407,
      "ddb:edm/hierarchyType": 148728,
      "http://www.cidoc-crm.org/cidoc-crm/P11_had_participant": 146228,
      "edm:wasPresentAt": 146207,
      "dc:identifier": 145126,
      "dc:description": 141935,
      "edm:hasView": 136759,
      "ddb:aggregationEntity": 132626,
      "edm:isShownAt": 115825,
      "edm:aggregatedCHO": 115432,
      "edm:provider": 115432,
      "ddb:hierarchyPosition": 104849,
      "edm:occurredAt": 102859,
      "edm:begin": 99928,
      "edm:end": 99928,
      "dcterms:extent": 95808,
      "dc:type": 92853,
      "edm:type": 73045,
      "dcterms:language": 72662,
      "dc:language": 71681,
      "dc:creator": 62984,
      "edm:isShownBy": 60386,
      "dc:contributor": 58993,
      "dc:date": 55602,
      "edm:currentLocation": 51200,
      "edm:happenedAt": 49816,
      "dcterms:issued": 48435,
      "edm:object": 39522,
      "dc:format": 20496,
      "dcterms:spatial": 12332,
      "edm:aggregator": 7742,
      "dcterms:alternative": 6583
    }
  },
  "mocho_vocab": {
    "properties_all": {
      "rdfs:label": 302578,
      "dcterms:subject": 180573,
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": 162807,
      "dc:subject": 107275,
      "dc:identifier": 83354,
      "dcterms:source": 73206,
      "owl:sameAs": 73072,
      "dc:title": 73072,
      "edm:dataProvider": 73070,
      "mocho:mediaType": 73045,
      "edm:hasType": 69963,
      "dcterms:extent": 54334,
      "dcterms:creator": 53453,
      "ddb:edm/hierarchyType": 52614,
      "dc:language": 49466,
      "foaf:thumbnail": 39518,
      "dc:contributor": 36773,
      "edm:currentLocation": 31837,
      "dcterms:language": 30405,
      "dcterms:issued": 29853,
      "rdam:P30134": 28913,
      "rico:note": 27196,
      "rico:creationDate": 23306,
      "dcterms:isPartOf": 22727,
      "rico:hasOrHadTitle": 21804,
      "rico:hasOrHadIdentifier": 21723,
      "dc:description": 20872,
      "rico:hasOrHadLanguage": 20040,
      "vra:description": 17168,
      "dc:format": 15597,
      "rdam:P30020": 14127,
      "rdam:P30137": 12660,
      "dcterms:spatial": 12048,
      "vra:title": 8972,
      "dc:date": 8570,
      "rdam:P30329": 8266,
      "vra:dateCreated": 7216,
      "rdaw:P10088": 3904,
      "dcterms:alternative": 2705,
      "rdam:P30128": 2241,
      "vra:partOf": 74,
      "rdam:P30278": 21,
      "vra:producer": 20,
      "rdaw:P10330": 19,
      "vra:photographer": 19,
      "rico:hasCreator": 14,
      "rdaw:P10065": 8,
      "rdaw:P10086": 4,
      "rdam:P30083": 2
    },
    "properties_new": {
      "mocho:mediaType": 73045,
      "rdam:P30134": 28913,
      "rico:note": 27196,
      "rico:creationDate": 23306,
      "rico:hasOrHadTitle": 21804,
      "rico:hasOrHadIdentifier": 21723,
      "rico:hasOrHadLanguage": 20040,
      "vra:description": 17168,
      "rdam:P30020": 14127,
      "rdam:P30137": 12660,
      "vra:title": 8972,
      "rdam:P30329": 8266,
      "vra:dateCreated": 7216,
      "rdaw:P10088": 3904,
      "rdam:P30128": 2241,
      "vra:partOf": 74,
      "rdam:P30278": 21,
      "vra:producer": 20,
      "rdaw:P10330": 19,
      "vra:photographer": 19,
      "rico:hasCreator": 14,
      "rdaw:P10065": 8,
      "rdaw:P10086": 4,
      "rdam:P30083": 2
    }
  }
}
```

---

### Assistant *(2026-05-07T17:09:27.872Z)*

Clean run. Key numbers vs the POC:

| Metric | POC (2026-05-06) | This run (2026-05-07) | Delta |
|---|---|---|---|
| Records | 115,432 | 115,432 | — |
| Triples total | 14,713,376 | 14,764,352 | +50,976 |
| ddbedm | 8,957,262 | 8,957,734 | +472 |
| mocho | 1,898,754 | 1,950,504 | **+51,750** |
| prov | 3,857,360 | 3,856,114 | −1,246 |
| Errors | 0 | 0 | — |
| uri_split | 4,188 | 2,685 | −1,503 |

The mocho graph gained ~51k triples — that's `edm:currentLocation` (31,837 triples) + label stubs + the creator/contributor/subject bare-ID expansions and multi-URI splits now landing correctly. `uri_split` dropped by ~1,500 because some previously-counted splits in the generic loop are now handled by the special emitters (and counted differently). Zero errors.

---
