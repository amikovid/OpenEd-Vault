# OpenEd NOW

**Last Updated:** 2026-01-26

---

## QBR Action Items (2026-01-26)

**From Q2 QBR meeting - do not let slip:**

| Action | Owner | When | Status |
|--------|-------|------|--------|
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
|---------|---------|-------|--------|
| **Justin Skycak** | Math Academy | Math acceleration | HOT LEAD - praised our AI tutoring article |
| **Mason Pashia** | Getting Smart | Marketplace data | Active convo Dec 2025, SEND EMAIL |
| **Michael Vilardo** | Subject.com | Netflix of high school | TED transcript + pitch ready, via Hollie |
| **Janssen Bradshaw** | Everyday Reading | Literacy/reading | AGREED - needs SEO topic |
| **Matt Beaudreau** | Apogee | Microschooling | Full Apogee blueprint in Notion |
| **Savvy Learning founder** | Savvy Learning | TBD | NEW - coordinate with Ela on partnership angle |

### Wave 2 - Warm Leads
| Contact | Company | Topic | Notes |
|---------|---------|-------|-------|
| Robin Smith | Surge Academy | Coding education | Highly engaged (5 replies) |
| Kathleen Ouellette | VictoryXR | VR education | Follow up needed |
| Jon England | Libertas | Microschool policy | Pitch drafted |
| Peter Gray | Self-Directed Ed | | Podcast done |
| Michael Horn | Disruption | | Gave book blurb |

**Full content in Notion:** Transcripts, source material, pitch emails, article angles for all Wave 1-2 contributors.

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

## Key Dates (Q3)

| Date | Event | Impact |
|------|-------|--------|
| **Feb 10** | Enrollment tasks open | Interest → Application conversion focus |
| **Feb 16** | Retargeting Pillar 1 launch | 4-6 ad variations needed |
| **Q3** | 4 new states launching | State pages become critical path |
| **Fall 2026** | Enrollment cycle | YouTube ads test window |

---

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
