# Curriculove

**Homeschool curriculum discovery tool** - Quiz determines philosophy, then Tinder-style swipe through matched curricula.

**Domain:** curricu.love (DNS configured)
**Live:** Deploy via Vercel (connected to this repo)

---

## Stack

| Layer | Technology | Status |
|-------|------------|--------|
| **Frontend** | Next.js 16.1 (Turbopack) | ✅ Working |
| **Quiz Engine** | Deterministic scoring (no LLM) | ✅ Working |
| **Recommendations** | Gemini 3 Flash Preview | ✅ Working |
| **Database** | Convex | ✅ Deployed |
| **Auth** | Clerk | ✅ Configured |
| **Email Capture** | HubSpot API | ✅ Working |
| **Voice Reviews** | Web Speech API + Gemini polish | ✅ Working |

### Convex Deployment
- **Project:** `curriculove-444f2`
- **Deployment:** `dev:wary-gerbil-502`
- **Dashboard:** https://dashboard.convex.dev/d/wary-gerbil-502
- **URL:** `https://wary-gerbil-502.convex.cloud`

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

## Current State (2026-01-20)

### What's Working

| Feature | Status | Notes |
|---------|--------|-------|
| **Philosophy Quiz** | ✅ | Deterministic 3-phase, 5-8 questions, ~90 sec |
| **12-Dimension Profiling** | ✅ | Returns primary + 2 secondaries + confidence |
| **Email Capture** | ✅ | HubSpot integration with state dropdown |
| **Gemini Recommendations** | ✅ | Top 12 matches with personalized reasons |
| **Swipe UI** | ✅ | Save/pass with match score badges |
| **Voice Reviews** | ✅ | Web Speech API → Gemini polish → editable |
| **Review Persistence** | ✅ | Saves to Convex database |
| **User Auth** | ✅ | Clerk sign-in (optional for users) |
| **PWA Install** | ✅ | Add to home screen on mobile |
| **Bottom Navigation** | ✅ | Discover / Saves / Profile tabs |

### Environment (`.env.local`)
```
CONVEX_DEPLOYMENT=dev:wary-gerbil-502
NEXT_PUBLIC_CONVEX_URL=https://wary-gerbil-502.convex.cloud
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=...
HUBSPOT_API_KEY=...
```

### Run Locally
```bash
npm run dev
# Visit http://localhost:3000
```

---

## Architecture

### User Flow

```
[Quiz Phase] 5-8 questions
    ↓
[Results] Philosophy breakdown with confidence %
    ↓
[Email Gate] Optional capture → HubSpot
    ↓
[Recommendations] Gemini matches 12 curricula
    ↓
[Swipe UI] Save/Pass with "Have you tried this?"
    ↓
[Voice Review] If yes → Web Speech → Gemini polish → Convex
    ↓
[Completion] View saves, browse more, or retake
```

### Quiz Scoring (Deterministic - No LLM)

**3-Phase Flow:**
1. **Opener** - 5 orthogonal options → initial philosophy bucketing
2. **Guided Q2** - Based on opener choice, further disambiguates
3. **Refinement** - 3-6 questions from discrimination bank until 75%+ confidence

**12-Dimension Profile:**
| Tag | Name | Category |
|-----|------|----------|
| CL | Classical | Core |
| CM | Charlotte Mason | Core |
| TR | Traditional | Core |
| MO | Montessori | Method |
| WA | Waldorf | Method |
| UN | Unschooling | Freedom |
| WF | Wild + Free | Movement |
| NB | Nature-Based | Movement |
| PB | Project-Based | Method |
| EC | Eclectic | Movement |
| MS | Microschool | Movement |
| FB | Faith-Based | Values |

### Database Schema (Convex)

**reviews table:**
```typescript
{
  curriculumSlug, curriculumName,
  rawTranscript, polishedReview, rating,
  highlights[], concerns[], bestFor[],
  userId?, userEmail?, userName?,
  createdAt
}
```

**users table:**
```typescript
{
  clerkId, email, name?, imageUrl?,
  primaryPhilosophy?, secondaryPhilosophies[],
  favorites[], reviewCount,
  createdAt, updatedAt
}
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main app - state orchestration for all phases |
| `src/app/layout.tsx` | Root layout with Clerk + Convex providers |
| `src/components/Quiz.tsx` | Quiz UI |
| `src/components/Recommendations.tsx` | Swipe UI + review prompts |
| `src/components/VoiceReview.tsx` | Voice capture + AI polish |
| `src/components/EmailGate.tsx` | Email capture form |
| `src/lib/quiz-agent/scoring.ts` | Deterministic quiz engine (512 lines) |
| `src/app/api/recommendations/route.ts` | Gemini matching |
| `src/app/api/polish-review/route.ts` | Review polishing |
| `convex/reviews.ts` | Review mutations/queries |
| `convex/users.ts` | User mutations/queries |
| `src/data/curricula-convex.json` | 216 curricula dataset |

---

## Data

### Curriculum Schema
```typescript
{
  slug: string,
  name: string,
  imageUrl?: string,        // Currently null - needs scraping
  logoUrl?: string,
  website: string,
  gradeRange: string,       // "K-5th", "PreK-12"

  philosophyTags: string[], // ["CM", "NB"]
  methodTags: string[],
  audienceTags: string[],

  description: string,
  pricingSummary: string,
  priceTier: string,        // "$", "$$", "$$$", "$$$$"
  openedInsight: string | { quote?, attribution?, synthesis?, hasFullReview },

  isOpenEdVendor: boolean,  // 49 of 216
  prepTimeScore?: number,   // 1-10
  teacherInvolvementLevel?: string,
}
```

**File:** `src/data/curricula-convex.json` (216 tools)

---

## Q3 Priorities

### ✅ Completed (This Session)
- [x] Convex persistence - reviews save to database
- [x] Clerk auth integration - user accounts work
- [x] PWA manifest - mobile installable
- [x] All API keys configured

### 🔲 Remaining
- [ ] UI polish pass (green accent, card refinements)
- [ ] Image scraping for curricula (all imageUrl currently null)
- [ ] Shareable image generation (Nano Banana templates)
- [ ] Provider outreach template
- [ ] Deploy to Vercel production

### Future Features
- "Reality Check" questions (time, budget)
- Neurodivergence screening
- "First year homeschooler?" mode
- Advanced filtering on saves
- Social sharing of quiz results

---

## Provider Partnership Play

1. Compile list of all 216 curriculum providers
2. Create outreach template: "You're featured in our new app"
3. Offer: Help them get reviews from their customers
4. Ask: Would you share with your audience?
5. Flywheel: Their audience → our app → our email list

**OpenEd Vendors:** 49 of 216 are official partners (flagged `isOpenEdVendor: true`)

---

## Session Log

### 2026-01-20 - MVP Infrastructure Complete

**Completed:**
- Created Convex project and deployed schema
- Enabled review persistence to Convex
- Configured all API keys (Convex, Clerk, Gemini, Anthropic, HubSpot)
- Added PWA manifest for mobile install
- Fixed Clerk provider issues (was breaking SSR)
- Simplified auth flow - ClerkProvider always wraps app

**Ready for:**
- Internal team testing
- Voice review collection
- User authentication

**Next session:**
- Deploy to Vercel
- Test full flow with team
- Image scraping for curricula
