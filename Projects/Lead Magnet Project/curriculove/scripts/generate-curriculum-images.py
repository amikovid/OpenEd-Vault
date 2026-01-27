#!/usr/bin/env python3
"""
Batch generate curriculum images using Gemini API.

Usage:
    python3 scripts/generate-curriculum-images.py
    python3 scripts/generate-curriculum-images.py --start 0 --count 20
    python3 scripts/generate-curriculum-images.py --skip-existing
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Install with: pip install google-genai")
    sys.exit(1)


VAULT_ROOT = Path(__file__).parent.parent.parent.parent.parent


def get_api_key():
    """Get API key from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        env_file = VAULT_ROOT / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        key = line.split("=", 1)[1].strip()
                        break
    if not key:
        print("Error: No API key found.")
        sys.exit(1)
    return key


def generate_prompt(curriculum: dict) -> str:
    """Generate a creative prompt based on curriculum name and description."""
    name = curriculum.get("name", "")
    description = curriculum.get("description", "")
    philosophy_tags = curriculum.get("philosophyTags", [])

    context_hints = []
    name_lower = name.lower()
    desc_lower = description.lower()

    if "math" in name_lower or "math" in desc_lower or "algebra" in name_lower or "geometry" in name_lower:
        context_hints.append("mathematical elements, numbers, geometric shapes")
    if "latin" in name_lower or "greek" in name_lower:
        context_hints.append("classical antiquity, scrolls, columns, Mediterranean aesthetics")
    if "reading" in name_lower or "phonics" in name_lower or "literacy" in name_lower:
        context_hints.append("open books, letters floating, cozy reading nook")
    if "science" in name_lower or "chemistry" in name_lower or "physics" in name_lower:
        context_hints.append("scientific equipment, nature observation, discovery")
    if "montessori" in name_lower:
        context_hints.append("wooden materials, child-sized furniture, hands-on learning objects")
    if "nature" in name_lower or "outdoor" in name_lower or "NB" in philosophy_tags:
        context_hints.append("outdoor scenes, plants, natural materials, sunlight")
    if "youtube" in name_lower:
        context_hints.append("screen with play button, digital learning, engaging visuals")
    if "podcast" in name_lower or "audio" in name_lower:
        context_hints.append("headphones, sound waves, cozy listening setup")
    if "logic" in name_lower or "argument" in name_lower or "fallacy" in name_lower:
        context_hints.append("puzzle pieces, thinking imagery, classical debate")

    context_str = ", ".join(context_hints) if context_hints else "educational warmth, learning materials"

    prompt = f"""Create a watercolor-line illustration for '{name}' - a homeschool curriculum/resource.

CONCEPT: A playful, warm visual interpretation of the name '{name}'. {f"Context: {context_str}." if context_hints else ""} The image should capture the essence and feeling of this educational resource in an inviting, non-generic way.

STYLE: Ink linework with soft watercolor washes. Hand-crafted, warm feel. Visible brushstrokes.

COLORS: Warm palette with subtle orange and sky blue accents. Cream/off-white background tones.

COMPOSITION: Centered focal point, generous negative space, square format.

TEXTURE: Paper grain visible, analog warmth, slight imperfections that feel human.

AVOID: Text, photorealism, generic educational imagery (no lightbulbs, no happy children raising hands, no graduation caps), cluttered composition, digital/glossy feel."""

    return prompt


def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate a single image using generate_content (same as working skill script)."""
    try:
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspectRatio="1:1",
            ),
        )

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
            config=config,
        )

        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                image.save(output_path)
                return True

        print(f"  No image in response")
        return False

    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Batch generate curriculum images")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--count", type=int, default=None, help="Number to generate (default: all)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if image file exists")
    args = parser.parse_args()

    # Load curricula
    curricula_file = Path(__file__).parent.parent / "src/data/curricula-convex.json"
    with open(curricula_file) as f:
        all_curricula = json.load(f)

    # Filter to those missing images
    missing = [c for c in all_curricula if not c.get("imageUrl")]

    # Check output folder for already generated
    output_dir = Path(__file__).parent.parent / "public/images/curricula"
    output_dir.mkdir(parents=True, exist_ok=True)

    already_done = set()
    for f in output_dir.glob("*.png"):
        slug = f.stem.split("_")[0]  # Handle both slug.png and slug_timestamp.png
        already_done.add(slug)

    print(f"Total missing images in JSON: {len(missing)}")
    print(f"Already generated: {len(already_done)}")

    if args.skip_existing:
        to_generate = [c for c in missing if c["slug"] not in already_done]
    else:
        to_generate = missing

    print(f"To generate: {len(to_generate)}")

    to_generate = to_generate[args.start:]
    if args.count:
        to_generate = to_generate[:args.count]

    if not to_generate:
        print("Nothing to generate!")
        return

    print(f"Will generate {len(to_generate)} images")
    print()

    # Initialize client
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    success = 0
    failed = 0

    for i, curriculum in enumerate(to_generate):
        slug = curriculum["slug"]
        name = curriculum["name"]
        output_path = output_dir / f"{slug}.png"

        print(f"[{i+1}/{len(to_generate)}] {name}")

        if args.skip_existing and output_path.exists():
            print(f"  Skipping (exists)")
            continue

        prompt = generate_prompt(curriculum)

        if generate_image(client, prompt, output_path):
            print(f"  ✓ Saved: {output_path.name}")
            success += 1
        else:
            failed += 1

        # Rate limiting
        if i < len(to_generate) - 1:
            time.sleep(2)

    print()
    print(f"Done! Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    main()
