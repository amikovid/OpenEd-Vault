# RSS Curation Skill - Handoff

**Date:** 2026-01-26
**Status:** Working, not yet scheduled

---

## What's Done

- **40 feeds configured** in `feeds.json` (tiers 1-6)
- **AI scoring script** (`curate.py`) fetches, scores with Claude CLI, posts to Slack
- **Clean Slack format** - hyperlinked titles, summaries, OpenEd angles
- **KTN automation** (`ktn_create.py`) - Playwright script to create Kill the Newsletter feeds
- **Slack channel** - Posts to `#curation-inbox` (private, ID: C0ABV2VQQKS)

### Feed Sources
- Tier 1: Kerry McDonald, EdChoice, The 74, Fab Fridays, Let Grow, Michael B. Horn
- Tier 2: Getting Smart, EdSurge, Rick Hess, NHERI, 1000 Hours Outside, ClarifiEd, Peter Gray
- Tier 3: Homeschool blogs (Simply Charlotte Mason, Christy-Faith, etc.), Withyweather, Coach Meg Thomas (KTN)
- Tier 4: Substacks (Ed3 World, Austin Scholar)
- Tier 5: Podcasts (Future of Ed, Hannah Frankman YT, NREA)
- Tier 6: Google News alerts (homeschooling, microschool, ESA, hybrid, learning pod, unschooling), Reddit

---

## Not Yet Done

### 1. Scheduler (launchd)
Script runs manually. Need to set up launchd plist for daily automation:

```bash
# Create plist at ~/Library/LaunchAgents/com.opened.rss-curation.plist
# Schedule for 7am daily
```

### 2. Deduplication
Currently no memory of what's been posted. Could add:
- SQLite db of posted URLs
- Or simple JSON file with last 100 URLs

---

## Future Directions

### Comment-to-Content Pipeline
User wants ability to:
1. **Comment on curated items** (voice memo or text reply in Slack)
2. **Route to content engine** - newsletter TREND segment, social posts, etc.
3. **Link back to Claude** for next steps

Possible implementation:
- Slack workflow that captures replies to curation posts
- Routes to inbox processor or dedicated "content ideas" channel
- Claude picks up via `/sort-inbox` or dedicated command

### Voice Memo Integration
- Reply to Slack message with voice memo
- Whisper transcription
- Route to appropriate content workflow

---

## Commands

```bash
# Dry run
python3 "OpenEd Vault/.claude/skills/rss-curation/curate.py" --test

# Post to Slack
python3 "OpenEd Vault/.claude/skills/rss-curation/curate.py" --slack

# Look back 7 days
python3 "OpenEd Vault/.claude/skills/rss-curation/curate.py" --days 7 --test

# See all scores
python3 "OpenEd Vault/.claude/skills/rss-curation/curate.py" --test --all

# Create KTN feed
python3 "OpenEd Vault/.claude/skills/rss-curation/ktn_create.py" "Newsletter Name"
```

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill documentation |
| `feeds.json` | 40 feeds by tier |
| `curate.py` | Main curation script |
| `ktn_create.py` | Kill the Newsletter automation |
| `HANDOFF.md` | This file |

---

## Next Session

1. ~~Set up launchd for 7am daily runs~~ DONE
2. Add deduplication (simple JSON file of recent URLs)
3. Consider Slack workflow for comment routing

---

## Split Off: Personal Feeds

Personal/AI/Marketing feeds moved to separate project:
`Creative Intelligence Agency/doodle-reader/FEATURE-curated-feeds.md`

This skill focuses on **OpenEd homeschool content only**.

Personal feeds will be consumed via Doodle Reader with a Pocket-like interface (future feature).
