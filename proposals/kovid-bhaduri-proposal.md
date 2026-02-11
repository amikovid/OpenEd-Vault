# Kovid Bhaduri - 2-Week Sprint Proposal

## Domain

Systems architecture, analytics infrastructure, and execution automation. Closing the feedback loop between published content and editorial decisions. Unblocking the bottlenecks that sit between "planned" and "shipped."

---

## The Value-Add Argument

The vault's content production engine is well-built. 60 skills, hub-and-spoke model, quality gates, 360+ social templates, Notion workflows. The AI handles drafting, formatting, and quality checking. A content associate who executes tasks within these existing systems - running skills, drafting newsletters, producing social batches - adds value, but it's incremental. The system already does that work. The human becomes a button-pusher.

The higher-value role is the one the AI can't fill on its own: someone who looks at the system from above, identifies where it breaks down, builds the connective tissue between components, and executes on the things Charlie doesn't have time for. Not "run the newsletter skill" but "why do analytics exist in 6 silos and never reach the decision point?" Not "draft a social post" but "why are 3 finished SEO articles sitting unpublished?"

That's what I focused on today, and what I'd focus on in a 2-week sprint.

---

## What I Built Today

### Primary: Content Performance Scoring System

The vault has analytics modules for GA4, GSC, HubSpot, YouTube, Meta, and DataForSEO. They work. But the data never reaches the point where decisions get made. Charlie approves content in Notion and Slack without knowing what similar content did last time.

I built a system that closes that loop:

**Scoring engine** (`agents/content_performance_agent.py`) - Imports the existing seomachine modules, calculates a 0-100 composite score for every published piece using platform-specific weighting (LinkedIn weights comments, X weights reposts, Instagram weights saves), and writes scores back to Notion. Generates narrative insight digests that lead with patterns, not just rankings.

**One-command setup** (`agents/setup_performance_scoring.py`) - Charlie runs one script. It checks his API keys, automatically creates 12 performance tracking properties on the Notion database via API, runs initial scoring, and offers to set up daily cron. Five minutes from zero to working.

**Approval context injection** (`get_approval_context()`) - Any skill can import this function. When Charlie is reviewing a draft, it returns historical performance context for that theme and platform, including which platform works best and what the top performer looked like.

### Secondary: Full Vault Audit

Audited every major system in the vault for gaps between documentation and reality. Findings below.

---

## Vault Audit: Where Things Break Down

### Critical (Blocking Growth)

**1. Social scheduling pipeline is broken mid-stream.**
Content gets created. Skills generate platform-specific posts. But the #content-inbox Slack workflow isn't operational, Notion staging has 100+ items in a triage backlog, and `schedule-approved` has a TODO comment for media handling. Text posts can schedule via GetLate; image/video posts require manual upload. The social distribution chain has 3+ manual gaps between "AI generates a post" and "post goes live."

**2. SEO content sitting unpublished.**
92 articles planned, 0 published. 3+ comparison articles (Khan vs IXL, Saxon vs Math-U-See, IXL vs Exact Path) are draft-complete, quality-checked, and thumbnailed. 7 tool review drafts exist. The `batch_webflow_upload.py` script exists but hasn't been run. Teacher approval emails for tool reviews haven't been sent. Guest contributor pitches drafted but never sent. This is a process bottleneck, not a technical one.

**3. Lead magnet (Curriculove) not deployed.**
Full product spec exists. Next.js codebase exists. Quiz-to-newsletter funnel documented. But nothing is live at curricula.love. No HubSpot automation built for lead nurture. ManyChat integration documented but not configured. This is the primary email list growth engine sitting idle.

**4. No monitoring or alerting anywhere.**
No broken link detection across 406 published articles. No failed post alerts from GetLate. No API error logging. No "this article is declining" notifications. No uptime monitoring for local servers (RSS dashboard, task dashboard, Curriculove). Silent failures accumulate until users report issues.

### High (Reducing Efficiency)

**5. No editorial calendar or theme coordination.**
Content queue last updated Jan 6. Mon-Thu newsletter cadence documented but no forward-looking schedule. Newsletters, podcasts, and social posts operate independently with no theme coordination. Charlie re-decides content strategy every session from scratch.

