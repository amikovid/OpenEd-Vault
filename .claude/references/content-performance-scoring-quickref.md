# Content Performance Scoring - Quick Reference

## What This Is

Every piece of published content gets a score (0-100) based on how it actually performed. Scores live in Notion on the Master Content Database. The system generates narrative insights (not just numbers) and feeds performance data back into every content decision - approval, planning, platform routing, and resurfacing.

---

## First-Time Setup (5 Minutes)

```bash
python agents/setup_performance_scoring.py
```

This wizard will:
1. Check your `.env` API keys and tell you what's working
2. Automatically add all 12 performance properties to Notion (with your permission)
3. Run initial scoring on all published content
4. Offer to set up daily automated cron job

**Charlie literally just runs that one command.**

---

## How Scores Work

### Score = Percentile Rank Against Your Own Content

A score of 75 means "this performed better than 75% of all similar OpenEd content." Scores automatically recalibrate as the library grows.

| Score | Label | Action |
|-------|-------|--------|
| 80-100 | **Top Performer** | Resurface. Create more like this. Study what worked. |
| 60-79 | **Strong** | Good baseline. Keep doing this. |
| 40-59 | **Average** | Normal. No action needed. |
| 20-39 | **Underperforming** | Review: wrong platform? weak hook? bad timing? |
| 0-19 | **Poor** | Don't repeat this pattern. |

### Different Content = Different Metrics

| Content Type | Primary Metrics | Sources |
|---|---|---|
| **Blog / SEO** | Pageviews, engagement rate, search impressions, CTR, conversions, trend | GA4 + GSC + HubSpot |
| **Social posts** | Impressions, engagement rate, saves, shares, comments | Meta (FB + IG), YouTube |
| **Newsletter** | Open rate, click rate, unsubscribe rate (inverse), reply rate | HubSpot email campaigns |
| **Podcast** | YouTube views, engagement rate, blog post traffic, clip performance | YouTube + GA4 |

### Platform-Specific Weighting

Each platform's algorithm rewards different behaviors:

- **LinkedIn**: Comments matter most (25%) - LinkedIn's algorithm rewards conversations
- **X**: Reposts matter most (25%) - X's algorithm rewards virality
- **Instagram**: Saves matter most (30%) - Instagram's strongest engagement signal
- **Facebook**: Shares matter most (25%) - Facebook reach depends on sharing

---

## What You Actually See

### Weekly Insights Digest (Slack or markdown)

Not rankings - actual insights. Example:

```
Content Insights - Feb 10, 2026
47 pieces scored

Key Insights
1. LinkedIn is your strongest platform (avg score: 64) -
   Facebook is weakest (38). Consider shifting volume.
2. "Curriculum Reviews" content consistently outperforms (avg 68)
   while "Education News" underperforms (31). Double down or rethink.
3. "School Choice" performs 82 on X but only 35 on Instagram.
   Route school choice content to X.
4. Outlier: "Why homeschool kids outperform" scored 91 (avg is 52).
   Study what made this work.

This Week's Recommendations
- Resurface: "Why homeschool kids outperform" (score: 91) - proven
- Review: "Education news roundup" (score: 12) - low engagement
- Increase LinkedIn posting volume - consistently top performer (avg 64)

Platform Averages
  LinkedIn     ============= 64 (23 posts)
  Instagram    =========== 58 (18 posts)
  X            ======== 41 (12 posts)
  Facebook     ======= 38 (8 posts)
```

### At Content Approval Time

When reviewing a draft, any skill can call `get_approval_context()` to inject:

```
---
Performance context for this draft:
  "Curriculum Reviews" on LinkedIn: avg score 72 (8 posts)
  Best: "Why Saxon Math works for struggling learners" (score: 89)
  Best platform for "Curriculum Reviews": LinkedIn (avg 72)
  -> Consider routing this to LinkedIn instead of X
```

### In Notion

Open the Performance Dashboard view:

