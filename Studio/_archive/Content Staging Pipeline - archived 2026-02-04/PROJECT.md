# Content Staging Pipeline

**Status:** Active
**Goal:** Clear workflow from source material → publish → outreach

---

## Content Production Order of Operations

```
INPUTS                    PRODUCTION                      OUTPUTS
────────────────────────────────────────────────────────────────────────

Slack #market-daily  ─┐
Voice memos          ─┼──► Source Material
Notion Staging       ─┘         │
                                ▼
                    ┌───────────────────────┐
                    │ 1. Draft Social Posts │ (text-content skill)
                    └───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ 2. Publish Blog Post  │ (Webflow CMS)
                    │    on Webflow         │
                    └───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ 3. Insert Blog Link   │ (update social drafts)
                    │    into Social Posts  │
                    └───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ 4. Post Suggestions   │ → Slack #market-daily
                    │    to Slack           │   for final approval
                    └───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
        ┌─────────────────┐     ┌─────────────────┐
        │ 5. Newsletter   │     │ 5. Social Posts │
        │ (HubSpot draft) │     │    go live      │
        └─────────────────┘     └─────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ 6. Outreach Emails    │ → Draft for Havala
                    │    to people mentioned│   to send
                    └───────────────────────┘
```

**Key timing:**
- Newsletter goes out simultaneously with social (unless it needs a social link, which is rare)
- Outreach emails drafted AFTER content is live (so links work)

---

## Source Material Inputs

### 1. Slack #market-daily
- Team shares links, articles, ideas
- Claude monitors and extracts for Staging

### 2. Voice Memos
- Processed via `inbox-processor` skill
- Routed to appropriate projects

### 3. Notion Staging
- 100+ items in backlog
- Weekly triage to Approved or Rejected

---

## Production Skills

| Step | Skill | Output |
|------|-------|--------|
| Draft social | `text-content` | Platform-specific posts |
| Draft newsletter | `opened-daily-newsletter-writer` | Markdown draft |
| Create HubSpot draft | `hubspot-email-draft` | Ready-to-publish email |
| Post to Slack | `slack-social-distribution` | Suggestions in #market-daily |
| Draft outreach | (new) `outreach-email-draft` | Email drafts for Havala |

---

## Outreach Email Step

After content goes live, draft emails to everyone mentioned:
- Podcast guests
- People quoted in newsletter
- Tools/curricula featured
- Anyone tagged on social

**Template:**
```
Subject: You were featured in OpenEd Daily!

Hi [Name],

We featured [your tool/quote/story] in today's OpenEd Daily newsletter
to our 10,000+ subscribers.

[Link to newsletter/blog post]

Thanks for the great work you're doing!

– Havala (OpenEd Team)
```

**Output:** Email drafts saved for Havala to review and send.

---

## Problem Statement (Original)

Content gets created in Studio (Claude Code) but the path to publication is unclear:
- 100+ items stuck in Staging status
- 0 items in Approved (bottleneck)
- No clear review workflow
- Multiple publishing routes (GetLate, Webflow) not documented
- "Mess" of properties, formats, and relations

---

## Current State

### Master Content Database

**ID:** `9a2f5189-6c53-4a9d-b961-3ccbcb702612`

| Status | Count | Issue |
|--------|-------|-------|
| Staging | 100+ | Backlog, not being reviewed |
| Approved | 0 | Pipeline not flowing |
| Scheduled | 8 | Only scheduled items |
| Posted | 100+ | Historical |
| Idea | 100+ | Healthy backlog |

### Related Databases

| Database | ID | Purpose |
|----------|-----|---------|
| Content Formats | `2a3afe52-ef59-80d0-af3f-f3f3d2cb25ca` | 26+ format types |
| Podcast Calendar | `d60323d3-8162-4cd0-9e1c-1fea5aad3801` | Episodes + derived content |

### Key Properties

| Property | Type | Status |
|----------|------|--------|
| Status | status | Working (Idea→Staging→Approved→Scheduled→Posted) |
| Content Formats | relation | Underutilized - many items have none set |
| Type | multi_select | Underutilized - most items blank |
| Basic Summary | rich_text | Contains actual content |
| Post Date | date | Used for scheduling |
| URL | url | Often missing on Posted items |
| Source URL | url | For curated content |

### Publishing Routes

1. **GetLate API** → 8 social platforms (LinkedIn, X, IG, FB, YT, TikTok, Pinterest, Mastodon)
2. **Webflow CMS** → Website articles (Deep Dives, Hub content)
3. **Manual** → Email newsletters (OpenEd Daily, Weekly)

