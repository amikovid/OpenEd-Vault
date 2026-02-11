# Content Performance Scoring System

## Purpose

Close the feedback loop between published content and editorial decisions. Every piece of content gets a performance score. Scores flow back into Notion. Charlie sees what's working at a glance when approving, planning, or triaging content.

## The Problem This Solves

The vault has analytics infrastructure scattered across 6 modules (GA4, GSC, HubSpot, YouTube, Meta, DataForSEO). The data exists but never reaches the point of decision. Charlie approves content in Notion and Slack without knowing what similar content did last time.

This skill connects analytics data TO content records so performance informs every future decision.

---

## Architecture

```
EXISTING ANALYTICS MODULES          THIS SYSTEM              DECISION POINTS
--------------------------          -----------              ---------------
GA4 (blog traffic)          -->                      -->  Notion: score visible
Meta (FB + IG engagement)   -->   Performance         -->  Slack: score in post
YouTube (views, engagement) -->   Scoring Agent       -->  Weekly digest: top/bottom
HubSpot (conversions, CRM)  -->   (agents/             -->  Planning: theme scores
GSC (keyword positions)     -->    content_             -->  Archive: resurface
                                   performance_             high scorers
                                   agent.py)
                                      |
                                      v
                                  Notion Master
                                  Content Database
                                  (new fields)
```

---

## Scoring Algorithm

### Content Type Determines Which Metrics Matter

Not all content is measured the same way. A newsletter and a LinkedIn post serve different purposes and have different success signals.

#### Blog / SEO Content (scored from GA4 + GSC + HubSpot)

| Metric | Weight | Source | Why |
|--------|--------|--------|-----|
| Pageviews (30d) | 25% | GA4 | Raw traffic volume |
| Engagement rate | 20% | GA4 | Quality of visit |
| Organic impressions | 15% | GSC | Search visibility |
| CTR from search | 15% | GSC | Title/meta effectiveness |
| Conversions | 15% | HubSpot | Business impact |
| Trend direction | 10% | GA4 | Growing or declining |

**Scoring scale:** 0-100, normalized against the site's own performance distribution.

**Normalization:** Each metric is scored relative to the vault's content library. A page with pageviews at the 80th percentile of all OpenEd blog posts gets 80 for that metric component. This means scores automatically adjust as the site grows.

```
blog_score = (
    percentile_rank(pageviews) * 0.25 +
    percentile_rank(engagement_rate) * 0.20 +
    percentile_rank(impressions) * 0.15 +
    percentile_rank(ctr) * 0.15 +
    percentile_rank(conversions) * 0.15 +
    trend_bonus * 0.10
)
```

**Trend bonus:** rising = 100, stable = 50, declining = 0

---

#### Social Posts (scored from platform APIs)

| Metric | Weight | Why |
|--------|--------|-----|
| Impressions | 20% | Reach |
| Engagement rate | 35% | Resonance (the thing we most want to optimize) |
| Saves / Bookmarks | 20% | Deep value signal (people want to return to it) |
| Shares / Reposts | 15% | Amplification |
| Comments | 10% | Conversation starter |

**Platform-specific adjustments:**
- **LinkedIn:** Comments weighted higher (25%) because LinkedIn's algorithm heavily rewards comments
- **X:** Reposts weighted higher (25%) because X's algorithm rewards virality
- **Instagram:** Saves weighted higher (30%) because saves are Instagram's strongest engagement signal
- **Facebook:** Shares weighted higher (25%) because Facebook reach depends on sharing

```
social_score = (
    percentile_rank(impressions) * impressions_weight +
    percentile_rank(engagement_rate) * engagement_weight +
    percentile_rank(saves) * saves_weight +
    percentile_rank(shares) * shares_weight +
    percentile_rank(comments) * comments_weight
)
```

Weights vary by platform (see platform_weights dict in agent).

---

#### Newsletter (scored from HubSpot email campaigns)

| Metric | Weight | Why |
|--------|--------|-----|
| Open rate | 30% | Subject line effectiveness |
| Click rate | 35% | Content resonance |
| Unsubscribe rate (inverse) | 15% | Didn't drive people away |
| Reply rate | 20% | Deep engagement |

```
newsletter_score = (
    percentile_rank(open_rate) * 0.30 +
    percentile_rank(click_rate) * 0.35 +
    inverse_percentile_rank(unsubscribe_rate) * 0.15 +
    percentile_rank(reply_rate) * 0.20
)
```

---

#### Podcast (scored from YouTube + GA4 for blog post)

