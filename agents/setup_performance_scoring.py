#!/usr/bin/env python3
"""
Content Performance Scoring - One-Time Setup

Run this ONCE to configure everything:
1. Adds performance tracking properties to Notion Master Content Database
2. Validates .env API keys (tells you what's working, what's missing)
3. Runs initial scoring pass
4. Generates first insights digest
5. Offers to set up daily cron job

Usage:
    python agents/setup_performance_scoring.py

Charlie: just run this and follow the prompts. ~5 minutes.
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

# Load environment
ENV_PATH = Path(__file__).parent.parent / ".env"
ENV_EXAMPLE_PATH = Path(__file__).parent.parent / ".env.example"
load_dotenv(ENV_PATH)

# Notion config
NOTION_DATABASE_ID = "9a2f5189-6c53-4a9d-b961-3ccbcb702612"

# ============================================================
# STEP 1: Check / Create .env
# ============================================================

def check_env():
    """Check which API keys are configured and working."""
    print("\n" + "=" * 60)
    print("STEP 1: Checking API Keys")
    print("=" * 60)

    if not ENV_PATH.exists():
        print(f"\n.env file not found at {ENV_PATH}")
        if ENV_EXAMPLE_PATH.exists():
            print(f"Found .env.example - copying as starting point...")
            import shutil
            shutil.copy(ENV_EXAMPLE_PATH, ENV_PATH)
            print(f"Created {ENV_PATH}")
            print("Please fill in your API keys, then re-run this script.")
            print(f"\nOpen: {ENV_PATH}")
            return False
        else:
            print("No .env or .env.example found.")
            print("Create a .env file in the vault root with your API keys.")
            return False

    # Reload after potential copy
    load_dotenv(ENV_PATH, override=True)

    keys = {
        "NOTION_API_KEY": {
            "env_vars": ["NOTION_API_KEY", "NOTION_TOKEN", "NOTION_KEY"],
            "required": True,
            "purpose": "Write scores back to Notion (REQUIRED)",
        },
        "GA4": {
            "env_vars": ["GA4_PROPERTY_ID"],
            "required": False,
            "purpose": "Blog/SEO traffic and engagement data",
        },
        "GA4_CREDENTIALS": {
            "env_vars": ["GA4_CREDENTIALS_PATH"],
            "required": False,
            "purpose": "GA4 service account authentication",
        },
        "META_ACCESS_TOKEN": {
            "env_vars": ["META_ACCESS_TOKEN"],
            "required": False,
            "purpose": "Facebook + Instagram post analytics",
        },
        "YOUTUBE_API_KEY": {
            "env_vars": ["YOUTUBE_API_KEY"],
            "required": False,
            "purpose": "YouTube video/channel analytics",
        },
        "HUBSPOT_API_KEY": {
            "env_vars": ["HUBSPOT_API_KEY"],
            "required": False,
            "purpose": "Email campaigns, conversions, CRM data",
        },
    }

    all_good = True
    available_sources = []

    for name, config in keys.items():
        found = False
        for env_var in config["env_vars"]:
            val = os.getenv(env_var)
            if val and val.strip() and not val.startswith("your_"):
                found = True
                break

        status = "OK" if found else "MISSING"
        marker = "[ok]" if found else "[--]"
        req = " (REQUIRED)" if config["required"] else ""

        print(f"  {marker} {name}{req}")
        print(f"       {config['purpose']}")

        if found:
            available_sources.append(name)
        elif config["required"]:
            all_good = False

    print(f"\n  {len(available_sources)}/{len(keys)} data sources configured")

    if not all_good:
        print("\n  NOTION_API_KEY is required. Add it to .env and re-run.")
        print(f"  File: {ENV_PATH}")
        return False

    if len(available_sources) == 1:
        print("\n  Only Notion is configured. Scores will default to 50 (median).")
        print("  Add more API keys to .env for real scoring.")
        resp = input("\n  Continue anyway? (y/n): ").strip().lower()
        if resp != "y":
            return False

    return True


# ============================================================
# STEP 2: Add Notion Properties
# ============================================================

PROPERTIES_TO_ADD = [
    {
        "name": "Performance Score",
        "type": "number",
        "config": {"number": {"format": "number"}},
    },
    {
        "name": "Score Label",
        "type": "select",
        "config": {
            "select": {
                "options": [
                    {"name": "Top Performer", "color": "green"},
                    {"name": "Strong", "color": "blue"},
                    {"name": "Average", "color": "yellow"},
                    {"name": "Underperforming", "color": "orange"},
                    {"name": "Poor", "color": "red"},
                ]
            }
        },
    },
    {
        "name": "Impressions",
        "type": "number",
        "config": {"number": {"format": "number"}},
    },
    {
        "name": "Engagements",
        "type": "number",
        "config": {"number": {"format": "number"}},
    },
    {
        "name": "Engagement Rate",
        "type": "number",
        "config": {"number": {"format": "percent"}},
    },
    {
        "name": "Clicks",
        "type": "number",
        "config": {"number": {"format": "number"}},
    },
    {
        "name": "Conversions",
        "type": "number",
        "config": {"number": {"format": "number"}},
    },
    {
        "name": "Trend",
        "type": "select",
        "config": {
            "select": {
                "options": [
                    {"name": "Rising", "color": "green"},
                    {"name": "Stable", "color": "default"},
                    {"name": "Declining", "color": "red"},
                ]
            }
        },
    },
    {
        "name": "Last Scored",
        "type": "date",
        "config": {"date": {}},
    },
    {
        "name": "Content Theme",
        "type": "multi_select",
        "config": {
            "multi_select": {
                "options": [
                    {"name": "Curriculum Reviews", "color": "blue"},
                    {"name": "School Choice", "color": "green"},
                    {"name": "Homeschool How-To", "color": "yellow"},
                    {"name": "Education Philosophy", "color": "purple"},
                    {"name": "Education News", "color": "orange"},
                    {"name": "Family Stories", "color": "pink"},
                    {"name": "ESA / Funding", "color": "red"},
                    {"name": "Alternative Pathways", "color": "default"},
                ]
            }
        },
    },
    {
        "name": "Score Notes",
        "type": "rich_text",
        "config": {"rich_text": {}},
    },
    {
        "name": "Platform Post IDs",
        "type": "rich_text",
        "config": {"rich_text": {}},
    },
]


def setup_notion_properties():
    """Add performance tracking properties to the Master Content Database."""
    print("\n" + "=" * 60)
    print("STEP 2: Setting Up Notion Properties")
    print("=" * 60)

    notion_key = os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN") or os.getenv("NOTION_KEY")
    if not notion_key:
        print("  No Notion API key found. Skipping.")
        return False

    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # First, check what properties already exist
    print("\n  Checking existing database properties...")
    response = requests.get(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
        headers=headers,
    )

    if response.status_code != 200:
        print(f"  Error accessing database: {response.status_code}")
        print(f"  {response.text[:200]}")
        print("\n  Make sure the Notion integration has access to the Master Content Database.")
        print("  In Notion: Settings > Connections > find your integration > grant access to the database")
        return False

    db = response.json()
    existing_props = set(db.get("properties", {}).keys())
    print(f"  Found {len(existing_props)} existing properties")

    # Determine which properties need to be added
    to_add = []
    already_exist = []
    for prop in PROPERTIES_TO_ADD:
        if prop["name"] in existing_props:
            already_exist.append(prop["name"])
        else:
            to_add.append(prop)

    if already_exist:
        print(f"\n  Already exist (skipping): {', '.join(already_exist)}")

    if not to_add:
        print("\n  All performance properties already exist!")
        return True

    print(f"\n  Will add {len(to_add)} new properties:")
    for prop in to_add:
        print(f"    + {prop['name']} ({prop['type']})")

    resp = input("\n  Add these properties to the Master Content Database? (y/n): ").strip().lower()
    if resp != "y":
        print("  Skipped. You can add them manually in Notion if you prefer.")
        return False

    # Add properties via Notion API
    # Notion's update database endpoint adds properties
    update_payload = {"properties": {}}
    for prop in to_add:
        update_payload["properties"][prop["name"]] = {prop["type"]: prop["config"].get(prop["type"], {})}

    response = requests.patch(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
        headers=headers,
        json=update_payload,
    )

    if response.status_code == 200:
        print(f"\n  Added {len(to_add)} properties successfully!")
        return True
    else:
        print(f"\n  Error adding properties: {response.status_code}")
        error_body = response.json()
        print(f"  {error_body.get('message', response.text[:200])}")
        print("\n  You may need to add these properties manually in Notion.")
        return False


# ============================================================
# STEP 3: Initial Scoring Run
# ============================================================

def run_initial_scoring():
    """Run the content performance agent for the first time."""
    print("\n" + "=" * 60)
    print("STEP 3: Running Initial Scoring")
    print("=" * 60)

    resp = input("\n  Run initial scoring now? This scores all Posted content. (y/n): ").strip().lower()
    if resp != "y":
        print("  Skipped. Run manually later:")
        print("  python agents/content_performance_agent.py")
        return

    print("\n  Launching content_performance_agent.py...\n")

    import subprocess
    agent_path = Path(__file__).parent / "content_performance_agent.py"
    result = subprocess.run(
        [sys.executable, str(agent_path), "--all"],
        cwd=str(Path(__file__).parent.parent),
    )

    if result.returncode == 0:
        print("\n  Initial scoring complete!")
    else:
        print(f"\n  Scoring finished with exit code {result.returncode}")
        print("  Check output above for errors. Most common: missing API keys.")


# ============================================================
# STEP 4: Set Up Cron (Optional)
# ============================================================

def setup_cron():
    """Offer to set up automated daily scoring."""
    print("\n" + "=" * 60)
    print("STEP 4: Automated Scheduling (Optional)")
    print("=" * 60)

    print("""
  Recommended schedule:
    - Daily scoring at 7am (scores new content)
    - Weekly digest Monday 8am (Slack-ready summary)
    """)

    resp = input("  Set up automated scheduling? (y/n): ").strip().lower()
    if resp != "y":
        print("  Skipped. You can always set up cron later.")
        return

    vault_root = str(Path(__file__).parent.parent.resolve())
    python_path = sys.executable

    if sys.platform == "darwin":
        # macOS: create launchd plist
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.opened.content-performance-scoring</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{vault_root}/agents/content_performance_agent.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{vault_root}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{vault_root}/.claude/logs/performance-scoring.log</string>
    <key>StandardErrorPath</key>
    <string>{vault_root}/.claude/logs/performance-scoring-error.log</string>
</dict>
</plist>"""

        plist_path = Path.home() / "Library" / "LaunchAgents" / "com.opened.content-performance-scoring.plist"
        log_dir = Path(vault_root) / ".claude" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n  Will create: {plist_path}")
        confirm = input("  Proceed? (y/n): ").strip().lower()
        if confirm == "y":
            plist_path.write_text(plist_content)
            os.system(f"launchctl load {plist_path}")
            print(f"  Created and loaded launchd plist.")
            print(f"  Scoring will run daily at 7:00 AM.")
            print(f"  Logs: {log_dir}/performance-scoring.log")
        else:
            print("  Skipped.")

    else:
        # Linux/Windows: show crontab entry
        cron_line = f"0 7 * * * cd {vault_root} && {python_path} agents/content_performance_agent.py"
        print(f"\n  Add this to your crontab (run `crontab -e`):\n")
        print(f"  {cron_line}")
        print(f"\n  For weekly digest, also add:")
        digest_line = f"0 8 * * 1 cd {vault_root} && {python_path} agents/content_performance_agent.py --digest-only --output slack"
        print(f"  {digest_line}")