**6. Archive content unused.**
405 published pieces (286 dailies, 66 podcasts, 48 blog posts). The `archive-suggest` skill is a 172-line process template with no automation, no dashboard, no scoring, and no Notion integration. Proven content sits idle.

**7. Nearbound pipeline dormant.**
81 contact profiles with social handles and warmth scores. 6 guest contributor contacts marked "Ready to Send" - emails not sent. Social posts don't systematically tag mentioned people. Justin Skycak marked as "HOT LEAD" in NOW.md - no outreach sent.

**8. Newsletter derivative content gets orphaned.**
NOW.md shows 30 social posts created from recent newsletters. No evidence of scheduling. The `newsletter-to-social` skill generates posts, but they don't flow into the Notion staging queue or GetLate. Content creation without distribution.

### Medium (Incremental Waste)

**9. Podcast clips don't get posted.**
SOP documents clip extraction and posting. Unclear if clips actually reach Instagram/TikTok/YouTube Shorts after being cut. Blog posts from podcast transcripts may not be published to Webflow.

**10. Zero scripts run on schedule.**
RSS curation, content scoring, SEO reports, social reports - all documented with cron schedules, none actually automated. The RSS curation launchd task is status "LATER."

**11. Task system not functioning as intended.**
59 tasks, 1 marked done (1.7% completion). Some work tracked in tasks/, some in NOW.md, some in EXECUTION.md. Dashboard requires manual `bun run server.ts`. Task creation outpaces completion.

**12. Meta ads creative backlog.**
100 concepts ready, Pillar 1 launch approaching, creative batch not started. No feedback loop between ad performance and content strategy.

### Root Cause Patterns

These aren't isolated problems. They share common causes:

1. **Last-mile automation gap** - Skills and agents exist for 90% of each workflow. The final 10% (schedule, deploy, send, monitor) requires a manual trigger that doesn't happen.
2. **Documentation exceeds implementation** - Workflows are beautifully documented but not automated. The SOP exists; the cron job doesn't.
3. **Tool proliferation without integration** - GetLate, Notion, Webflow, HubSpot, Slack, Beehiiv all partially connected. Each works alone; the handoffs between them break.
4. **Approval gates double as execution blockers** - Quality control is necessary, but every piece waiting for human review is a piece not moving. The system needs faster approval, not less quality.

---

## Vision: Content Performance Scoring - Fully Integrated

What this system looks like when it's wired into every decision point, not just sitting in a Notion column.

### Daily: Morning Planning

Charlie opens Slack at 8am. The scoring agent posted overnight:

```
Content Insights - Feb 12

3 things worth knowing:
1. Contrarian takes on LinkedIn are outperforming how-to posts by 2.4x
   this month. Your last 3 how-to posts scored below 30 there.
2. "Is it reimbursable?" videos are your highest-performing format on
   Instagram (avg score: 84). You haven't posted one in 12 days.
3. Your blog post "Waldorf vs Montessori" is getting organic traction
   (traffic up 40% this week, position 8 on Google). A social push
   right now could amplify it.

Today's content queue has 4 items in Staging.
Recommended routing based on theme scores:
  - Curriculum review draft -> LinkedIn (theme avg: 72)
  - School choice hot take -> X (theme avg: 85)
  - Parent story -> Instagram (theme avg: 61)
  - Tool roundup -> skip Facebook (theme avg: 22), try LinkedIn instead
```

Charlie knows what to approve, what to hold, and where to send each piece. No digging through analytics dashboards. The insight came to him.

### Content Approval: In-Context Scoring

When any skill generates content for review (newsletter-to-social, content-repurposer, text-content), the Performance Advisor automatically appends:

```
---
Performance context:
  "Curriculum Reviews" on LinkedIn: avg score 72 (8 posts)
  Best: "Why Saxon Math works for struggling learners" (89)
  Worst: "Curriculum roundup Jan 15" (23) - list format underperformed

  Recommendation: This is a review, not a roundup. Historical data
  suggests single-product reviews outperform roundups by 3x on LinkedIn.
  Approve for LinkedIn. Skip X (theme avg: 34 there).
```

This isn't a separate dashboard to check. It shows up inline, at the moment of decision, inside the workflow Charlie already uses.

### Weekly: Editorial Planning

Monday morning digest (Slack or markdown) shifts from "what happened" to "what to do about it":

