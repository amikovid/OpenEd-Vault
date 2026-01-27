#!/usr/bin/env python3
"""
Enrich curriculum data using Gemini to infer:
- Improved philosophyTags (reduce EC defaults from 121 to <30)
- prepTimeScore (1-10)
- teacherInvolvementLevel (high/medium/low/zero)
- lessonDuration (short/medium/long)

PRESERVES all original data - only adds/updates inference fields.

Usage:
    python3 scripts/enrich-curriculum-data.py

Requires:
    pip install google-generativeai
    export GEMINI_API_KEY=your_key
"""

import json
import os
import time
from pathlib import Path
from typing import Optional
import google.generativeai as genai

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_PATH = PROJECT_ROOT / "src/data/curricula-convex.json"
OUTPUT_PATH = PROJECT_ROOT / "src/data/curricula-enriched.json"
PROGRESS_PATH = PROJECT_ROOT / "src/data/.enrichment-progress.json"

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # Try reading from .env.local
    env_path = PROJECT_ROOT / ".env.local"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    GEMINI_API_KEY = line.split("=", 1)[1].strip()
                    break

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment or .env.local")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3-flash-preview")

# Philosophy definitions for Gemini
PHILOSOPHY_GUIDE = """
Philosophy Tags (choose 1-3 that BEST fit, avoid EC unless truly eclectic):

CL = Classical: Great Books, Latin, Socratic method, trivium (grammar/logic/rhetoric), Western canon, rigorous academics, virtue formation
CM = Charlotte Mason: Living books (not textbooks), narration, nature study, short lessons (15-20 min), habit training, picture study, composer study
TR = Traditional: School-at-home, textbooks, workbooks, grades, tests, grade-level standards, structured schedule, career/college prep
MO = Montessori: Prepared environment, child chooses work, hands-on materials, mixed ages, self-correction, practical life skills
WA = Waldorf/Steiner: Delayed academics (no reading before 7), imagination-first, rhythm/routine, handwork, watercolor, oral storytelling
UN = Unschooling: No curriculum, radical trust in child, interest-led, no grades/tests, learning through life
EC = Eclectic: ONLY use if curriculum explicitly markets itself as "mix and match" or "pick what works" - NOT as a default
PB = Project-Based: Real-world problems, authentic products, interdisciplinary, student-driven inquiry
NB = Nature-Based: Forest school, outdoor classroom, risky play, nature as primary teacher
WF = Wild + Free: Wonder-based, nature-centered, beauty, community, combines CM elements with modern aesthetics
FB = Faith-Based: Faith integrated throughout all subjects (not just Bible class), Christian/Catholic/Jewish worldview
MS = Microschool: Small multi-age groups, pod learning, shared teaching responsibilities

IMPORTANT:
- EC should be rare (<15% of curricula). Most curricula have a clear philosophy even if they don't name it.
- Look for teaching METHOD clues: "living books" = CM, "video lessons with tests" = TR, "child chooses" = MO
- A curriculum can be FB + another philosophy (e.g., FB + CL for classical Christian)
"""

ENRICHMENT_PROMPT = """
Analyze this homeschool curriculum and return a JSON object with your inferences.

CURRICULUM DATA:
Name: {name}
Description: {description}
Teaching Format: {teaching_format}
Pricing: {pricing}
Parent Involvement: {parent_involvement}
Current Philosophy Tags: {current_tags}
Philosophy Text: {philosophy_text}
OpenEd Insight: {insight}

{philosophy_guide}

Return ONLY a JSON object (no markdown, no explanation):
{{
  "philosophyTags": ["TAG1", "TAG2"],  // 1-3 tags, be specific, avoid EC unless truly eclectic
  "philosophyReasoning": "Brief explanation of why these tags fit",
  "prepTimeScore": 5,  // 1-10 where 1=open-and-go, 10=heavy Sunday prep required
  "prepTimeReasoning": "Brief explanation",
  "teacherInvolvementLevel": "medium",  // high/medium/low/zero
  "teacherInvolvementReasoning": "Brief explanation",
  "lessonDuration": "medium"  // short (<30min), medium (30-60min), long (60+ min per subject)
}}
"""


def build_context(curriculum: dict) -> str:
    """Build context string from all available curriculum fields."""
    return ENRICHMENT_PROMPT.format(
        name=curriculum.get("name", ""),
        description=curriculum.get("description", "")[:1500],  # Truncate if massive
        teaching_format=curriculum.get("teachingFormat", "")[:1000],
        pricing=curriculum.get("pricingSummary", "")[:500],
        parent_involvement=curriculum.get("parentInvolvement", "")[:500],
        current_tags=", ".join(curriculum.get("philosophyTags", [])),
        philosophy_text=curriculum.get("philosophyText", ""),
        insight=curriculum.get("openedInsight", "")[:2000],  # These can be huge
        philosophy_guide=PHILOSOPHY_GUIDE,
    )


