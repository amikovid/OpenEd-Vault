# Curriculove: Product Specification

**Vision:** A curriculum discovery and review platform that captures emails for OpenEd and builds a crowdsourced review corpus that makes the platform increasingly valuable.

**Domain:** curricula.love
**Owner:** OpenEd (internal tool, not standalone business)

---

## The Real Goal

Curriculove serves OpenEd's mission by:

1. **Capturing emails** → Feeds OpenEd's marketing funnel
2. **Collecting authentic reviews** → Builds irreplaceable content moat
3. **Promoting OpenEd partners** → Curricula that give OpenEd exposure get featured
4. **Driving program awareness** → "This is FREE through OpenEd in your state"

**We are not trying to monetize Curriculove directly.** OpenEd makes money from the program. Curriculove exists to:
- Grow the email list
- Generate review content
- Build community
- Increase program sign-ups

---

## What Actually Matters

### Primary Metrics
| Metric | Why It Matters |
|--------|----------------|
| **Email capture rate** | Direct funnel to OpenEd |
| **Reviews submitted** | Content moat, SEO value |
| **Review quality** | Useful to other parents |
| **Program sign-ups** | Revenue driver |

### Secondary Metrics
| Metric | Why It Matters |
|--------|----------------|
| Quiz completion | Leads to email capture |
| Return visits | More reviews, engagement |
| Referrals | Organic growth |

### Metrics We Don't Care About
- Swipes per session
- Like rate
- Time on site
- Premium conversions (no premium tier)

---

## User Journey

### Phase 1: Hook & Capture (MVP Priority)
```
Landing → Quick Philosophy Quiz → EMAIL GATE → Results + Recommendations
```

**Key insight:** Get email BEFORE showing full results. Tease the philosophy match, gate the curriculum recommendations.

- Quiz: 5-8 questions max (not 15)
- Email gate: "See your matched curricula" as the CTA
- Capture: email + state (for OpenEd eligibility)
- HubSpot: Tag with philosophy for nurture sequences

### Phase 2: Discovery & Engagement
```
Swipe Curricula → Save Favorites → See OpenEd Partner Benefits
```

- Swipe through matched curricula
- OpenEd partners get prominent "FREE through OpenEd" badges
- Periodic reminders: "You can access X for free in [state]"

### Phase 3: Review Collection (The Real Value)
```
"Have you tried this?" → Voice Review → AI Polish → Approve & Submit
```

- After liking a curriculum: "Have you used this?"
- If yes: Voice-to-text review capture
- AI polishes the rambling into a diplomatic, structured review
- User approves/edits before publishing
- Gamification: Status badges for prolific reviewers

### Phase 4: Community (Future)
```
Find Homeschool Families Near You → Local Groups → Meetups
```

- Location-based matching
- Philosophy-based matching
- Local homeschool group discovery
- This is far future - requires critical mass first

---

## Email Capture Strategy

### Current Flow (Too Late)
```
Quiz → Results → Recommendations → Email Gate → ???
```
Email comes after they've already gotten value. Low capture rate.

### Proposed Flow (Earlier Gate)
```
Quiz → Philosophy Teaser → EMAIL GATE → Full Results + Recommendations
```

**Teaser screen:**
> "You're a **Charlotte Mason** homeschooler!"
>
> *Enter your email to see your full profile and matched curricula*
>
> [Email input] [State dropdown]
> [See My Matches]

This gates the valuable content (full results + curriculum cards) behind email.

### Email Value Props
- "Get your personalized curriculum matches"
- "See which curricula are FREE through OpenEd in [state]"
- "Receive weekly curriculum tips based on your philosophy"

---

## Review System Architecture

### Voice-to-Text Flow
```
1. User taps "Leave a Review"
2. Prompt: "Tell us about your experience with [Curriculum]"
3. User speaks (Web Speech API)
4. Raw transcript captured
5. AI (Gemini) polishes into structured review
6. User sees polished version, can edit
7. User approves → Review saved
```

### AI Polish Prompt
```
You're helping a parent write a curriculum review. They spoke this:

"{raw_transcript}"

Transform this into a helpful, diplomatic review with:
- Overall impression (1-2 sentences)
- What worked well
- What could be better
- Who this curriculum is best for

Keep their authentic voice. Don't add information they didn't mention.
Remove filler words and false starts. Make it readable.

Return JSON:
{
  "polished_review": "...",
  "rating_suggestion": 4,
  "highlights": ["living books", "nature study"],
  "concerns": ["prep time heavy"]
}
```

