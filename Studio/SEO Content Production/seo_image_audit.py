#!/usr/bin/env python3
"""
SEO Image Audit - Fetch all blog posts and audit images for SEO issues.

Checks:
- Missing alt text
- Missing width/height attributes (CLS)
- Hero image with loading="lazy" instead of eager (LCP)
- Timestamp-based filenames (no SEO value)
- Format mismatch (JPEG data in .png extension)

Output: CSV report at seo-audit-report.csv
"""

import csv
import os
import re
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load API key
_script_dir = Path(__file__).resolve().parent
_vault_root = _script_dir.parents[1]  # OpenEd Vault/
load_dotenv(_vault_root / ".env")
API_KEY = os.getenv("WEBFLOW_API_KEY")

SITE_ID = "67c7406fc9e6913d1b92e341"
POSTS_COLLECTION = "6805bf729a7b33423cc8a08c"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Patterns
TIMESTAMP_PATTERN = re.compile(r'\d{8}_\d{6}')
IMG_TAG_PATTERN = re.compile(r'<img\s+([^>]+)>', re.IGNORECASE)
ATTR_PATTERN = re.compile(r'(\w[\w-]*)=["\']([^"\']*)["\']')


def fetch_all_posts():
    """Fetch all posts from Webflow CMS with pagination."""
    all_items = []
    offset = 0
    limit = 100

    while True:
        url = f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items?limit={limit}&offset={offset}"
        resp = requests.get(url, headers=HEADERS)

        if resp.status_code not in [200, 201, 202]:
            print(f"Error fetching posts: {resp.status_code}")
            print(resp.text[:300])
            break

        data = resp.json()
        items = data.get("items", [])
        all_items.extend(items)

        print(f"  Fetched {len(items)} posts (total: {len(all_items)})")

        if len(items) < limit:
            break

        offset += limit
        time.sleep(0.5)

    return all_items


def parse_img_attrs(img_tag_content):
    """Parse attributes from an img tag content string."""
    attrs = {}
    for match in ATTR_PATTERN.finditer(img_tag_content):
        attrs[match.group(1).lower()] = match.group(2)
    return attrs


def audit_post(post):
    """Audit a single post for image SEO issues. Returns list of issue dicts."""
    issues = []
    field_data = post.get("fieldData", {})
    slug = field_data.get("slug", "unknown")
    post_id = post.get("id", "unknown")
    name = field_data.get("name", "Untitled")
    content = field_data.get("content", "")
    summary = field_data.get("summary", "")
    thumbnail = field_data.get("thumbnail", {})

    # Check meta description length
    if summary:
        summary_len = len(summary)
        if summary_len < 120:
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "meta_description_short",
                "image_src": "",
                "detail": f"Summary only {summary_len} chars (aim for 120-160)",
                "current_value": summary[:80] + "..." if len(summary) > 80 else summary,
            })
        elif summary_len > 160:
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "meta_description_long",
                "image_src": "",
                "detail": f"Summary is {summary_len} chars (aim for 120-160, will be truncated)",
                "current_value": summary[:80] + "...",
            })
    else:
        issues.append({
            "post_id": post_id,
            "slug": slug,
            "name": name,
            "issue_type": "meta_description_missing",
            "image_src": "",
            "detail": "No summary/meta description",
            "current_value": "",
        })

    # Check thumbnail
    thumb_url = thumbnail.get("url", "") if isinstance(thumbnail, dict) else ""
    if not thumb_url:
        issues.append({
            "post_id": post_id,
            "slug": slug,
            "name": name,
            "issue_type": "thumbnail_missing",
            "image_src": "",
            "detail": "No thumbnail image set",
            "current_value": "",
        })
    elif thumb_url:
        # Check for timestamp filename
        filename = thumb_url.split("/")[-1] if "/" in thumb_url else thumb_url
        if TIMESTAMP_PATTERN.search(filename):
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "thumbnail_timestamp_name",
                "image_src": thumb_url,
                "detail": f"Timestamp-based filename: {filename}",
                "current_value": filename,
            })
        # Check for .png that might be JPEG (can't verify without downloading)
        if filename.endswith('.png'):
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "thumbnail_possible_format_mismatch",
                "image_src": thumb_url,
                "detail": "PNG extension - may contain JPEG data (common Gemini issue)",
                "current_value": filename,
            })

    # Parse content HTML for <img> tags
    if not content:
        return issues

    img_matches = list(IMG_TAG_PATTERN.finditer(content))

    for i, match in enumerate(img_matches):
        attrs = parse_img_attrs(match.group(1))
        src = attrs.get("src", "")
        alt = attrs.get("alt", "")
        loading = attrs.get("loading", "")
        width = attrs.get("width", "")
        height = attrs.get("height", "")
        filename = src.split("/")[-1] if "/" in src else src

        # Missing alt text
        if not alt or not alt.strip():
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "missing_alt_text",
                "image_src": src[:100],
                "detail": f"Image #{i+1} has no alt text",
                "current_value": "",
            })

        # Missing dimensions
        if not width or not height:
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "missing_dimensions",
                "image_src": src[:100],
                "detail": f"Image #{i+1} missing width/height (causes CLS)",
                "current_value": f"w={width} h={height}",
            })

        # Hero image (first image) should be eager, not lazy
        if i == 0 and loading == "lazy":
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "hero_lazy_loading",
                "image_src": src[:100],
                "detail": "First image uses loading='lazy' (should be eager for LCP)",
                "current_value": f"loading={loading}",
            })

        # Timestamp filename
        if TIMESTAMP_PATTERN.search(filename):
            issues.append({
                "post_id": post_id,
                "slug": slug,
                "name": name,
                "issue_type": "timestamp_filename",
                "image_src": src[:100],
                "detail": f"Image #{i+1} has timestamp-based filename",
                "current_value": filename,
            })

    return issues


def main():
    if not API_KEY:
        print("ERROR: WEBFLOW_API_KEY not found")
        sys.exit(1)

    print("SEO Image Audit")
    print("=" * 60)

    # Fetch all posts
    print("\nFetching all blog posts...")
    posts = fetch_all_posts()
    print(f"\nTotal posts: {len(posts)}")

    # Audit each post
    print("\nAuditing posts...")
    all_issues = []
    for post in posts:
        issues = audit_post(post)
        all_issues.extend(issues)

    # Write CSV report
    output_path = _script_dir / "seo-audit-report.csv"
    fieldnames = ["post_id", "slug", "name", "issue_type", "image_src", "detail", "current_value"]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_issues)

    print(f"\nReport saved: {output_path}")
    print(f"Total issues found: {len(all_issues)}")

    # Summary by issue type
    print("\n" + "=" * 60)
    print("SUMMARY BY ISSUE TYPE")
    print("=" * 60)
    type_counts = {}
    for issue in all_issues:
        t = issue["issue_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    for issue_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {issue_type:40s} {count:4d}")

    # Posts with no issues
    posts_with_issues = set(i["slug"] for i in all_issues)
    clean_posts = [p for p in posts if p.get("fieldData", {}).get("slug", "") not in posts_with_issues]
    print(f"\n  Posts with zero issues: {len(clean_posts)}")
    print(f"  Posts with issues:     {len(posts_with_issues)}")


if __name__ == "__main__":
    main()
