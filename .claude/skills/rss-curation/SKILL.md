# RSS Daily Curation

Automated RSS feed curation for OpenEd social content. Fetches from 64 education/homeschool feeds, scores with DEFINITELY/PROBABLY/NO criteria, and posts to Slack.

## When to Use

- Daily curation runs (morning)
- Ad-hoc content discovery
- Weekly catchup (7-day window)

## Quick Start

```bash
# Run curation (saves to file, attempts Slack)
python3 agents/rss_curation.py

# Run without Slack (just save file)
python3 agents/rss_curation.py --no-slack

# Then post via MCP Slack (if bot not in channel)
# Read the daily file and post using mcp__slack__conversations_add_message
```

## Workflow

1. **Fetch** - Parse 64 feeds (last 24 hours by default)
2. **Score** - Apply DEFINITELY/PROBABLY/NO rules
3. **Save** - Write to `Projects/RSS-Curation/daily/YYYY-MM-DD.md`
4. **Post** - Send DEFINITELY items to Slack #market-daily

## Scoring Criteria

### DEFINITELY (Post to Slack)
- Mixed approach families (one child homeschool, one not)
- Kids thriving outside traditional school
- Practical parent help (curriculum, routines)
- Relatable parent moments (struggles, joys)
- Neurodiversity focus (ADHD, autism, 2e)
- Free-range / independence themes

### NO (Skip)
- School choice policy / ESA news
- Political content (ICE, legislation)
- Public school focused
- Generic parenting

### High-Value Sources (Boosted)
- Lenore Skenazy, Peter Gray, Let Grow
- Kerry McDonald, Jon Haidt
- r/homeschool, r/unschool (gold mines)
- Pam Barnhill, 1000 Hours Outside

## Output Files

| File | Purpose |
|------|---------|
| `Projects/RSS-Curation/daily/YYYY-MM-DD.md` | Scored curation |
| `Projects/RSS-Curation/FEEDS.md` | 64 feed URLs |
| `agents/rss_curation.py` | Standalone script |

## Automation Options

### Option 1: Cron (Standalone)
```bash
# Add to crontab -e
0 6 * * * cd ~/Desktop/New\ Root\ Docs/OpenEd\ Vault && python3 agents/rss_curation.py --no-slack >> /tmp/rss_curation.log 2>&1
```

### Option 2: Clawdbot Heartbeat
Add to HEARTBEAT.md:
- [ ] RSS curation: Run python3 agents/rss_curation.py --no-slack then post daily file to #market-daily

### Option 3: Claude Code Manual
"Run RSS curation for today"

## Ed the Horse Voice

For X posts from curated items, use Ed the Horse patterns:
- **Values**: "Normalize [thing]." / "[Thing] is valid."
- **Observation**: "[Thing] happened. [Dry comment]."
- **Question**: "Why do we [accepted norm]?"
- **Contrarian**: "[Opposite of expected]. Think about it."

## Related Skills

- text-content - Template library for posts
- x-posting - Schedule via Getlate
- content-repurposer - Multi-platform distribution

---

*Last updated: 2026-01-29*
