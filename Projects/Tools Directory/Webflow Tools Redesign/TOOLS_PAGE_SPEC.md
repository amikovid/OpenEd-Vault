# Tools Page Redesign Spec

**Owner:** Ella (design) + Charlie (content)
**Status:** Ready for implementation
**Created:** 2026-01-26

---

## Summary

Redesign the tools page template based on Fred's SEO feedback. Changes affect all 76 tool pages.

---

## Current State

```
[Tab: Our review] [Tab: FAQs & alternatives]

└─ Toggle: Teacher's Take (collapsed by default)
   └─ Byline, intro, Quick Verdict, Best For, May Not Fit
└─ Toggle: What Parents Say (collapsed)
└─ Toggle: How It Works (collapsed)
└─ Toggle: Pricing (collapsed)
```

**Problems:**
- Quick Verdict buried inside Teacher's Take toggle
- No author photo
- FAQs hidden in separate tab
- Accordions collapsed by default (SEO concern)

---

## Target State

```
[Hero: Tool name, grade level, philosophy, tags]

┌─────────────────────────────────────────┐
│ QUICK VERDICT (new section, always visible)
│ One paragraph - OpenEd's high-level take
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ TEACHER'S TAKE                          │
│ [Photo] Author Name, Title              │
│ Personal intro + colleague quotes       │
│ Best For / May Not Fit lists            │
└─────────────────────────────────────────┘

WHAT PARENTS SAY (open by default)
External quotes as prose

HOW IT WORKS (open by default)
Coverage, materials, lesson flow

PRICING (open by default)
Costs + saving tips

FAQS (moved from tab to bottom)
Common questions

ALTERNATIVES (moved from tab to bottom)
Links to similar tools
```

---

## Design Changes (Ella)

### 1. Add Quick Verdict Section
- **Location:** Above Teacher's Take, below hero
- **Content:** New CMS rich text field OR repurpose existing field
- **Style:** Prominent callout box, always visible (not in accordion)

### 2. Add Author Photo Component
- **Location:** Top of Teacher's Take section
- **Source:** Link to Authors CMS collection (already exists: `68089af9024139c740e4b922`)
- **Layout:** Small circular headshot + name + title inline

### 3. Remove Tab UI
- **Current:** "Our review" and "FAQs & alternatives" tabs
- **Target:** Single continuous page, no tabs

### 4. Open Accordions by Default
- **Current:** All toggles start collapsed
- **Target:** All toggles start open (or remove accordion entirely)

### 5. Move FAQs & Alternatives
- **Current:** In separate tab
- **Target:** Regular sections at bottom of page (after Pricing)

---

## CMS Field Changes

| Current Field | Current Content | Change Needed |
|---------------|-----------------|---------------|
| `subject-content` | Teacher's Take (includes Quick Verdict) | Split: extract Quick Verdict to new field |
| `teaching-format-content` | What Parents Say | No change |
| `pricing-content` | How It Works | No change |
| `parent-involvement` | Pricing | No change |
| `parent-feedback-content` | FAQs & Alternatives | No change (just move in template) |
| **NEW: `quick-verdict`** | - | Add new rich text field |
| **NEW: `author` reference** | - | Link to Authors collection |

---

## Content Changes (Charlie/API)

Once Ella confirms template:

1. Write Quick Verdict intros for all 76 tools (extract from existing Teacher's Take)
2. Link author references to Authors collection
3. Batch update via Webflow API

---

## Reference

**Live examples (current format):**
- https://www.opened.co/tools/math-u-see
- https://www.opened.co/tools/saxon-math
- https://www.opened.co/tools/beast-academy-online

**Competitor reference (Fred mentioned):**
- Top-ranking Math-U-See review page (long-form, open content)

**Webflow IDs:**
- Tools Collection: `6811bc7ab1372f43ab83dec6`
- Authors Collection: `68089af9024139c740e4b922`

---

## Questions for Ella

1. Can you add a new CMS field (`quick-verdict`) or should we repurpose an existing one?
2. For author photo - link to Authors collection or add image field directly to Tools?
3. Preference on accordions: keep but open by default, or remove entirely?

---

*Spec created 2026-01-26. Ready for Ella's design review.*
