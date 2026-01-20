# Studio Consolidation & Architecture Plan
**Date:** January 6, 2026  
**Status:** Proposed

## Executive Summary

Consolidate fragmented project folders, integrate SEO Machine into main vault structure, and create clear architecture for Q1 2026 projects.

---

## Problems to Solve

### 1. Confusing Folder Structure
- `Articles/` folder has WIP articles that belong elsewhere
- SEO Machine isolated in `Misc. Utilities/` with duplicate .claude structure
- Unclear relationship between `SEO Article Factory`, `Grade Level Guides`, `Guest Contributors`
- No folder for Eddie Awards (new Q1 priority)

### 2. SEO Machine Isolation
- Has own `.claude/agents/` and `.claude/commands/` 
- 7 agents + 7 commands not integrated with main vault
- Context files (blog-index.csv, internal-links) not accessible to main skills
- Modules exist but need API testing

### 3. Project Overlap
- Grade Level Guides ARE part of SEO Article Factory (curriculum cluster)
- Guest Contributors ARE part of SEO Article Factory (external authors)
- Tools Directory also SEO play with similar workflow

---

## Proposed Architecture

### Top-Level Studio Structure

```
Studio/
├── OpenEd Daily/ ← Weekly newsletter production
├── Open Ed Podcasts/ ← Podcast production
├── Open Education Hub/ ← Deep dive articles, hub pages
│
├── SEO Content Production/ ← NEW (consolidates SEO work)
│   ├── PROJECT.md ← Master project file
│   ├── Factory/ ← 60 SEO articles Q1
│   ├── Grade Level Guides/ ← K-12 curriculum guides
│   ├── Tools Directory/ ← Parent-reviewed tools
│   ├── Guest Contributors/ ← External author pipeline
│   └── Articles/ ← WIP articles (from old Articles/)
│
├── Eddie Awards/ ← NEW Q1 project
│   ├── PROJECT.md
│   ├── Categories/
│   ├── Nominations/
│   ├── Website Design/
│   └── Marketing/
│
├── Lead Magnet Project/ ← Adaptive quiz funnel
│
└── Generated_Images/ ← AI image assets
    └── Reel Ideas/ ← Social video concepts
```

### SEO Machine Integration

**MOVE:** `Studio/Misc. Utilities/seomachine/` → `Studio/SEO Content Production/_seomachine/`

**Why underscore prefix?**
- Marks it as infrastructure (not content folder)
- Groups at top when sorted alphabetically
- Clarifies it's tooling for the project

**Structure:**
```
SEO Content Production/
├── PROJECT.md ← Master overview
├── _seomachine/ ← Tools & automation
│   ├── data_sources/ ← API modules (GA4, DataForSEO, etc.)
│   ├── context/ ← Reference files (blog-index.csv, etc.)
│   ├── scripts/ ← Automation scripts
│   └── tests/ ← API test scripts
├── Factory/ ← 60 article production
├── Grade Level Guides/
├── Tools Directory/
└── Guest Contributors/
```

**MOVE SEO Machine agents/commands to main vault:**
```
.claude/
├── agents/
│   ├── content-researcher.md ← From seomachine/internal-linker
│   ├── seo-optimizer.md ← From seomachine/seo-optimizer
│   ├── content-analyzer.md ← From seomachine
│   ├── keyword-mapper.md ← From seomachine
│   ├── meta-creator.md ← From seomachine
│   └── performance-monitor.md ← From seomachine/performance
├── commands/
│   ├── seo-research.md ← From seomachine
│   ├── seo-analyze.md ← From seomachine/analyze-existing
│   └── webflow-sync.md ← NEW (consolidate Webflow scripts)
└── skills/ ← Existing 24 skills
```

---

## Detailed Migration Plan

### Phase 1: SEO Machine Consolidation

