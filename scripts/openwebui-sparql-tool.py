"""
title: QLever SPARQL Query
description: Run SPARQL queries on the Goethe-Faust QLever instance
requirements: httpx
version: 0.1.0
"""

from pydantic import BaseModel, Field
import httpx


class Tools:
    class Valves(BaseModel):
        endpoint: str = Field(
            "http://host.docker.internal:7030",
            description="QLever SPARQL endpoint URL",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def sparql_query(self, query: str) -> str:
        """
        Execute a SPARQL query on the Goethe-Faust RDF dataset
        (8.6M triples, DDB EDM). Use for questions about items,
        creators, types, collections, or any structured data.

        :param query: A valid SPARQL SELECT or ASK query string.
        :return: SPARQL results as JSON text.
        """
        async with httpx.AsyncClient() as client:
            r = await client.get(
                self.valves.endpoint,
                params={"query": query},
                headers={
                    "Accept": "application/sparql-results+json"
                },
                timeout=30.0,
            )
            r.raise_for_status()
            return r.text
