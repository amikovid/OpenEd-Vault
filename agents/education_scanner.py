#!/usr/bin/env python3
"""
Education Community Scanner - Adapted from jdrhyne/agent-skills/last30days

Scans education-adjacent communities for trending conversations:
- Hacker News (free Algolia API)
- Reddit engagement enrichment (free JSON API)
- X/Twitter (via xAI - when key available)
- OpenAI web search (when key available)

Run: python3 agents/education_scanner.py
Run with specific sources: python3 agents/education_scanner.py --sources hn,reddit
Run with days override: python3 agents/education_scanner.py --days 7

Outputs to Projects/RSS-Curation/tracking.json (same format as RSS curation)
and Projects/RSS-Curation/community/YYYY-MM-DD.md
"""

import json
import os
import re
import sys
import time
import math
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from hashlib import sha256

# Paths
BASE_DIR = Path(__file__).parent.parent
TRACKING_PATH = BASE_DIR / "Projects/RSS-Curation/tracking.json"
COMMUNITY_DIR = BASE_DIR / "Projects/RSS-Curation/community"
CACHE_DIR = Path.home() / ".cache/education-scanner"

# ─── Education Search Queries ────────────────────────────────────────────

HN_QUERIES = [
    "homeschool",
    "homeschooling",
    "unschooling",
    "self-directed learning",
    "microschool",
    "alternative education",
    "deschooling",
    "classical education",
    "Charlotte Mason",
    "Montessori",
    "Waldorf",
    "forest school",
    "learning pod",
    "school choice",
    "education freedom",
    "compulsory education",
    "AI tutoring",
    "personalized learning",
    "child-led learning",
]

# Reddit subreddits to scan for trending threads (beyond RSS)
# Tier 1: Core homeschool/alt-ed (high signal, almost everything relevant)
# Tier 2: Adjacent education (needs engagement + keyword filtering)
# Skipped: r/Parenting (too noisy), r/Teachers (mostly venting, not alt-ed)
REDDIT_SUBREDDITS = [
    # Tier 1 - high signal
    "homeschool",
    "unschool",
    "afterschooling",
    "SelfDirectedLearning",
    "Montessori",
    "waldorf",
    "CharlotteMason",
    # Tier 2 - broader, needs filtering
    "education",
    "homeschoolrecovery",  # counter-signal: what goes wrong
]

# r/Teachers posts only if they match these patterns (system-is-broken signal)
TEACHERS_KEYWORDS = [
    "homeschool", "pulling kids out", "leaving teaching",
    "parents don't care", "AI cheating", "screen time",
    "can't read", "literacy", "reading level",
    "behavior crisis", "kids can't", "broken system",
]

# Minimum engagement thresholds for Reddit
REDDIT_MIN_UPVOTES = 15
REDDIT_MIN_COMMENTS = 10

# ─── Hacker News Search (Free Algolia API) ──────────────────────────────

def search_hn(query: str, days: int = 30, limit: int = 10) -> list:
    """Search Hacker News via free Algolia API"""
    cutoff = int((datetime.now() - timedelta(days=days)).timestamp())
    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"created_at_i>{cutoff}",
        "hitsPerPage": limit,
    })
    url = f"https://hn.algolia.com/api/v1/search?{params}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "education-scanner/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("hits", [])
    except Exception as e:
        print(f"  HN search error for '{query}': {e}")
        return []


def fetch_all_hn(days: int = 30) -> list:
    """Fetch HN results for all education queries, dedupe by URL"""
    print(f"\n── Hacker News (last {days} days) ──")
    seen_ids = set()
    items = []

    for query in HN_QUERIES:
        hits = search_hn(query, days=days)
        for hit in hits:
            obj_id = hit.get("objectID", "")
            if obj_id in seen_ids:
                continue
            seen_ids.add(obj_id)

            points = hit.get("points", 0) or 0
            comments = hit.get("num_comments", 0) or 0
            title = hit.get("title", "")
            hn_url = f"https://news.ycombinator.com/item?id={obj_id}"
            story_url = hit.get("url", hn_url)
            created = hit.get("created_at", "")

            # Skip low-engagement items
            if points < 5 and comments < 3:
                continue

            items.append({
                "source": "Hacker News",
                "title": title,
                "link": story_url,
                "hn_link": hn_url,
                "points": points,
                "comments": comments,
                "date": created[:10] if created else "",
                "query": query,
            })

        time.sleep(0.3)  # Rate limiting

    # Sort by engagement (points + comments)
    items.sort(key=lambda x: x["points"] + x["comments"], reverse=True)
    print(f"  Found {len(items)} unique HN items")
    return items


