# Schedule Approved Content

Query Notion for approved social posts and schedule them via GetLate API - no Zapier needed.

## Invocation

User says: "schedule approved", "push to getlate", "schedule content", "/schedule-approved"

---

## How It Works

This skill directly bridges Notion → GetLate without external automation services.

```
Notion (Approved) → Claude reads → GetLate API → Notion (Scheduled)
```

---

## Prerequisites

1. **GetLate API Key** in `.env` as `GETLATE_API_KEY`
2. **Notion MCP** connected with access to Master Content Database
3. **Content properly formatted** in Notion with required fields

---

## Required Notion Properties

Items must have these properties set to be scheduled:

| Property | Type | Required | Notes |
|----------|------|----------|-------|
| Status | status | Yes | Must be "Approved" |
| Platform | select | Yes | LinkedIn, X, Instagram, Facebook, etc. |
| Caption | rich_text | Yes | The actual post content |
| Post Date | date | Recommended | When to publish (defaults to now if empty) |
| Media URL | url | Optional | Image/video URL |
| Content Formats | relation | Optional | For tracking |

---

## Workflow

### Step 1: Query Notion for Approved Items

```
Filter: Status = "Approved" AND Platform is not empty AND Caption is not empty
Sort: Post Date ascending
```

Use Notion MCP:
```
mcp__notion__API-query-database
database_id: 9a2f5189-6c53-4a9d-b961-3ccbcb702612
filter: {
  "and": [
    {"property": "Status", "status": {"equals": "Approved"}},
    {"property": "Platform", "select": {"is_not_empty": true}}
  ]
}
```

### Step 2: Get GetLate Account IDs

Call GetLate API to get connected account IDs:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GETLATE_API_KEY")
base_url = "https://getlate.dev/api/v1"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

response = requests.get(f"{base_url}/accounts", headers=headers)
accounts = response.json().get("accounts", [])

# Map platform names to account IDs
platform_map = {}
for acc in accounts:
    platform = acc.get("platform")
    platform_map[platform] = acc.get("_id")

# Example: platform_map = {"twitter": "abc123", "linkedin": "def456", ...}
```

### Step 3: Schedule Each Item

For each approved item:

```python
# Map Notion platform names to GetLate platform names
PLATFORM_MAPPING = {
    "X": "twitter",
    "Twitter": "twitter",
    "LinkedIn": "linkedin",
    "Instagram": "instagram",
    "Facebook": "facebook",
    "TikTok": "tiktok",
    "Pinterest": "pinterest",
    "YouTube": "youtube",
    "Threads": "threads"
}

def schedule_post(caption, platform, scheduled_for=None, media_url=None):
    getlate_platform = PLATFORM_MAPPING.get(platform)
    account_id = platform_map.get(getlate_platform)

    if not account_id:
        return {"error": f"No account connected for {platform}"}

    post_data = {
        "platforms": [{"platform": getlate_platform, "accountId": account_id}],
        "content": caption,
    }

    if scheduled_for:
        post_data["scheduledFor"] = scheduled_for  # ISO 8601 format
    else:
        post_data["publishNow"] = True

    # TODO: Handle media_url if GetLate supports it

    response = requests.post(f"{base_url}/posts", headers=headers, json=post_data)
    return response.json()
```

### Step 4: Update Notion Status

After successful scheduling, update the Notion page:

```
mcp__notion__API-patch-page
page_id: [item's page ID]
properties: {
  "Status": {"status": {"name": "Scheduled"}},
  "GetLate Post ID": {"rich_text": [{"text": {"content": "[post_id from response]"}}]}
}
```

---

## Execution Script

When invoked, Claude should:

1. Load the Notion MCP tools
2. Query for Approved items
3. Present a summary to user:
   ```
   Found 3 approved items ready to schedule:

   1. [LinkedIn] "Your kid's minecraft addiction..." - Jan 29, 9am ET
   2. [X] "Dual enrollment is underrated..." - Jan 29, 12pm ET
   3. [Instagram] "The gap that matters..." - Jan 30, 9am ET

   Schedule all? (y/n) or specify numbers to schedule
   ```
4. On confirmation, schedule via GetLate
5. Update Notion statuses
6. Report results

---

## Time Zone Handling

GetLate expects ISO 8601 with timezone. Convert Notion dates:

```python
from datetime import datetime, timezone

# Notion date: "2026-01-29"
# Notion time (if set): "09:00"
# Assume ET timezone

def to_getlate_time(notion_date, time_str="09:00"):
    """Convert Notion date to GetLate ISO format (UTC)"""
    # Parse date
    dt = datetime.strptime(f"{notion_date} {time_str}", "%Y-%m-%d %H:%M")

    # ET offset (winter = -5, summer = -4)
    # For simplicity, assume -5 (EST)
    utc_dt = dt.replace(hour=dt.hour + 5)

    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

# Example: to_getlate_time("2026-01-29", "09:00") → "2026-01-29T14:00:00Z"
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No GETLATE_API_KEY | Abort, tell user to set up .env |
| Platform not connected | Skip item, report which platform missing |
| Caption too long | Warn user, truncate or skip |
| Notion update fails | Report but continue (post was scheduled) |

---

## Post-Scheduling Report

After completion, report:

```
Scheduled 3 of 3 items:

✅ LinkedIn - "Your kid's minecraft..." → Jan 29, 9am ET
✅ X - "Dual enrollment is underrated..." → Jan 29, 12pm ET
✅ Instagram - "The gap that matters..." → Jan 30, 9am ET

Notion statuses updated to "Scheduled"
```

---

## Related Skills

- `rss-curation` - Feeds content inbox
- `archive-suggest` - Suggests archive content
- `newsletter-to-social` - Generates social from newsletters
- `text-content` - Template library for creating posts

---

## Database Reference

**Master Content Database ID:** `9a2f5189-6c53-4a9d-b961-3ccbcb702612`

**Status Flow:** Idea → Staging → Approved → Scheduled → Posted

---

*Created: 2026-01-28*