# ============================================================
# STEP 5: Summary
# ============================================================

def print_summary():
    """Print what was set up and next steps."""
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)

    print("""
  What's now available:

  1. NOTION DASHBOARD
     Open Master Content Database > look for "Performance Dashboard" view
     (Create a view: filter Status = Posted, sort by Performance Score desc)

  2. RUN SCORING ANYTIME
     python agents/content_performance_agent.py

  3. GENERATE INSIGHTS DIGEST
     python agents/content_performance_agent.py --digest-only

  4. SLACK-READY DIGEST
     python agents/content_performance_agent.py --digest-only --output slack

  5. SCORE SPECIFIC CONTENT
     python agents/content_performance_agent.py --type blog
     python agents/content_performance_agent.py --type social

  Files created:
    .claude/skills/content-performance-scoring/SKILL.md  (full docs)
    .claude/references/content-performance-scoring-quickref.md  (quick ref)
    agents/content_performance_agent.py  (the scoring agent)
    agents/setup_performance_scoring.py  (this setup script)
    """)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("Content Performance Scoring - Setup Wizard")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print("""
  This will:
    1. Check your API keys (.env)
    2. Add performance tracking properties to Notion
    3. Run initial scoring on all published content
    4. Optionally set up daily automated scoring

  Takes about 5 minutes. Let's go.
    """)

    # Step 1: Check environment
    if not check_env():
        print("\nSetup cannot continue without required API keys.")
        print(f"Edit your .env file at: {ENV_PATH}")
        sys.exit(1)

    # Step 2: Notion properties
    setup_notion_properties()

    # Step 3: Initial scoring
    run_initial_scoring()

    # Step 4: Cron setup
    setup_cron()

    # Step 5: Summary
    print_summary()


if __name__ == "__main__":
    main()
