---
name: seo-content-production
description: End-to-end workflow for creating SEO-optimized content from topic selection through publication. Combines keyword research, source compilation, OpenEd perspective integration, and quality control into a repeatable process.
---

# SEO Content Production

Complete workflow for creating SEO-optimized articles for the Open Education Hub. Takes a topic from initial research through publication-ready draft.

## When to Use This Skill

- Writing comparison articles ("X vs Y")
- Creating curriculum guides or method explainers
- Developing pillar content for SEO
- Any article targeting specific search keywords

## The Complete Workflow

```
TOPIC → RESEARCH → STRUCTURE → SOURCES → DRAFT → QUALITY → PUBLISH
  1        2          3          4        5        6         7
```

---

## Phase 1: Topic Selection & Validation

### For Comparison Articles

Research all permutations of relevant comparisons. Use DataForSEO API:

```bash
# Credentials in seomachine config
Login: cdeist@opened.co
Password: 22e9510f77b0d182
Base URL: https://api.dataforseo.com
```

**Validation criteria:**
- Search volume > 500/month
- Keyword difficulty < 30 (winnable)
- Topic aligns with OpenEd's expertise
- We have (or can create) proprietary perspective

### Comparison Keyword Matrix

For educational philosophy comparisons, research:
- Waldorf vs [all others]
- Montessori vs [all others]
- Classical vs [all others]
- Charlotte Mason vs [all others]
- Unschooling vs [all others]

**Key insight:** Montessori appears in every high-volume comparison. Build content hub around it.

---

## Phase 2: SEO Research

### Create Research Brief

For each target article, document:

1. **Primary keyword** - Main target (volume, KD, CPC)
2. **Secondary keywords** - Related terms to include
3. **Long-tail opportunities** - Lower volume, easier wins
4. **People Also Ask** - Questions to answer in FAQ
5. **Competitor analysis** - What's ranking, what's missing

### Research Brief Template

```markdown
# SEO Research Brief: [Topic]

## Target Keywords
| Keyword | Volume | KD | Intent |
|---------|--------|-----|--------|
| primary | X | X | X |

## People Also Ask
1. [Question 1]
2. [Question 2]

## Competitor Gaps
- What's missing from top-ranking content
- Unique angles we can take

## Validation
- [ ] Volume > 500/mo
- [ ] KD < 30
- [ ] OpenEd has unique perspective
```

Save to: `Studio/SEO Content Production/[Topic]/SEO_RESEARCH_BRIEF.md`

---

## Phase 3: Structure & Substantive Take

### Identify OpenEd's Unique Perspective

Before outlining, answer:

1. **What does OpenEd believe about this topic?**
   - Check `opened-identity` skill for core values
   - Reference `.claude/references/OpenEdBook/` for detailed positions

2. **What can we say that competitors can't?**
   - Proprietary data from families we serve
   - Staff expertise (Keri Mae on early childhood, etc.)
   - Podcast guest insights

3. **What's the "hidden thread"?**
   - What do most articles avoid or get wrong?
   - What would be genuinely useful that's missing?

### OpenEd Content Principles

From `opened-identity`:
- **Pro-child, not anti-school** - Describe, don't prescribe
- **Mix and match** - No single approach is "the answer"
- **Parents as designers** - Empower, don't lecture
- **Sarah is our reader** - Speak to her specific situation

### Outline Structure

```markdown
# Outline: [Title]

## Meta
- Primary KW: [keyword]
- Target length: [X] words
- Unique angle: [what makes this ours]

## Structure
1. Hook (not definition)
2. Quick comparison table (for skimmers)
3. [Method A] explained
4. [Method B] explained
5. Key differences (the meat)
6. What both get right
7. What to consider (practical guidance)
8. The OpenEd take (permission to mix)
9. FAQ (targets PAA)
10. Next steps (internal links)

## OpenEd Perspective
[What's our substantive take on this topic?]

## Quotes to Include
- [Source 1]: "[Quote]"
- [Source 2]: "[Quote]"
```

