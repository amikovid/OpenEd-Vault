# OpenEd Content Engine - Skill Architecture Map

**Created:** 2026-01-23
**Updated:** 2026-01-29
**Purpose:** Visual reference for OpenEd Vault structure, documentation hierarchy, and skill chains

---

## OpenEd Vault - Folder Architecture

```
OpenEd Vault/                              CLAUDE.md ✓ + NOW.md ✓
│
├── .claude/                               (Claude Code config)
│   ├── skills/                            45+ content skills
│   ├── references/                        Shared references
│   │   ├── Master_Content_Index.md        406 published articles
│   │   ├── opened-program-details.md      9-state operations
│   │   ├── notion-content-schema.md       Staging pipeline
│   │   └── workspace-architecture-reference.md
│   └── work-summaries/                    Daily Slack updates
│
├── Studio/                                ─────── PRODUCTION WORKFLOWS ───────
│   │
│   ├── OpenEd Daily Studio/               PROJECT.md (Mon-Thu newsletter)
│   │   ├── 2026-01-27 - [Topic]/          Episode folders (date-stamped)
│   │   ├── ideas/                         Pipeline ideas
│   │   └── Archived/                      Past episodes
│   │
│   ├── OpenEd Weekly/                     (No PROJECT.md - needs one)
│   │   └── 2026-01-24 - Weekly/           Friday digest folders
│   │
│   ├── Podcast Studio/                    PROJECT.md (weekly production)
│   │   ├── [Guest Name]/                  Active episode folders
│   │   └── Archived Podcasts/             Completed episodes
│   │
│   ├── SEO Content Production/            PROJECT.md (master)
│   │   ├── Open Education Hub/            Deep dives + PROJECT.md
│   │   ├── Grade Level Guides/            K-12 guides + PROJECT.md
│   │   ├── State Pages/                   9-state guides + PROJECT.md
│   │   ├── Guest Contributors/            Outreach + PROJECT.md
│   │   ├── Versus/                        Comparisons + PROJECT.md
│   │   ├── Day in the Life/               User stories
│   │   └── seomachine/                    DataForSEO tooling
│   │
│   ├── Social Media/                      PROJECT.md
│   │   ├── Frictionless Content Engine/   Sub-project + PROJECT.md
│   │   ├── Format Notes/                  Platform learnings
│   │   ├── Platform Insights/             Analytics
│   │   ├── YouTube Clips/                 Clip staging
│   │   └── staging/                       Post drafts
│   │
│   ├── Meta Ads/                          PROJECT.md
│   │   ├── Ad Creative Concepts/          100 concepts (V1+V2)
│   │   └── Curriculum-Targeting-Campaign/ Sub-project + PROJECT.md
│   │
│   ├── Nearbound Pipeline/                PROJECT.md
│   │   ├── people/                        81 contact profiles
│   │   ├── _extraction/                   Source processing
│   │   └── scripts/                       Automation
│   │
│   ├── Analytics & Attribution/           PROJECT.md
│   │   ├── hubspot-integration/           Email tracking
│   │   └── reports/                       Performance data
│   │
│   ├── Content Staging Pipeline/          PROJECT.md (Notion integration)
│   │
│   └── _archive/                          Deprecated workflows
│
├── Projects/                              ─────── DISCRETE PROJECTS ───────
│   │
│   ├── Lead Magnet Project/               PROJECT.md (umbrella)
│   │   ├── curriculove/                   CLAUDE.md ✓ + NOW.md ✓ (app)
│   │   ├── pdf-generator/                 PDF tooling
│   │   ├── Lead Magnet Guides/            Content assets
│   │   └── Quick Guides/                  Short-form guides
│   │
│   ├── Eddie Awards/                      PROJECT.md (Feb-Apr 2026)
│   │
│   ├── Retargeting Strategy FY26-27/      PROJECT.md (Feb 16 launch)
│   │
│   ├── KPI Discussions/                   PROJECT.md (Q1 bonus)
│   │
│   ├── Tools Directory/                   PROJECT.md
│   │   ├── Webflow Tools Redesign/        Sub-project + PROJECT.md
│   │   ├── drafts/                        Review content
│   │   └── permission-requests/           Outreach
│   │
│   ├── OpenEd-Content-OS/                 Content OS (this file)
│   │   ├── PROJECT.md                     Main Content OS doc
│   │   └── SKILL_ARCHITECTURE_MAP.md      ← You are here
│   │
│   └── partnerships/                      (sparse - needs cleanup)
│
├── Published Content/                     ─────── OUTPUT ARCHIVE ───────
│   ├── Blog Posts/                        Published articles
│   ├── Daily Newsletters/                 Sent newsletters
│   ├── Podcasts/                          Episode archives
│   └── Announcements/                     Company updates
│
├── CRM/                                   ─────── CONTACT MANAGEMENT ───────
│   ├── contacts/                          Contact records
│   └── gmail-crm/                         Email integration
│
├── agents/                                Python automation scripts
│   └── _archived/                         Deprecated agents
│
├── todos/                                 Task management (deprecated?)
│
├── uploads/                               Temporary uploads
│
└── Archive/                               Historical content
```

