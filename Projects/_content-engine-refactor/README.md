# Content Engine Q3 Refactor

**Started:** 2026-01-23
**Goal:** Map and solidify the low-friction content engine with continual learning via skill updates.

## Core Technique: Framework Fitting

Extract standalone snippets from hub content → Match to proven formats → Use sub-agents per platform.

**North Star:** Newsletter subscriber growth - all content ladders up to subs.

## Project Structure

```
_content-engine-refactor/
├── README.md                          # This file
├── CHECKLIST.md                       # Implementation tracking
├── PLAN.md                            # Full strategy document
│
├── skill-drafts/                      # New skills to create
│   ├── newsletter-to-social/          # Newsletter → social router
│   ├── content-router/                # Meta-routing skill (optional)
│   └── curate-to-content/             # Curation promotion skill
│
├── template-drafts/                   # New template files
│   └── sub-agent-prompts/             # Platform sub-agent prompts
│       ├── linkedin-agent.md
│       ├── x-agent.md
│       ├── instagram-agent.md
│       └── facebook-agent.md
│
├── updates/                           # Changes to existing skills
├── nearbound/                         # Nearbound quick index work
├── analytics/                         # Analytics integration
└── curation/                          # Curation pipeline (separate plan)
```

## Phases

| Phase | Status | Description |
|-------|--------|-------------|
| 0 | ✅ Complete | Archive old skills |
| 1 | ✅ Complete | Framework fitting infrastructure |
| 2 | ✅ Complete | Quality loop universalization |
| 3 | ✅ Complete | Instagram coverage |
| 4 | ✅ Complete | Archive repurposing agent |
| 5 | ✅ Complete | Nearbound quick index |
| 6 | ✅ Complete | SEO report refocus |
| 7 | ✅ Complete | Curation pipeline |
| 8 | ✅ Complete | CLAUDE.md restructure |

**Initial implementation complete: 2026-01-23**

---

## Phase 9: Skills Audit & Refactoring (In Progress)

**Status:** Audits complete, refactoring in progress

### Audit Summary (All 5 Batches Complete)

| Batch | Skills | Key Findings |
|-------|--------|--------------|
| 1: Core Content | text-content, opened-daily-newsletter-writer, quality-loop, podcast-production, newsletter-to-social | 2 bloated (newsletter 2,852w, podcast 2,701w), quality-loop renamed |
| 2: Social/Video | short-form-video, video-caption-creation, x-posting, x-article-converter, meta-ads-creative | meta-ads bloated (2,880w), x-posting exemplary |
| 3: Writing/Voice | ghostwriter, human-writing, ai-tells, hook-and-headline-writing, opened-identity | ghostwriter (3,302w) and hook-writing (3,542w) bloated, duplicate refs |
| 4: Brand/SEO | seo-research, open-education-hub-deep-dives, opened-weekly-newsletter-writer, transcript-polisher, cold-open-creator | cold-open (2,517w) and weekly (2,194w) over target |
| 5: Utility | image-prompt-generator, skill-creator, gemini-writer, youtube-title-creator, youtube-clip-extractor | youtube-title has 6 broken refs, gemini-writer exemplary (911w) |

### Skills Over 2,000 Word Target (Need Refactoring)

| Skill | Words | Priority |
|-------|-------|----------|
| hook-and-headline-writing | 3,542 | High |
| ghostwriter | 3,302 | High |
| meta-ads-creative | 2,880 | Medium |
| opened-daily-newsletter-writer | 2,852 | High (in progress) |
| podcast-production | 2,701 | Medium |
| cold-open-creator | 2,517 | Medium |
| youtube-clip-extractor | 2,252 | Low |
| youtube-title-creator | 2,216 | Low |
| opened-weekly-newsletter-writer | 2,194 | Low |

### Completed Actions
- [x] Renamed `quality-loop/skill.md` → `SKILL.md`
- [x] Nearbound enrichment: 8 profiles updated with social handles
- [x] Identified `human-writing copy` duplicate folder for deletion

### In Progress
- [x] Refactoring `opened-daily-newsletter-writer`: **COMPLETE**
  - [x] Extracted segment archetypes to `references/segment-archetypes.md` (641 words)
  - [x] Removed voice duplication (now references ghostwriter/ai-tells)
  - [x] Added socials-first angle development step in Phase 2
  - [x] Created `references/opening-letter-patterns.md` (2,025 words, 12 examples)
  - **Result:** Skill reduced from 2,852 → 1,803 words (37% reduction, now under 2,000 target)

### Completed Refactoring (All High/Medium Priority Complete)

