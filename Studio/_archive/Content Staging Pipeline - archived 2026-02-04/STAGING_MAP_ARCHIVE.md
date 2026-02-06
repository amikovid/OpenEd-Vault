# OpenEd Content Staging Map

*Working document - mapping the flow from Studio → Notion → Publish*

---

## The Flow

```
STUDIO (Claude Code)                    NOTION                         PUBLISH
─────────────────────────────────────────────────────────────────────────────────

Create content
(newsletter, social, article)
        │
        ▼
   Send to Notion ──────────────►  STAGING status
                                        │
                                        ▼
                                   Review/Approve
                                        │
                        ┌───────────────┼───────────────┐
                        ▼               ▼               ▼
                    APPROVED        SCHEDULED        REJECTED
                        │               │
                        ▼               ▼
                   GetLate API     Webflow CMS
                   (8 platforms)   (website)
                        │               │
                        ▼               ▼
                      POSTED          POSTED
```

---

## Master Content Database

**ID:** `9a2f5189-6c53-4a9d-b961-3ccbcb702612`

### Status Options

| Status | Meaning |
| --- | --- |
| Idea | Raw concept, not developed |
| Staging | Ready for review - Claude sends here |
| Approved | User approved, ready to schedule |
| Scheduled | Queued with Post Date |
| Posted | Published |
| Rejected | Won't publish |

### Key Properties for Staging

| Property | Type | Use |
| --- | --- | --- |
| Name | title | Content headline |
| Status | status | Workflow state |
| Content Formats | relation | What type (Reel, Daily, Deep Dive, etc.) |
| Basic Summary | rich_text | The actual content/copy |
| Post Date | date | Target publish date |
| URL | url | Final published URL |
| Source URL | url | Original source (if curated) |
| Parent podcast | relation | Source episode (if podcast-derived) |

### Content Formats (Relation Options)

**High-frequency (daily/weekly):**

| Format | ID | Cadence |
| --- | --- | --- |
| OpenEd Daily | 2aaafe52-ef59-80bc-beea-ce72402611aa | 5x/week |
| Reel | 2a3afe52-ef59-80ce-aab4-cc804fe4818b | 1/day |
| Deep Dives | 2a3afe52-ef59-800b-8af2-e1347eda8f30 | 2/week |
| Memes | 2a3afe52-ef59-80ed-897a-e776a3d05cfe | 3/week |
| Text Heavy | 2a3afe52-ef59-80b0-b900-d397fc3c4ad6 | 2/week |
| Podcast clip | 2a3afe52-ef59-80db-9380-eda257e462de | 2/week |

**Lower frequency:**

| Format | ID | Cadence |
| --- | --- | --- |
| Weekly digest | c62c9b50-eb8a-4d30-977d-bea5fb57cada | 1/week |
| Carousel | 2aaafe52-ef59-80d1-888a-f872cd7e425d | 1/week |
| Screenshot | 2a3afe52-ef59-806c-8a82-dae10c8fbd8e | 2/week |

---

## Publishing Routes

### Route 1: Social Platforms (via GetLate)

**Platforms:** LinkedIn, X, Instagram, Facebook, YouTube, TikTok, Pinterest, Mastodon

**Flow:**

1. Content in **Approved** status

2. GetLate API polls for approved items

3. Publishes to platforms per Content Format

4. Status → **Posted**

### Route 2: Website (via Webflow)

**Content types:** Deep Dives, Hub articles, SEO content

**Flow:**

1. Content in **Staging** or **Approved**

2. Manual publish to Webflow CMS

3. Update `URL` property with Webflow URL

4. Status → **Posted**

---

## Podcast-Derived Content

**Source:** Podcast Master Calendar (`d60323d3-8162-4cd0-9e1c-1fea5aad3801`)

**Relation:** `Parent podcast` links content back to episode

**Derived content per episode:**

- Blog post (Deep Dive format)

- 2-3 short clips (Reel format)

- 5+ social posts (Text Heavy, Screenshot, etc.)

- Newsletter segment (OpenEd Daily)

---

## Open Questions

1. **Webflow publishing** - Is there an API integration, or always manual?

2. **Staging views** - What filtered views exist in Notion currently?

3. **GetLate configuration** - Which formats auto-publish vs manual?

4. **Type vs Content Formats** - Should Type property be deprecated?

---

## Next Steps

- \[ \] Connect Claude to Master Content Database (test API access)

- \[ \] Create "Staging Review" view in Notion

- \[ \] Document Webflow publishing workflow

- \[ \] Test creating content item via API

---

*Created: 2026-01-24*\
*Source: Content Engine Deck, notion-content-schema.md, \_content-engine-refactor*