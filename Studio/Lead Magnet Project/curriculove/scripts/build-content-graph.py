#!/usr/bin/env python3
"""
Content Graph Builder - Extract entities from OpenEd content and load into Neo4j.

Usage:
    python scripts/build-content-graph.py --sample 20  # Test with 20 files
    python scripts/build-content-graph.py              # Process all files
"""

import os
import json
import glob
import argparse
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

import google.generativeai as genai
from neo4j import GraphDatabase

# Config
CONTENT_DIR = Path("/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Content/Master Content Database")
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "demodemo"

# Gemini setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")


@dataclass
class ExtractedEntities:
    """Entities extracted from a single content file."""
    source_file: str
    source_type: str  # podcast, newsletter, blog_post
    title: str
    tools: list[dict]  # {name, context}
    people: list[dict]  # {name, role, context}
    resources: list[dict]  # {name, type, context}
    concepts: list[str]


EXTRACTION_PROMPT = """Extract entities from this homeschool/education content.

IMPORTANT: Only extract entities that are meaningfully discussed, not passing mentions.

Return JSON (no markdown, just raw JSON):
{
  "title": "article/episode title if present",
  "tools": [
    {"name": "exact curriculum/tool name", "context": "1-2 sentence quote or context"}
  ],
  "people": [
    {"name": "Full Name", "role": "author|educator|founder|guest", "context": "why mentioned"}
  ],
  "resources": [
    {"name": "resource name", "type": "book|community|website|podcast", "context": "brief context"}
  ],
  "concepts": ["charlotte mason", "unschooling", "math anxiety", "phonics"]
}

Rules:
- tools: Curricula, apps, platforms, programs (Beast Academy, Abeka, Khan Academy, etc.)
- people: Authors, educators, founders, podcast guests - NOT random name mentions
- resources: Books, communities, websites that aren't curricula
- concepts: Educational philosophies, methodologies, topics discussed

Content:
{content}
"""


def detect_source_type(filepath: str) -> str:
    """Detect content type from file path."""
    path_lower = filepath.lower()
    if "podcast" in path_lower:
        return "podcast"
    elif "newsletter" in path_lower or "daily" in path_lower:
        return "newsletter"
    elif "blog" in path_lower:
        return "blog_post"
    else:
        return "other"


def extract_entities(content: str, filepath: str) -> Optional[ExtractedEntities]:
    """Use Gemini to extract entities from content."""
    # Truncate very long content
    if len(content) > 30000:
        content = content[:30000] + "\n...[truncated]"

    prompt = EXTRACTION_PROMPT.replace("{content}", content)

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean up response - remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        data = json.loads(text)

        return ExtractedEntities(
            source_file=filepath,
            source_type=detect_source_type(filepath),
            title=data.get("title", Path(filepath).stem),
            tools=data.get("tools", []),
            people=data.get("people", []),
            resources=data.get("resources", []),
            concepts=data.get("concepts", [])
        )
    except Exception as e:
        print(f"  Error extracting from {filepath}: {e}")
        return None


def load_to_neo4j(entities_list: list[ExtractedEntities]):
    """Load extracted entities into Neo4j."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # Create constraints for uniqueness
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Article) REQUIRE a.filepath IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tool) REQUIRE t.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:Resource) REQUIRE r.name IS UNIQUE")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE")

        for entities in entities_list:
            # Create Article node
            session.run("""
                MERGE (a:Article {filepath: $filepath})
                SET a.title = $title,
                    a.source_type = $source_type,
                    a.filename = $filename
            """, filepath=entities.source_file,
                 title=entities.title,
                 source_type=entities.source_type,
                 filename=Path(entities.source_file).name)

            # Create Tool nodes and relationships
            for tool in entities.tools:
                session.run("""
                    MERGE (t:Tool {name: $name})
                    WITH t
                    MATCH (a:Article {filepath: $filepath})
                    MERGE (a)-[r:MENTIONS_TOOL]->(t)
                    SET r.context = $context
                """, name=tool["name"], filepath=entities.source_file,
                     context=tool.get("context", ""))

            # Create Person nodes and relationships
            for person in entities.people:
                session.run("""
                    MERGE (p:Person {name: $name})
                    SET p.role = $role
                    WITH p
                    MATCH (a:Article {filepath: $filepath})
                    MERGE (a)-[r:MENTIONS_PERSON]->(p)
                    SET r.context = $context
                """, name=person["name"], role=person.get("role", ""),
                     filepath=entities.source_file, context=person.get("context", ""))

            # Create Resource nodes and relationships
            for resource in entities.resources:
                session.run("""
                    MERGE (r:Resource {name: $name})
                    SET r.type = $type
                    WITH r
                    MATCH (a:Article {filepath: $filepath})
                    MERGE (a)-[rel:MENTIONS_RESOURCE]->(r)
                    SET rel.context = $context
                """, name=resource["name"], type=resource.get("type", ""),
                     filepath=entities.source_file, context=resource.get("context", ""))

            # Create Concept nodes and relationships
            for concept in entities.concepts:
                session.run("""
                    MERGE (c:Concept {name: $name})
                    WITH c
                    MATCH (a:Article {filepath: $filepath})
                    MERGE (a)-[:DISCUSSES]->(c)
                """, name=concept.lower(), filepath=entities.source_file)

        print(f"\nLoaded {len(entities_list)} articles into Neo4j")

        # Print summary stats
        result = session.run("""
            OPTIONAL MATCH (a:Article) WITH count(a) as articles
            OPTIONAL MATCH (t:Tool) WITH articles, count(t) as tools
            OPTIONAL MATCH (p:Person) WITH articles, tools, count(p) as people
            OPTIONAL MATCH (c:Concept) WITH articles, tools, people, count(c) as concepts
            RETURN articles, tools, people, concepts
        """)
        stats = result.single()
        if stats:
            print(f"Graph now contains:")
            print(f"  - {stats['articles']} articles")
            print(f"  - {stats['tools']} tools/curricula")
            print(f"  - {stats['people']} people")
            print(f"  - {stats['concepts']} concepts")

    driver.close()


def main():
    parser = argparse.ArgumentParser(description="Build content knowledge graph")
    parser.add_argument("--sample", type=int, help="Process only N files (for testing)")
    parser.add_argument("--output", type=str, help="Save extracted JSON to file")
    args = parser.parse_args()

    # Find all markdown files
    files = list(glob.glob(str(CONTENT_DIR / "**" / "*.md"), recursive=True))
    print(f"Found {len(files)} content files")

    if args.sample:
        files = files[:args.sample]
        print(f"Processing sample of {args.sample} files")

    # Extract entities
    all_entities = []
    for i, filepath in enumerate(files):
        print(f"[{i+1}/{len(files)}] Processing: {Path(filepath).name}")

        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        if len(content) < 100:
            print("  Skipping (too short)")
            continue

        entities = extract_entities(content, filepath)
        if entities:
            all_entities.append(entities)
            print(f"  Extracted: {len(entities.tools)} tools, {len(entities.people)} people, {len(entities.concepts)} concepts")

        # Rate limiting - Gemini has generous limits but let's be safe
        if i > 0 and i % 10 == 0:
            time.sleep(1)

    # Optionally save JSON
    if args.output:
        output_data = [asdict(e) for e in all_entities]
        Path(args.output).write_text(json.dumps(output_data, indent=2))
        print(f"\nSaved extraction results to {args.output}")

    # Load to Neo4j
    print("\nLoading to Neo4j...")
    load_to_neo4j(all_entities)

    print("\nDone! You can now query the graph.")


if __name__ == "__main__":
    main()
