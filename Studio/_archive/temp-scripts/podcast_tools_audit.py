#!/usr/bin/env python3
"""
Podcast Tools Audit - Extract tool/resource mentions from OpenEd podcast transcripts.

Uses Gemini 3 Flash to process episodes in batches and extract full transcript
sections where tools, curricula, apps, or resources are discussed.

Output: Markdown file with complete context for each mention.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
load_dotenv(Path(__file__).parent.parent / ".env")

MODEL_NAME = "gemini-3-flash-preview"
PODCASTS_DIR = (
    Path(__file__).parent.parent / "Content" / "Master Content Database" / "Podcasts"
)
OUTPUT_DIR = Path(__file__).parent / "Tools Directory"
BATCH_SIZE = 10


EXTRACTION_PROMPT = """You are analyzing podcast transcripts to find mentions of educational tools, resources, curricula, apps, programs, and services.

For each episode provided, identify ANY mention of:
- Curricula or educational programs (e.g., Classical Conversations, Tuttle Twins, Saxon Math)
- Apps or software (e.g., Khan Academy, Duolingo, any learning apps)
- Educational services or platforms (e.g., Praxis, Outschool, co-ops)
- Books or resources mentioned as recommendations
- Methods or approaches with specific names (e.g., Charlotte Mason, Montessori)
- Any product, service, or resource a parent might want to learn more about

For EACH tool/resource found, extract:
1. The tool/resource name
2. The COMPLETE transcript section where it's discussed (include full context - could be multiple paragraphs)
3. Include speaker labels and timestamps if present

Format your response EXACTLY like this for each episode:

---

## [Episode Title]

### [Tool/Resource Name]

**Full Transcript Section:**

> [Paste the ENTIRE relevant section of transcript here, preserving speaker labels]

### [Next Tool/Resource Name]

**Full Transcript Section:**

> [Full section...]

---

If an episode has NO tool mentions, write:

---

## [Episode Title]

*No specific tools, curricula, or resources mentioned in this episode.*

---

IMPORTANT:
- Include the FULL discussion, not just a sentence or two
- If a tool is mentioned multiple times, include ALL sections
- Err on the side of including MORE context rather than less
- Preserve the exact transcript text - do not summarize

Here are the episodes to analyze:

"""


def load_episodes() -> list[dict]:
    episodes = []

    if not PODCASTS_DIR.exists():
        print(f"Error: Podcasts directory not found: {PODCASTS_DIR}")
        sys.exit(1)

    for filepath in sorted(PODCASTS_DIR.glob("*.md")):
        content = filepath.read_text(encoding="utf-8")
        episodes.append({"filename": filepath.name, "content": content})

    print(f"Loaded {len(episodes)} episodes from {PODCASTS_DIR}")
    return episodes


def batch_episodes(episodes: list[dict], batch_size: int) -> list[list[dict]]:
    batches = []
    for i in range(0, len(episodes), batch_size):
        batches.append(episodes[i : i + batch_size])
    return batches


def process_batch(
    client: genai.Client, batch: list[dict], batch_num: int, total_batches: int
) -> str:
    print(f"\n{'=' * 60}")
    print(f"Processing Batch {batch_num}/{total_batches}")
    print(
        f"Episodes: {[ep['filename'][:40] + '...' if len(ep['filename']) > 40 else ep['filename'] for ep in batch]}"
    )
    print(f"{'=' * 60}")

    batch_content = EXTRACTION_PROMPT

    for i, episode in enumerate(batch, 1):
        batch_content += f"\n\n{'=' * 60}\n"
        batch_content += f"EPISODE {i}: {episode['filename']}\n"
        batch_content += f"{'=' * 60}\n\n"
        batch_content += episode["content"]

    char_count = len(batch_content)
    est_tokens = char_count // 4
    print(f"Batch size: ~{est_tokens:,} tokens ({char_count:,} chars)")

    try:
        print("Calling Gemini 3 Flash...")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Content(
                    role="user", parts=[types.Part.from_text(text=batch_content)]
                )
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=65536,
            ),
        )

        if (
            response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
        ):
            result_text = ""
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    result_text += part.text

            print(f"Received {len(result_text):,} chars of output")
            return result_text
        else:
            print("Warning: Empty response from Gemini")
            return f"## Batch {batch_num}\n\n*Error: Empty response from model*\n"

    except Exception as e:
        print(f"Error processing batch: {e}")
        return f"## Batch {batch_num}\n\n*Error: {str(e)}*\n"


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        print("Please set it in .env file or export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print(f"API Key loaded: {api_key[:4]}...{api_key[-4:]}")

    client = genai.Client(api_key=api_key)
    print(f"Gemini client initialized (model: {MODEL_NAME})")

    episodes = load_episodes()

    batches = batch_episodes(episodes, BATCH_SIZE)
    print(f"Split into {len(batches)} batches of ~{BATCH_SIZE} episodes each")

    all_results = []
    all_results.append(f"# OpenEd Podcast Tools Audit\n\n")
    all_results.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
    all_results.append(
        f"*{len(episodes)} episodes analyzed for tool/resource mentions*\n\n"
    )
    all_results.append("---\n\n")

    for i, batch in enumerate(batches, 1):
        result = process_batch(client, batch, i, len(batches))
        all_results.append(result)
        all_results.append("\n\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = (
        OUTPUT_DIR / f"podcast_tools_audit_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_results))

    print(f"\n{'=' * 60}")
    print("AUDIT COMPLETE")
    print(f"{'=' * 60}")
    print(f"Output saved to: {output_file}")
    print(f"Total episodes processed: {len(episodes)}")


if __name__ == "__main__":
    main()
