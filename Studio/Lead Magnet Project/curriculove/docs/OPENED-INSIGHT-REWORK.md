# OpenEd Insight Section Rework

**Status:** Spec Complete
**Created:** 2026-01-19
**Interview Source:** Claude Code session with Charlie

---

## Goal

Build trust and authority by showing OpenEd has real expertise on each curriculum. The insight section should feel like "we actually know this curriculum" rather than generic filler.

---

## Current State

- `openedInsight` is a single string field in `curricula-convex.json`
- Content is thin: "Ginny Yurich. Outdoor focus." or "Community favorite."
- "Full Review" link goes to curriculum's own website (not OpenEd)
- Same sparse treatment for all 216 curricula

---

## New Design

### Data Schema Change

Convert `openedInsight` from string to object:

```typescript
interface OpenEdInsight {
  quote?: string;           // Real teacher/parent quote (the gold)
  attribution?: string;     // "Sarah M." format (First name, last initial)
  synthesis?: string;       // 1-2 sentence editorial summary
  hasFullReview: boolean;   // Whether opened.co/tool/[slug] exists
}
```

### Content Tiers

**Tier 1: Full Review Available (~72 curricula)**
- Real quote with attribution
- Editorial synthesis
- "Read Full Review" link to opened.co/tool/[slug]

**Tier 2: Source Material Available (~80 curricula)**
- AI-generated mini-insight from:
  - Slack channel discussions
  - Podcast mentions
  - Internal team knowledge
- No "Full Review" link (or disabled)

**Tier 3: Minimal Data (~64 curricula)**
- AI-generated insight from curriculum's own data
- Based on: prepTimeScore, teacherInvolvementLevel, philosophyTags, description
- No "Full Review" link

### Visual Treatment

- **Same design for all tiers** - no gold/silver badge distinction
- Keep the current callout box style with icon
- Only show "Full Review" link when `hasFullReview: true`
- Link destination: `opened.co/tool/[slug]`

### UI Copy

**Header:** "OpenEd Insight" (not "OpenEd Expert Insight" - shorter)

**Content Format:**
```
"[Quote from real teacher]" - [First Name L.]

[1-2 sentence synthesis]

[Read Full Review →]  ← only if hasFullReview
```

**Example (Tier 1 - Beast Academy):**
```
"Fun without sacrificing quality - perfect for kids who want a challenge."
- Sarah M., OpenEd Teacher

Engaging comic-book style math that requires parent oversight
but delivers deep conceptual understanding.

Read Full Review →
```

**Example (Tier 2 - AI-generated with sources):**
```
Popular among Charlotte Mason families for its gentle,
literature-based approach. Requires moderate parent involvement.
```

**Example (Tier 3 - AI-generated from data):**
```
Traditional curriculum with high teacher involvement.
Best for structured families who prefer scripted lessons.
```

---

## Implementation Plan

### Phase 1: Structural Fix (This Session)
1. Update TypeScript interfaces for new schema
2. Migrate `openedInsight` string → object with `synthesis` field
3. Add `hasFullReview: false` to all entries (default)
4. Update UI components to handle new structure
5. Conditionally show/hide "Full Review" link
6. Change link destination to opened.co/tool/[slug]

### Phase 2: Content Enrichment (Future Session)
1. Export list of 72 Webflow tools with slugs
2. Cross-reference with curricula-convex.json
3. Set `hasFullReview: true` for matching entries
4. Generate Slack reports for remaining curricula
5. Extract quotes and synthesize insights
6. Update JSON with enriched content

### Phase 3: Template Alignment (Future)
1. Update Webflow tool page template per TOOL_REVIEW_TEMPLATE.md
2. Consolidate "What Parents Say" + basic facts into single page
3. Rewrite reviews using source material (podcast transcripts, Slack)

---

## Source Material Locations

| Source | Location | Coverage |
|--------|----------|----------|
| Webflow CMS | opened.co/tool/* | 72 tools |
| Slack Reports | Tools Directory/slack-reports/ | Generating |
| Podcast Transcripts | Via transcript search | ~50 tools mentioned |
| Internal Knowledge | Team Slack #recommendations | Ongoing |
| Enrichment Data | curricula-convex.json | prepTimeScore, etc. |

---

## Technical Notes

- **URL Pattern:** opened.co/tool/[slug]
- **Attribution Format:** "First Name L." (e.g., "Sarah M.")
- **Quote Max Length:** ~100 chars (fits on card)
- **Synthesis Max Length:** ~150 chars (2 lines on mobile)
- **Webflow MCP:** May need setup for live data sync

---

## Questions Resolved

| Question | Decision |
|----------|----------|
| Primary goal | Build trust/authority |
| Link destination | OpenEd review page (opened.co/tool/slug) |
| Fallback for no review | AI-generated mini-insight |
| Quote vs summary | Both - quote with attribution + synthesis |
| Visual treatment by tier | Same for all (no badge differentiation) |
| Attribution format | First Name L. |
| Data structure | Expand to object with structured fields |
| Implementation scope | Structural fix first, content later |

---

## Success Metrics

- Users click "Full Review" link (when available)
- Insight content feels specific, not generic
- No "Community favorite" type filler content
- Clear differentiation between curricula

---

*Spec created via interview process - ready for implementation*
