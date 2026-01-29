# Starter Prompts: SEO & Content OS Workstreams

*Created: 2026-01-29*
*Context: These prompts continue work from the SEO comparison strategy session*

---

## Prompt 1: RSS Curation + SEO Integration

**Purpose:** Connect the RSS curation system with SEO content refresh to create a closed-loop content improvement system.

```
Continue the SEO content refresh automation project.

CONTEXT:
- RSS Curation project exists at Projects/RSS-Curation/ with 64 verified education feeds
- seomachine skill has GSC and GA4 modules for tracking declining pages
- We want to adapt the "Last 30 Days" skill (https://github.com/jdrhyne/agent-skills/tree/main/skills/last30days) for education context

GOAL: Build a content refresh agent that:
1. Identifies declining pages via GSC (position drops, traffic drops)
2. Finds recent authoritative discussions on those topics using:
   - RSS feeds (last 30 days)
   - Forum discussions (Reddit homeschool subs, education Twitter)
3. Generates update suggestions with fresh source material

SPECIFIC TASKS:
1. Create an adapted "Last 30" skill for education context:
   - Remove HN (not education-relevant)
   - Add education-specific sources (r/homeschool, education Twitter accounts)
   - Configurable time window (24h for daily newsletter, 30-60 days for SEO refresh)
   - Configurable keywords per topic

2. Build integration between:
   - GSC declining pages report → topic extraction
   - Last 30 skill → recent discussions
   - RSS curation feeds → authoritative content

3. Create a weekly workflow that outputs:
   - Prioritized refresh queue (which pages need updates)
   - Source material package for each (recent quotes, stats, discussions)

KEY FILES:
- Projects/RSS-Curation/PROJECT.md - RSS architecture
- Projects/RSS-Curation/FEEDS.md - 64 verified feeds
- .claude/skills/seomachine/modules/google_search_console.py - GSC queries
- .claude/skills/seomachine/modules/google_analytics.py - GA4 queries
- .claude/skills/seo-content-production/references/comparison-keywords.md - tracking keywords

DO NOT write new content. Focus on building the automation infrastructure.
```

---

## Prompt 2: Content OS Documentation for Leadership

**Purpose:** Document the Content OS capabilities for non-technical stakeholders (boss brief, team onboarding).

```
Create documentation that explains OpenEd's Content OS to leadership and new team members.

CONTEXT:
From today's SEO session, we demonstrated:
- DataForSEO API integration for keyword research (found 27 comparison keywords totaling ~7,500 monthly searches)
- 5-judge quality loop for content QA (Human Detector, Accuracy, Voice, Reader, SEO)
- Systematic production pipeline (keyword → brief → draft → quality loop → publish)
- 4 articles ready to publish with full metadata, FAQs, and thumbnails

DELIVERABLES:

1. **Executive Summary (1 page)**
   Location: Studio/SEO Content Production/CONTENT_OS_EXECUTIVE_SUMMARY.md
   - What capabilities exist (tools, skills, data sources)
   - What we can produce and at what quality/speed
   - Key metrics: keywords discovered, articles in pipeline, monthly search opportunity
   - No jargon - written for Melissa/leadership

2. **Capability Map (visual)**
   Location: Same file, mermaid diagram
   - Show the flow: Data Sources → Skills → Outputs
   - Include: DataForSEO, GSC, GA4, RSS feeds, Slack MCP, Notion
   - Show quality gates in the pipeline

3. **Process Documentation**
   Location: .claude/skills/seo-content-production/references/PRODUCTION_PROCESS.md
   - Step-by-step for the comparison article workflow
   - When to use which skill
   - Quality loop checklist
   - Internal linking strategy

KEY FILES TO REFERENCE:
- Studio/SEO Content Production/SESSION_NOTES_2026-01-29.md - today's work
- .claude/skills/seo-content-production/references/comparison-keywords.md - master keyword list
- Studio/SEO Content Production/Versus/PROJECT.md - template and quality gates
- OpenEd Vault/CLAUDE.md - Content OS overview

TONE: Professional but accessible. Focus on outcomes and capabilities, not technical implementation.
```

