# Nearbound Pipeline

**Unified people database** - Everyone mentioned in OpenEd content, enriched with social handles, for tagging, outreach, and collaboration.

**Status:** Active development
**Location:** `Studio/Nearbound Pipeline/`

---

## Quick Context

This project **consolidates and extends** the existing Guest Contributors pipeline (`Studio/SEO Content Production/Guest Contributors/Pipeline.md`) by:

1. Mining the full content archive for named people (not yet extracted)
2. Adding multi-platform social handles
3. Creating a searchable/filterable view for the team

**Relationship to Guest Contributors:** The Pipeline.md has 50+ contacts with warmth scores and assigned topics. This project extracts the remaining ~200+ people from content, merges both datasets, and adds systematic social enrichment.

---

## Data Sources

| Source | Count | Status |
|--------|-------|--------|
| Master Content Index - Podcasts | 66 episodes | ✅ Extracted |
| Master Content Index - Dailies | 286 newsletters | ✅ Extracted |
| Master Content Index - Blogs | 48 articles | ✅ Extracted |
| Guest Contributors Pipeline.md | 50+ contacts | ✅ Merged |

**Current people count:** 81 unique people in `people/` folder

---

## Schema

```yaml
---
name: Peter Gray
slug: peter-gray
type:  # can have multiple
  - thought-leader  # has ideas/expertise we want to platform
  - podcast-guest   # has appeared on OpenEd podcast
  # Other options: influencer (reach, not writing), vendor, partner

# Fit scoring
guest_contributor_potential: high  # high | medium | low | null
podcast_prospect: true  # true if featured in blog/daily but not yet podcast guest

# Platforms (check all that apply)
x_twitter: "@petergray"
x_followers: 45000
linkedin: "in/peter-gray"
linkedin_followers: 12000
instagram: null
youtube: "@petergray"
youtube_subscribers: 8000
newsletter: "https://..."
newsletter_subscribers: null  # often unknown
website: "https://..."

# Reach score (calculated)
total_reach: 65000
engagement_score: high  # high | medium | low | unknown

# Relationship
relationship_status: featured  # featured | interviewed | partner | warm | cold
warmth_score: 3  # 1-5, from Pipeline.md if exists
last_contact: 2025-11-20
outreach_status: null  # null | pitched | in-progress | published | declined

# Content appearances
featured_in:
  - title: "What's behind the annual spike in youth anxiety"
    url: "/podcast/peter-gray-youth-anxiety"
    date: 2025-11-20
    type: podcast
  - title: "We're spending billions to break something free"
    url: "/daily/2025-11-03"
    date: 2025-11-03
    type: daily

# Pipeline integration
assigned_topic: null  # from Pipeline.md if exists
pitch_draft: null     # path to draft if exists
notes: "Pioneer of self-directed education. Author of Free to Learn."
---
```

---

## Workflow

### Phase 1: Extraction (Haiku)
- Input: Master Content Index summaries + titles
- Process: Use Claude Haiku to extract named people from each entry
- Output: Raw list with `name`, `content_url`, `content_type`, `date`

**Why Haiku:** Fast, cheap, good at NER. We'll batch 50+ articles per call.

### Phase 2: Deduplication
- Normalize names (Dr. vs no title, full name vs partial)
- Merge mentions of same person across content
- Flag ambiguous cases for manual review

### Phase 3: Enrichment (Web Search)
- For each person, search for social handles:
  - X/Twitter (primary)
  - LinkedIn
  - Instagram (if relevant)
  - YouTube (if they produce content)
  - Newsletter (Substack, Beehiiv, etc.)
- Record follower counts where visible
- Calculate total_reach and engagement_score

**Search strategy:** Web search with queries like:
- `"Peter Gray" Twitter education`
- `"Peter Gray" LinkedIn profile`

### Phase 4: Merge with Pipeline.md
- Import existing contacts from `Guest Contributors/Pipeline.md`
- Match by name
- Preserve warmth_score, assigned_topic, pitch_draft, notes
- Update relationship_status based on Pipeline tier

### Phase 5: Storage
- One markdown file per person in `people/` folder
- Frontmatter with structured data
- Body for extended notes, conversation history

