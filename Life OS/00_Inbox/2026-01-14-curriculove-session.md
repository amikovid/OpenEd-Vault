---
type: session-summary
date: 2026-01-14
projects: [curriculove]
---

# Curriculove Session - Jan 14

## Done
- Voice-to-text reviews (Web Speech API + Gemini polish)
- Convex storage for reviews and user profiles
- Clerk authentication (optional - works anonymously)
- `/browse` page to skip quiz and explore all curricula
- iOS app icon (risograph style, OpenEd brackets + heart)

## Ship Blockers
- [ ] Fix branding: "Curriculove" vs "Curricu.love"
- [ ] Fix double API fetch in recommendations
- [ ] Add UserButton to main quiz flow

## Polish Before Launch
- [ ] Remove "Coming Soon" section in Profile
- [ ] Add visual feedback when saving favorites

## Notes
- Domain is **curricu.love** (not curricula.love)
- Keep current "Pinterest cute" aesthetic
- App icon uses risograph style but app doesn't need to match
- Convex dashboard: https://dashboard.convex.dev/d/precise-rooster-565

## Run Commands
```bash
cd "Studio/Lead Magnet Project/curriculove"
npx convex dev  # Keep running
npm run dev     # Dev server
```

[[Studio/Lead Magnet Project/curriculove/PRODUCT-SPEC]]