| Content | Platform | Score | Label | Trend | Score Notes |
|---------|----------|-------|-------|-------|-------------|
| Why homeschool kids... | LinkedIn | 91 | Top Performer | Rising | High engagement (8.2%). Traffic rising 34% |
| Saxon vs Math-U-See | Blog | 78 | Strong | Stable | Strong engagement. 3,200 pageviews |
| Education news roundup | X | 12 | Poor | Declining | Reached 890 people but low engagement |

---

## Running the Agent

```bash
# Score all unscored content
python agents/content_performance_agent.py

# Score specific type
python agents/content_performance_agent.py --type blog
python agents/content_performance_agent.py --type social

# Generate insights digest (no Notion writes)
python agents/content_performance_agent.py --digest-only

# Slack-formatted digest
python agents/content_performance_agent.py --digest-only --output slack

# Re-score everything (even recently scored)
python agents/content_performance_agent.py --all
```

### Recommended Cron Schedule

```
# Daily scoring at 7am
0 7 * * * cd /path/to/vault && python agents/content_performance_agent.py

# Weekly digest Monday 8am
0 8 * * 1 cd /path/to/vault && python agents/content_performance_agent.py --digest-only --output slack
```

---

## How It Feeds Into Other Skills

| Skill | Integration Point |
|---|---|
| **Content approval** (Slack triage) | `get_approval_context("theme", "platform")` returns historical performance for similar content |
| **`archive-suggest`** | Prioritize resurfacing high-scorers (score > 70) |
| **`newsletter-to-social`** | Route derivatives to platform where that theme scores highest |
| **`content-repurposer`** | Include "similar content scored X on Y" when generating options |
| **`text-content`** | Inform template selection with which categories historically perform |
| **`quality-loop`** | Potential 6th judge: Performance Advisor checks if content pattern has historically performed |
| **`seo-content-production`** | Cross-reference keyword targets with actual page performance |

### Using Approval Context in Code

Any skill or agent can import the function:

```python
from agents.content_performance_agent import get_approval_context

# When approving a curriculum review for LinkedIn:
context = get_approval_context("Curriculum Reviews", "linkedin")
print(context)
# Output:
# ---
# Performance context for this draft:
#   "Curriculum Reviews" on LinkedIn: avg score 72 (8 posts)
#   Best: "Why Saxon Math works" (score: 89)
#   Best platform for "Curriculum Reviews": LinkedIn (avg 72)
```

---

## How It Connects to Existing Modules

| Existing Module | What This System Uses From It |
|---|---|
| `seomachine/modules/google_analytics.py` | Pageviews, engagement rate, trends, declining pages |
| `seomachine/modules/google_search_console.py` | Search impressions, CTR, keyword positions |
| `seomachine/modules/meta.py` | FB post reach/engagement, IG post metrics |
| `seomachine/modules/youtube.py` | Video views, likes, comments |
| `seomachine/modules/hubspot.py` | Conversions, email campaign stats, funnel data |
| `seomachine/modules/data_aggregator.py` | Comprehensive page performance (combined) |
| `agents/social_post_scheduler.py` | GetLate post IDs for tracking |

---

## What's Not Covered Yet (Future)

- **X/Twitter analytics** - No API module exists yet. Posts to X will score 50 (median) until added.
- **LinkedIn analytics** - Same gap. Need LinkedIn analytics module.
- **Beehiiv direct** - Newsletter metrics come from HubSpot email campaigns, not Beehiiv directly.
- **TikTok analytics** - Can add when posting volume justifies it.

---

## All Files

| File | Purpose |
|------|---------|
| `agents/setup_performance_scoring.py` | One-command setup wizard |
| `agents/content_performance_agent.py` | The scoring agent + digest + approval context |
| `.claude/skills/content-performance-scoring/SKILL.md` | Full system design + algorithm details |
| `.claude/references/content-performance-scoring-quickref.md` | This file |
| `.claude/references/execution-bottleneck-analysis.md` | Broader vault bottleneck analysis |

---

*Created: 2026-02-11*
