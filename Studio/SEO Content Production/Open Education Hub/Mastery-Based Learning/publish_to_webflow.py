#!/usr/bin/env python3
"""Publish Competency-Based Education article to Webflow as draft."""

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

# Paths
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "images"
DRAFT = SCRIPT_DIR / "drafts" / "video-article-v5.md"

# Images to upload
THUMBNAIL = IMAGES_DIR / "thumbnail-one-room-trap-v2_20260204_111852_gen_pro.png"
INFOGRAPHIC_LEBRON = IMAGES_DIR / "infographic-lebron-report-card.png"
INFOGRAPHIC_CBE = IMAGES_DIR / "infographic-traditional-vs-cbe.png"


def get_file_hash(filepath):
    """Get MD5 hash of file."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def verify_cdn_url(url):
    """Check if a CDN URL actually serves an image (not an XML error)."""
    try:
        r = requests.head(url, timeout=5)
        content_type = r.headers.get('Content-Type', '')
        return 'image' in content_type
    except Exception:
        return False


def upload_image(filepath, descriptive_name):
    """Upload image to Webflow and return CDN URL and asset ID.
    Verifies CDN URLs are live. Forces re-upload if stale."""
    print(f"  Uploading {filepath.name} as {descriptive_name}...")

    file_hash = get_file_hash(filepath)

    # Step 1: Request presigned URL
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

    # Check if Webflow says already uploaded
    if data.get('hostedUrl'):
        hosted = data['hostedUrl']
        asset_id = data.get('id')
        # Verify the CDN URL actually works
        if verify_cdn_url(hosted):
            print(f"    Verified existing: {hosted}")
            return hosted, asset_id
        else:
            print(f"    Stale asset detected (CDN returns error). Deleting and re-uploading...")
            # Delete the stale asset
            del_resp = requests.delete(
                f"https://api.webflow.com/v2/sites/{SITE_ID}/assets/{asset_id}",
                headers=HEADERS
            )
            print(f"    Delete status: {del_resp.status_code}")
            # Re-request with same hash (should now get uploadUrl)
            response = requests.post(
                f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
                headers=HEADERS,
                json={"fileName": descriptive_name, "fileHash": file_hash}
            )
            if response.status_code not in [200, 201, 202]:
                print(f"    Error on re-request: {response.status_code}")
                return None, None
            data = response.json()
            # If STILL returning hostedUrl after delete, bail
            if data.get('hostedUrl') and not data.get('uploadUrl'):
                print(f"    Still stale after delete. Trying with modified hash...")
                # Modify the file content slightly
                with open(filepath, 'ab') as f:
                    f.write(os.urandom(16))
                file_hash = get_file_hash(filepath)
                response = requests.post(
                    f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
                    headers=HEADERS,
                    json={"fileName": descriptive_name, "fileHash": file_hash}
                )
                if response.status_code not in [200, 201, 202]:
                    print(f"    Error on modified hash request: {response.status_code}")
                    return None, None
                data = response.json()

    if not data.get('uploadUrl'):
        print(f"    No uploadUrl in response. Cannot upload.")
        print(f"    Response: {json.dumps(data, indent=2)[:500]}")
        return None, None

    upload_url = data['uploadUrl']
    upload_details = data['uploadDetails']
    asset_id = data['id']

    # Step 2: Upload to S3 - use ALL form fields from uploadDetails exactly
    print(f"    uploadDetails keys: {list(upload_details.keys())}")
    content_type = upload_details.get('Content-Type', 'image/png')
    cache_control = upload_details.get('Cache-Control', 'max-age=31536000, must-revalidate')
    print(f"    Content-Type from policy: {content_type}")
    print(f"    Cache-Control from policy: {cache_control}")

    with open(filepath, 'rb') as f:
        files = {'file': (descriptive_name, f, content_type)}
        form_data = {}
        for key, value in upload_details.items():
            form_data[key] = value
        form_data['success_action_status'] = '201'

        upload_response = requests.post(upload_url, data=form_data, files=files)

        if upload_response.status_code not in [200, 201]:
            print(f"    S3 upload error: {upload_response.status_code}")
            print(f"    {upload_response.text[:500]}")
            return None, None

    # Construct CDN URL from the key in uploadDetails
    cdn_key = upload_details.get('key', f"{SITE_ID}/{asset_id}_{descriptive_name}")
    cdn_url = f"https://cdn.prod.website-files.com/{cdn_key}"
    print(f"    Uploaded: {cdn_url}")

    # Verify the new upload is live
    import time as _time
    _time.sleep(2)  # Give CDN a moment to propagate
    if verify_cdn_url(cdn_url):
        print(f"    Verified live!")
    else:
        print(f"    Warning: CDN not yet live (may need propagation time)")

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
    # Em dashes to spaced hyphens
    text = text.replace('—', ' - ')
    return text


def convert_table(block):
    """Convert markdown table to HTML table."""
    lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return ''

    html = '<table>'
    for i, line in enumerate(lines):
        # Skip separator line (contains ---)
        if re.match(r'^[\|\s\-:]+$', line):
            continue
        # Split cells, removing empty first/last from leading/trailing |
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]
        if not cells:
            continue
        tag = 'th' if i == 0 else 'td'
        row_html = ''.join(f'<{tag}>{convert_inline(c)}</{tag}>' for c in cells)
        html += f'<tr>{row_html}</tr>'

    html += '</table>'
    return html


def is_table_block(block):
    """Check if block is a markdown table."""
    lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return False
    return lines[0].startswith('|') and '---' in lines[1]


def is_metadata_line(line):
    """Check if line is metadata that should be stripped from content."""
    line = line.strip()
    patterns = [
        r'^\*\*Primary keyword:\*\*',
        r'^\*\*Secondary:\*\*',
        r'^\*\*Long-tail:\*\*',
        r'^\*\*Pop culture:\*\*',
        r'^\*\*Meta Title:\*\*',
        r'^\*\*Meta Description:\*\*',
        r'^\*\*URL:\*\*',
        r'^\*\*DRAFT v',
        r'^## SEO Notes',
    ]
    for pattern in patterns:
        if re.match(pattern, line):
            return True
    return False


def convert_block(block):
    """Convert a single paragraph block to HTML."""
    block = block.strip()
    if not block:
        return ''

    # Skip metadata
    if is_metadata_line(block):
        return ''

    # Skip SEO Notes section entirely
    if block.startswith('## SEO Notes'):
        return ''

    # Skip DRAFT header, byline, and rules
    if block == '---':
        return ''

    # Tables
    if is_table_block(block):
        return convert_table(block)

    # Headers
    if block.startswith('#### '):
        return f'<h4>{convert_inline(block[5:].strip("*"))}</h4>'
    elif block.startswith('### '):
        return f'<h3>{convert_inline(block[4:].strip("*"))}</h3>'
    elif block.startswith('## '):
        return f'<h2>{convert_inline(block[3:].strip("*"))}</h2>'
    elif block.startswith('# '):
        return ''  # Skip H1 - becomes post title

    # Video embed placeholder
    if block.strip() == '[VIDEO EMBED]':
        return '<p>[VIDEO EMBED]</p>'

    # Unordered list
    if block.startswith('- ') or block.startswith('* '):
        items = []
        for line in block.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
            elif line.startswith('* '):
                items.append(f'<li>{convert_inline(line[2:])}</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    # Ordered list
    if re.match(r'^\d+\.', block):
        items = []
        for line in block.split('\n'):
            match = re.match(r'^\d+\.\s*(.+)', line.strip())
            if match:
                items.append(f'<li>{convert_inline(match.group(1))}</li>')
        return '<ol>' + ''.join(items) + '</ol>'

    # Regular paragraph
    text = ' '.join(line.strip() for line in block.split('\n'))
    return f'<p>{convert_inline(text)}</p>'


def markdown_to_html(content):
    """Convert article markdown to HTML, stripping metadata."""
    # Remove everything after SEO Notes
    if '## SEO Notes' in content:
        content = content.split('## SEO Notes')[0]

    # Remove the H1 title line
    content = re.sub(r'^# .+\n', '', content)

    # Remove byline
    content = re.sub(r'^\*By .+\*\n', '', content, flags=re.MULTILINE)

    # Remove DRAFT marker
    content = re.sub(r'^\*\*DRAFT v\d+\*\*\n', '', content, flags=re.MULTILINE)

    # Split by blank lines
    blocks = re.split(r'\n\s*\n', content)
    html_blocks = [convert_block(b) for b in blocks]
    html = '\n\n'.join(b for b in html_blocks if b)

    return html


def make_figure(url, alt_text):
    """Create Webflow rich text figure HTML for an image."""
    return (
        f'<figure class="w-richtext-figure-type-image w-richtext-align-center" '
        f'data-rt-type="image" data-rt-align="center">'
        f'<div><img src="{url}" alt="{alt_text}" loading="lazy"></div>'
        f'</figure>'
    )


def insert_infographics(html, lebron_url, cbe_url):
    """Insert infographic images at the right spots in the article."""
    # Insert LeBron report card after the "LeBron James Is a Failure" H2
    lebron_figure = make_figure(lebron_url, "LeBron James student report card showing F grades on his basketball statistics")
    html = html.replace(
        '<h2>LeBron James Is a Failure</h2>',
        f'<h2>LeBron James Is a Failure</h2>\n\n{lebron_figure}'
    )

    # Insert CBE comparison after the comparison table
    cbe_figure = make_figure(cbe_url, "Traditional School vs Competency-Based Education comparison infographic")
    html = html.replace(
        '</table>',
        f'</table>\n\n{cbe_figure}',
        1  # Only first table
    )

    return html


def create_post(title, slug, summary, html_content, thumbnail_url, thumbnail_id):
    """Create blog post as draft in Webflow."""
    print("Creating blog post draft...")

    payload = {
        "isArchived": False,
        "isDraft": True,
        "fieldData": {
            "name": title,
            "slug": slug,
            "post-type": [BLOG_POST_TYPE],
            "summary": summary,
            "published-date": "2026-02-04T00:00:00.000Z",
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
        post_id = data.get('id')
        print(f"  Post created successfully!")
        print(f"  Post ID: {post_id}")
        print(f"  CMS: https://webflow.com/dashboard/sites/opened/cms/collections/{POSTS_COLLECTION}/items/{post_id}")
        return data
    else:
        print(f"  Error creating post: {response.status_code}")
        print(f"  {response.text[:500]}")
        return None


def main():
    os.chdir(SCRIPT_DIR)

    print("=" * 60)
    print("Publishing: What Is Competency-Based Education?")
    print("=" * 60)

    if not API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found in .env")
        return

    # Step 1: Upload images
    print("\n1. Uploading images...")
    import time
    ts = str(int(time.time()))
    thumb_url, thumb_id = upload_image(THUMBNAIL, f"cbe-thumb-{ts}.png")
    lebron_url, _ = upload_image(INFOGRAPHIC_LEBRON, f"cbe-lebron-{ts}.png")
    cbe_url, _ = upload_image(INFOGRAPHIC_CBE, f"cbe-compare-{ts}.png")

    if not thumb_url:
        print("ERROR: Thumbnail upload failed. Aborting.")
        return
    if not lebron_url or not cbe_url:
        print("WARNING: Infographic upload failed. Continuing without them.")

    # Step 2: Convert markdown to HTML
    print("\n2. Converting markdown to HTML...")
    with open(DRAFT, 'r') as f:
        markdown = f.read()

    html = markdown_to_html(markdown)

    # Insert infographics
    if lebron_url and cbe_url:
        html = insert_infographics(html, lebron_url, cbe_url)
        print(f"  Inserted 2 infographics into body")

    print(f"  Converted {len(markdown)} chars markdown -> {len(html)} chars HTML")

    # Save HTML for review
    preview_path = SCRIPT_DIR / "content-preview.html"
    with open(preview_path, 'w') as f:
        f.write(f'<html><head><style>body{{max-width:700px;margin:40px auto;font-family:Georgia,serif;line-height:1.6}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:8px;text-align:left}}th{{background:#f5f5f5}}img{{max-width:100%}}h2{{margin-top:2em}}</style></head><body>\n{html}\n</body></html>')
    print(f"  Saved preview to {preview_path}")

    # Step 3: Create post
    print("\n3. Creating Webflow draft...")
    result = create_post(
        title="What Is Competency-Based Education? Why School Was Never Designed for Your Kid",
        slug="competency-based-education",
        summary="Horace Mann imported a Prussian military model in 1837 and called it public school. LeBron James would fail by its grading standards. Here's the history and the better alternative.",
        html_content=html,
        thumbnail_url=thumb_url,
        thumbnail_id=thumb_id
    )

    if result:
        print("\n" + "=" * 60)
        print("SUCCESS! Post created as DRAFT in Webflow.")
        print("Next steps:")
        print("  1. Review in Webflow CMS dashboard")
        print("  2. Replace [VIDEO EMBED] with actual video embed")
        print("  3. Set author to Matt Bowman (if different from Charlie)")
        print("  4. Publish when ready")
        print("=" * 60)


if __name__ == '__main__':
    main()
