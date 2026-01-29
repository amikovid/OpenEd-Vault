#!/usr/bin/env python3
"""
OpenEd Daily Curation Pipeline
Fetches RSS feeds, filters for relevance, posts to Slack.

Usage:
  python daily_curation.py           # Run full pipeline
  python daily_curation.py --test    # Dry run (no Slack posting)
"""

import feedparser
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# Path to OPML or direct feed list
FEEDS_FILE = Path(__file__).parent.parent / "feeds" / "homeschool_feeds.json"

# Slack channel for output
SLACK_CHANNEL = "#curation-inbox"

# How far back to look for new items
HOURS_LOOKBACK = 36

# Maximum items to post per run
MAX_ITEMS = 10

# Claude CLI command for filtering (uses local auth)
CLAUDE_CMD = ["claude", "-p"]

# =============================================================================
# FEED DEFINITIONS (Homeschool Board - 30+ confirmed feeds)
# =============================================================================

HOMESCHOOL_FEEDS = [
    # Tier 1: Priority sources (check daily)
    {"name": "Kerry McDonald (Forbes)", "url": "https://www.forbes.com/sites/kerrymcdonald/feed/", "tier": 1},
    {"name": "EdChoice", "url": "https://www.edchoice.org/feed/", "tier": 1},
    {"name": "The 74 Million", "url": "https://the74million.org/feed", "tier": 1},
    {"name": "Fab Fridays", "url": "https://newsletter.afabrega.com/feed/", "tier": 1},
    {"name": "Let Grow", "url": "https://letgrow.org/feed/", "tier": 1},
    {"name": "Michael B. Horn", "url": "https://michaelbhorn.substack.com/feed", "tier": 1},

    # Tier 2: High-quality education blogs
    {"name": "Getting Smart", "url": "https://www.gettingsmart.com/feed/", "tier": 2},
    {"name": "EdSurge", "url": "https://www.edsurge.com/articles_rss", "tier": 2},
    {"name": "Rick Hess (AEI)", "url": "https://www.aei.org/profile/frederick-m-hess/feed/", "tier": 2},
    {"name": "NHERI", "url": "https://nheri.org/feed/", "tier": 2},
    {"name": "1000 Hours Outside", "url": "https://www.1000hoursoutside.com/blog?format=rss", "tier": 2},
    {"name": "ClarifiEd", "url": "https://www.clarified.life/feed", "tier": 2},

    # Tier 3: Homeschool community blogs
    {"name": "Simply Charlotte Mason", "url": "http://simplycharlottemason.com/feed/", "tier": 3},
    {"name": "Christy-Faith", "url": "https://christy-faith.com/feed/", "tier": 3},
    {"name": "Days With Grey", "url": "https://dayswithgrey.com/feed/", "tier": 3},
    {"name": "Simple Homeschool", "url": "http://feeds.feedburner.com/simplehomeschool", "tier": 3},
    {"name": "The Natural Homeschool", "url": "http://www.thenaturalhomeschool.com/feed", "tier": 3},
    {"name": "Weird Unsocialized Homeschoolers", "url": "http://www.weirdunsocializedhomeschoolers.com/feed/", "tier": 3},
    {"name": "Raising Lifelong Learners", "url": "https://raisinglifelonglearners.com/feed/", "tier": 3},
    {"name": "A Humble Place", "url": "http://ahumbleplace.com/feed/", "tier": 3},
    {"name": "Home-Centered Learning", "url": "https://www.homecenteredlearning.com/blog?format=rss", "tier": 3},
    {"name": "Homeschool Better Together", "url": "http://feeds.feedburner.com/EverydaySnapshots", "tier": 3},
    {"name": "Homegrown Learners", "url": "http://www.homegrownlearners.com/home/atom.xml", "tier": 3},
    {"name": "Humility and Doxology", "url": "https://humilityanddoxology.com/feed/", "tier": 3},

    # Tier 4: Substacks & newsletters with direct RSS
    {"name": "Ed3 World", "url": "https://ed3world.substack.com/feed", "tier": 4},
    {"name": "Austin Scholar", "url": "https://austinscholar.substack.com/feed", "tier": 4},

    # Tier 5: Podcasts & video
    {"name": "Future of Education Podcast", "url": "https://futureofeducationpod.com/feed/", "tier": 5},
    {"name": "Hannah Frankman (YT)", "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCJc7RzwJ0tIvPPMAM3iHZGQ", "tier": 5},
    {"name": "NREA Podcast", "url": "https://feeds.simplecast.com/vLBlb6gi", "tier": 5},

    # Tier 6: News aggregators & Google alerts
    {"name": "Utah Fits All (Google News)", "url": "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=utah+fits+all", "tier": 6},
    {"name": "r/homeschool", "url": "https://api.reddit.com/subreddit/homeschool;best", "tier": 6},
]

# =============================================================================
# RELEVANCE FILTER PROMPT (based on OpenEd brand identity)
# =============================================================================

