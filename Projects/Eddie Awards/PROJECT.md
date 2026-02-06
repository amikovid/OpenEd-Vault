---
name: The 2026 Eddy Awards
description: Open education's first major awards celebrating innovators in alternative learning
status: active
parent: OpenEd Vault
created: 2026-01-07
updated: 2026-02-05
---

# The 2026 Eddy Awards (The Eddys)

**Tagline:** Celebrating Innovation in Open Education

**Purpose:** Make others famous. Establish open education as a recognized category while positioning OpenEd as the authority celebrating its innovators. Expand nearbound reach through nominee and winner amplification.

**Target:** Complete winner announcements before Easter (April 20, 2026)

---

## The Vision

Combine the silly, self-aware goofiness of Ed (the OpenEd mascot) with the feel of a real honor. It should be fun but also something recipients genuinely want to display.

---

## Five Categories

### 1. Parent Educator of the Year
Honoring the parent or guardian who has built an innovative, comprehensive learning approach for their family—showcasing the art of blending resources, schedules, and methods into something transformative.

### 2. Innovator of the Year
Recognizing the teacher, tutor, microschool founder, or community organizer who is reimagining what instruction looks like outside traditional classrooms—whether through pods, online programs, co-ops, or local organizations that create impactful support networks for open education families.

### 3. Inspiring Student of the Year
Celebrating a young person whose educational journey exemplifies the power of personalized learning. This could be a student who has overcome challenges, pursued passions at an extraordinary level, started a business, or achieved something remarkable through an open education path. The emphasis is on inspiration—there are many ways to be inspiring.

### 4. Communicator of the Year
Honoring the YouTuber, podcaster, blogger, author, or social media creator who is making open education content accessible, engaging, and transformative for families exploring alternatives.

### 5. Open Education Resource of the Year
Recognizing a standout curriculum, tool, app, platform, or company that gives families more power and flexibility in how they educate. This could include learning platforms, educational startups, specific apps, video-based curricula, subscription boxes, or other innovative resources.

---

## Award Structure

- **Three nominees** announced per category
- Nominations from public submissions + internal selections
- **Panel of experts** selects winner from three nominees
- Winners receive:
  - Trophy (silver horse head with glasses—Ed in trophy form)
  - Gift card

---

## Timeline

| Week | Dates | Focus | Daily Content |
|------|-------|-------|---------------|
| -1 | Feb 10-14 | Internal Pre-Launch | Slack teaser, staff assets |
| 0-1 | Feb 17-28 | Hype & Awareness | Introduce Eddys, reveal categories |
| 2 | March 1-7 | Nominations | One category per weekday, call for nominations |
| 3 | March 8-14 | Nominees | Announce 3 nominees per category |
| 4 | March 15-21 | Winners | Announce winner per category |
| 5+ | March 22+ | Recap & Archive | Summary article, permanent page, trophy shipping |

---

## Branding

### Trophy Concept
Silver horse head with glasses—Ed in trophy form.
- Horse: Silver (like Oscar or Lombardi)
- Glasses: Black
- Base: Possibly book or educational symbol

### Visual Identity
- Sub-brand of OpenEd (own feel but clearly connected)
- "Brought to you by OpenEd" or "Powered by OpenEd"
- Primary color: Purple (or experiment)
- Tech-y, clean, crisp—think ed innovation
- Silver horse head with glasses badge in corner of all Eddy announcements

### Website Placement
- Landing page under OpenEd.com
- Consider: "What is Open Education" dropdown or standalone nav link
- Permanent archive page: `/eddy-awards` or `/the-eddys`

---

## Promotional Channels

### External
- **OpenEd Daily** (primary vehicle—content mapped to each campaign day)
- Social media (daily posts across all platforms)
- Nearbound emails to relevant contacts, nominees, partners
- Blog/website landing page

### Internal
- Slack channels (one week before public launch)
- Shareable assets for staff each week
- Emoji reactions to confirm participation
- Fresh assets provided each week

---

## Content Calendar

### Week 2: Nominations (March 1-7)
| Day | Category Focus |
|-----|----------------|
| Monday | Parent Educator of the Year |
| Tuesday | Innovator of the Year |
| Wednesday | Inspiring Student of the Year |
| Thursday | Communicator of the Year |
| Friday | Open Education Resource of the Year |

