# Graph-level pipeline provenance — future plan

**Date**: 2026-05-05
**Status**: Future work (not yet implemented)
**Relation**: Extends `notes/ddbedm-prov-o-plan.md` Layer 1 (per-CHO DDB ingest provenance, implemented)
**ADR**: `notes/transform-adr.md` D11, D12

---

## 1. Overview

Layer 1 (per-CHO item provenance from DDB ingest metadata) is implemented.
This document specifies Layer 2: graph-level pipeline provenance using the PROV-O full Activity pattern.

Each named graph in the triplestore is treated as a `prov:Entity` produced by a `prov:Activity` (script run).
The key addition over a bare PROV-O Activity record is a `gemea:inferenceMethod` annotation that classifies the epistemic status of the triples in a graph — not their correctness, but how errors would be diagnosed and traced.

---

## 2. `gemea:inferenceMethod` vocabulary

### 2.1 Three-way classification

Three classes are defined. All three can produce incorrect triples; the distinction is the **audit path** — how an error would be found and fixed.

| Term | Reproducible? | Error traceable to | Examples |
|---|---|---|---|
| `gemea:Deterministic` | Yes — bit-for-bit given same input + software version | Explicit rule definition | EDM→mocho field mappings, type coercion, named graph assignment |
| `gemea:Heuristic` | Yes — given same rules and thresholds | Rule design or threshold choice | String-similarity GND entity linking, confidence-threshold filters |
| `gemea:ModelDerived` | No — varies across model versions, hardware, random seed | Model weights, training data, prompt | NER annotations, LLM-ranked or LLM-generated triples |

### 2.2 rdfs:comment definitions (for vocabulary file)

```turtle
@prefix gemea:   <https://gemea.ise.fiz-karlsruhe.de/vocab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

gemea:InferenceMethod
    a owl:Class ;
    rdfs:label "Inference method"@en ;
    rdfs:comment "Classification of the epistemic process by which triples in a named graph were produced. Conveys the audit path for errors, not a claim of correctness."@en .

gemea:Deterministic
    a gemea:InferenceMethod ;
    rdfs:label "Deterministic"@en ;
    rdfs:comment "The producing script applies fixed rules with no learned parameters or probabilistic components. Given identical inputs and software versions, the output is bit-for-bit reproducible. Errors are traceable to explicit rule definitions and are correctable by updating those rules."@en .

gemea:Heuristic
    a gemea:InferenceMethod ;
    rdfs:label "Heuristic"@en ;
    rdfs:comment "The producing script applies rule-based matching or scoring (e.g. string normalisation, edit-distance threshold, confidence filter) without a learned model. Output is reproducible given the same rules and thresholds, but correctness is not guaranteed. Errors are traceable to rule design choices or threshold calibration."@en .

gemea:ModelDerived
    a gemea:InferenceMethod ;
    rdfs:label "Model-derived"@en ;
    rdfs:comment "Triples were produced or ranked by a statistical model (NER tagger, language model, embeddings). Output may vary across model versions, hardware configurations, or random seeds and is therefore not fully reproducible. Errors are not directly traceable to an explicit rule; diagnosis requires inspection of model behaviour on specific inputs."@en .
```

### 2.3 Mapping from original four-way split

The original plan in `ddbedm-prov-o-plan.md` used four values (`Deterministic`, `Heuristic`, `NER`, `LLMGenerated`). `NER` and `LLMGenerated` are collapsed into `ModelDerived` here because they share the same audit-path properties: model-dependent, not fully reproducible, errors not traceable to a rule.

| Old term | New term | Rationale |
|---|---|---|
| `gemea:Deterministic` | `gemea:Deterministic` | Unchanged |
| `gemea:Heuristic` | `gemea:Heuristic` | Unchanged |
| `gemea:NER` | `gemea:ModelDerived` | NER is a statistical model; audit path = model behaviour |
| `gemea:LLMGenerated` | `gemea:ModelDerived` | LLM is a statistical model; audit path = model behaviour |

If finer-grained provenance is needed (e.g. to distinguish NER from LLM enrichment), a `gemea:modelType` literal on the agent node is preferred over adding more `inferenceMethod` values.

---

## 3. Layer 2 design

### 3.1 PROV-O Activity pattern

```
Named graph ──prov:wasGeneratedBy──► Run (Activity)
                                          │
                              prov:wasAssociatedWith
                                          │
                                          ▼
                                   Script / LLM agent
                                   (prov:SoftwareAgent)
```

All Layer 2 triples are stored in a single meta-graph: `<urn:goethe-faust:graph/prov>`.

URI patterns:

| Resource | URI pattern |
|---|---|
| Named graph | `urn:goethe-faust:graph/<name>` |
| Script run (Activity) | `urn:goethe-faust:run/<script-stem>/<ISO8601-timestamp>` |
| Script agent | `urn:goethe-faust:agent/<script-stem>` |
| Model agent | `urn:goethe-faust:agent/<model-id>` |

### 3.2 Named graphs catalogue

| Named graph | Producing script | `inferenceMethod` |
|---|---|---|
| `urn:goethe-faust:graph/transform` | `transform_edm_to_mocho.py` | `gemea:Deterministic` |
| `urn:goethe-faust:graph/gnd-agents` | `link_gnd_agents.py` | `gemea:Heuristic` |
| `urn:goethe-faust:graph/gnd-works` | `link_gnd_works.py` | `gemea:Heuristic` |
| `urn:goethe-faust:graph/ner` | NER script (TBD) | `gemea:ModelDerived` |
| `urn:goethe-faust:graph/llm` | LLM enrichment script (TBD) | `gemea:ModelDerived` |
| `urn:goethe-faust:graph/prov` | all scripts (self-referential) | `gemea:Deterministic` |

