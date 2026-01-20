#!/usr/bin/env python3
"""Post a specific tweet via Get Late API"""

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

# Get the tweet content from command line or use default
if len(sys.argv) > 1:
    tweet_content = sys.argv[1]
else:
    tweet_content = """How do you compress a semester of math into 20-40 hours?

@justinskycak at @_MathAcademy_: "The AI handles personalization. The teaching comes from human expertise."

We surveyed the AI tutoring landscape. Here's what actually works:
opened.co/blog/ai-tutors-homeschool"""

print(f"Tweet content:\n{tweet_content}\n")
print(f"Length: {len(tweet_content)} characters\n")

# Get Twitter account
response = requests.get(f"{base_url}/accounts", headers=headers)
accounts = response.json().get("accounts", [])

twitter_account = None
for acc in accounts:
    if isinstance(acc, dict) and acc.get("platform") == "twitter":
        twitter_account = acc
        break

if not twitter_account:
    print("No Twitter account found")
    sys.exit(1)

account_id = twitter_account.get("_id")
print(
    f"Posting to @{twitter_account.get('username', twitter_account.get('displayName', 'Unknown'))}"
)

# Confirm before posting
confirm = input("\nPost this tweet? (y/n): ")
if confirm.lower() != "y":
    print("Cancelled.")
    sys.exit(0)

# Post tweet
post_data = {
    "platforms": [{"platform": "twitter", "accountId": account_id}],
    "content": tweet_content,
    "publishNow": True,
}

response = requests.post(f"{base_url}/posts", headers=headers, json=post_data)
print(f"\nStatus: {response.status_code}")

if response.status_code == 201:
    data = response.json()
    post = data.get("post", {})
    platforms = post.get("platforms", [])
    if platforms:
        url = platforms[0].get("platformPostUrl", "")
        print(f"Posted! {url}")
else:
    print(f"Error: {response.text}")
