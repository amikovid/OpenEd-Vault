#!/usr/bin/env python3
"""
Transform curriculum data from Webflow CSV to Convex-ready JSON.

Usage:
    python3 scripts/transform-curriculum-data.py

Input:
    - OpenEd - Tools.csv (Webflow export)
    - src/data/curricula.json (existing merged data)

Output:
    - src/data/curricula-convex.json (enriched, Convex-ready)
"""

import csv
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Optional

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
CSV_PATH = PROJECT_ROOT.parent / "OpenEd - Tools.csv"
EXISTING_JSON = PROJECT_ROOT / "src/data/curricula.json"
OUTPUT_PATH = PROJECT_ROOT / "src/data/curricula-convex.json"

# ============================================================================
# Official OpenEd Vendors
# ============================================================================

OPENED_VENDORS = {
    "accelerate", "adobe creative cloud", "aleks", "accelerate asu",
    "beast academy", "bottega", "brain buffet", "brainpop", "byu independent study",
    "byu", "canvas", "calvert", "ctc math", "clever", "class", "dreambox",
    "duolingo", "edgenuity", "edmentum", "apex", "exact path", "falcon aerolab",
    "generation genius", "gizmos", "great hearts", "ignite", "imagine language",
    "imagine math", "imagine my path", "ixl", "kiwico", "knowledge pillars",
    "legends of learning", "lexia", "mathseeds", "reading eggs", "microsoft 365",
    "musiquest", "mystery science", "newsela", "oc online", "on fire",
    "opened courses", "own it", "prodigy", "ramsey", "road to success",
    "rock by rock", "rosetta stone", "savvas", "savvy learning", "shmoop",
    "skill struck", "sneak on the lot", "snhu", "st math", "storycon", "tabc",
    "study island", "synthesis tutor", "talkbox", "twig", "typing.com",
    "unrulr", "utah's online library", "waterford",
}

def is_opened_vendor(name: str) -> bool:
    """Check if tool is an official OpenEd vendor."""
    name_lower = name.lower().strip()
    for vendor in OPENED_VENDORS:
        if vendor in name_lower:
            return True
    return False

# ============================================================================
# Philosophy Tag Mappings
# ============================================================================

PHILOSOPHY_MAPPINGS = {
    # Direct philosophy matches
    "charlotte mason": "CM",
    "classical": "CL",
    "traditional": "TR",
    "montessori": "MO",
    "waldorf": "WA",
    "steiner": "WA",
    "unschooling": "UN",
    "eclectic": "EC",
    "project-based": "PB",
    "project based": "PB",
    "nature-based": "NB",
    "nature based": "NB",
    "forest school": "NB",
    "wild + free": "WF",
    "wild and free": "WF",
    "faith-based": "FB",
    "christian": "FB",
    "biblical": "FB",
    "catholic": "FB",
    "microschool": "MS",

    # Inferred from teaching style
    "literature-based": "CM",
    "living books": "CM",
    "great books": "CL",
    "trivium": "CL",
    "rigorous": "CL",
    "hands-on": "MO",
    "self-directed": "MO",
    "play-based": "WA",
    "imagination": "WA",
}

# Method tags (not philosophies, but useful for filtering)
METHOD_KEYWORDS = {
    "adaptive", "mastery-based", "mastery", "gamified", "spiral",
    "orton-gillingham", "self-paced", "competency-based", "incremental",
    "multisensory", "research-based", "systematic", "personalized",
}

# Audience tags
AUDIENCE_KEYWORDS = {
    "secular", "christian", "catholic", "jewish", "inclusive",
    "special-needs", "gifted", "dyslexia", "adhd", "autism",
    "elementary", "middle school", "high school", "early learners",
}

def extract_philosophy_tags(text: str) -> list[str]:
    """Extract philosophy tags from descriptive text."""
    if not text:
        return ["EC"]  # Default to Eclectic

    tags = set()
    text_lower = text.lower()

    for keyword, tag in PHILOSOPHY_MAPPINGS.items():
        if keyword in text_lower:
            tags.add(tag)

    return list(tags) if tags else ["EC"]

def extract_method_tags(text: str) -> list[str]:
    """Extract teaching method tags."""
    if not text:
        return []

    tags = []
    text_lower = text.lower()

    for keyword in METHOD_KEYWORDS:
        if keyword in text_lower:
            tags.append(keyword)

    return tags