```
Weekly Performance Review - Feb 10-16

WHAT WORKED
- "Is a chicken reimbursable?" (IG Reel, score: 91) - 3rd week in a row
  that ESA-related humor outperforms. This is a pattern, not a fluke.
- Newsletter open rates up 8% after switching to question-format
  subject lines (last 4 editions vs prior 4).

WHAT DIDN'T
- Education news roundups score avg 28 across all platforms.
  5 straight underperformers. Consider dropping this format or
  rethinking the angle.
- Facebook avg score declined from 42 to 31 this month.
  Engagement is falling. Either invest in the platform or reduce volume.

STRATEGIC RECOMMENDATIONS
- Double down on ESA/reimbursable content (consistently top 10%)
- Test: Take your best-performing LinkedIn post this week and adapt
  it for X (cross-platform theme testing)
- 3 SEO articles in drafts are ready to publish. "Waldorf vs Montessori"
  is trending up in search - publish this week.
- Archive suggestion: "Why we don't grade" (newsletter from Sept,
  score: 82) is seasonally relevant for mid-year families. Resurface.

PLATFORM HEALTH
  LinkedIn     ============= 64 (23 posts) -> strongest, increase volume
  Instagram    =========== 58 (18 posts) -> stable
  X            ======== 41 (12 posts) -> weak, but school choice content
                                          performs well here specifically
  Facebook     ======= 31 (8 posts) -> declining, needs strategy review
```

### Monthly: Strategy Review

End-of-month report connects content performance to business outcomes:

```
February 2026 Content Performance Review

AUDIENCE GROWTH
- LinkedIn followers: +340 (best month)
- Newsletter subscribers: +180 (Curriculove not deployed yet - this
  number should be 5x higher once live)
- Organic search sessions: +22% (Waldorf vs Montessori driving 40%
  of new traffic)

CONTENT ROI
- Top converting content (HubSpot): Tool reviews (3.2% visitor-to-lead)
- Top traffic drivers (GA4): Comparison articles (avg 2,400 sessions/mo)
- Top social content (engagement): ESA humor + contrarian takes
- Worst performing category: Education news roundups (avg score: 28)

RECOMMENDATIONS FOR MARCH
- Publish remaining SEO articles (5 ready in drafts)
- Deploy Curriculove quiz (largest growth lever available)
- Shift Facebook budget to LinkedIn (data supports it)
- Create 2 more "Is it reimbursable?" videos (format is proven)
- Kill the education news roundup format (5 months of underperformance)
```

### How It Feeds Into Every Skill

| Skill | Without Scoring | With Scoring |
|---|---|---|
| `quality-loop` | 5 judges check quality | 6th judge (Performance Advisor) checks if the content pattern historically performs |
| `archive-suggest` | Random evergreen suggestions | Prioritizes resurfacing top scorers. "This scored 84 last time" |
| `newsletter-to-social` | Routes to all platforms equally | Routes derivatives to the platform where that theme scores highest |
| `content-repurposer` | Generates all platform variants | Skips platforms where the theme underperforms |
| `text-content` | Picks templates by category | Picks templates from the highest-scoring categories |
| `seo-content-production` | Targets keywords by volume | Cross-references keywords with actual content performance |
| `slack-social-distribution` | Posts drafts for approval | Appends performance context so Charlie approves faster |
| `opened-daily-newsletter-writer` | Selects topics from queue | Prioritizes topics from themes that score highest |

### Timeline to Full Integration

| Phase | Work | Duration | Outcome |
|---|---|---|---|
| **Done** | Scoring engine, setup wizard, approval context function, skill file | Today | Architecture built |
| **Phase 1** | Test against live data, fix edge cases, set up cron | 2-3 days | Scores appear in Notion, daily digest runs |
| **Phase 2** | Wire into quality-loop as 6th judge, wire into archive-suggest | 2-3 days | Scoring data informs content creation + resurfacing |
| **Phase 3** | Wire into newsletter-to-social and content-repurposer for platform routing | 2 days | Derivatives auto-route to best platform |
| **Phase 4** | Build Slack integration for morning insights digest | 1-2 days | Charlie gets proactive insights without checking anything |
| **Phase 5** | Add X/Twitter and LinkedIn analytics modules (currently missing) | 3-4 days | Full platform coverage, not just Meta + YouTube |
| **Phase 6** | Monthly strategy report generator | 1-2 days | End-of-month business review auto-generated |

