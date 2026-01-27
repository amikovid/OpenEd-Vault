# Curriculove - Current State

**Last Updated:** 2026-01-26

---

## Live

**Production:** https://curricu.love
**Browse All:** https://curricu.love/browse
**Repo:** https://github.com/cdeistopened/curriculove

---

## What Works

| Feature | Status | Notes |
|---------|--------|-------|
| **Quiz** | ✅ | Deterministic 3-phase, ~90 sec |
| **Results** | ✅ | Philosophy breakdown, CTA above fold |
| **Email Capture** | ✅ | HubSpot integration |
| **Recommendations** | ✅ | Gemini 3 Flash, top 12 matches |
| **Swipe UI** | ✅ | Save/pass with voice review prompt |
| **Voice Reviews** | ✅ | Web Speech API → Gemini polish |
| **Review Persistence** | ✅ | Saves to Convex |
| **User Auth** | ✅ | Clerk (dev keys on prod) |
| **PWA** | ✅ | Installable on mobile |
| **Browse Page** | ✅ | Full catalog with filters |
| **AI-Generated Images** | ✅ | 213/216 curricula have images |

---

## Data State

**File:** `src/data/curricula-convex.json`

| Metric | Count |
|--------|-------|
| Total curricula | 216 |
| OpenEd Vendors | 49 |
| With images | 213 |
| Without images | 3 |

**Images:** `public/images/curricula/` - 149 AI-generated watercolor-line style images via Gemini.

---

## Known Issues

1. **Clerk dev keys on production** - Need production keys before public launch
2. **Local dev API key caching** - After changing `.env.local`, delete `.next` folder and restart

---

## What's Next

### Before Internal Launch
- [ ] Get production Clerk keys
- [ ] OpenEd icon badge (SVG) for partner curricula
- [ ] Internal Slack announcement + Loom demo
- [ ] Swag budget for top reviewers

### Phase 2: Enhanced Discovery
- [ ] "Reality Check" questions (prep time, budget)
- [ ] Neurodivergence screening
- [ ] Side-by-side comparison tool

### Phase 3: Social & Sharing
- [ ] Shareable quiz results (image generation)
- [ ] Public review pages per curriculum

---

## Key Files

```
curriculove/
├── NOW.md                        # This file
├── PROJECT.md                    # Full project doc
├── docs/
│   └── PRODUCT-SPEC-V2.md        # Image generation + UI polish spec
├── marketing/
│   ├── CURRICULOVE_LAUNCH_BRIEF.md
│   └── PREMORTEM.md
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main app (quiz flow)
│   │   └── browse/page.tsx       # Browse catalog
│   ├── components/
│   │   ├── Quiz.tsx
│   │   ├── Recommendations.tsx   # Swipe UI
│   │   ├── BrowseRecommendations.tsx
│   │   └── VoiceReview.tsx
│   ├── lib/quiz-agent/
│   │   └── scoring.ts            # Deterministic engine
│   └── data/
│       └── curricula-convex.json # 216 curricula
├── public/images/curricula/      # 149 AI-generated images
├── convex/
│   ├── reviews.ts
│   └── users.ts
└── scripts/
    ├── generate-curriculum-images.py  # Batch image generation
    └── scrape-images.ts               # Original Playwright scraper
```

---

## Environment

All configured on Vercel + `.env.local`:

```
GEMINI_API_KEY=...
NEXT_PUBLIC_CONVEX_URL=https://wary-gerbil-502.convex.cloud
CONVEX_DEPLOYMENT=dev:wary-gerbil-502
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
HUBSPOT_API_KEY=...
```

**Convex Dashboard:** https://dashboard.convex.dev/d/wary-gerbil-502

---

## To Resume

1. Read this NOW.md
2. Check production at https://curricu.love
3. For local dev: `npm run dev` (delete `.next` if API issues)
4. Deploy: `git push` (Vercel auto-deploys from main)

---

## Session Log

### 2026-01-26

**Completed:**
- Generated 149 AI curriculum images via Gemini (~$6 total)
- Updated JSON with image references (213/216 now have images)
- Created batch generation script (`scripts/generate-curriculum-images.py`)
- Wrote product spec v2 for images + UI polish
- Moved marketing docs to `marketing/` folder
- Merged `cdeistopened/task-selection` branch
- Pushed all changes to GitHub

**Style decisions for images:**
- Watercolor-line style (ink + washes)
- Square format (1:1)
- Playful interpretation of curriculum names
- Brand-integrated colors (subtle orange/blue accents)
- No text in images (UI provides overlay)

**Left off:** Ready for internal launch. Need Clerk prod keys, OpenEd badge icon, and swag budget approval.

---

### 2026-01-20

**Completed:**
- Deployed to Vercel production (curricu.love)
- Set up all Vercel env vars
- Created image scraper, got 70/216 images
- Moved "See Matching Curricula" CTA above the fold
- Built full browse page with search, filters, sort