---

## Documentation Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         DOCUMENTATION TIERS                                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

TIER 1: CLAUDE.md + NOW.md (Workspaces)
├── OpenEd Vault/           ← Full workspace, context-switch into it
└── curriculove/            ← Full app with its own stack

TIER 2: PROJECT.md only (Discrete work)
├── Studio workflows        ← Newsletter, Podcast, Social, SEO
├── Campaigns               ← Meta Ads, Retargeting, Eddie Awards
└── Sub-projects            ← Within larger projects

TIER 3: No docs (Output folders)
├── Date-stamped episodes   ← 2026-01-27 - Topic Name/
├── Archive folders         ← Completed work
└── Asset folders           ← images/, uploads/
```

---

## Content Production Map

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         STUDIO → OUTPUT FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────────────┘

INPUTS (Sources)                    PRODUCTION                      OUTPUTS
─────────────────                   ──────────                      ───────

┌─────────────┐                ┌─────────────────────┐
│ Topic brief │───────────────▶│ OpenEd Daily Studio │──────────▶ HubSpot → 45K subs
│ + sources   │                │ (Mon-Thu)           │            + Social spokes
└─────────────┘                │ skill: opened-daily-│
                               │ newsletter-writer   │
                               └─────────────────────┘

┌─────────────┐                ┌─────────────────────┐
│ Week's      │───────────────▶│ OpenEd Weekly       │──────────▶ HubSpot → 45K subs
│ content     │                │ (Friday digest)     │            + LinkedIn roundup
└─────────────┘                │ skill: opened-weekly│
                               │ newsletter-writer   │
                               └─────────────────────┘

┌─────────────┐                ┌─────────────────────┐
│ Recording   │───────────────▶│ Podcast Studio      │──────────▶ YouTube + Spotify
│ + guest     │                │ (4 checkpoints)     │            + Blog post
└─────────────┘                │ skill: podcast-     │            + 12-25 social posts
                               │ production          │
                               └─────────────────────┘

┌─────────────┐                ┌─────────────────────┐
│ Keyword     │───────────────▶│ SEO Content Prod    │──────────▶ Webflow Hub
│ research    │                │ (deep dives, guides)│            + Social promotion
└─────────────┘                │ skill: open-edu-hub-│            + Internal links
                               │ deep-dives          │
                               └─────────────────────┘

┌─────────────┐                ┌─────────────────────┐
│ Any hub     │───────────────▶│ Social Media        │──────────▶ LinkedIn, X, IG, FB
│ content     │                │ (framework fitting) │            TikTok, YouTube
└─────────────┘                │ skill: text-content │
                               │ newsletter-to-social│
                               └─────────────────────┘

┌─────────────┐                ┌─────────────────────┐
│ Video clips │───────────────▶│ Video Production    │──────────▶ Reels, Shorts, TikTok
│ or concepts │                │ (captions + hooks)  │
└─────────────┘                │ skill: video-caption│
                               │ -creation           │
                               └─────────────────────┘

┌─────────────┐                ┌─────────────────────┐
│ Ad briefs   │───────────────▶│ Meta Ads            │──────────▶ FB/IG paid campaigns
│ + audience  │                │ (creative concepts) │
└─────────────┘                │ skill: meta-ads-    │
                               │ creative            │
                               └─────────────────────┘
```

---

## Active Projects Status

**Note:** For current project status, see **EXECUTION.md** (weekly tracking) and **NOW.md** (current state).

This map documents the *architecture*, not real-time status.

---

