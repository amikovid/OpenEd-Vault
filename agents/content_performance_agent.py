#!/usr/bin/env python3
"""
Content Performance Scoring Agent

Closes the feedback loop between published content and editorial decisions.
Pulls analytics from existing modules, calculates composite scores, writes
scores back to Notion Master Content Database.

Skill reference: .claude/skills/content-performance-scoring/SKILL.md

Usage:
    python agents/content_performance_agent.py                    # Score all unscored
    python agents/content_performance_agent.py --type blog        # Score blog content only
    python agents/content_performance_agent.py --type social      # Score social only
    python agents/content_performance_agent.py --digest-only      # Generate digest, no writes
    python agents/content_performance_agent.py --output slack     # Digest to Slack format

Dependencies:
    - google-analytics-data (GA4)
    - google-auth (service account)
    - requests (Notion, Meta, HubSpot, GetLate APIs)
    - python-dotenv
"""

import os
import sys
import json
import argparse
import requests
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict

from dotenv import load_dotenv

# Load environment
load_dotenv(Path(__file__).parent.parent / ".env")

# Add seomachine modules to path
SEOMACHINE_PATH = Path(__file__).parent.parent / "Studio" / "SEO Content Production" / "seomachine"
sys.path.insert(0, str(SEOMACHINE_PATH))

# ============================================================
# CONFIGURATION
# ============================================================

NOTION_DATABASE_ID = "9a2f5189-6c53-4a9d-b961-3ccbcb702612"
NOTION_KEY = os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN")

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Scoring weights by platform (social posts)
PLATFORM_WEIGHTS = {
    "linkedin": {
        "impressions": 0.15,
        "engagement_rate": 0.30,
        "saves": 0.15,
        "shares": 0.15,
        "comments": 0.25,
    },
    "x": {
        "impressions": 0.20,
        "engagement_rate": 0.30,
        "saves": 0.10,
        "shares": 0.25,
        "comments": 0.15,
    },
    "instagram": {
        "impressions": 0.15,
        "engagement_rate": 0.25,
        "saves": 0.30,
        "shares": 0.15,
        "comments": 0.15,
    },
    "facebook": {
        "impressions": 0.20,
        "engagement_rate": 0.25,
        "saves": 0.10,
        "shares": 0.25,
        "comments": 0.20,
    },
    "default": {
        "impressions": 0.20,
        "engagement_rate": 0.35,
        "saves": 0.20,
        "shares": 0.15,
        "comments": 0.10,
    },
}

# Blog/SEO scoring weights
BLOG_WEIGHTS = {
    "pageviews": 0.25,
    "engagement_rate": 0.20,
    "impressions": 0.15,
    "ctr": 0.15,
    "conversions": 0.15,
    "trend": 0.10,
}

# Newsletter scoring weights
NEWSLETTER_WEIGHTS = {
    "open_rate": 0.30,
    "click_rate": 0.35,
    "unsubscribe_rate_inverse": 0.15,
    "reply_rate": 0.20,
}

# Score label thresholds
SCORE_LABELS = [
    (80, "Top Performer"),
    (60, "Strong"),
    (40, "Average"),
    (20, "Underperforming"),
    (0, "Poor"),
]

# Content format IDs that map to content types
# From .claude/references/notion-content-schema.md
BLOG_FORMAT_IDS = [
    "2a3afe52-ef59-800b-8af2-e1347eda8f30",  # Deep Dives
    "f3e829fb-b1e6-43e3-a3e7-116c767722cb",  # Open Education Hub
]
NEWSLETTER_FORMAT_IDS = [
    "2aaafe52-ef59-80bc-beea-ce72402611aa",  # OpenEd Daily
    "c62c9b50-eb8a-4d30-977d-bea5fb57cada",  # Weekly digest
]
PODCAST_FORMAT_IDS = [
    "2acafe52-ef59-8050-940b-fae3327571af",  # Podcast
]
VIDEO_FORMAT_IDS = [
    "2a3afe52-ef59-80ce-aab4-cc804fe4818b",  # Reel
    "2abafe52-ef59-80b0-bb6a-d573d4a4c797",  # Horse Mask
    "2a3afe52-ef59-80db-9380-eda257e462de",  # Podcast clip
    "2aaafe52-ef59-80e6-abe5-c162872974a2",  # YouTube Remix
    "2aaafe52-ef59-8074-893f-da599e815117",  # Text on B-Roll
    "2abafe52-ef59-8048-bd47-d5f8e83b58f9",  # GreenScreen Memes
]
SOCIAL_FORMAT_IDS = [
    "2a3afe52-ef59-80b0-b900-d397fc3c4ad6",  # Text Heavy
    "2a3afe52-ef59-80ed-897a-e776a3d05cfe",  # Memes
    "2a3afe52-ef59-806c-8a82-dae10c8fbd8e",  # Screenshot
    "2aaafe52-ef59-80d1-888a-f872cd7e425d",  # Carousel
    "2abafe52-ef59-801e-b69f-f32081403886",  # X
]


# ============================================================
# ANALYTICS DATA COLLECTION
# ============================================================

