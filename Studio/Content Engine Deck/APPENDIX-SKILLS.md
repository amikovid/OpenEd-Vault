# Appendix: Complete Skills Catalog

Full documentation of all 25+ skills in the OpenEd content engine.

---

## Content Creation Skills

### text-content
**Purpose:** Create high-performing text posts for social media
**Templates:** 360+
**Platforms:** LinkedIn, X, Facebook, Instagram

Key features:
- Framework fitting methodology
- Platform-specific routing
- Progressive disclosure (load only relevant templates)
- SCAMPER proliferation for winning posts

### opened-daily-newsletter-writer
**Purpose:** Create Mon-Thu OpenEd Daily newsletters
**Format:** Thought-Trend-Tool (500-800 words)

Structure:
- 1 Thought (reflection/insight)
- 1 Trend (what's happening in education)
- 1 Tool (resource recommendation)

### opened-weekly-newsletter-writer
**Purpose:** Create Friday Weekly Digest
**Format:** Weekly roundup compilation

### open-education-hub-deep-dives
**Purpose:** Create SEO-optimized deep dive articles
**Output:** 2000-3000 word authoritative content

Features:
- Proprietary OpenEd insights (podcasts, Slack, newsletters)
- SEO-structured headers
- 3-5+ internal links per article
- Quality loop integration

### ghostwriter
**Purpose:** Transform AI output into authentic prose
**Focus:** Anti-AI pattern detection

Checks for:
- Correlative constructions
- Overused AI words
- Staccato patterns
- Fake enthusiasm

### hook-and-headline-writing
**Purpose:** Create attention-grabbing hooks and headlines
**Methods:** 15 formulas, 4 U's test

The 4 U's:
- Useful
- Ultra-specific
- Urgent
- Unique

### quality-loop
**Purpose:** Iterative drafting with quality gates
**Structure:** 5 judge personas evaluate each draft

Judges:
1. Content strategist
2. Voice guardian
3. SEO specialist
4. Reader advocate
5. Editor-in-chief

---

## Visual Content Skills

### image-prompt-generator
**Purpose:** Generate AI images using Gemini API
**Styles:** 4 predefined (watercolor-line, editorial, minimalist-ink, newyorker-cartoon)

Workflow:
1. Brainstorm 4-6 concepts
2. User selects direction
3. Optimize prompt
4. Style variations
5. Generate via API
6. Iterate

### video-caption-creation
**Purpose:** Create video hooks and captions
**System:** Triple Word Score optimization

Categories:
- Pattern interrupt hooks
- Curiosity gap hooks
- Controversy hooks
- Story hooks

### short-form-video
**Purpose:** Create Reels/TikTok/Shorts content
**Method:** Sponge-then-sharpen

Philosophy:
- Sponge phase: Prototype fast, publish everything
- Sharpen phase: Triple down on what works

### youtube-clip-extractor
**Purpose:** Identify and extract podcast clips
**Output:** Platform-optimized clips with on-screen text

### youtube-title-creator
**Purpose:** Generate high-CTR YouTube titles
**Formulas:** 119 proven patterns

### youtube-downloader
**Purpose:** Download YouTube transcripts
**Use:** Source material for content creation

---

## Podcast Skills

### podcast-production
**Purpose:** Complete episode workflow
**System:** 4 checkpoints to publication

Checkpoints:
1. Transcript analysis, key moments
2. Blog outline approval
3. Social package draft
4. Final asset delivery

### cold-open-creator
**Purpose:** Create 25-35 second podcast hooks
**Method:** Drop listeners into specific moment

Techniques:
- Character-driven narrative
- Rearrangement (best moment first)
- Thematic encapsulation

### transcript-polisher
**Purpose:** Transform raw transcripts
**Output:** Readable documents preserving voice

Removes:
- Filler words
- False starts
- Excessive qualifiers

---

## SEO & Research Skills

### seo-research
**Purpose:** Keyword research and analysis
**API:** DataForSEO

Commands:
- Quick wins (low difficulty, high volume)
- Content gaps (competitor analysis)
- Full keyword exploration

### seo-content-writer
**Purpose:** SEO-optimized article creation
**Integration:** Works with seo-research output

---

## Advertising Skills

### meta-ads-creative
**Purpose:** Facebook/Instagram ad creative
**Framework:** 6 Elements

Elements:
1. Hook (first 3 seconds)
2. Problem (agitation)
3. Solution (your offer)
4. Social proof
5. Call to action
6. Visual style

### x-article-converter
**Purpose:** Convert blog posts to X articles
**Features:** Handle insertion, posting strategy

---

## Voice & Identity Skills

### opened-identity
**Purpose:** OpenEd brand voice and values
**Content:** Messaging framework, audience understanding

### guidelines-brand
**Purpose:** Visual brand identity
**Specs:** Colors, typography, spacing

### ai-tells
**Purpose:** Patterns that reveal AI writing
**Use:** Apply constraints to all writing tasks

Categories:
- Word tells (delve, comprehensive)
- Phrase tells (The best part...)
- Structure tells (staccato patterns)

---

## Utility Skills

### transcript-polisher
**Purpose:** Clean up spoken content
**Preserves:** Authentic voice, key insights

### skill-creator
**Purpose:** Create new skills
**Template:** Frontmatter + methodology + references

### gemini-context
**Purpose:** Delegate to Gemini's 1M token context
**Use:** Large-scale reading, synthesis tasks

---

## Notion Integration Skills

### notion-meeting-intelligence
**Purpose:** Meeting preparation
**Output:** Internal pre-read + external agenda

### notion-research-documentation
**Purpose:** Synthesize Notion workspace content
**Output:** Research documentation with citations

### notion-knowledge-capture
**Purpose:** Transform conversations to Notion pages
**Output:** Structured documentation

### notion-spec-to-implementation
**Purpose:** Convert specs to tasks
**Output:** Implementation plans

---

## Deprecated Skills (Archived)

Consolidated into `text-content`:
- `social-content-creation`
- `linkedin-content`
- `dude-with-sign-writer`

---

## Skill Architecture

### File Structure

```
skill-name/
├── SKILL.md              # Core file (frontmatter + methodology)
└── references/           # Supporting documents
    ├── templates/        # Reusable patterns
    ├── examples/         # Sample outputs
    └── [topic]/          # Domain-specific
```

### Frontmatter Format

```yaml
---
name: skill-name
description: Brief description for skill discovery
---
```

### Loading Behavior

1. At startup: Only name/description loads
2. When invoked: Full SKILL.md loads
3. As needed: References load progressively

---

*25+ skills documented - Updated 2026-01-13*
