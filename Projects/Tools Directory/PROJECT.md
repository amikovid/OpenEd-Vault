---
name: Tools Directory
description: Teacher-reviewed curriculum database with E-E-A-T signals from OpenEd staff + parent voices
status: active
parent: SEO Content Production
created: 2026-01-01
updated: 2026-01-26
---

## Session Starter Prompt

```
I'm working on the OpenEd Tools Directory - a parent-reviewed curriculum database on Webflow.

Current state:
- 3 reviews published (Math-U-See, Saxon, Beast Academy)
- Teaching Textbooks draft ready
- Webflow CMS connected (collection ID: 6811bc7ab1372f43ab83dec6)
- 70+ tools mined from Slack with 150+ quotes

Today's focus: [FILL IN - e.g., "Webflow template refactoring" / "Draft 3 more reviews" / "Fix author linking"]

Read the full PROJECT.md at: OpenEd Vault/Projects/Tools Directory/PROJECT.md
```

---

## Curriculove Integration (NEW)

**The Flywheel:**
```
Curriculove quiz → User reviews curricula → Reviews feed Tools Directory → Tools Directory SEO → Traffic discovers Curriculove
```

**Key insight:** Curriculove generates *volume* of reviews (voice-enabled, low friction). Tools Directory needs *depth* (long-form, SEO-optimized). They complement each other:

| Curriculove | Tools Directory |
|-------------|-----------------|
| Quick voice reviews | Long-form written reviews |
| User-generated | Staff-authored (E-E-A-T) |
| Quantity play | Quality play |
| Lead capture | SEO traffic |

**Data flow:**
1. Curriculove collects quick reviews (stars + highlights + concerns)
2. Staff reviews aggregate Curriculove data as "What Parents Say"
3. Tools Directory pages link to Curriculove for "Leave Your Review"

---

# Tools Directory Project

**Goal:** Parent-reviewed curriculum/tool database as an SEO play with real voices.

**Q3 Target:** Launch with 20+ initial tool reviews

---

## Strategic Intent

Most curriculum review sites are:
- Generic aggregations of other review sites
- Written by nobody (or ChatGPT)
- No real perspective or experience

