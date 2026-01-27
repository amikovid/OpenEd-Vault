#!/usr/bin/env python3
"""
Incremental Graph Update - Only process new/modified content.

This script:
1. Checks which files have been added or modified since last run
2. Extracts entities only from those files
3. Merges new entities into the existing graph
4. Regenerates the lookup database

Usage:
    python scripts/update-graph.py           # Update with new content
    python scripts/update-graph.py --force   # Force full re-extraction
    python scripts/update-graph.py --dry-run # Show what would be processed
"""

import os
import json
import glob
import argparse
import time
import hashlib
from pathlib import Path
from datetime import datetime

import google.generativeai as genai
from neo4j import GraphDatabase

# Config
CONTENT_DIR = Path("/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault/Content/Master Content Database")
DATA_DIR = Path(__file__).parent.parent / "data"
STATE_FILE = DATA_DIR / "graph-state.json"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "demodemo"

# Gemini setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")

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

Content:
{content}
"""


def get_file_hash(filepath: str) -> str:
    """Get MD5 hash of file content."""
    content = Path(filepath).read_bytes()
    return hashlib.md5(content).hexdigest()


def load_state() -> dict:
    """Load previous run state."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"files": {}, "last_run": None}


def save_state(state: dict):
    """Save current state."""
    state["last_run"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def detect_source_type(filepath: str) -> str:
    """Detect content type from file path."""
    path_lower = filepath.lower()
    if "podcast" in path_lower:
        return "podcast"
    elif "newsletter" in path_lower or "daily" in path_lower:
        return "newsletter"
    elif "blog" in path_lower:
        return "blog_post"
    return "other"


def extract_entities(content: str, filepath: str) -> dict:
    """Use Gemini to extract entities from content."""
    if len(content) > 30000:
        content = content[:30000] + "\n...[truncated]"

    prompt = EXTRACTION_PROMPT.replace("{content}", content)

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        data = json.loads(text)
        return {
            "filepath": filepath,
            "source_type": detect_source_type(filepath),
            "title": data.get("title", Path(filepath).stem),
            "tools": data.get("tools", []),
            "people": data.get("people", []),
            "resources": data.get("resources", []),
            "concepts": data.get("concepts", [])
        }
    except Exception as e:
        print(f"  Error: {e}")
        return None


def load_entities_to_neo4j(entities: dict):
    """Load single file's entities into Neo4j."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        filepath = entities["filepath"]

        # Create/update Article node
        session.run("""
            MERGE (a:Article {filepath: $filepath})
            SET a.title = $title,
                a.source_type = $source_type,
                a.filename = $filename,
                a.updated_at = datetime()
        """, filepath=filepath,
             title=entities["title"],
             source_type=entities["source_type"],
             filename=Path(filepath).name)

        # Clear old relationships for this article (in case of update)
        session.run("""
            MATCH (a:Article {filepath: $filepath})-[r]-()
            DELETE r
        """, filepath=filepath)

        # Create Tool nodes and relationships
        for tool in entities["tools"]:
            session.run("""
                MERGE (t:Tool {name: $name})
                WITH t
                MATCH (a:Article {filepath: $filepath})
                MERGE (a)-[r:MENTIONS_TOOL]->(t)
                SET r.context = $context
            """, name=tool["name"], filepath=filepath,
                 context=tool.get("context", ""))

        # Create Person nodes and relationships
        for person in entities["people"]:
            session.run("""
                MERGE (p:Person {name: $name})
                SET p.role = COALESCE(p.role, $role)
                WITH p
                MATCH (a:Article {filepath: $filepath})
                MERGE (a)-[r:MENTIONS_PERSON]->(p)
                SET r.context = $context
            """, name=person["name"], role=person.get("role", ""),
                 filepath=filepath, context=person.get("context", ""))

        # Create Resource nodes and relationships
        for resource in entities["resources"]:
            session.run("""
                MERGE (r:Resource {name: $name})
                SET r.type = COALESCE(r.type, $type)
                WITH r
                MATCH (a:Article {filepath: $filepath})
                MERGE (a)-[rel:MENTIONS_RESOURCE]->(r)
                SET rel.context = $context
            """, name=resource["name"], type=resource.get("type", ""),
                 filepath=filepath, context=resource.get("context", ""))

        # Create Concept nodes and relationships
        for concept in entities["concepts"]:
            session.run("""
                MERGE (c:Concept {name: $name})
                WITH c
                MATCH (a:Article {filepath: $filepath})
                MERGE (a)-[:DISCUSSES]->(c)
            """, name=concept.lower(), filepath=filepath)

    driver.close()


def regenerate_lookup():
    """Regenerate the entity lookup JSON."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    lookup = {"people": {}, "tools": {}, "concepts": {}, "resources": {}}

    with driver.session() as session:
        # People
        for r in session.run("""
            MATCH (p:Person)<-[r:MENTIONS_PERSON]-(a:Article)
            RETURN p.name as name, p.role as role,
                   collect({file: a.filepath, title: a.title, type: a.source_type}) as sources
        """):
            lookup["people"][r["name"]] = {"role": r["role"], "mention_count": len(r["sources"]), "sources": r["sources"]}

        # Tools
        for r in session.run("""
            MATCH (t:Tool)<-[r:MENTIONS_TOOL]-(a:Article)
            RETURN t.name as name, collect({file: a.filepath, title: a.title, type: a.source_type}) as sources
        """):
            lookup["tools"][r["name"]] = {"mention_count": len(r["sources"]), "sources": r["sources"]}

        # Concepts
        for r in session.run("""
            MATCH (c:Concept)<-[:DISCUSSES]-(a:Article)
            RETURN c.name as name, collect({file: a.filepath, title: a.title}) as sources
        """):
            lookup["concepts"][r["name"]] = {"article_count": len(r["sources"]), "sources": r["sources"]}

        # Resources
        for r in session.run("""
            MATCH (r:Resource)<-[:MENTIONS_RESOURCE]-(a:Article)
            RETURN r.name as name, r.type as type, collect({file: a.filepath, title: a.title}) as sources
        """):
            lookup["resources"][r["name"]] = {"type": r["type"], "mention_count": len(r["sources"]), "sources": r["sources"]}

    driver.close()

    with open(DATA_DIR / "entity-lookup.json", "w") as f:
        json.dump(lookup, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Incremental graph update")
    parser.add_argument("--force", action="store_true", help="Force full re-extraction")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    args = parser.parse_args()

    # Load previous state
    state = load_state()
    previous_files = state.get("files", {})

    # Find all current content files
    all_files = list(glob.glob(str(CONTENT_DIR / "**" / "*.md"), recursive=True))
    print(f"Found {len(all_files)} content files")

    # Determine which files need processing
    to_process = []
    current_files = {}

    for filepath in all_files:
        file_hash = get_file_hash(filepath)
        current_files[filepath] = file_hash

        if args.force:
            to_process.append(filepath)
        elif filepath not in previous_files:
            to_process.append(filepath)
            print(f"  NEW: {Path(filepath).name}")
        elif previous_files[filepath] != file_hash:
            to_process.append(filepath)
            print(f"  MODIFIED: {Path(filepath).name}")

    if not to_process:
        print("\nNo new or modified files to process.")
        return

    print(f"\n{len(to_process)} files to process")

    if args.dry_run:
        print("\n[Dry run - no changes made]")
        return

    # Process files
    for i, filepath in enumerate(to_process):
        print(f"[{i+1}/{len(to_process)}] {Path(filepath).name}")

        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        if len(content) < 100:
            print("  Skipping (too short)")
            continue

        entities = extract_entities(content, filepath)
        if entities:
            load_entities_to_neo4j(entities)
            print(f"  Extracted: {len(entities['tools'])} tools, {len(entities['people'])} people")

        if i > 0 and i % 10 == 0:
            time.sleep(1)

    # Save state
    state["files"] = current_files
    save_state(state)

    # Regenerate lookup
    print("\nRegenerating entity lookup...")
    regenerate_lookup()

    print("\nDone!")


if __name__ == "__main__":
    main()
