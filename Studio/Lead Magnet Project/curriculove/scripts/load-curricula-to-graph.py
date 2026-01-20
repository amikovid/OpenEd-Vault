#!/usr/bin/env python3
"""
Load curricula.json into Neo4j and link to extracted tool mentions.

This script:
1. Loads curricula from data/curricula.json as CurriculumProduct nodes
2. Links them to extracted Tool nodes via SAME_AS relationships
3. Adds philosophy tags and other metadata

Usage:
    python scripts/load-curricula-to-graph.py
"""

import json
from pathlib import Path
from neo4j import GraphDatabase

CURRICULA_FILE = Path(__file__).parent.parent / "src" / "data" / "curricula-convex.json"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "demodemo"


def load_curricula():
    """Load curricula into Neo4j."""
    # Load curricula data
    with open(CURRICULA_FILE) as f:
        curricula = json.load(f)

    print(f"Loading {len(curricula)} curricula into Neo4j...")

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # Create constraint
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Curriculum) REQUIRE c.slug IS UNIQUE")

        loaded = 0
        linked = 0

        for curr in curricula:
            # Create Curriculum node
            session.run("""
                MERGE (c:Curriculum {slug: $slug})
                SET c.name = $name,
                    c.description = $description,
                    c.pricing = $pricing,
                    c.philosophy_tags = $philosophy_tags,
                    c.philosophy_text = $philosophy_text,
                    c.website = $website,
                    c.grade_range = $grade_range,
                    c.opened_insight = $opened_insight,
                    c.source = $source
            """,
                slug=curr.get("slug"),
                name=curr.get("name"),
                description=curr.get("description", ""),
                pricing=curr.get("pricingSummary", ""),
                philosophy_tags=curr.get("philosophyTags", []),
                philosophy_text=curr.get("philosophyText", ""),
                website=curr.get("website", ""),
                grade_range=curr.get("gradeRange", ""),
                opened_insight=curr.get("openedInsight", ""),
                source=curr.get("source", "markdown")
            )
            loaded += 1

            # Try to link to extracted Tool mentions (fuzzy match on name)
            result = session.run("""
                MATCH (c:Curriculum {slug: $slug})
                MATCH (t:Tool)
                WHERE toLower(t.name) = toLower($name)
                   OR toLower(t.name) CONTAINS toLower($name)
                   OR toLower($name) CONTAINS toLower(t.name)
                MERGE (c)-[:SAME_AS]->(t)
                RETURN count(t) as matches
            """, slug=curr.get("slug"), name=curr.get("name"))

            match_count = result.single()["matches"]
            if match_count > 0:
                linked += 1

        # Also create Philosophy nodes from tags
        session.run("""
            MATCH (c:Curriculum)
            UNWIND c.philosophy_tags as tag
            MERGE (p:Philosophy {code: tag})
            MERGE (c)-[:HAS_PHILOSOPHY]->(p)
        """)

        # Set philosophy names
        philosophy_names = {
            "CL": "Classical",
            "CM": "Charlotte Mason",
            "MO": "Montessori",
            "WA": "Waldorf/Steiner",
            "TR": "Traditional",
            "UN": "Unschooling",
            "WF": "Wild + Free",
            "PB": "Project-Based",
            "MS": "Microschool/Pod",
            "NB": "Nature-Based",
            "EC": "Eclectic",
            "FB": "Faith-Based"
        }
        for code, name in philosophy_names.items():
            session.run("""
                MATCH (p:Philosophy {code: $code})
                SET p.name = $name
            """, code=code, name=name)

        print(f"\nLoaded {loaded} curricula")
        print(f"Linked {linked} to extracted Tool mentions")

        # Show stats
        result = session.run("""
            MATCH (c:Curriculum) WITH count(c) as curricula
            OPTIONAL MATCH (c2:Curriculum)-[:SAME_AS]->(t:Tool) WITH curricula, count(DISTINCT c2) as linked
            OPTIONAL MATCH (p:Philosophy) WITH curricula, linked, count(p) as philosophies
            RETURN curricula, linked, philosophies
        """)
        stats = result.single()
        print(f"\nGraph now has:")
        print(f"  - {stats['curricula']} curriculum products")
        print(f"  - {stats['linked']} linked to content mentions")
        print(f"  - {stats['philosophies']} philosophy categories")

    driver.close()


if __name__ == "__main__":
    load_curricula()
