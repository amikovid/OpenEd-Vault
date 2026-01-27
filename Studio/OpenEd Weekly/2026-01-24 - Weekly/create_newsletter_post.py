#!/usr/bin/env python3
"""Create the weekly newsletter as a Webflow blog post."""

import requests
import re

# Webflow API config
API_KEY = "032c44041102703cc26944fe7e886b86467da16d228f55eb8d8f4cf75fd3ed7d"
COLLECTION_ID = "6805bf729a7b33423cc8a08c"  # Blog Posts collection
CHARLIE_AUTHOR_ID = "68089b4d33745cf5ea4d746d"

# Post types
DAILY_NEWSLETTERS_TYPE = "6805d5076ff8c966566279a4"

# Meme thumbnail (already uploaded)
MEME_ASSET_ID = "6973d3d46688c54edafc32bb"
MEME_CDN_URL = "https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/6973d3d46688c54edafc32bb_meme-ai-essays-darth-maul.png"

def convert_inline(text):
    """Convert inline markdown to HTML."""
    # Links first
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)
    return text

def convert_block(block):
    """Convert a markdown block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Skip the title
    if block.startswith('# '):
        return ''

    # Images
    img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', block)
    if img_match:
        alt = img_match.group(1)
        src = img_match.group(2)
        return f'''<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="{src}" alt="{alt}" loading="lazy">
  </div>
</figure>'''

    # Headers
    if block.startswith('#### '):
        return f'<h4>{convert_inline(block[5:])}</h4>'
    elif block.startswith('### '):
        return f'<h3>{convert_inline(block[4:])}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:])}</h2>'

    # Horizontal rule
    if block == '---':
        return '<hr>'

    # Unordered list
    if block.startswith('- '):
        items = []
        for line in block.split('\n'):
            if line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Numbered list
    if re.match(r'^\d+\.', block):
        items = []
        for line in block.split('\n'):
            match = re.match(r'^\d+\.\s*(.+)', line)
            if match:
                items.append(f'<li>{convert_inline(match.group(1))}</li>')
        return '<ol>' + ''.join(items) + '</ol>'

    # Regular paragraph
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'

def markdown_to_html(content):
    """Convert newsletter markdown to HTML."""
    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = [convert_block(b) for b in blocks]
    return '\n\n'.join(b for b in html_blocks if b)

# Read the newsletter
with open('Weekly_Newsletter_DRAFTv3.md', 'r') as f:
    markdown = f.read()

# Convert to HTML
html_content = markdown_to_html(markdown)
print(f"Converted to {len(html_content)} chars HTML")

# Create the post
payload = {
    "isArchived": False,
    "isDraft": True,
    "fieldData": {
        "name": "OpenEd Weekly: The Modern Apprenticeship",
        "slug": "opened-weekly-2026-01-24",
        "post-type": [DAILY_NEWSLETTERS_TYPE],
        "summary": "Why 'College-for-All' is cracking, the rise of apprenticeships and CTE, plus tools for career exploration and a free webinar on homeschool calm.",
        "published-date": "2026-01-24T00:00:00.000Z",
        "author": CHARLIE_AUTHOR_ID,
        "thumbnail": {
            "fileId": MEME_ASSET_ID,
            "url": MEME_CDN_URL
        },
        "content": html_content
    }
}

url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status: {response.status_code}")

if response.status_code in [200, 201]:
    data = response.json()
    print(f"\nPost created successfully!")
    print(f"Post ID: {data.get('id')}")
    print(f"Slug: {data.get('fieldData', {}).get('slug')}")
    print(f"Status: Draft")
else:
    print(f"\nError: {response.text[:500]}")