| Metric | Weight | Why |
|--------|--------|-----|
| YouTube views | 25% | Primary distribution reach |
| YouTube engagement rate | 20% | Quality signal |
| Blog post pageviews | 20% | SEO derivative value |
| Clip performance (avg) | 20% | Derivative content value |
| Download count | 15% | Podcast platform reach (if available) |

---

### Score Interpretation

| Score | Label | Meaning |
|-------|-------|---------|
| 80-100 | Top Performer | Resurface, create more like this, study what worked |
| 60-79 | Strong | Working well, good baseline |
| 40-59 | Average | Normal performance, no action needed |
| 20-39 | Underperforming | Review why - wrong platform? wrong time? weak hook? |
| 0-19 | Poor | Learn from this - don't repeat the pattern |

---

## Notion Schema Extension

### New Properties for Master Content Database

Add these fields to the existing database (`9a2f5189-6c53-4a9d-b961-3ccbcb702612`):

| Property | Type | Purpose |
|----------|------|---------|
| `Performance Score` | number | 0-100 composite score |
| `Score Label` | select | Top Performer / Strong / Average / Underperforming / Poor |
| `Impressions` | number | Total impressions/views across platforms |
| `Engagements` | number | Total likes + comments + shares + saves |
| `Engagement Rate` | number | Engagements / Impressions as percentage |
| `Clicks` | number | Link clicks (social) or pageviews (blog) |
| `Conversions` | number | HubSpot-tracked conversions (blog only) |
| `Trend` | select | Rising / Stable / Declining |
| `Last Scored` | date | When analytics were last pulled |
| `Platform Post IDs` | rich_text | JSON mapping: {"x": "id", "linkedin": "id", "getlate": "id"} |
| `Content Theme` | multi_select | Topic tags for theme-level analysis |
| `Score Notes` | rich_text | AI-generated one-line insight ("Outperformed avg by 3x on LinkedIn - contrarian format works for this topic") |

### New Notion Database Views (Charlie Creates These Manually)

1. **Performance Dashboard** - Sort by Performance Score descending, filter Status = Posted
2. **Underperformers** - Filter Score < 40, Status = Posted
3. **Top Performers** - Filter Score > 80, Status = Posted
4. **Needs Scoring** - Filter Last Scored is empty, Status = Posted
5. **Theme Analysis** - Group by Content Theme, show average score

---

## Agent: content_performance_agent.py

**Location:** `agents/content_performance_agent.py`

### What It Does

1. **Queries Notion** for content with Status = "Posted" and either:
   - `Last Scored` is empty (never scored), OR
   - `Last Scored` is older than 7 days (needs refresh)

2. **Identifies content type** from Content Formats relation:
   - Blog/SEO/Deep Dive -> use GA4 + GSC + HubSpot scoring
   - Social post -> use Meta/YouTube scoring
   - Newsletter -> use HubSpot email campaign scoring
   - Podcast -> use YouTube + GA4 scoring

3. **Pulls analytics** from the appropriate existing modules:
   - `seomachine/data_sources/modules/google_analytics.py`
   - `seomachine/data_sources/modules/meta.py`
   - `seomachine/data_sources/modules/youtube.py`
   - `seomachine/data_sources/modules/hubspot.py`
   - `seomachine/data_sources/modules/google_search_console.py`

4. **Calculates score** using the algorithm above

5. **Writes back to Notion** via API:
   - Performance Score
   - Score Label
   - Individual metrics (impressions, engagements, etc.)
   - Trend direction
   - Score Notes (one-line insight)
   - Last Scored timestamp

6. **Generates digest** (markdown + optional Slack):
   - Top 5 performers this period
   - Bottom 5 (with suggested actions)
   - Theme-level averages
   - Platform-level averages
   - Week-over-week trend

### Run Modes

```bash
# Score all unscored content
python agents/content_performance_agent.py

# Score specific content type
python agents/content_performance_agent.py --type blog
python agents/content_performance_agent.py --type social
python agents/content_performance_agent.py --type newsletter

# Generate digest only (no Notion writes)
python agents/content_performance_agent.py --digest-only

# Output as Slack message
python agents/content_performance_agent.py --digest-only --output slack
```

### Cron Schedule (Recommended)

```
# Score new content daily at 7am
0 7 * * * cd /path/to/vault && python agents/content_performance_agent.py

# Generate weekly digest Monday at 8am
0 8 * * 1 cd /path/to/vault && python agents/content_performance_agent.py --digest-only --output slack
```

---

## Decision Support: What Charlie Sees

### At Content Approval (Slack #market-daily)

When a social post is suggested for approval, the system appends context:

