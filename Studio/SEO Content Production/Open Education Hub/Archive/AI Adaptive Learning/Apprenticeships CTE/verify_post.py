#!/usr/bin/env python3
"""Verify the Webflow blog post content."""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(Path(__file__).resolve().parents[6] / ".env")
API_KEY = os.getenv("WEBFLOW_API_KEY")
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