## Master Flow: Any Source → Multi-Platform Distribution

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    SOURCE INPUTS                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│    │  PODCAST    │   │ NEWSLETTER  │   │  DEEP DIVE  │   │   ARCHIVE   │           │
│    │  EPISODE    │   │   (Daily)   │   │  (SEO Hub)  │   │  (406 pcs)  │           │
│    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│           │                 │                 │                 │                   │
│           ▼                 ▼                 ▼                 ▼                   │
│    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│    │  podcast-   │   │ opened-     │   │ open-edu-   │   │  (manual    │           │
│    │  production │   │ daily-      │   │ hub-deep-   │   │   scan)     │           │
│    │             │   │ newsletter- │   │ dives       │   │             │           │
│    │             │   │ writer      │   │             │   │             │           │
│    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│           │                 │                 │                 │                   │
└───────────┴─────────────────┴─────────────────┴─────────────────┴───────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CONTEXT LOADING (Always)                                │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                  │
│   │  opened-identity │  │     ai-tells     │  │   CLAUDE.md      │                  │
│   │                  │  │                  │  │  Writing Rules   │                  │
│   │  • Brand voice   │  │  • Hard blocks   │  │                  │                  │
│   │  • Sarah persona │  │  • Words to avoid│  │  • No correlatives│                 │
│   │  • Values        │  │  • Setup phrases │  │  • Hyphens w/space│                 │
│   └──────────────────┘  └──────────────────┘  └──────────────────┘                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SNIPPET EXTRACTION                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   From any hub content, extract standalone pieces:                                  │
│                                                                                      │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│   │  HOT TAKES  │  │    STATS    │  │   STORIES   │  │   HOW-TO    │               │
│   │  (opinions) │  │   (data)    │  │   (arcs)    │  │   (tips)    │               │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘               │
│          │                │                │                │                       │
│          └────────────────┴────────────────┴────────────────┘                       │
│                                        │                                            │
│                                        ▼                                            │
│                            ┌─────────────────────┐                                  │
│                            │  SNIPPET + TYPE     │                                  │
│                            │  ready for routing  │                                  │
│                            └─────────────────────┘                                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         FRAMEWORK FITTING (ROUTING)                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                            ┌─────────────────────┐                                  │
│                            │    text-content     │                                  │
│                            │   (master router)   │                                  │
│                            │                     │                                  │
│                            │  TEMPLATE_INDEX.md  │                                  │
│                            │  (lightweight)      │                                  │
│                            └──────────┬──────────┘                                  │
│                                       │                                             │
│       ┌───────────────┬───────────────┼───────────────┬───────────────┐            │
│       ▼               ▼               ▼               ▼               ▼            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│  │LinkedIn │    │    X    │    │Instagram│    │Facebook │    │ YouTube │          │
│  │         │    │         │    │         │    │         │    │ Shorts  │          │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘          │
│       │              │              │              │              │                │
│       ▼              ▼              ▼              ▼              ▼                │
│  references/    references/    references/    references/    video-caption-       │
│  linkedin/      templates/     platforms/     platforms/     creation             │
│                 post-          instagram-     facebook.md                         │
│  • authority    structures     captions.md                                        │
│  • contrarian   • one-liners                                                      │
│  • story        • justin-welsh                                                    │
│  • engagement                                                                      │
│  • list                                                                            │
│  • community                                                                       │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              QUALITY GATE                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                            ┌─────────────────────┐                                  │
│                            │    quality-loop     │                                  │
│                            │    (5-judge)        │                                  │
│                            └──────────┬──────────┘                                  │
│                                       │                                             │
│       ┌───────────────┬───────────────┼───────────────┬───────────────┐            │
│       ▼               ▼               ▼               ▼               ▼            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│  │  Voice  │    │ Clarity │    │  Value  │    │   CTA   │    │ AI-Tell │          │
│  │  Judge  │    │  Judge  │    │  Judge  │    │  Judge  │    │  Judge  │          │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘          │
│                                                                                      │
│   PASS → Schedule    |    FAIL → Revise with specific feedback                      │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT / SCHEDULING                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌─────────────────────┐      ┌─────────────────────┐                             │
│   │  GetLate API        │      │  Social_Scheduling  │                             │
│   │  (8 platforms)      │      │  .md (manual)       │                             │
│   └─────────────────────┘      └─────────────────────┘                             │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Hub-Specific Workflows

