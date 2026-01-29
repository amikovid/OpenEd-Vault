# Q3 Stretch Goal & Ideal Structure

**Created:** 2026-01-27
**Purpose:** Proposal for Melissa on stretch metric + contractor structure

---

## Part 1: Stretch Metric Proposal

### The Goal

**Metric:** Curriculove → Application Conversion

**Target:** 100 applications sourced from Curriculove in H1 (Jan-June)

**Payout:** $2,500 if hit

### Why This Metric

1. **Directly tied to growth** - Applications are what the company cares about
2. **Tests the lead magnet thesis** - Does Curriculove actually convert?
3. **I can influence it** - I own the funnel from Curriculove → nurture → app
4. **Clean attribution** - We can tag Curriculove leads distinctly

### The Funnel

```
Curriculove Quiz Complete
    ↓
Email Captured (tagged: source = curriculove)
    ↓
Nurture Sequence (3-5 emails, curriculum-focused)
    ↓
Interest Form / Application Start
    ↓
Application Complete
```

### Tracking Requirements

| Stage | How to Track | Status |
|-------|--------------|--------|
| Quiz complete | Curriculove → HubSpot via API | ✅ Working |
| Email captured | HubSpot contact created | ✅ Working |
| Source tag | Custom property: `lead_source = curriculove` | ⚠️ Need to set up |
| Nurture sequence | HubSpot workflow | ⚠️ Need to build |
| Interest form | Form submission | ✅ Exists |
| Application complete | Lifecycle stage = Applicant | ⚠️ Data accuracy issues |

### What I Need From Ops

**Request to Adam/Luke (by Feb 10):**

1. **Confirm lifecycle stage accuracy** - Melissa said this is being fixed. I need to know when it's reliable.

2. **Create or confirm these HubSpot properties exist:**
   - `original_lead_source` (single select: curriculove, organic, paid, referral, etc.)
   - `curriculove_quiz_date` (date)
   - `curriculove_philosophy_match` (text - their result)

3. **Build a report or list:**
   - Contacts where `original_lead_source = curriculove`
   - Cross-referenced with `lifecycle_stage = applicant` or `customer`
   - With date filtering so I can track month-over-month

4. **Newsletter overlap report:**
   - How many contacts on the Daily newsletter list are also `lifecycle_stage = customer`?
   - This answers Melissa's question: "Is the newsletter a retention tool?"

### Baseline Data Needed

Before I can set a realistic target, I need to know:

| Question | Data Source | Who Owns |
|----------|-------------|----------|
| Current newsletter → app conversion rate | HubSpot | Ops |
| How many newsletter subs are enrolled families? | HubSpot list + lifecycle | Ops |
| Historical organic subscriber → applicant rate | HubSpot | Ops |
| Curriculove signups to date | Convex dashboard | Me |

**If I can't get this from Ops by Feb 7**, I'll set the target based on assumptions and adjust next quarter.

---

## Part 2: Data Request Summary

### Email to Adam/Alex (Send Today)

```
Subject: Data request for Q3 goals - need by Feb 10

Hey Adam/Alex,

For Q3 planning, I need a few data points. Melissa and I discussed tying my stretch goal to subscriber → applicant conversion, but I need baseline data.

**Request 1: Newsletter audience breakdown**
- Of the ~1,900 contacts on the Daily newsletter list, how many are:
  - Lifecycle stage = Customer (enrolled families)
  - Lifecycle stage = Lead or Subscriber (prospects)
  - Lifecycle stage = Applicant (in funnel)

This tells us if the newsletter is a retention tool or acquisition tool.

**Request 2: Historical conversion rate**
- Of contacts who subscribed to the newsletter in the last 12 months, what % eventually became Applicants?
- If possible, broken down by original source (organic, paid, referral)

**Request 3: Custom property setup**
- Can we add `original_lead_source` as a property? I want to tag Curriculove leads distinctly so I can track their conversion separately.

I know lifecycle stage data is being cleaned up with target date Feb 10. Happy to wait for accurate data rather than pull bad numbers now.

Thanks,
Charlie
```

---

## Part 3: Ideal Structure (For Melissa)

### Current State

| Role | Person | Hours/Week | Monthly Cost |
|------|--------|------------|--------------|
| Head of Content | Charlie | 27-30 | ~$6,500 (salary) |
| Content Associate | Chavilah | 25 | ~$2,000 (intern rate?) |
| Podcast Editor | Angel | ~20 | ~$600 |
| **Total** | | ~75 hrs | ~$9,100 |