def init_analytics_modules() -> Dict[str, Any]:
    """
    Initialize available analytics modules.
    Gracefully handles missing credentials - only loads what's configured.
    """
    modules = {}

    # GA4
    try:
        from data_sources.modules.google_analytics import GoogleAnalytics
        modules["ga4"] = GoogleAnalytics()
        print("  [ok] GA4 connected")
    except Exception as e:
        print(f"  [--] GA4 not available: {e}")
        modules["ga4"] = None

    # GSC
    try:
        from data_sources.modules.google_search_console import GoogleSearchConsole
        modules["gsc"] = GoogleSearchConsole()
        print("  [ok] GSC connected")
    except Exception as e:
        print(f"  [--] GSC not available: {e}")
        modules["gsc"] = None

    # Meta (Facebook + Instagram)
    try:
        from data_sources.modules.meta import MetaAnalytics
        modules["meta"] = MetaAnalytics()
        print("  [ok] Meta connected")
    except Exception as e:
        print(f"  [--] Meta not available: {e}")
        modules["meta"] = None

    # YouTube
    try:
        from data_sources.modules.youtube import YouTubeAnalytics
        modules["youtube"] = YouTubeAnalytics()
        print("  [ok] YouTube connected")
    except Exception as e:
        print(f"  [--] YouTube not available: {e}")
        modules["youtube"] = None

    # HubSpot
    try:
        from data_sources.modules.hubspot import HubSpotAnalytics
        modules["hubspot"] = HubSpotAnalytics()
        print("  [ok] HubSpot connected")
    except Exception as e:
        print(f"  [--] HubSpot not available: {e}")
        modules["hubspot"] = None

    return modules


def collect_blog_metrics(url: str, modules: Dict) -> Dict[str, Any]:
    """Collect all available metrics for a blog/SEO page."""
    metrics = {
        "pageviews": 0,
        "sessions": 0,
        "engagement_rate": 0,
        "bounce_rate": 0,
        "impressions": 0,
        "clicks": 0,
        "ctr": 0,
        "avg_position": 0,
        "conversions": 0,
        "trend_direction": "unknown",
        "trend_percent": 0,
    }

    # Extract path from URL
    path = url
    if url.startswith("http"):
        from urllib.parse import urlparse
        path = urlparse(url).path

    # GA4 data
    if modules.get("ga4"):
        try:
            trends = modules["ga4"].get_page_trends(path, days=30)
            metrics["pageviews"] = trends.get("total_pageviews", 0)
            metrics["trend_direction"] = trends.get("trend_direction", "unknown")
            metrics["trend_percent"] = trends.get("trend_percent", 0)

            # Get engagement metrics from top pages
            top_pages = modules["ga4"].get_top_pages(days=30, limit=200, path_filter=path)
            for page in top_pages:
                if page["path"] == path:
                    metrics["sessions"] = page.get("sessions", 0)
                    metrics["engagement_rate"] = page.get("engagement_rate", 0)
                    metrics["bounce_rate"] = page.get("bounce_rate", 0)
                    break
        except Exception as e:
            print(f"    GA4 error for {path}: {e}")

    # GSC data
    if modules.get("gsc"):
        try:
            page_perf = modules["gsc"].get_page_performance(path, days=30)
            metrics["impressions"] = page_perf.get("impressions", 0)
            metrics["clicks"] = page_perf.get("clicks", 0)
            metrics["ctr"] = page_perf.get("ctr", 0)
            metrics["avg_position"] = page_perf.get("avg_position", 0)
        except Exception as e:
            print(f"    GSC error for {path}: {e}")

    # HubSpot conversion data
    if modules.get("hubspot"):
        try:
            conversions = modules["hubspot"].get_landing_page_conversions(days=30)
            for conv in conversions:
                if path in conv.get("url", ""):
                    metrics["conversions"] = conv.get("count", 0)
                    break
        except Exception:
            pass

    return metrics


