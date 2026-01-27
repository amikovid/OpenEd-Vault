# OpenEd Tool Review Template

**Title Tag:** `[Tool Name] Review: Pros, Cons, Pricing, Alternatives | OpenEd`
**Meta:** `Review of [Tool Name] for homeschooling. See pricing, key features, who it's best for, pros and cons, and parent feedback.`

---

## Page Structure

### H1: [Tool Name] Review (page title - automatic)

### Toggle 1: Teacher's Take
**CMS Field:** `subject-content`

- Author byline: *Reviewed by [Name], OpenEd Teacher*
- Personal intro hook (1-2 paragraphs)
- Weave in colleague quotes naturally ("My colleague Keely notes...")
- **H2: Quick Verdict** - One paragraph summary
- **H2: Who [Tool] Is Best For** - Bullet list
- **H2: Who [Tool] May Not Fit** - Bullet list (honest)

### Toggle 2: What Parents Say
**CMS Field:** `teaching-format-content`

- External community quotes (blogs, forums)
- Woven as prose, not stacked blockquotes
- Link to source blogs

### Toggle 3: How It Works
**CMS Field:** `pricing-content`

- **H2: What [Tool] Covers** - Subjects, grade levels
- **H2: [Tool] Materials** - What's included
- **H2: [Tool] Lesson Flow** - Daily/weekly structure
- **H2: Parent Involvement** - Time commitment

### Toggle 4: Pricing
**CMS Field:** `parent-involvement`

- **H2: [Tool] Pricing** - Costs, tiers
- **H2: Cost-Saving Tips** - Bullet list

### Toggle 5 (or Tab): FAQs & Alternatives
**CMS Field:** `parent-feedback-content`

- **H2: [Tool] FAQs** - 4-6 common questions
- **H2: Alternatives to [Tool]** - 3-5 options with internal links

---

## Webflow CMS Field Mapping

| Toggle Label | CMS Field | Content |
|--------------|-----------|---------|
| Teacher's Take | `subject-content` | Author intro, verdict, best for / not for |
| What Parents Say | `teaching-format-content` | External quotes as prose |
| How It Works | `pricing-content` | Coverage, materials, lesson flow, parent role |
| Pricing | `parent-involvement` | Costs, savings tips |
| FAQs & Alternatives | `parent-feedback-content` | Common questions + alternatives |

---

## Source Priority

| Section | Voice | Source |
|---------|-------|--------|
| Teacher's Take | Author | Slack quotes, podcast, interviews |
| What Parents Say | External | Homeschool blogs, forums |
| How It Works | Factual | Official site |
| Pricing | Factual | Official site |
| FAQs & Alternatives | Mixed | Research + author perspective |

---

## Workflow

1. **Mine Slack** for tool mentions and teacher quotes
2. **Identify primary author** (teacher with most quotes/experience)
3. **Draft Teacher's Take** weaving in colleague voices
4. **Source external quotes** for What Parents Say
5. **Fill How It Works + Pricing** from official site
6. **Write FAQs** using search-phrasing questions
7. **Push to Webflow** via API
8. **Publish**

---

## Anti-AI Writing Checklist

- [ ] No correlative constructions ("X isn't Y - it's Z")
- [ ] No em dashes (use hyphens with spaces - like this)
- [ ] No: delve, comprehensive, crucial, leverage, landscape, navigate
- [ ] No: "The best part?", "Here's the thing:", "Let's be honest"
- [ ] Tool name in H2 headers (e.g., "Math-U-See Pricing")
- [ ] Named sources, not "experts say"

---

*Updated: 2026-01-22*