### Phase 6: Dashboard
**Options (in order of preference):**

1. **Obsidian Dataview** - Query files directly in Obsidian
   ```dataview
   TABLE x_twitter, total_reach, relationship_status
   FROM "Studio/Nearbound Pipeline/people"
   WHERE x_followers > 10000
   SORT total_reach DESC
   ```

2. **Local web dashboard** - Simple HTML + websocket for filtering
   - Export JSON from markdown files
   - Filterable table view
   - Share via localhost or deploy

3. **Notion import** - Later, if team needs it
   - CSV export → Notion database
   - Use Notion API to keep in sync

---

## Use Cases

### 1. Tagging when posting old content
```
I'm posting the Peter Gray podcast clip.
→ Look up Peter Gray → @petergray on X
→ Include tag in post
```

### 2. Finding high-reach people to tag
```
Show me everyone with >10k X followers who we've featured
→ Filter by x_followers, relationship_status = featured
→ Prioritize for resurfacing campaigns
```

### 3. Outreach for guest contributor articles
```
Who from our content would write about classical education?
→ Filter by type, check notes for expertise
→ Draft pitch using ghostwriter method
```

### 4. Content strategy - who to feature next
```
Who have we mentioned but never interviewed?
→ Filter: featured_in.type = daily, never podcast
→ Identify gaps for future episodes
```

---

## Success Criteria

### Phase 1 Complete ✅
- [x] All 66 podcast guests extracted with names
- [x] All 286 dailies scanned for named experts/thought leaders
- [x] All 48 blogs scanned for named people
- [x] Raw extraction saved to `_extraction/raw_people.json`

### Phase 2 Complete ✅
- [x] Deduplicated list of unique people
- [x] Each person has at least one content reference
- [x] 47 people from content extraction

### Phase 3 In Progress
- [ ] Top 50 by reach potential have social handles
- [ ] X/Twitter handles for 80%+ of active social users
- [ ] Total reach calculated for scored subset

### Phase 4 Complete ✅
- [x] Pipeline.md contacts merged (34 additional people)
- [x] Warmth scores preserved
- [x] Assigned topics and draft pitches linked

### Phase 5 Complete ✅
- [x] Markdown files created in `people/` folder (81 files)
- [x] Queryable via Obsidian Dataview
- [ ] Teammate can filter and search (needs Dataview queries)

---

## File Structure

```
Studio/Nearbound Pipeline/
├── PROJECT.md              ← You are here
├── people/                 ← One file per person
│   ├── peter-gray.md
│   ├── lenore-skenazy.md
│   └── ...
├── _extraction/            ← Working files
│   ├── raw_people.json     ← Haiku extraction output
│   ├── deduplicated.json   ← After cleanup
│   └── enrichment_queue.md ← People needing social lookup
└── scripts/                ← Automation
    └── extract_people.py   ← Haiku extraction script
```

---

## Integration Points

| System | Integration |
|--------|-------------|
| **Guest Contributors Pipeline** | Merge contacts, preserve warmth data |
| **Frictionless Content Engine** | Feed handles for auto-tagging suggestions |
| **SEO Content Production** | Identify guest contributor candidates |
| **Social Media posting** | Quick handle lookup when scheduling |
| **HubSpot CRM** | Future: sync high-value contacts |

---

## Tools & APIs

| Tool | Purpose |
|------|---------|
| Claude Haiku | Entity extraction from content |
| Web Search | Social handle lookup |
| Obsidian Dataview | Local querying |
| (Optional) Notion API | Sync if team needs Notion view |

---

## Open Questions

1. **Follower count freshness** - How often to refresh? Manual for now, automate later?
2. **Engagement scoring** - What signals indicate "active/engaged" on social?
3. **Notion timeline** - When does teammate need Notion view vs Obsidian?

---

## Next Actions

1. ~~Create `people/` and `_extraction/` folders~~ ✅
2. ~~Build extraction script with Haiku~~ ✅
3. ~~Run extraction on Master Content Index~~ ✅
4. ~~Merge Pipeline.md contacts~~ ✅
5. **Begin social enrichment for top 50** ← Current priority
6. Create Dataview queries for dashboard

---

*Created: 2026-01-20*
*Last Updated: 2026-01-20*
