#!/usr/bin/env python3
"""Upload Horace Mann comedy sketch to YouTube via GetLate API."""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(Path(__file__).resolve().parents[4] / ".env")

API_KEY = os.getenv("GETLATE_API_KEY")
BASE_URL = "https://getlate.dev/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

YOUTUBE_ACCOUNT_ID = "6961354d4207e06f4ca849a4"
VIDEO_PATH = "/Users/charliedeist/Downloads/opened_horace_revised.mp4"

# Thumbnail - use the schoolhouse watercolor we uploaded to Webflow CDN
THUMBNAIL_URL = "https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/69839d7b61f7a7f954916e55_cbe-thumbnail-schoolhouse.png"

VIDEO_TITLE = "Horace Mann Pitches Public School (Nate Bargatze SNL Parody)"

VIDEO_DESCRIPTION = """In 1837, Horace Mann returned from Prussia with an idea: educate American children like you'd train soldiers. Sort them by age. Grade them like meat. Ring bells. Punish anyone who moves too slowly.

We made a comedy sketch about it - inspired by Nate Bargatze's George Washington SNL skit.

The punchline? Almost nothing has changed.

Filmed at a real one-room schoolhouse (Taylorsville-Bennion Heritage Center) with a real punishment chart still on the wall. Written by Matt Bowman, founder of OpenEd.

Read the full article: https://opened.co/blog/competency-based-education

RESOURCES:
Get the free Open Education toolkit: https://opened.co/book
Learn more about open education: https://opened.co
Listen to the OpenEd podcast: https://opened.co/podcast

CONNECT:
Twitter: @OpenEdOfficial
LinkedIn: /company/opened

#NateBargatze #SNL #SNLParody #Education #HoraceMann #Homeschool #OpenEducation #SchoolChoice #EducationReform #CompetencyBasedEducation #PublicSchool #Comedy #Sketch"""


def get_presigned_url(filename, content_type, size):
    """Get a presigned URL for uploading to GetLate."""
    print("Requesting presigned URL...")
    response = requests.post(
        f"{BASE_URL}/media/presign",
        headers=HEADERS,
        json={"filename": filename, "contentType": content_type, "size": size}
    )
    if response.status_code not in [200, 201]:
        print(f"Error: {response.status_code} - {response.text[:500]}")
        return None
    data = response.json()
    print(f"  Got presigned URL")
    return data


def upload_video(file_path, presign_data):
    """Upload video to GetLate's presigned URL with progress."""
    upload_url = presign_data.get('uploadUrl')
    if not upload_url:
        print("No upload URL in presign response")
        return False

    file_size = os.path.getsize(file_path)
    print(f"Uploading {file_size / (1024*1024):.0f} MB to GetLate...")

    try:
        with open(file_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": "video/mp4"}
            )
            response.raise_for_status()
        print("  Upload complete!")
        return True
    except Exception as e:
        print(f"  Upload failed: {e}")
        return False


def create_youtube_post(video_url, thumbnail_url=None):
    """Create YouTube post via GetLate."""
    print("Creating YouTube post...")

    payload = {
        "content": VIDEO_DESCRIPTION,
        "title": VIDEO_TITLE,
        "mediaItems": [
            {
                "type": "video",
                "url": video_url
            }
        ],
        "platforms": [
            {
                "platform": "youtube",
                "accountId": YOUTUBE_ACCOUNT_ID
            }
        ],
        "publishNow": False
    }

    if thumbnail_url:
        payload["mediaItems"][0]["thumbnail"] = thumbnail_url

    response = requests.post(
        f"{BASE_URL}/posts",
        headers=HEADERS,
        json=payload
    )

    if response.status_code in [200, 201, 202]:
        data = response.json()
        post_id = data.get('_id', data.get('id', 'unknown'))
        print(f"  Post created! ID: {post_id}")
        return data
    else:
        print(f"  Error: {response.status_code}")
        print(f"  {response.text[:500]}")
        return None


def main():
    print("=" * 60)
    print("YouTube Upload: Horace Mann Comedy Sketch")
    print("=" * 60)

    if not API_KEY:
        print("ERROR: GETLATE_API_KEY not found in .env")
        return

    if not os.path.exists(VIDEO_PATH):
        print(f"ERROR: Video not found at {VIDEO_PATH}")
        return

    file_size = os.path.getsize(VIDEO_PATH)
    print(f"Video: {VIDEO_PATH}")
    print(f"Size: {file_size / (1024*1024*1024):.2f} GB")
    print(f"Title: {VIDEO_TITLE}")

    # Step 1: Get presigned URL
    print(f"\n1. Getting presigned URL...")
    presign_data = get_presigned_url(
        filename="horace-mann-sketch.mp4",
        content_type="video/mp4",
        size=file_size
    )

    if not presign_data:
        print("Failed to get presigned URL. Aborting.")
        return

    public_url = presign_data.get('publicUrl')
    print(f"  Public URL: {public_url}")

    # Step 2: Upload video
    print(f"\n2. Uploading video (this will take a while for 2GB)...")
    if not upload_video(VIDEO_PATH, presign_data):
        print("Upload failed. Aborting.")
        return

    # Step 3: Create YouTube post
    print(f"\n3. Creating YouTube post as draft...")
    result = create_youtube_post(public_url, THUMBNAIL_URL)

    if result:
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print(f"Title: {VIDEO_TITLE}")
        print(f"Status: Draft (not published)")
        print(f"Dashboard: https://getlate.dev")
        print("Next: Review in GetLate dashboard, then publish")
        print("=" * 60)
    else:
        print("\nFailed to create YouTube post.")


if __name__ == '__main__':
    main()
