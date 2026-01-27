# RSS Curation Skill

Fetches RSS feeds, scores for OpenEd relevance, posts to Slack #market-daily.

## Invocation

User says: "run curation", "check feeds", "daily curation", "/rss-curation"

## Workflow

1. **Fetch feeds** - Run script or read pre-fetched output:
   ```bash
   python3 /path/to/curate.py --json --days 1
   # Or read: .claude/skills/rss-curation/output/latest.json
   ```

2. **Score items** - Use 3-tier system (see `scoring-prompt.md`)

3. **Post to Slack** - Each DEFINITELY item gets its own message to #market-daily (C07U9S53TLL)

4. **Develop on request** - When user reacts or says "develop [item]", fetch article and draft social posts

## 3-Tier Scoring

| Tier | When to Use |
|------|-------------|
| ✅ DEFINITELY | State news (AR/IN/IA/KS/MN/MT/NV/OR/UT), families mixing approaches, kids thriving outside traditional school, practical parent help, relatable parent moments |
| 🤔 PROBABLY | Fresh homeschool/alt-ed angle, neurodiversity, curriculum comparisons, ESA/policy news |
| ❌ NO | Public school focused, pure political, generic parenting, clickbait, dogmatic |

Full criteria: `scoring-prompt.md`

## Slack Post Format

**Each DEFINITELY item = separate message:**
```
📰 *[Title]*
_[Source] · [X hours ago]_

[1-2 sentence summary]

💡 *OpenEd angle:* [Why this matters]

🔗 [URL]
```

**PROBABLY items = one summary message at end**

## Develop Workflow

When user says "develop [item]":
1. WebFetch the full article
2. Check `nearbound/people/` for mentioned names
3. Web search for social handles if needed
4. Draft 2-3 social posts using `text-content` skill
5. Include @handles for tagging

## Feed Tiers

| Tier | Description | Examples |
|------|-------------|----------|
| 1 | Priority | Kerry McDonald, EdChoice, The 74, Michael B. Horn |
| 2 | Education blogs | EdSurge, Getting Smart, Peter Gray |
| 3 | Homeschool community | Simply Charlotte Mason, Homeschool Better Together |
| 4 | Substacks | Ed3 World, Austin Scholar |
| 5 | Podcasts/video | Future of Ed Podcast |
| 6 | News aggregators | Google News alerts, Reddit |

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