def collect_social_metrics(post_url: str, platform: str, modules: Dict) -> Dict[str, Any]:
    """Collect metrics for a social post."""
    metrics = {
        "impressions": 0,
        "engagements": 0,
        "engagement_rate": 0,
        "likes": 0,
        "comments": 0,
        "shares": 0,
        "saves": 0,
    }

    if platform in ("facebook", "fb") and modules.get("meta"):
        try:
            posts = modules["meta"].get_recent_posts(limit=50)
            for post in posts:
                if post.get("permalink") == post_url or post.get("post_id") in (post_url or ""):
                    metrics["impressions"] = post.get("impressions", 0)
                    metrics["likes"] = post.get("likes", 0)
                    metrics["comments"] = post.get("comments", 0)
                    metrics["shares"] = post.get("shares", 0)
                    metrics["engagements"] = metrics["likes"] + metrics["comments"] + metrics["shares"]
                    if metrics["impressions"] > 0:
                        metrics["engagement_rate"] = (metrics["engagements"] / metrics["impressions"]) * 100
                    break
        except Exception as e:
            print(f"    Meta error: {e}")

    elif platform == "instagram" and modules.get("meta"):
        try:
            posts = modules["meta"].get_instagram_media(limit=50)
            for post in posts:
                if post.get("permalink") == post_url or post.get("media_id") in (post_url or ""):
                    metrics["impressions"] = post.get("impressions", 0)
                    metrics["likes"] = post.get("likes", 0)
                    metrics["comments"] = post.get("comments", 0)
                    metrics["engagements"] = metrics["likes"] + metrics["comments"]
                    if metrics["impressions"] > 0:
                        metrics["engagement_rate"] = (metrics["engagements"] / metrics["impressions"]) * 100
                    break
        except Exception as e:
            print(f"    Instagram error: {e}")

    elif platform == "youtube" and modules.get("youtube"):
        try:
            channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
            if channel_id:
                videos = modules["youtube"].get_recent_videos(channel_id, max_results=50)
                for video in videos:
                    if post_url and video.get("url", "") in post_url:
                        metrics["impressions"] = video.get("views", 0)
                        metrics["likes"] = video.get("likes", 0)
                        metrics["comments"] = video.get("comments", 0)
                        metrics["engagements"] = metrics["likes"] + metrics["comments"]
                        if metrics["impressions"] > 0:
                            metrics["engagement_rate"] = (metrics["engagements"] / metrics["impressions"]) * 100
                        break
        except Exception as e:
            print(f"    YouTube error: {e}")

    # X/Twitter and LinkedIn: no API modules exist yet
    # When modules are added, extend this function
    elif platform in ("x", "twitter", "linkedin"):
        print(f"    [{platform}] No analytics module available yet (metrics will be zero)")

    return metrics


def collect_newsletter_metrics(title: str, modules: Dict) -> Dict[str, Any]:
    """Collect metrics for a newsletter edition."""
    metrics = {
        "open_rate": 0,
        "click_rate": 0,
        "unsubscribe_rate": 0,
        "reply_rate": 0,
        "sent": 0,
    }

    if modules.get("hubspot"):
        try:
            campaigns = modules["hubspot"].get_email_campaigns(limit=50)
            for campaign in campaigns:
                # Match by title similarity
                campaign_name = campaign.get("name", "").lower()
                if title.lower()[:30] in campaign_name or campaign_name in title.lower():
                    metrics["open_rate"] = campaign.get("open_rate", 0)
                    metrics["click_rate"] = campaign.get("click_rate", 0)
                    metrics["sent"] = campaign.get("sent", 0)
                    break
        except Exception as e:
            print(f"    HubSpot email error: {e}")

    return metrics


# ============================================================
# SCORING ENGINE
# ============================================================

def percentile_rank(value: float, distribution: List[float]) -> float:
    """
    Calculate percentile rank of a value within a distribution.
    Returns 0-100.
    """
    if not distribution or all(v == 0 for v in distribution):
        return 50  # Default to median if no data

    count_below = sum(1 for v in distribution if v < value)
    count_equal = sum(1 for v in distribution if v == value)

    n = len(distribution)
    if n == 0:
        return 50

    return ((count_below + 0.5 * count_equal) / n) * 100


def score_blog(metrics: Dict, distributions: Dict) -> Tuple[float, str]:
    """
    Score a blog/SEO page.
    Returns (score, notes).
    """
    scores = {
        "pageviews": percentile_rank(metrics["pageviews"], distributions.get("pageviews", [])),
        "engagement_rate": percentile_rank(metrics["engagement_rate"], distributions.get("engagement_rate", [])),
        "impressions": percentile_rank(metrics["impressions"], distributions.get("impressions", [])),
        "ctr": percentile_rank(metrics["ctr"], distributions.get("ctr", [])),
        "conversions": percentile_rank(metrics["conversions"], distributions.get("conversions", [])),
    }

    # Trend bonus
    trend_map = {"rising": 100, "stable": 50, "declining": 0, "unknown": 50}
    scores["trend"] = trend_map.get(metrics.get("trend_direction", "unknown"), 50)

    # Weighted composite
    composite = sum(scores[k] * BLOG_WEIGHTS[k] for k in BLOG_WEIGHTS)

    # Generate insight note
    notes = []
    if scores["pageviews"] > 80:
        notes.append(f"High traffic ({metrics['pageviews']} pageviews)")
    if scores["engagement_rate"] > 80:
        notes.append(f"Strong engagement ({metrics['engagement_rate']:.1%})")
    if metrics["trend_direction"] == "declining":
        notes.append(f"Traffic declining {abs(metrics['trend_percent']):.0f}% - needs refresh")
    if metrics["trend_direction"] == "rising":
        notes.append(f"Traffic rising {metrics['trend_percent']:.0f}%")
    if scores["ctr"] < 30 and metrics["impressions"] > 100:
        notes.append(f"Low CTR ({metrics['ctr']:.1%}) despite {metrics['impressions']} impressions - improve title/meta")

    note = ". ".join(notes) if notes else "No notable patterns"
    return round(composite, 1), note


