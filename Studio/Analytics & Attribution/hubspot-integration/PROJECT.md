# HubSpot Integration

**Token:** `HUBSPOT_API_KEY_REDACTED`
**Portal:** 45961901

---

## What I Can Do

| Capability | Status |
|------------|--------|
| Read email campaigns + stats | ✅ |
| Read contacts + engagement data | ✅ |
| Read lists + forms | ✅ |
| Clone email from template | ✅ |
| Update subject, preview, body HTML | ✅ |
| **Create complete ready-to-publish drafts** | ✅ |
| **Publish/schedule emails** | ❌ Needs `marketing-email` scope |
| **See workflows** | ❌ Needs `automation` scope |

---

## Key IDs

| Item | ID |
|------|-----|
| OpenEd Daily subscription | `958676154` |
| OpenEd Weekly subscription | `958675573` |
| Daily target list | `1347` (5,551 contacts) |
| Weekly target list | `1357` (20,857 contacts) |
| Newsletter signup form | `dc16907f-11dc-4998-9eab-5c9f97ddbfe8` |

---

## Email Performance (Jan 2026)

| Metric | Daily | Weekly |
|--------|-------|--------|
| Avg Open Rate | 53.5% | 36.3% |
| Avg Click Rate | 2.1% | 2.2% |
| **Unsub Rate** | **0.57%** | **0.58%** |
| List Size | ~2,200 | ~9,000 |

Unsub rates are identical. Daily has higher opens because of tighter list curation.

---

## Subscriber Attribution

**Most granular:** `first_conversion_event_name` property
- Shows page + form: `"Home | OpenEd: OpenEd Daily Primary Form"`
- Shows campaign: `"OpenEd Daily Facebook: Facebook - Daily + State"`

**Source breakdown (106k contacts):**
- 85% OFFLINE (imports/integrations - source lost)
- 7% Direct Traffic
- 3% Organic Search
- 2% Paid Social
- 1% Paid Search

**Application checkbox opt-ins:** 7,767 yes / 2,287 no

---

## Run Commands

```bash
cd "OpenEd Vault/Studio/SEO Content Production/seomachine"

# Email stats
python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.hubspot import HubSpotAnalytics
hs = HubSpotAnalytics()
stats = hs.get_email_stats_summary(30)
print(f'Open Rate: {stats[\"totals\"][\"avg_open_rate\"]}%')
"

# Lists
python3 -c "
from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
from data_sources.modules.hubspot import HubSpotAnalytics
hs = HubSpotAnalytics()
for l in hs.get_lists()[:10]:
    print(f'{l[\"name\"]}: {l[\"count\"]:,}')
"
```

---

## Files

| File | Purpose |
|------|---------|
| `seomachine/data_sources/modules/hubspot.py` | API module |
| `seomachine/data_sources/config/.env` | Token |

---

*Last updated: 2026-01-27*
