# RSS Curation Tracking System

**Purpose:** Track which items have been vetted/processed to avoid duplicate work and enable incremental scanning.

---

## Architecture

### Storage: `tracking.json`

```json
{
  "lastRun": "2026-01-29T06:00:00Z",
  "items": {
    "https://example.com/article-url": {
      "firstSeen": "2026-01-29",
      "score": "definitely",
      "status": "posted",
      "vettedDate": "2026-01-29",
      "postedDate": "2026-01-29",
      "platform": "slack",
      "source": "Lenore Skenazy",
      "title": "Article Title"
    }
  },
  "stats": {
    "totalTracked": 127,
    "duplicatesPrevented": 23
  }
}
```

### Status Flow

```
new → vetted → posted
         ↓
       skipped
```

| Status | Meaning |
|--------|---------|
| `new` | Just fetched, not yet reviewed |
| `vetted` | Human approved for posting |
| `skipped` | Human decided not to post |
| `posted` | Successfully posted to Slack |

---

## Integration Points

### 1. Fetch Phase (rss_curation.py)

Before scoring, check if URL exists in `tracking.json`:
- If exists with status `posted` or `skipped`: Skip entirely
- If exists with status `vetted`: Include in today's output for posting
- If new: Score and add to tracking with status `new`

```python
def is_new_item(url, tracking):
    return url not in tracking.get('items', {})

def load_tracking():
    try:
        with open('tracking.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lastRun": None, "items": {}, "stats": {"totalTracked": 0, "duplicatesPrevented": 0}}

def save_tracking(tracking):
    with open('tracking.json', 'w') as f:
        json.dump(tracking, f, indent=2)
```

### 2. Curation Output

Daily markdown files now include tracking context:
- Show only new items (not previously seen)
- Mark items that were auto-skipped as duplicates
- Include a "Previously Vetted" section for items ready to post

### 3. Dashboard Integration

The HTML dashboard reads `tracking.json` to show:
- Real item counts and statuses
- Date-based filtering that works with actual data
- Accurate deduplication stats

---

## Migration Plan

### Step 1: Create tracking.json from existing daily files

Scan `daily/*.md` files and extract URLs that have been processed:
- Parse DEFINITELY items → status: `posted` (assume posted if in output)
- Parse PROBABLY items → status: `vetted`
- Parse NO items → status: `skipped`

### Step 2: Update rss_curation.py

Add tracking integration:
1. Load tracking at start
2. Filter out known URLs before scoring
3. Add new URLs to tracking after scoring
4. Save tracking at end

### Step 3: Add manual status updates

The dashboard allows clicking "Vet" or "Skip" buttons which should:
1. Update `tracking.json` via a simple Python script or
2. Use a companion `track.py` CLI tool

---

## CLI Tool: track.py

```bash
# Mark item as vetted
python track.py vet "https://example.com/article"

# Mark item as posted
python track.py posted "https://example.com/article" --platform slack

# Mark item as skipped
python track.py skip "https://example.com/article"

# Show stats
python track.py stats

# Clean old items (older than 90 days)
python track.py clean --days 90
```

---

## Benefits

1. **No duplicate processing** - Items only appear once in the queue
2. **Date-based views** - Filter by when items were first seen or vetted
3. **Progress visibility** - Dashboard shows real metrics
4. **Lightweight** - Single JSON file, no database needed
5. **Human-readable** - Can inspect/edit tracking.json directly if needed

---

## Next Steps

1. [ ] Migrate existing daily files to seed tracking.json
2. [ ] Update rss_curation.py with tracking integration
3. [ ] Create track.py CLI tool
4. [ ] Update dashboard to read from tracking.json
5. [ ] Add launchd automation for daily runs

---

*Created: 2026-02-02*
