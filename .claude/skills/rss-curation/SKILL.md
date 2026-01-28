# RSS Curation Skill

Fetches RSS feeds, scores for OpenEd relevance, posts to Slack #content-inbox.

## Invocation

User says: "run curation", "check feeds", "daily curation", "/rss-curation"

## Workflow

1. **Fetch feeds** - Run script or read pre-fetched output:
   ```bash
   python3 /path/to/curate.py --json --days 1
   # Or read: .claude/skills/rss-curation/output/latest.json
   ```

2. **Score items** - Use 3-tier system (see `scoring-prompt.md`)

3. **Post to Slack** - Each DEFINITELY item gets its own message to #content-inbox (C0ABV2VQQKS)

4. **Develop on request** - When user reacts or says "develop [item]", fetch article and draft social posts

## 3-Tier Scoring

| Tier | When to Use |
|------|-------------|
| DEFINITELY | Families mixing approaches, kids thriving outside traditional school, practical parent help, relatable parent moments, neurodiversity |
| PROBABLY | Fresh homeschool/alt-ed angle, curriculum comparisons, microschool models (family experience not policy) |
| NO | School choice policy/ESA news, political content, public school focused, generic parenting, clickbait, dogmatic |

**School choice / ESA policy is NOT our topic.** Skip even if pro-homeschool.

Full criteria: `scoring-prompt.md`

## Slack Post Format

**Each DEFINITELY item = separate message (no emojis):**
```
*[Title]*
_[Source] - [X hours ago]_

[1-2 sentence summary]

OpenEd angle: [Why this matters]

[URL]
```

**PROBABLY items = one summary message at end**

## Develop Workflow (Framework Fitting)

When user says "develop [item]" or for auto-develop on slam-dunk items:

### Step 1: Fetch & Extract
1. WebFetch the full article
2. **Extract 2-3 standalone snippets** (not a summary):
   - Hot takes / opinions that stand alone
   - Stats or data points with interpretation
   - Story arcs / transformation moments
   - Quotable lines

### Step 2: Find Handles (Nearbound)
1. Check `Studio/Nearbound/people/` for mentioned names
2. If not found, web search for social handles:
   - Twitter/X: `[name] [org] twitter`
   - LinkedIn: `[name] [org] linkedin`
   - Instagram: `[name] [org] instagram`

### Step 3: Match Snippets to Platforms
| Snippet Type | Best Platform | Template Style |
|--------------|---------------|----------------|
| Hot take | X, LinkedIn | Contrarian hook, paradox |
| Stat/data | LinkedIn | Authority, "Here's what this means" |
| Story arc | LinkedIn, Instagram | Transformation, before/after |
| Quote | Instagram, X | Quote card, commentary |

### Step 4: Draft Posts (OpenEd Voice)
Use `text-content` skill templates. Key rules:
- No correlative constructions ("X isn't just Y - it's Z")
- No AI-isms: delve, journey, landscape, comprehensive
- Conversational, like sharing with a friend
- Include @handles for tagging

### Step 5: Screenshot (Optional)
Use screenshot tool for article captures:

```bash
cd "/Users/charliedeist/Desktop/New Root Docs/.claude/tools/playwright"
node screenshot.mjs "[article-url]" "/path/to/Studio/Social Screenshots/YYYY-MM-DD/[slug].png"
```

## Auto-Develop (Slam Dunks)

For DEFINITELY items, spawn a sub-agent to develop into social posts:

```
Task tool prompt:

Develop this article into social posts for OpenEd:

URL: [article url]
Title: [title]
Source: [source]

Steps:
1. WebFetch the full article
2. Extract 2-3 standalone snippets (not a summary):
   - Hot takes that stand alone
   - Stats with interpretation
   - Story moments
   - Quotable lines
3. Web search for social handles of people/orgs mentioned
4. Draft 2 LinkedIn variations and 2 X variations
5. Voice rules: no emojis, no AI-isms, no correlative constructions ("X isn't just Y - it's Z"), conversational tone

Return: snippets, handles found, and draft posts ready for review.
```

This can be run manually ("develop the Pam Barnhill article") or spawned automatically for slam dunks.

## Handles to Tag

Always search for handles when developing posts:
- Web search: `[name] [org] twitter` or `linkedin`
- Common sources:
  - Getting Smart: @Getting_Smart (X), /company/getting-smart (LinkedIn)
  - Pam Barnhill: @paborgnfld (X), pambarnhill.com
  - Kerry McDonald: @kaborgnfld (X)
  - EdSurge: @EdSurge (X)
  - Michael B. Horn: @michaelbhorn (X)

## Chained Skills

This skill references:
- `text-content` - 360+ social templates
- `screenshots` - Playwright article screenshots
- `ghostwriter` - Anti-AI voice patterns
- `ai-tells` - Patterns to avoid

## Feed Sources

Tiers are for organizing the feed list, not prejudging content. **Each article is scored individually** against DEFINITELY/PROBABLY/NO criteria.

| Tier | Type | Examples |
|------|------|----------|
| 1 | Usually relevant | Kerry McDonald, Pam Barnhill, Fab Fridays, Let Grow |
| 2 | Education blogs | EdSurge, Getting Smart, Peter Gray |
| 3 | Homeschool community | Simply Charlotte Mason, r/homeschool |
| 4 | Substacks | Ed3 World, Austin Scholar |
| 5 | Podcasts/video | Future of Ed Podcast |
| 6 | Mixed (policy + family) | EdChoice, The 74 Million, Google News |

A policy-heavy source can still have family-focused pieces worth sharing.

## Files

- `SKILL.md` - This file
- `feeds.json` - Feed list (40+ feeds)
- `curate.py` - Fetcher script

## Adding Feeds

1. WebFetch the URL to verify it's valid RSS
2. Determine tier (1-6)
3. Edit `feeds.json` and add to homeschool array

## Kill the Newsletter

For newsletters without direct RSS:
1. Go to https://kill-the-newsletter.com/
2. Create feed → get email + Atom URL
3. Subscribe newsletter to that email
4. Add Atom URL to feeds.json under ktn_feeds
