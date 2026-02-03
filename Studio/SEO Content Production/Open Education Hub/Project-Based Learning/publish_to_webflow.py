#!/usr/bin/env python3
"""Publish Project-Based Learning article to Webflow."""

import os
import re
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(Path(__file__).resolve().parents[4] / ".env")
API_KEY = os.getenv("WEBFLOW_API_KEY")
SITE_ID = "67c7406fc9e6913d1b92e341"
POSTS_COLLECTION = "6805bf729a7b33423cc8a08c"
BLOG_POST_TYPE = "6805d44048df4bd97a0754ed"
AUTHOR_CHARLIE = "68089b4d33745cf5ea4d746d"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Image paths
IMAGES_DIR = Path("images")
THUMBNAIL = IMAGES_DIR / "thumbnail-final.png"
INFOGRAPHIC = IMAGES_DIR / "infographic-spectrum.png"

# Will be populated after upload
CDN_URLS = {}


def get_file_hash(filepath):
    """Get MD5 hash of file."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def upload_image(filepath, descriptive_name):
    """Upload image to Webflow and return CDN URL and asset ID."""
    print(f"Uploading {filepath.name}...")

    file_hash = get_file_hash(filepath)

    # Step 1: Request presigned URL
    response = requests.post(
        f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
        headers=HEADERS,
        json={"fileName": descriptive_name, "fileHash": file_hash}
    )

    if response.status_code not in [200, 201, 202]:
        print(f"Error requesting upload URL: {response.status_code}")
        print(response.text)
        return None, None

    data = response.json()

    # Check if already uploaded (hash match)
    if data.get('hostedUrl'):
        print(f"  Already uploaded: {data['hostedUrl']}")
        return data['hostedUrl'], data.get('id')

    upload_url = data['uploadUrl']
    upload_details = data['uploadDetails']
    asset_id = data['id']

    # Step 2: Upload to S3
    with open(filepath, 'rb') as f:
        files = {'file': (descriptive_name, f, 'image/png')}
        form_data = {
            'acl': upload_details['acl'],
            'bucket': upload_details['bucket'],
            'X-Amz-Algorithm': upload_details['X-Amz-Algorithm'],
            'X-Amz-Credential': upload_details['X-Amz-Credential'],
            'X-Amz-Date': upload_details['X-Amz-Date'],
            'key': upload_details['key'],
            'Policy': upload_details['Policy'],
            'X-Amz-Signature': upload_details['X-Amz-Signature'],
            'success_action_status': '201',
            'Content-Type': 'image/png',
            'Cache-Control': 'max-age=31536000, immutable'
        }

        upload_response = requests.post(upload_url, data=form_data, files=files)

        if upload_response.status_code not in [200, 201]:
            print(f"Error uploading to S3: {upload_response.status_code}")
            print(upload_response.text)
            return None, None

    # Construct CDN URL
    cdn_url = f"https://cdn.prod.website-files.com/{SITE_ID}/{asset_id}_{descriptive_name}"
    print(f"  Uploaded: {cdn_url}")
    return cdn_url, asset_id


def convert_inline(text):
    """Convert inline markdown to HTML - LINKS FIRST, then bold/italic."""
    # Links FIRST (so **[link](url)** works)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Then bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Then italic
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)
    # Clean up escaped characters
    text = text.replace(r'\-', '-')
    text = text.replace(r'\~', '~')
    return text


def convert_block(block):
    """Convert a single paragraph block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Skip metadata sections
    if any(block.startswith(s) for s in ['**Meta Title:**', '**Meta Description:**', '**URL:**', '**Date:**', '**Type:**', '## **META ELEMENTS**', '**Title Options:**']):
        return ''
    if block.startswith('1. Project-Based Learning:') or block.startswith('2. Project-Based Learning') or block.startswith('3. Project-Based Learning'):
        return ''  # Skip title options

    # Skip the ARTICLE header
    if block == '## **ARTICLE**':
        return ''

    # Code blocks (the spectrum diagram)
    if block.startswith('```'):
        # Extract content between ```
        content = re.sub(r'^```\w*\n?', '', block)
        content = re.sub(r'\n?```$', '', content)
        return f'<pre><code>{content}</code></pre>'

    # Headers
    if block.startswith('#### '):
        return f'<h4>{convert_inline(block[5:].strip("*"))}</h4>'
    elif block.startswith('### '):
        return f'<h3>{convert_inline(block[4:].strip("*"))}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:].strip("*"))}</h2>'
    elif block.startswith('# '):
        return ''  # Skip H1 - becomes title

    # Horizontal rule
    if block == '---':
        return ''  # Skip horizontal rules

    # Unordered list (handle * and -)
    if block.startswith('* ') or block.startswith('- '):
        items = []
        for line in block.split('\n'):
            line = line.strip()
            if line.startswith('* '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
            elif line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Ordered list
    if re.match(r'^\d+\.', block):
        items = []
        for line in block.split('\n'):
            line = line.strip()
            match = re.match(r'^\d+\.\s*(.+)', line)
            if match:
                items.append(f'<li>{convert_inline(match.group(1))}</li>')
        return '<ol>' + ''.join(items) + '</ol>'

    # Regular paragraph
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'


def markdown_to_html(content):
    """Convert markdown content to HTML."""
    # Find the ARTICLE section
    if '## **ARTICLE**' in content:
        content = content.split('## **ARTICLE**')[1]

    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = [convert_block(b) for b in blocks]
    html = '\n\n'.join(b for b in html_blocks if b)

    return html


def insert_infographic(html, infographic_url):
    """Insert infographic after the spectrum code block."""
    # Find the spectrum pre/code block and insert image after it
    infographic_html = f'''<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="{infographic_url}" alt="Abstract to Applied learning spectrum - from Math to Science to Engineering to Making" loading="lazy">
  </div>
</figure>'''

    # Insert after the code block
    html = html.replace('</code></pre>', f'</code></pre>\n\n{infographic_html}')
    return html


def create_post(title, slug, summary, html_content, thumbnail_url, thumbnail_id):
    """Create the blog post in Webflow."""
    print("Creating blog post...")

    payload = {
        "isArchived": False,
        "isDraft": True,
        "fieldData": {
            "name": title,
            "slug": slug,
            "post-type": [BLOG_POST_TYPE],
            "summary": summary,
            "published-date": "2026-01-28T00:00:00.000Z",
            "author": AUTHOR_CHARLIE,
            "thumbnail": {
                "fileId": thumbnail_id,
                "url": thumbnail_url
            },
            "content": html_content
        }
    }

    response = requests.post(
        f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items",
        headers=HEADERS,
        json=payload
    )

    if response.status_code in [200, 201, 202]:
        data = response.json()
        print(f"Post created successfully!")
        print(f"Post ID: {data.get('id')}")
        print(f"View in CMS: https://webflow.com/dashboard/sites/opened/cms/collections/{POSTS_COLLECTION}/items/{data.get('id')}")
        return data
    else:
        print(f"Error creating post: {response.status_code}")
        print(response.text)
        return None


def main():
    os.chdir(Path(__file__).parent)

    print("=" * 50)
    print("Publishing Project-Based Learning to Webflow")
    print("=" * 50)

    # Step 1: Upload images
    print("\n1. Uploading images...")
    thumbnail_url, thumbnail_id = upload_image(THUMBNAIL, "pbl-thumbnail-treehouse.png")
    infographic_url, _ = upload_image(INFOGRAPHIC, "pbl-spectrum-infographic.png")

    if not thumbnail_url or not infographic_url:
        print("Image upload failed. Aborting.")
        return

    # Step 2: Read and convert markdown
    print("\n2. Converting markdown to HTML...")
    draft_path = Path("drafts/Copy of Completed_ Draft Content for Stephanie (1).md")
    with open(draft_path, 'r') as f:
        markdown = f.read()

    html = markdown_to_html(markdown)
    html = insert_infographic(html, infographic_url)

    print(f"   Converted {len(markdown)} chars to {len(html)} chars HTML")

    # Save HTML for inspection
    with open("content.html", 'w') as f:
        f.write(html)
    print("   Saved to content.html for review")

    # Step 3: Create the post
    print("\n3. Creating blog post...")
    result = create_post(
        title="Project-Based Learning: A Practical Guide for Homeschool Families",
        slug="project-based-learning",
        summary="Learn how project-based learning transforms homeschool education. Real examples, step-by-step framework, and resources from OpenEd families.",
        html_content=html,
        thumbnail_url=thumbnail_url,
        thumbnail_id=thumbnail_id
    )

    if result:
        print("\n" + "=" * 50)
        print("SUCCESS! Post created as draft.")
        print("Next: Review in Webflow CMS, then publish")
        print("=" * 50)


if __name__ == '__main__':
    main()