def score_social(metrics: Dict, platform: str, distributions: Dict) -> Tuple[float, str]:
    """
    Score a social media post.
    Returns (score, notes).
    """
    weights = PLATFORM_WEIGHTS.get(platform, PLATFORM_WEIGHTS["default"])

    scores = {
        "impressions": percentile_rank(metrics.get("impressions", 0), distributions.get("impressions", [])),
        "engagement_rate": percentile_rank(metrics.get("engagement_rate", 0), distributions.get("engagement_rate", [])),
        "saves": percentile_rank(metrics.get("saves", 0), distributions.get("saves", [])),
        "shares": percentile_rank(metrics.get("shares", 0), distributions.get("shares", [])),
        "comments": percentile_rank(metrics.get("comments", 0), distributions.get("comments", [])),
    }

    composite = sum(scores[k] * weights[k] for k in weights)

    notes = []
    if scores["engagement_rate"] > 80:
        notes.append(f"High engagement ({metrics.get('engagement_rate', 0):.1f}%)")
    if scores["comments"] > 80:
        notes.append(f"Strong conversation ({metrics.get('comments', 0)} comments)")
    if scores["shares"] > 80:
        notes.append(f"High amplification ({metrics.get('shares', 0)} shares)")
    if metrics.get("impressions", 0) > 0 and scores["engagement_rate"] < 20:
        notes.append(f"Reached {metrics['impressions']} people but low engagement - weak hook?")

    note = ". ".join(notes) if notes else "No notable patterns"
    return round(composite, 1), note


def score_newsletter(metrics: Dict, distributions: Dict) -> Tuple[float, str]:
    """
    Score a newsletter edition.
    Returns (score, notes).
    """
    scores = {
        "open_rate": percentile_rank(metrics["open_rate"], distributions.get("open_rate", [])),
        "click_rate": percentile_rank(metrics["click_rate"], distributions.get("click_rate", [])),
    }

    # Inverse scoring for unsubscribe rate (lower is better)
    unsub_dist = distributions.get("unsubscribe_rate", [])
    if unsub_dist:
        scores["unsubscribe_rate_inverse"] = 100 - percentile_rank(metrics["unsubscribe_rate"], unsub_dist)
    else:
        scores["unsubscribe_rate_inverse"] = 50

    scores["reply_rate"] = percentile_rank(metrics.get("reply_rate", 0), distributions.get("reply_rate", []))

    composite = sum(scores[k] * NEWSLETTER_WEIGHTS[k] for k in NEWSLETTER_WEIGHTS)

    notes = []
    if scores["open_rate"] > 80:
        notes.append(f"Great subject line ({metrics['open_rate']:.1f}% open rate)")
    if scores["click_rate"] > 80:
        notes.append(f"High clicks ({metrics['click_rate']:.1f}%)")
    if scores["open_rate"] < 30:
        notes.append(f"Low opens ({metrics['open_rate']:.1f}%) - test subject line")

    note = ". ".join(notes) if notes else "No notable patterns"
    return round(composite, 1), note


def get_score_label(score: float) -> str:
    """Map numeric score to label."""
    for threshold, label in SCORE_LABELS:
        if score >= threshold:
            return label
    return "Poor"


# ============================================================
# NOTION OPERATIONS
# ============================================================

def query_notion_posted(content_type: Optional[str] = None, needs_scoring: bool = True) -> List[Dict]:
    """
    Query Notion for posted content that needs scoring.

    Args:
        content_type: Filter by type (blog, social, newsletter, podcast)
        needs_scoring: If True, only return items without recent scores
    """
    filters = [
        {"property": "Status", "status": {"equals": "Posted"}}
    ]

    # Filter by content format if type specified
    format_ids = []
    if content_type == "blog":
        format_ids = BLOG_FORMAT_IDS
    elif content_type == "social":
        format_ids = SOCIAL_FORMAT_IDS + VIDEO_FORMAT_IDS
    elif content_type == "newsletter":
        format_ids = NEWSLETTER_FORMAT_IDS
    elif content_type == "podcast":
        format_ids = PODCAST_FORMAT_IDS

    if format_ids:
        format_filter = {
            "or": [
                {"property": "Content Formats", "relation": {"contains": fid}}
                for fid in format_ids
            ]
        }
        filters.append(format_filter)

    body = {
        "filter": {"and": filters} if len(filters) > 1 else filters[0],
        "sorts": [{"property": "Publish Date", "direction": "descending"}],
        "page_size": 100,
    }

    response = requests.post(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
        headers=NOTION_HEADERS,
        json=body,
    )

    if response.status_code != 200:
        print(f"Notion query error: {response.status_code} - {response.text[:200]}")
        return []

    results = response.json().get("results", [])

    if needs_scoring:
        # Filter to items that haven't been scored recently
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        filtered = []
        for item in results:
            props = item.get("properties", {})
            last_scored = props.get("Last Scored", {}).get("date", {})
            if not last_scored or not last_scored.get("start"):
                filtered.append(item)
            elif last_scored["start"] < seven_days_ago:
                filtered.append(item)
        return filtered

    return results


