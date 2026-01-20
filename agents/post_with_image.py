#!/usr/bin/env python3
"""Post to social platforms with optional image via Get Late API.

Usage:
    python post_with_image.py --platform linkedin --content "Post text" --image path/to/image.png
    python post_with_image.py --platform twitter --content "Tweet text"
    python post_with_image.py --platform linkedin,twitter --content "Cross-post" --image image.png
"""

import argparse
import mimetypes
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

api_key = os.getenv("GETLATE_API_KEY")
if not api_key:
    print("Error: GETLATE_API_KEY not found in .env")
    sys.exit(1)

base_url = "https://getlate.dev/api/v1"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def get_accounts():
    """Fetch all connected accounts."""
    response = requests.get(f"{base_url}/accounts", headers=headers)
    return response.json().get("accounts", [])


def find_account(accounts, platform):
    """Find account by platform name."""
    for acc in accounts:
        if isinstance(acc, dict) and acc.get("platform") == platform:
            return acc
    return None


def upload_image(image_path):
    """Upload image and return public URL."""
    path = Path(image_path)
    if not path.exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    # Determine content type
    content_type, _ = mimetypes.guess_type(str(path))
    if not content_type:
        content_type = "image/png"  # Default fallback

    print(f"Uploading {path.name} ({content_type})...")

    # 1. Get presigned URL
    presign_response = requests.post(
        f"{base_url}/media/presign",
        headers=headers,
        json={"filename": path.name, "contentType": content_type},
    )

    if presign_response.status_code != 200:
        print(f"Error getting presigned URL: {presign_response.text}")
        sys.exit(1)

    presign_data = presign_response.json()
    upload_url = presign_data["uploadUrl"]
    public_url = presign_data["publicUrl"]

    # 2. Upload directly to presigned URL
    with open(path, "rb") as f:
        upload_response = requests.put(
            upload_url, data=f, headers={"Content-Type": content_type}
        )

    if upload_response.status_code not in (200, 201):
        print(f"Error uploading image: {upload_response.text}")
        sys.exit(1)

    print(f"Uploaded: {public_url}")
    return public_url


def post_content(platforms, content, media_url=None):
    """Post content to specified platforms."""
    accounts = get_accounts()

    platform_configs = []
    for platform in platforms:
        account = find_account(accounts, platform)
        if not account:
            print(f"Warning: No {platform} account found, skipping")
            continue
        account_id = account.get("_id") or account.get("id")
        platform_configs.append({"platform": platform, "accountId": account_id})
        print(f"Posting to: {account.get('displayName', platform)}")

    if not platform_configs:
        print("Error: No valid platforms found")
        sys.exit(1)

    post_data = {
        "platforms": platform_configs,
        "content": content,
        "publishNow": True,
    }

    if media_url:
        post_data["mediaItems"] = [{"url": media_url}]

    response = requests.post(f"{base_url}/posts", headers=headers, json=post_data)
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 201:
        data = response.json()
        post = data.get("post", {})
        for p in post.get("platforms", []):
            url = p.get("platformPostUrl", "")
            platform_name = p.get("platform", "Unknown")
            print(f"{platform_name}: {url}")
    else:
        print(f"Error: {response.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Post to social media with optional image"
    )
    parser.add_argument(
        "--platform",
        "-p",
        required=True,
        help="Platform(s) to post to (comma-separated: linkedin,twitter)",
    )
    parser.add_argument("--content", "-c", required=True, help="Post content text")
    parser.add_argument("--image", "-i", help="Path to image file (optional)")
    parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation prompt"
    )

    args = parser.parse_args()

    platforms = [p.strip() for p in args.platform.split(",")]
    content = args.content

    print(f"\n{'=' * 60}")
    print(f"Platforms: {', '.join(platforms)}")
    print(f"Content:\n{content}")
    if args.image:
        print(f"Image: {args.image}")
    print(f"{'=' * 60}\n")

    if not args.yes:
        confirm = input("Post this? (y/n): ")
        if confirm.lower() != "y":
            print("Cancelled.")
            sys.exit(0)

    media_url = None
    if args.image:
        media_url = upload_image(args.image)

    post_content(platforms, content, media_url)


if __name__ == "__main__":
    main()
