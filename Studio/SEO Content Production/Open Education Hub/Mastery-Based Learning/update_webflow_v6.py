#!/usr/bin/env python3
"""Update existing Webflow draft post with v6-final article content."""

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

# Existing post to update
POST_ID = "69839fd64d38fc1fe12c9a90"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Paths
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "images"
DRAFT = SCRIPT_DIR / "drafts" / "video-article-v6-final.md"

# Images
THUMBNAIL = IMAGES_DIR / "thumbnail-one-room-trap-v2_20260204_111852_gen_pro.jpg"
INFOGRAPHIC_LEBRON = IMAGES_DIR / "infographic-lebron-report-card.jpg"
INFOGRAPHIC_CBE = IMAGES_DIR / "infographic-traditional-vs-cbe.jpg"


def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def verify_cdn_url(url):
    try:
        r = requests.head(url, timeout=5)
        content_type = r.headers.get('Content-Type', '')
        return 'image' in content_type
    except Exception:
        return False


def upload_image(filepath, descriptive_name):
    """Upload image to Webflow and return CDN URL and asset ID."""
    print(f"  Uploading {filepath.name} as {descriptive_name}...")

    file_hash = get_file_hash(filepath)

    response = requests.post(
        f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
        headers=HEADERS,
        json={"fileName": descriptive_name, "fileHash": file_hash}
    )

    if response.status_code not in [200, 201, 202]:
        print(f"    Error requesting upload URL: {response.status_code}")
        print(f"    {response.text}")
        return None, None

    data = response.json()

    if data.get('hostedUrl'):
        hosted = data['hostedUrl']
        asset_id = data.get('id')
        if verify_cdn_url(hosted):
            print(f"    Verified existing: {hosted}")
            return hosted, asset_id
        else:
            print(f"    Stale asset. Deleting and re-uploading...")
            requests.delete(
                f"https://api.webflow.com/v2/sites/{SITE_ID}/assets/{asset_id}",
                headers=HEADERS
            )
            response = requests.post(
                f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
                headers=HEADERS,
                json={"fileName": descriptive_name, "fileHash": file_hash}
            )
            if response.status_code not in [200, 201, 202]:
                print(f"    Error on re-request: {response.status_code}")
                return None, None
            data = response.json()

    if not data.get('uploadUrl'):
        # Already uploaded and CDN is live
        if data.get('hostedUrl') and verify_cdn_url(data['hostedUrl']):
            return data['hostedUrl'], data.get('id')
        print(f"    No uploadUrl. Response: {json.dumps(data, indent=2)[:500]}")
        return None, None

    upload_url = data['uploadUrl']
    upload_details = data['uploadDetails']
    asset_id = data['id']

    content_type = upload_details.get('content-type') or upload_details.get('Content-Type', 'image/jpeg')
    print(f"    Content-Type: {content_type}")

    with open(filepath, 'rb') as f:
        files = {'file': (descriptive_name, f, content_type)}
        form_data = {k: v for k, v in upload_details.items()}
        form_data['success_action_status'] = '201'

        upload_response = requests.post(upload_url, data=form_data, files=files)

        if upload_response.status_code not in [200, 201]:
            print(f"    S3 upload error: {upload_response.status_code}")
            print(f"    {upload_response.text[:500]}")
            return None, None

    cdn_key = upload_details.get('key', f"{SITE_ID}/{asset_id}_{descriptive_name}")
    cdn_url = f"https://cdn.prod.website-files.com/{cdn_key}"
    print(f"    Uploaded: {cdn_url}")

    import time
    time.sleep(2)
    if verify_cdn_url(cdn_url):
        print(f"    Verified live!")
    else:
        print(f"    Warning: CDN not yet live")

    return cdn_url, asset_id


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


def make_figure(url, alt_text):
    return (
        f'<figure class="w-richtext-figure-type-image w-richtext-align-center" '
        f'data-rt-type="image" data-rt-align="center">'
        f'<div><img src="{url}" alt="{alt_text}" loading="lazy"></div>'
        f'</figure>'
    )