def update_notion_score(page_id: str, score: float, label: str, metrics: Dict, notes: str):
    """Write performance score and metrics back to Notion."""
    properties = {
        "Performance Score": {"number": score},
        "Score Label": {"select": {"name": label}},
        "Impressions": {"number": metrics.get("impressions", metrics.get("pageviews", 0))},
        "Engagements": {"number": metrics.get("engagements", metrics.get("likes", 0) + metrics.get("comments", 0) + metrics.get("shares", 0))},
        "Clicks": {"number": metrics.get("clicks", metrics.get("pageviews", 0))},
        "Last Scored": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "Score Notes": {"rich_text": [{"text": {"content": notes[:2000]}}]},
    }

    # Engagement rate
    eng_rate = metrics.get("engagement_rate", 0)
    if isinstance(eng_rate, (int, float)):
        properties["Engagement Rate"] = {"number": round(float(eng_rate), 2)}

    # Trend
    trend = metrics.get("trend_direction")
    if trend and trend != "unknown":
        properties["Trend"] = {"select": {"name": trend.capitalize()}}

    response = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=NOTION_HEADERS,
        json={"properties": properties},
    )

    return response.status_code == 200


def detect_content_type(item: Dict) -> str:
    """Detect content type from Notion item's Content Formats relation."""
    props = item.get("properties", {})
    format_relations = props.get("Content Formats", {}).get("relation", [])
    format_ids = [r.get("id", "") for r in format_relations]

    for fid in format_ids:
        if fid in BLOG_FORMAT_IDS:
            return "blog"
        if fid in NEWSLETTER_FORMAT_IDS:
            return "newsletter"
        if fid in PODCAST_FORMAT_IDS:
            return "podcast"
        if fid in VIDEO_FORMAT_IDS:
            return "social"
        if fid in SOCIAL_FORMAT_IDS:
            return "social"

    return "social"  # Default assumption


def get_item_url(item: Dict) -> str:
    """Extract URL from Notion item."""
    props = item.get("properties", {})
    url = props.get("URL", {}).get("url", "")
    if not url:
        url = props.get("Source URL", {}).get("url", "")
    return url or ""


def get_item_title(item: Dict) -> str:
    """Extract title from Notion item."""
    props = item.get("properties", {})
    title_prop = props.get("Name", {}).get("title", [])
    return title_prop[0].get("plain_text", "Untitled") if title_prop else "Untitled"


def detect_platform(item: Dict) -> str:
    """Detect social platform from Notion item."""
    props = item.get("properties", {})

    # Check Content Formats for platform hints
    format_relations = props.get("Content Formats", {}).get("relation", [])
    format_ids = [r.get("id", "") for r in format_relations]

    # X format ID
    if "2abafe52-ef59-801e-b69f-f32081403886" in format_ids:
        return "x"

    # Check URL for platform
    url = get_item_url(item)
    if "linkedin.com" in url:
        return "linkedin"
    if "twitter.com" in url or "x.com" in url:
        return "x"
    if "instagram.com" in url:
        return "instagram"
    if "facebook.com" in url:
        return "facebook"
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    if "tiktok.com" in url:
        return "tiktok"

    return "default"


# ============================================================
# DISTRIBUTION BUILDING
# ============================================================

def build_distributions(items: List[Dict], modules: Dict) -> Dict[str, Dict[str, List[float]]]:
    """
    Build metric distributions from all posted content.
    Used for percentile ranking.

    Returns dict keyed by content_type with sub-dicts of metric distributions.
    """
    distributions = defaultdict(lambda: defaultdict(list))

    # For blog content, use GA4 top pages as distribution
    if modules.get("ga4"):
        try:
            top_pages = modules["ga4"].get_top_pages(days=30, limit=200)
            for page in top_pages:
                distributions["blog"]["pageviews"].append(page.get("pageviews", 0))
                distributions["blog"]["engagement_rate"].append(page.get("engagement_rate", 0))
                distributions["blog"]["sessions"].append(page.get("sessions", 0))
        except Exception:
            pass

    # For social content, use Meta recent posts as distribution
    if modules.get("meta"):
        try:
            fb_posts = modules["meta"].get_recent_posts(limit=50)
            for post in fb_posts:
                distributions["social"]["impressions"].append(post.get("impressions", 0))
                distributions["social"]["comments"].append(post.get("comments", 0))
                distributions["social"]["shares"].append(post.get("shares", 0))
                distributions["social"]["likes"].append(post.get("likes", 0))
                total_eng = post.get("likes", 0) + post.get("comments", 0) + post.get("shares", 0)
                imps = post.get("impressions", 1)
                distributions["social"]["engagement_rate"].append((total_eng / imps) * 100 if imps > 0 else 0)
        except Exception:
            pass

        try:
            ig_posts = modules["meta"].get_instagram_media(limit=50)
            for post in ig_posts:
                distributions["social"]["impressions"].append(post.get("impressions", 0))
                distributions["social"]["comments"].append(post.get("comments", 0))
                distributions["social"]["likes"].append(post.get("likes", 0))
                total_eng = post.get("likes", 0) + post.get("comments", 0)
                imps = post.get("impressions", 1)
                distributions["social"]["engagement_rate"].append((total_eng / imps) * 100 if imps > 0 else 0)
        except Exception:
            pass

    # For newsletters, use HubSpot email campaigns
    if modules.get("hubspot"):
        try:
            campaigns = modules["hubspot"].get_email_campaigns(limit=50)
            for c in campaigns:
                distributions["newsletter"]["open_rate"].append(c.get("open_rate", 0))
                distributions["newsletter"]["click_rate"].append(c.get("click_rate", 0))
        except Exception:
            pass

    # Ensure all distributions have defaults for scoring
    for ctype in ["blog", "social", "newsletter"]:
        for metric in ["impressions", "engagement_rate", "comments", "shares", "saves",
                       "likes", "pageviews", "ctr", "conversions", "open_rate", "click_rate",
                       "unsubscribe_rate", "reply_rate"]:
            if not distributions[ctype][metric]:
                distributions[ctype][metric] = [0]

    return dict(distributions)


