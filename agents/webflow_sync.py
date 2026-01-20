#!/usr/bin/env python3
"""
Webflow Content Sync - Consolidated sync agent for OpenEd Vault
Syncs posts from Webflow CMS to Master Content Database

Usage:
    python3 webflow_sync.py              # Sync new posts since last sync
    python3 webflow_sync.py --status     # Show sync status
    python3 webflow_sync.py --dry-run    # Preview without syncing
    python3 webflow_sync.py --full       # Full re-sync (use sparingly)

State tracking:
    Uses .webflow_sync_state.json to track last sync timestamp
    Only fetches posts updated after last sync (token-conserving)

Configuration:
    API key stored in /OpenEd Vault/.env as WEBFLOW_API_KEY
    Get new key: Webflow Dashboard → Workspace Settings → Integrations → API Access
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests
from dotenv import load_dotenv

# ============================================
# Configuration
# ============================================

AGENTS_DIR = Path(__file__).parent
VAULT_ROOT = AGENTS_DIR.parent
STATE_FILE = AGENTS_DIR / ".webflow_sync_state.json"
CONTENT_DB = VAULT_ROOT / "Content" / "Master Content Database"
ENV_PATH = VAULT_ROOT / ".env"

# Load environment
load_dotenv(ENV_PATH)
WEBFLOW_API_KEY = os.getenv("WEBFLOW_API_KEY")

# Webflow config
API_BASE = "https://api.webflow.com/v2"
COLLECTION_ID = "6805bf729a7b33423cc8a08c"

# Post type mapping
POST_TYPE_MAP = {
    "6812753c2611e43906dc13d6": "Announcements",
    "6805d5076ff8c966566279a4": "Daily Newsletters",
    "6805d44048df4bd97a0754ed": "Blog Posts",
    "6805d42ba524fabb70579f4e": "Podcasts",
}

# URL patterns by type
URL_PATTERNS = {
    "Podcasts": "https://opened.co/podcast/{slug}",
    "Daily Newsletters": "https://opened.co/newsletter/{slug}",
    "Blog Posts": "https://opened.co/blog/{slug}",
    "Announcements": "https://opened.co/blog/{slug}",
    "Other": "https://opened.co/blog/{slug}",
}


# ============================================
# HTML to Markdown Conversion
# ============================================


def html_to_markdown(html_content):
    """Convert HTML content to clean markdown."""
    if not html_content:
        return ""

    text = html_content

    # Remove style, script, and embedded content
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(
        r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r'<div data-rt-embed-type=[\'"]true[\'"]>.*?</div>\s*(?=<[^d]|$)',
        "",
        text,
        flags=re.DOTALL,
    )

    # Headers
    text = re.sub(
        r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n", text, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n", text, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", text, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r"<h4[^>]*>(.*?)</h4>", r"\n#### \1\n", text, flags=re.DOTALL | re.IGNORECASE
    )

    # Links, bold, italic
    text = re.sub(
        r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>',
        r"[\2](\1)",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    text = re.sub(
        r"<(strong|b)[^>]*>(.*?)</\1>", r"**\2**", text, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r"<(em|i)[^>]*>(.*?)</\1>", r"*\2*", text, flags=re.DOTALL | re.IGNORECASE
    )

    # Unordered lists
    text = re.sub(
        r"<ul[^>]*>(.*?)</ul>",
        lambda m: "\n"
        + re.sub(
            r"<li[^>]*>(.*?)</li>",
            r"- \1\n",
            m.group(1),
            flags=re.DOTALL | re.IGNORECASE,
        )
        + "\n",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Ordered lists
    def convert_ol(match):
        items = re.findall(
            r"<li[^>]*>(.*?)</li>", match.group(1), flags=re.DOTALL | re.IGNORECASE
        )
        return (
            "\n"
            + "\n".join(f"{i + 1}. {item.strip()}" for i, item in enumerate(items))
            + "\n"
        )

    text = re.sub(
        r"<ol[^>]*>(.*?)</ol>", convert_ol, text, flags=re.DOTALL | re.IGNORECASE
    )

    # Paragraphs and breaks
    text = re.sub(
        r"<p[^>]*>(.*?)</p>", r"\n\1\n", text, flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    # Blockquotes
    text = re.sub(
        r"<blockquote[^>]*>(.*?)</blockquote>",
        lambda m: "\n> " + m.group(1).strip().replace("\n", "\n> ") + "\n",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Clean remaining HTML and entities
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)

    # Normalize whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))

    return text.strip()


# ============================================
# State Management
# ============================================


def load_state():
    """Load sync state from JSON file."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return None


