# Curation Pipeline - Implementation Plan

**Goal:** Daily curated content suggestions from RSS feeds and industry sources, posted to Slack for human triage.

---

## Overview

```
RSS FEEDS → PARSER → RELEVANCE FILTER → SLACK SUGGESTION → HUMAN TRIAGE → CONTENT
```

---

## Components

### 1. RSS Feed Sources

**Primary feeds (education/homeschool):**
- Reason Foundation education
- Cato education
- FEE (Foundation for Economic Education)
- HSLDA news
- Coalition for Responsible Home Education
- Homeschool news aggregators

**Secondary feeds (general interest):**
- Marginal Revolution (Tyler Cowen)
- Astral Codex Ten (Scott Alexander)
- Matt Levine (business angle)
- Selected Substacks

**Format:** OPML file with all feeds

### 2. Parser (Python)

**Existing:** Adapt `rss_parser.py` if available

**Requirements:**
- Parse multiple RSS feeds
- Extract: title, summary, URL, publish date
- Dedupe by URL
- Filter by recency (last 24-48 hours)

**Output:** JSON array of candidate items

### 3. Relevance Filter

**Keyword matching:**
- Education, homeschool, unschool
- Learning, curriculum, pedagogy
- School choice, education policy
- Parenting, child development
- Technology + learning

**Exclusion patterns:**
- Pure political (no education angle)
- Clickbait patterns
- Paywalled (can't verify relevance)

**Output:** Filtered list with relevance score

### 4. Slack Integration

**Channel:** #curation-inbox

**Message format:**
```
📰 CURATED: [Source Name]

*[Title]*
[2-3 sentence summary]

🔗 [URL]

*OpenEd angle:* [Suggested connection to our content]

✅ Use for newsletter | 🐦 Tweet | ❌ Skip
```

### 5. Human Triage

**Daily workflow:**
1. Review #curation-inbox (5-10 items)
2. React to keep/skip
3. Items marked "Use" go to content queue

### 6. Content Promotion

**Skill:** `/curate-to-content`

When human selects an item:
1. Fetch full article (WebFetch)
2. Extract key insight
3. Generate OpenEd angle/take
4. Draft newsletter TREND segment OR social post
5. Apply quality loop

---

## Technical Implementation

### Phase 1: Feed Setup

1. Create OPML file with all feeds
2. Test feed parsing
3. Verify output format

### Phase 2: Parser Script

```python
# curation_parser.py

import feedparser
from datetime import datetime, timedelta

FEEDS = [
    # OPML or direct feed list
]

KEYWORDS = [
    "education", "homeschool", "learning",
    "school choice", "curriculum", ...
]

def parse_feeds():
    items = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # Extract, filter, score
            pass
    return items

def filter_relevant(items, threshold=0.5):
    # Keyword matching
    pass

def post_to_slack(items):
    # Slack MCP or API
    pass
```

### Phase 3: Scheduling

**Option A: Cron job**
- Run daily at 6am
- Posts to Slack

**Option B: Manual trigger**
- `/curate` slash command
- Runs on demand

### Phase 4: Curate-to-Content Skill

Create skill that takes a curated URL and:
1. Fetches content
2. Summarizes
3. Generates OpenEd take
4. Drafts content (newsletter segment or social)

---

## File Structure

```
Studio/_content-engine-refactor/curation/
├── PLAN.md                  # This file
├── feeds.opml               # RSS feed list
├── scripts/
│   ├── curation_parser.py   # Main parser
│   └── slack_poster.py      # Slack integration
└── config/
    ├── keywords.json        # Relevance keywords
    └── exclusions.json      # Patterns to skip
```

---

## Timeline

| Week | Deliverable |
|------|-------------|
| 1 | Feed list compiled, OPML created |
| 1 | Parser script adapted from existing |
| 2 | Relevance filter tested |
| 2 | Slack integration working |
| 3 | Daily run scheduled |
| 3 | /curate-to-content skill created |

---

## Success Metrics

- **Volume:** 5-10 suggestions daily
- **Relevance:** >70% items marked "useful" by human
- **Conversion:** 2-3 items/week become content
- **Time saved:** Reduce research time by ~30 min/day

---

## Dependencies

- Slack MCP (for posting)
- feedparser Python library
- Existing RSS parser code (if any)
- WebFetch (for full article retrieval)

---

## Related

- `archive-suggest` - Similar pattern for internal content
- `newsletter-to-social` - Output destination
- `opened-daily-newsletter-writer` - TREND segment source
