# Social Media

**Status:** Active
**Purpose:** Multi-platform content production, approval, and distribution for OpenEd.

---

## How It Works

```
CONTENT SOURCES                    PRODUCTION                DISTRIBUTION
──────────────────────────────────────────────────────────────────────────

Newsletter (Mon-Thu)  ─┐
Podcast episodes      ─┤
Blog/Deep Dives       ─┼──► Framework Fitting ──► Slack #market-daily ──► GetLate API
Archive (406 articles)─┤    (text-content skill)   (approval)             (8 platforms)
Elijah video batches  ─┘
```

**One pipeline.** Content enters from any source, gets framework-fitted to platform templates, posted to Slack for approval, and scheduled via GetLate.

---

## Quick Navigation

| Need | Go To |
|------|-------|
| Format templates | `FORMAT_INVENTORY.md` |
| Platform strategies | `Platform Insights/` (7 platforms) |
| Elijah's production system | `Frictionless Content Engine/PROJECT.md` |
| Calibration examples | `staging/Content_Concepts.md` |
| Nearbound tagging | `../Nearbound Pipeline/people/` |
| Retargeting creative | `../Meta Ads/PROJECT.md` |

---

## Content Production

### Framework Fitting (Core Method)

```
SOURCE → EXTRACT SNIPPETS → MATCH TO TEMPLATES → GENERATE DRAFTS → QUALITY GATE
```

| Snippet Type | LinkedIn | X | Instagram |
|---|---|---|---|
| Hot take | Contrarian post | Paradox Hook | Quote card |
| Stat | Authority post | Commentary | Carousel |
| Story | Transformation | Thread | Reel/Carousel |
| How-to | List post | Thread | Carousel |

**Primary skill:** `text-content` (360+ templates)
**Quality gate:** `quality-loop` (lite 3-judge for social)

### Production Targets

| Metric | Target |
|--------|--------|
| Production velocity | 2 videos + 2 text posts/day |
| Human time per asset | <15 min |
| Quality bar | No AI slop |

---

## Platform Strategies

Full guides in `Platform Insights/` folder. Quick reference:

| Platform | Success Heuristic | Key Format |
|----------|-------------------|------------|
| **X/Twitter** | "I wish I said that" - retweet-worthy | Short, punchy, quotable |
| **LinkedIn** | Thought leadership, vulnerability | Long-form (200-500 words) |
| **Facebook** | Engagement bait, comments drive reach | Questions, text-on-background |
| **Instagram** | Visual-first, Reels > everything | Reels, then carousels |
| **TikTok** | Educational entertainment | Hook in 1 sec, text-on-video |
| **YouTube** | Shorts for reach, long for depth | Shorts repurposed from Reels |
| **Pinterest** | SEO, evergreen discovery | Pins linking to articles |

---

## Video Arsenal

### Tier 1: No Filming Required
- **Text on B-roll** - Stock footage + text overlays
- **Screenshot + voiceover** - Tweet screenshots, article highlights
- **Podcast clips** - Existing audio + captions + waveform

### Tier 2: Replicable Formats (Elijah)
- **Pointing Format** - Point to tablet headline (90 sec production)
- **Tablet Swivel** - Reveal message on tablet (90 sec)
- **iPhone Notes Style** - Simple text on tablet (60 sec)
- **"Is It Reimbursable?"** - Hold item, reveal answer (unique to OpenEd)
- **Ed the Horse** - Character video with education commentary

### Tier 3: Produced Content
- **Podcast video episodes** - Full production
- **Explainer videos** - Scripted + edited

---

## Approval & Publishing

### Workflow

1. **Create** - Framework fitting produces platform-optimized drafts
2. **Post to Slack** - `slack-social-distribution` posts to #market-daily
3. **Approve** - Human reacts with emoji (see below)
4. **Schedule** - `schedule-approved` sends to GetLate API
5. **Track** - URL populated, performance noted

### Slack Reactions

| Emoji | Meaning |
|-------|---------|
| ✅ | Approved - schedule it |
| ✍️ | Develop further (spawn framework fitting) |
| ❌ | Skip |
| 👀 | Claimed (someone's working on it) |

### GetLate API

8 platforms configured: LinkedIn, X, Instagram, Facebook, YouTube, TikTok, Pinterest, Threads.

**Credentials:** `GETLATE_API_KEY` in `.env`
**Agent:** `agents/social_post_scheduler.py` (Notion queue integration)
**Direct posting:** `agents/social_media_agent.py`

---

## Notion Integration

**Master Content Database:** `9a2f5189-6c53-4a9d-b961-3ccbcb702612`

Status flow: `Idea` → `Staging` → `Approved` → `Scheduled` → `Posted`

**Current state:** 100+ items in Staging need triage. See archived Content Staging Pipeline docs in `Studio/_archive/` for full Notion schema and triage plan.

---

## Subprojects

### Frictionless Content Engine
**Owner:** Elijah (automation partner)
**Location:** `Frictionless Content Engine/PROJECT.md`
**Purpose:** Template-driven video + static production at velocity

### Calibration
**Location:** `staging/Content_Concepts.md`
**Purpose:** 40+ post concepts with inline feedback (`{good}`, `{reject}`, `{needs work}`)
**Use:** Reference before generating new content to calibrate quality bar

---

## Skills

| Skill | Purpose |
|-------|---------|
| `text-content` | 360+ social templates, framework fitting |
| `content-repurposer` | Source → multi-platform |
| `newsletter-to-social` | Newsletter → 6-9 social posts |
| `slack-social-distribution` | Post drafts to #market-daily |
| `schedule-approved` | Notion → GetLate scheduling |
| `video-caption-creation` | Hooks + captions for clips |
| `short-form-video` | Reels/TikTok production |
| `dude-with-sign-writer` | One-liner patterns |

---

## Content Sources

| Source | Location | Use For |
|--------|----------|---------|
| Blog archive (406 articles) | `Master_Content_Index.md` | All resurfacing |
| Podcast episodes | `../Podcast Studio/` | Clips, quotes, video |
| Newsletter archive | `../OpenEd Daily Studio/` | LinkedIn, short posts |
| Featured people | `../Nearbound Pipeline/people/` | Tagging strategy |

---

*Last updated: 2026-02-04*
