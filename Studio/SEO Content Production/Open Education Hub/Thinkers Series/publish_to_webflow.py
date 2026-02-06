#!/usr/bin/env python3
"""Publish Thinkers Series articles to Webflow as drafts.

Usage:
    python3 publish_to_webflow.py montessori
    python3 publish_to_webflow.py gray
    python3 publish_to_webflow.py all
"""

import os
import re
import sys
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load API key from vault root .env
_script_dir = Path(__file__).resolve().parent
_vault_root = _script_dir.parents[3]  # OpenEd Vault/
load_dotenv(_vault_root / ".env")
API_KEY = os.getenv("WEBFLOW_API_KEY")
SITE_ID = "67c7406fc9e6913d1b92e341"
POSTS_COLLECTION = "6805bf729a7b33423cc8a08c"
BLOG_POST_TYPE = "6805d44048df4bd97a0754ed"
AUTHOR_CHARLIE = "68089b4d33745cf5ea4d746d"

# Add seomachine tools to path for shared utilities
_seomachine_tools = _vault_root / "Studio" / "SEO Content Production" / "seomachine" / "tools"
if str(_seomachine_tools) not in sys.path:
    sys.path.insert(0, str(_seomachine_tools))

from seo_schema_generator import generate_all_schema

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SERIES_DIR = Path(__file__).resolve().parent

# Article configurations - paths relative to per-thinker folders
ARTICLES = {
    "gatto": {
        "folder": "gatto",
        "draft_file": "draft-v2.md",
        "title": "John Taylor Gatto: The Award-Winning Teacher Who Quit to Tell the Truth",
        "slug": "john-taylor-gatto",
        "summary": "NYC's Teacher of the Year quit to expose the \"hidden curriculum.\" Discover Gatto's 7 lessons schools really teach and why his critique still matters today.",
        "thumbnail": "images/thumbnail.png",
        "thumbnail_cdn_name": "gatto-thinker-thumbnail.png",
        "published_date": "2026-02-04T00:00:00.000Z",
    },
    "gray": {
        "folder": "gray",
        "draft_file": "draft-v2.md",
        "title": "Why Play Matters in Education: Peter Gray's Research on How Children Learn",
        "slug": "peter-gray",
        "summary": "Peter Gray's research shows play isn't a break from learning - it IS learning. His work on self-directed education is changing how families think about school.",
        "thumbnail": "images/thumbnail.png",
        "thumbnail_cdn_name": "gray-thinker-thumbnail.png",
        "published_date": "2026-02-04T00:00:00.000Z",
    },
    "montessori": {
        "folder": "montessori",
        "draft_file": "draft-v2.md",
        "title": "Maria Montessori and the Family Secret That Shaped Her Legacy",
        "slug": "maria-montessori",
        "summary": "Maria Montessori hid her son Mario for 14 years to protect her career. Here's how he became a pivotal partner in establishing the Montessori method.",
        "thumbnail": "images/tribute.png",
        "thumbnail_cdn_name": "montessori-thinker-thumbnail.png",
        "published_date": "2026-02-04T00:00:00.000Z",
    },
}


