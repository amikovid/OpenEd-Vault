# Execution Bottleneck Analysis

*Audit of vault automation gaps with prioritized recommendations.*

---

## Summary

The vault has excellent content production infrastructure (60 skills, hub-and-spoke model, quality gates). The gaps are in **execution automation** - content gets created but stalls at manual handoff points. These bottlenecks cost Charlie time and slow audience growth.

---

## Bottleneck 1: SEO Content Sitting Unpublished

**Impact:** HIGH (audience growth)
**Charlie's Time:** MEDIUM

**The situation:** 92 SEO articles planned, 0 published. But 3+ comparison articles are draft-complete, quality-checked, and thumbnailed (Khan vs IXL, Saxon vs Math-U-See, IXL vs Exact Path). `batch_webflow_upload.py` exists but hasn't been run. 7 tool review drafts also exist.

**The fix:**
1. Publish the 3 ready comparison articles this week (requires running the Webflow publish script)
2. For tool reviews: execute the teacher approval workflow (Google Doc sharing + follow-up)
3. Build a "publish queue" Notion view that shows what's ready to go

**Systemic solution:** Create an `seo-publish-pipeline` skill that:
- Maintains a prioritized publish queue (based on keyword volume + difficulty from the 151-row CSV)
- Runs pre-publish checklist automatically (quality loop passed? thumbnail generated? meta description set?)
- Triggers Webflow publish via existing API
- Creates social spokes automatically after publish
- Logs to Master Content Index

**Estimated effort:** 2-3 hours to build the skill, 30 min to publish the ready articles.

---

## Bottleneck 2: Archive Repurposing Non-Operational

**Impact:** MEDIUM-HIGH (audience growth with zero new content creation)
**Charlie's Time:** LOW (runs automatically)

**The situation:** 405 published pieces (286 dailies, 66 podcasts, 48 blog posts). `archive-suggest` skill is 172 lines - a process template, not a working system. No automation, no dashboard, no scoring, no Notion integration.

**The fix:** Rebuild `archive-suggest` into a proper system:
1. Automated daily scan of Master Content Index
2. Scoring based on: evergreen score, seasonal relevance, time since last shared, performance score (from new scoring system)
3. Direct Notion integration - creates Staging items with draft posts
4. Connects to content-performance-scoring - prioritizes resurfacing high scorers

**What this looks like running:**
- Every morning, 3-5 posts appear in Notion Staging with fresh angles on proven content
- Charlie sees: "This newsletter from June scored 84. Here's a LinkedIn version."
- Approve/reject in Notion. Approved posts flow to GetLate automatically.

**Estimated effort:** 3-4 hours for skill rebuild + Notion integration.

---

## Bottleneck 3: Quote Sourcing is Manual

**Impact:** MEDIUM (content quality + speed)
**Charlie's Time:** MEDIUM (saves 15-30 min per article)

**The situation:** SEO articles require real teacher/parent quotes for authenticity. Currently, writers manually search Slack for relevant discussions. No structured quote database exists.

**The fix:** Build a quote extraction system:
1. Scan all 66 podcast transcripts, extract quotable moments with speaker attribution
2. Structure in Notion or markdown: Quote | Speaker | Source | Topic Tags | Platform Suitability
3. When writing an article on "Saxon Math," query the database instead of searching Slack
4. Over time, add quotes from newsletters, Slack, and parent interviews

**What this looks like working:**
- Skill asks: "What's this article about?" -> "Saxon Math review"
- Returns: 12 relevant quotes from 4 podcast episodes and 3 newsletters
- Writer picks 2-3, weaves them in. No manual searching.

**Estimated effort:** 4-6 hours (extraction from transcripts is the heavy lift).

---

## Bottleneck 4: Slack MCP Not Operational

**Impact:** MEDIUM (Charlie's time)
**Charlie's Time:** HIGH

**The situation:** Content approval happens via Slack emoji reactions, but the Slack MCP is documented but not configured. This means:
- Social posts can't be auto-posted to #market-daily
- Emoji reactions can't be read programmatically
- The whole Slack approval workflow requires manual monitoring

**The fix:** Get Slack MCP operational. The xoxc/xoxd tokens are referenced in docs. Once configured:
- `slack-social-distribution` skill can post directly
- Agent can poll for emoji reactions and auto-advance approved content
- Weekly digests can post to Slack automatically

**Estimated effort:** 1-2 hours (mostly configuration, tokens may need refresh).

---

## Bottleneck 5: No Automated Scheduling

**Impact:** MEDIUM (consistency)
**Charlie's Time:** MEDIUM

**The situation:** RSS curation, scoring, and reporting scripts all exist but none run automatically. The launchd cron job for RSS is status "LATER." Everything is manual execution.

**The fix:**
1. Set up launchd plist files for:
   - RSS curation (daily 6am)
   - Content performance scoring (daily 7am)
   - Weekly SEO report (Monday 8am)
   - Weekly social report (Monday 8am)
2. Create a simple monitoring script that checks if jobs ran successfully

**Estimated effort:** 1-2 hours for all cron jobs.

---

## Priority Matrix

| Bottleneck | Audience Growth | Charlie's Time | Effort | Priority |
|---|---|---|---|---|
| SEO publish pipeline | HIGH | MEDIUM | 3 hrs | **1** |
| Archive repurposing | MEDIUM-HIGH | LOW | 4 hrs | **2** |
| Cron job automation | MEDIUM | MEDIUM | 2 hrs | **3** |
| Quote database | MEDIUM | MEDIUM | 5 hrs | **4** |
| Slack MCP | LOW-MEDIUM | HIGH | 2 hrs | **5** |

**Recommended 2-week sprint order:** Publish existing SEO articles (immediate win) -> Build archive repurposing system -> Set up cron automation -> Build quote database

---

*Created: 2026-02-11*
*Context: Candidate assessment of vault execution gaps*
