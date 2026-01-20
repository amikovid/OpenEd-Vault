# Notion Content Schema Reference

**Purpose:** Persistent mapping for querying OpenEd content databases via Notion/Rube MCP.

**Last Updated:** 2026-01-12

---

## Key Database IDs

| Database | ID | Purpose |
|----------|-----|---------|
| Master Content Database | `9a2f5189-6c53-4a9d-b961-3ccbcb702612` | All content items (articles, ideas, clips, etc.) |
| Content Formats | `2a3afe52-ef59-80d0-af3f-f3f3d2cb25ca` | Format types (Reel, Horse Mask, etc.) |
| Podcast Master Calendar | `d60323d3-8162-4cd0-9e1c-1fea5aad3801` | Podcast episodes with guest scheduling |

---

## Podcast-to-Content Relation

The Podcast Master Calendar links to content via a **dual-property relation**:

- **Podcast side:** Property `🔮 Master Content Database` links to content items
- **Content side:** Property `Parent podcast` links back to the source episode

### Pattern for Podcast-Derived Content

When creating content from a podcast episode:
1. Create content item in Master Content Database
2. Set `Parent podcast` relation to the episode page ID
3. Content automatically appears in linked database views within the podcast page

### Podcast Status Workflow

| Status | Group | Use |
|--------|-------|-----|
| Not started | To-do | Scheduled but not recorded |
| Scheduled | In progress | Recording date confirmed |
| Recorded | In progress | Recorded, in post-production |
| Done | Complete | Published |

Separate status tracking for clips:
- **Short Clips Status:** Not started → In progress → Done
- **Long Clip Status:** Not started → In progress → Done

---

## Content Format ID Mapping

Use these IDs when filtering by Content Format relation.

### Video Formats (Short-Form)

| Format | ID | Cadence | Platforms |
|--------|-----|---------|-----------|
| Reel | `2a3afe52-ef59-80ce-aab4-cc804fe4818b` | 1/day | IG Reels, YT Shorts, TT, FB, X, LinkedIn, Pinterest |
| Horse Mask Ideas | `2abafe52-ef59-80b0-bb6a-d573d4a4c797` | 2/week | - |
| Podcast clip | `2a3afe52-ef59-80db-9380-eda257e462de` | 2/week | IG Reels, YT Shorts, TT, FB, X, LinkedIn, Pinterest |
| YouTube Remix | `2aaafe52-ef59-80e6-abe5-c162872974a2` | 1/week | - |
| Text on B-Roll | `2aaafe52-ef59-8074-893f-da599e815117` | 1/week | - |
| GreenScreen Memes | `2abafe52-ef59-8048-bd47-d5f8e83b58f9` | 1/week | - |

### Static/Image Formats

| Format | ID | Cadence | Platforms |
|--------|-----|---------|-----------|
| Text Heavy | `2a3afe52-ef59-80b0-b900-d397fc3c4ad6` | 2/week | FB, LinkedIn, IG, X |
| Memes | `2a3afe52-ef59-80ed-897a-e776a3d05cfe` | 3/week | FB, X, IG, LinkedIn |
| Screenshot | `2a3afe52-ef59-806c-8a82-dae10c8fbd8e` | 2/week | FB, IG POST, X, LinkedIn |
| Carousel | `2aaafe52-ef59-80d1-888a-f872cd7e425d` | 1/week | LinkedIn, IG |

### Written/Long-Form Formats

| Format | ID | Cadence | Platforms |
|--------|-----|---------|-----------|
| Deep Dives | `2a3afe52-ef59-800b-8af2-e1347eda8f30` | 2/week | Website (optional: LinkedIn, FB, X) |
| Open Education Hub | `f3e829fb-b1e6-43e3-a3e7-116c767722cb` | As needed | Website |
| OpenEd Daily | `2aaafe52-ef59-80bc-beea-ce72402611aa` | 5x/week | Email |
| Weekly digest | `c62c9b50-eb8a-4d30-977d-bea5fb57cada` | 1/week | Email |

### Other Formats

| Format | ID |
|--------|-----|
| Trend | `2aaafe52-ef59-80ac-8d0d-dfaf98a8e653` |
| Podcast | `2acafe52-ef59-8050-940b-fae3327571af` |
| Tool | `2aaafe52-ef59-808a-a50e-d7afadf00c68` |
| Thought | `2aaafe52-ef59-8065-9f41-c5d7d5dc45ed` |
| X | `2abafe52-ef59-801e-b69f-f32081403886` |
| Meta Ads | `824b7278-e3bc-4349-89df-c6296a36448e` |
| Reddit | `1fd1d569-c8a7-4e98-b00a-d3def25d5248` |

---

## Master Content Database Schema

### Status Property (status type)