### 1. Podcast Production Chain

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            PODCAST → MULTI-PLATFORM                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

INPUT: Raw recording + guest info
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CHECKPOINT 1: TRANSCRIPT                                                            │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │ youtube-downloader │  ← If source is YouTube                                     │
│  │ (transcript only)  │                                                             │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│            ▼                                                                         │
│  ┌────────────────────┐                                                             │
│  │transcript-polisher │  ← Remove filler, fix grammar, add structure                │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│            ▼                                                                         │
│       Polished transcript + clip timestamp candidates                               │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CHECKPOINT 2: CLIPS                                                                 │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │youtube-clip-       │                                                             │
│  │extractor           │                                                             │
│  │                    │                                                             │
│  │ Phase 2: Analyze   │  ← Hook/coda criteria, quality tests                        │
│  │ Phase 3: Cut       │  ← ffmpeg extraction                                        │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│            ▼                                                                         │
│       3-5 video clips (30-90 sec each)                                              │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CHECKPOINT 3: CAPTIONS & HOOKS                                                      │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │video-caption-      │                                                             │
│  │creation            │                                                             │
│  │                    │                                                             │
│  │ • Triple Word Score│  ← Audio + On-Screen + Caption + Hashtags                   │
│  │ • Hook categories  │  ← Polarizing, Counter-Intuitive, Challenge, Curiosity      │
│  │ • McDonald's Test  │  ← Accessible language check                                │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│            ▼                                                                         │
│       CLIP_PACKAGE.md per clip (hooks + platform captions)                          │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CHECKPOINT 4: DISTRIBUTION                                                          │
│                                                                                      │
│  FOR EACH CLIP:                                                                      │
│                                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ TikTok   │  │Instagram │  │ YouTube  │  │ Facebook │  │ LinkedIn │              │
│  │ Reels    │  │ Reels    │  │ Shorts   │  │ Reels    │  │ Video    │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │             │             │                     │
│       │    ┌────────┴─────────────┴─────────────┘             │                     │
│       │    │                                                   │                     │
│       │    ▼                                                   ▼                     │
│       │  video-caption-creation              text-content + video                   │
│       │  (same caption strategy)             (LinkedIn-specific post)               │
│       │                                                                              │
│       ▼                                                                              │
│  Same video, different captions per platform                                        │
│                                                                                      │
│  ALSO GENERATE:                                                                      │
│  ┌────────────────────┐                                                             │
│  │ podcast-blog-post- │  ← Narrative blog post (~1,000 words)                       │
│  │ creator            │                                                             │
│  └────────────────────┘                                                             │
│                                                                                      │
│  OUTPUT: 12-25 social posts + 1 blog post per episode                               │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Newsletter Production Chain

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          NEWSLETTER → MULTI-PLATFORM                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘

