# Session Handoff: SEO Content Production Deep Dive

**Date:** 2026-01-08 (Updated 2026-01-08 PM)
**Duration:** ~3+ hours total
**Focus:** SEO Content Production infrastructure, API connections, template creation, content drafts

---

## Session 2 Update (Jan 8 PM)

### Completed This Session
1. **Studio folder cleanup**
   - Moved `philosophy_quiz_prototype.py` and `test_adaptive_quiz.py` → `Lead Magnet Project/`
   - Archived temp scripts → `Studio/_archive/temp-scripts/`
   - Moved `weekly-seo-report.md` → `SEO Content Production/`

2. **Utah State Page Created**
   - `State Pages/Utah/source-material.md` - Legal info, local resources, parent quotes
   - `State Pages/Utah/draft-v1.md` - Complete draft (~250 lines)
   - Features Utah Fits All vs OpenEd comparison
   - Rich local resources: Nature Kids Connect, Apogee Utah, Breakout School, etc.

3. **Versus Pages Status**
   - Oregon draft-v1: Complete (301 lines)
   - IXL vs Exact Path draft-v2: Complete, tightened (135 lines)
   - Saxon vs Math-U-See: Still v1, needs tightening
   - Khan vs IXL: Still v1, needs tightening

### Still Blocked
- **Fellow MCP** - Needs API key + subdomain from Fellow settings (developer access)
- **GSC** - Needs ops to add service account

### Next Session Priorities
1. Tighten Saxon vs Math-U-See (apply v2 style)
2. Tighten Khan vs IXL (apply v2 style)
3. Nevada state page (Q1 priority)
4. If Fellow access obtained: configure MCP

---

## Original Session (Jan 8 AM)

---

## TL;DR

Built the foundation for scalable SEO content production:
- Created State Pages and Versus templates with quality gates
- Connected Slack API (working) and Notion API (working)
- Extracted Fred's methodology from meeting notes
- Identified 9 operating states from program guide
- Found 247+ curriculum discussions in Slack #recommendations

---

## What Was Built

### 1. State Pages Sub-Project
**Location:** `Studio/SEO Content Production/State Pages/PROJECT.md`

**Template includes:**
- Legal nuance guidance (OpenEd families ≠ homeschoolers legally, but identify as such)
- Dual search intent: "how to homeschool in X" + "homeschool program in X"
- Competitor structure (HSLDA documented)
- Quality gates to avoid duplicate content
- Internal linking strategy to Grade Level Guides

**Operating States (9 total):**
| State | Priority | Notes |
|-------|----------|-------|
| Oregon | Q1 High | 3rd highest traffic, growth target |
| Nevada | Q1 High | New launch |
| Indiana | Q1 High | Brand confusion ("Braintree") |
| Utah | Q1 Medium | HQ state, Charlie has local resources |
| Kansas | Q2 | Ambassador: Delina Wallace |
| Arkansas | Q2 | |
| Iowa | Q2 | |
| Minnesota | Q2 | |
| Montana | Q3 | |

### 2. Versus Sub-Project
**Location:** `Studio/SEO Content Production/Versus/PROJECT.md`

**Template includes:**
- 3 quality gates (gap analysis, depth, original value)
- Slack mining strategy (unfair advantage)
- Content buckets with volume estimates
- Process: Pilot 2-3 manually → measure → scale

**High-Volume Opportunities:**
- montessori vs waldorf (2,900)
- Classical Conversations vs X (22,200 for CC alone)
- Khan Academy vs IXL area (4,400+)

### 3. Weekly SEO Report Enhanced
**Location:** `.claude/tools/seomachine/tools/weekly_seo_report.py`