def get_file_hash(filepath):
    """Get MD5 hash of file."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def detect_content_type(filepath):
    """Detect image content type from magic bytes."""
    with open(filepath, 'rb') as f:
        header = f.read(12)
    if header[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    if header[:2] == b'\xff\xd8':
        return 'image/jpeg'
    if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        return 'image/webp'
    if header[:4] == b'GIF8':
        return 'image/gif'
    return 'image/png'  # fallback


def upload_image(filepath, descriptive_name):
    """Upload image to Webflow and return CDN URL and asset ID."""
    print(f"  Uploading {filepath.name} as '{descriptive_name}'...")

    file_hash = get_file_hash(filepath)
    content_type = detect_content_type(filepath)

    response = requests.post(
        f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
        headers=HEADERS,
        json={"fileName": descriptive_name, "fileHash": file_hash}
    )

    if response.status_code not in [200, 201, 202]:
        print(f"  Error requesting upload URL: {response.status_code}")
        print(f"  {response.text}")
        return None, None

    data = response.json()

    # Already uploaded (hash match)
    if data.get('hostedUrl'):
        print(f"  Already uploaded: {data['hostedUrl']}")
        return data['hostedUrl'], data.get('id')

    upload_url = data['uploadUrl']
    upload_details = data['uploadDetails']
    asset_id = data['id']

    with open(filepath, 'rb') as f:
        files = {'file': (descriptive_name, f, content_type)}
        # Read ALL form fields from uploadDetails
        form_data = {}
        for key, value in upload_details.items():
            form_data[key] = value
        # Override Content-Type with detected type
        form_data['Content-Type'] = content_type
        upload_response = requests.post(upload_url, data=form_data, files=files)

        if upload_response.status_code not in [200, 201]:
            print(f"  Error uploading to S3: {upload_response.status_code}")
            print(f"  {upload_response.text}")
            return None, None

    cdn_url = f"https://cdn.prod.website-files.com/{SITE_ID}/{asset_id}_{descriptive_name}"
    print(f"  Uploaded: {cdn_url}")
    return cdn_url, asset_id


def convert_inline(text):
    """Convert inline markdown to HTML."""
    # Links first (so **[link](url)** works)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (asterisk)
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    # Italic (underscore)
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)
    # Clean escaped chars
    text = text.replace(r'\-', '-')
    text = text.replace(r'\~', '~')
    return text


def convert_block(block):
    """Convert a single paragraph block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Skip frontmatter and meta sections
    skip_prefixes = [
        '# Draft v2:', '**Date:**', '**Type:**', '**Target:**', '**Hook:**',
        '**Focus:**', '**Title:**',
        '## META ELEMENTS', '**Title Options:**', '**Meta Description',
        '**URL', '## ARTICLE', '## ENHANCED ARTICLE', '## NOTES FOR JUDGES',
        '**Word count:**', '**Internal links', '**External links',
        '**Target keywords', '**OpenEd connection', '**Unique angle',
        '**Changes from original', '**New sections'
    ]
    if any(block.startswith(s) for s in skip_prefixes):
        return ''

    # Skip numbered title options (1. Title here (XX chars))
    if re.match(r'^\d+\.\s+.+\(\d+ chars\)', block):
        return ''

    # Skip numbered notes items
    if re.match(r'^\d+\.\s+(Montessori|Peter|Podcast|What|Microschool|Lost|Why|Links|Living|Philosophy|Connected|Proprietary|Modern|Practical|Secret|Exile|Connects)', block):
        return ''

    # Code blocks
    if block.startswith('```'):
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
        return ''  # Skip H1 - becomes the title field

    # Horizontal rule
    if block == '---':
        return ''

    # Unordered list
    if block.startswith('* ') or block.startswith('- '):
        items = []
        for line in block.split('\n'):
            line = line.strip()
            if line.startswith('* '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
            elif line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        if items:
            return '<ul>' + ''.join(items) + '</ul>'
        return ''

    # Ordered list
    if re.match(r'^\d+\.', block):
        items = []
        for line in block.split('\n'):
            line = line.strip()
            match = re.match(r'^\d+\.\s*(.+)', line)
            if match:
                items.append(f'<li>{convert_inline(match.group(1))}</li>')
        if items:
            return '<ol>' + ''.join(items) + '</ol>'
        return ''

    # Regular paragraph
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'


def extract_article_content(markdown):
    """Extract only the article body from the full draft markdown."""
    # Find the ARTICLE section (handles both "## ARTICLE" and "## ENHANCED ARTICLE")
    if '## ENHANCED ARTICLE' in markdown:
        content = markdown.split('## ENHANCED ARTICLE')[1]
    elif '## ARTICLE' in markdown:
        content = markdown.split('## ARTICLE')[1]
    else:
        content = markdown

    # Remove NOTES FOR JUDGES and everything after
    if '## NOTES FOR JUDGES' in content:
        content = content.split('## NOTES FOR JUDGES')[0]

    return content


def markdown_to_html(markdown):
    """Convert markdown article content to HTML."""
    content = extract_article_content(markdown)

    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = [convert_block(b) for b in blocks]
    html = '\n\n'.join(b for b in html_blocks if b)

    return html


def create_post(title, slug, summary, html_content, thumbnail_url, thumbnail_id, published_date, faq_schema=None):
    """Create the blog post in Webflow as a draft."""
    print(f"  Creating draft post: '{title}'...")

    field_data = {
        "name": title,
        "slug": slug,
        "post-type": [BLOG_POST_TYPE],
        "summary": summary,
        "published-date": published_date,
        "author": AUTHOR_CHARLIE,
        "thumbnail": {
            "fileId": thumbnail_id,
            "url": thumbnail_url
        },
        "content": html_content
    }

    # Add FAQ schema if generated (requires faq-schema CMS field in Designer)
    if faq_schema:
        field_data["faq-schema"] = faq_schema

    payload = {
        "isArchived": False,
        "isDraft": True,
        "fieldData": field_data
    }

    response = requests.post(
        f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items",
        headers=HEADERS,
        json=payload
    )

    if response.status_code in [200, 201, 202]:
        data = response.json()
        post_id = data.get('id')
        print(f"  Post created as DRAFT!")
        print(f"  Post ID: {post_id}")
        print(f"  CMS URL: https://webflow.com/dashboard/sites/opened/cms/collections/{POSTS_COLLECTION}/items/{post_id}")
        return data
    else:
        print(f"  Error creating post: {response.status_code}")
        print(f"  {response.text}")
        return None


def publish_article(key):
    """Publish a single article by key."""
    config = ARTICLES[key]
    print(f"\n{'='*50}")
    print(f"Publishing: {config['title'][:50]}...")
    print(f"{'='*50}")

    folder = SERIES_DIR / config['folder']

    # Step 1: Upload thumbnail
    print("\n1. Uploading thumbnail...")
    thumb_path = folder / config['thumbnail']
    if not thumb_path.exists():
        print(f"  ERROR: Thumbnail not found: {thumb_path}")
        return None
    thumb_url, thumb_id = upload_image(thumb_path, config['thumbnail_cdn_name'])
    if not thumb_url:
        print("  Thumbnail upload failed. Aborting.")
        return None

    # Step 2: Convert markdown to HTML
    print("\n2. Converting markdown to HTML...")
    draft_path = folder / config['draft_file']
    if not draft_path.exists():
        print(f"  ERROR: Draft not found: {draft_path}")
        return None
    with open(draft_path, 'r') as f:
        markdown = f.read()
    html = markdown_to_html(markdown)
    print(f"  Converted {len(markdown)} chars markdown -> {len(html)} chars HTML")

    # Save HTML for review
    html_path = folder / "content.html"
    with open(html_path, 'w') as f:
        f.write(html)
    print(f"  Saved HTML preview: {html_path.name}")

    # Step 2b: Generate SEO schema
    print("\n2b. Generating SEO schema...")
    schemas = generate_all_schema(
        headline=config['title'],
        description=config['summary'],
        date_published=config['published_date'],
        slug=config['slug'],
        html_content=html,
        image_url=thumb_url,
    )
    faq_schema = schemas.get('faq', '')
    if faq_schema:
        print(f"  FAQ schema generated ({faq_schema.count('Question')} questions)")
    else:
        print("  No FAQ pairs found in content")

    # Step 3: Create draft post
    print("\n3. Creating Webflow draft...")
    result = create_post(
        title=config['title'],
        slug=config['slug'],
        summary=config['summary'],
        html_content=html,
        thumbnail_url=thumb_url,
        thumbnail_id=thumb_id,
        published_date=config['published_date'],
        faq_schema=faq_schema,
    )

    return result


def main():
    if not API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found in .env")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python3 publish_to_webflow.py [montessori|gray|all]")
        sys.exit(1)

    target = sys.argv[1].lower()

    if target == "all":
        keys = list(ARTICLES.keys())
    elif target in ARTICLES:
        keys = [target]
    else:
        print(f"Unknown article: {target}")
        print(f"Available: {', '.join(ARTICLES.keys())}, all")
        sys.exit(1)

    results = {}
    for key in keys:
        result = publish_article(key)
        results[key] = result

    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    for key, result in results.items():
        status = "CREATED" if result else "FAILED"
        print(f"  {key}: {status}")
        if result:
            post_id = result.get('id')
            print(f"    CMS: https://webflow.com/dashboard/sites/opened/cms/collections/{POSTS_COLLECTION}/items/{post_id}")


if __name__ == '__main__':
    main()
