# SEO Strategy Session Notes - 2026-01-29

---

## Executive Summary (For Boss Brief)

Today we built a systematic SEO content strategy for "X vs Y" comparison articles and validated it works with real data.

**Key Results:**
- 1 article ready to publish (Waldorf vs Montessori - 2,900 searches/month)
- 3 existing drafts discovered and assessed (Khan vs IXL, Saxon vs MUS, IXL vs Exact Path)
- 27 comparison keywords identified totaling ~7,500 monthly searches
- Master keyword list consolidated into single source of truth
- Production queue established for next 5 articles

**Tools Used:**
- **DataForSEO API** - Real-time keyword research with search volume, competition data
- **seomachine skill** - Custom integration for programmatic SEO queries
- **quality-loop skill** - 5-judge quality gate system for content QA

**What This Enables:**
- Data-driven content prioritization (not guessing which articles to write)
- Systematic production at 2 articles/week pace
- Clear tracking from keyword research → draft → publish → rank

---

## What We Did Today

### 1. Fixed Waldorf vs Montessori Article
- Rewrote awkward "Do You Have to Choose?" section
- Removed off-topic Classical/Unschooling references
- Added 4 practical Waldorf + Montessori hybrid approaches
- Ran full 5-judge quality loop → PASSED
- **Status:** Ready to publish to Webflow

### 2. Keyword Discovery Sprint
Used DataForSEO API to research comparison keywords:

**Pedagogy comparisons found:**
| Keyword | Volume |
|---------|--------|
| waldorf vs montessori | 2,900/mo |
| montessori vs reggio emilia | 1,900/mo |
| unschooling vs homeschooling | 320/mo |
| montessori vs traditional | 260/mo |
| charlotte mason vs classical | 110/mo |

**Curriculum comparisons found:**
| Keyword | Volume |
|---------|--------|
| ixl vs khan academy | 590/mo |
| abeka vs bju | 170/mo |
| math u see vs saxon | 140/mo |
| my father's world vs tgatb | 70/mo |

### 3. Discovered Existing Work
Found `Versus/` folder with 3 drafts already written:
- `khan-academy-vs-ixl/draft-v1.md` - Complete, good quality
- `saxon-vs-math-u-see/draft-v1.md` - Complete, good quality
- `ixl-vs-exact-path/draft-v2.md` - Complete, shorter format

All include real teacher quotes and follow the template.

### 4. Consolidated Files
- Merged duplicate keyword files into single source of truth
- Location: `.claude/skills/seo-content-production/references/comparison-keywords.md`
- Deleted duplicate in Deep Dive Studio

### 5. Created Content Brief
- Montessori vs Reggio Emilia (1,900/mo opportunity)
- Full structure, internal links, quality gates defined

---

## Current State

### Drafts Ready for Quality Loop
| Article | Volume | Location | Next Step |
|---------|--------|----------|-----------|
| Waldorf vs Montessori | 2,900/mo | Deep Dive Studio/ | ✅ Publish |
| Khan Academy vs IXL | 590/mo | Versus/ | Run quality loop |
| Saxon vs Math-U-See | 140/mo | Versus/ | Run quality loop |
| IXL vs Exact Path | - | Versus/ | Run quality loop |

### Production Queue
1. Montessori vs Reggio Emilia (1,900/mo) - Brief created
2. Unschooling vs Homeschooling (320/mo)
3. Abeka vs BJU (170/mo)
4. Charlotte Mason vs Classical (110/mo)
5. My Father's World vs TGATB (70/mo)

---

## Key Files

| Purpose | Location |
|---------|----------|
| **Master keyword list** | `.claude/skills/seo-content-production/references/comparison-keywords.md` |
| **Versus project/template** | `Studio/SEO Content Production/Versus/PROJECT.md` |
| **Curriculum drafts** | `Studio/SEO Content Production/Versus/` |
| **Pedagogy drafts** | `Studio/SEO Content Production/Open Education Hub/Deep Dive Studio/` |
| **seomachine skill** | `.claude/skills/seomachine/` |

---

## Future Vision: Automated Content Refresh

### The Goal
Build agents that automatically:
1. Detect declining pages via GSC
2. Find recent authoritative discussions on those topics
3. Suggest content updates with fresh material

### Components Needed

**1. GSC Integration (Existing)**
- `gsc` skill can query Google Search Console
- Need: Weekly report of declining pages (position drops, traffic drops)

**2. Last 30 Days Skill (To Adapt)**
- Source: https://github.com/jdrhyne/agent-skills/tree/main/skills/last30days
- Current: Searches Reddit, X, HN, Stack Overflow, Dev.to, Lobsters
- Adaptation needed:
  - Remove HN focus (not education-relevant)
  - Add education forums (homeschool subreddits, education Twitter)
  - Configurable time window (24h for daily newsletter, 30-60 days for SEO)
  - Configurable keywords per topic

**3. RSS Curation Integration**
- Already have: 64 verified education RSS feeds in `Projects/RSS-Curation/`
- Connection: Use Last 30 to supplement RSS with forum discussions
- Daily use: Last 24h forum discussions for newsletter ideas
- SEO use: Last 30-60 days for updating evergreen articles

### Workflow Vision

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT REFRESH AGENT                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. GSC Query: "Which pages dropped >20% in 30 days?"       │
│                           ↓                                  │
│  2. For each declining page:                                 │
│     - Extract topic/keywords                                 │
│     - Run Last 30 skill with those keywords                 │
│     - Pull relevant RSS items from past month               │
│                           ↓                                  │
│  3. Generate update suggestions:                             │
│     - New stats/data to add                                  │
│     - Recent discussions to reference                        │
│     - Fresh examples from community                          │
│                           ↓                                  │
│  4. Output: Prioritized refresh queue with source material  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Daily Newsletter Integration

```
RSS Feeds (last 24h)     Forum Discussions (last 24h)
        │                           │
        └───────────┬───────────────┘
                    ↓
            Combined Curation
                    ↓
        Score: DEFINITELY / PROBABLY / NO
                    ↓
            Ed the Horse drafts
```

---

## Next Actions

### Immediate (This Week)
- [ ] Publish Waldorf vs Montessori to Webflow
- [ ] Run quality loop on Khan vs IXL draft
- [ ] Run quality loop on Saxon vs MUS draft
- [ ] Write Montessori vs Reggio Emilia draft

### Short-Term (Next 2 Weeks)
- [ ] Adapt Last 30 skill for education context
- [ ] Set up weekly GSC declining pages report
- [ ] Publish 4 comparison articles

### Medium-Term (Q2)
- [ ] Build content refresh agent
- [ ] Create hub page `/blog/homeschool-methods-compared`
- [ ] Integrate Last 30 into daily RSS curation workflow

---

## DataForSEO Notes

**API Details:**
- Cost: ~$0.01-0.05 per request
- Endpoints used: `related_keywords`, `serp/google/organic`
- Auth: Basic auth with login/password from `.env`

**Best Practices:**
- Batch queries efficiently (costs add up)
- Cache results when possible
- Volume numbers can vary between research dates - use as directional

**Credentials Location:**
- File: `/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault/.env`
- Variables: `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD`

---

*Session completed: 2026-01-29*
