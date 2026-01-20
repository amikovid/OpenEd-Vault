# OpenEd Vault Agents

Automation agents for content management and workflow optimization.

## Structure

```
agents/
├── webflow_sync.py           # Main Webflow sync script (use this)
├── .webflow_sync_state.json  # Tracks last sync timestamp
├── social_media_agent.py     # Social media posting via GetLate
├── content_multiplier.py     # Content repurposing utilities
├── _archived/                # Old scripts kept for reference
└── README.md
```

---

## Webflow Content Sync

Syncs posts from Webflow CMS to Master Content Database with full metadata.

### Quick Start

```bash
cd agents/

# Check what's new since last sync
python3 webflow_sync.py --status

# Preview what would be synced
python3 webflow_sync.py --dry-run

# Sync new posts
python3 webflow_sync.py
```

### How It Works

1. **State tracking**: Uses `.webflow_sync_state.json` to remember last sync timestamp
2. **Incremental sync**: Only fetches posts updated after last sync (saves API calls)
3. **Duplicate prevention**: Checks existing `webflow_id` in database files
4. **Full metadata**: Captures title, slug, URL, type, date, thumbnail, author, summary, and full content

### Commands

| Command | Description |
|---------|-------------|
| `python3 webflow_sync.py` | Sync new posts since last sync |
| `python3 webflow_sync.py --status` | Show sync status and pending posts |
| `python3 webflow_sync.py --dry-run` | Preview without actually syncing |
| `python3 webflow_sync.py --full` | Full re-sync (use sparingly) |

### Output Format

Each synced post becomes a markdown file with:

```yaml
---
title: "Post Title"
slug: post-slug
url: https://opened.co/blog/post-slug
type: blog_posts
date: 2026-01-09
webflow_id: abc123def456
author_id: 68089b4d33745cf5ea4d746d
thumbnail: https://cdn.prod.website-files.com/...
meta_description: "SEO description"
summary: "Brief summary"
created_on: 2026-01-09T18:28:27.048Z
last_updated: 2026-01-09T18:57:07.552Z
last_published: 2026-01-09T18:57:07.552Z
last_synced: 2026-01-12 12:30
---

# Post Title

**URL:** [https://opened.co/blog/post-slug](...)
**Type:** Blog Posts
**Published:** 2026-01-09

## Summary
Brief summary...

## Content
Full markdown content converted from HTML...
```

### Configuration

**API Key Location:** `/OpenEd Vault/.env`

```bash
WEBFLOW_API_KEY=your_token_here
```

**To get a new API key:**
1. Go to [Webflow Dashboard](https://webflow.com/dashboard)
2. Navigate to: **Workspace Settings** → **Integrations** → **API Access**
3. Click "Generate API Token"
4. Select permissions: **CMS read** (minimum required)
5. Copy the token and add to `.env` file

### Webflow IDs Reference

| Resource | ID |
|----------|-----|
| **Site** | opened.co |
| **Posts Collection** | `6805bf729a7b33423cc8a08c` |
| **Blog Posts Type** | `6805d44048df4bd97a0754ed` |
| **Daily Newsletters Type** | `6805d5076ff8c966566279a4` |
| **Podcasts Type** | `6805d42ba524fabb70579f4e` |
| **Announcements Type** | `6812753c2611e43906dc13d6` |

### Content Organization

Posts are organized into folders by type:
- `Blog Posts/` - Articles and long-form content
- `Daily Newsletters/` - Newsletter content
- `Podcasts/` - Podcast episodes
- `Announcements/` - Important updates
- `Other/` - Uncategorized

---

## Other Agents

### social_media_agent.py

Posts content to social media via GetLate API.

```bash
# Requires GETLATE_API_KEY in .env
python3 social_media_agent.py
```

### content_multiplier.py

Utilities for repurposing content across formats.

---

## Troubleshooting

**API returns 403 or missing scopes:**
- Regenerate API key with correct permissions (CMS read)

**No state file found:**
- Run `python3 webflow_sync.py --full --dry-run` to see all posts
- Or manually create `.webflow_sync_state.json` with a timestamp

**Duplicate posts appearing:**
- Check that `webflow_id` is being captured in frontmatter
- The sync checks this ID to prevent duplicates

---

*Part of the OpenEd Vault automation ecosystem*
*Last updated: 2026-01-12*
