# EDM → mocho Transformation: Tabula Rasa

## 1. Layers

A transformation pipeline from EDM to another RDF schema proceeds in six ordered stages:

1. **Parse** — deserialize source records (JSON-LD, XML, Turtle) into an in-memory graph or document model
2. **Validate** — check that source conforms to EDM constraints before touching it (fail fast, log bad records)
3. **Map** — property-by-property translation (EDM predicates → mocho predicates, datatypes, languages)
4. **Reconcile** — resolve entity identity: blank nodes, URIs, literals that should be URIs (GND lookups, etc.)
5. **Enrich** — optional side-calls (external APIs, lookups, inference rules)
6. **Serialize** — write mocho-conformant triples to sink (file, triplestore, stream)

## 2. Software Engineering Patterns

### 2.1 Pipeline / Chain of Responsibility

Each layer is a stage that receives a record and passes it forward (or rejects it). Stages are composable and replaceable.

### 2.2 Record as unit of work

One EDM `ore:Aggregation` (or `edm:ProvidedCHO`) per record. Keep state local to the record; nothing shared across records except lookup tables.

### 2.3 Strategy pattern for mapping rules

Separate *what gets mapped* from *how*. A mapping registry — `{edm:title → mocho:titleProper, transform: literal_lang_filter}` — lets you swap rules without touching pipeline logic.

### 2.4 Streaming over batching

Use a generator/iterator model — never load all records into memory. Each record flows through all stages before the next one is read. In Python: `yield`; in Java: `Stream<>` or Reactor `Flux`.

```
source → parse → validate → map → reconcile → serialize → sink
         ↑ yields one record at a time through each stage
```

### 2.5 Dead-letter queue

Records that fail validation or mapping go to a separate error sink with the original record + error reason. Never silently drop.

### 2.6 Idempotent output

Serialize to named graphs keyed by source record URI. Re-running the pipeline overwrites only affected records.

## 3. Where to Start

1. **Write the mapping spec first** — a flat table: `source predicate | target predicate | cardinality | transform`. Forces enumeration of all decisions before writing code.
2. **Build the map stage alone** — hardcode two or three representative records, get the output right.
3. **Wrap in a streaming shell** — add parse/serialize around the working mapper.
4. **Add validate and reconcile** — once the happy path works.
5. **Add error handling last** — dead-letter, logging, metrics.

The mapping spec is the load-bearing artifact. Everything else is plumbing around it.