#### Step 1.1: Move & Rename
```bash
# Move SEO Machine into SEO Content Production
mv "Studio/Misc. Utilities/seomachine" "Studio/SEO Content Production/_seomachine"

# Move old Articles folder into SEO Content Production
mv "Studio/Articles" "Studio/SEO Content Production/Articles"

# Move Grade Level Guides
mv "Studio/Grade Level Guides" "Studio/SEO Content Production/Grade Level Guides"

# Move Guest Contributors
mv "Studio/Guest Contributors" "Studio/SEO Content Production/Guest Contributors"

# Rename SEO Article Factory to Factory
mv "Studio/SEO Article Factory" "Studio/SEO Content Production/Factory"

# Move Tools Directory
mv "Studio/Tools Directory" "Studio/SEO Content Production/Tools Directory"
```

#### Step 1.2: Integrate Agents
**Action:** Copy SEO Machine agents to main `.claude/agents/`

**Agent Mapping:**
| SEO Machine Agent | New Main Agent | Rationale |
|-------------------|----------------|-----------|
| `internal-linker.md` | `content-researcher.md` | Finds internal linking opportunities |
| `seo-optimizer.md` | `seo-optimizer.md` | Analyzes & improves existing content |
| `content-analyzer.md` | `content-analyzer.md` | Reviews content quality |
| `keyword-mapper.md` | `keyword-mapper.md` | Maps keywords to content |
| `meta-creator.md` | `meta-creator.md` | Generates meta descriptions |
| `performance.md` | `performance-monitor.md` | Tracks content performance |
| `editor.md` | *(Keep as reference)* | May integrate with existing skills |

**Adapt for OpenEd:**
- Replace "Castos" references with "OpenEd"
- Update context files references
- Integrate with existing `opened-identity` voice

#### Step 1.3: Integrate Commands
**Action:** Copy SEO Machine commands to main `.claude/commands/`

**Command Mapping:**
| SEO Machine Command | New Main Command | Purpose |
|---------------------|------------------|---------|
| `research.md` | `seo-research.md` | Keyword research workflow |
| `analyze-existing.md` | `seo-analyze.md` | Audit existing content |
| `optimize.md` | `seo-optimize.md` | Improve underperforming content |
| `performance-review.md` | `seo-performance.md` | Monthly performance review |
| `write.md` | *(Covered by skill)* | Use `seo-content-writer` skill |
| `rewrite.md` | *(Covered by skill)* | Use existing skills |
| `scrub.md` | *(Utility command)* | Keep in _seomachine/scripts/ |

#### Step 1.4: Context File Access
**Problem:** Agents need access to blog-index.csv, internal-links-reference.md

**Solution:**
```
.claude/
└── context/ ← NEW directory
    ├── blog-index.csv ← Symlink or copy from _seomachine/context/
    ├── content-index.csv ← Symlink or copy
    ├── internal-links-reference.md ← Symlink or copy
    └── seo-guidelines.md ← Symlink or copy
```

**OR:** Agents reference `Studio/SEO Content Production/_seomachine/context/` directly

---

### Phase 2: Project Architecture

#### SEO Content Production PROJECT.md

Create master project file:

```markdown
# SEO Content Production

Master project for all SEO-driven content initiatives Q1 2026.

## Sub-Projects

### 1. Factory (60 Articles)
**Goal:** Ship 60 SEO articles in Q1
**Workflow:** Research → Outline → Draft → Polish → Publish
**Skills:** `seo-content-writer`, `ghostwriter`, `hook-and-headline-writing`
**Agents:** `seo-optimizer`, `content-researcher`, `keyword-mapper`

### 2. Grade Level Guides (K-12)
**Goal:** Curriculum guides for each grade level
**Content Cluster:** Part of Factory's curriculum cluster
**Focus:** Marketplace vendor partnerships

### 3. Tools Directory (20+ Reviews)
**Goal:** Parent-reviewed curriculum database
**Workflow:** Ella interviews → Extract reviews → Publish
**Skills:** `verified-review`, `ghostwriter`, `seo-content-writer`

### 4. Guest Contributors (10+ Posts)
**Goal:** External authors publishing on OpenEd
**Strategy:** Low-friction (compile from existing writing)
**Priority:** High-status authors with audience

## Shared Infrastructure

- `_seomachine/` - API tools, analytics, automation
- Keyword research (DataForSEO)
- Performance tracking (GA4)
- Internal linking (blog-index.csv)
- Content optimization

## Metrics & KPIs

| Metric | Q1 Target | Current |
|--------|-----------|---------|
| Factory Articles | 60 | 0 |
| Grade Level Guides | 12 (K-12) | 0 |
| Tool Reviews | 20 | 0 |
| Guest Posts | 10 | 0 |
| Organic Traffic | +50% | Baseline TBD |
| Newsletter Signups from Organic | +100% | Baseline TBD |
```

