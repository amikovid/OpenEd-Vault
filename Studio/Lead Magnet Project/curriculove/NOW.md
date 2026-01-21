# Curriculove - Current State

**Last Updated:** 2026-01-20

---

## Live

**Production:** https://curricu.love
**Browse All:** https://curricu.love/browse

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

---

## Browse Page Features (NEW)

Full curriculum catalog at `/browse`:

- **Search** - Name + description
- **Philosophy filter** - All 12 philosophies
- **Grade filter** - PreK, K-5, 6-8, 9-12
- **Price filter** - Budget to Luxury
- **Sort** - A-Z, Z-A, Price, OpenEd Partners first
- **OpenEd Only toggle** - 49 partner curricula
- **View toggle** - List (default) or Swipe mode

---

## Data State

**File:** `src/data/curricula-convex.json`

| Metric | Count |
|--------|-------|
| Total curricula | 216 |
| OpenEd Vendors | 49 |
| With images | 70 |
| Without images | 146 |

---

## Environment

All configured on Vercel + `.env.local`:

```
GEMINI_API_KEY=AIzaSy...
NEXT_PUBLIC_CONVEX_URL=https://wary-gerbil-502.convex.cloud
CONVEX_DEPLOYMENT=dev:wary-gerbil-502
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
HUBSPOT_API_KEY=...
```

**Convex Dashboard:** https://dashboard.convex.dev/d/wary-gerbil-502

---

## Known Issues

1. **Local dev API key caching** - After changing `.env.local`, must delete `.next` folder and restart
2. **Clerk dev keys on production** - Need production keys before public launch
3. **146 curricula missing images** - Many sites block scraping or lack og:image

---

## What's Next

### Immediate
- [ ] Get production Clerk keys
- [ ] Manual image collection for top 50 curricula
- [ ] UI polish pass (green accent consistency)

### Phase 2: Enhanced Discovery
- [ ] "Reality Check" questions (prep time, budget)
- [ ] Neurodivergence screening
- [ ] Side-by-side comparison tool
- [ ] Per-subject recommendations (not just one box)

### Phase 3: Social & Sharing
- [ ] Shareable quiz results (image generation)
- [ ] Public review pages per curriculum
- [ ] Social sharing buttons

---

## Key Files

```
curriculove/
├── PROJECT.md                    # Full project doc
├── NOW.md                        # This file
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main app (quiz flow)
│   │   ├── browse/page.tsx       # Browse catalog
│   │   └── api/
│   │       ├── recommendations/  # Gemini matching
│   │       └── polish-review/    # Review polishing
│   ├── components/
│   │   ├── Quiz.tsx              # Quiz UI
│   │   ├── Results.tsx           # Philosophy breakdown
│   │   ├── Recommendations.tsx   # Swipe UI
│   │   ├── BrowseRecommendations.tsx  # Browse catalog
│   │   └── VoiceReview.tsx       # Voice capture
│   ├── lib/quiz-agent/
│   │   └── scoring.ts            # Deterministic engine
│   └── data/
│       └── curricula-convex.json # 216 curricula
├── convex/
│   ├── reviews.ts                # Review mutations
│   └── users.ts                  # User mutations
└── scripts/
    └── scrape-images.ts          # Image scraper (Playwright)
```

---

## To Resume

1. Read this NOW.md
2. Check production at https://curricu.love
3. For local dev: `npm run dev` (delete `.next` if API issues)
4. Deploy: `vercel --prod --yes`

---

## Session Log

### 2026-01-20

**Completed:**
- Deployed to Vercel production (curricu.love)
- Set up all Vercel env vars
- Created image scraper, got 70/216 images
- Moved "See Matching Curricula" CTA above the fold
- Built full browse page with search, filters, sort
- Updated Gemini API key (old was expired)

**Blockers resolved:**
- Gemini model name confusion (both `gemini-3-flash-preview` and `gemini-2.0-flash` work)
- Convex not configured on Vercel (added env vars)
- Local dev caching old API key (need to clear `.next`)
