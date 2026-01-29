# RSS → Social Post Workflow

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DAILY CURATION                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │  64 RSS      │
    │  FEEDS       │ ←── Automated (cron or manual trigger)
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  FETCH &     │     Tool: Python + feedparser
    │  SCORE       │     Output: Markdown file with DEFINITELY/PROBABLY/NO
    └──────┬───────┘
           │
           ▼
    ╔══════════════╗
    ║  CHECKPOINT  ║     👤 HUMAN: Review scored list
    ║      1       ║     Tool: Claude Code terminal OR Obsidian
    ╚══════╤═══════╝     Time: 2-3 min
           │             Action: Scan DEFINITELYs, override if needed
           │
           ▼
    ┌──────────────┐
    │  GENERATE    │     Tool: Claude Code
    │  DRAFTS      │     Output: 5 post options per article
    └──────┬───────┘     Voice: Ed the Horse for X, OpenEd for LinkedIn
           │
           ▼
    ╔══════════════╗
    ║  CHECKPOINT  ║     👤 HUMAN: Pick favorites
    ║      2       ║     Tool: Markdown file (mark with ★) OR Notion
    ╚══════╤═══════╝     Time: 3-5 min
           │             Action: Star picks, light edits, add comments
           │
           ▼
    ┌──────────────┐
    │  PUSH TO     │     Tool: Python → Notion API
    │  NOTION      │     Creates rows in Social Post Queue
    └──────┬───────┘     Status: "Draft"
           │
           │
┌──────────┴──────────────────────────────────────────────────────────────────┐
│                              APPROVAL QUEUE                                  │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           ▼
    ╔══════════════╗
    ║  CHECKPOINT  ║     👤 HUMAN: Final review & approval
    ║      3       ║     Tool: NOTION (this is the main workspace)
    ╚══════╤═══════╝     Time: 5-10 min (can batch multiple days)
           │
           │             Actions:
           │             • Edit post text in page body
           │             • Set scheduled time
           │             • Flip Status → "Approved"
           │
           ▼
    ┌──────────────┐
    │  SCHEDULER   │     Tool: Python script (cron or manual)
    │  POLLS       │     Reads: Status = "Approved"
    │  NOTION      │     Writes: Getlate API
    └──────┬───────┘     Updates: Status → "Scheduled" + Getlate ID
           │
           ▼
    ┌──────────────┐
    │  GETLATE     │     Automated posting at scheduled times
    │  POSTS       │     Platforms: X, LinkedIn, Instagram, Facebook
    └──────┬───────┘
           │
           ▼
    ╔══════════════╗
    ║  CHECKPOINT  ║     👤 HUMAN: Engagement (optional)
    ║      4       ║     Tool: Native apps (X, LinkedIn, etc.)
    ╚══════╤═══════╝     Time: As desired
           │             Action: Reply to comments, retweet, etc.
           │
           ▼
    ┌──────────────┐
    │  NOTION      │     Update Status → "Posted"
    │  UPDATED     │     (Could be automated via Getlate webhook)
    └──────────────┘
```

---

## Tool Rationale

### Why Each Tool

| Stage | Tool | Why This Tool |
|-------|------|---------------|
| Fetch | Python + feedparser | Reliable, captures full URLs, runs anywhere |
| Score | Claude Code | AI judgment on relevance, can explain reasoning |
| Review #1 | Claude Code terminal | Fast, stays in flow, can override inline |
| Draft | Claude Code | Voice consistency, template matching, batch generation |
| Pick favorites | Markdown (★) | Fastest, no context switch, stays in terminal |
| Push to Notion | Python + Notion API | Automated, preserves formatting |
| Final review | **NOTION** | **GUI for editing**, visual queue, easy status toggle |
| Schedule | Python + Getlate API | Automated, bulk scheduling, tracks IDs |
| Post | Getlate | Handles timing, multi-platform |
| Engage | Native apps | Where the conversations happen |

### Why Notion is the Approval Layer

1. **Visual editing** - See the post, edit inline, no code
2. **Status toggles** - One click to approve
3. **Calendar view** - See what's scheduled when
4. **Batch processing** - Approve multiple posts at once
5. **Mobile** - Can approve from phone if needed
6. **Shareable** - Team members can access

### Why NOT Notion Earlier

- Notion is slow for rapid iteration (scoring, drafting)
- Claude Code is faster for AI-heavy work
- Markdown files are fastest for quick decisions (★ marking)

---

## Checkpoint Summary

| # | Stage | Human Input | Time | Tool |
|---|-------|-------------|------|------|
| 1 | Post-score | Scan list, override if needed | 2-3 min | Claude Code |
| 2 | Post-draft | Pick favorites, light edits | 3-5 min | Markdown |
| 3 | Pre-schedule | Final text edits, approve | 5-10 min | **Notion** |
| 4 | Post-publish | Engage with replies | Optional | Native apps |

**Total human time per day: ~15 min** (excluding engagement)

---

## Automation Opportunities

### Now (Manual Triggers)
```bash
# Daily curation
python3 scripts/rss_fetch.py

# After Claude drafts, push to Notion
python3 scripts/push_to_notion.py

# After you approve in Notion
python3 agents/social_post_scheduler.py
```

### Later (Cron Automation)
```bash
# 6am: Fetch and score
0 6 * * * cd ~/OpenEd && python3 scripts/rss_fetch.py

# Every hour: Check for approved posts and schedule
0 * * * * cd ~/OpenEd && python3 agents/social_post_scheduler.py
```

### Future (Full Automation)
- Notion automation triggers on status change
- Webhook from Getlate on post success
- Slack notification when posts need approval

---

## File Locations

```
Projects/RSS-Curation/
├── FEEDS.md                    # 64 feed URLs
├── PROJECT.md                  # Project overview
├── WORKFLOW-DIAGRAM.md         # This file
├── SOCIAL-POST-QUEUE.md        # Notion integration docs
├── references/
│   └── ORCHESTRATION.md        # Ed voice, platform routing
├── daily/
│   └── YYYY-MM-DD.md          # Daily curation outputs
│   └── YYYY-MM-DD-ed-posts.md # Draft posts
└── screenshots/                # For Reddit/article screenshots

agents/
└── social_post_scheduler.py    # Notion → Getlate automation
```

---

## Quick Reference Commands

```bash
# Run daily curation (in Claude Code)
"Run RSS curation for today"

# Check scheduled posts
python3 -c "import requests; ..." # (see x-posting skill)

# Manual schedule check
python3 agents/social_post_scheduler.py
```

---

*Last updated: 2026-01-29*
