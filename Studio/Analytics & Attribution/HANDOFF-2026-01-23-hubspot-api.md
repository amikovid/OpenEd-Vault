# HubSpot API Integration - Session Handoff

**Date:** 2026-01-23
**Status:** Partially working - CRM access only, marketing scopes needed

---

## What Was Built

Created comprehensive HubSpot analytics module with 4 files:

| File | Location | Purpose |
|------|----------|---------|
| `hubspot.py` | `seomachine/data_sources/modules/` | Core API module |
| `hubspot_insights.py` | `seomachine/data_sources/modules/` | Automated pattern detection |
| `weekly_hubspot_report.py` | `seomachine/tools/` | Weekly attribution report |
| `hubspot_deep_dive.py` | `Analytics & Attribution/` | One-time audit script |

---

## What Works Now

**Using:** Private app token `HUBSPOT_API_KEY_REDACTED`
**Scope:** `crm.objects.contacts.read`, `crm.objects.contacts.write`

Working queries:
- Contact source attribution (organic, paid, direct, social, etc.)
- Landing page conversions
- Lifecycle stage funnel (subscriber → lead → customer)
- State distribution
- Weekly/monthly signup trends
- Custom properties (including Curriculove fields)

**Sample data retrieved:**
- OFFLINE: 354 contacts (bulk imports?)
- DIRECT_TRAFFIC: 75
- ORGANIC_SEARCH: 56
- Top states: UT (299), OR (247), NM (203), TX (190)

---

## What Doesn't Work (Missing Scopes)

| Feature | Required Scope | Status |
|---------|---------------|--------|
| Marketing emails | `content` | ❌ Not available |
| Email open/click rates | `content` | ❌ Not available |
| Forms | `forms` | ❌ Not available |
| Lists | `contacts-lists-read` | ❌ Not available |

---

## Token/Access Situation

**20 private apps exist** - at the limit, can't create new ones

**Tokens tested:**
1. Original `.env` token (`CiRuYTEt...`) - Expired/invalid (showed 1970 expiration)
2. Private app token (`HUBSPOT_KEY_REDACTED`) - ✅ Working for CRM
3. Developer API key (`e9811754-ffaa...`) - For dev platform only, not CRM access
4. Personal access key - Same format as expired token, likely same issue

**HubSpot MCP Server** - Available in beta, but limited to CRM objects (same as what we have)

---

## To Get Marketing Data

Someone with admin access needs to:

1. **Option A:** Edit existing private app to add scopes
   - Go to Settings → Integrations → Private Apps
   - Find the app we're using
   - Add scopes: `content`, `forms`, `contacts-lists-read`
   - Token may regenerate

2. **Option B:** Find existing app with marketing scopes
   - Check all 20 private apps for one with `content` scope
   - Look for apps with "marketing" or "email" in name/description

3. **Option C:** Request from ops/admin
   - They may have a reason for restricting marketing API access
   - Ask which app has email/marketing permissions

---

## Questions to Answer with Full Access

Once marketing scopes are available:

1. **Email attribution:** Which campaigns drive the most subscribers?
2. **Open rates by source:** Do organic contacts engage better with email than paid?
3. **Form performance:** Which forms convert best?
4. **List growth:** How are key lists growing over time?

---

## Run Commands

```bash
# Test current access
cd "Studio/SEO Content Production/seomachine"
python3 -c "
from dotenv import load_dotenv
load_dotenv('data_sources/config/.env')
from data_sources.modules.hubspot import HubSpotAnalytics
hs = HubSpotAnalytics()
print(hs.get_contacts_by_source(days=30, max_contacts=100))
"

# Weekly report (CRM data only)
python3 tools/weekly_hubspot_report.py --output markdown

# Deep dive audit
cd "Studio/Analytics & Attribution"
python3 hubspot_deep_dive.py
```

---

## Files Modified

- `OpenEd Vault/.env` - Updated HUBSPOT_API_KEY
- `seomachine/data_sources/config/.env` - Updated HUBSPOT_API_KEY
- `Analytics & Attribution/PROJECT.md` - Updated status

---

## Next Steps

1. [ ] Get marketing scopes added to a private app (requires admin)
2. [ ] Once available, add email analytics to `hubspot.py`
3. [ ] Run full deep dive with complete access
4. [ ] Build email attribution into weekly report

---

*Session ended: 2026-01-23*