# ─── Reddit Engagement Enrichment ────────────────────────────────────────

def fetch_reddit_json(url: str) -> dict:
    """Fetch actual Reddit thread JSON for engagement data"""
    # Convert reddit URL to .json endpoint
    json_url = url.rstrip("/") + ".json"
    if "?" in json_url:
        json_url = json_url.split("?")[0] + ".json"

    try:
        req = urllib.request.Request(json_url, headers={
            "User-Agent": "education-scanner/1.0 (research tool)",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return None


def enrich_reddit_item(url: str) -> dict:
    """Get engagement metrics for a Reddit URL"""
    data = fetch_reddit_json(url)
    if not data or not isinstance(data, list) or len(data) < 1:
        return None

    try:
        post = data[0]["data"]["children"][0]["data"]
        result = {
            "upvotes": post.get("score", 0),
            "upvote_ratio": post.get("upvote_ratio", 0),
            "num_comments": post.get("num_comments", 0),
            "subreddit": post.get("subreddit", ""),
        }

        # Get top comments if available
        if len(data) > 1:
            comments = data[1].get("data", {}).get("children", [])
            top_comments = []
            for c in comments[:3]:
                if c.get("kind") == "t1":
                    body = c["data"].get("body", "")[:200]
                    score = c["data"].get("score", 0)
                    if body and score > 0:
                        top_comments.append({"body": body, "score": score})
            result["top_comments"] = top_comments

        return result
    except (KeyError, IndexError):
        return None


def fetch_subreddit_top(subreddit: str, timeframe: str = "week", limit: int = 10) -> list:
    """Fetch top posts from a subreddit"""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t={timeframe}&limit={limit}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "education-scanner/1.0 (research tool)",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            posts = data.get("data", {}).get("children", [])
            items = []
            for p in posts:
                d = p.get("data", {})
                upvotes = d.get("score", 0)
                comments = d.get("num_comments", 0)

                # Apply engagement threshold
                if upvotes < REDDIT_MIN_UPVOTES and comments < REDDIT_MIN_COMMENTS:
                    continue

                items.append({
                    "source": f"r/{subreddit}",
                    "title": d.get("title", ""),
                    "link": f"https://www.reddit.com{d.get('permalink', '')}",
                    "upvotes": upvotes,
                    "upvote_ratio": d.get("upvote_ratio", 0),
                    "num_comments": comments,
                    "date": datetime.fromtimestamp(d.get("created_utc", 0)).strftime("%Y-%m-%d"),
                    "selftext": (d.get("selftext", "") or "")[:200],
                })
            return items
    except Exception as e:
        print(f"  Reddit error for r/{subreddit}: {e}")
        return []


def fetch_all_reddit(days: int = 30) -> list:
    """Fetch top Reddit posts across education subreddits"""
    timeframe = "week" if days <= 7 else "month"
    print(f"\n── Reddit Top Posts (timeframe: {timeframe}) ──")

    seen_urls = set()
    items = []

    for sub in REDDIT_SUBREDDITS:
        posts = fetch_subreddit_top(sub, timeframe=timeframe)
        for p in posts:
            if p["link"] not in seen_urls:
                seen_urls.add(p["link"])
                items.append(p)
        time.sleep(1.0)  # Reddit rate limiting - be generous

    # Also scan r/Teachers but with strict keyword filtering
    print("  Scanning r/Teachers (strict filter)...")
    teachers_posts = fetch_subreddit_top("Teachers", timeframe=timeframe, limit=25)
    teachers_kept = 0
    for p in teachers_posts:
        if p["link"] in seen_urls:
            continue
        text = (p.get("title", "") + " " + p.get("selftext", "")).lower()
        if any(kw in text for kw in TEACHERS_KEYWORDS):
            seen_urls.add(p["link"])
            items.append(p)
            teachers_kept += 1
    print(f"  r/Teachers: kept {teachers_kept} of {len(teachers_posts)} (keyword-filtered)")

    items.sort(key=lambda x: x.get("upvotes", 0) + x.get("num_comments", 0), reverse=True)
    print(f"  Found {len(items)} high-engagement Reddit posts")
    return items


# ─── Enrichment of Existing RSS Reddit Items ─────────────────────────────

def enrich_rss_reddit_items(tracking: dict) -> dict:
    """Enrich existing Reddit items in tracking.json with engagement data"""
    print("\n── Enriching RSS Reddit items ──")
    enriched = 0

    for url, item in tracking.get("items", {}).items():
        source = item.get("source", "")
        if "r/" not in source and "reddit" not in url:
            continue

        # Skip if already enriched
        if item.get("upvotes") is not None:
            continue

        data = enrich_reddit_item(url)
        if data:
            item["upvotes"] = data["upvotes"]
            item["num_comments"] = data["num_comments"]
            item["upvote_ratio"] = data.get("upvote_ratio", 0)

            # Re-score based on engagement
            if data["upvotes"] >= 50 or data["num_comments"] >= 30:
                if item.get("score") != "definitely":
                    item["score"] = "definitely"
                    item["status"] = "new"  # Re-surface high-engagement items
            elif data["upvotes"] < 5 and data["num_comments"] < 5:
                item["score"] = "no"

            enriched += 1
            time.sleep(1.0)  # Rate limit

    print(f"  Enriched {enriched} Reddit items with engagement data")
    return tracking


# ─── Scoring ──────────────────────────────────────────────────────────────

EDUCATION_RELEVANCE_KEYWORDS = [
    # Core topics
    "homeschool", "unschool", "self-directed", "microschool",
    "alternative education", "deschool", "child-led",
    "charlotte mason", "montessori", "waldorf", "classical education",
    "forest school", "learning pod", "hybrid homeschool",
    # Adjacent topics we care about
    "screen time", "phone ban", "childhood", "free play",
    "curiosity", "intrinsic motivation", "project-based",
    "AI tutor", "personalized learning", "competency-based",
    "school choice", "education freedom", "parent rights",
    # People we follow
    "peter gray", "john holt", "john taylor gatto", "ken robinson",
    "jon haidt", "lenore skenazy", "kerry mcdonald",
]

EDUCATION_NO_KEYWORDS = [
    # Policy/politics
    "republican", "democrat", "trump", "biden", "congress",
    "union", "strike", "teachers union",
    # Corporate/higher ed
    "enterprise", "corporate training", "b2b", "saas",
    "college ranking", "ivy league", "mba",
    # Off-topic tech
    "cryptocurrency", "blockchain", "nft",
    "devops", "kubernetes", "docker",
    # Generic parenting noise
    "sleep training", "breastfeed", "formula feeding",
    "potty train", "diaper", "teething",
    "daycare pickup", "babysitter",
    "mother in law", "in-laws",
]


def score_community_item(item: dict) -> str:
    """Score a community item for education relevance.

    Key principle: engagement alone is NOT enough. Must have education relevance.
    A parenting vent post with 5000 upvotes is still NO if it's not about education.
    """
    text = (item.get("title", "") + " " + item.get("selftext", "")).lower()
    source = item.get("source", "").lower()

    # Filter out irrelevant
    for kw in EDUCATION_NO_KEYWORDS:
        if kw in text:
            return "no"

    # Count education relevance keywords
    relevance = 0
    for kw in EDUCATION_RELEVANCE_KEYWORDS:
        if kw in text:
            relevance += 1

    # Core homeschool/alt-ed subreddits get a relevance boost (almost everything is on-topic)
    core_subs = ["homeschool", "unschool", "afterschooling", "selfdirectedlearning",
                 "montessori", "waldorf", "charlottemason"]
    is_core = any(sub in source for sub in core_subs)
    if is_core:
        relevance += 1

    # Engagement as a multiplier, NOT a standalone qualifier
    points = item.get("points", 0) or item.get("upvotes", 0) or 0
    comments = item.get("comments", 0) or item.get("num_comments", 0) or 0

    # Must have at least SOME education relevance to qualify
    if relevance == 0:
        return "no"

    # Now score: relevance required, engagement amplifies
    if relevance >= 2 and (points >= 50 or comments >= 20):
        return "definitely"
    elif relevance >= 2:
        return "probably"
    elif relevance >= 1 and (points >= 100 or comments >= 50):
        return "probably"
    else:
        return "no"


# ─── Deduplication ────────────────────────────────────────────────────────

def trigram_similarity(a: str, b: str) -> float:
    """Jaccard similarity on character trigrams"""
    if len(a) < 3 or len(b) < 3:
        return 0.0
    a_trigrams = set(a[i:i+3] for i in range(len(a) - 2))
    b_trigrams = set(b[i:i+3] for i in range(len(b) - 2))
    intersection = len(a_trigrams & b_trigrams)
    union = len(a_trigrams | b_trigrams)
    return intersection / union if union else 0.0


def dedupe_items(items: list, threshold: float = 0.65) -> list:
    """Remove near-duplicate items by title similarity"""
    if not items:
        return items

    kept = [items[0]]
    for item in items[1:]:
        title = item.get("title", "").lower()
        is_dupe = False
        for k in kept:
            if trigram_similarity(title, k.get("title", "").lower()) > threshold:
                is_dupe = True
                break
        if not is_dupe:
            kept.append(item)

    removed = len(items) - len(kept)
    if removed:
        print(f"  Deduped: removed {removed} near-duplicates")
    return kept


# ─── Output ───────────────────────────────────────────────────────────────

def merge_to_tracking(items: list, tracking: dict) -> int:
    """Merge community scanner items into tracking.json format"""
    added = 0
    today = datetime.now().strftime("%Y-%m-%d")

    for item in items:
        url = item.get("link", "")
        if not url or url in tracking.get("items", {}):
            continue

        score = score_community_item(item)
        if score == "no":
            continue

        points = item.get("points", 0) or item.get("upvotes", 0) or 0
        comments = item.get("comments", 0) or item.get("num_comments", 0) or 0

        tracking["items"][url] = {
            "firstSeen": today,
            "score": score,
            "status": "new",
            "source": item.get("source", "Unknown"),
            "title": item.get("title", "")[:120],
            "summary": item.get("selftext", item.get("summary", ""))[:300],
            "upvotes": points,
            "num_comments": comments,
            "scanner_query": item.get("query", ""),
        }
        added += 1

    tracking["stats"]["totalTracked"] = len(tracking["items"])
    return added


def save_community_report(hn_items: list, reddit_items: list):
    """Save daily community report"""
    COMMUNITY_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = COMMUNITY_DIR / f"{date_str}.md"

    lines = [
        f"# Education Community Scanner - {date_str}",
        "",
    ]

    if hn_items:
        lines.append(f"## Hacker News ({len(hn_items)} items)")
        lines.append("")
        for item in hn_items[:20]:
            score = score_community_item(item)
            points = item.get("points", 0)
            comments = item.get("comments", 0)
            lines.append(f"### [{item['title']}]({item['link']})")
            lines.append(f"**{points} pts / {comments} comments** | Score: {score.upper()} | Query: {item.get('query', '')}")
            if item.get("hn_link") and item["hn_link"] != item["link"]:
                lines.append(f"[HN Discussion]({item['hn_link']})")
            lines.append("")

    if reddit_items:
        lines.append(f"## Reddit Top Posts ({len(reddit_items)} items)")
        lines.append("")
        for item in reddit_items[:20]:
            score = score_community_item(item)
            upvotes = item.get("upvotes", 0)
            comments = item.get("num_comments", 0)
            lines.append(f"### [{item['title']}]({item['link']})")
            lines.append(f"**{upvotes} upvotes / {comments} comments** | {item['source']} | Score: {score.upper()}")
            if item.get("selftext"):
                lines.append(f"> {item['selftext'][:150]}...")
            lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"\nReport saved to {output_path}")


# ─── X/Twitter via xAI Grok API ──────────────────────────────────────────
# Requires XAI_API_KEY in environment or ~/.config/last30days/.env
# Get a key at https://console.x.ai

X_QUERIES = [
    "homeschooling",
    "homeschool",
    "unschooling",
    "alternative education",
    "self-directed learning",
    "microschool",
    "deschooling",
    "Charlotte Mason education",
    "classical education homeschool",
]


def search_x(query: str, days: int = 7) -> list:
    """Search X/Twitter via xAI Responses API with x_search tool.
    Uses subprocess curl to avoid Cloudflare blocking urllib.
    Requires grok-4 family models for server-side tools.
    """
    import subprocess

    api_key = os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY")
    if not api_key:
        return []

    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    prompt = (
        f"Search X/Twitter for popular posts about '{query}' since:{since_date}. "
        f"Return the top 10 most engaged posts (highest likes + retweets). "
        f"For each post, return JSON with fields: text, author_handle, "
        f"likes, retweets, replies, url. Return ONLY a JSON array, no other text."
    )

    payload = json.dumps({
        "model": "grok-4-1-fast-non-reasoning",
        "tools": [{"type": "x_search"}],
        "input": prompt,
        "temperature": 0,
    })

    try:
        result = subprocess.run(
            ["curl", "-s", "https://api.x.ai/v1/responses",
             "-H", "Content-Type: application/json",
             "-H", f"Authorization: Bearer {api_key}",
             "-d", payload],
            capture_output=True, text=True, timeout=90
        )
        data = json.loads(result.stdout)

        if data.get("error"):
            err = data["error"]
            msg = err.get("message", err) if isinstance(err, dict) else err
            print(f"  X API error for '{query}': {msg}")
            return []

        # Extract text from Responses API output
        content = ""
        for item in data.get("output", []):
            if item.get("type") == "message":
                for c in item.get("content", []):
                    if c.get("type") == "output_text":
                        content += c["text"]

        # Parse JSON array from response
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            items = json.loads(json_match.group())
            results = []
            for item in items:
                likes = item.get("likes", 0) or 0
                retweets = item.get("retweets", 0) or 0
                # Skip very low engagement
                if likes < 5 and retweets < 2:
                    continue
                results.append({
                    "source": "X/Twitter",
                    "title": item.get("text", "")[:140],
                    "summary": item.get("text", "")[:300],
                    "link": item.get("url", ""),
                    "author": item.get("author_handle", ""),
                    "upvotes": likes,
                    "num_comments": item.get("replies", 0) or 0,
                    "retweets": retweets,
                    "date": item.get("date", ""),
                    "query": query,
                })
            return results
    except Exception as e:
        print(f"  X search error for '{query}': {e}")

    return []


def fetch_all_x(days: int = 7) -> list:
    """Fetch X/Twitter results for all education queries"""
    api_key = os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY")
    if not api_key:
        print("\n── X/Twitter: SKIPPED (no XAI_API_KEY) ──")
        print("  Set XAI_API_KEY in ~/.zshrc or ~/.config/last30days/.env")
        print("  Get a key at https://console.x.ai")
        return []

    print(f"\n── X/Twitter via xAI Grok (last {days} days) ──")
    seen_urls = set()
    items = []

    for query in X_QUERIES:
        results = search_x(query, days=days)
        for item in results:
            url = item.get("link", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                items.append(item)
        time.sleep(1.0)

    items.sort(key=lambda x: x.get("upvotes", 0) + x.get("retweets", 0), reverse=True)
    print(f"  Found {len(items)} unique X/Twitter posts")
    return items


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    print(f"Education Community Scanner - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Parse args
    days = 30
    sources = ["hn", "reddit", "x"]

    for arg in sys.argv[1:]:
        if arg.startswith("--days="):
            days = int(arg.split("=")[1])
        elif arg.startswith("--sources="):
            sources = arg.split("=")[1].split(",")

    print(f"Scanning: {', '.join(sources)} (last {days} days)")

    # Load tracking
    try:
        with open(TRACKING_PATH, 'r') as f:
            tracking = json.load(f)
    except FileNotFoundError:
        tracking = {"lastRun": None, "items": {}, "stats": {"totalTracked": 0}}

    hn_items = []
    reddit_items = []
    x_items = []

    # Hacker News
    if "hn" in sources:
        hn_items = fetch_all_hn(days=days)
        hn_items = dedupe_items(hn_items)

    # Reddit top posts
    if "reddit" in sources:
        reddit_items = fetch_all_reddit(days=days)
        reddit_items = dedupe_items(reddit_items)

    # X/Twitter via xAI
    if "x" in sources:
        x_items = fetch_all_x(days=min(days, 7))
        x_items = dedupe_items(x_items)

    # Enrich existing RSS Reddit items
    if "reddit" in sources:
        tracking = enrich_rss_reddit_items(tracking)

    # Merge into tracking
    all_items = hn_items + reddit_items + x_items
    added = merge_to_tracking(all_items, tracking)

    # Save tracking
    tracking["lastCommunityRun"] = datetime.now().isoformat()
    with open(TRACKING_PATH, 'w') as f:
        json.dump(tracking, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Added {added} new community items to tracking")
    print(f"HN: {len(hn_items)} | Reddit: {len(reddit_items)} | X: {len(x_items)}")
    print(f"Total tracked: {tracking['stats']['totalTracked']}")

    # Save community report
    save_community_report(hn_items, reddit_items)

    print("\nDone. Refresh dashboard at http://localhost:8000 to see new items.")


if __name__ == "__main__":
    main()
