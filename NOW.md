# OpenEd NOW

**Last Updated:** 2026-01-23

---

## Session: Content Engine Refactor Phase 9 (2026-01-23)

### Content Engine Refactor - Phase 9 IN PROGRESS

**Project folder:** `Studio/_content-engine-refactor/`

**Phases 0-8 complete.** Phase 9 = Skills Audit & Refactoring.

#### Skills Audit Complete (5 Batches)

| Batch | Skills | Key Findings |
|-------|--------|--------------|
| 1: Core Content | text-content, newsletter-writer, quality-loop, podcast, newsletter-to-social | 2 bloated (newsletter 2,852w, podcast 2,701w) |
| 2: Social/Video | short-form-video, video-caption, x-posting, x-article-converter, meta-ads | meta-ads bloated (2,880w), x-posting exemplary |
| 3: Writing/Voice | ghostwriter, human-writing, ai-tells, hook-writing, opened-identity | ghostwriter (3,302w), hook-writing (3,542w) bloated |
| 4: Brand/SEO | seo-research, deep-dives, weekly-newsletter, transcript-polisher, cold-open | cold-open (2,517w), weekly (2,194w) over target |
| 5: Utility | image-prompt, skill-creator, gemini-writer, youtube-title, youtube-clip | youtube-title has 6 broken refs, gemini-writer exemplary (911w) |

#### Skills Over 2,000 Word Target

| Skill | Words | Priority |
|-------|-------|----------|
| hook-and-headline-writing | 3,542 | High |
| ghostwriter | 3,302 | High |
| meta-ads-creative | 2,880 | Medium |
| opened-daily-newsletter-writer | 2,852 | High (in progress) |
| podcast-production | 2,701 | Medium |
| cold-open-creator | 2,517 | Medium |

#### Completed Actions
- [x] Renamed `quality-loop/skill.md` → `SKILL.md`
- [x] Nearbound enrichment: 8 profiles updated with social handles
- [x] Identified `human-writing copy` duplicate folder for deletion

#### Refactoring Complete (All High/Medium Priority)

| Skill | Before | After | Reduction |
|-------|--------|-------|-----------|
| opened-daily-newsletter-writer | 2,852 | 1,803 | 37% |
| ghostwriter | 3,302 | 1,185 | 64% |
| hook-and-headline-writing | 3,542 | 1,445 | 59% |
| meta-ads-creative | 2,880 | 1,062 | 63% |
| podcast-production | 2,701 | 1,924 | 29% |
| cold-open-creator | 2,517 | 982 | 61% |

**Total:** ~8,400 words removed across 6 skills

#### Remaining (Low Priority)
- youtube-clip-extractor (2,252w) - ✅ broken refs fixed
- youtube-title-creator (2,216w) - has 6 broken refs
- opened-weekly-newsletter-writer (2,194w)

#### Phase 11: Skill Architecture Map (Complete - 2026-01-23)

Created comprehensive visual documentation: `Studio/_content-engine-refactor/SKILL_ARCHITECTURE_MAP.md`

**Included:**
- Master flow diagram (Source → Context Loading → Snippet Extraction → Framework Fitting → Quality Gate → Output)
- Hub-specific chains: Podcast (4 checkpoints), Newsletter (TTT → Quality → Spokes), Deep Dive
- Video content skill chain with Triple Word Score
- Skill dependency matrix
- Platform-specific quick reference
- Identified gaps for future work

**Fixes applied:**
- `youtube-clip-extractor`: Fixed 2 broken references (`social-content-creation` → `text-content`, removed archived `hook-and-headline-writing`)
- `video-caption-creation`: Fixed 4 broken references
- `youtube-downloader`: Fixed frontmatter name mismatch

**Philosophy documented in skill-creator:**
- "Examples Over Instructions" - One output example worth a thousand words of instructions
- Skills should be example-heavy, instruction-light

#### Phase 10: Hook/Headline Skill Split (Complete)

Split `hook-and-headline-writing` into skills + references:

| Asset | Type | Purpose |
|-------|------|---------|
| `newsletter-subject-lines` | Skill | Subject lines for newsletters |
| `article-titles` | Skill | Blog posts, deep dives (formal/journalistic) |
| `segment-titles.md` | Reference | In daily-newsletter skill (1-6 words) |
| `witty-voice-patterns.md` | Reference | Pirate Wires-inspired wit for newsletters |
| `opening-letter-patterns.md` | Reference | 12+ real examples with analysis + substance→take pattern |
| `pirate-wires-segment-techniques.md` | Reference | A la carte Pirate Wires techniques for TTT segments (7 techniques, full excerpts) |

**Key:** Pirate Wires wit = newsletter voice (opening letters, segments), not article titles. Articles are more formal/journalistic.

**Substance → Take Pattern:** The core rhythm of OpenEd Daily prose. Alternate between facts/quotes/data (substance) and interpretation/what it means (take). This creates prose that feels both informed and opinionated.

#### Phase 10b: Archived Reference Restoration (Complete)

Restored valuable archived content that was lost during refactoring:

**article-titles/references/** (3 files restored):
- `headline-formulas-library.md` - 15 headline formulas with OpenEd examples (682 lines)
- `10-commandments-checklist.md` - Full evaluation framework with scoring (891 lines)
- `sticky-sentence-techniques.md` - 5 techniques with OpenEd bank (571 lines)

**newsletter-subject-lines/references/** (3 files restored):
- `newsletter-subject-lines-analyzed.md` - Real OpenEd examples with 10 Commandments scoring (404 lines)
- `10-commandments-checklist.md` - Condensed for subject lines (297 lines)
- `sticky-sentence-techniques.md` - Condensed for subject lines (173 lines)

**SKILL.md updates:** Both skills now have:
- 3-phase workflow (identify → generate → evaluate)
- References to restored materials
- 10 Commandments quick reference
- Quality checklists
- Bundled resources table

#### Decisions Made
- **ai-tells vs human-writing:** Keep separate. ai-tells = constraint layer (what NOT to do), human-writing = Charlie's personal voice patterns.
- **human-writing location:** Should move to OpenEd Vault (colleagues need access)
- **Socials-first approach:** Insert framework-fitting check early in angle development
- **Content engine skill design:** Examples do heavy lifting, no prescriptive scoring

#### Folder Reorganization Needed
- `Content/Master Content Database/` → Rename to "Published Content Database"
- `Master_Content_Index.md` → Move from `.claude/references/` to live with content it indexes
- **Principle:** Indexes should live with the content they reference

---

## Previous Session: Vault Audit (2026-01-15)

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

**Full visual map:** `Studio/_content-engine-refactor/SKILL_ARCHITECTURE_MAP.md`

| Content Type | Primary Skill | Notes |
|--------------|---------------|-------|
| **Text posts** | `text-content` | 360+ templates, platform routing |
| **Short-form video** | `short-form-video` | Production workflow |
| **Video hooks** | `video-caption-creation` | Triple Word Score system |
| **Podcast** | `podcast-production` | Full episode workflow |
| **Newsletter** | `opened-daily-newsletter-writer` | Mon-Thu format |
| **Subject lines** | `newsletter-subject-lines` | 10 Commandments + 15 formulas |
| **Article titles** | `article-titles` | SEO-focused, journalistic |
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