#### Eddie Awards PROJECT.md

```markdown
# The Eddie Awards

Open education awards program - establishing OpenEd as curator and authority.

## Categories (5)
1. Innovation in Open Education
2. Community Leader
3. Thought Leader
4. Most Innovative Curriculum
5. Student Achievement

## Timeline Q1 2026
- [ ] Nominations open: Feb 1
- [ ] Nominations close: March 1
- [ ] Winners announced: March 15
- [ ] Website launch: Jan 31

## Website Strategy
- Build OUTSIDE Webflow ecosystem (more control)
- Acts as funnel → OpenEd Daily
- Category-driven content (not program-driven)
- Ella handling design

## Folder Structure
Eddie Awards/
├── PROJECT.md
├── Categories/
│   ├── Innovation.md
│   ├── Community-Leader.md
│   ├── Thought-Leader.md
│   ├── Curriculum.md
│   └── Student.md
├── Nominations/
│   └── [Nominee folders]
├── Website/
│   ├── Design/
│   ├── Copy/
│   └── Technical/
└── Marketing/
    ├── Launch-Plan.md
    ├── Outreach-List.md
    └── Social-Calendar.md
```

---

### Phase 3: Webflow Sync as Command

**Current State:**
- `agents/webflow_sync_agent.py` (Python automation)
- `Studio/Misc. Utilities/seomachine/sync_webflow.py`
- Multiple Webflow scripts scattered

**Consolidation:**

Create single command: `.claude/commands/webflow-sync.md`

```markdown
# Webflow Sync Command

Sync published content from Webflow CMS to local Master Content Database.

## When to Run
- Start of newsletter/podcast session (to get latest content)
- After publishing new content
- Weekly (Monday morning)

## Usage
```bash
/webflow-sync
```

## What It Does
1. Fetches all blog posts from Webflow API
2. Converts to markdown with YAML frontmatter
3. Saves to `Content/Master Content Database/`
4. Updates blog-index.csv
5. Reports: X new items synced

## Implementation
Location: `Studio/SEO Content Production/_seomachine/scripts/sync_webflow.py`

## API Keys Required
- WEBFLOW_API_TOKEN (in .env)
```

**Consolidate Python scripts:**
```
_seomachine/
└── scripts/
    ├── sync_webflow.py ← Master sync script
    ├── test_api.py ← Test all API connections
    └── utils/
        ├── webflow.py ← Webflow API wrapper
        ├── ga4.py ← GA4 wrapper
        └── dataforseo.py ← DataForSEO wrapper
```

---

### Phase 4: API Testing Plan

**Goal:** Verify all SEO Machine APIs are working

**APIs to Test:**
1. Google Analytics 4 (GA4) - Traffic data
2. DataForSEO - Keyword research, SERP analysis
3. Google Search Console - Search performance
4. Webflow - Content sync

**Test Script:** `_seomachine/scripts/test_api.py`