### Proposed State (Q3-Q4)

| Role | Person | Hours/Week | Monthly Cost |
|------|--------|------------|--------------|
| **Content Lead** (strategic) | Charlie | 20-25 | ~$5,500 |
| **Content Ops** (execution) | Chavilah (FT) | 40 | ~$3,500? |
| **Senior Editor** (polish) | Linda Taylor | 5 | ~$1,000 |
| **Video/Ads Creative** | Elijah | 10-15 | ~$1,500 |
| **Podcast Editor** | Angel | 10 | ~$400 |
| **Total** | | ~80-95 hrs | ~$11,900 |

**Net increase:** ~$2,800/month for significantly more capacity

### What Each Person Owns

**Charlie (20-25 hrs) - Strategy & Architecture**
- Content engine design and maintenance
- SEO strategy and keyword targeting
- Curriculove development and launch
- High-judgment editorial decisions
- Training and oversight
- Stretch goal: Curriculove → Application conversion

**Chavilah (40 hrs) - Core Operations**
- Newsletter drafting (from templates/skills)
- Social media scheduling and posting
- Nearbound outreach execution
- Podcast production (taking over from Angel)
- Webflow content updates
- State launch checklist execution

**Linda Taylor (5 hrs) - Quality & Polish**
- Final edit pass on SEO articles
- Newsletter proofread before send
- Tool reviews from interview transcripts
- Overflow long-form writing

**Elijah (10-15 hrs) - Video & Paid Creative**
- Short-form video production (Reels, TikTok, Shorts)
- Retargeting ad creative refresh
- Meta/YouTube ad concepts
- Organic social experiments

**Angel (10 hrs) - Reduced Role**
- Long-form podcast clips (supervised by Chavilah)
- Descript specialist tasks only
- May phase out as Chavilah absorbs podcast workflow

### The Shift

| From | To |
|------|-----|
| Charlie doing 6 jobs | Charlie doing 2 jobs (strategy + oversight) |
| No video capacity | Elijah fills the gap |
| No senior editor | Linda fills the gap |
| Chavilah part-time | Chavilah full-time, running daily ops |
| Angel as podcast person | Angel reduced, Chavilah absorbs |

### Budget Ask

| Line Item | Monthly |
|-----------|---------|
| Chavilah FT upgrade | +$1,500 (estimate) |
| Linda Taylor | $1,000 |
| Elijah | $1,500 |
| **New monthly spend** | ~$4,000 |
| **Offset by Angel reduction** | -$200 |
| **Net new** | ~$3,800/month |

**ROI case:** This unlocks video (our biggest gap), improves content quality, and frees me to focus on growth strategy that drives applications.

---

## Part 4: Timeline

| Date | Milestone |
|------|-----------|
| **This week** | Send data request to Ops |
| **This week** | Start Elijah on retargeting creative |
| **Jan 31 (Fri)** | Curriculove Show & Tell |
| **Feb 7** | Finalize stretch metric with baseline data |
| **Feb 10** | Ops delivers clean lifecycle data |
| **Feb 14** | Ideal structure doc to Melissa |
| **Feb 28** | Chavilah decision finalized |
| **Mar 1** | New structure in place |

---

## Part 5: Immediate Actions

### Today

- [ ] Send data request email to Adam/Alex
- [ ] Message Elijah - confirm he's ready to start
- [ ] Set up `original_lead_source` property in HubSpot (if I have access)
- [ ] Pull Curriculove signup count from Convex

### This Week

- [ ] Build Curriculove → HubSpot nurture sequence (draft)
- [ ] Friday: Curriculove internal demo
- [ ] Get test reviews from marketing team

### Next Week

- [ ] Follow up on data request
- [ ] Finalize stretch metric target
- [ ] Send ideal structure doc to Melissa

---

## Appendix: HubSpot Properties to Request

| Property | Type | Purpose |
|----------|------|---------|
| `original_lead_source` | Single select | Track where contact first came from |
| `curriculove_quiz_date` | Date | When they completed the quiz |
| `curriculove_philosophy` | Text | Their matched philosophy result |
| `curriculove_top_curricula` | Text | Their recommended curricula |
| `newsletter_subscriber_date` | Date | When they joined newsletter |

These allow us to:
1. Segment Curriculove leads from other sources
2. Track time-to-conversion
3. Personalize nurture based on quiz results
4. Answer "is newsletter serving prospects or customers?"

---

*Document ready for action. Update as data comes in.*