| Skill | Before | After | Reduction | Key Changes |
|-------|--------|-------|-----------|-------------|
| **opened-daily-newsletter-writer** | 2,852 | 1,803 | 37% | Extracted archetypes + opening patterns |
| **ghostwriter** | 3,302 | 1,185 | 64% | Removed AI-tells duplicates, extracted human desires |
| **hook-and-headline-writing** | 3,542 | 1,445 | 59% | Extracted output templates, condensed formulas |
| **meta-ads-creative** | 2,880 | 1,062 | 63% | Extracted formats + audience segments |
| **podcast-production** | 2,701 | 1,924 | 29% | Condensed quality gates + structure sections |
| **cold-open-creator** | 2,517 | 982 | 61% | Extracted Schultz example + output template |

**Total words removed:** ~8,400 words across 6 skills

### Remaining Skills (Low Priority - Under 2,300w)
- youtube-clip-extractor (2,252w) - ✅ broken references fixed
- youtube-title-creator (2,216w) - has 6 broken references to fix
- opened-weekly-newsletter-writer (2,194w)

### Phase 11: Skill Architecture Map (Complete)

**Status:** Complete (2026-01-23)

Created `SKILL_ARCHITECTURE_MAP.md` - comprehensive visual documentation:
- Master flow diagram (Source → Distribution)
- Hub-specific chains (Podcast, Newsletter, Deep Dive)
- Video content skill chain
- Skill dependency matrix
- Platform-specific quick reference
- Identified gaps for future work

Fixed broken skill references in:
- `youtube-clip-extractor` (2 fixes)
- `video-caption-creation` (4 fixes)
- `youtube-downloader` (frontmatter fix)

Added "Examples Over Instructions" philosophy to `skill-creator`

### Phase 10: Slack Distribution Pipeline (New)

**Status:** Initial implementation complete
**Handoff:** `HANDOFF-slack-distribution.md`

New skill `slack-social-distribution` posts social content to `#market-daily` as threaded replies. Integrates with `newsletter-to-social` and `webflow-publish`.

**Open issue:** Slack reply editing restrictions - may need channel structure redesign.

### Phase 10: Hook/Headline Skill Split (Complete)

**Status:** Complete

Split monolithic `hook-and-headline-writing` into focused skills + references:

| Asset | Type | Purpose |
|-------|------|---------|
| `newsletter-subject-lines` | Skill | Subject lines for newsletters |
| `article-titles` | Skill | Blog posts, deep dives (formal/journalistic) |
| `references/segment-titles.md` | Reference | Segment headlines (1-6 words, in daily-newsletter) |
| `references/witty-voice-patterns.md` | Reference | Pirate Wires-inspired wit (in daily-newsletter) |
| `references/opening-letter-patterns.md` | Reference | 12+ real examples with full segment examples showing substance→take |
| `references/pirate-wires-segment-techniques.md` | Reference | A la carte Pirate Wires techniques for TTT segments (7 techniques with full excerpts) |

**Key design decisions:**
- Segment titles = reference file, not skill (only used during newsletter drafting)
- Pirate Wires witty voice = newsletter voice, not article titles (articles are more formal)
- Witty voice applies to: opening letters, segment titles, segment writing, weekly newsletter
- Examples do heavy lifting (swipe file approach)
- No scoring systems (removed 10 Commandments, 4 U's, Anatomy scores)
- Added note to `skill-creator` about content engine skill preferences
- Archived old `hook-and-headline-writing` to `_archived-pre-refactor/`
- **Substance → Take Pattern:** Core rhythm of newsletter prose - alternate between facts/quotes/data and interpretation/implication. Added to daily newsletter skill and opening-letter-patterns.md.

### Decisions Made
- **ai-tells vs human-writing:** Keep separate. ai-tells = constraint layer (what NOT to do), human-writing = Charlie's personal voice patterns.
- **human-writing location:** Should move to OpenEd Vault (colleagues need access)
- **Socials-first approach:** Insert framework-fitting check early in angle development
- **Content engine skill design:** Examples-heavy, no scoring, framework fitting approach (documented in skill-creator)

### Folder Reorganization Needed
- `Content/Master Content Database/` → Collapse, rename to "Published Content Database"
- `Master_Content_Index.md` → Move from `.claude/references/` to live with content it indexes
- **Principle:** Indexes should live with the content they reference

---

## Key Files Created

- `TEMPLATE_INDEX.md` - Lightweight template index for sub-agents (~200 tokens vs ~5,500)
- `sub-agent-prompts/*.md` - Platform-specific prompts for parallel execution
- Archived skills in `.claude/skills/_archived-pre-refactor/`

## Related

- Full plan: `PLAN.md`
- Archived skills: `.claude/skills/_archived-pre-refactor/README.md`
- Template index: `.claude/skills/text-content/references/templates/TEMPLATE_INDEX.md`