**Total to full integration: ~2 weeks** (aligns with sprint proposal below)

---

## What I'd Deliver in 2 Weeks

### Week 1: Scoring system production-ready + immediate wins

- Test scoring agent against live data, fix edge cases
- Wire `get_approval_context()` into `quality-loop` as Performance Advisor judge
- Wire scoring data into `archive-suggest` for performance-aware resurfacing
- Wire platform routing into `newsletter-to-social`
- Build Slack-ready morning digest with narrative insights
- Publish the 3 ready SEO comparison articles (immediate organic traffic wins)
- Set up cron jobs for daily scoring + weekly digest + RSS curation
- Send the 6 "Ready to Send" guest contributor outreach emails

### Week 2: Systems + automation + coverage gaps

- Build X/Twitter and LinkedIn analytics modules (close the two biggest platform gaps)
- Rebuild `archive-suggest` into a proper system with Notion integration
- Build quote extraction system from 66 podcast transcripts
- Build monthly strategy report generator
- Fix the social scheduling media upload gap in `schedule-approved`
- Document all changes, update vault guide

### Measurable outcomes after 2 weeks:

- Every published piece has a performance score in Notion
- Charlie gets a Monday morning Slack digest with narrative insights and platform routing recommendations
- Performance context appears inline during content approval
- 3+ SEO articles published (from existing ready drafts)
- Archive resurfacing generates 3-5 scored post suggestions daily
- X and LinkedIn analytics integrated (currently blind spots)
- Quote database covers 66 podcast episodes
- 6 guest contributor outreach emails sent
- Cron automation running for scoring, RSS, and weekly reports

---

## Why This Domain

The AI can draft a newsletter. The AI can generate 15 social posts from a podcast. The AI can run a 5-judge quality loop. These are impressive capabilities, and they're already built.

What the AI can't do on its own: notice that analytics data never reaches the decision point. Notice that finished articles are sitting unpublished. Notice that 81 contact profiles exist but nobody's sending the outreach emails. Notice that the social scheduling pipeline breaks at the media upload step. These are systems-level observations that require understanding the whole machine, not just the individual components.

My value-add is at that layer - the connective tissue between systems, the execution of things that fall through the cracks, and the architectural improvements that create leverage across every workflow rather than improving one output at a time.

---

## What I Learned Today

- The vault is architecturally sophisticated. The skill system, hub-and-spoke model, and quality gates are genuinely well-designed. The bottlenecks are at the seams between components, not in the components themselves.
- Charlie's time is the scarcest resource. Every manual step in a workflow is a cost. The system has dozens of these manual handoff points where automation exists but isn't connected.
- The gap between "planned" and "shipped" is the defining challenge. 92 SEO articles planned, 0 published. 100 ad concepts ready, creative batch not started. 6 outreach emails ready, none sent. 405 archive pieces, no resurfacing system. The production engine works - the execution layer doesn't.
- The existing analytics infrastructure is solid but siloed. GA4, GSC, HubSpot, Meta, YouTube modules all work independently. The problem was never "we can't get the data" - it was "the data doesn't reach the decision."
- "I did" over "we should." I'd rather ship an imperfect scoring agent today than pitch a perfect analytics strategy next week.

---

## Rate

Open to discussing based on scope and expectations. Happy to align on this after you've seen the work.

---

## Files Created/Modified Today

| File | Type | Purpose |
|---|---|---|
| `agents/content_performance_agent.py` | New | Scoring engine + narrative digest + approval context |
| `agents/setup_performance_scoring.py` | New | One-command setup wizard (Notion properties + .env + cron) |
| `.claude/skills/content-performance-scoring/SKILL.md` | New | Full system design + scoring algorithm |
| `.claude/references/content-performance-scoring-quickref.md` | New | Charlie's one-page reference card |
| `.claude/references/execution-bottleneck-analysis.md` | New | 5 execution bottlenecks with fixes |
| `.claude/references/notion-content-schema.md` | Modified | Added 12 performance tracking properties |
| `agents/README.md` | Modified | Added agent documentation |
| `proposals/kovid-bhaduri-proposal.md` | New | This document |