def extract_audience_tags(text: str) -> list[str]:
    """Extract audience tags."""
    if not text:
        return []

    tags = []
    text_lower = text.lower()

    for keyword in AUDIENCE_KEYWORDS:
        if keyword in text_lower:
            tags.append(keyword)

    return tags

# ============================================================================
# HTML Stripping
# ============================================================================

def strip_html(html_content: str) -> str:
    """Convert HTML to clean plain text."""
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, 'html.parser')

    # Replace <br> with newlines
    for br in soup.find_all('br'):
        br.replace_with('\n')

    # Replace <p> with double newlines
    for p in soup.find_all('p'):
        p.insert_before('\n\n')

    # Get text
    text = soup.get_text(separator=' ')

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()

    return text

# ============================================================================
# Price Tier Extraction
# ============================================================================

def extract_price_tier(pricing_text: str) -> str:
    """Extract price tier from pricing description."""
    if not pricing_text:
        return "$$"  # Default

    text_lower = pricing_text.lower()

    # Check for free (but not free trial)
    if "free" in text_lower and "trial" not in text_lower:
        # Make sure it's actually free, not just "free trial"
        if "completely free" in text_lower or "100% free" in text_lower:
            return "Free"

    # Look for price indicators
    prices = re.findall(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)', pricing_text)

    if prices:
        max_price = max(float(p.replace(',', '')) for p in prices)
        if max_price < 50:
            return "$"
        elif max_price < 200:
            return "$$"
        elif max_price < 500:
            return "$$$"
        else:
            return "$$$$"

    return "$$"  # Default

# ============================================================================
# Grade Range Normalization
# ============================================================================

def normalize_grade_range(grade_text: str) -> str:
    """Normalize grade range to consistent format."""
    if not grade_text:
        return "K-12"

    # Already clean formats
    clean_formats = ["K-12", "PreK-12", "1-12", "K-8", "K-5", "6-12", "9-12"]
    if grade_text in clean_formats:
        return grade_text

    # Convert number ranges
    if re.match(r'^\d+-\d+$', grade_text):
        return grade_text

    # Map common variations
    text_lower = grade_text.lower()
    if "elementary" in text_lower:
        return "K-5th"
    if "middle" in text_lower:
        return "6th-8th"
    if "high school" in text_lower:
        return "9th-12th"
    if "all" in text_lower:
        return "K-12"

    return grade_text

# ============================================================================
# Subject Tags
# ============================================================================

def parse_subject_tags(tags_string: str) -> list[str]:
    """Parse semicolon-separated tags."""
    if not tags_string:
        return []

    # Tags are semicolon-separated: "ai-adaptive; math; science"
    return [tag.strip() for tag in tags_string.split(';') if tag.strip()]

# ============================================================================
# Main Transformation
# ============================================================================

def transform_csv_row(row: dict) -> dict:
    """Transform a single CSV row to Convex schema."""

    # Combine philosophy text from multiple sources
    philosophy_text = row.get('Educational Philosophy', '')

    # Extract all tag types
    philosophy_tags = extract_philosophy_tags(philosophy_text)
    method_tags = extract_method_tags(philosophy_text)
    audience_tags = extract_audience_tags(philosophy_text)

    # Strip HTML from content fields
    description = strip_html(row.get('Subject Content', ''))
    teaching_format = strip_html(row.get('Teaching Format Content', ''))
    pricing_summary = strip_html(row.get('Pricing Content', ''))
    opened_insight = strip_html(row.get('Parent Feedback Content', ''))

    return {
        # Identity
        "slug": row.get('Slug', ''),
        "name": row.get('Name', ''),

        # Visual
        "imageUrl": None,  # To be filled from scraping
        "logoUrl": row.get('Icon', '') or None,

        # Core Info
        "website": row.get('Website', ''),
        "gradeRange": normalize_grade_range(row.get('AI Grade level', '')),

        # Philosophy (for quiz matching)
        "philosophyTags": philosophy_tags,
        "philosophyText": philosophy_text,

        # Teaching Method (for filtering)
        "methodTags": method_tags,

        # Audience (for filtering)
        "audienceTags": audience_tags,

        # Content
        "description": description,
        "teachingFormat": teaching_format,
        "pricingSummary": pricing_summary,
        "priceTier": extract_price_tier(pricing_summary),
        "parentInvolvement": row.get('Parent Involvement', ''),

        # Editorial
        "openedInsight": opened_insight,

        # Subject Tags
        "subjectTags": parse_subject_tags(row.get('Tags', '')),

        # OpenEd Partnership
        "isOpenEdVendor": is_opened_vendor(row.get('Name', '')),

        # Metadata
        "source": "webflow",
        "webflowItemId": row.get('Item ID', ''),
    }

