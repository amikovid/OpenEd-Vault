# Skill Architecture Draft

## The Dependency Problem

Content creation has three layers, each with different scopes:

```
┌─────────────────────────────────────────────────────────┐
│  SOURCE TYPE                                            │
│  (podcast, article, newsletter, standalone idea)        │
│  → Determines extraction method                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  FORMAT                                                 │
│  (short-form video, text post, carousel, one-liner)    │
│  → Determines structure, hooks, visual treatment       │
│  → MOSTLY PLATFORM-AGNOSTIC                            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  PLATFORM ADAPTATION                                    │
│  (X, LinkedIn, Facebook, Instagram, TikTok, etc.)      │
│  → Determines captions, hashtags, voice, limits        │
│  → VARIES PER PLATFORM                                 │
└─────────────────────────────────────────────────────────┘
```

## The Overlap Reality

### Short-Form Video (Reels/TikTok/Shorts)
These are essentially THE SAME FORMAT with minor platform tweaks:
- **Same:** On-screen text, hook timing, video structure, Triple Word Score
- **Different:** Caption length, hashtag count, trending audio availability

### Text Posts (X/LinkedIn/Facebook)
These DIVERGE significantly:
- **X:** Short, punchy, retweet-worthy
- **LinkedIn:** Long-form, thought leadership, vulnerability
- **Facebook:** Questions, engagement bait, informal

### One-Liners
Work ACROSS formats:
- Text-on-background (FB, Instagram static)
- On-screen text for video
- Tweet/X post
- Easel reveal (video format)

---

## Proposed Skill Structure

### Option C Refined: Format-Based Skills with Platform References

```
social-content-creation/           # ROUTER SKILL
├── SKILL.md                       # Routing logic only
└── references/
    └── routing-guide.md           # When to use which skill

short-form-video/                  # FORMAT SKILL
├── SKILL.md                       # Video creation methodology
└── references/
    ├── hooks.md                   # On-screen text patterns
    ├── triple-word-score.md       # Algorithm optimization
    ├── video-arsenal.md           # What we can produce
    └── platforms/
        ├── reels-tiktok-shorts.md # Combined (they're the same)
        └── x-video.md             # X-specific video

text-content/                      # FORMAT SKILL
├── SKILL.md                       # Framework fitting methodology
└── references/
    ├── post-structures.md         # 100+ templates
    ├── one-liners.md              # Dude-with-sign patterns
    ├── proliferation.md           # SCAMPER, Human Desires
    └── platforms/
        ├── linkedin.md            # Long-form, thought leadership
        ├── x-twitter.md           # Short, punchy
        └── facebook.md            # Engagement bait

carousel-content/                  # FORMAT SKILL (future)
├── SKILL.md                       # Carousel methodology
└── references/
    ├── slide-patterns.md          # Common structures
    └── platforms/
        ├── linkedin.md            # PDF documents
        └── instagram.md           # Swipeable carousels
```

---

## Router Skill Logic (social-content-creation)

The router asks:

### 1. What's your source?
- Podcast clip → Suggest: short-form-video + text-content for captions
- Article/Newsletter → Suggest: text-content (multi-platform) + short-form-video clips
- Standalone idea → Ask: What format?

### 2. What format(s)?
- Short-form video → Load short-form-video skill
- Text post → Load text-content skill
- Carousel → Load carousel-content skill
- Multiple → Can spawn parallel sub-agents

### 3. Which platforms?
- Pass to format skill, which loads relevant platform reference

---

## Sub-Agent Pattern for Batch Production

When processing a podcast episode:

```
User: "Repurpose this podcast for social"

Router (social-content-creation):
├── Agent 1: short-form-video
│   ├── Select 3-5 clip moments
│   ├── Generate on-screen text options
│   └── Create platform captions (Reels/TikTok/Shorts + X)
│
├── Agent 2: text-content → LinkedIn
│   ├── Extract key insights
│   ├── Match to LinkedIn frameworks
│   └── Generate 2-3 post options
│
├── Agent 3: text-content → X
│   ├── Extract quotable moments
│   ├── Generate tweet options
│   └── Suggest thread structure
│
└── Agent 4: text-content → Facebook
    ├── Extract relatable moments
    ├── Generate question posts
    └── Create engagement hooks
```

---

## What Each Skill Needs to Know

### short-form-video
- Video arsenal (what we can produce)
- Hook patterns (polarizing, counter-intuitive, etc.)
- Triple Word Score optimization
- Platform specs (minimal - they're nearly identical)

### text-content
- Framework fitting methodology
- Post structures (100+ templates)
- One-liner patterns
- Platform-specific voice and limits
- Proliferation methods (SCAMPER, Human Desires)

### carousel-content (future)
- Slide structure patterns
- Visual hierarchy
- Platform specs (LinkedIn PDF vs Instagram swipe)
- BannerBear integration (when ready)

---

## Context Efficiency

This structure means:
- If you just need a tweet, load only: text-content + x-twitter.md
- If you need a Reel, load only: short-form-video + reels-tiktok-shorts.md
- If you're doing full podcast repurposing, spawn agents with minimal overlap

The router skill stays lightweight - just routing logic, no content templates.

---

## Questions to Resolve

1. **Should one-liners be their own skill?** They cross formats (text, video overlay, easel reveal). Could be a reference loaded by both text-content and short-form-video.

2. **LinkedIn as special case?** It's so different from other text platforms (long-form, 118 frameworks) - does it warrant its own skill?

3. **Podcast-specific skill?** The podcast → social pipeline is common enough it might warrant its own orchestration skill that invokes the others.

---

*This is a working architecture draft. Refine based on actual usage patterns.*
