#!/usr/bin/env python3
"""
Batch upload comparison articles to Webflow as drafts.
Created: 2026-01-29
"""

import os
import re
import sys
import json
import hashlib
import requests
from pathlib import Path

# Load API key from .env
ENV_PATH = Path(__file__).parent.parent.parent / ".env"
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith("WEBFLOW_API_KEY="):
            API_KEY = line.strip().split("=", 1)[1]
            break

# Webflow config
SITE_ID = "67c7406fc9e6913d1b92e341"
POSTS_COLLECTION = "6805bf729a7b33423cc8a08c"
BLOG_POST_TYPE = "6805d44048df4bd97a0754ed"
CHARLIE_AUTHOR = "68089b4d33745cf5ea4d746d"

BASE_PATH = Path(__file__).parent

# Add seomachine tools to path for shared utilities
_seomachine_tools = BASE_PATH / "seomachine" / "tools"
if str(_seomachine_tools) not in sys.path:
    sys.path.insert(0, str(_seomachine_tools))

from seo_schema_generator import generate_all_schema

# Articles to upload
ARTICLES = [
    {
        "name": "Waldorf vs Montessori: A Parent's Guide",
        "slug": "waldorf-vs-montessori",
        "summary": "Comparing Waldorf and Montessori? Understand the real differences - philosophy, materials, technology, and reading approaches - plus how to take what works from each for your family.",
        "draft_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Waldorf vs Montessori/DRAFT_v1.md",
        "thumbnail_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Waldorf vs Montessori/thumbnail-final_20260128_213719_edit_pro.png",
    },
    {
        "name": "Montessori vs Reggio Emilia: What Parents Should Know",
        "slug": "montessori-vs-reggio-emilia",
        "summary": "Compare Montessori and Reggio Emilia approaches to early childhood education. Learn how these Italian-born methods differ in curriculum, materials, and teacher roles.",
        "draft_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Montessori vs Reggio Emilia/DRAFT_v1.md",
        "thumbnail_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Montessori vs Reggio Emilia/thumbnail_20260129_120350_gen_pro.png",
    },
    {
        "name": "Khan Academy vs IXL: Honest Comparison for Homeschool Math",
        "slug": "khan-academy-vs-ixl",
        "summary": "Khan Academy is free. IXL has thousands of skills. Which is actually better for your homeschooler? We break down when to use each - and why many families use both.",
        "draft_path": BASE_PATH / "Versus/khan-academy-vs-ixl/draft-v1.md",
        "thumbnail_path": BASE_PATH / "Versus/khan-academy-vs-ixl/thumbnail_20260129_112654_gen_pro.png",
    },
    {
        "name": "Saxon Math vs Math-U-See: Which Is Right for Your Family?",
        "slug": "saxon-math-vs-math-u-see",
        "summary": "Saxon Math or Math-U-See? We break down the real differences - spiral vs mastery, drill vs manipulatives - to help you choose the right math curriculum.",
        "draft_path": BASE_PATH / "Versus/saxon-vs-math-u-see/draft-v1.md",
        "thumbnail_path": BASE_PATH / "Versus/saxon-vs-math-u-see/thumbnail_20260129_112720_gen_pro.png",
    },
    {
        "name": "IXL vs Exact Path: What OpenEd Teachers Actually Recommend",
        "slug": "ixl-vs-exact-path",
        "summary": "Our teachers work with both daily. Here's when to use IXL, when to use Exact Path - and why most families should use both.",
        "draft_path": BASE_PATH / "Versus/ixl-vs-exact-path/draft-v2.md",
        "thumbnail_path": BASE_PATH / "Versus/ixl-vs-exact-path/thumbnail_20260129_112742_gen_pro.png",
    },
]


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

    # Skip metadata lines
    if block.startswith('*Meta Title:') or block.startswith('*Meta Description:') or block.startswith('*URL:'):
        return ''
    if block.startswith('*Word count:'):
        return ''

    # Headers
    if block.startswith('#### '):
        return f'<h4>{convert_inline(block[5:])}</h4>'
    elif block.startswith('### '):
        return f'<h3>{convert_inline(block[4:])}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:])}</h2>'
    elif block.startswith('# '):
        return ''  # Skip H1 - it becomes the name field

    # Horizontal rule
    if block == '---':
        return ''  # Skip separators

    # Unordered list
    if block.startswith('- '):
        items = []
        for line in block.split('\n'):
            if line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Ordered list
    if re.match(r'^\d+\.', block):
        items = []
        for line in block.split('\n'):
            match = re.match(r'^\d+\.\s*(.+)', line)
            if match:
                items.append(f'<li>{convert_inline(match.group(1))}</li>')
        return '<ol>' + ''.join(items) + '</ol>'

    # Blockquote
    if block.startswith('>'):
        quote_text = block[1:].strip()
        return f'<blockquote>{convert_inline(quote_text)}</blockquote>'

    # Table - convert to HTML table
    if '|' in block and block.count('|') > 2:
        lines = block.strip().split('\n')
        html = '<table>'
        for i, line in enumerate(lines):
            if '---' in line:
                continue  # Skip separator line
            cells = [c.strip() for c in line.split('|') if c.strip()]
            tag = 'th' if i == 0 else 'td'
            row = ''.join(f'<{tag}>{convert_inline(c)}</{tag}>' for c in cells)
            html += f'<tr>{row}</tr>'
        html += '</table>'
        return html

    # Regular paragraph
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'


def markdown_to_html(content):
    """Convert full markdown to HTML."""
    # Remove title line
    lines = content.split('\n')
    if lines[0].startswith('# '):
        content = '\n'.join(lines[1:])

    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = [convert_block(b) for b in blocks]
    return '\n\n'.join(b for b in html_blocks if b)