### Week 3: Nominees (March 8-14)
Same daily rotation—announce 3 nominees per category

### Week 4: Winners (March 15-21)
Same daily rotation—announce winner per category

---

## Potential Nominees to Consider

- Outschool
- Synthesis
- Claire Honeycutt
- Michael B. Horn
- Recess
- Alpha School
- Kiwi Crates

---

## Categories Tabled for Year 1

(Consider for future years)
- **Rising Voice in Open Education:** Someone new (<2 years) making waves
- **Lifetime Achievement in Educational Freedom:** Pioneers advancing alternative education for decades
- **Open Education Advocate of the Year:** Thought leaders, policy makers, organizers

---

## File Structure (To Build)

```
Eddie Awards/
├── PROJECT.md                  ← You are here
├── Branding/
│   ├── trophy-concepts/
│   ├── color-palette.md
│   └── badge-assets/
├── Categories/
│   ├── parent-educator.md
│   ├── innovator.md
│   ├── inspiring-student.md
│   ├── communicator.md
│   └── resource.md
├── Nominations/
│   ├── public-submissions/
│   └── internal-picks/
├── Content/
│   ├── week-1-hype/
│   ├── week-2-nominations/
│   ├── week-3-nominees/
│   ├── week-4-winners/
│   └── week-5-recap/
├── Website/
│   └── landing-page-copy.md
└── Outreach/
    ├── partner-emails/
    └── judging-panel/
```

---

## Key Decisions Made

- Five categories with consistent "of the Year" naming
- Three nominees per category (public + internal)
- Panel of experts selects winners
- Silver horse trophy with glasses (Ed the mascot)
- Sub-brand identity connected to OpenEd
- Five-week active campaign with daily content
- Permanent archive page on OpenEd website
- Complete before Easter (April 20, 2026)

---

## Next Steps

- [ ] Finalize branding/trophy design with Ella
- [ ] Build landing page
- [x] ~~Create nomination Google Form~~ → Nomination wizard built and deployed
- [ ] Draft internal Slack announcement
- [ ] Create Week 1 hype content
- [x] Assemble judging panel candidates - see Google Doc below
- [ ] Create shareable staff assets
- [ ] Finalize Week 2 nominations comms
- [ ] Embed/link nomination tool from Webflow landing page
- [ ] Test nomination flow on mobile

---

## Nomination Tool

**Live:** https://eddy-nominations.vercel.app
**Backend:** Convex (`festive-rook-937`)
**Source:** `~/project-temp/eddy-nominations/`

### Architecture
- Single-file HTML wizard (vanilla JS, no framework)
- Convex HTTP action at `https://festive-rook-937.convex.site/nominate`
- DM Sans font, coral-to-purple-to-blue gradient, Lucide-style SVG icons
- Mobile-first (100dvh, safe-area-insets, 44px touch targets)

### Flow
1. Welcome screen (trophy image)
2. Category selection (multi-select)
3. Per-category nomination forms (nominee name, email, description, category-specific fields)
4. Your Info (nominator details, newsletter subscribe)
5. Success screen with nominee notification (mailto: draft + copy message)

### Admin
- Convex Dashboard: https://dashboard.convex.dev/t/chdeist/eddy-nominations
- Query nominations: `nominations.list` (filter by category) or `nominations.count` (totals)

### Deployment
```bash
cd ~/project-temp/eddy-nominations
npx vercel --prod          # Frontend
npx convex deploy          # Backend (if schema changes)
```

---

## Working Documents

| Document | Location | Contents |
|----------|----------|----------|
| **Judge Selection & Outreach** | [Google Doc](https://docs.google.com/document/d/1jNCFz_fgTPkpWEzwPdn1GI4mfsRpUnxr9VSfsU2skJk/edit) | 27 potential judges by tier, personalized email templates |
| **Campaign Assets** | `Campaign Assets.md` | Landing page copy, form fields, Slack announcements, social templates |
| **Nominations Comms** | `Nominations-Comms.md` | Week 2 content: Facebook posts, Instagram options, newsletter draft |
| **Nomination Tool Source** | `~/project-temp/eddy-nominations/` | Convex backend + HTML wizard frontend |

---

*Created: 2026-01-07*
*Updated: 2026-02-05*