RELEVANCE_PROMPT = '''You are a content curator for OpenEd, an alternative education company helping families design personalized learning journeys.

Rate the following article for relevance to OpenEd's audience (1-5 scale):

TITLE: {title}
SOURCE: {source}
SUMMARY: {summary}

SCORING CRITERIA:

5 = HIGHLY RELEVANT - Must share
- Families mixing educational approaches (Charlotte Mason + Singapore Math + screens)
- Real stories of kids thriving outside traditional school
- Practical help for overwhelmed parents
- Research on homeschool/alternative education outcomes
- State-specific news for: AR, IN, IA, KS, MN, MT, NV, OR, UT

4 = GOOD FIT - Likely share
- General homeschool/unschool content with fresh perspective
- Neurodiversity and "doesn't fit the mold" angles
- Curriculum/method comparisons (without declaring winners)
- Parenting philosophy aligned with educational freedom

3 = MAYBE - Context-dependent
- General education news with possible OpenEd angle
- Policy news that affects homeschool families
- EdTech that could benefit homeschoolers

2 = WEAK FIT - Probably skip
- Public school focused with no homeschool angle
- Pure political school choice (no family/practical angle)
- Generic parenting content

1 = NOT RELEVANT - Skip
- Content that trashes public schools without offering alternatives
- Dogmatic single-method advocacy ("unschooling is the ONLY way")
- Clickbait or outrage-bait
- Paywalled content we can't verify

Respond with ONLY a JSON object:
{{"score": N, "reason": "1-2 sentence explanation", "angle": "OpenEd angle if score >= 4, else null"}}
'''

# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def fetch_feeds():
    """Fetch all feeds and return recent items."""
    items = []
    cutoff = datetime.now() - timedelta(hours=HOURS_LOOKBACK)

    for feed_info in HOMESCHOOL_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:5]:  # Limit per feed
                # Parse publication date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])

                # Skip old items
                if published and published < cutoff:
                    continue

                items.append({
                    "title": entry.get("title", "No title"),
                    "url": entry.get("link", ""),
                    "summary": entry.get("summary", "")[:500],  # Truncate
                    "source": feed_info["name"],
                    "tier": feed_info["tier"],
                    "published": published.isoformat() if published else None,
                })
        except Exception as e:
            print(f"Error fetching {feed_info['name']}: {e}", file=sys.stderr)

    return items


def filter_with_claude(items):
    """Use Claude CLI to score items for relevance."""
    scored = []

    for item in items:
        prompt = RELEVANCE_PROMPT.format(
            title=item["title"],
            source=item["source"],
            summary=item["summary"][:300]
        )

        try:
            result = subprocess.run(
                CLAUDE_CMD + [prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            response = result.stdout.strip()

            # Parse JSON response
            data = json.loads(response)
            item["score"] = data.get("score", 0)
            item["reason"] = data.get("reason", "")
            item["angle"] = data.get("angle")
            scored.append(item)

        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"Filtering error for '{item['title'][:50]}': {e}", file=sys.stderr)
            item["score"] = 0
            scored.append(item)

    # Sort by score (desc) then tier (asc)
    scored.sort(key=lambda x: (-x.get("score", 0), x.get("tier", 99)))
    return scored


def format_slack_message(item):
    """Format a single item for Slack."""
    tier_emoji = {1: "🔥", 2: "⭐", 3: "📚", 4: "📰", 5: "🎙️", 6: "🔍"}.get(item["tier"], "📄")
    score = item.get("score", "?")

    message = f"{tier_emoji} *{item['title']}*\n"
    message += f"_{item['source']}_ | Score: {score}/5\n"

    if item.get("angle"):
        message += f"\n💡 *OpenEd angle:* {item['angle']}\n"

    message += f"\n🔗 {item['url']}"

    return message


def post_to_slack(items, dry_run=False):
    """Post filtered items to Slack."""
    # Only post items scoring 4+
    top_items = [i for i in items if i.get("score", 0) >= 4][:MAX_ITEMS]

    if not top_items:
        print("No items scored 4+ today")
        return

    header = f"📰 *Daily Curation* - {datetime.now().strftime('%Y-%m-%d')}\n"
    header += f"{len(top_items)} items scored 4+ relevance\n"
    header += "─" * 40

    if dry_run:
        print("\n=== DRY RUN - Would post to Slack ===\n")
        print(header)
        for item in top_items:
            print("\n" + format_slack_message(item))
        return

    # TODO: Replace with actual Slack MCP call or webhook
    # For now, print instructions
    print(f"Ready to post {len(top_items)} items to {SLACK_CHANNEL}")
    print("Use Slack MCP: mcp__slack__conversations_add_message")


def main():
    dry_run = "--test" in sys.argv

    print(f"Fetching feeds (last {HOURS_LOOKBACK} hours)...")
    items = fetch_feeds()
    print(f"Found {len(items)} recent items")

    if not items:
        print("No new items to process")
        return

    print("Filtering with Claude...")
    scored = filter_with_claude(items)

    print("Posting to Slack...")
    post_to_slack(scored, dry_run=dry_run)

    print("Done!")


if __name__ == "__main__":
    main()
