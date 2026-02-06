#!/usr/bin/env python3
"""
RSS Daily Curation - Automated Feed Scoring and Slack Posting

Fetches from 64 education/homeschool feeds, scores using DEFINITELY/PROBABLY/NO
criteria, and posts curated items to Slack.

Run manually: python3 agents/rss_curation.py
Run via cron: 0 6 * * * cd ~/Desktop/New\ Root\ Docs/OpenEd\ Vault && python3 agents/rss_curation.py

Environment: Requires SLACK_BOT_TOKEN in .env
"""

import os
import re
import json
import feedparser
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import time

# Load environment
load_dotenv(Path(__file__).parent.parent / ".env")

# Tracking file path
TRACKING_PATH = Path(__file__).parent.parent / "Projects/RSS-Curation/tracking.json"


def load_tracking() -> dict:
    """Load tracking data from JSON file"""
    try:
        with open(TRACKING_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lastRun": None, "items": {}, "stats": {"totalTracked": 0, "duplicatesPrevented": 0}}


def save_tracking(tracking: dict):
    """Save tracking data to JSON file"""
    tracking["lastRun"] = datetime.now().isoformat()
    with open(TRACKING_PATH, 'w') as f:
        json.dump(tracking, f, indent=2)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "C07U9S53TLL"  # #market-daily channel ID

# All 64 feeds organized by tier
FEEDS = [
    # Tier 1 - Thought Leaders (10)
    ("Michael B. Horn", "https://michaelbhorn.substack.com/feed"),
    ("Kerry McDonald", "https://forbes.com/sites/kerrymcdonald/feed/"),
    ("Claire Honeycutt", "https://honeycutt.substack.com/feed"),
    ("Peter Gray", "https://petergray.substack.com/feed"),
    ("After Babel (Jon Haidt)", "https://afterbabel.com/feed"),
    # REMOVED: Off-topic culture commentary, not homeschool-relevant
    # ("Freddie deBoer", "https://freddiedeboer.substack.com/feed"),
    # ("Rob Henderson", "https://robkhenderson.substack.com/feed"),
    ("Let Grow", "https://letgrow.org/feed/"),
    ("Corey DeAngelis", "https://deangeliscorey.substack.com/feed"),
    ("Lenore Skenazy", "https://reason.com/people/lenore-skenazy/feed/"),

    # Tier 1 - Core Homeschool (4)
    ("Pam Barnhill", "https://pambarnhill.com/feed/"),
    ("Simple Homeschool", "https://simplehomeschool.net/feed/"),
    ("Brave Writer", "https://blog.bravewriter.com/feed/"),
    ("1000 Hours Outside", "https://1000hoursoutside.com/blog?format=rss"),

    # Tier 2 - Homeschool Community (10)
    ("The Homeschool Mom", "https://thehomeschoolmom.com/feed/"),
    ("Hip Homeschool Moms", "https://hiphomeschoolmoms.com/feed/"),
    ("Homeschool Hideout", "https://homeschoolhideout.com/feed/"),
    ("Fearless Homeschool", "https://fearlesshomeschool.com/feed/"),
    ("Homeschool Boss", "https://homeschoolboss.com/feed/"),
    ("A Gentle Feast", "https://agentlefeast.com/feed/"),
    ("Homeschool Your Boys", "https://homeschoolyourboys.com/feed/"),
    ("Secular Homeschool", "https://secularhomeschooler.com/feed/"),
    ("Hybrid Homeschool Project", "https://hybridhomeschoolproject.com/feed/"),
    ("Raising Lifelong Learners", "https://raisinglifelonglearners.com/feed/"),

    # Tier 2 - Classical & Charlotte Mason (4)
    ("Classical Conversations", "https://classicalconversations.com/blog/feed/"),
    ("CiRCE Institute", "https://circeinstitute.org/blog/feed/"),
    ("Simply Charlotte Mason", "https://simplycharlottemason.com/blog/feed/"),
    ("Memoria Press", "https://memoriapress.com/feed/"),

    # Tier 2 - Research & Unschooling (4)
    ("NHERI", "https://nheri.org/feed/"),
    ("Alliance for Self-Directed Education", "https://self-directed.org/feed/"),
    ("Peter Gray - Psychology Today", "https://psychologytoday.com/us/blog/freedom-learn/feed"),
    ("Sudbury Valley School", "https://sudburyvalley.org/feed"),

    # Tier 2 - Education News (5)
    ("The 74 Million", "https://the74million.org/feed/"),
    ("EdSurge", "https://edsurge.com/news.rss"),
    ("Getting Smart", "https://gettingsmart.com/feed/"),
    ("EdWeek", "https://edweek.org/feed"),
    ("Chalkbeat", "https://chalkbeat.org/arc/outboundfeeds/rss/"),

    # Tier 2 - Microschools (4)
    ("Acton Academy", "https://actonacademy.org/feed/"),
    ("KaiPod Learning", "https://kaipodlearning.com/blog-feed.xml"),
    ("VELA Education Fund", "https://velaedfund.org/feed/"),
    ("Outschool", "https://outschool.com/blog/feed"),

    # Tier 2 - Community (2) - GOLD MINES
    ("r/homeschool", "https://www.reddit.com/r/homeschool/.rss"),
    ("r/unschool", "https://www.reddit.com/r/unschool/.rss"),

    # Tier 3 - Policy (8) - Filter heavily
    ("Education Next", "https://educationnext.org/feed/"),
    ("Reason Education", "https://reason.com/tag/education/feed/"),
    ("Cato Education", "https://cato.org/research/education/rss.xml"),
    ("EdChoice", "https://edchoice.org/feed/"),
    ("Rick Hess - AEI", "https://aei.org/profile/frederick-m-hess/feed/"),
    ("CRPE", "https://crpe.org/feed/"),
    ("Pioneer Institute", "https://pioneerinstitute.org/topic/education/feed/"),
    ("School Choice Week", "https://schoolchoiceweek.com/feed/"),

    # Tier 4 - Substacks & Emerging (5)
    ("Ed3 World", "https://ed3world.substack.com/feed"),
    ("Austin Scholar", "https://austinscholar.substack.com/feed"),
    ("Jay Wamstead", "https://jaywamsted.substack.com/feed"),
    ("Hannah Frankman", "https://hannahfrankman.substack.com/feed"),
    ("Rebel Educator", "https://rebeleducator.substack.com/feed"),

    # Tier 5 - Podcasts (4)
    ("Future of Education Podcast", "https://feeds.simplecast.com/XppMFbfg"),
    ("Homeschool Solutions Podcast", "https://homeschoolsolutionsshow.com/feed/podcast/"),
    ("Read-Aloud Revival", "https://readaloudrevival.com/feed/podcast/"),
    ("Brave Learner Podcast", "https://feeds.libsyn.com/421298/rss"),
]

# Scoring keywords
DEFINITELY_KEYWORDS = [
    # Mixed approach / flexibility
    "mix", "hybrid", "both", "different", "one child", "not the other",
    "what works", "respecting", "individuality",

    # Kids thriving
    "thriving", "flourishing", "loving", "excited", "passionate",
    "self-directed", "curiosity", "wonder",

    # Practical help
    "how to", "tips", "ideas", "resources", "curriculum",
    "schedule", "routine", "planning",

    # Relatable moments
    "struggle", "hard day", "overwhelmed", "joy", "proud",
    "dad", "father", "single parent", "working parent",

    # Neurodiversity
    "adhd", "autism", "dyslexia", "learning difference",
    "special needs", "twice exceptional", "2e",

    # Free-range / independence
    "free-range", "independence", "trust", "let them",
    "play", "outdoor", "nature",
]

NO_KEYWORDS = [
    # Policy/Political
    "esa", "voucher", "school choice week", "legislation",
    "trump", "biden", "republican", "democrat", "congress",
    "ice raid", "immigration", "deportation",
    "moms for liberty", "culture war", "book review",
    "universal eligibility", "universal access",

    # Public school focused
    "public school", "district", "superintendent", "principal",
    "classroom", "school board", "standardized test",
    "charter school", "charter agreement",
    "pre-k application", "3-k application",
    "school closure", "school safety officer",
    "snow day", "weather day",

    # State/local politics (not homeschool-specific)
    "governor", "lawmakers", "legislature", "bill tracker",

    # Off-topic health/misc
    "oral health", "school chef", "healthy habits",
    "child care", "day care",

    # Religious/devotional
    "biblical perspective", "psalm", "scripture", "devotional",
    "prayer life", "faith-based", "christian school",

    # Union/labor politics
    "teachers union", "union strike", "staffing demands",
    "pay equity", "pay gap",

    # Generic/off-topic
    "college admission", "higher ed", "university",
    "corporate training", "workplace",
]

# High-value sources (always consider DEFINITELY if not filtered out)
HIGH_VALUE_SOURCES = [
    "Lenore Skenazy", "Peter Gray", "Let Grow", "Kerry McDonald",
    "Pam Barnhill", "1000 Hours Outside",
    "Jon Haidt", "After Babel",
]

# Reddit requires higher bar - generic posts shouldn't auto-qualify
REDDIT_DEFINITELY_KEYWORDS = [
    # Only high-signal Reddit discussions
    "thriving", "flourishing", "self-directed", "unschooling success",
    "data", "research", "study", "statistic",
    "documentary", "nyt", "new york times", "washington post",
    "microschool", "learning pod", "forest school",
    "neurodiversity", "twice exceptional", "2e",
    "college admission", "sat", "act score",
    "socialization", "social skills",
]


def score_item(source: str, title: str, summary: str) -> str:
    """Score an item as DEFINITELY, PROBABLY, or NO"""
    text = (title + " " + summary).lower()

    # Check NO keywords first (filter out)
    for kw in NO_KEYWORDS:
        if kw.lower() in text:
            return "NO"

    # Reddit has a separate, higher bar
    if "r/" in source:
        return score_reddit_item(text)

    # Check DEFINITELY keywords
    definitely_score = 0
    for kw in DEFINITELY_KEYWORDS:
        if kw.lower() in text:
            definitely_score += 1

    # Boost for high-value sources
    if any(hv in source for hv in HIGH_VALUE_SOURCES):
        definitely_score += 2

    if definitely_score >= 2:
        return "DEFINITELY"
    elif definitely_score >= 1:
        return "PROBABLY"
    else:
        return "PROBABLY"  # Default to PROBABLY, not NO


def score_reddit_item(text: str) -> str:
    """Score Reddit items with a higher bar - only strong signals qualify"""
    # Reddit DEFINITELY requires specific high-signal keywords
    reddit_score = 0
    for kw in REDDIT_DEFINITELY_KEYWORDS:
        if kw.lower() in text:
            reddit_score += 1

    # Also check general DEFINITELY keywords but require more matches
    general_score = 0
    for kw in DEFINITELY_KEYWORDS:
        if kw.lower() in text:
            general_score += 1

    if reddit_score >= 1 and general_score >= 1:
        return "DEFINITELY"
    elif reddit_score >= 1 or general_score >= 2:
        return "PROBABLY"
    elif general_score >= 1:
        return "PROBABLY"
    else:
        return "NO"  # Generic Reddit posts filtered out


def get_description(source: str, title: str) -> str:
    """Generate a short description for why this item is interesting"""
    title_lower = title.lower()

    if "dad" in title_lower or "father" in title_lower:
        return "Unique dad perspective, relatable"
    elif "one child" in title_lower or "not the other" in title_lower:
        return "Mixed approach families - respecting individuality"
    elif any(x in title_lower for x in ["free-range", "soccer", "play", "outdoor"]):
        return "Free-range parenting, trusting kids"
    elif any(x in title_lower for x in ["restrain", "seclud", "special needs", "adhd"]):
        return "Special needs angle - why families leave school"
    elif any(x in title_lower for x in ["joy", "steal", "overwhelm", "struggle"]):
        return "Relatable parent moment"
    elif any(x in title_lower for x in ["curriculum", "math", "reading"]):
        return "Practical parent help - curriculum"
    elif any(x in title_lower for x in ["phone", "screen", "tech"]):
        return "Digital wellness / screen time"
    elif "r/" in source:
        return "Community discussion - conversation starter"
    elif source in HIGH_VALUE_SOURCES:
        return f"Thought leader content from {source}"
    else:
        return "Fresh perspective on education"


def fetch_feeds(hours: int = 24, tracking: dict = None) -> list:
    """Fetch all feeds and return items from last N hours, skipping tracked URLs"""
    cutoff = datetime.now() - timedelta(hours=hours)
    items = []
    errors = []
    skipped = 0
    tracked_urls = set(tracking.get("items", {}).keys()) if tracking else set()

    print(f"Fetching {len(FEEDS)} feeds (last {hours} hours)...")
    print(f"Tracking {len(tracked_urls)} known URLs for deduplication")

    for name, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:  # Max 10 per feed
                title = entry.get('title', 'No title')[:120]
                link = entry.get('link', '')
                summary = entry.get('summary', '')[:300]

                # Skip if already tracked
                if link in tracked_urls:
                    skipped += 1
                    continue

                # Clean HTML from summary
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = re.sub(r'\s+', ' ', summary).strip()

                # Parse date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                if pub_date and pub_date > cutoff:
                    score = score_item(name, title, summary)
                    items.append({
                        'source': name,
                        'title': title,
                        'link': link,
                        'summary': summary,
                        'date': pub_date.strftime('%Y-%m-%d'),
                        'score': score,
                        'description': get_description(name, title),
                    })
        except Exception as e:
            errors.append(f"{name}: {str(e)[:50]}")

        time.sleep(0.2)  # Rate limiting

    if skipped:
        print(f"Skipped {skipped} already-tracked URLs")
    if errors:
        print(f"Errors ({len(errors)}): {', '.join(errors[:5])}...")

    return items


def format_slack_message(items: list) -> str:
    """Format DEFINITELY items for Slack"""
    definitely_items = [i for i in items if i['score'] == 'DEFINITELY']

    if not definitely_items:
        return None

    date_range = datetime.now().strftime('%b %d')

    lines = [
        f"📬 *RSS Curation - {date_range}*",
        f"",
        f"{len(definitely_items)} high-quality items for potential social content. React with ✅ to claim, ❌ to skip.",
        "",
        "---",
    ]

    for i, item in enumerate(definitely_items[:10], 1):  # Max 10
        lines.append(f"")
        lines.append(f"*{i}. {item['title']}* ({item['source']})")
        lines.append(f"{item['link']}")
        lines.append(f"_{item['description']}_")
        lines.append("")
        lines.append("---")

    lines.append("")
    lines.append("_Curated via RSS Curation system • Reply in thread to discuss_")

    return "\n".join(lines)


def post_to_slack(message: str, channel: str = SLACK_CHANNEL) -> bool:
    """Post message to Slack using bot token"""
    if not SLACK_BOT_TOKEN:
        print("ERROR: No SLACK_BOT_TOKEN in environment")
        return False

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "channel": channel,
            "text": message,
            "mrkdwn": True,
        }
    )

    result = response.json()
    if not result.get("ok"):
        print(f"Slack error: {result.get('error')}")
        return False

    return True


