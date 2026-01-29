#!/usr/bin/env python3
"""Upload thumbnails and update existing draft posts."""

import os
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

SITE_ID = "67c7406fc9e6913d1b92e341"
POSTS_COLLECTION = "6805bf729a7b33423cc8a08c"
BASE_PATH = Path(__file__).parent

# Post IDs from the batch upload
POSTS = [
    {
        "post_id": "697bbf1e05a9f64dbf85e913",
        "name": "Waldorf vs Montessori",
        "thumbnail_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Waldorf vs Montessori/thumbnail-final_20260128_213719_edit_pro.png",
    },
    {
        "post_id": "697bbf1fc80c845945e64a37",
        "name": "Montessori vs Reggio Emilia",
        "thumbnail_path": BASE_PATH / "Open Education Hub/Deep Dive Studio/Montessori vs Reggio Emilia/thumbnail_20260129_120350_gen_pro.png",
    },
    {
        "post_id": "697bbf203c348338e9a993e7",
        "name": "Khan Academy vs IXL",
        "thumbnail_path": BASE_PATH / "Versus/khan-academy-vs-ixl/thumbnail_20260129_112654_gen_pro.png",
    },
    {
        "post_id": "697bbf213a058d27011d1027",
        "name": "Saxon Math vs Math-U-See",
        "thumbnail_path": BASE_PATH / "Versus/saxon-vs-math-u-see/thumbnail_20260129_112720_gen_pro.png",
    },
    {
        "post_id": "697bbf23681286546825ecdc",
        "name": "IXL vs Exact Path",
        "thumbnail_path": BASE_PATH / "Versus/ixl-vs-exact-path/thumbnail_20260129_112742_gen_pro.png",
    },
]


def upload_image(image_path):
    """Upload image to Webflow CDN. Returns (asset_id, cdn_url)."""
    with open(image_path, 'rb') as f:
        file_data = f.read()
    file_hash = hashlib.md5(file_data).hexdigest()

    # Step 1: Get presigned URL
    resp = requests.post(
        f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "fileName": image_path.name,
            "fileHash": file_hash
        }
    )

    if resp.status_code not in [200, 201, 202]:
        print(f"  Error getting presigned URL: {resp.status_code}")
        return None, None

    data = resp.json()
    asset_id = data.get("id")
    upload_url = data.get("uploadUrl")
    upload_details = data.get("uploadDetails", {})

    if not upload_url:
        # Asset may already exist
        cdn_url = f"https://cdn.prod.website-files.com/{SITE_ID}/{asset_id}_{image_path.name}"
        print(f"  Asset already exists: {asset_id}")
        return asset_id, cdn_url

    # Step 2: Upload to S3
    print(f"  Uploading to S3...")
    files = {"file": (image_path.name, file_data, "image/png")}
    form_data = {
        "acl": upload_details.get("acl"),
        "bucket": upload_details.get("bucket"),
        "X-Amz-Algorithm": upload_details.get("X-Amz-Algorithm"),
        "X-Amz-Credential": upload_details.get("X-Amz-Credential"),
        "X-Amz-Date": upload_details.get("X-Amz-Date"),
        "key": upload_details.get("key"),
        "Policy": upload_details.get("Policy"),
        "X-Amz-Signature": upload_details.get("X-Amz-Signature"),
        "success_action_status": "201",
        "Content-Type": "image/png",
        "Cache-Control": "max-age=31536000, must-revalidate"
    }

    s3_resp = requests.post(upload_url, data=form_data, files=files)

    if s3_resp.status_code != 201:
        print(f"  S3 upload failed: {s3_resp.status_code}")
        print(f"  {s3_resp.text[:200]}")
        return None, None

    cdn_url = f"https://cdn.prod.website-files.com/{SITE_ID}/{asset_id}_{image_path.name}"
    return asset_id, cdn_url


def update_post_thumbnail(post_id, asset_id, cdn_url):
    """Update an existing post with a thumbnail."""
    resp = requests.patch(
        f"https://api.webflow.com/v2/collections/{POSTS_COLLECTION}/items/{post_id}",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "fieldData": {
                "thumbnail": {
                    "fileId": asset_id,
                    "url": cdn_url
                }
            }
        }
    )
    return resp


def main():
    print("Updating thumbnails for 5 draft posts...")
    print("=" * 50)

    for post in POSTS:
        print(f"\n{post['name']}")
        print("-" * 30)

        if not post["thumbnail_path"].exists():
            print(f"  ERROR: Thumbnail not found")
            continue

        # Upload thumbnail
        print(f"  Uploading thumbnail...")
        asset_id, cdn_url = upload_image(post["thumbnail_path"])

        if not asset_id:
            print(f"  Failed to upload thumbnail")
            continue

        print(f"  Asset ID: {asset_id}")

        # Update post
        print(f"  Updating post...")
        resp = update_post_thumbnail(post["post_id"], asset_id, cdn_url)

        if resp.status_code in [200, 201, 202]:
            print(f"  SUCCESS!")
        else:
            print(f"  FAILED: {resp.status_code}")
            print(f"  {resp.text[:200]}")

    print("\n" + "=" * 50)
    print("Done! Check Webflow CMS to verify thumbnails.")


if __name__ == "__main__":
    main()
