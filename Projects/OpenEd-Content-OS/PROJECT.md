# OpenEd Content OS

**A frictionless system of pathways from concept to publication.**

The more often we tread these pathways, the better they get.

**Status:** Active
**Updated:** 2026-01-29

---

## What This Is

The Content OS is both a reference document and an operational framework. It defines:

1. **Pathways** - Standard routes from source content to published assets
2. **Auto-invoke triggers** - When skills should activate automatically during workflows
3. **Format inventory** - All defined output formats by platform
4. **The repurposing agent** - Specialized framework fitting for multi-platform distribution

**Philosophy:** Skills are modular. Pathways chain them together. The OS knows when to invoke what.

---

## Three Pathway Types

### 1. Hub-and-Spoke (One → Many)
Transform one piece of hub content into multiple derivative assets.

| Hub | Skill Chain | Outputs |
|-----|-------------|---------|
| **Podcast** | podcast-production → video-caption-creation → text-content | 12-25 assets |
| **Newsletter** | opened-daily-newsletter-writer → newsletter-to-social | 6-9 posts |
| **Deep Dive** | seo-content-production → newsletter-to-social | 10-15 posts |

### 2. Transformation (Format → Format)
Convert one format into another.

| Source | Target | Skills Involved |
|--------|--------|-----------------|
| Article | Carousel | text-content + nano-banana |
| Newsletter segment | Quote card | dude-with-sign-writer + nano-banana |
| Podcast clip | Reel with hooks | video-caption-creation |
| Infographic (16:9) | Instagram (4:5) | nano-banana (re-input + resize) |

### 3. Repurposing (Archive → Fresh)
Resurface evergreen content with new framing.

| Source | Process | Output |
|--------|---------|--------|
| Archive article | archive-suggest → text-content | Platform-optimized post |
| Old podcast | youtube-clip-extractor | New clips with fresh hooks |
| Newsletter archive | newsletter-to-social | Social posts |

---

## Auto-Invoke Triggers

**When working on content, these skills should activate automatically at specific stages.**

### SEO Article Production
```
Phase 1: Topic Selection
  └─ AUTO: seomachine (keyword validation)

Phase 2: Research
  └─ AUTO: opened-identity (brand positioning check)

Phase 3: Outline
  └─ AUTO: open-education-hub-deep-dives (structure template)

Phase 5: Draft Complete
  └─ AUTO: quality-loop (5-judge gate)
  └─ AUTO: ai-tells (hard blocks check)

Phase 6: Pre-Publish
  └─ AUTO: article-titles (10+ options, 10 Commandments scoring)
  └─ AUTO: nano-banana (thumbnail generation)

Phase 7: Post-Publish
  └─ AUTO: newsletter-to-social (extract social posts)
```

### Newsletter Production
```
Phase 1: Source Curation
  └─ AUTO: opened-identity (brand alignment)

Phase 2: Angle Development
  └─ AUTO: newsletter-subject-lines (10+ options)

Phase 3: Draft
  └─ AUTO: ai-tells + ghostwriter (voice constraints)

Phase 4: Post-Send
  └─ AUTO: newsletter-to-social (6-9 platform posts)
```

### Podcast Production
```
Checkpoint 1: Analysis
  └─ AUTO: transcript-polisher (clean transcript)

Checkpoint 2: Clips
  └─ AUTO: cold-open-creator + video-caption-creation

Checkpoint 3: YouTube
  └─ AUTO: youtube-title-creator

Checkpoint 4: Blog
  └─ AUTO: podcast-blog-post-creator
  └─ AUTO: newsletter-to-social (derivative posts)
```

---

## The Repurposing Agent Concept

**A specialized agent for framework fitting across platforms.**

### Core Competencies

1. **Brand Context**
   - OpenEd is a company, not an individual
   - Brand account voice (not personal voice)
   - 125,000+ families, 9 states, tuition-free resources

2. **Source Context Awareness**
   - Podcast guest? → Third person, make THEM look good, tag them
   - Newsletter? → First person plural ("we found...")
   - Archive content? → Fresh angle, current relevance

3. **Platform Optimization**
   - LinkedIn: Authority templates, 200-500 words, 3-5 hashtags
   - X: 70-100 chars, 1-2 hashtags max, punchy
   - Instagram: Visual-first, 5-10 hashtags, carousel-friendly
   - Facebook: Questions, no external links, no hashtags
   - TikTok/Reels: Hook in 2 seconds, on-screen text 2-4 words

4. **Nearbound Integration**
   - Check nearbound index for mentioned people
   - Add @handles for tagged platforms
   - Note new profiles needed if mentioned 2+ times

### Agent Workflow
```
INPUT: Source content + context (podcast guest, newsletter, archive)
    │
    ├─→ Load: opened-identity + ai-tells (always)
    ├─→ Check: nearbound/people/ for @handles
    │
    ├─→ Extract standalone snippets by type:
    │   • hot_take → Contrarian templates
    │   • stat → Authority templates
    │   • how_to → List templates
    │   • quote → Quote + commentary
    │   • story → Transformation templates
    │
    ├─→ Route to platforms with appropriate templates
    │
    └─→ OUTPUT: 2-3 drafts per platform, tagged and optimized
```

