# Social Media

**Status:** Active
**Purpose:** Platform strategies, content formats, and production systems

---

## Quick Navigation

### Active Subprojects
- `Frictionless Content Engine/PROJECT.md` - Automated content production system
- `Platform Insights/` - Platform-specific strategies (7 platforms)
- `Format Notes/` - Video arsenal and format definitions
- `staging/` - Content awaiting scheduling

### Related Files in Studio/
- `../Social_Scheduling.md` - X post scheduling queue
- `staging/Content_Concepts.md` - Calibration examples with feedback (moved from X_Post_Batch_Review.md)
- `../Retargeting Strategy FY26-27/PROJECT.md` - Paid social

### Related Projects
- `../Nearbound Pipeline/PROJECT.md` - Rolodex for tagging
- `../Analytics & Attribution/PROJECT.md` - Tracking performance

---

## What We're Building

One master `social-content-creation` skill that:
1. Takes source content (article, podcast, newsletter, standalone idea)
2. Routes to format-specific references based on content type
3. Applies platform-specific heuristics
4. Can fan out to parallel sub-agents for batch production

---

## Skill Architecture (Target)

```
social-content-creation/
├── SKILL.md                      # Router + orchestration
└── references/
    ├── platforms/
    │   ├── linkedin.md           # Thought leadership, comment-to-get
    │   ├── x-twitter.md          # Retweet-worthy, "I wish I said that"
    │   ├── facebook.md           # Engagement bait, text-on-background
    │   ├── instagram.md          # Visual-first, Reels > static
    │   ├── tiktok.md             # Educational entertainment
    │   ├── youtube.md            # Shorts + community posts
    │   └── pinterest.md          # SEO-focused pins
    │
    ├── formats/
    │   ├── text-posts.md         # Framework fitting, post structures
    │   ├── one-liners.md         # Dude-with-sign patterns
    │   ├── video-clips.md        # Producible video arsenal
    │   ├── carousels.md          # Multi-slide (future: BannerBear)
    │   └── threads.md            # X threads, LinkedIn docs
    │
    └── methods/
        ├── post-structures.md    # 100+ templates (existing)
        ├── proliferation.md      # SCAMPER, Human Desires
        └── framework-fitting.md  # Core methodology
```

---

## Platform Heuristics to Define

For each platform, we need:

1. **Success Heuristic** - What makes content work here
2. **Optimal Formats** - What performs (length, media, etc.)
3. **Anti-Patterns** - What fails
4. **API Limitations** - What we can't do programmatically
5. **Examples** - Proven posts

### Quick Reference (Draft)

| Platform | Success Heuristic | Key Format |
|----------|-------------------|------------|
| **X/Twitter** | "I wish I said that" - retweet-worthy | Short, punchy, quotable |
| **LinkedIn** | Thought leadership, vulnerability wins | Long-form (200-500 words) |
| **Facebook** | Engagement bait, comments drive reach | Questions, text-on-background |
| **Instagram** | Visual-first, Reels > everything | Reels, then carousels |
| **TikTok** | Educational entertainment | Hook in 1 sec, text-on-video |
| **YouTube** | Shorts for reach, long for depth | Shorts repurposed from Reels |
| **Pinterest** | SEO, evergreen discovery | Pins linking to articles |

---

## Video Arsenal (What We Can Actually Produce)

### Tier 1: No Filming Required
- **Text on B-roll** - Stock footage + text overlays
- **Screenshot + voiceover** - Tweet screenshots, article highlights
- **Podcast clips** - Existing audio + captions + waveform
- **Greenscreen memes** - Ed the Horse reacting to content

### Tier 2: UGC/Mom Footage
- **Day-in-life snippets** - Families can film specific moments
- **Testimonial style** - Talking head responses
- **Product demos** - Using curriculum, apps

### Tier 3: Produced Content
- **Podcast video episodes** - Full production
- **Explainer videos** - Scripted + edited

---

## Content Being Consolidated

### From Studio/Social Media Transformation/
- `Workflows/automation-priorities.md` - Tier system for automation
- `Workflows/unified-taxonomy.md` - Classification system
- `Workflows/social-orchestration-map.md` - Architecture thinking
- `Content Formats/` - Notion exports (need to extract value, archive rest)

### From Studio/Social Media Engine/
- `PROJECT.md` - API integration, Get Late workflow (keep as separate project)
- This is about *distribution*, not *creation* - different concern

### From Studio/LinkedIn Content/
- Example LinkedIn posts - extract patterns, archive folder

### From Existing Skills/
- `linkedin-content/` - 6 framework categories, 118 templates
- `video-caption-creation/` - Triple Word Score, hook categories
- `dude-with-sign-writer/` - 12 one-liner patterns
- `social-content-creation/` - Framework fitting methodology

---

## Work Completed

### Platform Insights (Created)
- [x] `Platform Insights/linkedin.md` - 118 frameworks, comment-to-get strategy
- [x] `Platform Insights/x-twitter.md` - Retweet-worthy heuristic, reply game
- [x] `Platform Insights/facebook.md` - Question posts, engagement bait
- [x] `Platform Insights/instagram.md` - Reels priority, visual-first
- [x] `Platform Insights/tiktok.md` - Educational entertainment, no-face formats
- [x] `Platform Insights/youtube.md` - Shorts + long-form strategy
- [x] `Platform Insights/pinterest.md` - SEO gold mine

### Format Definitions (Created)
- [x] `Format Notes/video-arsenal.md` - Tier 1/2/3 producible formats

### Still Needed
- [ ] Text posts reference (consolidate post-structures)
- [ ] One-liners reference (absorb dude-with-sign)
- [ ] Carousels reference (document capability)
- [ ] Threads reference (X threads, LinkedIn docs)

---

## Decisions Needed

1. **Skill consolidation** - Merge linkedin-content, dude-with-sign into social-content-creation as references? Or keep as separate skills that get invoked?

2. **Video-caption-creation** - Keep separate (it's format-specific) or merge?

3. **Social Media Engine** - Keep as separate project (distribution) vs. merge (end-to-end)?

4. **Sub-agent pattern** - When processing source content, spawn parallel agents for each format/platform combo?

---

## Archive Plan

Once consolidated:
- `Studio/Social Media Transformation/` → Archive valuable docs, delete Notion cruft
- `Studio/LinkedIn Content/` → Extract examples, archive folder
- `Studio/Short-Form Video/` → Already empty, delete

---

*This is a working document. Update as decisions are made.*
