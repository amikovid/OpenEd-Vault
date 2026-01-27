# Analytics & Attribution

**Marketing analytics infrastructure** - Connect the dots from content channels to subscriber acquisition to enrollment revenue.

**Status:** Active - HubSpot module complete
**Location:** `Studio/Analytics & Attribution/`
**Ops Contact:** TBD (request HubSpot permissions)

---

## Quick Navigation (Start Here)

### Related Projects
- `../KPI Discussions/Q3-2026-strategy-spec.md` - Q3 strategy and compensation spec
- `../Retargeting Strategy FY26-27/PROJECT.md` - Paid social (needs pixel tracking)
- `../Social Media/Frictionless Content Engine/PROJECT.md` - Content production
- `../Lead Magnet Project/curriculove/PROJECT.md` - Curricula lead tracking

### Key Files
- `../Master_Content_Index.md` - 406 articles (content to track)
- `../Social_Scheduling.md` - Active social posts

### External Systems
- **GA4:** https://analytics.google.com
- **HubSpot:** https://app.hubspot.com
- **Webflow:** https://webflow.com
- **Databox:** Ask Alex for access (has existing dashboards)

---

## QBR Action Items (2026-01-26)

| Action | Status | Notes |
|--------|--------|-------|
| Show Melissa Search Console integration | ⏳ Tomorrow | Add to 1:1 agenda |
| Set up Monday morning SEO report to Slack | ⏳ This week | Pages getting closer to page 1 |
| Request Databox access from Alex | ⏳ This week | He has existing dashboards |
| YouTube ads research | ✅ Complete | See `youtube-vs-meta-ads-research.md` |

**YouTube Ads Recommendation:** Test $1,500-2,000 over 8 weeks for fall enrollment. Video Action Campaigns with lead forms, targeting ESA states.

---

## Getting Started (For New Sessions)

### 1. Check What's Already Tracked
```bash
# Review Q3 strategy context
Read: Studio/KPI Discussions/Q3-2026-strategy-spec.md

# Check retargeting (depends on pixel setup)
Read: Studio/Retargeting Strategy FY26-27/PROJECT.md
```

### 2. Verify Access
- [ ] GA4 - confirm events and conversions are firing
- [ ] Webflow - check analytics integration
- [ ] HubSpot - verify contact/lead access level

### 3. Report Back
What I need from you:
- Current HubSpot access level
- Whether enrollment data is in HubSpot or separate system
- Any existing dashboards or reports

---

## Vision

Build the full funnel view:
```
Channel → Traffic → Subscriber → Lead → Enrollment → Revenue
   ↑                    ↑           ↑         ↑          ↑
  GA4              HubSpot      HubSpot    ???      LTV calc
```

When this is done, every marketing activity can be traced to revenue impact.

---

## Current State

| System | Access | Status |
|--------|--------|--------|
| **Google Analytics 4** | Full | ✅ Working (tested 2026-01-20) |
| **Google Search Console** | Full | ✅ Working (tested 2026-01-20) |
| **DataForSEO** | Full | ✅ Working (tested 2026-01-20) |
| **YouTube Data API** | Full | ✅ Working (tested 2026-01-20) |
| **Meta (FB + IG)** | Full | ✅ Working (tested 2026-01-20) |
| **Webflow** | Full | Active |
| **HubSpot** | Partial | ✅ Contacts working (no lists/forms) |
| **Enrollment system** | Unknown | Need to identify |

---

## Data Source Modules

All modules live in `../SEO Content Production/seomachine/data_sources/modules/`

| Module | File | Status |
|--------|------|--------|
| Google Analytics 4 | `google_analytics.py` | ✅ Working |
| Google Search Console | `google_search_console.py` | ✅ Working |
| DataForSEO | `dataforseo.py` | ✅ Working |
| YouTube | `youtube.py` | ✅ Working |
| Meta (FB + IG) | `meta.py` | ✅ Working |
| HubSpot CRM | `hubspot.py` | ✅ Working |
| HubSpot Insights | `hubspot_insights.py` | ✅ Working |

### YouTube Setup ✅ Complete

Channel ID: `UCzfHIDt2uKzwEclA94tom_Q` (OpenEd / Unstandard Education)
- 1,160 subscribers | 301,761 total views | 497 videos

### Meta Setup ✅ Complete

- **Facebook:** OpenEd HQ (5,146 followers)
- **Instagram:** @openedhq (2,200 followers, 547 posts)
- Token expires ~60 days - regenerate via Graph API Explorer

### HubSpot Setup ✅ Full Access (Updated 2026-01-26)

Portal ID: `45961901`
**Token:** `HUBSPOT_API_KEY_REDACTED`

**Available scopes:**
- `content` - Email campaigns, landing pages, blog
- `business-intelligence` - Analytics API
- `crm.lists.read`, `crm.lists.write` - List management
- `forms`, `forms-uploaded-files` - Form data
- `communication_preferences.read`, `communication_preferences.read_write` - Subscriptions
- `crm.objects.contacts.read`, `crm.objects.contacts.write` - Contacts
- `files` - File manager

