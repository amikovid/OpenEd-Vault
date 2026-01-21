# Weekly Marketing Reports

Generate consolidated SEO and social media performance reports.

---

## When to Use

- `/weekly-reports` - Run every Monday or end of week
- When preparing for team meetings or CMO check-ins
- When you need current channel performance data

---

## Quick Run

```bash
cd "Studio/SEO Content Production/seomachine"
./tools/weekly_reports.sh
```

This generates both reports in `Studio/Analytics & Attribution/reports/`

---

## What's Generated

### SEO Report (`weekly-seo-YYYY-MM-DD.md`)
- Priority keyword rankings
- Quick wins (keywords close to page 1)
- Declining content (traffic drops)
- Keyword opportunities

### Social Report (`weekly-social-YYYY-MM-DD.md`)
- Channel follower counts (YouTube, Facebook, Instagram)
- Top performing content across platforms
- Recent YouTube videos performance
- Instagram reach analysis

---

## Manual Runs

If you need individual reports:

```bash
cd "Studio/SEO Content Production/seomachine"

# SEO only
python3 tools/weekly_seo_report.py --domain opened.co --output markdown

# Social only
python3 tools/weekly_social_report.py --output markdown

# Quick stats to console
python3 tools/weekly_social_report.py --output console
```

---

## Data Sources

| Source | Module | Credentials |
|--------|--------|-------------|
| GA4 | `google_analytics.py` | Service account (no expiry) |
| Search Console | `google_search_console.py` | Service account (no expiry) |
| DataForSEO | `dataforseo.py` | API key in .env |
| YouTube | `youtube.py` | Service account (no expiry) |
| Meta (FB + IG) | `meta.py` | Access token (~60 day expiry) |

---

## Troubleshooting

### Meta token expired
1. Go to [developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer)
2. Select OpenEd Analytics app
3. Get Token → Get Page Access Token
4. Update `META_ACCESS_TOKEN` in `seomachine/data_sources/config/.env`

### Missing data
Check credentials in `seomachine/data_sources/config/.env`

---

## Report Location

All reports saved to:
```
Studio/Analytics & Attribution/reports/
├── weekly-seo-2026-01-20.md
├── weekly-social-2026-01-20.md
└── ...
```

---

## Related

- Project docs: `Studio/Analytics & Attribution/PROJECT.md`
- Handoff: `Studio/Analytics & Attribution/HANDOFF-2026-01-20.md`
- Growth strategy: See handoff for Facebook/Instagram growth tactics