---

## Phase 4: Source Compilation

### Search Order (Priority)

1. **OpenEd Book** - `.claude/references/OpenEdBook/OpenEd book - 1-7-25.docx.md`
2. **Published Content** - `Published Content/` (podcasts, newsletters, blog posts)
3. **Podcast Transcripts** - Search for relevant guest expertise
4. **Staff Knowledge** - Who on the team has relevant experience?
5. **External Research** - Fill gaps with web research

### Source Search Commands

```bash
# Search published content for topic
grep -rli "waldorf\|montessori" "Published Content/" | head -20

# Search podcast transcripts
grep -rli "[topic]" "Published Content/Podcasts/"

# Check Master Content Index for tagged content
grep -B5 "Tags:.*[tag]" "Published Content/Master_Content_Index.md"
```

### Spawn Source Research Agent

For comprehensive source finding:

```
Task: Search for all OpenEd content related to [topic]

Look in:
1. Published Content/Blog Posts/
2. Published Content/Daily Newsletters/
3. Published Content/Podcasts/

For each relevant piece, extract:
- Title and URL
- Specific quotes that support our angle
- How it could be used (link, quote, reference)

Return ranked list of most useful sources.
```

### Source Compilation Template

```markdown
# Sources: [Topic]

## From OpenEd Book
[Relevant passages]

## From Published Content
### [Article Title]
**URL:** [url]
**Quote:** "[exact quote]"
**Use in:** [which section]

## From Podcasts
### Episode [X] - [Guest]
**Quote:** "[exact quote]"
**Context:** [why this matters]

## External Research Needed
- [Gap 1]
- [Gap 2]
```

Save to: `Studio/SEO Content Production/[Topic]/SOURCES.md`

---

## Phase 5: Draft

### Before Drafting

- [ ] Outline approved
- [ ] Sources compiled
- [ ] Unique angle identified
- [ ] Internal links planned

### Drafting Principles

1. **Hook first** - Start with curiosity, not definitions
2. **Table early** - Skimmers need quick comparison
3. **Quotes integrated** - Use proprietary sources naturally
4. **Links purposeful** - 5+ internal, 2-3 external
5. **Voice authentic** - Apply `ai-tells` and `ghostwriter` constraints

### Internal Linking Strategy

**Link FROM this article to:**
- Related deep dives (methodology articles)
- Practical guides (curriculum recommendations)
- Age-specific content (kindergarten, high school)
- The "What is Open Education?" foundational piece

**Update AFTER publishing:**
- Add links TO this article from related content
- Update Master Content Index

### Draft Template

```markdown
# Draft v[N]: [Title]

**Date:** [YYYY-MM-DD]
**Target:** ~[X] words
**Primary KW:** [keyword]

---

## META

**Title:** [Title] ([char count])
**Meta Description:** [155 chars]
**URL:** /blog/[slug]

---

## ARTICLE

[Full content]

---

## INTERNAL LINKS USED
- [Link 1] - [context]
- [Link 2] - [context]

## EXTERNAL LINKS USED
- [Link 1] - [authority signal]

## QUOTES USED
- [Source]: "[Quote]" - [location in article]
```

---

## Phase 6: Quality Control

### Run Quality Loop

Invoke `quality-loop` skill for 5-judge review:

| Judge | Type | Checks |
|-------|------|--------|
| Human Detector | BLOCKING | AI tells, correlative constructions |
| Accuracy Checker | BLOCKING | Facts verified against sources |
| OpenEd Voice | BLOCKING | Brand alignment, not preachy |
| Reader Advocate | BLOCKING | Engaging, logical flow |
| SEO Advisor | ADVISORY | Keywords, links, meta elements |

### Common Issues

**Human Detector failures:**
- Correlative constructions ("X isn't just Y - it's Z")
- Forbidden words (delve, comprehensive, crucial)
- Staccato patterns ("No fluff. No filler. Just results.")