INPUT: Topic brief, sources, angle
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: WRITE NEWSLETTER                                                           │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐│
│  │                      opened-daily-newsletter-writer                              ││
│  │                                                                                  ││
│  │  Structure: THOUGHT → TREND → TOOL (TTT)                                        ││
│  │                                                                                  ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                 ││
│  │  │     THOUGHT     │  │      TREND      │  │      TOOL       │                 ││
│  │  │                 │  │                 │  │                 │                 ││
│  │  │ Contrarian take │  │ Data/research/  │  │ Practical       │                 ││
│  │  │ on education    │  │ news item       │  │ resource        │                 ││
│  │  │                 │  │                 │  │                 │                 ││
│  │  │ Substance→Take  │  │ Stats + context │  │ Recommendation  │                 ││
│  │  │ pattern         │  │                 │  │                 │                 ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                 ││
│  │                                                                                  ││
│  │  References:                                                                     ││
│  │  • pirate-wires-segment-techniques.md (7 techniques)                            ││
│  │  • opening-letter-patterns.md (12+ examples)                                    ││
│  │  • witty-voice-patterns.md                                                      ││
│  │                                                                                  ││
│  └─────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │newsletter-subject- │  ← 10+ options, 10 Commandments scoring                     │
│  │lines               │                                                             │
│  │                    │                                                             │
│  │ references/        │                                                             │
│  │ • 10-commandments  │                                                             │
│  │ • sticky-techniques│                                                             │
│  │ • analyzed-examples│                                                             │
│  └────────────────────┘                                                             │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: QUALITY GATE                                                               │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │    quality-loop    │  ← Full 5-judge review                                      │
│  │    (5 judges)      │                                                             │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│       PASS → Send newsletter                                                        │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: EXTRACT SOCIAL SPOKES                                                      │
│                                                                                      │
│  From each TTT segment, extract standalone snippet:                                 │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐│
│  │  THOUGHT segment → Hot take (opinion)                                           ││
│  │  TREND segment → Stat + interpretation                                          ││
│  │  TOOL segment → Practical recommendation                                        ││
│  └─────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                      │
│  FOR EACH SNIPPET:                                                                   │
│                                                                                      │
│  ┌─────────────────────┐                                                            │
│  │    text-content     │  ← Match to templates                                      │
│  │                     │                                                            │
│  │  TEMPLATE_INDEX.md  │  ← Quick lookup by snippet type                            │
│  └──────────┬──────────┘                                                            │
│             │                                                                        │
│    ┌────────┴────────┬────────────────┬────────────────┐                           │
│    ▼                 ▼                ▼                ▼                            │
│  ┌──────────┐  ┌──────────┐    ┌──────────┐    ┌──────────┐                        │
│  │ LinkedIn │  │    X     │    │Instagram │    │ Facebook │                        │
│  └────┬─────┘  └────┬─────┘    └────┬─────┘    └────┬─────┘                        │
│       │             │               │               │                               │
│       ▼             ▼               ▼               ▼                               │
│                                                                                      │
│  THOUGHT → Contrarian    Paradox Hook    Quote card     Engagement                  │
│            template      or Binary       (visual)       hook                        │
│                                                                                      │
│  TREND →   Authority     Commentary      Carousel       Question                    │
│            (stats)       (stat+take)     (data viz)     post                        │
│                                                                                      │
│  TOOL →    List/How-to   Thread          Carousel       Share                       │
│                          (tool+benefits) (steps)                                    │
│                                                                                      │
│  OUTPUT: 6-9 social posts per newsletter                                            │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3. Deep Dive / SEO Article Chain

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          DEEP DIVE → MULTI-PLATFORM                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

INPUT: Keyword research (DataForSEO)
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: RESEARCH                                                                   │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │   seo-research     │  ← DataForSEO keyword gap analysis                          │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│       Target keyword + search intent + competitor gaps                              │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: WRITE                                                                      │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │open-education-hub- │                                                             │
│  │deep-dives          │                                                             │
│  │                    │                                                             │
│  │ Structure:         │                                                             │
│  │ • Hook (intent)    │                                                             │
│  │ • Overview         │                                                             │
│  │ • Deep H2 sections │                                                             │
│  │ • Internal links   │  ← Master_Content_Index.md                                  │
│  │ • FAQ (long-tail)  │                                                             │
│  │ • CTA              │                                                             │
│  └─────────┬──────────┘                                                             │
│            │                                                                         │
│  ┌────────────────────┐                                                             │
│  │  article-titles    │  ← 15 formulas, 10 Commandments                             │
│  │                    │                                                             │
│  │  references/       │                                                             │
│  │  • headline-formulas│                                                            │
│  │  • sticky-techniques│                                                            │
│  │  • 10-commandments │                                                             │
│  └────────────────────┘                                                             │
│                                                                                      │
│       2,000-3,000 word article                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: QUALITY + PUBLISH                                                          │
│                                                                                      │
│  ┌────────────────────┐      ┌────────────────────┐                                │
│  │    quality-loop    │  →   │ Webflow publish    │                                │
│  │    (extended)      │      │ + meta description │                                │
│  │                    │      │ + featured image   │                                │
│  │  + SEO judge       │      │                    │                                │
│  │  + internal links  │      │ image-prompt-      │                                │
│  │                    │      │ generator          │                                │
│  └────────────────────┘      └────────────────────┘                                │
└──────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: SOCIAL DISTRIBUTION                                                        │
│                                                                                      │
│  Extract 3-5 standalone insights from article                                       │
│                                                                                      │
│  ┌────────────────────┐                                                             │
│  │    text-content    │  ← Framework fitting                                        │
│  └──────────┬─────────┘                                                             │
│             │                                                                        │
│    ┌────────┴────────┬────────────────┐                                            │
│    ▼                 ▼                ▼                                             │
│  LinkedIn         X Thread         X Single                                         │
│  Authority        (5-7 tweets)     Commentary                                       │
│                                                                                      │
│  All posts link back to full article                                                │
│                                                                                      │
│  OUTPUT: 10-15 posts driving traffic to deep dive                                   │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Social Media Skill Detail

