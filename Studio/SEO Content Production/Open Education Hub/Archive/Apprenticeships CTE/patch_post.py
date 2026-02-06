#!/usr/bin/env python3
"""Patch the Webflow blog post to add author and fix content."""

import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(Path(__file__).resolve().parents[6] / ".env")
API_KEY = os.getenv("WEBFLOW_API_KEY")
COLLECTION_ID = "6805bf729a7b33423cc8a08c"  # Blog Posts collection
POST_ID = "6973ba66baa7f67631a9093c"
CHARLIE_AUTHOR_ID = "68089b4d33745cf5ea4d746d"

# Read the fixed HTML content
with open('content_fixed.html', 'r') as f:
    html_content = f.read()

# Build the payload
payload = {
    "fieldData": {
        "content": html_content,
        "author": CHARLIE_AUTHOR_ID
    }
}

# Make the PATCH request
url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{POST_ID}"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.patch(url, headers=headers, json=payload)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500] if len(response.text) > 500 else response.text}")

if response.status_code == 200:
    print("\nPost updated successfully!")
    data = response.json()
    print(f"Slug: {data.get('fieldData', {}).get('slug')}")
    print(f"Author: {data.get('fieldData', {}).get('author')}")