| Status | Group | Use |
|--------|-------|-----|
| Idea | To-do | Raw idea, not developed |
| Staging | In progress | Ready for production/review |
| Approved | In progress | Approved, awaiting publish |
| Scheduled | In progress | Scheduled for future publish |
| Posted | Complete | Published |
| Rejected | Complete | Not publishing |

### Key Properties

| Property | Type | Notes |
|----------|------|-------|
| Name | title | Content title/headline |
| Status | status | See above |
| Content Formats | relation | Links to Content Formats database |
| Type | multi_select | Daily, Thought, Trend, Tool, Reel, Meme/Fun, etc. |
| Audience Pillar | multi_select | Alternative Pathseeker, Aspiring Homeschooler, etc. |
| Source URL | url | Original source |
| URL | url | Published URL |
| Basic Summary | rich_text | Description |
| Post Date | date | Target post date |
| Publish Date | date | Actual publish date |
| Author/Partner | multi_select | Content creator |

---

## Common Query Patterns

### Get all Staging content for a specific format

```json
{
  "database_id": "9a2f5189-6c53-4a9d-b961-3ccbcb702612",
  "filter": {
    "and": [
      {"property": "Status", "status": {"equals": "Staging"}},
      {"property": "Content Formats", "relation": {"contains": "FORMAT_ID_HERE"}}
    ]
  }
}
```

### Get all Reel content in Staging

```json
{
  "database_id": "9a2f5189-6c53-4a9d-b961-3ccbcb702612",
  "filter": {
    "and": [
      {"property": "Status", "status": {"equals": "Staging"}},
      {"property": "Content Formats", "relation": {"contains": "2a3afe52-ef59-80ce-aab4-cc804fe4818b"}}
    ]
  }
}
```

### Get all Horse Mask content in Staging

```json
{
  "database_id": "9a2f5189-6c53-4a9d-b961-3ccbcb702612",
  "filter": {
    "and": [
      {"property": "Status", "status": {"equals": "Staging"}},
      {"property": "Content Formats", "relation": {"contains": "2abafe52-ef59-80b0-bb6a-d573d4a4c797"}}
    ]
  }
}
```

---

## MCP Connection Info

**Toolkit:** notion (via Rube/Composio)
**Connection Status:** Active
**Workspace:** OpenEd
**Connected Account:** cdeist@opened.co

### Key Tools

| Tool | Purpose |
|------|---------|
| `NOTION_QUERY_DATABASE_WITH_FILTER` | Query with filters (Status, Content Format, etc.) |
| `NOTION_QUERY_DATABASE` | Query without filters |
| `NOTION_FETCH_BLOCK_CONTENTS` | Get page content blocks |
| `NOTION_SEARCH_NOTION_PAGE` | Find pages/databases by name |

---

## Usage in Skills

When building skills that pull from Notion content:

1. Load this reference first
2. Use the format ID mapping to construct filters
3. Query Master Content Database with appropriate Status + Content Format filters
4. Process results

Example skill header:
```
# Load Notion schema reference
Reference: .claude/references/notion-content-schema.md
```

---

---

## Approval Workflow Design

### Current Flow

```
Idea → Staging → Approved → Scheduled → Posted
         ↓
      Rejected
```

**Idea:** Raw content idea, saved article, or concept. Not ready for production.

**Staging:** Content is being prepared. Claude creates drafts, user reviews.

**Approved:** Content reviewed and approved by user. Ready for scheduling.

**Scheduled:** Queued for publishing (optionally with Post Date set).

**Posted:** Published. Ideally with URL field populated.

### Claude-to-User Approval Pattern

1. **Claude generates content** → Creates item in Staging with:
   - Name (headline/title)
   - Content Formats relation
   - Basic Summary (the actual content or copy)
   - Source URL (if derived from saved article)
   - Parent podcast (if podcast-derived)

2. **User reviews in Notion** → Views Staging items in Kanban or list view

3. **User approves** → Drags to Approved or changes Status

4. **Scheduling options:**
   - Manual: User sets Post Date, moves to Scheduled
   - Automated: GetLate API polls Approved items and schedules

### Query for Approved Content Ready to Schedule

```json
{
  "database_id": "9a2f5189-6c53-4a9d-b961-3ccbcb702612",
  "filter": {
    "property": "Status",
    "status": {"equals": "Approved"}
  },
  "sorts": [{"property_name": "Post Date", "ascending": true}]
}
```

### Data Quality Notes

- Many Posted items lack URL field (historical data)
- Type property underutilized (most items have no Type)
- Content Formats relation more reliable than Type property

---

*Schema discovered: 2026-01-12*
*Updated: 2026-01-13 - Added podcast relations, format cadence, approval workflow*