### text-content Skill Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              text-content SKILL                                      │
│                           (Master Social Router)                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  SKILL.md (Core)                                                                     │
│  • Framework fitting methodology                                                    │
│  • Snippet type → Template matching logic                                           │
│  • Platform routing rules                                                           │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  references/templates/TEMPLATE_INDEX.md (Lightweight - ~200 tokens)                 │
│                                                                                      │
│  Quick lookup table:                                                                │
│  ┌───────────────┬────────────────────────────────────────────────────────────┐    │
│  │ Snippet Type  │ LinkedIn           │ X                │ Instagram          │    │
│  ├───────────────┼────────────────────┼──────────────────┼────────────────────┤    │
│  │ Hot take      │ contrarian.md      │ post-structures  │ one-liners.md      │    │
│  │ Stat          │ authority.md       │ post-structures  │ carousel concept   │    │
│  │ Story         │ story.md           │ post-structures  │ reel caption       │    │
│  │ How-to        │ list.md            │ post-structures  │ carousel concept   │    │
│  │ Quote         │ authority.md       │ post-structures  │ quote card         │    │
│  └───────────────┴────────────────────┴──────────────────┴────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  references/        │    │  references/        │    │  references/        │
│  linkedin/          │    │  templates/         │    │  platforms/         │
│                     │    │                     │    │                     │
│  ┌───────────────┐  │    │  ┌───────────────┐  │    │  ┌───────────────┐  │
│  │ authority.md  │  │    │  │post-structures│  │    │  │ facebook.md   │  │
│  │ (stats/expert)│  │    │  │ (360+ X fmts) │  │    │  │               │  │
│  ├───────────────┤  │    │  ├───────────────┤  │    │  ├───────────────┤  │
│  │ contrarian.md │  │    │  │ one-liners.md │  │    │  │ instagram-    │  │
│  │ (hot takes)   │  │    │  │ (dude w/sign) │  │    │  │ captions.md   │  │
│  ├───────────────┤  │    │  ├───────────────┤  │    │  ├───────────────┤  │
│  │ story.md      │  │    │  │ justin-welsh  │  │    │  │ x-twitter.md  │  │
│  │ (narratives)  │  │    │  │ .md (swipes)  │  │    │  │               │  │
│  ├───────────────┤  │    │  ├───────────────┤  │    │  └───────────────┘  │
│  │ engagement.md │  │    │  │ linkedin-     │  │    │                     │
│  │ (questions)   │  │    │  │ swipe-file.md │  │    │                     │
│  ├───────────────┤  │    │  └───────────────┘  │    │                     │
│  │ list.md       │  │    │                     │    │                     │
│  │ (how-to)      │  │    │                     │    │                     │
│  ├───────────────┤  │    │                     │    │                     │
│  │ community.md  │  │    │                     │    │                     │
│  │ (connection)  │  │    │                     │    │                     │
│  └───────────────┘  │    │                     │    │                     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

---

### Video Content Skill Chain

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            VIDEO CONTENT SKILLS                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  SOURCE: Existing video OR new concept                                              │
└─────────────────────────────────────────────────────────────────────────────────────┘
           │                                              │
           ▼                                              ▼
┌─────────────────────────┐                  ┌─────────────────────────┐
│  FROM YOUTUBE URL       │                  │  NEW SHORT-FORM         │
│                         │                  │                         │
│  ┌───────────────────┐  │                  │  ┌───────────────────┐  │
│  │ youtube-downloader│  │                  │  │ short-form-video  │  │
│  │ (transcript)      │  │                  │  │                   │  │
│  └─────────┬─────────┘  │                  │  │ FORMAT_INVENTORY  │  │
│            │            │                  │  │ • Pointing Format │  │
│            ▼            │                  │  │ • Tablet Swivel   │  │
│  ┌───────────────────┐  │                  │  │ • Ed the Horse    │  │
│  │youtube-clip-      │  │                  │  │ • Fridge Magnet   │  │
│  │extractor          │  │                  │  │ (Tier 1-4)        │  │
│  │                   │  │                  │  └─────────┬─────────┘  │
│  │ Phase 1: Download │  │                  │            │            │
│  │ Phase 2: Analyze  │  │                  │            │            │
│  │ Phase 3: Cut      │  │                  │            │            │
│  │ Phase 4: Caption  │  │                  │            │            │
│  └─────────┬─────────┘  │                  │            │            │
│            │            │                  │            │            │
└────────────┼────────────┘                  └────────────┼────────────┘
             │                                            │
             └────────────────────┬───────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  video-caption-creation │
                    │                         │
                    │  • Triple Word Score    │
                    │  • Hook categories      │
                    │  • Platform captions    │
                    │  • Hashtag strategy     │
                    │  • McDonald's Test      │
                    └─────────────┬───────────┘
                                  │
                                  ▼
           ┌──────────────────────┴──────────────────────┐
           │                                             │
           ▼                                             ▼
