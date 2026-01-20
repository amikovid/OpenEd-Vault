# Curriculove - Current State

**Last Updated:** 2026-01-13

---

## What It Is

Tinder for homeschool curriculum. Quiz determines your philosophy, then swipe through matched curricula.

**Working MVP at:** `npm run dev` → http://localhost:3000

---

## What Works

1. **Deterministic Scoring Quiz** (NEW 2026-01-13)
   - Fixed opener: "Which best describes your homeschool vision?"
   - 5 maximally orthogonal options mapping to philosophy clusters
   - Guided Q2 based on opener choice (deterministic branching)
   - Question bank with explicit score deltas for disambiguation
   - Tracks 12-dimensional philosophy profile
   - Completes at 75%+ confidence with minimum 5 questions
   - Returns primary + secondary with percentage breakdown
   - **NEW: Results screen shows philosophy breakdown before recommendations**

2. **Recommendations** (Gemini 3 Flash)
   - Pre-filters 216 curricula by philosophy tags
   - Returns 12 ranked matches with personalized reasons
   - Includes match score, pricing, OpenEd insight

3. **Basic Swipe UI**
   - Cards with curriculum info
   - ✕ pass / ♥ save buttons
   - Favorites summary at end

---

## Data State

**File:** `src/data/curricula-convex.json` (enriched 2025-01-13)

| Metric | Count |
|--------|-------|
| Total curricula | 216 |
| OpenEd Vendors | 49 |
| With editorial insight | 212 |
| EC-only tags | **4** (down from 81) |

**Philosophy Distribution (post-enrichment):**
| Tag | Count | Philosophy |
|-----|-------|------------|
| TR | 93 | Traditional |
| PB | 50 | Project-Based |
| CL | 47 | Classical |
| UN | 38 | Unschooling |
| MO | 36 | Montessori |
| CM | 28 | Charlotte Mason |
| FB | 22 | Faith-Based |
| EC | 19 | Eclectic |
| WF | 8 | Wild + Free |
| MS | 5 | Microschool |
| NB | 3 | Nature-Based |

**Schema fields:**
- slug, name, website, gradeRange
- philosophyTags, methodTags, audienceTags
- description, pricingSummary, priceTier
- openedInsight, isOpenEdVendor, source
- imageUrl (all null - needs scraping)
- logoUrl (from Webflow icons)

**NEW enrichment fields (2025-01-13):**
- `prepTimeScore` (1-10, where 1=open-and-go)
- `teacherInvolvementLevel` (high/medium/low/zero)
- `lessonDuration` (short/medium/long)
- `originalPhilosophyTags` (audit trail)
- `philosophyReasoning` (AI explanation)

---

## What's Next

### Ralph-Ready Tasks

**Task 1: Schema Enrichment** - COMPLETED 2025-01-13
- Ran `scripts/enrich-curriculum-data.py` with Gemini 3 Flash
- Reduced EC-only from 81 → 4 (95% reduction)
- Added prepTimeScore, teacherInvolvementLevel, lessonDuration
- All original source data preserved

**Task 1.5: Quiz Redesign** - COMPLETED 2026-01-13
- Replaced LLM-reasoning quiz with deterministic scoring engine
- Created `docs/QUIZ-REDESIGN.md` architecture doc
- Added Results component with percentage breakdown
- 4-stage flow: Opener → Guided Q2 → Question Bank → Complete
- Question bank with 12 disambiguation questions
- Minimum 5 questions, completes at 75% confidence

**Task 2: Image Scraping**

```
/ralph-loop "
For each curriculum in src/data/curricula-convex.json where imageUrl is null:
1. Fetch the website URL
2. Try to extract og:image meta tag
3. If no og:image, take Puppeteer screenshot of homepage
4. Save image to public/images/{slug}.jpg
5. Update imageUrl in JSON

Skip failures, log them.
Output <promise>IMAGES_COMPLETE</promise> when 200+ have imageUrl populated.
" --max-iterations 40 --completion-promise "IMAGES_COMPLETE"
```

**Task 3: Frontend Polish**

```
/ralph-loop "
Implement the Curriculove swipe UI to match the mockups:
- Green accent color (#10B981)
- Match badge on card (e.g., '94% Match')
- Pills for price tier, grade range, philosophy tags
- 'OpenEd Expert Insight' callout box
- Bottom nav: Discover / Saves / Profile
- Saves list with filters (Price, Grade, Philosophy)
- Completion screen with celebration

Test each screen renders without errors.
Output <promise>UI_COMPLETE</promise> when all screens match spec.
" --max-iterations 25 --completion-promise "UI_COMPLETE"
```

### After Ralph

- Convex setup (currently using in-memory sessions)
- Email capture → HubSpot
- Reviews/ratings after save
- "Reality check" quiz questions (time/budget conflicts)

### Design

