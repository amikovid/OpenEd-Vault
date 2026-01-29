#!/usr/bin/env python3
"""
Social Post Scheduler

Polls Notion Social Post Queue for approved posts, schedules via Getlate,
and updates Notion status.

Run manually: python3 agents/social_post_scheduler.py
Run via cron: Add to crontab for periodic execution

Workflow:
1. Query Notion for Status = "Approved"
2. Read page body to get post text
3. Schedule via Getlate API
4. Update Notion: Status = "Scheduled", add Getlate ID
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(Path(__file__).parent.parent / ".env")

# API Keys
NOTION_KEY = os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN") or os.getenv("NOTION_KEY")
GETLATE_KEY = os.getenv("GETLATE_API_KEY")

# IDs
NOTION_DATABASE_ID = "2f7afe52-ef59-8111-8044-e797e95a6a7d"
GETLATE_TWITTER_ID = "696135064207e06f4ca849a1"
GETLATE_LINKEDIN_ID = "696135294207e06f4ca849a2"

# Headers
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

GETLATE_HEADERS = {
    "Authorization": f"Bearer {GETLATE_KEY}",
    "Content-Type": "application/json"
}


def get_approved_posts():
    """Query Notion for posts with Status = Approved"""
    response = requests.post(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
        headers=NOTION_HEADERS,
        json={
            "filter": {
                "property": "Status",
                "select": {"equals": "Approved"}
            }
        }
    )

    if response.status_code != 200:
        print(f"Error querying Notion: {response.status_code}")
        return []

    return response.json().get("results", [])


def get_page_content(page_id):
    """Get the text content from page body (blocks)"""
    response = requests.get(
        f"https://api.notion.com/v1/blocks/{page_id}/children",
        headers=NOTION_HEADERS
    )

    if response.status_code != 200:
        return ""

    blocks = response.json().get("results", [])
    text_parts = []

    for block in blocks:
        block_type = block.get("type")
        if block_type == "paragraph":
            rich_text = block.get("paragraph", {}).get("rich_text", [])
            for rt in rich_text:
                text_parts.append(rt.get("plain_text", ""))
        elif block_type == "bulleted_list_item":
            rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
            for rt in rich_text:
                text_parts.append("• " + rt.get("plain_text", ""))

    return "\n\n".join(text_parts)


def get_platform_account_id(platform):
    """Map platform name to Getlate account ID"""
    platform_map = {
        "X": GETLATE_TWITTER_ID,
        "LinkedIn": GETLATE_LINKEDIN_ID,
        # Add more as needed
    }
    return platform_map.get(platform)


def schedule_post(content, platform, scheduled_time=None):
    """Schedule post via Getlate API"""
    account_id = get_platform_account_id(platform)
    if not account_id:
        print(f"  No account configured for platform: {platform}")
        return None

    # Default to 1 hour from now if no time specified
    if not scheduled_time:
        scheduled_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    post_data = {
        "platforms": [{"platform": platform.lower(), "accountId": account_id}],
        "content": content,
        "scheduledFor": scheduled_time
    }

    response = requests.post(
        "https://getlate.dev/api/v1/posts",
        headers=GETLATE_HEADERS,
        json=post_data
    )

    if response.status_code in [200, 201]:
        result = response.json()
        return result.get("post", {}).get("_id")
    else:
        print(f"  Getlate error: {response.status_code} - {response.text[:100]}")
        return None


def update_notion_status(page_id, status, getlate_id=None):
    """Update Notion page status and optionally add Getlate ID"""
    properties = {
        "Status": {"select": {"name": status}}
    }

    if getlate_id:
        properties["Getlate ID"] = {
            "rich_text": [{"text": {"content": getlate_id}}]
        }

    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=NOTION_HEADERS,
        json={"properties": properties}
    )

    return response.status_code == 200


def main():
    print(f"Social Post Scheduler - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # Check for required keys
    if not NOTION_KEY:
        print("ERROR: No Notion API key found")
        sys.exit(1)
    if not GETLATE_KEY:
        print("ERROR: No Getlate API key found")
        sys.exit(1)

    # Get approved posts
    approved = get_approved_posts()
    print(f"\nFound {len(approved)} approved posts\n")

    if not approved:
        print("Nothing to schedule.")
        return

    for post in approved:
        page_id = post["id"]
        properties = post.get("properties", {})

        # Get source title
        title_prop = properties.get("Source", {}).get("title", [])
        title = title_prop[0].get("plain_text", "Untitled") if title_prop else "Untitled"

        # Get platform
        platform = properties.get("Platform", {}).get("select", {}).get("name", "X")

        # Get scheduled time
        scheduled_time = properties.get("Scheduled Time", {}).get("date", {}).get("start")

        # Get post content from page body
        content = get_page_content(page_id)

        if not content:
            print(f"⚠ {title[:40]}... - No content in page body, skipping")
            continue

        print(f"→ {title[:40]}...")
        print(f"  Platform: {platform}")
        print(f"  Content: {content[:60]}...")

        # Schedule via Getlate
        getlate_id = schedule_post(content, platform, scheduled_time)

        if getlate_id:
            # Update Notion
            if update_notion_status(page_id, "Scheduled", getlate_id):
                print(f"  ✓ Scheduled! Getlate ID: {getlate_id}")
            else:
                print(f"  ⚠ Scheduled but failed to update Notion")
        else:
            print(f"  ✗ Failed to schedule")

    print("\nDone.")


if __name__ == "__main__":
    main()
