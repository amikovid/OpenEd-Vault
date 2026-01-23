# Lead Magnet Project

**Purpose:** Build OpenEd's email list through valuable free resources that solve specific homeschool parent pain points and naturally lead to OpenEd program awareness.

**Philosophy:** "Comment X to get" social media catnip - quickly consumable answers to the test, not the textbook.

---

## Components

### 1. Curriculove App (curricula.love)
**Location:** `curriculove/`
**Stack:** Next.js 15 + Tailwind + Convex + HubSpot + Gemini
**Status:** In development

A curriculum discovery platform that:
- Captures emails via philosophy quiz gate
- Collects crowdsourced reviews (content moat)
- Promotes OpenEd partner curricula
- Drives program sign-ups in eligible states

**Key docs:**
- `curriculove/PRODUCT-SPEC.md` - Full specification
- `curriculove/docs/QUIZ-REDESIGN.md` - Quiz UX improvements

### 2. PDF Generator
**Location:** `pdf-generator/`
**Purpose:** Generate downloadable lead magnet PDFs from markdown

### 3. Quick Guides (Content)
**Location:** `Quick Guides/`
**Status:** Several drafted, ready for Notion deployment

| Guide | Status | Keyword |
|-------|--------|---------|
| ADHD Starter Kit | Drafted | ADHD |
| Confidence Scripts | Drafted | SCRIPTS |
| Youre-Qualified Reel Captions | Drafted | - |

### 4. Lead Magnet Strategy
**Location:** `OpenEd_Lead_Magnet_Ideas.md`
**Status:** 15+ concepts prioritized

**Tier 1 (Highest Potential):**
1. Confidence Script Collection
2. "What Did We Do Today?" Tracker
3. State-Specific Starter Kits
4. Age-Specific "Don't Panic" Guides
5. "Actually Free" Resource Roundup

### 5. Curriculum Database
**Location:** `110+ Most Popular OpenEd Curriculum Providers/`
**Purpose:** Source content for Curriculove and comparison guides

---

## Workflows

### The 15-Minute Lead Magnet Pipeline
**Documented in:** `NOTION-LEAD-MAGNET-WORKFLOW.md`

```
Step 1: Create in Notion (5 min)
Step 2: Create HubSpot Form (5 min)
Step 3: Deploy CTA via ManyChat or social (5 min)
```

### ManyChat Integration
Comment-to-DM flow captures email before delivering Notion guide link.

---

## Priority Actions

### Immediate
- [ ] Deploy first lead magnet via Notion workflow (Confidence Scripts)
- [ ] Set up ManyChat keyword triggers
- [ ] Test HubSpot email capture flow

### Short-term
- [ ] Complete Curriculove MVP for internal testing
- [ ] Create state-specific guides for AR, UT (high-volume states)
- [ ] Build age-specific guides (K-2 first)

### Medium-term
- [ ] Launch Curriculove at curricula.love
- [ ] Reach 1000 reviews for content moat
- [ ] Integrate quiz results with HubSpot nurture sequences

---

## Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| Email capture rate | 30%+ | Direct funnel to OpenEd |
| Lead magnet downloads | 500/month | List growth |
| Curriculove reviews | 1000 total | Content moat |
| Program sign-ups from leads | 5% conversion | Revenue |

---

## Related Files

- `../Social Media/Platform Insights/instagram.md` - ManyChat strategy
- `.claude/references/opened-program-details.md` - State eligibility
- `OpenEd - Tools.csv` - Full curriculum database

---

*Last Updated: 2026-01-21*
