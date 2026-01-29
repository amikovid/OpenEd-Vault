# RSS Curation Project

**Purpose:** Daily RSS curation for OpenEd's content pipeline with multi-platform distribution.

---

## Quick Start

1. Run daily fetch (last 24h from 64 feeds)
2. Score articles: DEFINITELY / PROBABLY / NO
3. Generate Ed the Horse drafts for X
4. Route to other platforms as appropriate
5. Output to `daily/YYYY-MM-DD.md` and `daily/YYYY-MM-DD-ed-posts.md`

---

## Project Structure

| File | Purpose |
|------|---------|
| `PROJECT.md` | This file - project overview |
| `FEEDS.md` | 64 verified RSS feeds with URLs |
| `references/ORCHESTRATION.md` | Platform routing, Ed voice, frameworks |
| `daily/` | Daily curation outputs |

---

## Feed Architecture

**64 feeds** organized by tier (see `FEEDS.md` for full list):

| Tier | Description | Count |
|------|-------------|-------|
| 1 | Thought Leaders | 10 |
| 1 | Core Homeschool | 4 |
| 2 | Homeschool Community | 10 |
| 2 | Classical & Charlotte Mason | 4 |
| 2 | Research & Unschooling | 4 |
| 2 | Education News | 5 |
| 2 | Microschools | 4 |
| 2 | Community (Reddit) | 2 |
| 3 | Policy (filter heavily) | 8 |
| 4 | Substacks & Emerging | 5 |
| 5 | Podcasts | 4 |

### Key Thought Leaders (Tier 1)
- Michael B. Horn, Kerry McDonald, Claire Honeycutt
- Peter Gray, Jon Haidt (After Babel), Freddie deBoer
- Rob Henderson, Let Grow, Lenore Skenazy

---

## Scoring Criteria

### DEFINITELY (Post to platforms)
- Families mixing approaches
- Kids thriving outside traditional school
- Practical parent help
- Relatable parent moments
- Neurodiversity focus

### PROBABLY (Review for framing)
- Fresh homeschool/alt-ed angle
- Curriculum comparisons
- Microschool models (family experience, not policy)

### NO (Skip)
- School choice policy/ESA news
- Political content
- Public school focused
- Generic parenting
- Clickbait
- Dogmatic religious content

---

## Platform Distribution

See `references/ORCHESTRATION.md` for full details.

| Platform | Persona | Content Type |
|----------|---------|--------------|
| X/Twitter | Ed the Horse | Hot takes, one-liners |
| LinkedIn | OpenEd | Data-driven, long-form |
| Facebook | OpenEd | Reddit screenshots, discussions |
| Instagram | OpenEd | Carousels, quote cards |
| Newsletter | OpenEd | Trend items, context pieces |

### Key Platform Notes
- **X:** 70-100 chars optimal, link at end
- **LinkedIn:** Put links in first comment (algorithm penalty)
- **Reddit:** Use screenshots, not direct links

---

## Daily Output Format

### Curation File (`daily/YYYY-MM-DD.md`)
```markdown
# Daily Curation - [Date]

## DEFINITELY (X items)
### 1. [Title]
**Source:** [Feed] | **Tier X**
**URL:** [Full URL]
**Why DEFINITELY:** [Reason]

## PROBABLY (X items)
[Same format]

## NO (X items) - Skip
| Title | Source | Reason |
```

### Ed Posts File (`daily/YYYY-MM-DD-ed-posts.md`)
```markdown
# Ed the Horse - Daily Posts

## Item 1: [Title]
**Source:** [Author/Publication]
**URL:** [Full URL]

### 5 Post Options
1. **Pattern Name**
   > Post text
   > [link]

**Pick:** #X - [Reason]

---

## Platform Routing Summary
| Article | Platform | Format | Status |
```

---

## User Preferences

- Mark favorites with `***` asterisks
- Insert comments with `< >` brackets
- Final picks go in scheduling table

---

## Workflow Integration

After curation, content can flow to:
- `text-content` skill for template matching
- `content-repurposer` for multi-platform drafts
- `newsletter-to-social` for newsletter integration
- Slack `#content-inbox` for team review

---

## Technical Notes

### Feed URL Formats
- Substack: `{name}.substack.com/feed`
- WordPress: `{domain}/feed/`
- Reddit: `reddit.com/r/{subreddit}/.rss`
- Medium: `medium.com/feed/@{username}`

### No RSS Available (Manual Check)
- Fab Fridays (Ana Lorena Fabrega)
- HSLDA
- Well-Trained Mind
- John Holt GWS
- Prenda
- Synthesis School

---

## History

**2026-01-29:** Project created. Consolidated 64 verified feeds. Created Ed the Horse persona. Built multi-platform orchestration system.

---

*Related skills:* `rss-curation`, `text-content`, `content-repurposer`
