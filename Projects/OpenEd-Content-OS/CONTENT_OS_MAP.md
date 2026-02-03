# OpenEd Content OS - Complete System Map

**Created:** 2026-01-30
**Purpose:** Visual map of all skills, workflows, and integrations

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FOUNDATION LAYER                                       │
│         (Applied to ALL content - these are always active)                       │
│                                                                                  │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│   │ opened-identity │  │    ai-tells     │  │   ghostwriter   │                │
│   │                 │  │                 │  │                 │                │
│   │ Brand values,   │  │ Forbidden       │  │ Source → prose  │                │
│   │ Sarah persona,  │  │ patterns,       │  │ conversion,     │                │
│   │ messaging       │  │ AI vocabulary,  │  │ voice matching, │                │
│   │ framework       │  │ syntax to avoid │  │ anti-AI writing │                │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│                                                                                  │
│   ┌─────────────────┐  ┌─────────────────┐                                     │
│   │  quality-loop   │  │ guidelines-brand│                                     │
│   │                 │  │                 │                                     │
│   │ 5-judge gate    │  │ Visual identity │                                     │
│   │ for long-form,  │  │ colors, fonts,  │                                     │
│   │ 3-judge for     │  │ spacing specs   │                                     │
│   │ social posts    │  │ (design only)   │                                     │
│   └─────────────────┘  └─────────────────┘                                     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            INPUT LAYER                                           │
│              (External data sources feeding into the system)                     │
│                                                                                  │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │ seomachine  │    │rss-curation │    │  youtube-   │    │  archive-   │    │
│   │             │    │             │    │  downloader │    │  suggest    │    │
│   │ DataForSEO, │    │ 64 RSS feeds│    │             │    │             │    │
│   │ GA4, GSC    │    │ → Slack     │    │ YouTube →   │    │ Archive →   │    │
│   │ → keywords, │    │ curation    │    │ transcripts │    │ daily       │    │
│   │ rankings    │    │             │    │             │    │ suggestions │    │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
│          │                  │                  │                  │            │
└──────────┼──────────────────┼──────────────────┼──────────────────┼────────────┘
           │                  │                  │                  │
           ▼                  ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION LAYER                                         │