```
[Draft post content here]

---
Similar content performance:
- "Curriculum reviews" theme avg score: 7.2 (LinkedIn), 4.1 (X)
- Best performer in this theme: "Why Saxon Math works for struggling learners" (score: 89)
- Recommended platform: LinkedIn (2.3x avg engagement for this topic)
```

### In Notion (Dashboard View)

Charlie opens Notion, sees the Performance Dashboard view:

| Content | Platform | Score | Label | Impressions | Eng Rate | Trend |
|---------|----------|-------|-------|-------------|----------|-------|
| Why homeschool kids... | LinkedIn | 91 | Top | 12,400 | 8.2% | Rising |
| Saxon vs Math-U-See | Blog | 78 | Strong | 3,200 pv | 62% eng | Stable |
| Free curriculum list | X | 34 | Under | 890 | 1.1% | Declining |

### Weekly Digest (Slack or Markdown)

```
## Content Performance - Week of Feb 10

### Top 5
1. "Why homeschool kids outperform" (LinkedIn) - Score: 91
2. "Is a chicken reimbursable?" (IG Reel) - Score: 87
3. "Waldorf vs Montessori" (Blog) - Score: 78

### Bottom 5 (Review These)
1. "Education news roundup" (X) - Score: 12
   -> Roundup format consistently underperforms on X. Consider dropping.
2. "Weekly digest promo" (Facebook) - Score: 18
   -> Promotional posts score low. Try question format instead.

### Theme Scores (30-day avg)
- Curriculum reviews: 68 (strong)
- School choice policy: 72 (strong)
- Homeschool how-to: 54 (average)
- Education news: 31 (underperforming)

### Platform Averages
- LinkedIn: 64 (best platform)
- Instagram: 58
- X: 41
- Facebook: 38 (weakest platform)
```

---

## Integration Points

### Existing Skills That Benefit

| Skill | How It Uses Scores |
|-------|-------------------|
| `archive-suggest` | Prioritize resurfacing high-scoring content. Score > 70 = resurface candidate |
| `newsletter-to-social` | Route derivatives to platforms where similar themes score highest |
| `content-repurposer` | When creating spokes from a hub, check theme scores to prioritize platforms |
| `text-content` | When selecting templates, reference which template categories score highest |
| `quality-loop` | Add a 6th judge: "Performance Advisor" that checks if the content pattern has historically performed |
| `seo-content-production` | Cross-reference keyword targets with actual page performance |

### Future Enhancements

1. **Beehiiv API integration** - When available, pull newsletter open/click rates directly (currently proxied through HubSpot email campaigns)
2. **X/Twitter analytics** - Post-level metrics (currently a gap - no X analytics module)
3. **LinkedIn analytics** - Post-level metrics (currently a gap)
4. **TikTok analytics** - When posting volume justifies it
5. **A/B scoring** - Compare two versions of similar content (same theme, different format) to identify winning patterns
6. **Automated recommendations** - "Based on your last 30 posts, contrarian takes on LinkedIn outperform how-to posts by 2.4x"

---

## Setup Instructions

### Step 1: Add Notion Properties

Charlie needs to manually add these properties to the Master Content Database:
1. Open Notion > Master Content Database
2. Add each property from the schema extension table above
3. Set up the 5 database views described above

### Step 2: Configure Environment

Ensure `.env` has these keys (most should already exist):
```
GA4_PROPERTY_ID=...
GA4_CREDENTIALS_PATH=...
META_ACCESS_TOKEN=...
META_PAGE_ID=...
META_INSTAGRAM_ID=...
YOUTUBE_API_KEY=...
YOUTUBE_CHANNEL_ID=...
HUBSPOT_API_KEY=...
NOTION_API_KEY=...
```

### Step 3: Run Initial Scoring

```bash
# First run: score all Posted content
python agents/content_performance_agent.py

# Verify scores appear in Notion
# Set up cron for ongoing scoring
```

### Step 4: Start Using Scores

- Check Notion Performance Dashboard before approving new content
- Review weekly digest for patterns
- Reference theme scores when planning content calendar

---

## Maintenance

- Scoring weights are configurable in `agents/content_performance_agent.py` (PLATFORM_WEIGHTS and CONTENT_TYPE_WEIGHTS dicts)
- Add new content types by adding a scoring function and registering it in the SCORING_FUNCTIONS dict
- If a new analytics module is added (e.g., TikTok), add it to the data collection step and update the social scoring weights
- Score history is tracked via Last Scored date - Notion's page history preserves previous values

---

*Created: 2026-02-11*
*Author: Content Performance Scoring System Design*
