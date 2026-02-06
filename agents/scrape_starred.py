#!/usr/bin/env python3
"""
Scrape Starred RSS Items → Markdown staging files

Reads tracking.json, finds starred items, scrapes full article content,
saves as clean markdown to staging folder.

Usage:
    python3 agents/scrape_starred.py                  # Scrape all starred items
    python3 agents/scrape_starred.py --date 2026-02-03  # Custom date folder
    python3 agents/scrape_starred.py --clear-queue      # Also bulk-skip non-starred new items
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
import trafilatura
from markdownify import markdownify as md

TRACKING_PATH = Path(__file__).parent.parent / "Projects/RSS-Curation/tracking.json"
STAGING_BASE = Path(__file__).parent.parent / "Projects/RSS-Curation/staging"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def load_tracking():
    with open(TRACKING_PATH, "r") as f:
        return json.load(f)


def save_tracking(data):
    with open(TRACKING_PATH, "w") as f:
        json.dump(data, f, indent=2)


def slugify(text, max_len=60):
    """Convert title to filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len]


def scrape_article(url):
    """Scrape article content. Returns (title, markdown_content) or (None, None)."""
    try:
        # Reddit gets special handling
        if "reddit.com" in url:
            return scrape_reddit(url)

        # trafilatura is best for article extraction
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            # Fallback to requests
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            downloaded = resp.text

        result = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            include_links=True,
            output_format="txt",
        )

        if not result:
            return None, "Could not extract article content (JS-rendered or paywalled)"

        # Get metadata
        metadata = trafilatura.extract(
            downloaded,
            output_format="xml",
            include_comments=False,
        )
        title = None
        if metadata:
            title_match = re.search(r"<title>(.*?)</title>", metadata)
            if title_match:
                title = title_match.group(1)

        return title, result

    except Exception as e:
        return None, f"Scrape error: {str(e)[:200]}"


def scrape_reddit(url):
    """Scrape Reddit thread - get post + top comments."""
    try:
        json_url = url.rstrip("/") + ".json"
        resp = requests.get(
            json_url,
            headers={**HEADERS, "User-Agent": "OpenEd-RSS-Bot/1.0"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        # Post content
        post = data[0]["data"]["children"][0]["data"]
        title = post.get("title", "")
        selftext = post.get("selftext", "(link post)")
        score = post.get("score", 0)
        num_comments = post.get("num_comments", 0)

        lines = [
            selftext,
            "",
            f"*{score} upvotes, {num_comments} comments*",
            "",
            "---",
            "",
            "## Top Comments",
            "",
        ]

        # Top comments
        if len(data) > 1:
            comments = data[1]["data"]["children"]
            for c in comments[:10]:
                if c["kind"] != "t1":
                    continue
                cd = c["data"]
                body = cd.get("body", "")
                cscore = cd.get("score", 0)
                if cscore < 2:
                    continue
                lines.append(f"**({cscore} pts)** {body}")
                lines.append("")

        return title, "\n".join(lines)

    except Exception as e:
        return None, f"Reddit scrape error: {str(e)[:200]}"


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    clear_queue = False

    for arg in sys.argv[1:]:
        if arg.startswith("--date="):
            date_str = arg.split("=")[1]
        if arg == "--clear-queue":
            clear_queue = True

    tracking = load_tracking()
    items = tracking["items"]

    # Find starred items
    starred = {url: item for url, item in items.items() if item.get("starred")}

    if not starred:
        print("No starred items to scrape.")
        return

    # Create staging folder
    staging_dir = STAGING_BASE / f"day-{date_str}"
    staging_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scraping {len(starred)} starred items → {staging_dir}")
    print("=" * 60)

    results = []

    for url, item in starred.items():
        title = item.get("title", "Untitled")
        source = item.get("source", "Unknown")
        slug = slugify(f"{source}-{title}")

        print(f"\n  → {title[:60]}... ({source})")

        scraped_title, content = scrape_article(url)

        if not content:
            print(f"    ✗ Failed to scrape")
            content = "(Could not scrape - visit manually)"

        # Build markdown file
        file_content = f"""---
title: "{title}"
source: "{source}"
url: "{url}"
scraped: "{datetime.now().isoformat()}"
score: "{item.get('score', 'unknown')}"
---

# {scraped_title or title}

**Source:** {source}
**URL:** {url}

---

{content}
"""

        filepath = staging_dir / f"{slug}.md"
        filepath.write_text(file_content)
        results.append({"title": title, "source": source, "url": url, "file": str(filepath.name)})
        print(f"    ✓ Saved → {filepath.name}")

        # Mark as published in tracking
        items[url]["status"] = "published"

        time.sleep(0.5)  # Rate limit

    # Write manifest
    manifest = {
        "date": date_str,
        "scraped_at": datetime.now().isoformat(),
        "count": len(results),
        "items": results,
    }
    manifest_path = staging_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Clear queue - bulk skip all non-starred new items
    if clear_queue:
        skipped = 0
        for url, item in items.items():
            if item.get("status") == "new" and not item.get("starred"):
                item["status"] = "rejected"
                skipped += 1
        print(f"\n  Bulk-skipped {skipped} non-starred items")

    # Unstar processed items (they're now in staging)
    for url in starred:
        items[url]["starred"] = False

    save_tracking(tracking)

    print(f"\n{'=' * 60}")
    print(f"Done. {len(results)} articles scraped to {staging_dir}")
    print(f"Manifest: {manifest_path}")
    if clear_queue:
        print("Queue cleared - non-starred items skipped.")
    print(f"\nNext: Read manifest.json and draft OpenEd angles")


if __name__ == "__main__":
    main()