│                    (Hub content creation workflows)                              │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        NEWSLETTER WORKFLOW                               │   │
│  │                                                                          │   │
│  │  Sources ──► opened-daily-newsletter-writer ──► newsletter-subject-lines │   │
│  │              (Mon-Thu, 500-800 words,            (10+ options,           │   │
│  │               Thought-Trend-Tool)                 10 Commandments)       │   │
│  │                        │                                                 │   │
│  │                        ├──────────────────────────────────────────┐      │   │
│  │                        │                                          │      │   │
│  │                        ▼                                          ▼      │   │
│  │              hubspot-email-draft                      newsletter-to-social│   │
│  │              (markdown → HubSpot)                     (6-9 social posts)  │   │
│  │                                                                          │   │
│  │  ────────────────────────────────────────────────────────────────────    │   │
│  │                                                                          │   │
│  │  Weekly ──► opened-weekly-newsletter-writer                              │   │
│  │  sources    (Friday digest, 1500-2500 words,                             │   │
│  │             consolidates week's content)                                 │   │
│  │                        │                                                 │   │
│  │                        └──► Ed's Roundup X thread                        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         PODCAST WORKFLOW                                 │   │
│  │                                                                          │   │
│  │  Recording ──► transcript-polisher ──► podcast-production (4 checkpoints)│   │
│  │                (cleanup, structure)    │                                 │   │
│  │                                        ├─► narrative-snippets            │   │
│  │                                        │   (extract story beats)         │   │
│  │                                        │                                 │   │
│  │                                        ├─► cold-open-creator             │   │
│  │                                        │   (25-35 sec hooks)             │   │
│  │                                        │                                 │   │
│  │                                        ├─► youtube-clip-extractor        │   │
│  │                                        │   (identify + cut clips)        │   │
│  │                                        │         │                       │   │
│  │                                        │         ▼                       │   │
│  │                                        │   video-caption-creation        │   │
│  │                                        │   (Triple Word Score hooks)     │   │
│  │                                        │                                 │   │
│  │                                        ├─► youtube-title-creator         │   │
│  │                                        │   (119 formulas for CTR)        │   │
│  │                                        │                                 │   │
│  │                                        └─► podcast-blog-post-creator     │   │
│  │                                            (episode → ~1000 word post)   │   │
│  │                                                     │                    │   │
│  │                                                     ▼                    │   │
│  │                                            webflow-publish               │   │
│  │                                                     │                    │   │
│  │                                                     ▼                    │   │
│  │                                            newsletter-to-social          │   │
│  │                                                                          │   │
│  │  ──────── FEEDS INTO NEWSLETTER ────────                                 │   │
│  │  Podcast clips + insights can become newsletter segments                 │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      SEO CONTENT WORKFLOW                                │   │
│  │                                                                          │   │
│  │  seomachine ──► seo-content-production ──► open-education-hub-deep-dives │   │
│  │  (keywords)     (orchestrates full        (1500-4000 words,              │   │
│  │                  workflow)                 proprietary + SEO)            │   │
│  │                        │                                                 │   │
│  │                        ├─► article-titles                                │   │
│  │                        │   (15 formulas, 10+ options)                    │   │
│  │                        │                                                 │   │
│  │                        ├─► nano-banana-image-generator                   │   │
│  │                        │   (thumbnails via Gemini)                       │   │
│  │                        │                                                 │   │
│  │                        └─► webflow-publish                               │   │
│  │                                   │                                      │   │
│  │                                   ▼                                      │   │
│  │                          newsletter-to-social                            │   │
│  │                                                                          │   │
│  │  ──────── FEEDS INTO NEWSLETTER ────────                                 │   │
│  │  Deep dives become "Trend" segment in daily newsletter                   │   │
│  │                                                                          │   │
│  │  ──────── RELATED CONTENT TYPES ────────                                 │   │
│  │                                                                          │   │
│  │  verified-review        day-in-the-life                                  │   │
│  │  (curriculum/tool       (family profile                                  │   │
│  │   reviews with          posts with                                       │   │
│  │   real families)        schedules)                                       │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      VIDEO / SHORT-FORM WORKFLOW                         │   │
│  │                                                                          │   │
│  │  Concept ──► short-form-video ──► video-caption-creation                 │   │
│  │              (Sponge-then-      (hooks + captions                        │   │
│  │               Sharpen method)    + hashtags)                             │   │
│  │                                         │                                │   │
│  │                                         ▼                                │   │
│  │                                  schedule-approved                       │   │
│  │                                  (Notion → GetLate)                      │   │
│  │                                                                          │   │
│  │  ──────── SOURCES FROM OTHER WORKFLOWS ────────                          │   │
│  │  • Podcast clips (youtube-clip-extractor)                                │   │
│  │  • Newsletter segments (dude-with-sign-writer for hooks)                 │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      PAID ADS WORKFLOW                                   │   │
│  │                                                                          │   │
│  │  Brief ──► meta-ads-creative ──► dude-with-sign-writer                   │   │
│  │            (6 Elements          (punchy one-liners                       │   │
│  │             framework,           for text-only ads)                      │   │
│  │             lo-fi native)                                                │   │
│  │                  │                                                       │   │
│  │                  ├─► nano-banana-image-generator                         │   │
│  │                  │   (ad visuals)                                        │   │
│  │                  │                                                       │   │
│  │                  └─► single-panel-comic                                  │   │
│  │                      (editorial comics for                               │   │
│  │                       education critique)                                │   │
│  │                                                                          │   │
│  │  ──────── INDEPENDENT WORKFLOW ────────                                  │   │
│  │  Ads don't feed back into other content (paid vs organic separation)    │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        DISTRIBUTION LAYER                                        │
│              (Multiplying and routing content to platforms)                      │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                    CONTENT MULTIPLICATION                                │  │
│   │                                                                          │  │
│   │   Hub Content ──► content-repurposer ──► text-content (360+ templates)  │  │
│   │   (any source)    (framework fitting     │                              │  │
│   │                    specialist)           ├─► LinkedIn templates         │  │
│   │                           │              ├─► X/Twitter templates        │  │
│   │                           │              ├─► Instagram templates        │  │
│   │                           │              └─► Facebook templates         │  │
│   │                           │                                              │  │
│   │                           ▼                                              │  │
│   │                  x-article-converter                                     │  │
│   │                  (blog → X Article                                       │  │
│   │                   with handles)                                          │  │
│   │                                                                          │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                    DISTRIBUTION CHANNELS                                 │  │
│   │                                                                          │  │
│   │   Content ──► slack-social-distribution ──► #market-daily               │  │
│   │               (threaded Slack posts          (team review)              │  │
│   │                for team approval)                                       │  │
│   │                       │                                                  │  │
│   │                       ▼                                                  │  │
│   │               schedule-approved ──────────► GetLate API                  │  │
│   │               (Notion → GetLate             (8 platforms)               │  │
│   │                bridge)                                                   │  │
│   │                                                                          │  │
│   │   Direct posting:                                                        │  │
│   │               x-posting ──────────────────► X/Twitter                    │  │
│   │               (framework fitting            (direct via API)            │  │
│   │                + scheduling)                                             │  │
│   │                                                                          │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        OUTPUT LAYER                                              │
│              (External platforms and systems receiving content)                  │
│                                                                                  │
│   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │
│   │   HubSpot   │ │   Webflow   │ │   GetLate   │ │    Slack    │             │
│   │             │ │             │ │             │ │             │             │
│   │ Newsletter  │ │ Blog posts, │ │ 8 platforms:│ │ #market-    │             │
│   │ drafts via  │ │ deep dives  │ │ LinkedIn    │ │ daily for   │             │
│   │ hubspot-    │ │ via         │ │ X/Twitter   │ │ approval    │             │
│   │ email-draft │ │ webflow-    │ │ Instagram   │ │             │             │
│   │             │ │ publish     │ │ Facebook    │ │ #content-   │             │
│   │             │ │             │ │ TikTok      │ │ inbox for   │             │
│   │             │ │ ◄─── SYNC   │ │ YouTube     │ │ curation    │             │
│   │             │ │ Back to     │ │ Pinterest   │ │             │             │
│   │             │ │ Master      │ │ Threads     │ │             │             │
│   │             │ │ Content     │ │             │ │             │             │
│   │             │ │ Index       │ │             │ │             │             │
│   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘             │
│                                                                                  │
│   ┌─────────────┐ ┌─────────────┐                                              │
│   │   Notion    │ │   YouTube   │                                              │
│   │             │ │             │                                              │
│   │ Content     │ │ Full eps +  │                                              │
│   │ staging via │ │ Shorts via  │                                              │
│   │ schedule-   │ │ youtube-    │                                              │
│   │ approved    │ │ clip-       │                                              │
│   │             │ │ extractor   │                                              │
│   └─────────────┘ └─────────────┘                                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     POST-PUBLICATION LAYER                                       │
│              (After content is live - analytics, outreach, archiving)           │
│                                                                                  │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐               │
│   │outreach-email-  │  │  work-summary   │  │  seomachine     │               │
│   │draft            │  │                 │  │  (analytics)    │               │
│   │                 │  │ Git commits →   │  │                 │               │
│   │ Notify guests,  │  │ Slack updates   │  │ Track rankings, │               │
│   │ quoted experts, │  │ for team        │  │ traffic, CTR    │               │
│   │ featured tools  │  │ visibility      │  │ opportunities   │               │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Bi-Directional Flows (Content Feeding Between Workflows)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     CROSS-WORKFLOW CONTENT FLOWS                                 │
│                                                                                  │
│   PODCAST ────────────────────────────────► NEWSLETTER                          │
│   • Guest insights become "Thought" segment                                     │
│   • Clips become newsletter visual elements                                     │
│   • Episode summaries become "Trend" content                                    │
│                                                                                  │
│   SEO CONTENT ────────────────────────────► NEWSLETTER                          │
│   • Deep dives become "Trend" segment                                           │
│   • Comparison articles fuel topic ideas                                        │
│   • Stats/data become "Thought" material                                        │
│                                                                                  │
│   NEWSLETTER ────────────────────────────► SOCIAL                               │
│   • Each newsletter → 6-9 social posts                                          │
│   • Subject line testing informs hooks                                          │
│                                                                                  │
│   PODCAST ────────────────────────────────► VIDEO                               │
│   • youtube-clip-extractor pulls clips                                          │
│   • Clips become Reels/Shorts/TikToks                                           │
│                                                                                  │
│   SOCIAL ─────────────────────────────────► PODCAST                             │
│   • High-performing posts indicate topics                                       │
│   • Social engagement informs guest selection                                   │
│                                                                                  │
│   RSS CURATION ───────────────────────────► NEWSLETTER                          │
│   • Curated articles become "Tool" segment                                      │
│   • External content provides commentary material                               │
│                                                                                  │
│   ARCHIVE ────────────────────────────────► SOCIAL                              │
│   • archive-suggest resurfaces evergreen content                                │
│   • Old posts get fresh hooks and framing                                       │
│                                                                                  │
│   WEBFLOW ────────────────────────────────► VAULT                               │
│   • Published content syncs to Master Content Index                             │
│   • Enables archive-suggest and internal linking                                │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Skill Status Inventory

### Foundation Skills (Always Active)
| Skill | Purpose | Status |
|-------|---------|--------|
| `opened-identity` | Brand values, Sarah persona, messaging framework | ✅ Active |
| `ai-tells` | Forbidden AI patterns, vocabulary, syntax | ✅ Active |
| `ghostwriter` | Source → authentic prose conversion | ✅ Active |
| `quality-loop` | 5-judge (long-form) / 3-judge (social) gates | ✅ Active |
| `guidelines-brand` | Visual identity specs (design only) | ✅ Active |

### Production Skills
| Skill | Purpose | Workflow | Status |
|-------|---------|----------|--------|
| `opened-daily-newsletter-writer` | Mon-Thu newsletters, TTT structure | Newsletter | ✅ Active |
| `opened-weekly-newsletter-writer` | Friday digest, consolidates week | Newsletter | ✅ Active |
| `podcast-production` | 4-checkpoint episode workflow | Podcast | ✅ Active |
| `seo-content-production` | Orchestrates full SEO workflow | SEO | ✅ Active |
| `open-education-hub-deep-dives` | 1500-4000 word SEO articles | SEO | ✅ Active |
| `meta-ads-creative` | 6 Elements framework for ads | Paid Ads | ✅ Active |
| `short-form-video` | Sponge-then-Sharpen video method | Video | ✅ Active |

### Distribution Skills
| Skill | Purpose | Integration | Status |
|-------|---------|-------------|--------|
| `newsletter-to-social` | Newsletter → 6-9 social posts | Slack | ✅ Active |
| `content-repurposer` | Framework fitting any source | None | ✅ Active |
| `text-content` | 360+ social templates | None | ✅ Active |
| `x-posting` | X/Twitter posting + scheduling | GetLate | ✅ Active |
| `slack-social-distribution` | Posts to #market-daily | Slack | ✅ Active |
| `schedule-approved` | Notion → GetLate bridge | Notion, GetLate | ✅ Active |

### Specialized Production Skills
| Skill | Purpose | Parent Workflow | Status |
|-------|---------|-----------------|--------|
| `article-titles` | 15 formulas, 10+ title options | SEO | ✅ Active |
| `newsletter-subject-lines` | Subject line optimization | Newsletter | ✅ Active |
| `cold-open-creator` | 25-35 sec podcast hooks | Podcast | ✅ Active |
| `narrative-snippets` | Extract story beats | Podcast | ✅ Active |
| `transcript-polisher` | Cleanup raw transcripts | Podcast | ✅ Active |
| `video-caption-creation` | Triple Word Score hooks | Video | ✅ Active |
| `youtube-title-creator` | 119 CTR formulas | Podcast/Video | ✅ Active |
| `youtube-clip-extractor` | Identify + cut clips | Podcast | ✅ Active |
| `dude-with-sign-writer` | Punchy one-liners | Ads, Social | ✅ Active |
| `single-panel-comic` | Editorial comics | Ads, Social | ✅ Active |

### Integration Skills
| Skill | Purpose | External System | Status |
|-------|---------|-----------------|--------|
| `seomachine` | Keyword research, rankings, analytics | DataForSEO, GA4, GSC | ✅ Active |
| `webflow-publish` | Publish articles to CMS | Webflow API | ✅ Active |
| `hubspot-email-draft` | Newsletter to HubSpot | HubSpot API | ✅ Active |
| `rss-curation` | 64 feeds → Slack curation | RSS, Slack | ✅ Active |
| `youtube-downloader` | Download transcripts | YouTube, yt-dlp | ✅ Active |
| `nano-banana-image-generator` | AI image generation | Gemini API | ✅ Active |

### Utility Skills
| Skill | Purpose | Status |
|-------|---------|--------|
| `archive-suggest` | Daily suggestions from archive | ✅ Active |
| `work-summary` | Git → Slack updates | ✅ Active |
| `outreach-email-draft` | Post-publish nearbound emails | ✅ Active |
| `verified-review` | Curriculum/tool reviews | ✅ Active |
| `day-in-the-life` | Family profile posts | ✅ Active |
| `x-article-converter` | Blog → X Article with handles | ✅ Active |

### Meta/System Skills (Not Content Production)
| Skill | Purpose | Status |
|-------|---------|--------|
| `skill-creator` | Guide for creating new skills | ✅ Active |
| `manage-skills` | Maintain existing skills | ✅ Active |
| `create-interface` | Render HTML interfaces | ✅ Active |
| `daily-notes` | Personal daily notes | ✅ Active |
| `todos` | Task management via API | ✅ Active |
| `screenshots` | Screenshot utilities | ✅ Active |

### Orphan Skills (Need Review)
| Skill | Issue | Recommendation |
|-------|-------|----------------|
| `podcast-blog-post-creator` | Empty - no SKILL.md | Delete or implement |
| `opened-daily-style` | Unclear purpose, possibly redundant | Audit vs opened-identity |

---

## External System Integrations

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION MAP                                           │
│                                                                                  │
│   INBOUND (Data into Vault)                                                     │
│   ─────────────────────────                                                     │
│   DataForSEO ──────► seomachine ──────► keyword data, rankings                  │
│   GA4 ─────────────► seomachine ──────► traffic, pageviews                      │
│   GSC ─────────────► seomachine ──────► search queries, CTR                     │
│   YouTube ─────────► youtube-downloader ► transcripts                           │
│   RSS (64 feeds) ──► rss-curation ────► curated articles                        │
│   Webflow ─────────► sync script ─────► Master Content Index                    │
│                                                                                  │
│   OUTBOUND (Vault to External)                                                  │
│   ───────────────────────────                                                   │
│   hubspot-email-draft ────► HubSpot ────► Newsletter sends                      │
│   webflow-publish ────────► Webflow ────► Blog posts                            │
│   schedule-approved ──────► Notion ─────► Status updates                        │
│   schedule-approved ──────► GetLate ────► 8 social platforms                    │
│   x-posting ──────────────► GetLate ────► X/Twitter                             │
│   slack-social-distribution► Slack ─────► #market-daily                         │
│   nano-banana ────────────► Gemini ─────► AI images                             │
│                                                                                  │
│   BI-DIRECTIONAL                                                                │
│   ──────────────                                                                │
│   Notion ◄────────► schedule-approved ◄─► Query + Update staging               │
│   Webflow ◄───────► sync + publish ◄────► Read index + Write posts             │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Which Skill For What?

| I want to... | Use this skill |
|--------------|----------------|
| Write a daily newsletter | `opened-daily-newsletter-writer` |
| Write the Friday digest | `opened-weekly-newsletter-writer` |
| Process a podcast episode | `podcast-production` |
| Create SEO content | `seo-content-production` → `open-education-hub-deep-dives` |
| Make social posts from content | `content-repurposer` → `text-content` |
| Post to Slack for review | `slack-social-distribution` |
| Schedule approved posts | `schedule-approved` |
| Create ad concepts | `meta-ads-creative` |
| Make short-form video | `short-form-video` → `video-caption-creation` |
| Get keyword data | `seomachine` |
| Publish to Webflow | `webflow-publish` |
| Generate images | `nano-banana-image-generator` |
| Check quality | `quality-loop` |
| Write one-liners | `dude-with-sign-writer` |

---

*Last Updated: 2026-01-30*
