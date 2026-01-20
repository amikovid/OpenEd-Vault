#!/usr/bin/env python3
"""Audit all connected platforms and their capabilities"""

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

api_key = os.getenv("GETLATE_API_KEY")
if not api_key:
    print("GETLATE_API_KEY not found")
    sys.exit(1)

base_url = "https://getlate.dev/api/v1"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Get all accounts
response = requests.get(f"{base_url}/accounts", headers=headers)
data = response.json()
accounts = data.get("accounts", [])

print("=" * 60)
print("CONNECTED PLATFORMS - FULL CAPABILITIES AUDIT")
print("=" * 60)

for acc in accounts:
    platform = acc.get("platform", "unknown").upper()
    display = acc.get("displayName") or acc.get("username", "Unknown")
    permissions = acc.get("permissions", [])
    metadata = acc.get("metadata", {})

    print(f"\n{'=' * 40}")
    print(f"{platform}: {display}")
    print(f"{'=' * 40}")
    print(f"Account ID: {acc.get('_id')}")
    print(f"Active: {acc.get('isActive', False)}")

    if permissions:
        print(f"\nPermissions:")
        for p in permissions:
            print(f"  - {p}")

    # Platform-specific
    if platform == "TWITTER":
        profile = metadata.get("profileData", {})
        print(f"\nStats:")
        print(f"  Followers: {profile.get('followersCount', 'N/A')}")
        print(f"  Premium: {profile.get('isPremium', False)}")

    elif platform == "FACEBOOK":
        pages = metadata.get("availablePages", [])
        if pages:
            print(f"\nPages ({len(pages)}):")
            for page in pages[:3]:
                print(f"  - {page.get('name')}")

    elif platform == "LINKEDIN":
        print(f"\nURL: {acc.get('profileUrl', 'N/A')}")

print("\n" + "=" * 60)
print("RAW DATA (first account sample)")
print("=" * 60)
if accounts:
    print(json.dumps(accounts[0], indent=2, default=str)[:2000])