┌─────────────────────────┐              ┌─────────────────────────┐
│  VIDEO PLATFORMS        │              │  TEXT PLATFORMS         │
│                         │              │  (about the video)      │
│  • TikTok               │              │                         │
│  • Instagram Reels      │              │  text-content           │
│  • YouTube Shorts       │              │  └→ LinkedIn video post │
│  • Facebook Reels       │              │  └→ X thread about clip │
│                         │              │                         │
│  Same video,            │              │  Framework fitting for  │
│  different captions     │              │  text posts promoting   │
│                         │              │  the video              │
└─────────────────────────┘              └─────────────────────────┘
```

---

## Skill Dependency Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          SKILL DEPENDENCIES                                          │
│                    (← means "loads/references")                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

ALWAYS LOADED (every public content task):
├── opened-identity ← brand voice, Sarah persona
├── ai-tells ← hard blocks, words to avoid
└── CLAUDE.md Writing Rules ← correlatives, dashes

NEWSLETTER CHAIN:
├── opened-daily-newsletter-writer
│   ├── ← pirate-wires-segment-techniques.md
│   ├── ← opening-letter-patterns.md
│   └── ← witty-voice-patterns.md
├── newsletter-subject-lines
│   ├── ← 10-commandments-checklist.md
│   ├── ← sticky-sentence-techniques.md
│   └── ← newsletter-subject-lines-analyzed.md
└── quality-loop (5-judge)

PODCAST CHAIN:
├── podcast-production (4 checkpoints)
├── youtube-downloader (transcript)
├── transcript-polisher
├── youtube-clip-extractor
│   └── ← video-caption-creation
├── video-caption-creation
│   └── ← Triple Word Score inline
└── text-content (for LinkedIn posts about clips)

DEEP DIVE CHAIN:
├── seo-research (DataForSEO)
├── open-education-hub-deep-dives
│   └── ← Master_Content_Index.md (internal links)
├── article-titles
│   ├── ← headline-formulas-library.md
│   ├── ← sticky-sentence-techniques.md
│   └── ← 10-commandments-checklist.md
├── quality-loop (extended)
├── image-prompt-generator (featured image)
└── text-content (social promotion)

SOCIAL (text-content) INTERNALS:
├── SKILL.md (framework fitting)
├── TEMPLATE_INDEX.md (quick lookup)
├── references/linkedin/
│   ├── authority.md
│   ├── contrarian.md
│   ├── story.md
│   ├── engagement.md
│   ├── list.md
│   └── community.md
├── references/templates/
│   ├── post-structures.md (360+ X formats)
│   ├── one-liners.md
│   ├── justin-welsh.md
│   └── linkedin-swipe-file.md
└── references/platforms/
    ├── facebook.md
    ├── instagram-captions.md
    └── x-twitter.md

VIDEO CHAIN:
├── short-form-video (production)
│   └── ← FORMAT_INVENTORY.md
├── youtube-clip-extractor
│   ├── ← youtube-downloader (Phase 1 alternative)
│   └── ← video-caption-creation (Phase 4)
└── video-caption-creation
    ├── ← Hook categories inline
    └── ← Triple Word Score inline
```

---

## Platform-Specific Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    PLATFORM → SKILL MAPPING                                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┬───────────────────────────────────────────────────────────────────────┐
│  LINKEDIN   │                                                                       │
├─────────────┼───────────────────────────────────────────────────────────────────────┤
│ Text posts  │ text-content → references/linkedin/ (6 templates)                    │
│ Video posts │ video-caption-creation + text-content (post about video)             │
│ Tone        │ Professional authority, stats-driven, thought leadership             │
│ Hashtags    │ 3-5                                                                   │
└─────────────┴───────────────────────────────────────────────────────────────────────┘

