"""
YouTube Analytics Data Integration

Fetches channel stats, video performance, and engagement data from YouTube Data API v3.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from googleapiclient.discovery import build
from google.oauth2 import service_account

class YouTubeAnalytics:
    """YouTube Data API v3 client for channel and video analytics"""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize YouTube client

        Args:
            credentials_path: Path to credentials JSON (defaults to env var YOUTUBE_CREDENTIALS_PATH)
        """
        credentials_path = credentials_path or os.getenv('YOUTUBE_CREDENTIALS_PATH')

        if not credentials_path or not os.path.exists(credentials_path):
            raise ValueError(f"Credentials file not found: {credentials_path}")

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/youtube.readonly']
        )

        self.youtube = build('youtube', 'v3', credentials=credentials)

    def get_channel_stats(self, channel_id: str) -> Dict[str, Any]:
        """
        Get channel statistics

        Args:
            channel_id: YouTube channel ID (e.g., UCxxxxxx)

        Returns:
            Dict with channel stats
        """
        request = self.youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel_id
        )
        response = request.execute()

        if not response.get('items'):
            return {'error': f'Channel not found: {channel_id}'}

        channel = response['items'][0]
        stats = channel['statistics']
        snippet = channel['snippet']

        return {
            'channel_id': channel_id,
            'title': snippet['title'],
            'description': snippet.get('description', '')[:200],
            'custom_url': snippet.get('customUrl', ''),
            'published_at': snippet['publishedAt'],
            'subscribers': int(stats.get('subscriberCount', 0)),
            'total_views': int(stats.get('viewCount', 0)),
            'video_count': int(stats.get('videoCount', 0)),
            'hidden_subscriber_count': stats.get('hiddenSubscriberCount', False),
        }

    def get_channel_by_username(self, username: str) -> Dict[str, Any]:
        """
        Get channel by username or handle

        Args:
            username: YouTube username or @handle

        Returns:
            Dict with channel stats
        """
        # Try forUsername first
        request = self.youtube.channels().list(
            part='snippet,statistics',
            forUsername=username.lstrip('@')
        )
        response = request.execute()

        if response.get('items'):
            channel_id = response['items'][0]['id']
            return self.get_channel_stats(channel_id)

        # Try search if forUsername doesn't work
        request = self.youtube.search().list(
            part='snippet',
            q=username,
            type='channel',
            maxResults=1
        )
        response = request.execute()

        if response.get('items'):
            channel_id = response['items'][0]['snippet']['channelId']
            return self.get_channel_stats(channel_id)

        return {'error': f'Channel not found: {username}'}

    def get_recent_videos(
        self,
        channel_id: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent videos from a channel

        Args:
            channel_id: YouTube channel ID
            max_results: Number of videos to return

        Returns:
            List of video dicts with stats
        """
        # First get uploads playlist ID
        request = self.youtube.channels().list(
            part='contentDetails',
            id=channel_id
        )
        response = request.execute()

        if not response.get('items'):
            return []

        uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Get videos from uploads playlist
        request = self.youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=uploads_id,
            maxResults=max_results
        )
        response = request.execute()

        videos = []
        video_ids = []

        for item in response.get('items', []):
            video_id = item['contentDetails']['videoId']
            video_ids.append(video_id)
            videos.append({
                'video_id': video_id,
                'title': item['snippet']['title'],
                'description': item['snippet'].get('description', '')[:200],
                'published_at': item['snippet']['publishedAt'],
                'thumbnail': item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
            })

        # Get stats for all videos in one call
        if video_ids:
            request = self.youtube.videos().list(
                part='statistics,contentDetails',
                id=','.join(video_ids)
            )
            stats_response = request.execute()

            stats_lookup = {}
            for item in stats_response.get('items', []):
                stats = item['statistics']
                stats_lookup[item['id']] = {
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'duration': item['contentDetails'].get('duration', ''),
                }

            for video in videos:
                video.update(stats_lookup.get(video['video_id'], {}))

        return videos

    def get_video_stats(self, video_id: str) -> Dict[str, Any]:
        """
        Get detailed stats for a single video

        Args:
            video_id: YouTube video ID

        Returns:
            Dict with video stats
        """
        request = self.youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        )
        response = request.execute()

        if not response.get('items'):
            return {'error': f'Video not found: {video_id}'}

        video = response['items'][0]
        stats = video['statistics']
        snippet = video['snippet']

        return {
            'video_id': video_id,
            'title': snippet['title'],
            'description': snippet.get('description', '')[:500],
            'channel_title': snippet['channelTitle'],
            'published_at': snippet['publishedAt'],
            'duration': video['contentDetails'].get('duration', ''),
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0)),
            'tags': snippet.get('tags', [])[:10],
        }

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = 'relevance'
    ) -> List[Dict[str, Any]]:
        """
        Search for videos

        Args:
            query: Search query
            max_results: Number of results
            order: Sort order (relevance, date, viewCount, rating)

        Returns:
            List of video dicts
        """
        request = self.youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=max_results,
            order=order
        )
        response = request.execute()

        videos = []
        video_ids = []

        for item in response.get('items', []):
            video_id = item['id']['videoId']
            video_ids.append(video_id)
            videos.append({
                'video_id': video_id,
                'title': item['snippet']['title'],
                'channel_title': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'description': item['snippet'].get('description', '')[:200],
            })

        # Get stats for all videos
        if video_ids:
            request = self.youtube.videos().list(
                part='statistics',
                id=','.join(video_ids)
            )
            stats_response = request.execute()

            stats_lookup = {}
            for item in stats_response.get('items', []):
                stats = item['statistics']
                stats_lookup[item['id']] = {
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                }

            for video in videos:
                video.update(stats_lookup.get(video['video_id'], {}))

        return videos


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    yt = YouTubeAnalytics()

    # Replace with actual OpenEd channel ID
    channel_id = os.getenv('YOUTUBE_CHANNEL_ID')

    if channel_id:
        print("Channel Stats:")
        stats = yt.get_channel_stats(channel_id)
        print(f"  Title: {stats.get('title')}")
        print(f"  Subscribers: {stats.get('subscribers'):,}")
        print(f"  Total Views: {stats.get('total_views'):,}")
        print(f"  Videos: {stats.get('video_count')}")
        print()

        print("Recent Videos:")
        videos = yt.get_recent_videos(channel_id, max_results=5)
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video['title']}")
            print(f"   Views: {video.get('views', 0):,} | Likes: {video.get('likes', 0):,}")
            print()
    else:
        print("Set YOUTUBE_CHANNEL_ID in .env to test")
