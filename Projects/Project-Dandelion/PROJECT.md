# Project Dandelion

> *"The founders and creators who will define the next generation are those who understand the invisible physics of how groups of people decide to trust something new."*
> — Lewis Kallow

**Status:** Active
**Created:** 2026-01-27
**Updated:** 2026-01-29
**Operators:** Charlie Deist, Elijah

---

## What This Is

Project Dandelion is OpenEd's paid acquisition and content format testing initiative. The goal is to build replicable content systems that:

1. Create low-friction, high-volume content formats
2. Find what spreads and why (format playbook)
3. Drive top-of-funnel traffic that converts via Curriculove
4. Document everything as repeatable workflows

**Why "Dandelion"?** Content should spread like dandelion seeds - native to the environment, designed to be carried by others, resilient across platforms.

---

## The Thesis

From Lewis Kallow's research on complex contagions:

**Simple contagions** spread with single exposure (viral videos, memes). Project Dandelion focuses here:
- Paid ads, short-form video, shareable templates
- Volume, reach, top-of-funnel awareness
- Formats that can run independently

**Complex contagions** require multiple exposures from trusted sources (behavior change, product adoption). Curriculove focuses here:
- Trust-based, community-embedded
- Influencers and social dandelions in homeschool communities
- Multiple touchpoints from trusted sources

**The connection:** Simple contagion content drives traffic → Curriculove captures and converts.

---

## Three Workstreams

### 1. Meta Ads (Retargeting + Prospecting)

**Goal:** Revive and optimize Meta advertising with evidence-based creative.

**Key insight from performance analysis:** Lo-fi, native-feeling formats dramatically outperform polished designs. Notes App format delivers $5.33 CPA at volume. Same copy with "corporate" styling performed 28x worse.

**Related projects:**
- `Retargeting Strategy FY26-27/` - Campaign structure, Pillar 1/2/3 audiences
- `Studio/Meta Ads/` - 100 ad concepts (V1 + V2), creative skill

**Current state:**
- Performance analysis complete (see `research/meta-ads-performance-analysis-2026-01-28.md`)
- Improved Pillar 1 concepts drafted with "evidence over accusation" approach
- Pillar 1 launch: Feb 16

### 2. Short-Form Video

**Goal:** Test native-feeling video formats tied to curriculum content.

**Format experiments:**
- Talking head with captions
- B-roll with voiceover
- Screen recordings (Curriculove walkthrough)
- Duet/stitch with homeschool creators
- Trending sounds + homeschool twist

**Related skills:**
- `short-form-video` - Production methodology
- `video-caption-creation` - Hook writing, captions
- `youtube-clip-extractor` - Podcast → clips

### 3. Format Playbook

**Goal:** Document what works so formats can be repeated.

**Output:** `playbook/` folder with:
- Format templates
- Performance benchmarks
- "What works / what doesn't" learnings
- Workflows others can run

---

## Active Sprint

**Sprint 01:** Jan 27 - Feb 7, 2026
**Operator:** Elijah
**Details:** See [SPRINT-01.md](./SPRINT-01.md)

### Sprint 01 Goals

| Milestone | Target | Status |
|-----------|--------|--------|
| Audit existing ads | Jan 29 | ✅ Complete |
| 3 refreshed concepts | Jan 31 | 🔄 In Progress |
| 1 short-form video | Jan 31 | ⏳ |
| YouTube Ads research | Jan 31 | ⏳ |
| 5 ads live in Meta | Feb 7 | ⏳ |
| Format playbook v1 | Feb 7 | ⏳ |

---

## Key Research Findings

### What Works (from performance analysis)

| Format | CPA | Volume | Notes |
|--------|-----|--------|-------|
| Notes App (Notes3) | $5.33 | 747 apps | Best high-volume performer |
| MG2 (video + text overlay) | $4.25 | 142 apps | Lowest CPA |
| Text-Heavy V1 (black/white) | $5.82 | 1,278 apps | Highest volume |
| TikTok Response (AsADad) | $5.10 | 38 apps | Skeptic-turned-believer angle |
| Testimonial compilations | $5.85 | 78 apps | Real parent photos + outcomes |

### What Fails

| Format | CPA | Why |
|--------|-----|-----|
| SecretWeapon narrative | $220 | Too long, poetic, abstract |
| Text-Heavy V3 (styled) | $122 | Same copy as V1 but with highlights/underlines - looks like corporate ad |

**Key lesson:** The exact same copy performed 28x worse with different visual treatment. Lo-fi wins.

### Creative Patterns

**Do:**
- Question hooks addressing barriers
- Pattern interrupts ("stop scrolling")
- Specific numbers (110+ resources, 17,000+ families)
- Transformation stories (struggling → thriving)
- Low-friction CTAs (free, easy, newsletter)

**Don't:**
- Long narrative copy
- Excessive visual styling (highlights, underlines)
- Abstract/poetic messaging
- Accusatory retargeting ("finish what you started")

---

## Folder Structure

```
Project-Dandelion/
├── PROJECT.md           # This file
├── SPRINT-01.md         # Current sprint plan
├── research/            # Analysis, findings, source material
│   ├── meta-ads-performance-analysis-2026-01-28.md
│   ├── retargeting-ad-concepts-2026-01-28.md
│   ├── parent-testimonial-content-2026-01-27.md
│   ├── tool-discovery-2026-01-27.md
│   └── how-to-scale-your-newsletter-nathan-may.md
└── playbook/            # (To create) Replicable format templates
```

---

## Related Projects

### Paid Acquisition

| Project | Location | Relationship |
|---------|----------|--------------|
| **Retargeting Strategy** | `Projects/Retargeting Strategy FY26-27/` | Campaign structure, Pillar 1/2/3 |
| **Meta Ads** | `Studio/Meta Ads/` | 100 ad concepts, creative skill |
| **Analytics & Attribution** | `Studio/Analytics & Attribution/` | Tracking, HubSpot, data |

### Content Sources

| Project | Location | Use |
|---------|----------|-----|
| **Curriculove** | `Projects/Lead Magnet Project/curriculove/` | Lead capture, quiz content |
| **Podcast Studio** | `Studio/Podcast Studio/` | Clips, testimonials |
| **OpenEd Daily** | `Studio/OpenEd Daily Studio/` | Newsletter → social |
| **Tools Directory** | `Projects/Tools Directory/` | Curriculum content hooks |

### Skills

| Skill | Use |
|-------|-----|
| `meta-ads-creative` | Ad concept generation |
| `short-form-video` | Video production |
| `video-caption-creation` | Hooks, captions |
| `dude-with-sign-writer` | One-liners for text-only ads |
| `newsletter-to-social` | Content atomization |

---

## Success Metrics

### Sprint-Level (2 weeks)
- Ads live and running
- Videos published
- Formats documented

### Quarter-Level (Q3)
- Cost per application from paid channels (target: <$7)
- Organic follower growth on IG/TikTok
- Format playbook complete
- YouTube ads: test or no-test decision made

---

## Operators

**Charlie Deist** - Strategy, oversight, research
**Elijah** - Execution, creative, experimentation

---

## Philosophy

- **Ship fast** - Publish and learn, don't overthink
- **Measure everything** - If we can't track it, we can't improve it
- **Document learnings** - Every flop is data for the playbook
- **Evidence over accusation** - Show outcomes, don't pressure
- **Lo-fi wins** - Native-feeling content outperforms polished

---

*Last Updated: 2026-01-29*
