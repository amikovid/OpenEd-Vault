# SEO Content Production Process

*Documented: 2026-01-29*

Complete workflow from keyword research to Webflow publication.

---

## Overview

This session demonstrated a full SEO content pipeline:

```
KEYWORD RESEARCH → CONTENT BRIEFS → DRAFTS → QUALITY LOOP → WEBFLOW
     ↓                  ↓              ↓           ↓            ↓
 DataForSEO API    seomachine      Templates   5-Judge      API Upload
```

**Result:** 5 comparison articles published as drafts with thumbnails.

---

## Phase 1: Keyword Research

### Tool: DataForSEO API

**Module:** `.claude/skills/seomachine/modules/dataforseo.py`

**Methods used:**
- `get_keyword_ideas(seed, limit)` - Returns related keywords with volume/difficulty
- `get_serp_data(keyword)` - Returns current SERP for competitive analysis

**Process:**
1. Started with seed keywords ("waldorf vs montessori", "homeschool curriculum comparison")
2. Filtered results for comparison patterns (contains "vs", "versus", "compared")
3. Prioritized by volume and relevance to OpenEd audience

**Sample query:**
```python
from modules.dataforseo import DataForSEO
dfs = DataForSEO()
results = dfs.get_keyword_ideas("montessori vs", limit=50)
comparisons = [k for k in results if 'vs' in k['keyword'].lower()]
```

### Keywords Discovered

| Keyword | Monthly Volume | Status |
|---------|----------------|--------|
| waldorf vs montessori | 2,900 | ✅ Published |
| montessori vs reggio emilia | 1,900 | ✅ Published |
| khan academy vs ixl | 590 | ✅ Published |
| unschooling vs homeschooling | 320 | Queued |
| abeka vs bju | 170 | Queued |
| math u see vs saxon | 140 | ✅ Published |
| charlotte mason vs classical | 110 | Queued |

**Master list:** `.claude/skills/seo-content-production/references/comparison-keywords.md`

---

## Phase 2: Content Production

### Template Structure

All comparison articles follow this structure:

1. **Quick comparison table** (featured snippet target)
2. **"What Is [Method A]?"** section
3. **"What Is [Method B]?"** section
4. **Key Differences** (4-5 dimensions)
5. **"Which Is Better For..."** specific audiences
6. **FAQ section** (for featured snippets)
7. **Internal links** (3+ minimum)

### Source Integration

For each article:
1. Search OpenEd proprietary content (podcasts, newsletters, Slack)
2. Extract relevant quotes from mentor teachers
3. Add practical OpenEd-specific value (marketplace, included resources)

---

## Phase 3: Quality Loop

### Skill: `quality-loop`

Every article passed through 5 judges:

| Judge | Type | What It Checks |
|-------|------|----------------|
| Human Detector | BLOCKING | AI tells, forbidden words, patterns |
| Accuracy Checker | BLOCKING | Facts, dates, quotes match sources |
| OpenEd Voice | BLOCKING | Pro-child tone, practical value, 3+ links |
| Reader Advocate | BLOCKING | Hook, flow, scannability |
| SEO Advisor | ADVISORY | Keyword placement, meta elements |

### Automated Quick Check

**File:** `.claude/skills/quality-loop/references/quick-check.md`

Grep patterns for fast AI-tell detection:
```bash
# Forbidden words
grep -inE "delve|comprehensive|crucial|vital|leverage|landscape" DRAFT*.md

# Correlative constructions (auto-fail)
grep -inE "isn't just|not just .* - it's|not about .*, it's about" DRAFT*.md

# Em dashes (should be hyphens with spaces)
grep -n "—" DRAFT*.md
```

---

## Phase 4: Image Generation

### Tool: Gemini API (Nano Banana Pro)

**Skill:** `nano-banana-image-generator`

**Script:** `.claude/skills/nano-banana-image-generator/scripts/generate_image.py`

**Usage:**
```bash
python3 generate_image.py "prompt" \
  --model pro \
  --aspect 16:9 \
  --output "path/to/folder" \
  --name "thumbnail"
```

**Style:** Watercolor-line (default for OpenEd thumbnails)
- Warm watercolor washes
- Gentle ink outlines
- Conceptual, not literal
- No clipart aesthetic

---

## Phase 5: Webflow Publication