def detect_content_type(file_data):
    """Detect image content type from magic bytes."""
    if file_data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    if file_data[:2] == b'\xff\xd8':
        return 'image/jpeg'
    if file_data[:4] == b'RIFF' and file_data[8:12] == b'WEBP':
        return 'image/webp'
    if file_data[:4] == b'GIF8':
        return 'image/gif'
    return 'image/png'  # fallback


def upload_image(image_path, descriptive_name=None):
    """Upload image to Webflow CDN. Returns (asset_id, cdn_url)."""
    upload_name = descriptive_name or image_path.name

    # Step 1: Get presigned URL
    with open(image_path, 'rb') as f:
        file_data = f.read()
    file_hash = hashlib.md5(file_data).hexdigest()
    content_type = detect_content_type(file_data)

    resp = requests.post(
        f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "fileName": upload_name,
            "fileHash": file_hash
        }
    )

    if resp.status_code not in [200, 201, 202]:
        print(f"  Error getting presigned URL: {resp.status_code}")
        print(f"  {resp.text[:300]}")
        return None, None

    data = resp.json()
    asset_id = data.get("id")
    upload_url = data.get("uploadUrl")
    upload_details = data.get("uploadDetails", {})

    if not upload_url:
        # Asset may already exist
        cdn_url = data.get('hostedUrl', f"https://cdn.prod.website-files.com/{SITE_ID}/{asset_id}_{upload_name}")
        return asset_id, cdn_url

    # Step 2: Upload to S3 - read ALL fields from uploadDetails
    files = {"file": (upload_name, file_data, content_type)}
    form_data = dict(upload_details)
    form_data['Content-Type'] = content_type

    s3_resp = requests.post(upload_url, data=form_data, files=files)

    if s3_resp.status_code not in [200, 201]:
        print(f"  S3 upload failed: {s3_resp.status_code}")
        return None, None

    cdn_url = f"https://cdn.prod.website-files.com/{SITE_ID}/{asset_id}_{upload_name}"
    return asset_id, cdn_url


def create_draft_post(article, thumbnail_asset_id, thumbnail_url):
    """Create a draft blog post in Webflow."""
    # Read and convert markdown
    with open(article["draft_path"], 'r') as f:
        markdown = f.read()

    html_content = markdown_to_html(markdown)

    # Generate SEO schema
    schemas = generate_all_schema(
        headline=article["name"],
        description=article["summary"],
        date_published="2026-02-06T00:00:00.000Z",
        slug=article["slug"],
        html_content=html_content,
        image_url=thumbnail_url,
    )
    faq_schema = schemas.get('faq', '')
    if faq_schema:
        print(f"  FAQ schema: {faq_schema.count('Question')} questions found")

    field_data = {
        "name": article["name"],
        "slug": article["slug"],
        "post-type": [BLOG_POST_TYPE],
        "summary": article["summary"],
        "author": CHARLIE_AUTHOR,
        "content": html_content
    }

    # Add thumbnail if uploaded successfully
    if thumbnail_asset_id and thumbnail_url:
        field_data["thumbnail"] = {
            "fileId": thumbnail_asset_id,
            "url": thumbnail_url
        }

    # Add FAQ schema if generated
    if faq_schema:
        field_data["faq-schema"] = faq_schema

    payload = {
        "isArchived": False,
        "isDraft": True,
        "fieldData": field_data
    }

    resp = requests.post(
        f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    return resp


def main():
    print("=" * 60)
    print("Webflow Batch Upload - 5 Comparison Articles")
    print("=" * 60)

    results = []

    for i, article in enumerate(ARTICLES, 1):
        print(f"\n[{i}/5] {article['name']}")
        print("-" * 40)

        # Check files exist
        if not article["draft_path"].exists():
            print(f"  ERROR: Draft not found: {article['draft_path']}")
            results.append({"article": article["name"], "status": "FAILED", "error": "Draft not found"})
            continue

        if not article["thumbnail_path"].exists():
            print(f"  WARNING: Thumbnail not found: {article['thumbnail_path']}")
            thumbnail_id, thumbnail_url = None, None
        else:
            # Upload thumbnail with descriptive name
            print(f"  Uploading thumbnail...")
            descriptive_name = f"{article['slug']}-thumbnail{article['thumbnail_path'].suffix}"
            thumbnail_id, thumbnail_url = upload_image(article["thumbnail_path"], descriptive_name)
            if thumbnail_id:
                print(f"  Thumbnail uploaded: {thumbnail_id}")
            else:
                print(f"  Thumbnail upload failed - continuing without image")

        # Create draft post
        print(f"  Creating draft post...")
        resp = create_draft_post(article, thumbnail_id, thumbnail_url)

        if resp.status_code in [200, 201, 202]:
            data = resp.json()
            post_id = data.get("id")
            print(f"  SUCCESS! Post ID: {post_id}")
            results.append({
                "article": article["name"],
                "status": "SUCCESS",
                "post_id": post_id,
                "slug": article["slug"]
            })
        else:
            print(f"  FAILED: {resp.status_code}")
            print(f"  {resp.text[:300]}")
            results.append({
                "article": article["name"],
                "status": "FAILED",
                "error": resp.text[:200]
            })

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    success = [r for r in results if r["status"] == "SUCCESS"]
    failed = [r for r in results if r["status"] == "FAILED"]

    print(f"\nSuccessfully created: {len(success)}")
    for r in success:
        print(f"  - {r['article']}")
        print(f"    Slug: {r['slug']}")
        print(f"    Post ID: {r['post_id']}")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for r in failed:
            print(f"  - {r['article']}: {r.get('error', 'Unknown error')}")

    print("\nAll posts created as DRAFTS. Review in Webflow CMS before publishing.")


if __name__ == "__main__":
    main()