**Reader Advocate failures:**
- Definition-first hooks
- Awkward transitions (especially in "permission" sections)
- Missing practical takeaways

---

## Phase 7: Visual Assets

### Required Assets

| Asset | Dimensions | Style | Tool |
|-------|------------|-------|------|
| Thumbnail | 16:9 | watercolor-line | nano-banana |
| Comparison infographic | 16:9 | watercolor-line | nano-banana |
| Social cards | 1:1, 4:5 | brand colors | nano-banana |

### Thumbnail Concepts for Comparisons

For "X vs Y" articles, effective concepts:
- Two hands offering different gifts
- Split path through two environments
- Same tree with different root systems
- Two doorways in an open field

---

## Phase 8: Publication

### Pre-Publish Checklist

- [ ] All 5 judges passed (or advisory noted)
- [ ] Thumbnail created and saved to project folder
- [ ] Meta elements finalized
- [ ] Internal links verified
- [ ] External links verified (not broken)

### Publish Workflow

1. **Webflow** - Use `webflow-publish` skill
2. **Newsletter** - Use `opened-daily-newsletter-writer` for Deep Dive Daily
3. **HubSpot** - Use `hubspot-email-draft` skill
4. **Social** - Use `newsletter-to-social` for derivative posts

### Post-Publish

1. Update articles that should link TO this piece
2. Add to Master Content Index (via Webflow sync)
3. Schedule social promotion

---

## Project Folder Structure

```
Studio/SEO Content Production/[Topic]/
├── PROJECT.md              # Main context, workflow status
├── SEO_RESEARCH_BRIEF.md   # Keywords, competition, validation
├── SOURCES.md              # Compiled proprietary sources
├── CONTENT_REFERENCES.md   # Quotes with citations
├── INTERNAL_LINKS.md       # Linking strategy
├── OUTLINE.md              # Approved structure
├── DRAFT_v1.md             # First draft
├── DRAFT_v2.md             # Post-quality-loop revision
├── thumbnail-final.png     # Header image
└── [other assets]
```

---

## Reference Documents

### OpenEd Perspective
- `.claude/skills/opened-identity/SKILL.md` - Core values and stance
- `.claude/references/OpenEdBook/` - Detailed positions
- `.claude/skills/opened-identity/references/strategic-narrative.md` - Paradigm shift framing

### Writing Quality
- `.claude/skills/ai-tells/SKILL.md` - Patterns to avoid
- `.claude/skills/ghostwriter/SKILL.md` - Authentic voice
- `.claude/skills/quality-loop/SKILL.md` - 5-judge system

### SEO Tools
- DataForSEO API (credentials in `.env`)
- Master Content Index (`Published Content/Master_Content_Index.md`)

---

## Quick Start

For a new SEO article:

```
1. Validate topic: Does it have volume? Can we win? Do we have perspective?

2. Create project folder: Studio/SEO Content Production/[Topic]/

3. Run research: Keywords, competition, PAA questions

4. Compile sources: OpenEd book → Published content → Podcasts → External

5. Get outline approved: Structure + unique angle + quotes planned

6. Draft with constraints: ai-tells + ghostwriter + internal links

7. Quality loop: 5 judges, fix blocking issues

8. Create visuals: Thumbnail via nano-banana

9. Publish: Webflow → Newsletter → Social
```

---

## Integration with Other Skills

| Phase | Skills Used |
|-------|-------------|
| Research | `seo-research` (DataForSEO) |
| Sources | Explore agents, content database grep |
| Perspective | `opened-identity` |
| Draft | `ghostwriter`, `ai-tells` |
| Quality | `quality-loop` |
| Visuals | `nano-banana-image-generator` |
| Publish | `webflow-publish`, `hubspot-email-draft` |
| Social | `newsletter-to-social`, `text-content` |

---

*Created: 2026-01-28*
*Based on: Waldorf vs Montessori production workflow*
