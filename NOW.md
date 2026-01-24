# OpenEd NOW

**Last Updated:** 2026-01-23

---

## Content Engine Refactor - COMPLETE

**Project folder:** `Studio/_content-engine-refactor/`

All phases complete. The content engine is now documented and streamlined.

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
|-------|-----------|
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

*Update this file at session end. For project context, see PROJECT.md in each Studio folder.*