### Review Data Model
```typescript
interface Review {
  id: string;
  curriculumSlug: string;
  userId: string;

  // Content
  rawTranscript?: string;      // Original voice input
  polishedReview: string;      // AI-cleaned version
  userEditedReview?: string;   // If they modified it
  rating: 1 | 2 | 3 | 4 | 5;

  // Structured data (AI-extracted)
  highlights: string[];
  concerns: string[];
  bestFor: string[];           // "visual learners", "large families"

  // Context
  yearsUsed: string;           // "1 year", "2+ years"
  gradesUsed: string[];        // ["3rd", "4th"]
  childCount: number;

  // Meta
  isVerified: boolean;         // Did they prove purchase?
  helpfulVotes: number;
  createdAt: Date;
}
```

### Gamification / Status
| Status | Requirement |
|--------|-------------|
| **Newcomer** | 0 reviews |
| **Contributor** | 1-2 reviews |
| **Reviewer** | 3-5 reviews |
| **Expert** | 6-10 reviews |
| **Community Pillar** | 11+ reviews |

Badges visible on profile and reviews. Maybe small perks for top reviewers (early access to new features, featured on homepage).

---

## OpenEd Integration

### Partner Curriculum Benefits
Curricula that partner with OpenEd (give program exposure) receive:
- "FREE through OpenEd" badge on card
- Priority placement in recommendations
- Featured in "Staff Picks" sections
- Highlighted in email nurture sequences

### State Eligibility
OpenEd operates in: AR, IN, IA, KS, MN, MT, NV, OR, UT

When user enters state:
- If eligible: "Great news! You can access [X] curricula for FREE through OpenEd"
- Show eligibility badge on partner curricula
- CTA: "Learn about the OpenEd program" → opened.co

### Integration Points
- HubSpot: Philosophy tags, state, review count
- OpenEd website: Link to program application
- Retargeting: Users who engage but don't sign up

---

## MVP Scope (v1.0 for Colleagues)

### Must Have
- [ ] Philosophy quiz (5-8 questions)
- [ ] Email capture gate (before full results)
- [ ] Philosophy results page
- [ ] Curriculum swipe interface (all matched curricula)
- [ ] OpenEd partner badges ("FREE through OpenEd")
- [ ] Save favorites locally (IndexedDB)
- [ ] Basic review submission (text input)
- [ ] Deploy to curricula.love

### Should Have
- [ ] Voice-to-text review input
- [ ] AI review polishing
- [ ] Review display on curriculum cards
- [ ] State-based eligibility messaging
- [ ] HubSpot integration working

### Nice to Have
- [ ] User accounts (beyond email)
- [ ] Review editing/approval flow
- [ ] Reviewer status badges
- [ ] Share results on social

### Not in MVP
- [ ] Find families near you
- [ ] Premium features
- [ ] Native mobile app
- [ ] Real-time sync across devices

---

## Technical Architecture (Minimal)

### Frontend
- **Next.js 15** - App Router, React Server Components
- **Tailwind CSS v4** - Styling
- **IndexedDB** - Local persistence (no account required)
- **Web Speech API** - Voice input for reviews

### Backend
- **Next.js API Routes** - Simple, no separate backend
- **Convex** - Reviews, user data, real-time (when needed)
- **HubSpot** - Email capture, marketing automation
- **Gemini API** - Review polishing, recommendations

### Data Flow
```
Quiz → Local State → Email Gate → HubSpot
                                → Convex (if review)
                                → Local IndexedDB (favorites)
```

### Hosting
- **Vercel** - Next.js hosting, automatic deploys
- **Domain** - curricula.love → Vercel

---

## Deployment Checklist (curricula.love)

### Before Launch
- [ ] Domain DNS configured to Vercel
- [ ] Environment variables set (Gemini, HubSpot)
- [ ] HubSpot properties created (philosophy, state)
- [ ] Test email capture flow
- [ ] Test on mobile devices
- [ ] OpenGraph meta tags for sharing

### After Launch
- [ ] Monitor HubSpot captures
- [ ] Gather colleague feedback
- [ ] Track quiz completion rate
- [ ] Iterate on email capture conversion

---

## Content Strategy

### Review Corpus Value
Every review collected is:
- **SEO content** - Unique, user-generated, keyword-rich
- **Trust signal** - Real parent experiences
- **Moat** - Competitors can't easily replicate
- **AI training data** - Better recommendations over time

### Target: 1000 Reviews
At 1000 quality reviews across 200 curricula:
- Average 5 reviews per curriculum
- Credible, useful resource for parents
- Strong SEO foundation
- Network effects kick in (people come to read AND write)

---

## Questions to Resolve

1. **Account system**: Email-only or full auth?
   - Email-only is simpler for MVP
   - Full auth enables cross-device, richer profiles

2. **Review verification**: How to confirm they actually used it?
   - Honor system for MVP
   - Future: Receipt upload, purchase verification

3. **Moderation**: How to handle bad reviews?
   - AI filter for spam/abuse
   - Flag system for community moderation

4. **Curriculum data updates**: How to keep current?
   - Manual for now
   - Future: Vendor portal for updates

---

*Last Updated: 2026-01-13*
