#!/usr/bin/env python3
"""
Natural language query interface for the content knowledge graph.

Uses Claude to translate natural language questions into Cypher queries.

Usage:
    python scripts/nl-query.py "What curricula are mentioned with Charlotte Mason?"
    python scripts/nl-query.py "Who are the most referenced people?"
    python scripts/nl-query.py "Find content about math anxiety"
"""

import os
import sys
import json
import anthropic
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "demodemo"

SCHEMA_DESCRIPTION = """
The graph has these node types:
- Article: content files (properties: filepath, filename, title, source_type)
- Tool: curricula, apps, platforms mentioned (properties: name)
- Person: educators, authors, founders mentioned (properties: name, role)
- Resource: books, communities, websites (properties: name, type)
- Concept: topics/keywords discussed (properties: name - always lowercase)
- Curriculum: products from curricula database (properties: id, name, slug, description, pricing, philosophy_tags, website)
- Philosophy: education philosophies (properties: code, name) - codes: CL, CM, MO, WA, TR, UN, WF, PB, MS, NB, EC, FB

Relationships:
- (Article)-[:MENTIONS_TOOL]->(Tool)
- (Article)-[:MENTIONS_PERSON]->(Person)
- (Article)-[:MENTIONS_RESOURCE]->(Resource)
- (Article)-[:DISCUSSES]->(Concept)
- (Curriculum)-[:SAME_AS]->(Tool) - links database products to content mentions
- (Curriculum)-[:HAS_PHILOSOPHY]->(Philosophy)
"""

SYSTEM_PROMPT = f"""You are a Cypher query generator for a Neo4j knowledge graph about homeschool education content.

{SCHEMA_DESCRIPTION}

When given a natural language question, respond with ONLY a valid Cypher query that answers it.
Do not include any explanation, just the query.

Guidelines:
- Use OPTIONAL MATCH when results might not exist
- Concept names are always lowercase
- For text search, use toLower() and CONTAINS
- Limit results to reasonable numbers (10-20) unless counting
- Return useful columns with clear names
"""


def generate_cypher(question: str) -> str:
    """Use Claude to generate Cypher from natural language."""
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}]
    )

    return response.content[0].text.strip()


def run_query(cypher: str) -> list:
    """Execute Cypher query."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        try:
            result = session.run(cypher)
            records = [dict(record) for record in result]
        except Exception as e:
            records = [{"error": str(e)}]
    driver.close()
    return records


def format_results(results: list) -> str:
    """Format query results for display."""
    if not results:
        return "No results found."

    if "error" in results[0]:
        return f"Query error: {results[0]['error']}"

    # Simple table-like formatting
    output = []
    keys = list(results[0].keys())

    for record in results:
        row = " | ".join(str(record.get(k, ""))[:50] for k in keys)
        output.append(row)

    header = " | ".join(keys)
    return f"{header}\n{'-' * len(header)}\n" + "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/nl-query.py \"your question\"")
        print("\nExamples:")
        print('  "What tools are mentioned with Charlotte Mason?"')
        print('  "Who are the most referenced people?"')
        print('  "Find articles about dyslexia"')
        print('  "Which curricula have the most content mentions?"')
        return

    question = " ".join(sys.argv[1:])

    print(f"Question: {question}\n")

    # Generate Cypher
    cypher = generate_cypher(question)
    print(f"Generated Cypher:\n{cypher}\n")

    # Run query
    results = run_query(cypher)

    # Format and display
    print("Results:")
    print(format_results(results))


if __name__ == "__main__":
    main()
