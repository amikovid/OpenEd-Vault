#!/usr/bin/env python3
"""
Query the content knowledge graph.

Usage:
    python scripts/query-graph.py "your cypher query"
    python scripts/query-graph.py --tools           # List all tools
    python scripts/query-graph.py --people          # List all people
    python scripts/query-graph.py --concepts        # List all concepts
    python scripts/query-graph.py --stats           # Show graph stats
    python scripts/query-graph.py --related "Beast Academy"  # Find related content
"""

import sys
import json
import argparse
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "demodemo"


def run_query(query: str) -> list:
    """Execute Cypher query and return results."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run(query)
        records = [dict(record) for record in result]
    driver.close()
    return records


def show_stats():
    """Show graph statistics."""
    stats = run_query("""
        MATCH (a:Article) WITH count(a) as articles
        MATCH (t:Tool) WITH articles, count(t) as tools
        MATCH (p:Person) WITH articles, tools, count(p) as people
        MATCH (r:Resource) WITH articles, tools, people, count(r) as resources
        MATCH (c:Concept) WITH articles, tools, people, resources, count(c) as concepts
        RETURN articles, tools, people, resources, concepts
    """)[0]
    print("Graph Statistics:")
    print(f"  Articles:  {stats['articles']}")
    print(f"  Tools:     {stats['tools']}")
    print(f"  People:    {stats['people']}")
    print(f"  Resources: {stats['resources']}")
    print(f"  Concepts:  {stats['concepts']}")


def list_tools():
    """List all tools with mention counts."""
    results = run_query("""
        MATCH (t:Tool)
        OPTIONAL MATCH (t)<-[:MENTIONS_TOOL]-(a:Article)
        RETURN t.name as tool, count(a) as mentions
        ORDER BY mentions DESC
    """)
    print("Tools (by mention count):")
    for r in results:
        print(f"  {r['tool']}: {r['mentions']} mentions")


def list_people():
    """List all people with mention counts."""
    results = run_query("""
        MATCH (p:Person)
        OPTIONAL MATCH (p)<-[:MENTIONS_PERSON]-(a:Article)
        RETURN p.name as person, p.role as role, count(a) as mentions
        ORDER BY mentions DESC
    """)
    print("People (by mention count):")
    for r in results:
        role = f" ({r['role']})" if r['role'] else ""
        print(f"  {r['person']}{role}: {r['mentions']} mentions")


def list_concepts():
    """List all concepts with counts."""
    results = run_query("""
        MATCH (c:Concept)
        OPTIONAL MATCH (c)<-[:DISCUSSES]-(a:Article)
        RETURN c.name as concept, count(a) as mentions
        ORDER BY mentions DESC
        LIMIT 50
    """)
    print("Top Concepts:")
    for r in results:
        print(f"  {r['concept']}: {r['mentions']} articles")


def find_related(entity_name: str):
    """Find all content related to an entity."""
    # Try as tool first
    results = run_query(f"""
        MATCH (t:Tool {{name: "{entity_name}"}})<-[:MENTIONS_TOOL]-(a:Article)
        RETURN a.filename as article, a.source_type as type
    """)
    if results:
        print(f"Articles mentioning tool '{entity_name}':")
        for r in results:
            print(f"  [{r['type']}] {r['article']}")

        # Also find co-occurring tools
        co_tools = run_query(f"""
            MATCH (t:Tool {{name: "{entity_name}"}})<-[:MENTIONS_TOOL]-(a:Article)-[:MENTIONS_TOOL]->(t2:Tool)
            WHERE t2.name <> t.name
            RETURN t2.name as tool, count(a) as co_mentions
            ORDER BY co_mentions DESC
            LIMIT 10
        """)
        if co_tools:
            print(f"\nTools often mentioned with '{entity_name}':")
            for r in co_tools:
                print(f"  {r['tool']} ({r['co_mentions']}x)")
        return

    # Try as person
    results = run_query(f"""
        MATCH (p:Person {{name: "{entity_name}"}})<-[:MENTIONS_PERSON]-(a:Article)
        RETURN a.filename as article, a.source_type as type
    """)
    if results:
        print(f"Articles mentioning '{entity_name}':")
        for r in results:
            print(f"  [{r['type']}] {r['article']}")
        return

    # Try as concept (case insensitive)
    results = run_query(f"""
        MATCH (c:Concept)<-[:DISCUSSES]-(a:Article)
        WHERE toLower(c.name) CONTAINS toLower("{entity_name}")
        RETURN a.filename as article, c.name as concept
    """)
    if results:
        print(f"Articles discussing '{entity_name}':")
        for r in results:
            print(f"  {r['article']} (concept: {r['concept']})")
        return

    print(f"No results found for '{entity_name}'")


def main():
    parser = argparse.ArgumentParser(description="Query content knowledge graph")
    parser.add_argument("query", nargs="?", help="Cypher query to run")
    parser.add_argument("--stats", action="store_true", help="Show graph stats")
    parser.add_argument("--tools", action="store_true", help="List all tools")
    parser.add_argument("--people", action="store_true", help="List all people")
    parser.add_argument("--concepts", action="store_true", help="List concepts")
    parser.add_argument("--related", type=str, help="Find content related to entity")
    args = parser.parse_args()

    if args.stats:
        show_stats()
    elif args.tools:
        list_tools()
    elif args.people:
        list_people()
    elif args.concepts:
        list_concepts()
    elif args.related:
        find_related(args.related)
    elif args.query:
        results = run_query(args.query)
        print(json.dumps(results, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