def enrich_curriculum(curriculum: dict) -> dict:
    """Enrich a single curriculum with Gemini inference."""
    prompt = build_context(curriculum)

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2,  # Low temp for consistency
            ),
        )

        result = json.loads(response.text)

        # Validate tags
        valid_tags = {"CL", "CM", "TR", "MO", "WA", "UN", "EC", "PB", "NB", "WF", "FB", "MS"}
        result["philosophyTags"] = [t for t in result.get("philosophyTags", []) if t in valid_tags]

        if not result["philosophyTags"]:
            result["philosophyTags"] = ["EC"]  # Fallback

        return result

    except Exception as e:
        print(f"  Error: {e}")
        return None


def load_progress() -> dict:
    """Load progress from checkpoint file."""
    if PROGRESS_PATH.exists():
        with open(PROGRESS_PATH) as f:
            return json.load(f)
    return {"processed": [], "enriched": {}}


def save_progress(progress: dict):
    """Save progress to checkpoint file."""
    with open(PROGRESS_PATH, "w") as f:
        json.dump(progress, f, indent=2)


def main():
    print("=" * 60)
    print("Curriculum Data Enrichment (Gemini)")
    print("=" * 60)

    # Load data
    with open(INPUT_PATH) as f:
        curricula = json.load(f)

    print(f"\nLoaded {len(curricula)} curricula from {INPUT_PATH}")

    # Count current EC defaults
    ec_count = sum(1 for c in curricula if c.get("philosophyTags") == ["EC"])
    print(f"Current EC-only count: {ec_count}")

    # Load progress
    progress = load_progress()
    processed_slugs = set(progress["processed"])
    print(f"Already processed: {len(processed_slugs)}")

    # Process each curriculum
    enriched_curricula = []
    new_ec_count = 0

    for i, curriculum in enumerate(curricula):
        slug = curriculum["slug"]
        name = curriculum["name"]

        # Preserve ALL original fields
        enriched = curriculum.copy()

        # Store original tags before overwriting
        if "originalPhilosophyTags" not in enriched:
            enriched["originalPhilosophyTags"] = curriculum.get("philosophyTags", [])

        if slug in processed_slugs:
            # Use cached enrichment
            cached = progress["enriched"].get(slug, {})
            if cached:
                enriched["philosophyTags"] = cached.get("philosophyTags", enriched["philosophyTags"])
                enriched["philosophyReasoning"] = cached.get("philosophyReasoning", "")
                enriched["prepTimeScore"] = cached.get("prepTimeScore")
                enriched["teacherInvolvementLevel"] = cached.get("teacherInvolvementLevel")
                enriched["lessonDuration"] = cached.get("lessonDuration")

            if enriched.get("philosophyTags") == ["EC"]:
                new_ec_count += 1
            enriched_curricula.append(enriched)
            continue

        print(f"\n[{i+1}/{len(curricula)}] {name}")

        # Call Gemini
        result = enrich_curriculum(curriculum)

        if result:
            enriched["philosophyTags"] = result["philosophyTags"]
            enriched["philosophyReasoning"] = result.get("philosophyReasoning", "")
            enriched["prepTimeScore"] = result.get("prepTimeScore")
            enriched["teacherInvolvementLevel"] = result.get("teacherInvolvementLevel")
            enriched["lessonDuration"] = result.get("lessonDuration")

            print(f"  Tags: {result['philosophyTags']}")
            print(f"  Prep: {result.get('prepTimeScore')}/10, Teacher: {result.get('teacherInvolvementLevel')}")

            # Cache result
            progress["enriched"][slug] = result
        else:
            print(f"  FAILED - keeping original tags")

        progress["processed"].append(slug)

        if enriched.get("philosophyTags") == ["EC"]:
            new_ec_count += 1

        enriched_curricula.append(enriched)

        # Save progress every 10 items
        if (i + 1) % 10 == 0:
            save_progress(progress)
            print(f"\n  [Checkpoint saved: {len(progress['processed'])} processed]")

        # Rate limiting (Gemini free tier: 15 RPM)
        time.sleep(4)

    # Final save
    save_progress(progress)

    # Sort and save output
    enriched_curricula.sort(key=lambda x: x["name"].lower())

    with open(OUTPUT_PATH, "w") as f:
        json.dump(enriched_curricula, f, indent=2)

    # Stats
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Total curricula: {len(enriched_curricula)}")
    print(f"EC-only count: {ec_count} -> {new_ec_count}")

    # Philosophy breakdown
    from collections import Counter
    all_tags = []
    for c in enriched_curricula:
        all_tags.extend(c.get("philosophyTags", []))
    tag_counts = Counter(all_tags)

    print(f"\nPhilosophy Distribution:")
    for tag, count in tag_counts.most_common():
        print(f"  {tag}: {count}")

    print(f"\nOutput saved to: {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
