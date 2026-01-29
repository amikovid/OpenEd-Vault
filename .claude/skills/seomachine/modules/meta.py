"""
Meta (Facebook + Instagram) Analytics Integration

Fetches page stats, post performance, and audience insights from Meta Graph API.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


class MetaAnalytics:
    """Meta Graph API client for Facebook and Instagram analytics"""

    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(
        self,
        access_token: Optional[str] = None,
        page_id: Optional[str] = None,
        instagram_id: Optional[str] = None
    ):
        """
        Initialize Meta client

        Args:
            access_token: Meta access token (defaults to env var META_ACCESS_TOKEN)
            page_id: Facebook Page ID (defaults to env var META_PAGE_ID)
            instagram_id: Instagram Business Account ID (defaults to env var META_INSTAGRAM_ID)
        """
        self.access_token = access_token or os.getenv('META_ACCESS_TOKEN')
        self.page_id = page_id or os.getenv('META_PAGE_ID')
        self.instagram_id = instagram_id or os.getenv('META_INSTAGRAM_ID')

        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN must be provided or set in environment")

    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Graph API"""
        params = params or {}
        params['access_token'] = self.access_token

        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            error = response.json().get('error', {})
            raise Exception(f"Meta API error: {error.get('message', response.text)}")

        return response.json()

    # ========== FACEBOOK PAGE ==========

    def get_page_info(self, page_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Facebook Page basic info and follower count

        Args:
            page_id: Facebook Page ID (uses default if not provided)

        Returns:
            Dict with page info
        """
        page_id = page_id or self.page_id
        if not page_id:
            raise ValueError("page_id required")

        data = self._request(
            page_id,
            params={'fields': 'name,username,followers_count,fan_count,link,about,category'}
        )

        return {
            'page_id': page_id,
            'name': data.get('name'),
            'username': data.get('username'),
            'followers': data.get('followers_count', 0),
            'likes': data.get('fan_count', 0),
            'link': data.get('link'),
            'about': data.get('about', '')[:200],
            'category': data.get('category'),
        }

    def get_page_insights(
        self,
        page_id: Optional[str] = None,
        period: str = 'day',
        days: int = 28
    ) -> Dict[str, Any]:
        """
        Get Facebook Page insights (reach, engagement, etc.)

        Args:
            page_id: Facebook Page ID
            period: 'day', 'week', 'days_28'
            days: Number of days to look back

        Returns:
            Dict with insights data
        """
        page_id = page_id or self.page_id
        if not page_id:
            raise ValueError("page_id required")

        since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        until = datetime.now().strftime('%Y-%m-%d')

        metrics = [
            'page_impressions',
            'page_impressions_unique',
            'page_engaged_users',
            'page_post_engagements',
            'page_fans',
            'page_fan_adds',
            'page_views_total',
        ]

        data = self._request(
            f"{page_id}/insights",
            params={
                'metric': ','.join(metrics),
                'period': period,
                'since': since,
                'until': until,
            }
        )

        results = {}
        for item in data.get('data', []):
            metric_name = item['name']
            values = item.get('values', [])
            if values:
                # Get the most recent value
                results[metric_name] = values[-1].get('value', 0)

        return {
            'page_id': page_id,
            'period': period,
            'days': days,
            'impressions': results.get('page_impressions', 0),
            'reach': results.get('page_impressions_unique', 0),
            'engaged_users': results.get('page_engaged_users', 0),
            'post_engagements': results.get('page_post_engagements', 0),
            'total_fans': results.get('page_fans', 0),
            'new_fans': results.get('page_fan_adds', 0),
            'page_views': results.get('page_views_total', 0),
        }

    def get_recent_posts(
        self,
        page_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent Facebook posts with engagement metrics

        Args:
            page_id: Facebook Page ID
            limit: Number of posts to return

        Returns:
            List of post dicts
        """
        page_id = page_id or self.page_id
        if not page_id:
            raise ValueError("page_id required")

        data = self._request(
            f"{page_id}/posts",
            params={
                'fields': 'id,message,created_time,shares,permalink_url,'
                          'insights.metric(post_impressions,post_engagements,'
                          'post_reactions_by_type_total)',
                'limit': limit,
            }
        )

        posts = []
        for post in data.get('data', []):
            insights = {}
            for item in post.get('insights', {}).get('data', []):
                insights[item['name']] = item['values'][0]['value'] if item.get('values') else 0

            reactions = insights.get('post_reactions_by_type_total', {})

            posts.append({
                'post_id': post['id'],
                'message': post.get('message', '')[:200],
                'created_at': post.get('created_time'),
                'permalink': post.get('permalink_url'),
                'shares': post.get('shares', {}).get('count', 0),
                'impressions': insights.get('post_impressions', 0),
                'engagements': insights.get('post_engagements', 0),
                'likes': reactions.get('like', 0),
                'loves': reactions.get('love', 0),
                'comments': reactions.get('comment', 0),
            })

        return posts

    # ========== INSTAGRAM ==========

    def get_instagram_info(self, instagram_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Instagram Business Account info

        Args:
            instagram_id: Instagram Business Account ID

        Returns:
            Dict with account info
        """
        instagram_id = instagram_id or self.instagram_id
        if not instagram_id:
            raise ValueError("instagram_id required")

        data = self._request(
            instagram_id,
            params={'fields': 'username,name,biography,followers_count,follows_count,'
                              'media_count,profile_picture_url,website'}
        )

        return {
            'instagram_id': instagram_id,
            'username': data.get('username'),
            'name': data.get('name'),
            'bio': data.get('biography', '')[:200],
            'followers': data.get('followers_count', 0),
            'following': data.get('follows_count', 0),
            'posts': data.get('media_count', 0),
            'website': data.get('website'),
            'profile_picture': data.get('profile_picture_url'),
        }

    def get_instagram_insights(
        self,
        instagram_id: Optional[str] = None,
        period: str = 'day',
        days: int = 28
    ) -> Dict[str, Any]:
        """
        Get Instagram account insights

        Args:
            instagram_id: Instagram Business Account ID
            period: 'day', 'week', 'days_28'
            days: Number of days (max 30)

        Returns:
            Dict with insights
        """
        instagram_id = instagram_id or self.instagram_id
        if not instagram_id:
            raise ValueError("instagram_id required")

        metrics = [
            'impressions',
            'reach',
            'profile_views',
            'follower_count',
        ]

        data = self._request(
            f"{instagram_id}/insights",
            params={
                'metric': ','.join(metrics),
                'period': period,
            }
        )

        results = {}
        for item in data.get('data', []):
            values = item.get('values', [])
            if values:
                results[item['name']] = values[-1].get('value', 0)

        return {
            'instagram_id': instagram_id,
            'period': period,
            'impressions': results.get('impressions', 0),
            'reach': results.get('reach', 0),
            'profile_views': results.get('profile_views', 0),
            'followers': results.get('follower_count', 0),
        }

    def get_instagram_media(
        self,
        instagram_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent Instagram posts with metrics

        Args:
            instagram_id: Instagram Business Account ID
            limit: Number of posts

        Returns:
            List of media dicts
        """
        instagram_id = instagram_id or self.instagram_id
        if not instagram_id:
            raise ValueError("instagram_id required")

        data = self._request(
            f"{instagram_id}/media",
            params={
                'fields': 'id,caption,media_type,media_url,permalink,timestamp,'
                          'like_count,comments_count,insights.metric(impressions,reach)',
                'limit': limit,
            }
        )

        posts = []
        for item in data.get('data', []):
            insights = {}
            for insight in item.get('insights', {}).get('data', []):
                insights[insight['name']] = insight['values'][0]['value'] if insight.get('values') else 0

            posts.append({
                'media_id': item['id'],
                'caption': item.get('caption', '')[:200],
                'media_type': item.get('media_type'),
                'permalink': item.get('permalink'),
                'timestamp': item.get('timestamp'),
                'likes': item.get('like_count', 0),
                'comments': item.get('comments_count', 0),
                'impressions': insights.get('impressions', 0),
                'reach': insights.get('reach', 0),
            })

        return posts

    # ========== COMBINED DASHBOARD ==========

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get combined Facebook + Instagram summary for dashboard

        Returns:
            Dict with both platform stats
        """
        result = {
            'generated_at': datetime.now().isoformat(),
            'facebook': None,
            'instagram': None,
        }

        if self.page_id:
            try:
                fb_info = self.get_page_info()
                result['facebook'] = {
                    'name': fb_info['name'],
                    'followers': fb_info['followers'],
                    'likes': fb_info['likes'],
                }
            except Exception as e:
                result['facebook'] = {'error': str(e)}

        if self.instagram_id:
            try:
                ig_info = self.get_instagram_info()
                result['instagram'] = {
                    'username': ig_info['username'],
                    'followers': ig_info['followers'],
                    'posts': ig_info['posts'],
                }
            except Exception as e:
                result['instagram'] = {'error': str(e)}

        return result


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    meta = MetaAnalytics()

    print("Dashboard Summary:")
    summary = meta.get_dashboard_summary()

    if summary['facebook']:
        fb = summary['facebook']
        if 'error' not in fb:
            print(f"\nFacebook: {fb['name']}")
            print(f"  Followers: {fb['followers']:,}")
            print(f"  Likes: {fb['likes']:,}")
        else:
            print(f"\nFacebook error: {fb['error']}")

    if summary['instagram']:
        ig = summary['instagram']
        if 'error' not in ig:
            print(f"\nInstagram: @{ig['username']}")
            print(f"  Followers: {ig['followers']:,}")
            print(f"  Posts: {ig['posts']}")
        else:
            print(f"\nInstagram error: {ig['error']}")
