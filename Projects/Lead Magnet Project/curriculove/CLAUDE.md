# Curriculove

**Homeschool curriculum discovery app** - Quiz determines philosophy, then Tinder-style swipe through matched curricula with voice reviews.

**Live:** https://curricu.love
**Repo:** https://github.com/cdeistopened/curriculove

---

## Quick Start

```bash
npm run dev          # http://localhost:3000
git push             # Auto-deploys to Vercel
```

If API issues after env changes: `rm -rf .next && npm run dev`

---

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 16.1 (Turbopack) |
| Database | Convex (`wary-gerbil-502`) |
| Auth | Clerk |
| AI | Gemini 3 Flash (recommendations + review polish) |
| Email | HubSpot API |

**Convex Dashboard:** https://dashboard.convex.dev/d/wary-gerbil-502

---

## Key Files

| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main quiz flow orchestration |
| `src/app/browse/page.tsx` | Full catalog with filters |
| `src/components/Quiz.tsx` | Quiz UI |
| `src/components/Recommendations.tsx` | Swipe UI + review prompts |
| `src/components/VoiceReview.tsx` | Voice capture + AI polish |
| `src/lib/quiz-agent/scoring.ts` | Deterministic quiz engine |
| `src/data/curricula-convex.json` | 216 curricula dataset |
| `convex/reviews.ts` | Review mutations/queries |
| `convex/users.ts` | User mutations/queries |
| `scripts/generate-curriculum-images.py` | Batch AI image generation |

---

## Data

**216 curricula** in `src/data/curricula-convex.json`
- 49 are OpenEd vendors (`isOpenEdVendor: true`)
- 213 have AI-generated images (`public/images/curricula/`)

**12-Dimension Philosophy Tags:**
CL (Classical), CM (Charlotte Mason), TR (Traditional), MO (Montessori), WA (Waldorf), UN (Unschooling), WF (Wild + Free), NB (Nature-Based), PB (Project-Based), EC (Eclectic), MS (Microschool), FB (Faith-Based)

---

## User Flow

```
Quiz (5-8 questions, ~90 sec)
    ↓
Results (philosophy breakdown + confidence %)
    ↓
Email Gate (optional → HubSpot)
    ↓
Recommendations (Gemini matches 12 curricula)
    ↓
Swipe UI (Save/Pass + "Have you tried this?")
    ↓
Voice Review (if yes → Web Speech → Gemini polish → Convex)
```

---

## Environment

All keys configured on Vercel + `.env.local`:

```
GEMINI_API_KEY=...
NEXT_PUBLIC_CONVEX_URL=https://wary-gerbil-502.convex.cloud
CONVEX_DEPLOYMENT=dev:wary-gerbil-502
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
HUBSPOT_API_KEY=...
```

---

## Related Files

- `NOW.md` - Current state, session log, what's next
- `PROJECT.md` - Strategic vision, full roadmap, provider partnership play
- `docs/PRODUCT-SPEC-V2.md` - Image generation + UI polish spec
- `marketing/CURRICULOVE_LAUNCH_BRIEF.md` - Launch materials

---

*For current priorities and session context, see NOW.md*
