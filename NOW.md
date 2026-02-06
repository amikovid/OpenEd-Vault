# OpenEd NOW

**Last Updated:** 2026-02-04

---

## Newsletter Batch Finalized - 2026-02-04

**6 newsletters finalized** from draft to publish-ready. Parents Know Best archived (superseded by Homeschool Data Gap).

| Edition | Date | Type | Subject | Status |
| --- | --- | --- | --- | --- |
| Scrolling Is The New Smoking | Jan 27 (Tue) | TTT + WOTD | "Why The Minimalists pulled their daughter out" | FINAL |
| Project-Based Learning | Jan 28 (Wed) | Deep Dive | "A practical guide to project-based learning" | FINAL |
| Joshua Fields Millburn | Jan 29 (Thu) | Deep Dive | "Why The Minimalists quit traditional school" | FINAL |
| Homeschool Data Gap | Feb 3 (Mon) | Meme + TTT | "The research says one thing. The headlines say another." | FINAL |
| Design Over Delivery | Feb 4 (Wed) | TTT | "Two courses, one platform, opposite outcomes" | FINAL |
| Gatto Deep Dive | Feb 5 (Thu) | Deep Dive | "He won Teacher of the Year. Then he quit." | FINAL |

**Per edition:** Newsletter_FINAL.md + social_spokes.md (5 posts: 2 LinkedIn, 2 X, 1 Instagram) = 30 social posts total

**Infographics (5):** HTML files ready to screenshot/export
- Homeschool performance data (bar chart, HSLDA stats)
- Screen time stats (3x depression, 40% sleep problems)
- Gatto's 7 Hidden Lessons (list format)
- PBL spectrum (Abstract to Applied)
- Printer cost comparison (inkjet vs ink tank vs laser)

**Nearbound profiles created:** Brett Pike (@ClassicLearner), Robert Enlow (@Robert_Enlow/EdChoice), Julie Bogart (@JulieBogart/Brave Writer)

**Open items:**
- [ ] JFM podcast episode URL placeholder `[PODCAST_LINK]` in Scrolling newsletter
- [ ] Design Over Delivery date: assigned to Feb 4 but calendar says Wednesday not Tuesday - verify intended send day

---

## Newsletter Voice - UPDATED 2026-02-04

**Status:** Hypothesis #5 executed. Pirate Wires examples replaced with Charlie's actual published newsletters.

**What changed:** The `opened-daily-newsletter-writer/SKILL.md` Voice Priming section now uses 5 real OpenEd Daily excerpts instead of 4 adapted Pirate Wires examples. Source material: Gatto Deep Dive, Homeschool Data Gap, Design Over Delivery, Printers segment.

**Why:** Pirate Wires is tech/politics snark; OpenEd Daily is education/parent authority. Same energy, different register. The LLM was imitating Pirate Wires rather than writing like Charlie. Using Charlie's own voice as the training set should fix the register mismatch.

**Next test:** Generate a newsletter draft with the updated skill and compare against v1-v5 of Design Over Delivery. The "Homeschool Data Gap" draft remains the voice target - it has the real rhythm, asides that interrupt thought, and "I just noticed this" energy.

**Reference files:** Pirate Wires techniques still available at `references/pirate-wires-segment-techniques.md` for technique reference (not voice priming).

---

## Vault Cleanup - COMPLETED 2026-02-04

**Full structural refactor of the OpenEd Vault.** Major changes:

### Folder Changes
- `Studio/Open Ed Podcasts/` → merged into `Studio/Podcast Studio/` (orphaned file moved, empty folder deleted)
- `Studio/Content Staging Pipeline/` → archived to `Studio/_archive/` (concepts absorbed into Social Media/PROJECT.md)
- `Studio/SEO Content Production/skill-sandbox/` → deleted (180MB of unused git clones, zero references)
- `Studio/Social Media/Comics/` → deleted (empty)
- `Studio/Nearbound Pipeline/scripts/` → deleted (empty)
- `Studio/Social Media/staging/drafts|ready|published/` → deleted (empty, never used)

### Agents Cleanup
- 12 files archived to `agents/_archived/` (5 superseded Webflow scripts, 5 test files, 1 debug script, 1 test config)
- Active agents: `webflow_sync.py`, `rss_curation.py`, `scrape_starred.py`, `social_post_scheduler.py`, `social_media_agent.py`, `content_multiplier.py`

### Newsletter Archive Rotation
- 10 daily newsletters (pre-2026-01-21) moved to `OpenEd Daily Studio/Archived/`
- 1 weekly newsletter moved to `OpenEd Weekly/_archive/`
- Active folders: 7 daily + 2 weekly