```python
#!/usr/bin/env python3
"""
Test all SEO Machine API connections
"""

from dotenv import load_dotenv
load_dotenv('_seomachine/data_sources/config/.env')

from _seomachine.data_sources.modules import (
    google_analytics,
    dataforseo,
    google_search_console,
    webflow
)

def test_ga4():
    """Test Google Analytics 4"""
    print("\n🔍 Testing GA4...")
    try:
        ga = google_analytics.GoogleAnalytics()
        pages = ga.get_top_pages(days=30, limit=5)
        print(f"✅ GA4 working - Retrieved {len(pages)} pages")
        for p in pages[:3]:
            print(f"   - {p['title'][:40]}: {p['pageviews']} views")
        return True
    except Exception as e:
        print(f"❌ GA4 failed: {e}")
        return False

def test_dataforseo():
    """Test DataForSEO"""
    print("\n🔍 Testing DataForSEO...")
    try:
        dfs = dataforseo.DataForSEO()
        keywords = dfs.get_keyword_ideas('homeschool curriculum', limit=5)
        print(f"✅ DataForSEO working - Retrieved {len(keywords)} keywords")
        for kw in keywords[:3]:
            vol = kw.get('search_volume', 'N/A')
            print(f"   - {kw['keyword']}: {vol} volume")
        return True
    except Exception as e:
        print(f"❌ DataForSEO failed: {e}")
        return False

def test_search_console():
    """Test Google Search Console"""
    print("\n🔍 Testing Search Console...")
    try:
        gsc = google_search_console.GoogleSearchConsole()
        queries = gsc.get_top_queries(days=30, limit=5)
        print(f"✅ Search Console working - Retrieved {len(queries)} queries")
        return True
    except Exception as e:
        print(f"❌ Search Console failed: {e}")
        return False

def test_webflow():
    """Test Webflow"""
    print("\n🔍 Testing Webflow...")
    try:
        wf = webflow.Webflow()
        collections = wf.get_collections()
        print(f"✅ Webflow working - {len(collections)} collections found")
        return True
    except Exception as e:
        print(f"❌ Webflow failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("SEO Machine API Test Suite")
    print("=" * 50)
    
    results = {
        'GA4': test_ga4(),
        'DataForSEO': test_dataforseo(),
        'Search Console': test_search_console(),
        'Webflow': test_webflow()
    }
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    for api, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {api}")
    
    if all(results.values()):
        print("\n🎉 All APIs working!")
    else:
        print("\n⚠️  Some APIs need configuration")
```

**Run with actual project:**

1. Start with simple task: "Get top 10 performing articles last 30 days"
2. Use GA4 module
3. Verify output
4. Move to keyword research for one article
5. Test internal linking suggestions

---

## Migration Checklist

### Immediate (Today)
- [ ] Create `SEO Content Production/` folder
- [ ] Move sub-projects into it
- [ ] Create Eddie Awards folder with PROJECT.md
- [ ] Move SEO Machine to `_seomachine/`

### This Week
- [ ] Adapt SEO Machine agents for OpenEd (remove Castos references)
- [ ] Copy agents to main `.claude/agents/`
- [ ] Copy commands to main `.claude/commands/`
- [ ] Create consolidated Webflow sync command
- [ ] Test APIs with test_api.py script

### Next Week
- [ ] Run actual SEO research for 5 articles
- [ ] Test content-researcher agent with real article
- [ ] Verify GA4 data pulling correctly
- [ ] Test keyword research workflow

### By End of Month
- [ ] Publish first 5 Factory articles
- [ ] Complete Eddie Awards website design
- [ ] Conduct first Ella interview for Tools Directory
- [ ] Reach out to first 5 guest contributors

---

## Success Metrics

### Structure
- ✅ Clear hierarchy: All SEO work under one parent folder
- ✅ No duplicate .claude structures
- ✅ Context files accessible to agents
- ✅ All APIs tested and working

### Workflow
- ✅ Can run keyword research in <5 minutes
- ✅ Internal linking suggestions work automatically
- ✅ Content performance data available on demand
- ✅ Webflow sync runs without manual intervention

### Output
- ✅ First Factory article published
- ✅ Eddie Awards site launched
- ✅ Tools Directory first review published
- ✅ First guest contributor confirmed

---

## Notes

### Why "SEO Content Production" not "SEO Article Factory"?
- More encompassing name
- Includes Tools, Guides, Guest Contributors
- Factory is sub-project, not entire operation

### Why Keep _seomachine Folder?
- Infrastructure vs content separation
- Reusable across projects
- APIs and tools are project-agnostic
- Underscore prefix makes it clear it's tooling

### What About Other Studio Folders?
- `Lead Magnet Project/` - stays separate (different purpose)
- `OpenEd Daily/` - weekly content, not SEO focus
- `Open Ed Podcasts/` - separate production workflow
- `Open Education Hub/` - hub pages, different strategy

---

*This consolidation brings all SEO work under unified structure while maintaining clear separation between content production and infrastructure.*