def save_state(state):
    """Save sync state to JSON file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_existing_webflow_ids():
    """Get set of webflow_ids already in database."""
    existing = set()

    if not CONTENT_DB.exists():
        return existing

    for folder in CONTENT_DB.iterdir():
        if folder.is_dir():
            for file in folder.glob("*.md"):
                try:
                    content = file.read_text(encoding="utf-8")
                    match = re.search(r"webflow_id:\s*(\w+)", content)
                    if match:
                        existing.add(match.group(1))
                except:
                    pass

    return existing


# ============================================
# Webflow API
# ============================================


def get_headers():
    """Get API headers."""
    return {"Authorization": f"Bearer {WEBFLOW_API_KEY}", "accept": "application/json"}


def fetch_posts_since(last_sync_timestamp):
    """Fetch posts updated since last sync timestamp."""
    all_posts = []
    offset = 0
    limit = 100

    last_sync_dt = datetime.fromisoformat(last_sync_timestamp.replace("Z", "+00:00"))

    print(f"Fetching posts updated after {last_sync_timestamp}...")

    while True:
        url = f"{API_BASE}/collections/{COLLECTION_ID}/items"
        params = {"limit": limit, "offset": offset}

        response = requests.get(url, headers=get_headers(), params=params)

        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        items = data.get("items", [])

        if not items:
            break

        for item in items:
            last_updated = item.get("lastUpdated")
            if last_updated:
                item_dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
                if item_dt > last_sync_dt:
                    if not item.get("isDraft", False):
                        all_posts.append(item)

        if len(items) < limit:
            break

        offset += limit
        print(f"  Checked {offset} posts...")

    return all_posts


def fetch_all_posts():
    """Fetch all published posts (for full sync)."""
    all_posts = []
    offset = 0
    limit = 100

    print("Fetching all posts...")

    while True:
        url = f"{API_BASE}/collections/{COLLECTION_ID}/items"
        params = {"limit": limit, "offset": offset}

        response = requests.get(url, headers=get_headers(), params=params)

        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        items = data.get("items", [])

        if not items:
            break

        for item in items:
            if not item.get("isDraft", False):
                all_posts.append(item)

        if len(items) < limit:
            break

        offset += limit
        print(f"  Fetched {offset} posts...")

    return all_posts


# ============================================
# Markdown File Creation
# ============================================


def resolve_post_type(post_type_ids):
    """Convert post-type reference IDs to folder name."""
    if not post_type_ids:
        return "Other"
    type_id = post_type_ids[0] if isinstance(post_type_ids, list) else post_type_ids
    return POST_TYPE_MAP.get(type_id, "Other")


def create_markdown_file(post):
    """Create markdown file for a post with complete metadata."""
    field_data = post.get("fieldData", {})

    # Core fields
    title = field_data.get("name", "Untitled")
    slug = field_data.get("slug", "")
    post_type_ids = field_data.get("post-type", [])
    post_type = resolve_post_type(post_type_ids)

    # Metadata fields
    meta_description = field_data.get("meta-description", "") or ""
    summary = field_data.get("summary", "") or ""
    html_content = field_data.get("content", "") or ""

    # IDs and timestamps
    webflow_id = post.get("id", "")
    author_id = field_data.get("author", "")
    created_on = post.get("createdOn", "")
    last_updated = post.get("lastUpdated", "")
    last_published = post.get("lastPublished", "")

    # Thumbnail
    thumbnail = field_data.get("thumbnail", {})
    thumbnail_url = thumbnail.get("url", "") if isinstance(thumbnail, dict) else ""

    # Published date
    published_date = (
        field_data.get("published-date", "")
        or field_data.get("published-on", "")
        or created_on
    )
    if published_date:
        try:
            dt = datetime.fromisoformat(published_date.replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d")
        except:
            date_str = published_date[:10] if len(published_date) >= 10 else ""
    else:
        date_str = ""

    # Build URL
    url_pattern = URL_PATTERNS.get(post_type, URL_PATTERNS["Other"])
    url = url_pattern.format(slug=slug)

    # Escape quotes for YAML
    def escape_yaml(s):
        return s.replace('"', "'").replace("\n", " ").strip() if s else ""

    sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    markdown_content = html_to_markdown(html_content)

    # Build frontmatter with all metadata
    frontmatter = f'''---
title: "{escape_yaml(title)}"
slug: {slug}
url: {url}
type: {post_type.lower().replace(" ", "_")}
date: {date_str}
webflow_id: {webflow_id}
author_id: {author_id}
thumbnail: {thumbnail_url}
meta_description: "{escape_yaml(meta_description)}"
summary: "{escape_yaml(summary)}"
created_on: {created_on}
last_updated: {last_updated}
last_published: {last_published}
last_synced: {sync_time}
---'''

    # Build content section
    content_parts = [frontmatter, "", f"# {title}", ""]

    # Metadata block
    content_parts.append(f"**URL:** [{url}]({url})")
    content_parts.append(f"**Type:** {post_type}")
    content_parts.append(f"**Published:** {date_str}")
    if thumbnail_url:
        content_parts.append(f"**Thumbnail:** ![]({thumbnail_url})")
    content_parts.append("")

    # Summary
    if summary:
        content_parts.append("## Summary")
        content_parts.append(summary)
        content_parts.append("")

    # Main content
    if markdown_content:
        content_parts.append("## Content")
        content_parts.append("")
        content_parts.append(markdown_content)
    else:
        content_parts.append("_No content available_")

    file_content = "\n".join(content_parts)

    # Create file
    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()[:60]
    filename = f"{safe_title}.md"

    type_dir = CONTENT_DB / post_type
    type_dir.mkdir(parents=True, exist_ok=True)
    filepath = type_dir / filename

    filepath.write_text(file_content, encoding="utf-8")

    return {
        "title": title,
        "url": url,
        "type": post_type,
        "file": str(filepath),
        "webflow_id": webflow_id,
        "has_content": bool(markdown_content),
    }


# ============================================
# Sync Operations
# ============================================


def sync_posts(posts, existing_ids):
    """Sync a list of posts, skipping existing ones."""
    synced = []
    skipped = 0

    for post in posts:
        webflow_id = post.get("id", "")
        title = post.get("fieldData", {}).get("name", "Untitled")

        if webflow_id in existing_ids:
            skipped += 1
            continue

        try:
            result = create_markdown_file(post)
            synced.append(result)
            existing_ids.add(webflow_id)  # Prevent duplicates in same run
            print(f"  ✓ {result['title']} ({result['type']})")
        except Exception as e:
            print(f"  ✗ Error: {title} - {e}")

    if skipped:
        print(f"  (Skipped {skipped} existing posts)")

    return synced


def update_state_after_sync(state, synced_count):
    """Update state file after successful sync."""
    now = datetime.now(timezone.utc)

    state["last_sync"] = {
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "posts_synced": state["last_sync"]["posts_synced"] + synced_count,
        "note": f"Synced {synced_count} posts",
    }

    state["sync_history"].append(
        {
            "date": now.strftime("%Y-%m-%d %H:%M"),
            "posts_added": synced_count,
            "method": "incremental",
        }
    )

    # Keep only last 20 history entries
    state["sync_history"] = state["sync_history"][-20:]

    save_state(state)


# ============================================
# Commands
# ============================================


def cmd_status():
    """Show sync status."""
    print("=" * 50)
    print("WEBFLOW SYNC STATUS")
    print("=" * 50)

    state = load_state()
    if not state:
        print("No sync state found. Run sync first.")
        return

    last_sync = state.get("last_sync", {})
    print(f"Last sync: {last_sync.get('timestamp', 'Unknown')}")
    print(f"Total posts synced: {last_sync.get('posts_synced', 0)}")

    print("\nRecent sync history:")
    for entry in state.get("sync_history", [])[-5:]:
        print(
            f"  {entry['date']}: +{entry['posts_added']} ({entry.get('method', 'sync')})"
        )

    print("\nChecking for new posts...")
    new_posts = fetch_posts_since(last_sync.get("timestamp", "2020-01-01T00:00:00Z"))

    existing_ids = get_existing_webflow_ids()
    truly_new = [p for p in new_posts if p.get("id") not in existing_ids]

    print(f"New posts available: {len(truly_new)}")

    if truly_new:
        print("\nPosts to sync:")
        for post in truly_new[:10]:
            name = post.get("fieldData", {}).get("name", "Untitled")
            updated = post.get("lastUpdated", "")[:10]
            print(f"  - {name} ({updated})")
        if len(truly_new) > 10:
            print(f"  ... and {len(truly_new) - 10} more")


def cmd_sync(dry_run=False):
    """Run incremental sync."""
    if not WEBFLOW_API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found in .env")
        print(f"Add it to: {ENV_PATH}")
        return

    state = load_state()
    if not state:
        print("ERROR: No sync state found.")
        print(f"Create {STATE_FILE} first or run --full for initial sync.")
        return

    print("=" * 50)
    print("WEBFLOW INCREMENTAL SYNC")
    print("=" * 50)

    last_sync = state["last_sync"]["timestamp"]
    print(f"Last sync: {last_sync}\n")

    # Fetch and filter
    new_posts = fetch_posts_since(last_sync)
    existing_ids = get_existing_webflow_ids()
    truly_new = [p for p in new_posts if p.get("id") not in existing_ids]

    if not truly_new:
        print("No new posts to sync.")
        return

    print(f"\nFound {len(truly_new)} new posts:")
    for post in truly_new:
        print(f"  - {post.get('fieldData', {}).get('name', 'Untitled')}")

    if dry_run:
        print("\n[DRY RUN] Run without --dry-run to sync.")
        return

    print("\nSyncing...")
    synced = sync_posts(truly_new, existing_ids)

    if synced:
        update_state_after_sync(state, len(synced))
        print(f"\n✓ Synced {len(synced)} posts")
        print(f"State saved to {STATE_FILE}")


def cmd_full_sync(dry_run=False):
    """Full sync - fetches all posts."""
    if not WEBFLOW_API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found")
        return

    print("=" * 50)
    print("WEBFLOW FULL SYNC")
    print("=" * 50)
    print("This will sync ALL posts from Webflow.\n")

    all_posts = fetch_all_posts()
    existing_ids = get_existing_webflow_ids()

    new_posts = [p for p in all_posts if p.get("id") not in existing_ids]

    print(f"Total posts in Webflow: {len(all_posts)}")
    print(f"Already synced: {len(existing_ids)}")
    print(f"New to sync: {len(new_posts)}")

    if not new_posts:
        print("\nAll posts already synced.")
        return

    if dry_run:
        print("\n[DRY RUN] Would sync these posts:")
        for post in new_posts[:20]:
            print(f"  - {post.get('fieldData', {}).get('name', 'Untitled')}")
        if len(new_posts) > 20:
            print(f"  ... and {len(new_posts) - 20} more")
        return

    print("\nSyncing...")
    synced = sync_posts(new_posts, existing_ids)

    # Update or create state
    state = load_state() or {
        "webflow_config": {
            "site": "opened.co",
            "collection_id": COLLECTION_ID,
            "post_types": POST_TYPE_MAP,
        },
        "last_sync": {"posts_synced": 0},
        "sync_history": [],
        "sync_history": [],
    }

    update_state_after_sync(state, len(synced))
    print(f"\n✓ Synced {len(synced)} posts")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
    elif "--status" in args:
        cmd_status()
    elif "--full" in args:
        cmd_full_sync(dry_run="--dry-run" in args)
    elif "--dry-run" in args:
        cmd_sync(dry_run=True)
    else:
        cmd_sync()


if __name__ == "__main__":
    main()