┌─────────────┬───────────────────────────────────────────────────────────────────────┐
│  X/TWITTER  │                                                                       │
├─────────────┼───────────────────────────────────────────────────────────────────────┤
│ Single post │ text-content → references/templates/post-structures.md               │
│ Thread      │ text-content → references/templates/post-structures.md               │
│ One-liner   │ text-content → references/templates/one-liners.md                    │
│ Tone        │ Punchy, scroll-stopping, concise                                     │
│ Hashtags    │ 0-3 (usually none)                                                   │
└─────────────┴───────────────────────────────────────────────────────────────────────┘

┌─────────────┬───────────────────────────────────────────────────────────────────────┐
│  INSTAGRAM  │                                                                       │
├─────────────┼───────────────────────────────────────────────────────────────────────┤
│ Reels       │ video-caption-creation (caption + hashtags)                          │
│ Posts       │ text-content → references/platforms/instagram-captions.md            │
│ Quote cards │ image-prompt-generator + one-liner                                   │
│ Carousels   │ Manual (concept from text-content)                                   │
│ Tone        │ Casual, visual-first, emoji OK                                       │
│ Hashtags    │ 5-10                                                                  │
└─────────────┴───────────────────────────────────────────────────────────────────────┘

┌─────────────┬───────────────────────────────────────────────────────────────────────┐
│  FACEBOOK   │                                                                       │
├─────────────┼───────────────────────────────────────────────────────────────────────┤
│ Posts       │ text-content → references/platforms/facebook.md                      │
│ Reels       │ video-caption-creation (longer caption, NO hashtags)                 │
│ Tone        │ Conversational, engagement-driving, question-ending                  │
│ Hashtags    │ 0-2 (usually none - kills reach)                                     │
│ Links       │ In comments only (not main post)                                     │
└─────────────┴───────────────────────────────────────────────────────────────────────┘

┌─────────────┬───────────────────────────────────────────────────────────────────────┐
│  YOUTUBE    │                                                                       │
├─────────────┼───────────────────────────────────────────────────────────────────────┤
│ Shorts      │ video-caption-creation (include #Shorts)                             │
│ Long-form   │ youtube-title-creator + manual description                           │
│ Clips       │ youtube-clip-extractor (full workflow)                               │
│ Tone        │ Hook-heavy first 3 seconds, CTR-optimized titles                     │
│ Hashtags    │ 3-5 + #Shorts                                                        │
└─────────────┴───────────────────────────────────────────────────────────────────────┘

┌─────────────┬───────────────────────────────────────────────────────────────────────┐
│  TIKTOK     │                                                                       │
├─────────────┼───────────────────────────────────────────────────────────────────────┤
│ Videos      │ video-caption-creation                                               │
│ Tone        │ Trend-aware, casual, emoji OK, trending sounds                       │
│ Hashtags    │ 3-5 (mix trending + niche)                                           │
└─────────────┴───────────────────────────────────────────────────────────────────────┘
```

---

## Gaps / Future Development

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          IDENTIFIED GAPS                                             │
└─────────────────────────────────────────────────────────────────────────────────────┘

1. ARCHIVE REPURPOSING ✅ DONE
   - archive-suggest skill created
   - Posts to Slack for triage

2. NEARBOUND TAGGING ✅ DONE
   - 81 profiles in Studio/Nearbound Pipeline/people/
   - @handles included for social tagging

3. INSTAGRAM COVERAGE
   - Carousel workflow is manual
   - Quote card → nano-banana exists but not integrated
   - Stories workflow undefined

4. ANALYTICS FEEDBACK LOOP
   - weekly_social_report.py exists
   - No automatic template performance tracking
   - Future: Which templates → which engagement?

5. CURATION PIPELINE
   - RSS work moved to Projects/RSS-Curation/
   - Future: automated Slack posting for triage

6. VIDEO-TO-TEXT BRIDGE
   - Clips generate captions but not text posts ABOUT the clips
   - Could auto-generate LinkedIn text posts for each clip
   - Future: clip-to-text-posts sub-skill
```

---

*This map reflects the skill architecture as of 2026-01-29. Update when skills are refactored or new chains are added.*