# ============================================================
# DIGEST GENERATION
# ============================================================

def generate_digest(scored_items: List[Dict], output_format: str = "markdown") -> str:
    """
    Generate a narrative insights digest from scored items.
    Leads with patterns and recommendations, not just rankings.

    Args:
        scored_items: List of {title, score, label, content_type, platform, notes, metrics}
        output_format: "markdown" or "slack"
    """
    if not scored_items:
        return "No scored content to report."

    sorted_items = sorted(scored_items, key=lambda x: x["score"], reverse=True)
    top_5 = sorted_items[:5]
    bottom_5 = [i for i in sorted_items if i["score"] < 40][-5:] if any(i["score"] < 40 for i in sorted_items) else []

    # Compute platform and theme analytics
    theme_scores = defaultdict(list)
    platform_scores = defaultdict(list)
    content_type_scores = defaultdict(list)
    for item in scored_items:
        for theme in item.get("themes", []):
            theme_scores[theme].append(item["score"])
        platform_scores[item.get("platform", "unknown")].append(item["score"])
        content_type_scores[item.get("content_type", "unknown")].append(item["score"])

    # Cross-reference: theme x platform performance
    theme_platform = defaultdict(lambda: defaultdict(list))
    for item in scored_items:
        for theme in item.get("themes", []):
            theme_platform[theme][item.get("platform", "unknown")].append(item["score"])

    date_str = datetime.now().strftime("%b %d, %Y")
    lines = []
    b = "*" if output_format == "slack" else "**"  # bold marker
    h2 = "" if output_format == "slack" else "## "
    h3 = "" if output_format == "slack" else "### "

    lines.append(f"{h2}Content Insights - {date_str}")
    lines.append(f"{len(scored_items)} pieces scored\n")

    # ---- SECTION 1: Key Insights (the main value) ----
    lines.append(f"{h3}{b}Key Insights{b}" if output_format == "slack" else f"{h3}Key Insights")
    insights = []

    # Best platform
    if platform_scores:
        best_platform = max(platform_scores.items(), key=lambda x: statistics.mean(x[1]))
        worst_platform = min(platform_scores.items(), key=lambda x: statistics.mean(x[1]))
        if best_platform[0] != worst_platform[0]:
            spread = statistics.mean(best_platform[1]) - statistics.mean(worst_platform[1])
            if spread > 15:
                insights.append(
                    f"{best_platform[0].capitalize()} is your strongest platform (avg score: {statistics.mean(best_platform[1]):.0f}) - "
                    f"{worst_platform[0].capitalize()} is weakest ({statistics.mean(worst_platform[1]):.0f}). "
                    f"Consider shifting volume toward {best_platform[0].capitalize()}."
                )

    # Theme performance gaps
    if theme_scores:
        sorted_themes = sorted(theme_scores.items(), key=lambda x: statistics.mean(x[1]), reverse=True)
        if len(sorted_themes) >= 2:
            best_theme = sorted_themes[0]
            worst_theme = sorted_themes[-1]
            if statistics.mean(best_theme[1]) - statistics.mean(worst_theme[1]) > 20:
                insights.append(
                    f'"{best_theme[0]}" content consistently outperforms (avg {statistics.mean(best_theme[1]):.0f}) '
                    f'while "{worst_theme[0]}" underperforms ({statistics.mean(worst_theme[1]):.0f}). '
                    f"Double down on {best_theme[0]} or rethink the {worst_theme[0]} approach."
                )

    # Theme x platform mismatches (the money insight)
    for theme, platforms in theme_platform.items():
        if len(platforms) >= 2:
            platform_avgs = {p: statistics.mean(s) for p, s in platforms.items() if len(s) >= 2}
            if len(platform_avgs) >= 2:
                best_p = max(platform_avgs, key=platform_avgs.get)
                worst_p = min(platform_avgs, key=platform_avgs.get)
                if platform_avgs[best_p] - platform_avgs[worst_p] > 25:
                    insights.append(
                        f'"{theme}" performs {platform_avgs[best_p]:.0f} on {best_p.capitalize()} '
                        f"but only {platform_avgs[worst_p]:.0f} on {worst_p.capitalize()}. "
                        f"Route {theme.lower()} content to {best_p.capitalize()}."
                    )

    # Anomaly detection (outliers)
    if len(scored_items) >= 5:
        avg_score = statistics.mean([i["score"] for i in scored_items])
        for item in sorted_items[:3]:
            if item["score"] > avg_score * 1.5:
                insights.append(
                    f'Outlier: "{item["title"][:40]}" scored {item["score"]:.0f} '
                    f"(avg is {avg_score:.0f}). {item.get('notes', 'Study what made this work.')}".rstrip(".")
                )
                break

    # Declining content alert
    declining = [i for i in scored_items if i.get("metrics", {}).get("trend_direction") == "declining"]
    if declining:
        insights.append(
            f"{len(declining)} piece{'s' if len(declining) > 1 else ''} trending down. "
            f'Top decline: "{declining[0]["title"][:40]}" - consider refreshing or resurfacing.'
        )

    if not insights:
        insights.append("Not enough data for pattern detection yet. Scores will become more useful as the library grows.")

    for i, insight in enumerate(insights, 1):
        lines.append(f"{i}. {insight}")

    # ---- SECTION 2: Recommendations ----
    lines.append(f"\n{h3}{b}This Week's Recommendations{b}" if output_format == "slack" else f"\n{h3}This Week's Recommendations")

    recs = []
    # Recommend resurfacing top performer
    if top_5:
        recs.append(f'Resurface: "{top_5[0]["title"][:40]}" (score: {top_5[0]["score"]:.0f}) - proven content worth resharing')

    # Recommend dropping underperformer pattern
    if bottom_5:
        recs.append(f'Review: "{bottom_5[0]["title"][:40]}" (score: {bottom_5[0]["score"]:.0f}) - {bottom_5[0].get("notes", "low engagement")}')

    # Platform routing rec
    if platform_scores:
        best_p = max(platform_scores.items(), key=lambda x: statistics.mean(x[1]))
        if len(best_p[1]) >= 3:
            recs.append(f"Increase {best_p[0].capitalize()} posting volume - consistently your top performer (avg {statistics.mean(best_p[1]):.0f})")

    for rec in recs:
        lines.append(f"- {rec}")

    # ---- SECTION 3: Scoreboard (compact) ----
    lines.append(f"\n{h3}{b}Top 5{b}" if output_format == "slack" else f"\n{h3}Top 5")
    for i, item in enumerate(top_5, 1):
        lines.append(f"{i}. {item['title'][:50]} ({item.get('platform', '')}) - {item['score']:.0f}")

    if bottom_5:
        lines.append(f"\n{h3}{b}Needs Attention{b}" if output_format == "slack" else f"\n{h3}Needs Attention")
        for item in bottom_5[:3]:
            lines.append(f"- {item['title'][:50]} ({item['score']:.0f}) - {item.get('notes', '')[:60]}")

    # ---- SECTION 4: Platform & Theme Summary ----
    if platform_scores:
        lines.append(f"\n{h3}Platform Averages")
        for platform, scores in sorted(platform_scores.items(), key=lambda x: statistics.mean(x[1]), reverse=True):
            avg = statistics.mean(scores)
            count = len(scores)
            bar = "=" * int(avg / 5)  # simple visual bar
            lines.append(f"  {platform:12s} {bar} {avg:.0f} ({count} posts)")

    return "\n".join(lines)


