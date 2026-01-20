# Curriculove

**Homeschool curriculum discovery tool** - Quiz determines philosophy, then Tinder-style swipe through matched curricula.

**Domain:** curricu.love
**Stack:** Next.js, Claude (quiz), Gemini (recommendations), Convex (planned)

---

## Strategic Vision

> "Almost like a new social media platform for homeschool moms" - but not ready to pitch that yet.

**Q3 Goal:** Prove the concept before scaling.

### Why This Could Be Huge

1. **Automatic lead capture** - Every user gives email = lead by default
2. **Data moat** - Reviews on curricula = proprietary data no one else has
3. **Expert positioning** - OpenEd becomes THE authority on curriculum
4. **Partnership flywheel** - Providers want to be featured, drive their audiences to us
5. **Viral potential** - Shareable assets (quiz results, recommendations) spread organically

### The Flywheel

```
User takes quiz → Gets recommendations → Saves favorites → Shares result
        ↓                                        ↓              ↓
   Email captured                          Writes review    Friends see
        ↓                                        ↓              ↓
   Nurture sequence                        Data grows     New users
        ↓                                        ↓              ↓
   Enrollment lead                       Expert authority    Repeat
```

---

## Current State

Working MVP:
- Adaptive quiz (Claude Haiku) → determines philosophy
- Gemini recommendations → matches to 216 curricula
- Basic swipe UI → save favorites

**Run locally:** `npm run dev` → http://localhost:3000

---

## Architecture

```
Quiz (Claude Haiku)     →  Philosophy Result  →  Recommendations (Gemini)  →  Swipe UI
   ↓                           ↓                        ↓
Tool-use agent           12 philosophy tags        216 curricula
asks 3-6 questions       + confidence %            ranked by match
```

### Philosophy Tags (12)

| Tag | Name | Core Distinction |
|-----|------|------------------|
| CL | Classical | Great Books, Latin, Socratic, trivium |
| CM | Charlotte Mason | Living books, nature study, narration |
| TR | Traditional | Textbooks, grades, tests, school-at-home |
| MO | Montessori | Prepared environment, child chooses work |
| WA | Waldorf | Rhythm, imagination, delayed academics |
| UN | Unschooling | Child-led, no curriculum |
| EC | Eclectic | Mix and match |
| PB | Project-Based | Real problems, authentic products |
| NB | Nature-Based | Forest school, outdoor focus |
| WF | Wild + Free | Wonder, nature, community |
| FB | Faith-Based | Faith integrated throughout |
| MS | Microschool | Small group, shared teaching |

---

## Data

### Curriculum Schema

```typescript
{
  slug: string,
  name: string,
  imageUrl?: string,
  logoUrl?: string,
  website: string,
  gradeRange: string,           // "K-5th", "PreK-12"

  // Matching
  philosophyTags: string[],     // ["CM", "NB"]
  methodTags: string[],         // ["mastery-based", "adaptive"]
  audienceTags: string[],       // ["secular", "christian"]

  // Content
  description: string,
  pricingSummary: string,
  priceTier: string,            // "$", "$$", "$$$", "$$$$"
  openedInsight: string,        // Editorial summary

  // Flags
  isOpenEdVendor: boolean,      // Official partner
  source: string,               // "webflow" | "markdown"
}
```

**File:** `src/data/curricula-convex.json` (216 tools)

### Transform Data

```bash
python3 scripts/transform-curriculum-data.py
```

Reads from `OpenEd - Tools.csv`, outputs enriched JSON.

---

## Key Files

| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main app (quiz → recs → favorites) |
| `src/components/Quiz.tsx` | Quiz UI |
| `src/components/Recommendations.tsx` | Swipe UI |
| `src/lib/quiz-agent/agent.ts` | Claude agent with tools |
| `src/lib/quiz-agent/prompt.ts` | Quiz system prompt |
| `src/app/api/quiz/*` | Quiz API routes |
| `src/app/api/recommendations/route.ts` | Gemini matching |
| `scripts/transform-curriculum-data.py` | Data transformation |

---

## Future Enhancements

### Schema (add when needed)
- `prepTimeScore` (1-10)
- `teacherInvolvementLevel` (high/medium/low/zero)
- `specialNeedsTags` (dyslexia, adhd friendly)
- `lessonDuration` (short/medium/long)
- `familyStyleFriendly` (boolean)

### Quiz (Phase 2)
- "Reality Check" questions (time, budget conflicts)
- Neurodivergence screening
- "First year homeschooling?" filter
- Multi-select options

### Features
- Convex persistence
- User accounts
- Review/rating after save
- Email capture → HubSpot
- Image scraping for hero images

### Viral Mechanics (Q3 Priority)
- **Shareable quiz results** - Pinterest-perfect images with philosophy match
- **Nano Banana templates** - Customizable but templated images (engineered elements)
- **Provider co-marketing** - "Your curriculum is listed, share with your audience"
- **Instagram-ready assets** - Cute, shareable, drives traffic back

### Provider Partnership Play
1. Compile list of all 216 curriculum providers
2. Create outreach template: "You're featured in our new app"
3. Offer: Help them get reviews from their customers
4. Ask: Would you share with your audience?
5. Flywheel: Their audience → our app → our email list

---

## Handoff Docs

Separate tasks that can be done elsewhere:

- `CONTENT-EXTRACTION-HANDOFF.md` - Scan content database for entities (GraphRAG)
- `SWIPE-UI-SPEC.md` - Detailed swipe interface design
- `DATA-TRANSFORMATION-PLAN.md` - Full transformation logic

---

## OpenEd Vendors (49 of 216)

Tools available through OpenEd partnership - flagged with `isOpenEdVendor: true`.

See `scripts/transform-curriculum-data.py` for full list.

---

## Q3 Priorities

### Must Do
- [ ] UI polish pass (looks good, make it great)
- [ ] Shareable image generation (Nano Banana templates)
- [ ] Provider outreach template
- [ ] Track as lead source in HubSpot

### Success Metrics
- Signups per week (trend)
- Email → nurture → enrollment attribution
- Provider partnership conversations started
- Organic shares (viral coefficient proxy)

### Separate Strategy Session Needed
Full curricula strategy session to map out:
- Detailed viral mechanics
- Provider partnership program
- Feature roadmap beyond Q3
- Potential as "social platform for homeschool moms"