### Skill: `webflow-publish`

**API:** Webflow v2 (`https://api.webflow.com/v2`)

### Key IDs

| Resource | ID |
|----------|-----|
| Site | `67c7406fc9e6913d1b92e341` |
| Posts Collection | `6805bf729a7b33423cc8a08c` |
| Blog Post Type | `6805d44048df4bd97a0754ed` |
| Author (Charlie) | `68089b4d33745cf5ea4d746d` |

### Workflow

**Step 1: Upload thumbnail**
```python
# 1a. Get presigned URL
resp = requests.post(
    f"https://api.webflow.com/v2/sites/{SITE_ID}/assets",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"fileName": "thumbnail.png", "fileHash": md5_hash}
)

# 1b. Upload to S3
# IMPORTANT: Cache-Control must be "max-age=31536000, must-revalidate"
```

**Step 2: Convert markdown to HTML**

Key rules:
- Strip metadata lines (`**Meta Title:**`, `**Meta Description:**`, `**URL:**`)
- Replace em dashes (`—`) with spaced hyphens (` - `)
- Convert tables properly (handle `|` delimiters)
- Process links BEFORE bold (so `**[text](url)**` works)
- Skip H1 (becomes `name` field, not in content)

**Step 3: Create post**
```python
payload = {
    "isArchived": False,
    "isDraft": True,
    "fieldData": {
        "name": "Post Title",
        "slug": "post-slug",
        "post-type": [BLOG_POST_TYPE_ID],
        "summary": "Meta description",
        "author": AUTHOR_ID,
        "thumbnail": {"fileId": asset_id, "url": cdn_url},
        "content": html_content  # NO thumbnail in body
    }
}
```

### Common Issues Fixed

| Issue | Cause | Fix |
|-------|-------|-----|
| Metadata in body | Converter didn't strip `**Meta Title:**` | Match bold format, not just italic |
| Tables broken | Empty cells from `\|` delimiters | Filter empty strings after split |
| Em dashes | Not replaced | Global replace before conversion |
| S3 upload failed | Wrong Cache-Control | Use `must-revalidate` not `immutable` |

---

## Files Created This Session

| File | Purpose |
|------|---------|
| `batch_webflow_upload.py` | Batch upload articles to Webflow |
| `update_thumbnails.py` | Upload thumbnails to existing posts |
| `fix_webflow_posts.py` | Fix metadata/table issues |
| `PUBLISH_PACKAGE_2026-01-29.md` | All 5 articles with metadata |
| `CONTENT_OS_EXECUTIVE_SUMMARY.md` | Leadership documentation |
| `SESSION_NOTES_2026-01-29.md` | Full session notes |
| `comparison-keywords.md` | Master keyword list |
| `quick-check.md` | Quality loop automation helpers |

---

## APIs Used

| API | Purpose | Auth |
|-----|---------|------|
| DataForSEO | Keyword research, SERP data | `.env` → `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` |
| Gemini | Image generation | `.env` → `GEMINI_API_KEY` |
| Webflow | CMS publication | `.env` → `WEBFLOW_API_KEY` |

---

## Results

**5 articles published as drafts:**

1. Waldorf vs Montessori (2,900/mo)
2. Montessori vs Reggio Emilia (1,900/mo)
3. Khan Academy vs IXL (590/mo)
4. Saxon Math vs Math-U-See (140/mo)
5. IXL vs Exact Path

**Total monthly search opportunity:** ~5,500+ searches

**Next in queue:**
- Unschooling vs Homeschooling (320/mo)
- Abeka vs BJU (170/mo)
- Charlotte Mason vs Classical (110/mo)

---

## Reproducible Workflow

For future comparison articles:

```bash
# 1. Research keyword
cd ".claude/skills/seomachine"
python3 -c "from modules.dataforseo import DataForSEO; print(DataForSEO().get_keyword_ideas('your keyword vs'))"

# 2. Create draft following Versus template
# Studio/SEO Content Production/Versus/PROJECT.md

# 3. Run quality loop
# Use quality-loop skill or quick-check.md grep patterns

# 4. Generate thumbnail
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" "prompt" --model pro --aspect 16:9

# 5. Upload to Webflow
python3 "Studio/SEO Content Production/batch_webflow_upload.py"
```

---

*Process documented for repeatability and team onboarding.*
