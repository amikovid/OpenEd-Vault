# Notion Lead Magnet Workflow

**Purpose:** Streamlined process to create quick Notion guides and connect them to lead capture.

**Why Notion:** 
- Zero dev work (no landing page needed)
- Beautiful by default
- Shareable with one link
- Can update content anytime without re-uploading
- Mobile-friendly

---

## The 15-Minute Lead Magnet Pipeline

### Step 1: Create in Notion (5 min)

1. Duplicate the **Lead Magnet Template** (see below)
2. Fill in the content
3. Click **Share** → **Publish to web**
4. Copy the public URL

### Step 2: Create HubSpot Form (5 min)

1. Go to HubSpot → Marketing → Forms
2. Create new form with fields:
   - Email (required)
   - First Name (optional but recommended)
3. Add hidden field: `lead_magnet_source` = guide name
4. Thank you page → Redirect to Notion URL
5. Copy form embed code OR get direct form link

### Step 3: Deploy CTA (5 min)

**For ManyChat (Instagram):**
- Create flow: Keyword trigger → Ask for email → Send Notion link
- Keywords: GUIDE, FREEBIE, [specific keyword]

**For Social Posts:**
- Link in bio → HubSpot form → Notion guide
- Or: "Comment [KEYWORD] and I'll DM you the link"

**For Paid Ads:**
- HubSpot form as landing page
- On submit → Redirect to Notion guide

---

## Notion Lead Magnet Template

Copy this structure for each new guide:

```
[TITLE] - Free Guide from OpenEd

---

[Opening hook - 2-3 sentences that validate their struggle]

---

## Section 1: [Specific Actionable Thing]

[Content - 100-200 words max]

---

## Section 2: [Another Specific Thing]

[Content]

---

## Section 3: [Final Thing]

[Content]

---

## Want More Help?

[Soft pitch for OpenEd]

📧 Questions? Reply to the email you got this from.

---

*© 2026 OpenEd | [Website Link]*
```

### Template Rules

1. **One page max** - No clicking through
2. **3-5 sections** - Scannable chunks
3. **Specific and actionable** - Not "think about your goals"
4. **No fluff intro** - Start with value immediately
5. **Soft CTA at end** - Don't hard sell

---

## Lead Magnet Ideas (Quick Wins)

These can each be created in under 30 minutes:

| Guide | Keyword | Audience Pain |
|-------|---------|---------------|
| 5 Questions to Ask Before Choosing Curriculum | COMPARE | Decision paralysis |
| Scripts for the Socialization Question | SCRIPTS | Social anxiety |
| [STATE] Homeschool Checklist | [STATE] | Legal confusion |
| The One-Page Learning Log | TRACKER | Record keeping guilt |
| What 5-Year-Olds Actually Need | KINDY | Kindergarten pressure |
| Middle School Sanity Check | MIDDLE | Tween transition fears |
| High School Without Anxiety | HIGHSCHOOL | Graduation worries |
| First Week Survival Guide | FIRSTWEEK | Getting started panic |

---

## Tracking & Attribution

### HubSpot Properties to Create

| Property | Type | Purpose |
|----------|------|---------|
| `lead_magnet_name` | Single-line text | Which guide they downloaded |
| `lead_source` | Dropdown | instagram_dm, fb_ad, organic_social |
| `utm_campaign` | Single-line text | Campaign tracking |

### UTM Convention

```
?utm_source=instagram&utm_medium=dm&utm_campaign=adhd_guide
?utm_source=facebook&utm_medium=paid&utm_campaign=curriculum_compare
```

Add UTMs to the Notion link when possible for better tracking.

---

## ManyChat Integration Details

### Comment-to-DM Flow

```
Trigger: Comment contains "GUIDE" (or specific keyword)
↓
Action: Send DM
"Hey! I've got that guide ready for you. 📚

Quick question - what's your email? I'll send it there too so you can find it later."
↓
User replies with email
↓
Action: Tag user as [lead_magnet_name]
Action: Send to HubSpot via webhook (if configured)
Action: Send DM with Notion link
"Perfect! Here's your guide: [Notion Link]

Let me know if you have any questions!"
```

### Webhook to HubSpot

If ManyChat Pro:
1. Add "HTTP Request" action
2. POST to HubSpot Contact API
3. Include email + lead_magnet_name + source=instagram_dm

---

## Quality Checklist

Before publishing any lead magnet:

- [ ] Title passes the "would I click this?" test
- [ ] Opens with validation, not definition
- [ ] Each section is actionable (not just information)
- [ ] Under 1,000 words total
- [ ] No AI-isms (delve, comprehensive, journey, etc.)
- [ ] Soft CTA at end, not hard sell
- [ ] Mobile-readable (preview on phone)
- [ ] Notion page published to web
- [ ] HubSpot form created
- [ ] Thank you redirect points to Notion URL
- [ ] UTM tracking in place

---

## Example: End-to-End

**Guide:** "Scripts for the Socialization Question"

1. **Create:** Notion page with 5 word-for-word scripts
2. **Publish:** Share → Publish to web → Copy link
3. **Form:** HubSpot form, redirect to Notion link
4. **Deploy:** 
   - Instagram post with "Comment SCRIPTS"
   - ManyChat flow triggers on "SCRIPTS"
   - Collects email, sends Notion link
5. **Track:** lead_magnet_name = "socialization_scripts", source = "instagram_dm"

**Time:** ~20 minutes total

---

## Related Files

- `OpenEd_Lead_Magnet_Ideas.md` - Full list of lead magnet concepts
- `Quick Guides/` - Existing guide content (can convert to Notion)
- `../Social Media/Platform Insights/instagram.md` - ManyChat strategy details

---

*Created: 2026-01-20*