def save_daily_output(items: list):
    """Save scored items to daily markdown file"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_path = Path(__file__).parent.parent / f"Projects/RSS-Curation/daily/{date_str}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    definitely = [i for i in items if i['score'] == 'DEFINITELY']
    probably = [i for i in items if i['score'] == 'PROBABLY']

    content = [
        f"# RSS Curation - {date_str}",
        "",
        f"**Total fetched:** {len(items)}",
        f"**DEFINITELY:** {len(definitely)}",
        f"**PROBABLY:** {len(probably)}",
        "",
        "---",
        "",
        "## DEFINITELY",
        "",
    ]

    for item in definitely:
        content.append(f"### {item['title']}")
        content.append(f"**Source:** {item['source']}")
        content.append(f"**URL:** {item['link']}")
        content.append(f"**Why:** {item['description']}")
        content.append("")

    content.append("---")
    content.append("")
    content.append("## PROBABLY")
    content.append("")

    for item in probably[:15]:  # Limit PROBABLY list
        content.append(f"- [{item['title']}]({item['link']}) ({item['source']})")

    output_path.write_text("\n".join(content))
    print(f"Saved to {output_path}")


def main():
    import sys

    print(f"RSS Daily Curation - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Parse --hours flag; default: auto-calculate from lastRun
    hours = None
    for arg in sys.argv:
        if arg.startswith("--hours="):
            hours = int(arg.split("=")[1])

    # Load tracking for deduplication
    tracking = load_tracking()
    last_run = tracking.get('lastRun')
    print(f"Last run: {last_run or 'never'}")

    # Auto-calculate hours from lastRun if not specified
    if hours is None:
        if last_run:
            last_run_dt = datetime.fromisoformat(last_run)
            hours_since = (datetime.now() - last_run_dt).total_seconds() / 3600
            hours = max(int(hours_since) + 1, 6)  # At least 6h, round up
            print(f"Auto-fetching since last run: {hours} hours")
        else:
            hours = 48  # First run: cast a wider net
            print(f"First run - fetching last {hours} hours")

    # Fetch and score (with deduplication)
    items = fetch_feeds(hours=hours, tracking=tracking)
    print(f"\nFetched {len(items)} NEW items from last {hours} hours")

    # Add new items to tracking
    today = datetime.now().strftime('%Y-%m-%d')
    for item in items:
        if item['link'] not in tracking['items']:
            tracking['items'][item['link']] = {
                'firstSeen': today,
                'score': item['score'].lower(),
                'status': 'new',
                'source': item['source'],
                'title': item['title'][:100],
                'summary': item.get('summary', '')[:300],
            }
            tracking['stats']['totalTracked'] = len(tracking['items'])

    # Save tracking
    save_tracking(tracking)
    print(f"Tracking updated: {tracking['stats']['totalTracked']} total URLs")

    # Count by score
    definitely = [i for i in items if i['score'] == 'DEFINITELY']
    probably = [i for i in items if i['score'] == 'PROBABLY']
    print(f"DEFINITELY: {len(definitely)} | PROBABLY: {len(probably)}")

    # Save to file
    save_daily_output(items)

    # Check for --no-slack flag
    if "--no-slack" in sys.argv:
        print("Skipping Slack post (--no-slack)")
        print("\nDone.")
        return

    # Post to Slack
    if definitely:
        message = format_slack_message(items)
        if message:
            if post_to_slack(message):
                print(f"✓ Posted {len(definitely)} items to Slack")
            else:
                print("✗ Failed to post to Slack (bot may need to be added to channel)")
                print("  Run: /invite @YourBot in the Slack channel")
                print("  Or use Claude Code MCP to post from the daily file")
    else:
        print("No DEFINITELY items to post")

    print("\nDone.")


if __name__ == "__main__":
    main()
