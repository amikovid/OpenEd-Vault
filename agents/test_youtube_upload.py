#!/usr/bin/env python3
"""
Test script for uploading a video to YouTube via GetLate API
Downloads from Descript and uploads to GetLate → YouTube
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment
parent_dir = Path(__file__).parent.parent
load_dotenv(parent_dir / '.env')

API_KEY = os.getenv('GETLATE_API_KEY')
BASE_URL = "https://getlate.dev/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Video source
DESCRIPT_VIDEO_URL = "https://storage.googleapis.com/production-273614-media-export/6a4b93a3-fbd1-48b6-ac66-ca57ba6bda59/original.mp4"
THUMBNAIL_URL = "https://d1d3n03t5zntha.cloudfront.net/6a4b93a3-fbd1-48b6-ac66-ca57ba6bda59/media_stream-1126fab4ae3346c69a07bdd87c6181d8.jpg"
VIDEO_TITLE = "Joshua Millburn on Decluttering Beyond Possessions | Open Ed Podcast"

# YouTube account ID
YOUTUBE_ACCOUNT_ID = "6961354d4207e06f4ca849a4"


def download_video(url: str, output_path: str) -> bool:
    """Download video with progress indicator"""
    print(f"Downloading video from Descript...")
    print(f"URL: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        print(f"File size: {total_size / (1024*1024*1024):.2f} GB")

        downloaded = 0
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192*1024):  # 8MB chunks
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    pct = (downloaded / total_size) * 100 if total_size else 0
                    print(f"\rDownloaded: {downloaded / (1024*1024):.1f} MB ({pct:.1f}%)", end='', flush=True)

        print(f"\nDownload complete: {output_path}")
        return True

    except Exception as e:
        print(f"\nDownload failed: {e}")
        return False


def get_presigned_url(filename: str, content_type: str, size: int) -> dict:
    """Get a presigned URL for uploading to GetLate"""
    print(f"\nRequesting presigned URL from GetLate...")

    payload = {
        "filename": filename,
        "contentType": content_type,
        "size": size
    }

    try:
        response = requests.post(
            f"{BASE_URL}/media/presign",
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print(f"Got presigned URL")
        return data

    except Exception as e:
        print(f"Failed to get presigned URL: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None


def upload_to_getlate(file_path: str, presign_data: dict) -> bool:
    """Upload file to GetLate's presigned URL"""
    print(f"\nUploading to GetLate...")

    upload_url = presign_data.get('uploadUrl')
    if not upload_url:
        print("No upload URL in presign response")
        return False

    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size / (1024*1024*1024):.2f} GB")

    try:
        with open(file_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": "video/mp4"}
            )
            response.raise_for_status()

        print("Upload complete!")
        return True

    except Exception as e:
        print(f"Upload failed: {e}")
        return False


def create_youtube_post(video_url: str, thumbnail_url: str = None) -> dict:
    """Create a YouTube post via GetLate API"""
    print(f"\nCreating YouTube post...")

    payload = {
        "content": """Joshua Fields Millburn from The Minimalists joins us to discuss decluttering beyond physical possessions.

In this episode:
- Relationship clutter and toxic connections
- Career clutter and unfulfilling work
- Education clutter and learning differently
- Emotional clutter and past baggage

Joshua shares his personal journey growing up in poverty, discovering his dyslexia, and how these experiences shaped his minimalist philosophy.

RESOURCES:
📖 Full episode: https://opened.com/podcast
🌐 Website: https://opened.com
📧 Newsletter: https://opened.com/newsletter

CONNECT:
Twitter: @OpenEdOfficial
LinkedIn: /company/opened

#OpenEd #Minimalism #Education #Podcast #JoshuaMillburn #TheMinimalists""",
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
        "publishNow": False  # Set to True to publish immediately
    }

    if thumbnail_url:
        payload["mediaItems"][0]["thumbnail"] = thumbnail_url

    try:
        response = requests.post(
            f"{BASE_URL}/posts",
            headers=HEADERS,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print(f"Post created successfully!")
        print(f"Post ID: {data.get('_id', data.get('id', 'unknown'))}")
        return data

    except Exception as e:
        print(f"Failed to create post: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None


def main():
    print("=" * 60)
    print("GetLate YouTube Upload Test")
    print("=" * 60)

    if not API_KEY:
        print("ERROR: GETLATE_API_KEY not found in .env")
        return

    # Step 1: Download video
    video_path = "/tmp/joshua_millburn_podcast.mp4"

    if os.path.exists(video_path):
        print(f"Video already downloaded: {video_path}")
        file_size = os.path.getsize(video_path)
        print(f"File size: {file_size / (1024*1024*1024):.2f} GB")
    else:
        if not download_video(DESCRIPT_VIDEO_URL, video_path):
            print("Failed to download video")
            return
        file_size = os.path.getsize(video_path)

    # Step 2: Get presigned URL
    presign_data = get_presigned_url(
        filename="joshua_millburn_podcast.mp4",
        content_type="video/mp4",
        size=file_size
    )

    if not presign_data:
        print("Failed to get presigned URL")
        return

    print(f"Public URL will be: {presign_data.get('publicUrl', 'unknown')}")

    # Step 3: Upload to GetLate
    if not upload_to_getlate(video_path, presign_data):
        print("Failed to upload video")
        return

    # Step 4: Create YouTube post
    public_url = presign_data.get('publicUrl')
    result = create_youtube_post(public_url, THUMBNAIL_URL)

    if result:
        print("\n" + "=" * 60)
        print("SUCCESS! Video uploaded and YouTube post created.")
        print("Check your GetLate dashboard: https://getlate.dev")
        print("=" * 60)
    else:
        print("\nFailed to create YouTube post")

    # Cleanup option
    # os.remove(video_path)


if __name__ == "__main__":
    main()
