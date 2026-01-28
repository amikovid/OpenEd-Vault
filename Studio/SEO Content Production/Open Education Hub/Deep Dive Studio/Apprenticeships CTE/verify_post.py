#!/usr/bin/env python3
"""Verify the Webflow blog post content."""

import requests

API_KEY = "032c44041102703cc26944fe7e886b86467da16d228f55eb8d8f4cf75fd3ed7d"
COLLECTION_ID = "6805bf729a7b33423cc8a08c"
POST_ID = "6973ba66baa7f67631a9093c"

url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{POST_ID}"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)
data = response.json()
content = data['fieldData']['content']

print("=== INTRO (first 800 chars) ===")
print(content[:800])
print("\n=== VERIFICATION ===")
print(f"New intro present: {'education reform' in content[:500]}")
print(f"V3 infographic present: {'opportunity-gap-v3' in content}")
print(f"Old infographic gone: {'6973ba00bd51c5d837e4169b' not in content}")
print(f"Thumbnail in body: {'first-dollar-workbench' in content}")
print(f"Total content length: {len(content)} chars")
