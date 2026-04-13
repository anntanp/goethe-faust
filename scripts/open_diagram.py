#!/usr/bin/env python3
# Purpose:    Open the goethe-faust setup diagram in mermaid.live.
# Usage:      python3 scripts/open_diagram.py
#             Prints the URL and opens it in the default browser.
# Inputs:     Inline Mermaid diagram string
# Outputs:    mermaid.live URL (stdout) + browser open
# Dependencies: Python 3 stdlib only
# Assumptions: Internet access to mermaid.live

import base64
import json
import webbrowser

DIAGRAM = """\
graph TB
    NT["📄 output/ddbedm-goethe-faust.nt\\n1.3 GB · 8.6M triples"]

    subgraph compose-qlever["docker-compose.qlever.yml"]
        QLever["adfreiburg/qlever:latest\\nSPARQL endpoint\\n:7030"]
        YASGUI["nginx:alpine\\nYASGUI\\n:7031"]
        SHMARQLq["ghcr.io/epoz/shmarql:latest\\nUI → QLever proxy\\n:7032"]
        QIdx["💾 data/qlever-index/\\nbinary index"]
    end

    subgraph compose-shmarql["docker-compose.shmarql.yml"]
        SHMARQL["ghcr.io/epoz/shmarql:latest\\nSPARQL + UI\\n:8030"]
        SStore["💾 data/shmarql-store/\\npyoxigraph store"]
    end

    MCP["mcp-server-qlever\\n(docker run, --network=host)"]
    Browser["🌐 Browser"]
    Claude["🤖 Claude Code"]

    NT -->|"mount :ro /input"| QLever
    QLever <-->|"bind mount"| QIdx
    NT -->|"mount :ro /data"| SHMARQL
    SHMARQL <-->|"bind mount"| SStore

    YASGUI -->|"depends_on healthy"| QLever
    SHMARQLq -->|"depends_on healthy"| QLever
    SHMARQLq -->|"ENDPOINT=http://qlever:7019"| QLever

    Browser -->|":7031"| YASGUI
    Browser -->|":7032"| SHMARQLq
    Browser -->|":7030 SPARQL"| QLever
    Browser -->|":8030"| SHMARQL

    Claude -->|"MCP tools"| MCP
    MCP -->|"http://localhost:7030"| QLever\
"""

payload = json.dumps({"code": DIAGRAM, "mermaid": {"theme": "default"}})
encoded = base64.urlsafe_b64encode(payload.encode()).decode()
url = "https://mermaid.live/edit#base64:" + encoded

print(url)
webbrowser.open(url)
