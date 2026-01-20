#!/usr/bin/env python3
"""Post to LinkedIn via Get Late API"""

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

post_content = """How do you compress a semester of math into 20-40 focused hours?

We spent weeks talking to the people actually building AI education - not the hype merchants.

The pattern that emerged: the platforms that work use AI differently than you'd expect.

Math Academy doesn't use chatbots to generate explanations. Humans design every lesson. AI just figures out what your kid is ready to learn next.

Justin Skycak put it simply: "The AI handles personalization and pacing. The teaching comes from human expertise embedded in the content."

Meanwhile, most free AI tutors optimize for engagement - bright colors, dopamine hits, achievement badges - because they need millions of casual users to survive.

The full guide breaks down what's working, what isn't, and how to build your own AI tutoring stack:

opened.co/blog/ai-tutors-homeschool

Thanks to Justin Skycak, Claire Honeycutt, Ben Somers, Ray Ravaglia, and the teams at Math Academy, Synthesis, Khan Academy, and Alpha School for their insights."""

print(f"LinkedIn post:\n{post_content}\n")
print(f"Length: {len(post_content)} characters\n")

# Get LinkedIn account
response = requests.get(f"{base_url}/accounts", headers=headers)
accounts = response.json().get("accounts", [])

linkedin_account = None
for acc in accounts:
    if isinstance(acc, dict) and acc.get("platform") == "linkedin":
        linkedin_account = acc
        break

if not linkedin_account:
    print("No LinkedIn account found")
    sys.exit(1)

account_id = linkedin_account.get("_id")
print(f"Posting to: {linkedin_account.get('displayName', 'Unknown')}")

# Confirm before posting
confirm = input("\nPost to LinkedIn? (y/n): ")
if confirm.lower() != "y":
    print("Cancelled.")
    sys.exit(0)

# Post
post_data = {
    "platforms": [{"platform": "linkedin", "accountId": account_id}],
    "content": post_content,
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
