# Content Curation System

**Goal:** Daily curated content from RSS feeds → AI filter → Slack → OpenEd Daily content

---

## Session Starter Prompt

```
RSS/Slack Curation Pipeline - OpenEd

Current state (2026-01-26):
- 30 Homeschool feeds ready (direct RSS URLs confirmed)
- Python script created: scripts/daily_curation.py
- AI filtering prompt written (based on OpenEd brand identity)
- NOT YET RUNNING - needs: feedparser install, launchd setup, Slack webhook

Today's focus: [FILL IN]

Quick commands:
  pip install feedparser
  python scripts/daily_curation.py --test  # Dry run

Read context: curation/README.md
```

---

## Quick Start Commands

```bash
# Install blogwatcher (requires Go)
go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest

# Install last30days skill
git clone https://github.com/mvanhorn/last30days-skill.git ~/.claude/skills/last30days

# Create Slack channel
# Manual: Create #curation-inbox in Slack workspace
```

---

## Architecture

```
SOURCES                           PROCESSING                    OUTPUT
───────                           ──────────                    ──────
RSS/OPML (blogwatcher)  ───┐
                           ├──→  Relevance Filter  ──→  Slack #curation-inbox
Reddit/X (last30days)   ───┘     (keywords + AI)        (reactions for triage)
```

---

## Components

| Component | Tool | Status |
|-----------|------|--------|
| RSS monitoring | [blogwatcher](https://github.com/Hyaxia/blogwatcher) | To install |
| Community research | [last30days](https://github.com/mvanhorn/last30days-skill) | To install |
| Slack posting | Slack MCP | Available |
| AI filtering | Claude (via script) | To build |

---

## Feed Boards

| Board | Count | Primary Use |
|-------|-------|-------------|
| [Homeschool](feeds/homeschool.md) | 36 | OpenEd Daily TREND segment |
| [AI/Marketing](feeds/ai-marketing.md) | 16 | Skill Stack |
| [Marketing/Social](feeds/marketing-social.md) | 14 | Skill Stack |
| [Charlie](feeds/charlie-personal.md) | 15 | Personal |

**Total feeds:** 81 (42 direct RSS, 39 via Feedly/Kill-the-Newsletter)

---

## Files

```
curation/
├── README.md              # This file
├── PLAN.md                # Implementation plan
├── feeds/
│   ├── homeschool.md      # Education/homeschool feeds
│   ├── ai-marketing.md    # AI newsletters
│   ├── marketing-social.md # Creator/marketing feeds
│   ├── charlie-personal.md # Personal interests
│   └── master.opml        # Full OPML export
├── scripts/               # (future)
│   ├── scan.py            # Daily scan script
│   └── post_to_slack.py   # Slack integration
└── config/                # (future)
    ├── keywords.json      # Relevance keywords
    └── exclusions.json    # Patterns to skip
```

---

## Quick Start (When Ready)

```bash
# Install blogwatcher
go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest

# Install last30days skill
git clone https://github.com/mvanhorn/last30days-skill.git ~/.claude/skills/last30days

# Add API keys for last30days
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << 'EOF'
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
EOF
```

---

## Related

- Full plan: `PLAN.md`
- Content engine refactor: `../README.md`
- Archive suggest skill: `.claude/skills/archive-suggest/`
- OpenEd Daily writer: `.claude/skills/opened-daily-newsletter-writer/`

---

*Last updated: 2026-01-25*
