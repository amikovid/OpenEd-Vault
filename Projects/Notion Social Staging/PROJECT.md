# Notion Social Staging

**Status:** Active
**Goal:** Use Notion as the approval UI for social posts, with direct GetLate scheduling

---

## Context

We built a content inbox pipeline where suggestions flow into Slack #content-inbox. The next step is staging approved posts in Notion and scheduling them via GetLate - without Zapier or external automation.

**Related skill:** `.claude/skills/schedule-approved/SKILL.md`
**Workflow reference:** `.claude/references/content-inbox-workflow.md`

---

## Current Flow

```
#content-inbox (suggestions)
    ↓ ✍️ develop
Thread replies (draft options)
    ↓ ✅ approve
??? → Notion staging → GetLate
```

---

## What Needs to Be Done

### 1. Verify/Add Notion Properties

Check Master Content Database (`9a2f5189-6c53-4a9d-b961-3ccbcb702612`) for these properties:

| Property | Type | Status | Notes |
|----------|------|--------|-------|
| Platform | select | ❓ Check | LinkedIn, X, Instagram, Facebook, TikTok, etc. |
| Caption | rich_text | ❓ Check | The actual post content |
| Post Date | date | ✅ Exists | When to publish (include time) |
| Media URL | url | ❓ Check | Optional image/video URL |
| GetLate Post ID | text | ❓ Add | Filled after scheduling |
| Source Slack TS | text | ❓ Add | Link back to original suggestion |

**To check:**
```
Use Notion MCP to query database schema:
mcp__notion__API-retrieve-a-database
database_id: 9a2f5189-6c53-4a9d-b961-3ccbcb702612
```

### 2. Create Platform Select Options

If Platform property doesn't exist, create it with options:
- LinkedIn
- X
- Instagram
- Facebook
- TikTok
- Pinterest
- YouTube
- Threads

### 3. Test schedule-approved Skill

Once properties exist:
1. Manually create a test item in Notion with Status = "Approved", Platform, Caption
2. Run "schedule approved" to test the flow
3. Verify GetLate receives the post
4. Verify Notion status updates to "Scheduled"

### 4. Create Notion View

Create a filtered view for social staging:
- **Name:** Social Staging
- **Filter:** Platform is not empty
- **Sort:** Post Date ascending
- **Group by:** Status (Kanban)

---

## GetLate API Reference

**Base URL:** `https://getlate.dev/api/v1`
**Auth:** Bearer token (`GETLATE_API_KEY` in .env)

**Endpoints:**
- `GET /accounts` - List connected platforms
- `POST /posts` - Create/schedule post

**Post payload:**
```json
{
  "platforms": [{"platform": "twitter", "accountId": "..."}],
  "content": "Post text",
  "publishNow": true,
  // OR
  "scheduledFor": "2026-01-29T14:00:00Z"
}
```

**Platform mapping:**
| Notion | GetLate |
|--------|---------|
| X | twitter |
| LinkedIn | linkedin |
| Instagram | instagram |
| Facebook | facebook |
| TikTok | tiktok |
| Pinterest | pinterest |
| YouTube | youtube |
| Threads | threads |

---

## Existing Scripts

| Script | Purpose |
|--------|---------|
| `agents/post_tweet.py` | Post single tweet |
| `agents/post_linkedin.py` | Post to LinkedIn |
| `agents/audit_platforms.py` | List connected accounts |

---

## Architecture Decision: No Zapier

We chose to avoid Zapier/Make for this bridge. Instead:

1. **Manual trigger:** User says "schedule approved"
2. **Claude queries Notion** for Status = "Approved" items
3. **Claude calls GetLate API** for each item
4. **Claude updates Notion** Status → "Scheduled"

This keeps everything in Claude Code without external automation costs.

---

## Related Files

- `.claude/skills/schedule-approved/SKILL.md` - The scheduling skill
- `.claude/references/content-inbox-workflow.md` - Full pipeline reference
- `.claude/references/notion-content-schema.md` - Existing Notion schema
- `agents/post_tweet.py` - GetLate API example

---

## Next Session

1. Query Notion to check which properties exist
2. Add missing properties (Platform, Caption, GetLate Post ID)
3. Create Social Staging view
4. Test end-to-end with one post

---

*Created: 2026-01-28*
