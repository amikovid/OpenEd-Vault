#!/usr/bin/env python3
"""Update the Webflow blog post with DRAFTv6 content (thumbnail removed from body)."""

import requests
import re

# Webflow API config
API_KEY = "032c44041102703cc26944fe7e886b86467da16d228f55eb8d8f4cf75fd3ed7d"
COLLECTION_ID = "6805bf729a7b33423cc8a08c"  # Blog Posts collection
POST_ID = "6973ba66baa7f67631a9093c"
CHARLIE_AUTHOR_ID = "68089b4d33745cf5ea4d746d"

# Read the new HTML content
with open('content.html', 'r') as f:
    html_content = f.read()

# Remove the first figure element (the thumbnail/header image)
# It contains "first-dollar-workbench" in the src
html_content = re.sub(
    r'<figure class="w-richtext-figure-type-image[^>]*>.*?first-dollar-workbench.*?</figure>\s*',
    '',
    html_content,
    count=1,
    flags=re.DOTALL
)

print(f"Content length after removing thumbnail: {len(html_content)} chars")

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

if response.status_code == 200:
    print("\nPost updated successfully!")
    data = response.json()
    print(f"Last Updated: {data.get('lastUpdated')}")
else:
    print("\nError updating post")
    print(response.text[:500])
