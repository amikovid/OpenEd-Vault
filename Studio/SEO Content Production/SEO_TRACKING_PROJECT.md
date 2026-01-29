# SEO Tracking Project

Track performance of SEO content over time using GSC and GA4 data.

---

## Setup Status

### Required Credentials

Add these to `.env`:

```bash
# Google OAuth (shared by GSC and GA4)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REFRESH_TOKEN=

# GA4 specific
GA4_PROPERTY_ID=

# DataForSEO (already configured)
DATAFORSEO_LOGIN=cdeist@opened.co
DATAFORSEO_PASSWORD=22e9510f77b0d182
```

### Setup Steps

1. [ ] **Create Google Cloud Project** (or use existing)
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create project or select existing

2. [ ] **Enable APIs**
   - [Search Console API](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com)
   - [Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)

3. [ ] **Create OAuth Credentials**
   - APIs & Services → Credentials → Create OAuth client ID
   - Application type: Desktop app
   - Download JSON, extract client_id and client_secret

4. [ ] **Configure OAuth Consent Screen**
   - Add scopes: `webmasters.readonly`, `analytics.readonly`
   - Add your email as test user

5. [ ] **Get Refresh Token**
   - Run auth flow to get refresh token
   - Add to `.env`

6. [ ] **Find GA4 Property ID**
   - GA4 Admin → Property Settings → Property ID

---

## Content to Track

### Active SEO Articles

| Article | URL | Published | Target KW | Status |
|---------|-----|-----------|-----------|--------|
| Waldorf vs Montessori | /blog/waldorf-vs-montessori | TBD | waldorf vs montessori | Draft ready |
| Montessori Curriculum | /blog/montessori-curriculum-for-homeschooling | 2025-09-24 | montessori homeschool | Live |
| Classical Education | /blog/classical-education | 2025-08-20 | classical education | Live |

### Planned Articles (from keyword research)

| Priority | Article | Target KW | Volume | KD |
|----------|---------|-----------|--------|-----|
| 1 | Waldorf vs Montessori | waldorf vs montessori | 5,800 | 8 |
| 2 | Montessori vs Reggio Emilia | montessori vs reggio emilia | 3,800 | 2 |
| 3 | Montessori vs Traditional | montessori vs traditional | 520 | 2 |
| 4 | Charlotte Mason vs Classical | charlotte mason vs classical | 210 | 7 |

---

## Tracking Schedule

### Weekly Check (Fridays)

```bash
# Top queries bringing traffic
python3 .claude/skills/gsc/scripts/gsc_query.py top-queries \
  --site "https://opened.co" \
  --days 7 \
  --limit 30

# New article rankings
python3 .claude/skills/gsc/scripts/gsc_query.py search-analytics \
  --site "https://opened.co" \
  --days 7 \
  --dimensions query page \
  --filter "page=/blog/waldorf-vs-montessori"
```

### Monthly Report

```bash
# Top pages
python3 .claude/skills/gsc/scripts/gsc_query.py top-pages \
  --site "https://opened.co" \
  --days 28

# CTR opportunities
python3 .claude/skills/gsc/scripts/gsc_query.py opportunities \
  --site "https://opened.co" \
  --days 28 \
  --min-impressions 100

# Traffic by source (GA4)
python3 .claude/skills/ga4/scripts/ga4_query.py \
  --metric sessions \
  --dimensions sessionSource,sessionMedium \
  --limit 20
```

---

## Performance Baselines

*To be filled after tracking begins*

### Comparison Articles Baseline

| Article | Week 1 | Month 1 | Month 3 | Month 6 |
|---------|--------|---------|---------|---------|
| Waldorf vs Montessori | - | - | - | - |

---

## Integration with Skills

| Skill | Purpose |
|-------|---------|
| `seo-content-production` | Create new articles |
| `gsc` | Search Console data |
| `ga4` | Analytics data |
| `seo-research` | Keyword research (DataForSEO) |
| `webflow-publish` | Publish to site |

---

## Notes

- GSC data has ~3 day delay
- New pages take 1-2 weeks to appear in GSC
- Track position changes weekly for first 3 months
- Refresh content annually based on performance

---

*Created: 2026-01-28*