def transform_existing_json(item: dict) -> dict:
    """Transform existing curricula.json item to new schema."""

    # Get philosophy text from existing tags
    existing_tags = item.get('philosophy_tags', [])
    philosophy_text = item.get('philosophy_text', '')

    return {
        # Identity
        "slug": item.get('slug', ''),
        "name": item.get('name', ''),

        # Visual
        "imageUrl": None,
        "logoUrl": None,

        # Core Info
        "website": item.get('website', ''),
        "gradeRange": item.get('grade_levels', 'K-12'),

        # Philosophy
        "philosophyTags": existing_tags if existing_tags else ["EC"],
        "philosophyText": philosophy_text,

        # Teaching Method & Audience
        "methodTags": extract_method_tags(philosophy_text),
        "audienceTags": extract_audience_tags(philosophy_text),

        # Content
        "description": item.get('description', ''),
        "teachingFormat": "",
        "pricingSummary": item.get('pricing', ''),
        "priceTier": extract_price_tier(item.get('pricing', '')),
        "parentInvolvement": "",

        # Editorial
        "openedInsight": item.get('opened_notes', ''),

        # Subject Tags
        "subjectTags": [],

        # OpenEd Partnership
        "isOpenEdVendor": is_opened_vendor(item.get('name', '')),

        # Metadata
        "source": item.get('source', 'markdown'),
    }

def main():
    print("=" * 60)
    print("Curriculum Data Transformation")
    print("=" * 60)

    all_curricula = {}

    # 1. Load and transform existing JSON
    if EXISTING_JSON.exists():
        print(f"\n1. Loading existing data: {EXISTING_JSON}")
        with open(EXISTING_JSON) as f:
            existing = json.load(f)

        for item in existing:
            transformed = transform_existing_json(item)
            slug = transformed['slug']
            if slug:
                all_curricula[slug] = transformed

        print(f"   Loaded {len(all_curricula)} items from existing JSON")

    # 2. Load and transform CSV (overwrites existing where overlap)
    if CSV_PATH.exists():
        print(f"\n2. Loading Webflow CSV: {CSV_PATH}")
        with open(CSV_PATH, 'r') as f:
            reader = csv.DictReader(f)
            csv_count = 0
            for row in reader:
                if row.get('Archived', 'false').lower() == 'true':
                    continue  # Skip archived
                if row.get('Draft', 'false').lower() == 'true':
                    continue  # Skip drafts

                transformed = transform_csv_row(row)
                slug = transformed['slug']
                if slug:
                    all_curricula[slug] = transformed
                    csv_count += 1

        print(f"   Loaded {csv_count} items from CSV (overwrites existing)")
    else:
        print(f"\n2. CSV not found: {CSV_PATH}")

    # 3. Convert to list and sort
    curricula_list = sorted(all_curricula.values(), key=lambda x: x['name'].lower())

    # 4. Stats
    print(f"\n3. Statistics:")
    print(f"   Total curricula: {len(curricula_list)}")

    vendors = sum(1 for c in curricula_list if c['isOpenEdVendor'])
    print(f"   OpenEd Vendors: {vendors}")

    with_insight = sum(1 for c in curricula_list if c['openedInsight'])
    print(f"   With OpenEd Insight: {with_insight}")

    # Philosophy breakdown
    from collections import Counter
    all_tags = []
    for c in curricula_list:
        all_tags.extend(c['philosophyTags'])
    tag_counts = Counter(all_tags)
    print(f"\n   Philosophy Tags:")
    for tag, count in tag_counts.most_common():
        print(f"      {tag}: {count}")

    # Price tier breakdown
    price_counts = Counter(c['priceTier'] for c in curricula_list)
    print(f"\n   Price Tiers:")
    for tier, count in sorted(price_counts.items()):
        print(f"      {tier}: {count}")

    # 5. Save output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(curricula_list, f, indent=2)

    print(f"\n4. Output saved to: {OUTPUT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