### 3.3 Triple mapping

#### 3.3.1 Named graph node

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Entity` |
| `prov:wasGeneratedBy` | runtime | run IRI |
| `gemea:inferenceMethod` | script config | `gemea:` vocab term |

#### 3.3.2 Run node

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:Activity` |
| `prov:startedAtTime` | runtime | xsd:dateTime |
| `prov:endedAtTime` | runtime | xsd:dateTime |
| `prov:wasAssociatedWith` | script config | agent IRI |
| `prov:used` | script config | input graph IRI(s) |
| `rdfs:comment` | optional | free-text note (e.g. threshold, model version) |

#### 3.3.3 Script agent

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:SoftwareAgent` |
| `rdfs:label` | script header | filename string |
| `dcterms:hasVersion` | script header or git tag | string literal |

#### 3.3.4 Model agent (NER / LLM)

| Triple | Source | Value type |
|---|---|---|
| `rdf:type` | — | `prov:SoftwareAgent` |
| `rdfs:label` | config | model name string |
| `dcterms:hasVersion` | config | model version / API version |
| `gemea:modelProvider` | config | string literal (e.g. `"Anthropic"`) |
| `gemea:modelType` | config | string literal (e.g. `"NER"`, `"LLM"`) |

### 3.4 Turtle example

```turtle
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix gemea:      <https://gemea.ise.fiz-karlsruhe.de/vocab/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .

# ── Deterministic: EDM → mocho transform ─────────────────────────────────────

<urn:goethe-faust:graph/transform>
    a prov:Entity ;
    prov:wasGeneratedBy <urn:goethe-faust:run/transform_edm_to_mocho/2026-05-03T09:14:22Z> ;
    gemea:inferenceMethod  gemea:Deterministic .

<urn:goethe-faust:run/transform_edm_to_mocho/2026-05-03T09:14:22Z>
    a prov:Activity ;
    prov:startedAtTime     "2026-05-03T09:14:22Z"^^xsd:dateTime ;
    prov:endedAtTime       "2026-05-03T09:31:05Z"^^xsd:dateTime ;
    prov:wasAssociatedWith <urn:goethe-faust:agent/transform_edm_to_mocho> ;
    prov:used              <urn:goethe-faust:graph/raw-json> .

<urn:goethe-faust:agent/transform_edm_to_mocho>
    a prov:SoftwareAgent ;
    rdfs:label         "transform_edm_to_mocho.py" ;
    dcterms:hasVersion "0.9.1" .

# ── Heuristic: GND agent linking ─────────────────────────────────────────────

<urn:goethe-faust:graph/gnd-agents>
    a prov:Entity ;
    prov:wasGeneratedBy <urn:goethe-faust:run/link_gnd_agents/2026-05-03T10:02:47Z> ;
    gemea:inferenceMethod  gemea:Heuristic .

<urn:goethe-faust:run/link_gnd_agents/2026-05-03T10:02:47Z>
    a prov:Activity ;
    prov:startedAtTime     "2026-05-03T10:02:47Z"^^xsd:dateTime ;
    prov:endedAtTime       "2026-05-03T10:44:19Z"^^xsd:dateTime ;
    prov:wasAssociatedWith <urn:goethe-faust:agent/link_gnd_agents> ;
    prov:used              <urn:goethe-faust:graph/transform> ;
    rdfs:comment           "lobid-gnd API; confidence threshold 0.85" .

<urn:goethe-faust:agent/link_gnd_agents>
    a prov:SoftwareAgent ;
    rdfs:label         "link_gnd_agents.py" ;
    dcterms:hasVersion "0.3.0" .

# ── ModelDerived: LLM enrichment ──────────────────────────────────────────────

<urn:goethe-faust:graph/llm>
    a prov:Entity ;
    prov:wasGeneratedBy <urn:goethe-faust:run/llm_enrich/2026-05-03T11:00:00Z> ;
    gemea:inferenceMethod  gemea:ModelDerived .

<urn:goethe-faust:run/llm_enrich/2026-05-03T11:00:00Z>
    a prov:Activity ;
    prov:startedAtTime     "2026-05-03T11:00:00Z"^^xsd:dateTime ;
    prov:endedAtTime       "2026-05-03T11:28:33Z"^^xsd:dateTime ;
    prov:wasAssociatedWith <urn:goethe-faust:agent/claude-sonnet-4-6> ;
    prov:used              <urn:goethe-faust:graph/transform> .

<urn:goethe-faust:agent/claude-sonnet-4-6>
    a prov:SoftwareAgent ;
    rdfs:label         "claude-sonnet-4-6" ;
    dcterms:hasVersion "claude-sonnet-4-6" ;
    gemea:modelProvider   "Anthropic" ;
    gemea:modelType       "LLM" .
```

---

## 4. Prefix declarations

| Prefix | URI |
|---|---|
| `prov:` | `http://www.w3.org/ns/prov#` |
| `gemea:` | `https://gemea.ise.fiz-karlsruhe.de/vocab/` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` |
| `owl:` | `http://www.w3.org/2002/07/owl#` |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` |