---

## Prompt 3: Quality Loop Automation

**Purpose:** Make the 5-judge quality loop faster and more consistent by creating a dedicated skill.

```
Refactor the quality loop into a more automated, reusable skill.

CONTEXT:
Currently the quality loop is manual - I read the quality-loop skill, then manually check each judge. This works but is slow and inconsistent.

GOAL: Create a streamlined quality check that can:
1. Auto-detect content type (article, social post, newsletter)
2. Run appropriate judges (full 5-judge for articles, lite 3-judge for social)
3. Output a structured verdict with specific line-by-line fixes
4. Track pass/fail history per article

SPECIFIC IMPROVEMENTS:

1. **Human Detector Automation**
   - Create a checklist that can be programmatically checked:
     - Grep for forbidden words (delve, comprehensive, etc.)
     - Pattern match for correlative constructions
     - Check for em dashes vs hyphens
   - Output: specific line numbers and suggested fixes

2. **Internal Link Checker**
   - Count internal links in article
   - Verify links exist (check against Master_Content_Index.md)
   - Suggest additional link opportunities based on topic

3. **Structured Output**
   - JSON output for each judge verdict
   - Can be stored for tracking over time
   - Easy to parse for "what needs fixing"

KEY FILES:
- .claude/skills/quality-loop/SKILL.md - current skill
- .claude/skills/quality-loop/references/*.md - judge criteria
- .claude/skills/ai-tells/SKILL.md - AI detection patterns

OUTPUT: Updated quality-loop skill with automation helpers.
```

---

## Prompt 4: Comparison Article Production Sprint

**Purpose:** Continue producing comparison articles from the keyword list.

```
Continue the comparison article production sprint.

CONTEXT:
- Master keyword list: .claude/skills/seo-content-production/references/comparison-keywords.md
- 4 articles published/ready: Waldorf vs Montessori, Khan vs IXL, Saxon vs MUS, IXL vs Exact Path
- Production template: Studio/SEO Content Production/Versus/PROJECT.md

NEXT IN QUEUE:
1. Montessori vs Reggio Emilia (1,900/mo) - Brief exists at Deep Dive Studio/
2. Unschooling vs Homeschooling (320/mo)
3. Abeka vs BJU (170/mo)
4. Charlotte Mason vs Classical (110/mo)

WORKFLOW FOR EACH:
1. Create content brief (if not exists)
2. Search for OpenEd proprietary content (podcasts, newsletters, Slack)
3. Write draft following Versus template
4. Run 5-judge quality loop
5. Add FAQ section
6. Generate thumbnail
7. Prepare publish package

Start with Montessori vs Reggio Emilia - the brief already exists.

KEY FILES:
- Deep Dive Studio/Montessori vs Reggio Emilia/CONTENT_BRIEF.md
- Versus/PROJECT.md - template
- quality-loop skill - QA process
```

---

## How These Prompts Connect

```
┌─────────────────────────────────────────────────────────────┐
│                     CONTENT OS                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Prompt 1   │    │   Prompt 3   │    │   Prompt 4   │  │
│  │ RSS + SEO    │───▶│ Quality Loop │───▶│ Production   │  │
│  │ Integration  │    │ Automation   │    │ Sprint       │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    Prompt 2                          │   │
│  │            Leadership Documentation                  │   │
│  │     (Explains what all this enables)                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Prompt 1** builds the infrastructure for finding what needs updating
**Prompt 3** makes quality control faster and more reliable
**Prompt 4** is the actual production work
**Prompt 2** documents all of this for stakeholders

---

## Session Continuity Notes

When resuming any of these prompts, the agent should:

1. Read `NOW.md` for current state
2. Check `SESSION_NOTES_2026-01-29.md` for context from this session
3. Reference the master keyword list for priorities
4. Use the quality-loop skill for all content QA

Key insight from today: **The seomachine skill + quality-loop skill + content templates = a repeatable system** that can produce high-quality SEO content at scale. The bottleneck is now production time, not research or quality control.
