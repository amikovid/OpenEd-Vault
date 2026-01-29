# RSS Curation Context Handoff

**Purpose:** Context package for starting the SEO Content Refresh project. Includes all RSS curation infrastructure built in the January 29, 2026 session.

---

## What Was Built

### 1. RSS Feed Infrastructure

**Location:** `Projects/RSS-Curation/`

**64 verified feeds** organized by tier:

| Tier | Category | Count | Examples |
|------|----------|-------|----------|
| 1 | Thought Leaders | 10 | Lenore Skenazy, Peter Gray, Kerry McDonald, Jon Haidt |
| 1 | Core Homeschool | 4 | Pam Barnhill, Brave Writer, 1000 Hours Outside |
| 2 | Community | 12 | r/homeschool, r/unschool (gold mines) |
| 2 | Education News | 5 | The 74 Million, Chalkbeat, EdSurge |
| 3 | Policy | 8 | Education Next, EdChoice (filter heavily) |

**Full feed list:** `Projects/RSS-Curation/FEEDS.md`

### 2. Scoring System

Three-tier scoring for content curation:

**DEFINITELY** (Post immediately)
- Families mixing approaches
- Kids thriving outside traditional school
- Practical parent help
- Relatable parent moments
- Neurodiversity focus

**PROBABLY** (Review for framing)
- Fresh homeschool/alt-ed angle
- Curriculum comparisons
- Microschool models (family experience, not policy)

**NO** (Skip)
- School choice policy/ESA news
- Political content
- Public school focused
- Generic parenting

### 3. Fetch Script Pattern

Working Python pattern that preserves full URLs:

```python
import feedparser
from datetime import datetime, timedelta

FEEDS = [
    ("Lenore Skenazy", "https://reason.com/people/lenore-skenazy/feed/"),
    ("r/homeschool", "https://www.reddit.com/r/homeschool/.rss"),
    ("The 74 Million", "https://www.the74million.org/feed/"),
    # ... 64 total feeds in FEEDS.md
]

cutoff = datetime.now() - timedelta(hours=48)  # Configurable window

for name, url in FEEDS:
    feed = feedparser.parse(url)
    for entry in feed.entries[:10]:
        # Key fields to preserve:
        title = entry.get('title')
        link = entry.get('link')  # CRITICAL: Full URL
        summary = entry.get('summary', '')[:300]
        pub_date = entry.published_parsed if hasattr(entry, 'published_parsed') else None
```

### 4. Output Format

Daily curation outputs to:
- `daily/YYYY-MM-DD.md` - Scored articles with full URLs
- `daily/YYYY-MM-DD-ed-posts.md` - Platform-ready drafts

### 5. Platform Integration

**Getlate API** for scheduling:
- Account ID (Twitter): `696135064207e06f4ca849a1`
- Accounts connected: X, LinkedIn, Instagram, Facebook, Pinterest, TikTok, YouTube, Reddit
- Working POST endpoint for scheduling

---

## Key Learnings

1. **URL preservation is critical** - Must flow from RSS fetch → scoring → drafts → posting
2. **Reddit is a gold mine** - r/homeschool yields 4-5 DEFINITELY items per day
3. **Time windows matter** - 24h for daily curation, 30-60 days for SEO refresh context
4. **Source handles** - Need to capture X handles during curation (e.g., @The74)

---

## Adaptation for SEO Refresh

The RSS system can be adapted for SEO content refresh by:

### 1. Configurable Time Windows
```python
# Daily newsletter: 24 hours
cutoff = datetime.now() - timedelta(hours=24)

# SEO refresh context: 30-60 days
cutoff = datetime.now() - timedelta(days=30)
```

### 2. Keyword Filtering
Add keyword matching to find discussions relevant to specific declining pages:

```python
target_keywords = ["homeschool math", "curriculum comparison", "state requirements"]

for entry in feed.entries:
    text = (entry.title + entry.summary).lower()
    if any(kw in text for kw in target_keywords):
        # This entry is relevant to a declining page
```

### 3. Source Attribution
Track which feeds/discussions could update which pages:

| Declining Page | Relevant Feeds | Keyword Filter |
|----------------|----------------|----------------|
| /homeschool-math-curriculum | r/homeschool, Kerry McDonald | math, curriculum |
| /utah-homeschool-laws | HSLDA, r/homeschool | utah, requirements |

---

## Integration Points for SEO Refresh

### GSC → Topic Extraction
1. Query GSC for position drops (seomachine skill)
2. Extract topics from declining URLs
3. Convert to keyword filters for RSS feeds

### RSS → Fresh Content
1. Run RSS fetch with topic keywords
2. Filter to 30-60 day window
3. Score for authority/relevance
4. Package as source material

### Output for Content Updates
```markdown
## Refresh Package: [Page Title]

**Current performance:** Position dropped from X to Y

### Fresh Source Material (Last 30 Days)

1. **[Article Title]** - [Source]
   URL: [full link]
   Key quote: "[relevant excerpt]"

2. **[Reddit Discussion]** - r/homeschool
   URL: [full link]
   Top insight: "[comment summary]"
```

---

## Files to Reference

| File | Purpose |
|------|---------|
| `Projects/RSS-Curation/PROJECT.md` | Project overview |
| `Projects/RSS-Curation/FEEDS.md` | 64 verified feeds |
| `Projects/RSS-Curation/references/ORCHESTRATION.md` | Platform routing |
| `.claude/skills/seomachine/modules/google_search_console.py` | GSC queries |
| `.claude/skills/seomachine/modules/google_analytics.py` | GA4 queries |

---

## Prompt for New Thread

Use this to start the SEO refresh thread:

```
Continue the SEO content refresh automation project.

CONTEXT FROM RSS CURATION SESSION:
- RSS infrastructure exists at Projects/RSS-Curation/ with 64 verified education feeds
- Working Python fetch pattern with feedparser
- Scoring system (DEFINITELY/PROBABLY/NO) already defined
- Time windows configurable (24h for daily, 30-60 days for refresh)
- See HANDOFF-SEO-REFRESH.md for full technical context

GOAL: Build a content refresh agent that:
1. Identifies declining pages via GSC (position drops, traffic drops)
2. Finds recent authoritative discussions using RSS feeds + Reddit
3. Generates update suggestions with fresh source material

SPECIFIC TASKS:
1. Create GSC declining pages query (adapt seomachine skill)
2. Add keyword filtering to RSS fetch for topic matching
3. Build weekly workflow that outputs prioritized refresh queue

DO NOT write new content. Focus on building the automation infrastructure.
```

---

*Generated: 2026-01-29*