Ours will be:
- Written by named parents (their byline, their perspective)
- Based on actual interviews (Ella's pipeline)
- Real opinions, not hedged everything-is-great reviews
- SEO-optimized but authentically human

---

## Key Decision: Author Model

**Option A: One author per tool (SELECTED)**
- Each review has a named parent author
- Their byline, their portfolio piece
- Better for SEO (real author, E-E-A-T signals)
- Better for community (parents become contributors)

**Option B: Multiple reviews per tool** (future phase)
- User-generated reviews
- Rating aggregation
- Requires account system
- Save for v2

---

## The Ella Interview Pipeline

Ella does interview-style meetings (not podcasts) to gather source material.

**Per interview yield:** ~5 tool reviews

### Interview Template (send to Ella)

**Opening:**
- How long have you been homeschooling?
- How many kids, what ages/grades?
- What's your general approach? (Classical, Charlotte Mason, eclectic, etc.)

**For each curriculum/tool:**
1. What is it? (Name, subject, grade level)
2. How long have you used it?
3. What made you try it?
4. What do your kids think of it?
5. What works well?
6. What doesn't work or who is it NOT for?
7. How does it fit into your daily/weekly routine?
8. Would you recommend it? To whom specifically?
9. Anything you wish you'd known before starting?

**Closing:**
- What's the one tool you couldn't homeschool without?
- Any tools you tried and abandoned? Why?
- What's on your wishlist to try next?

---

## Review Structure

Each published review:

```markdown
# [Tool Name] Review: A [Grade Level] [Subject] Curriculum

**Reviewed by:** [Parent Name], [City, State]
**Family:** [X] kids, ages [Y-Z]
**Homeschool style:** [Approach]
**Used for:** [Duration]

## The Bottom Line
[One paragraph summary - would they recommend, to whom]

## What We Loved
- [Specific benefit 1]
- [Specific benefit 2]
- [Specific benefit 3]

## What Didn't Work
- [Honest criticism 1]
- [Honest criticism 2]

## Who This Is For
[Specific family types, learning styles, situations]

## Who Should Skip This
[Honest about who it's NOT for]

## Daily/Weekly Implementation
[How they actually use it - practical details]

## The Verdict
[Rating or recommendation level]

---
*[Parent Name] homeschools [X] children in [Location]. [One sentence about their approach or philosophy.]*
```

---

## SEO Targets by Category

| Category | Example Keywords | Search Volume |
|----------|------------------|---------------|
| Math | "best homeschool math curriculum" | High |
| Reading | "teach reading at home" | High |
| Science | "homeschool science curriculum review" | Medium |
| History | "classical history curriculum" | Medium |
| Full Curriculum | "all in one homeschool curriculum" | High |

---

## Folder Structure

```
Tools Directory/
├── PROJECT.md (this file)
├── Interview Template.md
├── Tools/
│   └── [Tool Name]/
│       ├── Parent_Interview.md
│       ├── Review_Draft.md
│       ├── Review_Final.md
│       └── Meta.md (SEO keywords, internal links)
├── Author Guidelines.md
└── Publishing Calendar.md
```

---

## Webflow CMS Integration

**Site:** opened.co
**Tools Collection ID:** `6811bc7ab1372f43ab83dec6`
**Authors Collection ID:** `68089af9024139c740e4b922`

### Field Mapping (E-E-A-T First Structure)

| Toggle Label | CMS Field | Content |
|--------------|-----------|---------|
| **Teacher's Take** | `subject-content` | Author byline, review intro, quick verdict, best for / not for |
| **What Parents Say** | `teaching-format-content` | OpenEd teacher quotes + external quotes (woven as prose) |
| **How It Works** | `pricing-content` | Subjects, grade levels, materials, lesson structure, parent involvement |
| **Pricing** | `parent-involvement` | Costs, cost-saving tips |
| **FAQs & Alternatives** | `parent-feedback-content` | Common questions, alternative curriculum links |

### Publishing via API

```bash
# Update item
curl -X PATCH "https://api.webflow.com/v2/collections/{collection_id}/items/{item_id}" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fieldData": {...}}'

# Publish (required for changes to go live)
curl -X POST "https://api.webflow.com/v2/collections/{collection_id}/items/publish" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -d '{"itemIds": ["{item_id}"]}'
```

---

## Slack Mining (Source Material)

**Report:** `slack-reports/tool-mentions-2026-01-21.md`
**Tools mined:** 70+ curriculum tools with 150+ authentic teacher quotes

### Top Tools by Quote Volume (prioritize these)
1. Math-U-See (Rachael Davie - 4 quotes) ✓ DRAFTED
2. Teaching Textbooks (Chelsea Forsythe)
3. Saxon Math (Rachael Davie)
4. Beast Academy (Danielle Randall)
5. Life of Fred (Morgann Wray)

---

## Session Notes (2026-01-22)

### Published Reviews (3 live)

| Tool | Author | URL |
|------|--------|-----|
| Math-U-See | Rachael Davie | opened.co/tools/math-u-see |
| Saxon Math | Rachael Davie | opened.co/tools/saxon-math |
| Beast Academy | Danielle Randall | opened.co/tools/beast-academy-online |

### Template Finalized

- **Teacher's Take** leads with named author, weaves colleague quotes ("My colleague Keely notes...")
- **What Parents Say** = external community only (blogs, forums)
- **H2 headers** include tool name for SEO (e.g., "Math-U-See Pricing")
- **Honest Best For / May Not Fit** lists
- **Toggles kept** for UX - Google confirms accordion content indexed in mobile-first

### Pending

- **Teaching Textbooks** - Draft ready, needs Webflow item created first
- **Author links** - Not yet connected to author profiles (hardcoded in template)
- **External quotes** - What Parents Say sections need more attributed blog quotes

### Authors in Webflow

| Author | ID | Specialty |
|--------|-----|-----------|
| Rachael Davie | `697133d342e4976b0b0f8019` | Math, former HS teacher |
| Danielle Randall | TBD | Gifted learners |
| Chelsea Forsythe | TBD | Independent curricula |

---

## Metrics

- **Slack tools mined:** 70+
- **Reviews drafted:** 4 (Math-U-See, Saxon, Beast Academy, Teaching Textbooks)
- **Reviews published:** 3 / 20

---

## Skills to Chain

- `ghostwriter` - Human voice, anti-AI patterns
- `ai-tells` - Check for AI writing patterns before publish

---

## Drafts Ready

```
Tools Directory/drafts/
├── math-u-see-v2.md        ✓ PUBLISHED
├── saxon-math.md           ✓ PUBLISHED
├── beast-academy.md        ✓ PUBLISHED
├── teaching-textbooks.md   READY (needs Webflow item)
└── khan-academy-review-draft.md  (older format)
```

## Next Priority Reviews

From Slack mining, by quote volume:
1. ~~Math-U-See~~ ✓
2. ~~Saxon Math~~ ✓
3. ~~Beast Academy~~ ✓
4. Teaching Textbooks (draft ready)
5. Life of Fred (Morgann Wray)
6. All About Reading
7. Singapore Math

---

*Created: 2026-01-01*
*Updated: 2026-01-22*