**Changes:**
- Removed fake "Content Gaps" section
- Added Priority Keyword Tracking (OpenEd's actual targets)
- Added relevance filtering to Quick Wins
- Status indicators: 🟢 Top 3, 🟡 Page 1, 🟠 Page 2, 🔴 Not ranking

### 4. Program Reference Created
**Location:** `.claude/references/opened-program-details.md`

Extracted from OpenEd 26-27 Info Guide PDF:
- All 9 operating states
- How the program works (5-step flow)
- Key features (free, flexible, reimbursement, support)
- Legal nuance for content positioning

### 5. Meeting Notes Archived
**Location:** `Studio/SEO Content Production/_archive/meetings/`

- Full transcript moved to archive
- Summary extracted with:
  - Fred's methodology (SEMrush, outlines, content calendar)
  - Charlie's todos from meetings
  - Content buckets and priorities

---

## API Connections Established

### Slack ✅ WORKING
**Method:** Direct API with browser tokens

**Tokens (URL-encoded):**
```
xoxd: xoxd-hoNuFGntRLyBseWuGiY36trjX5%2BQmYR%2BCk68jWZaCIYdzQ9bWkt9QSVd7uL1fj%2B0jSiByg7%2BGfK4WsuQmzfVvuXdj3DJL1qPFHz%2FXTHi7UUWScYJkd5M5IOhmRfoZ4EA9aQL9Al4htjJKafnTbwtamGHMzsn1fXY5tIDAsLOweyFevU1H0Bk3nZKbQ3AiT4qftzDbSc%3D
xoxc: xoxc-1120304371283-7037730349847-9034755777190-fa4af2e645668d0c83dadc3a0ddd3627217d3133d0f4a18d397121748ed3fdb7
```

**Key Channels Found:**
| Channel | ID | Members | Use For |
|---------|----|---------|---------| 
| #recommendations | C07DMDU0YQ4 | 154 | Curriculum opinions for Versus pages |
| #team-curriculum | C013WM4UBMF | 90 | Curriculum discussions |
| #teachers-state-specific-feedback | C07E7USNU2U | 116 | State page local insights |

**Example Query (working):**
```bash
curl -s -X POST 'https://slack.com/api/search.messages' \
  -H "Authorization: Bearer xoxc-..." \
  -H "Cookie: d=xoxd-..." \
  -d "query=in:#recommendations Saxon Math&count=10"
```

**Data Found:**
- 247 messages about "curriculum" in #recommendations
- 10+ discussions about Saxon Math
- Real teacher perspectives on Calvert, Exact Path, Study Island, Lexia, K-12

### Notion ✅ WORKING
**Method:** Direct API with integration token

**Token:** `[REDACTED]`
**Integration Name:** "Claude MCP"
**Workspace:** OpenEd

**Shared:** OpenEd Content Engine (contains 30+ databases)

**Key Databases Found:**
| Database | ID | Use For |
|----------|----|---------| 
| Curriculum List | 129afe52-ef59-80b6-a434-d070095fc776 | Versus pages |
| Oregon Homeschool Hubs/Watering Holes | 376a31a1-1c61-4406-82b1-8f9ed163f7ce | Oregon state page |
| Our Favorite Resources | 19fafe52-ef59-80da-a83e-e4242046b848 | Recommendations |
| Master Content Database | 9a2f5189-6c53-4a9d-b961-3ccbcb702612 | Track published |
| Meeting Notes | 21eafe52-ef59-8085-aec0-fb31927f74a1 | Context |

### Fellow MCP ⚠️ NEEDS CONFIGURATION
**Location:** `OpenEd Vault/.claude/settings.local.json`

**Status:** Configured but needs credentials
```json
{
  "fellow": {
    "command": "npx",
    "args": ["-y", "fellow-mcp"],
    "env": {
      "FELLOW_API_KEY": "YOUR_API_KEY_HERE",
      "FELLOW_SUBDOMAIN": "YOUR_SUBDOMAIN_HERE"
    }
  }
}
```

**To configure:**
1. Get API key from Fellow settings
2. Get subdomain (e.g., "opened" if URL is opened.fellow.app)
3. Update the settings.local.json

### DataForSEO ✅ WORKING
**Config:** `.claude/tools/seomachine/data_sources/config/.env`

### GSC ⚠️ BLOCKED
Need ops to add service account:
`opened-service-account@gen-lang-client-0217199859.iam.gserviceaccount.com`

---

## Oregon State Page - Ready to Draft

### Data Sources Available

**From Notion:**
- "Oregon Homeschool Hubs/Watering Holes" database
- Query: `curl -s 'https://api.notion.com/v1/databases/376a31a1-1c61-4406-82b1-8f9ed163f7ce/query'`

**From Slack:**
- #teachers-state-specific-feedback (116 members)
- Query: `in:#teachers-state-specific-feedback Oregon`

**From Charlie:**
- Local resources database for Oregon (mentioned, location TBD)

**From HSLDA (scraped structure):**
- Oregon legal requirements documented in State Pages template

### Template Ready
See: `Studio/SEO Content Production/State Pages/PROJECT.md`

---

## Versus Pages - Ready to Pilot

### Slack Data Mining Process
1. Search #recommendations for curriculum name
2. Extract teacher perspectives
3. Synthesize into "What Teachers Say" section
4. Add to Versus template

### Curricula with Slack Discussions Found
- Saxon Math (10+ messages)
- Calvert Learning
- Exact Path
- Study Island
- Lexia
- K-12
- ALEKS

---

## Decisions Made This Session

1. **State pages only for operating states** - 9 states, not arbitrary high-volume keywords
2. **Versus pages need quality gates** - No mass replication without gap analysis
3. **Slack is the unfair advantage** - Real teacher perspectives differentiate content
4. **Fred provides strategy, Charlie builds automation** - Complement, don't replace (yet)
5. **Direct API calls work in OpenCode** - Don't need MCP servers for Slack/Notion
6. **Legal nuance is critical** - OpenEd families ≠ homeschoolers legally, but identify as such

---

## Continuation Prompt

```
Continue SEO Content Production work for OpenEd.

## CONTEXT
Last session built the infrastructure:
- State Pages template at `Studio/SEO Content Production/State Pages/PROJECT.md`
- Versus template at `Studio/SEO Content Production/Versus/PROJECT.md`
- Slack API working (xoxc/xoxd tokens in handoff)
- Notion API working ("Claude MCP" integration)
- 9 operating states identified: AR, IN, IA, KS, MN, MT, NV, OR, UT

## READY TO EXECUTE

### Option 1: Draft Oregon State Page
Data sources ready:
- Notion: "Oregon Homeschool Hubs/Watering Holes" database (ID: 376a31a1-1c61-4406-82b1-8f9ed163f7ce)
- Slack: #teachers-state-specific-feedback for Oregon insights
- Charlie: Has local resources database
- Template: Ready in State Pages/PROJECT.md

### Option 2: Pilot Versus Page
Data sources ready:
- Slack: 247+ curriculum discussions in #recommendations
- Known curricula with discussions: Saxon Math, Calvert, Exact Path, Lexia
- Template: Ready in Versus/PROJECT.md with quality gates

### Option 3: Configure Fellow MCP
Needs:
- FELLOW_API_KEY
- FELLOW_SUBDOMAIN
Location: `OpenEd Vault/.claude/settings.local.json`

## KEY FILES
- Handoff: `.claude/sessions/2026-01-08-seo-content-production-handoff.md`
- NOW.md: `OpenEd Vault/NOW.md`
- State template: `Studio/SEO Content Production/State Pages/PROJECT.md`
- Versus template: `Studio/SEO Content Production/Versus/PROJECT.md`
- Program details: `.claude/references/opened-program-details.md`
```

---

## Files Modified This Session

```
Created:
├── Studio/SEO Content Production/State Pages/PROJECT.md
├── Studio/SEO Content Production/Versus/PROJECT.md
├── Studio/SEO Content Production/_archive/meetings/SEO-Meetings-Summary.md
├── .claude/references/opened-program-details.md
├── .claude/sessions/2026-01-08-seo-content-production-handoff.md (this file)
└── .claude/MCP_SETUP_GUIDE.md

Modified:
├── OpenEd Vault/NOW.md
├── OpenEd Vault/CLAUDE.md (added operating states line)
├── Studio/SEO Content Production/PROJECT.md
├── Studio/SEO Content Production/Lead Magnet Project/PROJECT.md (quiz keyword)
└── .claude/tools/seomachine/tools/weekly_seo_report.py

Moved:
└── SEO Meetings notes.md → _archive/meetings/
```

---

*Created: 2026-01-08 ~2:30 PM PT*
