#!/usr/bin/env python3
"""
Add vector embeddings to graph nodes for semantic search.

Uses Gemini's text-embedding-004 model to embed:
1. Article titles + first 500 chars
2. Tool descriptions
3. Concept names

Then creates Neo4j vector indexes for similarity search.

Usage:
    python scripts/add-embeddings.py
"""

import os
import time
from pathlib import Path
from neo4j import GraphDatabase
import google.generativeai as genai

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "demodemo"

# Gemini setup
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


def get_embedding(text: str) -> list[float]:
    """Get embedding vector from Gemini."""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']


def add_embeddings():
    """Add embeddings to graph nodes."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # Create vector index for articles
        try:
            session.run("""
                CREATE VECTOR INDEX article_embeddings IF NOT EXISTS
                FOR (a:Article) ON (a.embedding)
                OPTIONS {indexConfig: {
                    `vector.dimensions`: 768,
                    `vector.similarity_function`: 'cosine'
                }}
            """)
            print("Created article vector index")
        except Exception as e:
            print(f"Article index already exists or error: {e}")

        # Create vector index for tools
        try:
            session.run("""
                CREATE VECTOR INDEX tool_embeddings IF NOT EXISTS
                FOR (t:Tool) ON (t.embedding)
                OPTIONS {indexConfig: {
                    `vector.dimensions`: 768,
                    `vector.similarity_function`: 'cosine'
                }}
            """)
            print("Created tool vector index")
        except Exception as e:
            print(f"Tool index already exists or error: {e}")

        # Get articles without embeddings
        articles = session.run("""
            MATCH (a:Article)
            WHERE a.embedding IS NULL
            RETURN a.filepath as filepath, a.title as title, a.filename as filename
        """).data()

        print(f"\nEmbedding {len(articles)} articles...")

        for i, article in enumerate(articles):
            # Read article content for embedding
            filepath = article['filepath']
            title = article['title'] or article['filename']

            try:
                content = Path(filepath).read_text(encoding="utf-8", errors="ignore")[:1000]
                text_to_embed = f"{title}\n\n{content}"

                embedding = get_embedding(text_to_embed)

                session.run("""
                    MATCH (a:Article {filepath: $filepath})
                    SET a.embedding = $embedding
                """, filepath=filepath, embedding=embedding)

                if (i + 1) % 20 == 0:
                    print(f"  Embedded {i + 1}/{len(articles)} articles")
                    time.sleep(0.5)  # Rate limit

            except Exception as e:
                print(f"  Error embedding {filepath}: {e}")

        # Embed tools (using name only)
        tools = session.run("""
            MATCH (t:Tool)
            WHERE t.embedding IS NULL
            RETURN t.name as name
        """).data()

        print(f"\nEmbedding {len(tools)} tools...")

        for i, tool in enumerate(tools):
            try:
                embedding = get_embedding(tool['name'])
                session.run("""
                    MATCH (t:Tool {name: $name})
                    SET t.embedding = $embedding
                """, name=tool['name'], embedding=embedding)

                if (i + 1) % 50 == 0:
                    print(f"  Embedded {i + 1}/{len(tools)} tools")
                    time.sleep(0.5)

            except Exception as e:
                print(f"  Error embedding tool {tool['name']}: {e}")

        print("\nEmbeddings complete!")

        # Show final stats
        result = session.run("""
            MATCH (a:Article) WHERE a.embedding IS NOT NULL
            WITH count(a) as embedded_articles
            MATCH (t:Tool) WHERE t.embedding IS NOT NULL
            RETURN embedded_articles, count(t) as embedded_tools
        """).single()

        print(f"  - {result['embedded_articles']} articles with embeddings")
        print(f"  - {result['embedded_tools']} tools with embeddings")

    driver.close()


if __name__ == "__main__":
    add_embeddings()
