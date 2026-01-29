# Social Post Queue - Process Documentation

**Notion Database:** https://www.notion.so/2f7afe52ef5981118044e797e95a6a7d
**Location:** OpenEd Content Engine > Social Post Queue

---

## Schema

| Property | Type | Purpose |
|----------|------|---------|
| Source | Title | Article/episode title (shows in list view) |
| Platform | Select | X, LinkedIn, Instagram, Facebook |
| Status | Select | Draft → Review → Approved → Scheduled → Posted |
| Scheduled Time | Date | When to post (with time) |
| Source URL | URL | Link to source article/video |
| Voice | Select | Ed the Horse, OpenEd |
| Getlate ID | Text | Auto-filled after scheduling |
| *Page body* | Blocks | **The actual post text** (editable, supports line breaks) |

---

## Workflow

### 1. Content Creation → Notion

Claude creates posts and adds to Notion:

```python
# Key: Split long content into paragraphs to avoid 2000 char limit
paragraphs = content.split("\n\n")
children = [
    {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": p}}]}}
    for p in paragraphs if p.strip()
]
```

### 2. Human Review in Notion

- View as **Table** (overview) or **Board** (by status)
- **Edit post text** directly in page body
- **Set Scheduled Time** if specific time needed
- **Change Status to "Approved"** when ready

### 3. Automation Scheduling

**Manual run:**
```bash
python3 agents/social_post_scheduler.py
```

**Cron job (hourly):**
```bash
0 * * * * cd ~/Desktop/New\ Root\ Docs/OpenEd\ Vault && python3 agents/social_post_scheduler.py >> /tmp/social_scheduler.log 2>&1
```

**What it does:**
1. Queries Notion for Status = "Approved"
2. Reads post text from page body
3. Schedules via Getlate API
4. Updates Status to "Scheduled" + adds Getlate ID

---

## Adding Posts Programmatically

### Single Post
```python
page_data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Source": {"title": [{"text": {"content": "Article Title"}}]},
        "Platform": {"select": {"name": "X"}},
        "Status": {"select": {"name": "Draft"}},
        "Voice": {"select": {"name": "Ed the Horse"}},
        "Source URL": {"url": "https://..."}
    },
    "children": [
        {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Post text here"}}]}}
    ]
}
```

### Long Content (>2000 chars)
Split into multiple paragraph blocks:
```python
paragraphs = long_content.split("\n\n")
children = [
    {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": p.strip()}}]}}
    for p in paragraphs if p.strip()
]
```

---

## Platform Account IDs (Getlate)

| Platform | Account ID |
|----------|------------|
| Twitter (@OpenEdHQ) | `696135064207e06f4ca849a1` |
| LinkedIn (OpenEd.co) | `696135294207e06f4ca849a2` |
| Instagram (@openedhq) | `6961355a4207e06f4ca849a5` |
| Facebook (@openedhq) | `696135da4207e06f4ca849a8` |
| TikTok (@openedhq) | `696135344207e06f4ca849a3` |

---

## Integration Points

### From RSS Curation
After daily curation, add DEFINITELY items:
```
RSS Fetch → Score → Draft Ed Posts → Add to Notion Queue
```

### From Podcast/Content Production
After content creation, add social posts:
```
social-plan.md → Parse posts → Add to Notion Queue
```

---

## Files

| File | Purpose |
|------|---------|
| `agents/social_post_scheduler.py` | Polls Notion → Schedules via Getlate |
| `Projects/RSS-Curation/SOCIAL-POST-QUEUE.md` | This documentation |

---

## Views to Create in Notion

1. **All Posts** - Table view, sorted by Scheduled Time
2. **By Status** - Board view, grouped by Status
3. **Today's Posts** - Filter: Scheduled Time is today
4. **Needs Approval** - Filter: Status = Draft or Review
5. **By Platform** - Board view, grouped by Platform

---

*Last updated: 2026-01-29*