**Modules:**
- `hubspot.py` - Core CRM + email analytics
- `hubspot_insights.py` - Automated pattern detection

**Reports:**
- `weekly_hubspot_report.py` - Weekly attribution report
- `hubspot_deep_dive.py` - Comprehensive audit

**Key Features (CRM):**
- Source attribution (organic, paid, social, referral, direct)
- Landing page conversion tracking
- Curriculove lead magnet analytics
- Funnel conversion rates
- Week-over-week trends

**Key Features (Email - NEW):**
- Campaign stats: sent, opens, clicks, bounces, unsubs
- Open/click rates by campaign
- Link click tracking (which URLs clicked)
- Subscription type management
- List membership and growth

**Run Reports:**
```bash
cd "Studio/SEO Content Production/seomachine"

# Email stats summary
python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.hubspot import HubSpotAnalytics
hs = HubSpotAnalytics()
stats = hs.get_email_stats_summary(limit=30)
print(f'Avg Open Rate: {stats[\"totals\"][\"avg_open_rate\"]}%')
print(f'Avg Click Rate: {stats[\"totals\"][\"avg_click_rate\"]}%')
"

# Full marketing dashboard
python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.hubspot import HubSpotAnalytics
import json
hs = HubSpotAnalytics()
print(json.dumps(hs.get_full_marketing_dashboard(), indent=2))
"

# Lists with member counts
python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.hubspot import HubSpotAnalytics
hs = HubSpotAnalytics()
for l in hs.get_lists()[:10]:
    print(f'{l[\"name\"]}: {l[\"count\"]:,}')
"
```

### Weekly SEO Report

Run: `python3 tools/weekly_seo_report.py` from seomachine folder

Generates: Priority keyword tracking, quick wins, declining content, opportunities

---

## Success Criteria

### Phase 1: Audit & Access (Week 1-2)
- [ ] Verify GA4 tracking is clean (events, conversions)
- [ ] Map Webflow → GA4 integration
- [ ] Request full HubSpot access from Ops
- [ ] Identify where enrollment data lives

### Phase 2: Attribution Setup (Week 3-4)
- [ ] Ensure subscriber source tracking is clean in HubSpot
- [ ] Create/configure lead source properties
- [ ] Build subscriber acquisition report (by channel, by week)

### Phase 3: Revenue Attribution (Week 5-8)
- [ ] Connect subscriber → lead → enrollment journey
- [ ] Calculate channel-level enrollment attribution
- [ ] Estimate LTV by acquisition source

### Phase 4: Dashboard (Ongoing)
- [ ] Build monthly attribution dashboard
- [ ] Decide on dashboard location (HubSpot? Notion? Custom?)
- [ ] Automate refresh

---

## Key Questions

1. **Where does enrollment data live?**
   - CRM? Separate system? Need to find out.

2. **What's the lead-to-enrollment timeline?**
   - Affects attribution window

3. **Do we have LTV data by cohort?**
   - Needed to calculate true channel value

4. **Dashboard home:**
   - HubSpot (if all data is there)
   - Notion (if we need to stitch sources)
   - Custom (websocket/app if complex)

---

## Ops Request Draft

```
Subject: HubSpot Access Request for Marketing Attribution

Hi [Ops contact],

I'm building out marketing attribution to track the full funnel from content → subscribers → enrollment. This will help us understand which channels actually drive revenue.

I need access to:
1. Full HubSpot contact/lead data
2. Lead stage and source properties
3. Enrollment/deal data (if in HubSpot)

If enrollment data lives elsewhere, can you point me to the right person/system?

Thanks,
[Name]
```

---

## Dashboard Requirements

### Core Metrics
- Subscriber growth (total, by source)
- Traffic by channel (GA4)
- Lead creation (HubSpot)
- Enrollment (source TBD)

### Attribution Views
- Channel → Subscriber rate
- Subscriber → Lead rate
- Lead → Enrollment rate
- Channel → Revenue (the holy grail)

### Refresh Cadence
- Weekly for operational use
- Monthly for reporting

---

## Technical Options

### Option A: HubSpot Native
If all data can live in HubSpot:
- Use HubSpot dashboards and reports
- Cleanest, least maintenance
- Limited by HubSpot's capabilities

### Option B: Notion Dashboard
If we need to stitch sources:
- Pull from GA4 API + HubSpot API
- Display in Notion via embed or manual update
- More flexible, more maintenance

### Option C: Custom App
If we need real-time or complex:
- Build simple dashboard app
- WebSocket for live data
- Most powerful, most effort

**Recommendation:** Start with HubSpot native, escalate only if limited.

---

## Links

- KPI spec: `../KPI Discussions/Q3-2026-strategy-spec.md`
- HubSpot docs: https://knowledge.hubspot.com/
- GA4 docs: https://support.google.com/analytics/

---

*Created: 2026-01-20*
