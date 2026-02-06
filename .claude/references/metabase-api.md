# Metabase API Reference

**Instance:** https://data.opened.co
**API Key:** `METABASE_API_KEY` in `.env`
**User:** market_team (admin access)
**Created:** 2026-02-04 by McKay Bowman

---

## Quick Start

```bash
# Test connection
curl -s -H "x-api-key: $METABASE_API_KEY" \
  "https://data.opened.co/api/user/current"

# Query a card
curl -s -H "x-api-key: $METABASE_API_KEY" \
  "https://data.opened.co/api/card/865/query" \
  -X POST -H "Content-Type: application/json" \
  -d '{"parameters":[]}'
```

---

## Key Dashboards

| ID | Name | Use Case |
|----|------|----------|
| 115 | Enrollment Funnel Dashboard | Interest forms, funnel stages, state breakdown |
| 19 | Active Student Dashboard | Current enrollment by state/grade |
| 70 | LD Scorecard SY2025-26 | Orders, marketplace, operational KPIs |
| 54 | Enrollment Task Status | Task completion tracking |
| 50 | 25-26 Enrollment | SY25-26 specific metrics |

---

## Key Cards (Queries)

### Enrollment Funnel (Dashboard 115)

| Card ID | Name | Returns |
|---------|------|---------|
| 865 | Enrollment Funnel all years pivot | Funnel stages with counts |
| 956 | Interested Students by state | Daily interest forms by state |
| 958 | Interested Students by Year/State | Year + program + state breakdown |
| 999 | Dm Hubspot Deal | Full deal data with all stages |
| 1000 | Interested Students Last 15 days | Recent interest form activity |
| 884 | Cancelled | Total cancelled count |
| 886 | Transferred | Total transferred count |
| 887 | Withdrawn | Total withdrawn count |
| 889 | State and Program | Full funnel by state/program/year |

### Active Students (Dashboard 19)

| Card ID | Name | Returns |
|---------|------|---------|
| 107 | Number of Active Students | Count by state and grade |
| 118 | Number of Families | Family count |
| 112 | New and Returning Students | Split by student type |

### Operations (Dashboard 70)

| Card ID | Name | Returns |
|---------|------|---------|
| 644 | Orders Last 7 Days | Recent order count |
| 684 | Marketplace Purchases Total | Total dollar amount |
| 645 | SPED Students (504/IEP) | Special ed count |
| 718 | All Programs Active Students | Total active across programs |
| 873 | Tasks Viewer | Enrollment task status breakdown |

---

## Database Structure

**Primary Database:** Snowflake (ID: 11)
**Schema:** DATA_MARTS

### Tables

| Table | Description |
|-------|-------------|
| DM_FUNNEL_VIEW | Enrollment funnel aggregated view |
| DM_HUBSPOT_DEAL | HubSpot deals (one per family) |
| DM_HUBSPOT_DEAL_CONTACT | Deal-contact associations |
| DM_INTERESTED_STUDENTS | Interest form submissions |
| DM_PROGRAM | Program definitions |
| DM_PROGRAM_ENROLLMENT | Individual student enrollments |
| DM_PROGRAM_ENROLLMENT_TASK | Enrollment task tracking |

---

## School Year Mapping

| API Value | Meaning |
|-----------|---------|
| MY26 | Marketing Year 26 = SY26-27 (current recruiting) |
| MY25 | Marketing Year 25 = SY25-26 |
| SY25-26 | School Year 2025-26 (current enrolled) |
| SY26-27 | School Year 2026-27 (next year) |
| Rolling | Academy program (continuous enrollment) |

---

## Funnel Stages

```
INTERESTED → APPLIED → ENROLLING → COMPLETING → ACCEPTED → ENROLLED
                                                      ↓
                              CANCELLED / WITHDRAWN / TRANSFERRED
```

---

## Common Queries

### Get SY26-27 Interest Forms Total

```bash
curl -s -H "x-api-key: $METABASE_API_KEY" \
  "https://data.opened.co/api/card/958/query" \
  -X POST -H "Content-Type: application/json" \
  -d '{"parameters":[]}' | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
rows = d.get('data', {}).get('rows', [])
my26_total = sum(row[3] for row in rows if row[0] == 'MY26' and row[1] == 'OpenEd')
print(f'SY26-27 Interest Forms: {int(my26_total):,}')
"
```

### Get Last 15 Days Activity

```bash
curl -s -H "x-api-key: $METABASE_API_KEY" \
  "https://data.opened.co/api/card/1000/query" \
  -X POST -H "Content-Type: application/json" \
  -d '{"parameters":[]}'
```

### Get Full Funnel by State/Program

```bash
curl -s -H "x-api-key: $METABASE_API_KEY" \
  "https://data.opened.co/api/card/889/query" \
  -X POST -H "Content-Type: application/json" \
  -d '{"parameters":[]}'
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/user/current` | GET | Test auth, get user info |
| `/api/dashboard` | GET | List all dashboards |
| `/api/dashboard/{id}` | GET | Get dashboard details + cards |
| `/api/card/{id}` | GET | Get card/question details |
| `/api/card/{id}/query` | POST | Execute card query |
| `/api/database` | GET | List databases |
| `/api/database/{id}/schemas` | GET | List schemas |
| `/api/database/{id}/schema/{name}` | GET | List tables in schema |
| `/api/collection` | GET | List collections (folders) |

---

## Parameters

Cards with parameters accept them in the POST body:

```json
{
  "parameters": [
    {
      "type": "category",
      "target": ["variable", ["template-tag", "year_param"]],
      "value": "SY26-27"
    }
  ]
}
```

**Common parameters:**
- `year_param` - School year filter
- `state_param` - State filter
- `program_type_param` - Program type (OpenEd, Academy, RISE)
- `test_user` - Include/exclude test users

---

## Current Metrics (as of 2026-02-04)

### SY26-27 (MY26) OpenEd Interest Forms
- **Total:** 7,177
- **Top states:** UT (2,524), OR (1,736), IN (714), NV (531), MN (522)

### Operations
- **Orders (7 days):** 257
- **Marketplace total:** $6.85M
- **SPED students:** 123

### Active Students (SY25-26)
- **Utah alone:** 9,944+ (by grade breakdown)

---

## Notes

- The `testing_user` column in DM_FUNNEL_VIEW doesn't exist (query bug) - use queries without that filter
- MY26 = Marketing Year = the year you're recruiting FOR (SY26-27)
- Dashboard 115 is the primary funnel dashboard referenced in Slack
- Card 889 gives the most complete funnel breakdown by state/program/year

---

*Last updated: 2026-02-04*
