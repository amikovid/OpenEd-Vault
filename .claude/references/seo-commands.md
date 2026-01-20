# SEO Machine Commands

**Location:** `/Root Docs/.claude/tools/seomachine/` (global, shared across workspaces)

**Status:** GA4 working | DataForSEO working | GSC needs permissions

## Weekly Report

```bash
cd "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/.claude/tools/seomachine/tools"
python3 weekly_seo_report.py --domain opened.co --competitors cathyduffy.com
```

## Quick Commands

**Declining Blog Posts:**
```bash
cd "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/.claude/tools/seomachine" && python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.google_analytics import GoogleAnalytics
for p in GoogleAnalytics().get_declining_pages(comparison_days=30, path_filter='/blog/')[:5]:
    print(f\"- {p['change_percent']:.0f}% | {p['title'][:50]}\")
"
```

**Keyword Research:**
```bash
cd "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/.claude/tools/seomachine" && python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.dataforseo import DataForSEO
for kw in DataForSEO().get_keyword_ideas('YOUR KEYWORD', limit=10):
    print(f\"- {kw['keyword']}: {kw.get('search_volume', 'N/A')} vol\")
"
```

## Credentials

| Item | Location |
|------|----------|
| GA4 JSON | `Archived Large Files/seo-article-factory-credentials/ga4-credentials.json` |
| Config | `/Root Docs/.claude/tools/seomachine/data_sources/config/.env` |
| GA4 Property ID | `451203520` |
| GSC Site URL | `sc-domain:opened.co` (needs permissions) |

## Modules

| Module | Purpose | Status |
|--------|---------|--------|
| `google_analytics.py` | GA4 traffic, declining pages | Working |
| `dataforseo.py` | Keyword research, SERP analysis | Working |
| `google_search_console.py` | Quick wins, keyword positions | Needs access |