---

## What Done Looks Like

### 1. Clear Workflow Definition

```
STUDIO (Claude Code)                NOTION                         PUBLISH
─────────────────────────────────────────────────────────────────────────────

Create content
   │
   ▼
Send to Notion ──────────────►  STAGING
(API or manual)                     │
                                    ▼
                              Weekly Review
                              (Kanban view)
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                    APPROVED              REJECTED
                         │                 (archive)
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
         SCHEDULED              Direct Publish
         (Post Date set)            │
              │                     │
              ▼                     ▼
         GetLate auto           Webflow/Manual
              │                     │
              ▼                     ▼
           POSTED                 POSTED
           (URL set)              (URL set)
```

### 2. Notion Views Created

- [ ] **Staging Review** - Kanban of Staging items, grouped by Content Format
- [ ] **This Week** - Scheduled items with Post Date in next 7 days
- [ ] **Published** - Posted items with URL populated
- [ ] **Backlog Triage** - Staging items older than 30 days (reject or schedule)

### 3. Properties Cleaned Up

- [ ] Audit Content Formats relation - ensure all Staging items have format set
- [ ] Decide: Keep Type property or deprecate in favor of Content Formats?
- [ ] Ensure URL property populated for all Posted items (or mark as "Published - No URL")

### 4. Publishing Routes Documented

- [ ] GetLate configuration documented (which formats auto-publish)
- [ ] Webflow publishing workflow documented
- [ ] Newsletter publishing workflow documented

### 5. Claude Integration Working

- [ ] Claude can create items in Staging via API
- [ ] Claude can read Staging items for review/action
- [ ] Claude can update Status (Staging → Approved)
- [ ] Notion MCP server working (currently broken - token caching issue)

---

## Success Criteria

**Done when:**

1. **New content** created in Studio goes to Staging with one command
2. **Weekly review** clears Staging backlog (approve, schedule, or reject)
3. **Scheduled items** auto-publish via GetLate
4. **Published items** have URL populated
5. **Backlog** (Staging 30+ days old) is triaged monthly

**Metrics:**
- Staging backlog < 50 items (currently 100+)
- Approved → Posted within 7 days
- 90% of Posted items have URL property set

---

## Implementation Phases

### Phase 1: Triage (This Week)

- [ ] Review 100+ Staging items
- [ ] Bulk reject outdated content (Christmas puzzles in January, etc.)
- [ ] Set Content Formats on items missing it
- [ ] Move viable items to Approved or Scheduled

### Phase 2: Views & Workflow

- [ ] Create Staging Review Kanban view
- [ ] Create This Week calendar view
- [ ] Document review cadence (daily? weekly?)

### Phase 3: Claude Integration

- [ ] Fix Notion MCP server (token caching)
- [ ] Create `/stage` skill to send content to Notion
- [ ] Test end-to-end: create → stage → approve → publish

### Phase 4: Automation

- [ ] GetLate polling Approved items
- [ ] Slack notification for Staging backlog > 50
- [ ] Weekly digest of what got Published

---

## Related Projects

- `Projects/OpenEd-Content-OS/` - Content OS docs, skill architecture map
- `Social Media/` - Platform strategies, format definitions
- `Analytics & Attribution/` - Post-publish tracking

## Related Skills

- `text-content` - Creates social posts
- `newsletter-to-social` - Newsletter → multi-platform
- `slack-social-distribution` - Posts to #market-daily

---

## API Access

**Notion Integration:** "Clawd" (bot user)
**Token:** Stored in `.mcp.json` (root)
**Access:** Master Content Database, Content Formats, Podcast Calendar

**Working API call:**
```bash
curl -s -X POST "https://api.notion.com/v1/databases/9a2f5189-6c53-4a9d-b961-3ccbcb702612/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Status", "status": {"equals": "Staging"}}}'
```

---

## Session Log

### 2026-01-24 - Discovery Session

**Completed:**
- Explored Content Engine Deck architecture
- Explored _content-engine-refactor docs
- Mapped Notion schema (databases, properties, statuses)
- Tested API access to Master Content Database
- Counted items by status (100+ in Staging, 0 in Approved)
- Identified the bottleneck (review/approval not happening)

**Key Finding:** The infrastructure exists (databases, formats, statuses) but the workflow isn't being followed. Content goes to Staging and sits there.

**Next Session:** Phase 1 triage - review and clear Staging backlog.

---

*Created: 2026-01-24*