def get_approval_context(content_theme: str, platform: str, scored_items: List[Dict] = None) -> str:
    """
    Generate context string for content approval decisions.
    Call this when a new post is being reviewed to show historical performance.

    Args:
        content_theme: Topic/theme of the content being approved
        platform: Target platform
        scored_items: Previously scored items (if None, queries Notion)

    Returns:
        Context string to append to approval message

    Usage in other skills:
        from agents.content_performance_agent import get_approval_context
        context = get_approval_context("Curriculum Reviews", "linkedin")
    """
    if scored_items is None:
        # Query Notion for all scored Posted content
        scored_items = []
        items = query_notion_posted(needs_scoring=False)
        for item in items:
            props = item.get("properties", {})
            score = props.get("Performance Score", {}).get("number")
            if score is None:
                continue

            themes = [opt.get("name", "") for opt in props.get("Content Theme", {}).get("multi_select", [])]
            platform_detect = detect_platform(item)

            scored_items.append({
                "title": get_item_title(item),
                "score": score,
                "platform": platform_detect,
                "themes": themes,
                "label": props.get("Score Label", {}).get("select", {}).get("name", ""),
            })

    if not scored_items:
        return "No historical performance data available yet."

    # Filter by theme
    theme_matches = [i for i in scored_items if content_theme.lower() in [t.lower() for t in i.get("themes", [])]]

    # Filter by platform
    platform_matches = [i for i in scored_items if i.get("platform", "").lower() == platform.lower()]

    # Theme x platform matches
    both_matches = [i for i in theme_matches if i.get("platform", "").lower() == platform.lower()]

    lines = ["---", "Performance context for this draft:"]

    if both_matches:
        avg = statistics.mean([i["score"] for i in both_matches])
        best = max(both_matches, key=lambda x: x["score"])
        lines.append(f'  "{content_theme}" on {platform.capitalize()}: avg score {avg:.0f} ({len(both_matches)} posts)')
        lines.append(f'  Best: "{best["title"][:40]}" (score: {best["score"]:.0f})')

    if theme_matches:
        # Show which platform works best for this theme
        platform_avgs = defaultdict(list)
        for item in theme_matches:
            platform_avgs[item.get("platform", "unknown")].append(item["score"])

        if len(platform_avgs) >= 2:
            sorted_platforms = sorted(platform_avgs.items(), key=lambda x: statistics.mean(x[1]), reverse=True)
            best_p = sorted_platforms[0]
            lines.append(f'  Best platform for "{content_theme}": {best_p[0].capitalize()} (avg {statistics.mean(best_p[1]):.0f})')
            if platform.lower() != best_p[0].lower():
                lines.append(f"  -> Consider routing this to {best_p[0].capitalize()} instead of {platform.capitalize()}")

    if platform_matches and not both_matches:
        avg = statistics.mean([i["score"] for i in platform_matches])
        lines.append(f"  {platform.capitalize()} overall avg: {avg:.0f} ({len(platform_matches)} posts)")

    if len(lines) <= 2:
        lines.append(f"  No historical data for \"{content_theme}\" on {platform.capitalize()} yet.")

    return "\n".join(lines)


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Content Performance Scoring Agent")
    parser.add_argument("--type", choices=["blog", "social", "newsletter", "podcast"],
                        help="Score only this content type")
    parser.add_argument("--digest-only", action="store_true",
                        help="Generate digest without writing to Notion")
    parser.add_argument("--output", choices=["markdown", "slack"], default="markdown",
                        help="Output format for digest")
    parser.add_argument("--all", action="store_true",
                        help="Re-score all content, not just unscored")
    args = parser.parse_args()

    print("=" * 60)
    print("Content Performance Scoring Agent")
    print(f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Check Notion access
    if not NOTION_KEY:
        print("\nERROR: No Notion API key found.")
        print("Set NOTION_API_KEY or NOTION_TOKEN in .env")
        sys.exit(1)

    # Initialize analytics modules
    print("\nConnecting analytics modules...")
    modules = init_analytics_modules()

    active_count = sum(1 for v in modules.values() if v is not None)
    print(f"\n{active_count}/{len(modules)} modules active")

    if active_count == 0:
        print("\nWARNING: No analytics modules available.")
        print("Scores will default to 50 (median). Configure API keys in .env to enable scoring.")
        if not args.digest_only:
            print("Use --digest-only to skip Notion writes.")

    # Query Notion for posted content
    print(f"\nQuerying Notion for {'all' if args.all else 'unscored'} posted content...")
    items = query_notion_posted(
        content_type=args.type,
        needs_scoring=not args.all,
    )
    print(f"Found {len(items)} items to score")

    if not items:
        print("Nothing to score. All content is up to date.")
        return

    # Build distributions for percentile ranking
    print("\nBuilding metric distributions...")
    distributions = build_distributions(items, modules)

    # Score each item
    print("\nScoring content...")
    scored_items = []

    for item in items:
        page_id = item["id"]
        title = get_item_title(item)
        content_type = detect_content_type(item)
        url = get_item_url(item)

        print(f"\n  [{content_type}] {title[:60]}")

        if content_type == "blog":
            metrics = collect_blog_metrics(url, modules)
            score, notes = score_blog(metrics, distributions.get("blog", {}))
            platform = "blog"

        elif content_type == "social":
            platform = detect_platform(item)
            metrics = collect_social_metrics(url, platform, modules)
            score, notes = score_social(metrics, platform, distributions.get("social", {}))

        elif content_type == "newsletter":
            metrics = collect_newsletter_metrics(title, modules)
            score, notes = score_newsletter(metrics, distributions.get("newsletter", {}))
            platform = "email"

        elif content_type == "podcast":
            # Podcast: combine YouTube metrics + blog post metrics
            metrics = collect_social_metrics(url, "youtube", modules)
            score, notes = score_social(metrics, "youtube", distributions.get("social", {}))
            platform = "youtube"

        else:
            metrics = {"impressions": 0, "engagement_rate": 0}
            score, notes = 50.0, "Unclassified content type"
            platform = "unknown"

        label = get_score_label(score)
        print(f"    Score: {score} ({label}) - {notes[:80]}")

        scored_items.append({
            "page_id": page_id,
            "title": title,
            "content_type": content_type,
            "platform": platform,
            "score": score,
            "label": label,
            "notes": notes,
            "metrics": metrics,
            "themes": [],  # TODO: Extract from Content Theme property
        })

        # Write score to Notion
        if not args.digest_only:
            success = update_notion_score(page_id, score, label, metrics, notes)
            if success:
                print(f"    [saved to Notion]")
            else:
                print(f"    [FAILED to save]")

    # Generate digest
    print("\n" + "=" * 60)
    digest = generate_digest(scored_items, args.output)
    print(digest)

    # Save digest to file
    digest_path = Path(__file__).parent.parent / ".claude" / "work-summaries" / f"performance-digest-{datetime.now().strftime('%Y-%m-%d')}.md"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text(digest)
    print(f"\nDigest saved to {digest_path}")

    print(f"\nDone. Scored {len(scored_items)} items.")


if __name__ == "__main__":
    main()
