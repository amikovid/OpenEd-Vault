#!/usr/bin/env python3
"""
Webflow Incremental Sync - Token-conserving sync that only fetches new posts
Uses .webflow_sync_state.json to track last sync timestamp

Usage:
    python3 webflow_incremental_sync.py           # Sync new posts
    python3 webflow_incremental_sync.py --status  # Show sync status
    python3 webflow_incremental_sync.py --dry-run # Preview without syncing
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Import sync functions from main agent
from webflow_sync_agent import get_existing_posts, sync_new_webflow_posts

# Paths
AGENTS_DIR = Path(__file__).parent
STATE_FILE = AGENTS_DIR / ".webflow_sync_state.json"
VAULT_ROOT = AGENTS_DIR.parent

# Config
WEBFLOW_API_KEY = os.getenv("WEBFLOW_API_KEY")
COLLECTION_ID = "6805bf729a7b33423cc8a08c"
API_BASE = "https://api.webflow.com/v2"


def load_state():
    """Load sync state from JSON file."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return None


def save_state(state):
    """Save sync state to JSON file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_headers():
    """Get API headers."""
    return {"Authorization": f"Bearer {WEBFLOW_API_KEY}", "accept": "application/json"}


def fetch_posts_since(last_sync_timestamp):
    """
    Fetch posts updated since last sync.
    Uses pagination to get all posts, filters by lastUpdated.
    """
    all_posts = []
    offset = 0
    limit = 100  # Max allowed by Webflow API

    # Parse the last sync timestamp
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

        # Filter for posts updated after last sync
        for item in items:
            last_updated = item.get("lastUpdated")
            if last_updated:
                item_dt = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
                if item_dt > last_sync_dt:
                    # Only include published posts
                    if not item.get("isDraft", False):
                        all_posts.append(item)

        # Check if we've reached the end
        if len(items) < limit:
            break

        offset += limit
        print(f"  Checked {offset} posts...")

    return all_posts


def show_status():
    """Display current sync status."""
    state = load_state()

    print("=" * 50)
    print("WEBFLOW SYNC STATUS")
    print("=" * 50)

    if not state:
        print("No sync state found. Run a sync first.")
        return

    last_sync = state.get("last_sync", {})
    print(f"Last sync: {last_sync.get('timestamp', 'Unknown')}")
    print(f"Posts in database: {last_sync.get('posts_synced', 'Unknown')}")

    if last_sync.get("note"):
        print(f"Note: {last_sync['note']}")

    print("\nSync History:")
    for entry in state.get("sync_history", [])[-5:]:  # Last 5 syncs
        print(f"  {entry['date']}: +{entry['posts_added']} posts ({entry['method']})")

    # Check for new posts
    print("\nChecking for new posts...")
    new_posts = fetch_posts_since(last_sync.get("timestamp", "2020-01-01T00:00:00Z"))
    print(f"New/updated posts available: {len(new_posts)}")

    if new_posts:
        print("\nNew posts:")
        for post in new_posts[:10]:  # Show first 10
            name = post.get("fieldData", {}).get("name", "Untitled")
            updated = post.get("lastUpdated", "")[:10]
            print(f"  - {name} (updated: {updated})")
        if len(new_posts) > 10:
            print(f"  ... and {len(new_posts) - 10} more")


def run_sync(dry_run=False):
    """Run incremental sync."""
    if not WEBFLOW_API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found in .env")
        print("Add it to: " + str(env_path))
        return

    state = load_state()
    if not state:
        print("ERROR: No sync state found. Cannot determine last sync time.")
        print("If this is a fresh setup, create .webflow_sync_state.json first.")
        return

    last_sync = state["last_sync"]["timestamp"]

    print("=" * 50)
    print("WEBFLOW INCREMENTAL SYNC")
    print("=" * 50)
    print(f"Last sync: {last_sync}")
    print()

    # Fetch new posts
    new_posts = fetch_posts_since(last_sync)

    if not new_posts:
        print("No new posts to sync.")
        return

    print(f"\nFound {len(new_posts)} new/updated posts:")
    for post in new_posts:
        name = post.get("fieldData", {}).get("name", "Untitled")
        print(f"  - {name}")

    if dry_run:
        print("\n[DRY RUN] Would sync these posts. Run without --dry-run to execute.")
        return

    print("\nSyncing...")

    # Use existing sync function
    synced = sync_new_webflow_posts(new_posts)

    # Update state
    now = datetime.now(timezone.utc)
    state["last_sync"] = {
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "posts_synced": state["last_sync"]["posts_synced"] + len(synced),
        "note": f"Incremental sync added {len(synced)} posts",
    }
    state["sync_history"].append(
        {
            "date": now.strftime("%Y-%m-%d"),
            "posts_added": len(synced),
            "method": "incremental_sync",
        }
    )

    save_state(state)

    print(f"\nSync complete! Added {len(synced)} posts.")
    print(f"State saved to {STATE_FILE}")


def main():
    args = sys.argv[1:]

    if "--status" in args:
        show_status()
    elif "--dry-run" in args:
        run_sync(dry_run=True)
    elif "--help" in args or "-h" in args:
        print(__doc__)
    else:
        run_sync()


if __name__ == "__main__":
    main()
