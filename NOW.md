# OpenEd NOW

**Last Updated:** 2026-01-15

---

## Session: Vault Audit (2026-01-15)

### Cruft Cleaned
- Deleted `quality-loop copy` and `quality-loop2` (duplicate skills)
- Deleted `OpenEd Daily.zip` (stale backup)
- Deleted `4dc9011b086c410392982e6bbf2940ef/` UUID folder in podcasts
- Deleted `Untitled.md` orphans in archived podcasts

### New Asset Created
**`Studio/Social Media/FORMAT_INVENTORY.md`** - Unified format inventory combining:
- Andrew Muto video formats (Tier 1-4 evaluation)
- Content concepts text patterns (formerly X_Post_Batch_Review)
- User feedback preferences (reject correlatives, like stats+one-liners)
- Decision trees for format selection
- Daily production targets (2 videos + 2 text posts)

### Remaining " 1" Podcast Folders
Left in place - contain unique content, not duplicates:
- `Corey DeAngelis 1/`
- `Kade Hinkle... 1/`
- `Michael Gibson 1/`

### Meta Ads UUID Files
50+ files with Notion UUID suffixes remain in `Ad Creative Concepts/`. Too many to rename safely; content is valid.

---

## Current Focus

### Content Concepts Calibration - AWAITING FEEDBACK
105 content concepts generated with inline feedback patterns applied.

**File:** `Studio/Social Media/staging/Content_Concepts.md` (moved from X_Post_Batch_Review.md)

**User Feedback Patterns (apply to all future posts):**
- REJECT: Correlative constructions ("X isn't Y - it's Z")
- REJECT: Soft/preachy endings
- REJECT: Tired openers ("Hot take:", "Unpopular opinion:", "Genuine question:")
- LIKE: Stats + provocative one-liner
- LIKE: Visual concepts (cartoons, graphs, reels)
- ADD: Alternating caps for mocking ("bUt WhAt AbOuT...")

---

## Active Projects (Studio/)

| Project | Location | Status | Priority |
|---------|----------|--------|----------|
| **Lead Magnet** | `Lead Magnet Project/PROJECT.md` | Active dev (curriculove) | HIGH |
| **Meta Ads** | `Meta Ads/PROJECT.md` | 100 concepts ready | HIGH |
| **SEO Content** | `SEO Content Production/PROJECT.md` | PBL article complete | MEDIUM |
| **Eddie Awards** | `Eddie Awards/PROJECT.md` | Website planning | MEDIUM |
| **KPI Discussions** | `KPI Discussions/PROJECT.md` | Q1 bonus planning | MEDIUM |
| **Social Media** | `Social Media/FORMAT_INVENTORY.md` | Format inventory done | LOW |
| **Retargeting** | `Retargeting Strategy FY26-27/PROJECT.md` | Planning | LOW |

### Ongoing Workflows
| Workflow | Location | Cadence |
|----------|----------|---------|
| **OpenEd Daily** | `OpenEd Daily/` | Mon-Thu |
| **Podcasts** | `Open Ed Podcasts/` | Weekly |
| **Open Education Hub** | `Open Education Hub/` | As needed |

---

## Blocked Items

- **GSC Access** - Need ops to add service account for SEO quick wins
  - Account: `opened-service-account@gen-lang-client-0217199859.iam.gserviceaccount.com`

---

## Guest Contributor Pipeline - READY TO SEND

| Contact | Company | Topic | Status |
|---------|---------|-------|--------|
| Mason Pashia | Getting Smart | Marketplace data | Ready |
| Kathleen Ouellette | VictoryXR | VR education | Ready |
| Robin Smith | Surge Academy | Coding/game design | Ready |
| Jon England | Libertas Institute | Microschools | Ready |

**Drafts:** `Studio/SEO Content Production/Guest Contributors/Drafts/`

---

## Folder Structure

```
OpenEd Vault/
├── CLAUDE.md                    # Navigation + writing rules
├── NOW.md                       # This file - living handoff
├── Master_Content_Index.md      # 406 published pieces indexed
│
├── Studio/                      # Active projects + workflows
│   ├── Eddie Awards/PROJECT.md
│   ├── Meta Ads/PROJECT.md
│   ├── SEO Content Production/PROJECT.md
│   ├── Lead Magnet Project/curriculove/    # Next.js app
│   ├── Retargeting Strategy FY26-27/PROJECT.md
│   ├── KPI Discussions/PROJECT.md
│   ├── Social Media/FORMAT_INVENTORY.md    # Unified format guide
│   ├── Social Media/staging/Content_Concepts.md  # 105 concepts awaiting review
│   ├── OpenEd Daily/                       # Workflow
│   ├── Open Ed Podcasts/                   # Workflow
│   ├── Open Education Hub/                 # Workflow
│   └── _archive/                           # Archived projects
│
├── Content/Master Content Database/        # Published archive
├── CRM/                                    # 382 contacts
├── Archive/                                # Historical content
│   └── Andrew Muto/                        # Gold: 40+ video formats
│
└── .claude/
    ├── skills/          # 39 active skills (cleaned 2 duplicates)
    ├── references/      # SEO commands, program details, etc.
    └── sessions/        # Historical handoffs
```

---

## Skills Architecture

| Content Type | Primary Skill | Notes |
|--------------|---------------|-------|
| **Text posts** | `text-content` | 360+ templates, platform routing |
| **Short-form video** | `short-form-video` | Production workflow |
| **Video hooks** | `video-caption-creation` | Triple Word Score system |
| **Podcast** | `podcast-production` | Full episode workflow |
| **Newsletter** | `opened-daily-newsletter-writer` | Mon-Thu format |
| **SEO content** | `seo-content-writer` | Hub page optimization |
| **Deep dives** | `open-education-hub-deep-dives` | Quality-loop integration |
| **Quality control** | `quality-loop` | 5-judge system |
| **AI image gen** | `image-prompt-generator` | Nano Banana Pro |

---

## API Access

| Service | Status | Notes |
|---------|--------|-------|
| Slack | ✅ | xoxc/xoxd tokens |
| Notion | ✅ | ntn_* token |
| DataForSEO | ✅ | Keyword research |
| GSC | ⚠️ | Service account pending |
| GA4 | ✅ | Analytics access |
| GetLate | ✅ | 8 platforms connected |
| Gemini | ✅ | gemini-3-flash-preview |

---

## High Engagement Contacts

| Contact | Company | Opportunity |
|---------|---------|-------------|
| Sara Jean Kwapien | Outschool | Pitch article |
| Ryhen Miller-Hollis | Education Reimagined | Reciprocal blog |
| The Good and the Beautiful | - | Major curriculum brand |
| Rainbow Resource | - | Largest retailer |

---

*Update this file at session end. For project context, see PROJECT.md in each Studio folder.*
