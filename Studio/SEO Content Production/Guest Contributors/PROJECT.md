---
name: Guest Contributor Pipeline
description: Nearbound strategy - leverage trusted voices to publish on OpenEd
status: active
parent: SEO Content Production
created: 2026-01-01
updated: 2026-01-26
---

# Guest Contributor Pipeline

**Goal:** 20 pitches → 5+ published pieces (Q1-Q2 2026)

**Core Strategy:** The Charlie Ghostwriter Method - we do 80% of the work, they get the byline and a plug for their platform.

---

## Architecture

| System | Purpose | What Lives There |
|--------|---------|------------------|
| **Notion Database** | Tracking + Research | Status, warmth, waves, source material, article angles |
| **This Folder** | Templates + Workflow | Outreach templates, reusable frameworks, this PROJECT.md |
| **Nearbound Pipeline** | Contact Profiles | `Studio/Nearbound Pipeline/people/` - canonical contact info |

**Notion Database:** [Guest Contributor Pipeline](https://www.notion.so/2f4afe52ef5981bc8d7accc5e00e1a17)

---

## Current Status (see Notion for full pipeline)

| Wave | Count | Status |
|------|-------|--------|
| **Wave 1** | 6 | Ready to execute - outreach materials prepped |
| **Wave 2** | 5 | High-value warm leads from podcasts |
| **Wave 3** | 7 | Strategic targets needing topic discovery |
| **Wave 4** | 7 | Research needed |

**Active Wins:**
- Janssen Bradshaw - AGREED
- Justin Skycak - HOT LEAD (praised AI tutoring article)
- Michael Vilardo - TED talk transcript ready, pitch drafted

---

## The Protocol

### Phase 1: Source Gathering (in Notion page content)

**Checklist:**
- YouTube: Scrape channel/appearances with yt-dlp
- Podcast: Pull OpenEd episode transcript if exists
- Blog/Newsletter: Key articles
- Social: Best LinkedIn/X posts
- Books: Note key chapters

### Phase 2: SEO Topic Discovery

Use `/seo-research` skill:
1. Input expertise area + OpenEd audience keywords
2. Find gaps where their authority meets search intent
3. Prioritize: 500+ monthly volume, low-medium competition, parent intent

### Phase 3: Draft Creation

**The 80% Draft Rule:**
- Write in their voice (study their content)
- Include their frameworks/terminology
- Leave places for personal anecdotes
- Build in natural plug for their platform
- Make it something they'd be proud to share

**Quality Gate:** Run through `ghostwriter` skill before sending

### Phase 4: Pitch & Collaborate

**Templates in this folder:**
- `Outreach Templates/Initial_Pitch.md` - general pitch
- `Outreach Templates/Guest_Article_Pitch_Template.md` - article-specific pitch
- `Outreach Templates/Partner_Promo_Template.md` - promotional content template

**Example Implementation:**
- `Justin Skycak/README.md` - complete research + outreach email example

### Phase 5: Publish & Amplify

- Publish on OpenEd blog with full byline
- Create social assets via `newsletter-to-social`
- Notify contributor with share-ready posts
- Track referral traffic

---

## Skills to Chain

| Step | Skill |
|------|-------|
| SEO topic discovery | `seo-research` |
| YouTube transcript | `youtube-downloader` |
| Voice matching | `ghostwriter` + `human-writing` |
| Draft quality | `quality-loop` |
| Social amplification | `newsletter-to-social` |
| Article titles | `article-titles` |

---

## Folder Structure

```
Guest Contributors/
├── PROJECT.md              # This file
├── Outreach Templates/     # Reusable pitch templates
│   ├── Initial_Pitch.md
│   ├── Guest_Article_Pitch_Template.md
│   └── Partner_Promo_Template.md
├── Justin Skycak/          # Example of complete research + outreach
│   └── README.md
└── Archive/                # Old drafts, handoffs
```

---

## Notes

**On Controversial Topics:**
Not shying away from slightly controversial articles - education reform takes, school choice politics, disruption narratives.

**Notion Workflow:**
1. Check Notion for contributor status
2. Add source material and article angles to Notion page content
3. Use vault templates for outreach
4. Working drafts can live in Notion or Google Docs for collaboration
5. Final articles go to Webflow via normal publishing flow

---

*Last Updated: 2026-01-26*