- Have UI mockups (green accent, match badges)
- See research doc on curriculum discovery architectures
- Competitors: Cathy Duffy, Homeschool On, Timberdoodle

---

## Key Files

```
curriculove/
├── PROJECT.md              # Full project doc
├── NOW.md                  # This file
├── docs/QUIZ-REDESIGN.md   # Quiz architecture doc (for review)
├── src/
│   ├── app/page.tsx        # Main app (quiz → results → recs → favorites)
│   ├── components/
│   │   ├── Quiz.tsx        # Quiz UI
│   │   ├── Results.tsx     # NEW: Philosophy breakdown display
│   │   └── Recommendations.tsx  # Swipe UI
│   ├── lib/quiz-agent/
│   │   ├── scoring.ts      # NEW: Deterministic scoring engine
│   │   ├── agent.ts        # Claude tool-use agent (legacy, not used)
│   │   └── prompt.ts       # Opener question + guided Q2 signals
│   ├── lib/sessionStore.ts # Session state (scores, phase, history)
│   ├── app/api/
│   │   ├── quiz/           # Quiz endpoints (deterministic scoring)
│   │   └── recommendations/route.ts  # Gemini matching
│   └── data/
│       └── curricula-convex.json  # 216 curricula
└── scripts/
    └── enrich-curriculum-data.py  # Gemini batch enrichment
```

---

## Reference Data (Parent Folder)

- `OpenEd - Tools.csv` - Webflow export (76 tools, HTML content)
- `OpenEd_Tool_Database.md` - Markdown tool database
- `110+ Most Popular.../` - Notion export of curriculum info
- `Lead Magnet Guides/` - Hormozi, Brunson lead magnet strategy

---

## Technical Notes

- **Quiz now uses deterministic scoring** - no LLM calls during quiz (faster, predictable)
- **4-stage quiz flow:** Opener → Guided Q2 → Refinement (question bank) → Complete
- **Score deltas are explicit:** Each answer updates specific philosophy scores
- **Question bank:** 12 disambiguation questions targeting ambiguous pairs
- **Convex schema changes are easy** - just add fields, no migrations
- **Sessions are in-memory** - will lose on server restart until Convex
- **Gemini model:** `gemini-3-flash-preview`

---

## Strategic Context (from Research)

### Homeschool On Survey Analysis

**Full survey:** `references/homeschool-on-survey.md`

Competitor uses 45+ question form across 6 sections. Key differences:

| Aspect | Homeschool On | Curriculove |
|--------|--------------|-------------|
| Approach | Information gathering | Philosophy discovery |
| Length | 10+ minutes, 45+ inputs | 90 seconds, 3-6 questions |
| Philosophy | User self-identifies | We tell them |
| Feel | Tax form | Personality quiz |
| Input types | Drag-rank, multi-select, sliders | Simple buttons |

**Steal-worthy for Phase 2:**
- Visual opener (pick images representing ideal homeschool day)
- Subject-specific preferences (mastery vs spiral math)
- Learning needs screening (dyslexia, attention, twice-exceptional)
- Child fascination topics (for per-subject matching)

**Our advantage:** Fun, fast, mobile-first, discovery-based.

---

Reviewed comprehensive competitive analysis doc. Key insights:

**Competitor Landscape:**
- Homeschool On - personality quiz (45 questions, weighted)
- Cathy Duffy - parametric search (granular filters)
- Timberdoodle - kit builder wizard
- Uschool - AI chatbot planner

**Gaps We Can Fill:**
1. "Aspiration vs Reality" - detect conflicts (wants Classical but has 1hr/day)
2. "Eclectic Stack" - recommend per-subject, not one box
3. "Deschooling" - first-year homeschoolers need gentler ramp

**Schema Fields to Add (when ready):**
- `prepTimeScore` (1-10) - prevents burnout
- `teacherInvolvementLevel` - high/med/low/zero
- `lessonDuration` - short/med/long (ADHD filter)
- `specialNeedsTags` - dyslexia, adhd, asd friendly
- `familyStyleFriendly` - combine multiple ages?
- `sensoryProfile` - V/A/K (visual/auditory/kinesthetic)

**Quiz Enhancements (Phase 2):**
- "Reality check" after philosophy (time, budget)
- "Is this your first year?" (deschooling filter)
- Neurodivergence screening
- Multi-select options

---

## Questions/Decisions Pending

1. Do we add kid ages/grades to quiz? (Decided: skip for now - style transcends ages)
2. Multi-select quiz options? (Discussed but not implemented)
3. Slack integration for gathering curriculum insights? (Mentioned but not built)
4. Convex vs continue with in-memory? (Convex when ready for persistence)

---

## To Resume

1. Read this NOW.md + PROJECT.md
2. `cd curriculove && npm run dev`
3. Test at http://localhost:3000
4. Pick a Ralph-able task or continue building
