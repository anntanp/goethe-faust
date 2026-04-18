# OpenWebUI native SPARQL tool for QLever

## Why not MCPO

OpenWebUI's "Manage Tool Servers" (OpenAPI/MCPO) is broken with
Ollama — the `tools` parameter doesn't propagate through
OpenWebUI's Ollama proxy, so models never see or call MCPO tools.
This is a known upstream bug (open-webui/open-webui #7597).

## Solution

A **native Python tool** added via Workspace → Tools. These run
inside OpenWebUI's own Python runtime — no proxy layers, no
function-calling fragility. They appear in the ◈ chat menu and
work with any Ollama model that supports tool calling.

## Tool code

See `scripts/openwebui-sparql-tool.py` in this directory.

One function: `sparql_query(query: str) → str` — sends a SPARQL
SELECT query to QLever at `http://host.docker.internal:7030` and
returns JSON results.

## Setup

1. Open http://localhost:3000
2. Go to **Workspace → Tools → +**
3. Paste the contents of `scripts/openwebui-sparql-tool.py`
4. Click **Save**
5. In a chat, click **◈** → enable **QLever SPARQL Query**
6. Test:

   ```
   How many triples are in the dataset?
   ```

   The model will call `sparql_query` with:

   ```sparql
   SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }
   ```

   Expected result: ~8.6M

## Valves (configurable settings)

The tool exposes one valve in the OpenWebUI UI:

| Valve | Default | Description |
|-------|---------|-------------|
| `endpoint` | `http://host.docker.internal:7030` | QLever SPARQL URL |

Change this if QLever runs on a different host or port.