### Dimension Handling (nano-banana integration)
```
Article thumbnail (16:9)
    │
    ├─→ Re-input to nano-banana
    ├─→ Specify: "Adapt this infographic to Instagram (4:5)"
    └─→ OUTPUT: Instagram-optimized version

Same process for:
- 16:9 → 1:1 (LinkedIn, X)
- 16:9 → 9:16 (Stories, Reels cover)
```

---

## Format Inventory

### Video Formats (20+ named)

**Tier 1: No Filming (2-5 min production)**
- Pointing Format (point to tablet, hold 5-8 sec)
- Fridge Magnet / Tablet Swivel
- iPhone Notes Style
- Caption-Heavy Loops

**Tier 2: Light Production (5-15 min)**
- Ed the Horse (character)
- Is It Reimbursable? (item reveal)
- Hot Takes + Easel
- Greenscreen Commentary

**Tier 3: Produced (30+ min)**
- Text + B-Roll (Pinterest style)
- Hidden Genius Stories
- Stats Infographics
- New Yorker Cartoons

### Text Post Formats

**LinkedIn (118 templates, 6 categories)**
- Engagement (16): Polls, Agree/Disagree, Fill-blank
- Story (24): Before/After, Transformation, Values
- List (17): Tips, DOs/DONTs, Frameworks
- Contrarian (20): Hot takes, Call BS, Rants
- Authority (26): Quotes, How-to, Pro tips
- Community (15): Shoutouts, Introductions

**X/Twitter**
- One-liners (70-100 chars)
- Commentary (stat + interpretation)
- Threads (3-7 tweets)
- Pattern recognition

**Instagram**
- Reel captions (1-2 sentences)
- Carousel captions ("Swipe for...")
- Quote cards
- Micro-stories

**Facebook**
- Question posts (10-20 words)
- Fill-in-the-blank
- Text-on-background
- Validation posts

### One-Liner Patterns (Universal - 12 patterns)
1. Normalize - "Normalize [behavior]"
2. Stop + Complaint - "Stop [annoying thing]"
3. Everyday Observations
4. Relationship Rules
5. Pop Culture Commentary
6. Mock Instructions
7. Wordplay
8. Existential Questions
9. Aspirational
10. Calendar Commentary
11. Everyday Struggles
12. Values

---

## Quality Gates

### Full 5-Judge (Articles, Newsletters, Deep Dives)

| Judge | Focus | Blocking? |
|-------|-------|-----------|
| Human Detector | AI tells, correlatives | YES |
| Accuracy Checker | Facts vs sources | YES |
| OpenEd Voice | Brand alignment | YES |
| Reader Advocate | Flow, engagement | YES |
| SEO Advisor | Keywords, links | NO |

### Lite 3-Judge (Social Posts)

| Judge | Focus | Blocking? |
|-------|-------|-----------|
| AI-Tell | Hard blocks only | YES |
| Voice | Brand alignment | YES |
| Platform | Platform optimization | NO |

---

## Skill Dependencies (Quick Reference)

### Always Load (Any Content)
- `opened-identity` - Brand voice
- `ai-tells` - Hard blocks
- CLAUDE.md Writing Rules

### By Content Type

| Creating | Load These |
|----------|------------|
| Newsletter | opened-daily-newsletter-writer, newsletter-subject-lines, ghostwriter |
| Podcast assets | podcast-production, cold-open-creator, video-caption-creation |
| SEO article | seo-content-production, article-titles, quality-loop |
| Social posts | text-content, newsletter-to-social |
| Video | short-form-video, video-caption-creation |
| Images | nano-banana-image-generator |
| Meta ads | meta-ads-creative, dude-with-sign-writer |

---

## File Locations

| Need | Location |
|------|----------|
| All skills | `.claude/skills/` (45+) |
| Template index | `.claude/skills/text-content/references/templates/TEMPLATE_INDEX.md` |
| LinkedIn templates | `.claude/skills/text-content/references/linkedin/` |
| Platform guides | `.claude/skills/text-content/references/platforms/` |
| Format inventory | `Studio/Social Media/FORMAT_INVENTORY.md` |
| Master content index | `.claude/references/Master_Content_Index.md` |
| Nearbound profiles | `Studio/Nearbound Pipeline/people/` |

---

## Proactive Behaviors

**The Content OS should encourage:**

1. **Auto-suggest spokes** - After completing any hub content, proactively offer derivative formats
2. **Skill chaining** - Automatically invoke the next skill in a pathway
3. **Format suggestions** - When source content is identified, suggest best-fit formats
4. **Nearbound checks** - Always check for taggable people
5. **Quality gates** - Never skip quality-loop for publishable content
6. **Archive mining** - Periodically suggest repurposing opportunities

---

## Open Architectural Questions

1. **Agent Orchestration** - How does an orchestrator spawn specialists? Currently no formalized trigger mechanism.

2. **Webflow Publishing** - No automated path from vault markdown to published blog posts.

3. **GetLate Integration** - x-posting skill exists but batch scheduling untested at scale.

---

## Remaining Gaps

- [ ] Add dimension handling to nano-banana skill (16:9 → 4:5, 1:1, 9:16)
- [ ] Define carousel production workflow
- [ ] Define comic/infographic transformation pathways
- [ ] Instagram Stories workflow

---

## Related Files

| File | Purpose |
|------|---------|
| `SKILL_ARCHITECTURE_MAP.md` | Visual diagrams of all skill chains |
| `EXECUTION.md` (root) | Weekly task tracking |
| `NOW.md` (root) | Current state |

---

*The Content OS grows through use. Every pathway we tread improves it.*
