# SEOMachine Architecture Analysis

## Overview

The seomachine is a **Python-based data pipeline** - not an AI orchestration system. It has no Claude/GPT integration. The "intelligence" comes from combining multiple data sources programmatically.

---

## Structure

```
seomachine/
├── data_sources/
│   ├── config/.env              # All credentials (WORKING)
│   └── modules/                 # 15 API integrations
│       ├── google_analytics.py  # GA4 traffic data
│       ├── google_search_console.py  # GSC rankings
│       ├── dataforseo.py        # Keyword research, SERP
│       ├── data_aggregator.py   # COMBINES ALL SOURCES
│       ├── hubspot.py           # Email/contacts
│       ├── hubspot_insights.py  # Email analytics
│       ├── meta.py              # FB/Instagram
│       ├── youtube.py           # YouTube analytics
│       ├── webflow.py           # CMS publishing
│       ├── keyword_analyzer.py  # Keyword analysis
│       ├── search_intent_analyzer.py  # Intent classification
│       ├── seo_quality_rater.py # Content scoring
│       ├── content_scrubber.py  # Page extraction
│       ├── content_length_comparator.py  # Competitor analysis
│       └── readability_scorer.py # Readability metrics
│
├── tools/                       # Workflow scripts
│   ├── weekly_seo_report.py     # Weekly SEO report
│   ├── weekly_hubspot_report.py # Weekly email report
│   ├── weekly_social_report.py  # Weekly social report
│   ├── content_brief_generator.py  # Generate briefs
│   ├── competitor_gap_finder.py # Find keyword gaps
│   ├── markdown_to_webflow.py   # Publish to Webflow
│   └── seo_history.py           # Historical tracking
│
├── context/                     # Reference docs
│   ├── brand-voice.md
│   ├── style-guide.md
│   ├── seo-guidelines.md
│   ├── competitor-analysis.md
│   ├── target-keywords.md
│   └── internal-links-map.md
│
└── data/                        # Output storage
```

---

## Key Architecture Patterns

### 1. Module Layer (data_sources/modules/)
Each module is a **standalone Python class** that wraps one API:

```python
class GoogleAnalytics:
    def get_top_pages(days, limit, path_filter)
    def get_page_trends(url, days)
    def get_declining_pages(comparison_days, threshold)
    def get_traffic_sources(url, days)
```

### 2. Aggregation Layer (data_aggregator.py)
Combines multiple modules into unified queries:

```python
class DataAggregator:
    def __init__(self):
        self.ga = GoogleAnalytics()
        self.gsc = GoogleSearchConsole()
        self.dfs = DataForSEO()

    def identify_content_opportunities()  # Combines all
    def generate_performance_report()     # Full report
    def get_priority_queue()              # Task list
```

### 3. Report Layer (tools/)
Scripts that run aggregator methods and format output:

```python
# weekly_seo_report.py
report = WeeklyReport(domain="opened.co")
report.generate()
print(report.format_markdown())
```

---

## Proposed Skills Breakdown

### Tier 1: Data Source Skills (Already Have Most)

| Skill | Status | Source |
|-------|--------|--------|
| `gsc` | EXISTS | `.claude/skills/gsc/` |
| `ga4` | EXISTS | `.claude/skills/ga4/` |
| `seo-research` | EXISTS | Part of seo-content-production |

**Action:** Update these to use seomachine's working auth config.

### Tier 2: Analysis Skills (NEW - Extract from seomachine)

| Skill | Creates | Source Module |
|-------|---------|---------------|
| `content-brief` | Competitor-informed brief | content_brief_generator.py |
| `competitor-gap` | Keyword gap analysis | competitor_gap_finder.py |
| `seo-aggregator` | Combined opportunities | data_aggregator.py |

**Action:** Create skill YAML that tells Claude when/how to run these scripts.

### Tier 3: Report Skills (NEW - Weekly Automation)

| Skill | Output | Source Tool |
|-------|--------|-------------|
| `weekly-seo-report` | SEO performance report | weekly_seo_report.py |
| `weekly-hubspot-report` | Email analytics | weekly_hubspot_report.py |
| `weekly-social-report` | Social metrics | weekly_social_report.py |

**Action:** Create skills that invoke these and format for Slack/user.

### Tier 4: Publishing Skills

| Skill | Action | Source |
|-------|--------|--------|
| `webflow-publish` | Publish to CMS | webflow.py, markdown_to_webflow.py |

---

## Key Insight: Orchestration Model

**Seomachine = Data pipelines (Python)**
**Claude Code = Orchestration layer (skills)**

The seomachine scripts don't need rewriting. Create skills that:
1. Document WHEN to invoke each script
2. Show Claude HOW to call them
3. Let Claude orchestrate the workflow conversationally

Example skill pattern:

```yaml
# .claude/skills/content-brief/SKILL.md
---
name: content-brief
description: Generate SEO content brief using DataForSEO + competitor analysis
---

## When to Use
- Starting new SEO article
- User asks for content brief
- Before writing hub content

## Command
```bash
python3 "Studio/SEO Content Production/seomachine/tools/content_brief_generator.py" "keyword"
```

## Output
Markdown file in tools/ folder with:
- Primary keyword metrics
- Secondary keyword cluster
- Competitor H2/H3 structure
- FAQ questions to answer
- Target word count
```

---

## Recommended Next Steps

### Phase 1: Consolidate Auth
1. Update `.env` in OpenEd Vault to include all seomachine credentials
2. Update `gsc` and `ga4` skills to use same auth method as seomachine
3. Test that both skill scripts AND seomachine scripts work

### Phase 2: Create Analysis Skills
1. `content-brief` skill - Wraps content_brief_generator.py
2. `competitor-gap` skill - Wraps competitor_gap_finder.py
3. `seo-aggregator` skill - Wraps data_aggregator.py

### Phase 3: Create Report Skills
1. `weekly-seo-report` skill - Invokes weekly_seo_report.py
2. Add Slack formatting for automated delivery
3. Add scheduling via cron or manual invocation

### Phase 4: Integrate into Workflows
1. Update `seo-content-production` to invoke `content-brief` at start
2. Add post-publish tracking using `gsc` + `ga4`
3. Create end-to-end SEO workflow documentation

---

## Context Files Worth Preserving

The `context/` folder has valuable reference docs:

| File | Purpose | Migrate To |
|------|---------|------------|
| brand-voice.md | Writing style | Already in opened-identity |
| style-guide.md | Formatting rules | Already in ghostwriter |
| seo-guidelines.md | SEO best practices | seo-content-production |
| target-keywords.md | Priority keywords | Already tracked |
| internal-links-map.md | Link structure | seo-content-production |

---

*Analysis completed: 2026-01-29*