def markdown_to_html(content, lebron_url, cbe_url):
    """Convert v6 markdown to Webflow-ready HTML."""
    # Remove everything after SEO Notes
    if '## SEO Notes' in content:
        content = content.split('## SEO Notes')[0]

    # Remove H1 title
    content = re.sub(r'^# .+\n', '', content)
    # Remove byline
    content = re.sub(r'^\*By .+\*\n', '', content, flags=re.MULTILINE)

    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Skip horizontal rules
        if block == '---':
            continue

        # Headers
        if block.startswith('## '):
            html_blocks.append(f'<h2>{convert_inline(block[3:])}</h2>')
            continue

        # Video embed placeholder
        if block.strip() == '[VIDEO EMBED]':
            html_blocks.append('<p>[VIDEO EMBED]</p>')
            continue

        # Inline images - convert to Webflow figures
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', block)
        if img_match:
            alt_text = img_match.group(1)
            img_ref = img_match.group(2)
            if 'INFOGRAPHIC_LEBRON' in img_ref and lebron_url:
                html_blocks.append(make_figure(lebron_url, alt_text))
            elif 'INFOGRAPHIC_CBE' in img_ref and cbe_url:
                html_blocks.append(make_figure(cbe_url, alt_text))
            continue

        # Regular paragraph
        text = ' '.join(line.strip() for line in block.split('\n'))
        html_blocks.append(f'<p>{convert_inline(text)}</p>')

    return '\n\n'.join(html_blocks)


def update_post(html_content, thumbnail_url, thumbnail_id):
    """Update existing post in Webflow."""
    print("Updating blog post draft...")

    payload = {
        "isArchived": False,
        "isDraft": True,
        "fieldData": {
            "name": "What Is Competency-Based Education? Why School Was Never Designed for Your Kid",
            "slug": "competency-based-education",
            "summary": "Horace Mann imported a Prussian military model in 1837 and called it public school. LeBron James would fail by its grading standards. Here's the history and the better alternative.",
            "published-date": "2026-02-05T00:00:00.000Z",
            "author": "68089b4d33745cf5ea4d746d",
            "thumbnail": {
                "fileId": thumbnail_id,
                "url": thumbnail_url
            },
            "content": html_content
        }
    }

    response = requests.patch(
        f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items/{POST_ID}",
        headers=HEADERS,
        json=payload
    )

    if response.status_code in [200, 201, 202]:
        data = response.json()
        print(f"  Post updated successfully!")
        print(f"  Post ID: {POST_ID}")
        print(f"  CMS: https://webflow.com/dashboard/sites/opened/cms/collections/{POSTS_COLLECTION}/items/{POST_ID}")
        return data
    else:
        print(f"  Error updating post: {response.status_code}")
        print(f"  {response.text[:1000]}")
        return None


def main():
    os.chdir(SCRIPT_DIR)

    print("=" * 60)
    print("Updating: What Is Competency-Based Education? (v6-final)")
    print(f"Post ID: {POST_ID}")
    print("=" * 60)

    if not API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found in .env")
        return

    # Step 1: Upload/verify images
    print("\n1. Uploading/verifying images...")
    import time
    ts = str(int(time.time()))
    thumb_url, thumb_id = upload_image(THUMBNAIL, f"cbe-thumb-v6-{ts}.jpg")
    lebron_url, _ = upload_image(INFOGRAPHIC_LEBRON, f"cbe-lebron-v6-{ts}.jpg")
    cbe_url, _ = upload_image(INFOGRAPHIC_CBE, f"cbe-compare-v6-{ts}.jpg")

    if not thumb_url:
        print("ERROR: Thumbnail upload failed. Aborting.")
        return
    if not lebron_url or not cbe_url:
        print("WARNING: Infographic upload failed.")

    # Step 2: Convert markdown to HTML
    print("\n2. Converting v6 markdown to HTML...")
    with open(DRAFT, 'r') as f:
        markdown = f.read()

    html = markdown_to_html(markdown, lebron_url, cbe_url)
    print(f"  {len(markdown)} chars markdown -> {len(html)} chars HTML")

    # Save preview
    preview_path = SCRIPT_DIR / "content-preview-v6.html"
    with open(preview_path, 'w') as f:
        f.write(f'<html><head><style>body{{max-width:700px;margin:40px auto;font-family:Georgia,serif;line-height:1.6}}img{{max-width:100%}}h2{{margin-top:2em}}</style></head><body>\n{html}\n</body></html>')
    print(f"  Preview: {preview_path}")

    # Step 3: Update post
    print("\n3. Updating Webflow draft...")
    result = update_post(html, thumb_url, thumb_id)

    if result:
        print("\n" + "=" * 60)
        print("SUCCESS! Post updated with v6 content.")
        print("Next steps:")
        print("  1. Review in Webflow CMS dashboard")
        print("  2. Replace [VIDEO EMBED] with YouTube embed")
        print("  3. Publish when ready")
        print("=" * 60)


if __name__ == '__main__':
    main()
