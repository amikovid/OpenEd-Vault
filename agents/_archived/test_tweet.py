#!/usr/bin/env python3
"""Quick test tweet via Get Late API"""

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

# Get accounts
print("Fetching accounts...")
response = requests.get(f"{base_url}/accounts", headers=headers)
data = response.json()

print(f"Response type: {type(data)}")
print(f"Response: {json.dumps(data, indent=2)[:1000]}")

# Handle different response formats
accounts = []
if isinstance(data, list):
    accounts = data
elif isinstance(data, dict):
    accounts = data.get("accounts", data.get("data", []))

# Find Twitter
twitter_account = None
for acc in accounts:
    if isinstance(acc, dict) and acc.get("platform") == "twitter":
        twitter_account = acc
        break

if not twitter_account:
    print("\nNo Twitter account found in accounts list")
    print(
        "Available platforms:",
        [a.get("platform") for a in accounts if isinstance(a, dict)],
    )
    sys.exit(1)

account_id = twitter_account.get("_id") or twitter_account.get("id")
print(f"\nTwitter account ID: {account_id}")
print(
    f"Username: {twitter_account.get('username', twitter_account.get('displayName', 'Unknown'))}"
)

# Send test tweet
post_data = {
    "platforms": [{"platform": "twitter", "accountId": account_id}],
    "content": "Testing our new social media automation pipeline. Please ignore!",
    "publishNow": True,
}

print("\nSending test tweet...")
response = requests.post(f"{base_url}/posts", headers=headers, json=post_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