### Social Media Consolidation
- `Social Media/PROJECT.md` rewritten as unified hub (pipeline, platforms, approval, publishing)
- Content Staging Pipeline workflow absorbed into Social Media
- Frictionless Content Engine kept as subproject (Elijah's domain)
- `staging/README.md` simplified

### New Files Created
- `SKILLS_SCORECARD.md` - Audit of all 46 active + 13 archived skills with recommendations
- Newsletter frontmatter standardized across active drafts

### Documentation Updated
- `CLAUDE.md` - Fixed folder references (Open Ed Podcasts → Podcast Studio, OpenEd Daily → OpenEd Daily Studio)
- Newsletter voice skill upgraded with real examples

---

## RSS Curation Dashboard - NEW

**Status:** Working. Full triage-to-staging pipeline operational.

**Start:** `cd Projects/RSS-Curation && python3 serve_dashboard.py` → http://localhost:8000

**What we built this session:**
- Local Python server with warm sand/Notion theme dashboard
- Star/Used/Skip buttons that persist to `tracking.json`
- Reject-with-reason modal (feeds back into scoring prompt improvement)
- Clear Done button (removes processed items, keeps reject reasons)
- Staging folder: `Projects/RSS-Curation/staging/week-YYYY-MM-DD/`

**Files:**
- Dashboard: `Projects/RSS-Curation/serve_dashboard.py`
- Data: `Projects/RSS-Curation/tracking.json`
- Feeds: `.claude/skills/rss-curation/feeds.json` (47 feeds)
- Handoff: `.claude/skills/rss-curation/HANDOFF.md`
- Staging: `Projects/RSS-Curation/staging/week-2026-02-03/`

**Workflow:** Fetch feeds → Review in dashboard → Star keepers → Save → Claude reads tracking.json → Fetch articles to staging → Route to newsletter/social

**Playground preferences:** `.claude/references/playground-preferences.md` - warm sand theme + local server pattern (not dark theme, not copy/paste prompts). Apply to all future playgrounds.

**Pending:**
- [ ] Add playground preferences note to CLAUDE.md
- [ ] Automate fetching with launchd (daily 7am)
- [ ] After 5+ reject reasons, update scoring-prompt.md
- [ ] LinkedIn post for Michael Horn (drafted, not posted)

---

## QBR Action Items (2026-01-26)

**From Q2 QBR meeting - do not let slip:**

| Action | Owner | When | Status |
| --- | --- | --- | --- |
| Show Melissa Search Console integration | Charlie | Tomorrow (add to agenda) | ⏳ |
| Talk to Melissa about daily cadence | Charlie | Tomorrow | ⏳ |
| Set up Monday morning SEO report to Slack | Charlie | This week | ⏳ |
| Request Databox access from Alex | Charlie | This week | ⏳ |
| Align with Ela on Chavilah task allocation | Charlie + Ela | This week | ⏳ |
| Savvy Learning article → coordinate with Ela | Charlie | Before publish | ⏳ |

**Daily cadence decision pending:** Currently 3-4/week. Trade-off: More bandwidth vs. more nearbound at-bats. Discuss with Melissa tomorrow.

**YouTube ads research:** Complete research saved to `Studio/Analytics & Attribution/youtube-vs-meta-ads-research.md`. Recommendation: Test $1,500-2,000 over 8 weeks for fall enrollment.

---

## Guest Contributor Pipeline - ACTIVE

**Architecture:** Notion database + vault templates

- **Notion:** [Guest Contributor Pipeline](https://www.notion.so/2f4afe52ef5981bc8d7accc5e00e1a17) - tracking, source material, article angles

- **Vault:** `Studio/SEO Content Production/Guest Contributors/` - PROJECT.md, outreach templates, examples

### Wave 1 - Ready to Send

| Contact | Company | Topic | Status |
| --- | --- | --- | --- |
| Justin Skycak | Math Academy | Math acceleration | HOT LEAD - praised our AI tutoring article |
| Mason Pashia | Getting Smart | Marketplace data | Active convo Dec 2025, SEND EMAIL |
| Michael Vilardo | Subject.com | Netflix of high school | TED transcript + pitch ready, via Hollie |
| Janssen Bradshaw | Everyday Reading | Literacy/reading | AGREED - needs SEO topic |
| Matt Beaudreau | Apogee | Microschooling | Full Apogee blueprint in Notion |
| Savvy Learning founder | Savvy Learning | TBD | NEW - coordinate with Ela on partnership angle |

### Wave 2 - Warm Leads

| Contact | Company | Topic | Notes |
| --- | --- | --- | --- |
| Robin Smith | Surge Academy | Coding education | Highly engaged (5 replies) |
| Kathleen Ouellette | VictoryXR | VR education | Follow up needed |
| Jon England | Libertas | Microschool policy | Pitch drafted |
| Peter Gray | Self-Directed Ed |  | Podcast done |
| Michael Horn | Disruption |  | Gave book blurb |

**Full content in Notion:** Transcripts, source material, pitch emails, article angles for all Wave 1-2 contributors.

---

## Content Engine Refactor - ARCHIVED

**Archived to:** `Projects/_archive/_content-engine-refactor-archived-2026-01-29/`

All phases complete. Valuable parts moved:
- Sub-agent prompts → `.claude/skills/content-repurposer/references/sub-agents/`
- Architecture map → `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md`

### What Was Done

**New Skills Created:**

- `newsletter-to-social` - Router for hub-to-spoke workflow

- `archive-suggest` - Daily suggestions from content archive

- `slack-social-distribution` - Post to #market-daily as threads

- `newsletter-subject-lines` - Dedicated subject line skill (split from hook-writing)

- `article-titles` - SEO-focused headline skill (split from hook-writing)

- `work-summary` - Translate git commits to Slack-friendly updates

**Skills Refactored (8,400 words removed):**

| Skill | Reduction |
| --- | --- |
| ghostwriter | 64% |
| meta-ads-creative | 63% |
| cold-open-creator | 61% |
| hook-and-headline-writing | 59% (then split) |
| opened-daily-newsletter-writer | 37% |
| podcast-production | 29% |

**Architecture Documented:**

- `SKILL_ARCHITECTURE_MAP.md` - Visual map of entire content engine

- "Examples Over Instructions" philosophy added to skill-creator

- Fixed 7 broken skill references

**Infrastructure:**

- Work summaries folder: `.claude/work-summaries/`

- Nearbound profiles: 8 updated with social handles

### Next Session Approach

**Test skills through actual workflows** rather than isolated audits:

- Run a newsletter → social spoke workflow

- Run a podcast clip extraction

- Note friction points in real use

---

## SEO Comparison Articles - ACTIVE

**New initiative (2026-01-29):** Pedagogy comparison SEO strategy.

**Master keyword list:** `Studio/SEO Content Production/Open Education Hub/Deep Dive Studio/PEDAGOGY_COMPARISON_KEYWORDS.md`

| Article | Volume | Status | Notes |
| --- | --- | --- | --- |
| Waldorf vs Montessori | 2,900/mo | ✅ Ready to publish | Passed 5-judge quality loop |
| Montessori vs Reggio Emilia | 1,900/mo | 📋 Brief created | Next priority |
| Khan Academy vs IXL | 590/mo | 📋 Queued | Ed-tech comparison |
| Unschooling vs Homeschooling | 320/mo | 📋 Queued | Strong OpenEd angle |

**Production cadence:** 2 articles/week using established template.

---

## Active Projects (Studio/)

| Project | Location | Status | Priority |
| --- | --- | --- | --- |
| Lead Magnet | Lead Magnet Project/PROJECT.md | Active dev (curriculove) | HIGH |
| Meta Ads | Meta Ads/PROJECT.md | 100 concepts ready | HIGH |
| SEO Content | SEO Content Production/PROJECT.md | Comparison series active | HIGH |
| Eddie Awards | Eddie Awards/PROJECT.md | Website planning | MEDIUM |
| KPI Discussions | KPI Discussions/PROJECT.md | Q1 bonus planning | MEDIUM |
| Social Media | Social Media/FORMAT_INVENTORY.md | Format inventory done | LOW |
| Project Dandelion | Project-Dandelion/PROJECT.md | Active | HIGH |
| ↳ Retargeting | Project-Dandelion/retargeting-strategy/ | Pillar 1 Feb 16 | HIGH |

### Ongoing Workflows

| Workflow | Location | Cadence |
| --- | --- | --- |
| OpenEd Daily | OpenEd Daily Studio/ | Mon-Thu |
| Podcasts | Podcast Studio/ | Weekly |
| Open Education Hub | Open Education Hub/ | As needed |

---

## Blocked Items

- **GSC Access** - Need ops to add service account for SEO quick wins

  - Account: `opened-service-account@gen-lang-client-0217199859.iam.gserviceaccount.com`

---

## Key Dates (Q3)

| Date | Event | Impact |
| --- | --- | --- |
| Feb 10 | Enrollment tasks open | Interest → Application conversion focus |
| Feb 16 | Retargeting Pillar 1 launch | 4-6 ad variations needed |
| Q3 | 4 new states launching | State pages become critical path |
| Fall 2026 | Enrollment cycle | YouTube ads test window |

---

---

## API Access

| Service | Status | Notes |
| --- | --- | --- |
| Slack | ✅ | xoxc/xoxd tokens |
| Notion | ✅ | ntn_* token |
| DataForSEO | ✅ | Keyword research |
| GSC | ⚠️ | Service account pending |
| GA4 | ✅ | Analytics access |
| GetLate | ✅ | 8 platforms connected |
| Gemini | ✅ | gemini-3-flash-preview |

---

*Update this file at session end. For project context, see PROJECT.md in each Studio folder.*