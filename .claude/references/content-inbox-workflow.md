# Content Inbox Workflow

Unified workflow for content suggestions → development → scheduling via Slack #content-inbox.

---

## Channel

**#content-inbox** - `C0ABV2VQQKS`

All content suggestions flow through this single channel regardless of source.

---

## Standard Message Format

Every suggestion posted to #content-inbox should use this format:

```
*[Title]*
_[Source] | [Type]_

[1-2 sentence summary or snippet]

OpenEd angle: [Why this matters / why share now]
Suggested: [Platforms - LinkedIn, X, Instagram, etc.]

[URL if applicable]
```

**Examples by type:**

### External (RSS Curation)
```
*Helping Kids Who Resist: Low-Demand Homeschooling*
_Raising Lifelong Learners | External_

Low-demand homeschooling directly addresses families mixing approaches. Practical parent help for resistance/autonomy challenges.

OpenEd angle: Frame as strategy for parents struggling with resistant learners - validates flexible approaches
Suggested: LinkedIn, X

https://raisinglifelonglearners.com/article
```

### Archive
```
*The Socialization Question: What Research Actually Shows*
_Archive | Blog | Published 2025-08-15_

New research from Harvard shows homeschooled students demonstrate stronger social skills in mixed-age settings.

OpenEd angle: Evergreen FAQ - always relevant when families are deciding
Suggested: LinkedIn, X, Instagram

https://opened.co/blog/socialization-research
```

### Newsletter
```
*Dual enrollment: The overlooked school choice*
_Newsletter | OpenEd Daily 2026-01-28_

Dual enrollment lets teens earn college credit while still at home - and most families don't know it's an option.

OpenEd angle: Practical path that fits OpenEd's "build your own education" philosophy
Suggested: LinkedIn, X

[No URL - from today's newsletter]
```

### Podcast
```
*Ken Danford on why he quit teaching to prove schools are optional*
_Podcast | Episode 87_

"The factory model assumes all kids learn the same way at the same pace. That's not education - that's sorting."

OpenEd angle: Founder story that validates alternative paths
Suggested: LinkedIn, X (thread potential)

https://opened.co/podcast/ken-danford
```

---

## Reaction Workflow

Users react to trigger actions:

| Reaction | Action |
|----------|--------|
| ✍️ | **Develop** - Claude spawns framework fitting sub-agent |
| ❌ | **Skip** - Not pursuing this one |
| 👀 | **Claimed** - Someone is looking at it |
| ✅ | **Approve** - On developed posts, stage to Notion |

---

## Development Flow (✍️ Reaction)

When user reacts with ✍️ or says "develop the [title] post":

### 1. Spawn Sonnet Sub-Agent

```
Develop this content into social posts for OpenEd:

Title: [title]
Source: [source]
URL: [url]

Context: [summary/snippet from original message]

Steps:
1. If external URL, WebFetch the full article
2. Extract 2-3 standalone snippets:
   - Hot takes that stand alone
   - Stats with interpretation
   - Story moments / transformation
   - Quotable lines
3. Check nearbound/people/ for any mentioned names
4. Web search for social handles of people/orgs mentioned
5. Load TEMPLATE_INDEX.md and match snippets to 2-3 best templates per platform
6. Generate 2 LinkedIn options and 2 X options
7. Run lite 3-judge quality gate (AI-tells, Voice, Platform)

Voice rules:
- No emojis
- No correlative constructions ("X isn't just Y - it's Z")
- No AI-isms (delve, comprehensive, crucial, leverage, landscape)
- Conversational tone - like sharing with a friend
- Include @handles for tagging

Return: Snippets extracted, handles found, and draft posts ready for review.
```

### 2. Post Drafts as Thread Reply

```
**Developed: [Title]**

---

**LinkedIn Option A** (Contrarian template)
> [Post content]
>
> @michaelbhorn

**LinkedIn Option B** (Story template)
> [Post content]

---

**X Option A** (Commentary template)
> [Post content]

**X Option B** (Paradox hook)
> [Post content]

---

React ✅ on the option you want to stage to Notion.
```

### 3. User Edits in Thread

User can:
- Reply with edits
- Ask for variations
- Approve with ✅

---

## Staging Flow (✅ Reaction on Draft)

When user reacts ✅ to a developed draft:

### Option A: Manual Copy to Notion

User copies the approved draft and pastes into Notion Master Content Database with:
- **Caption**: The post text
- **Platform**: LinkedIn, X, etc.
- **Status**: Staging → Approved
- **Post Date**: When to publish

### Option B: Claude Creates Notion Page (Future)

Claude uses Notion MCP to:
1. Create new page in Master Content Database
2. Set Caption, Platform, Status = "Staging"
3. Link source Slack message TS for traceability

---

## Scheduling Flow

Once items are in Notion with Status = "Approved":

Invoke: "schedule approved content" or `/schedule-approved`

Claude will:
1. Query Notion for Approved items
2. Present list for confirmation
3. Call GetLate API to schedule each
4. Update Notion Status to "Scheduled"

See: `.claude/skills/schedule-approved/SKILL.md`

---

## Input Sources

| Source | Skill | Trigger |
|--------|-------|---------|
| External RSS | `rss-curation` | "run curation", "check feeds" |
| Archive content | `archive-suggest` | "suggest archive content", "find evergreen" |
| Newsletter/Blog | `webflow-publish` → `newsletter-to-social` | **Automatic** after Webflow publish (Step 6) |
| Podcast | `podcast-production` | After Checkpoint 2 (clips ready) |

**Note:** When you publish to Webflow, social suggestions are generated automatically as Step 6 of the webflow-publish workflow. No separate invocation needed.

---

## Full Pipeline

```
INPUTS (to #content-inbox)
├─ rss-curation (external)
├─ archive-suggest (evergreen)
├─ newsletter-to-social (from daily/weekly)
└─ podcast-production (clips)
        │
        ▼
TRIAGE (in Slack)
├─ ✍️ → Develop with framework fitting
├─ ❌ → Skip
└─ 💬 → Discuss in thread
        │
        ▼
DEVELOPMENT (thread replies)
├─ Sub-agent does deep template matching
├─ Returns 2-3 options per platform
└─ User edits/approves with ✅
        │
        ▼
STAGING (Notion)
├─ Approved draft → Notion page
├─ Set Platform, Caption, Post Date
└─ Status: Approved
        │
        ▼
SCHEDULING (GetLate)
├─ "schedule approved" invokes skill
├─ Queries Notion, calls GetLate API
└─ Updates Status: Scheduled
        │
        ▼
POSTED
```

---

## Key Files

| Purpose | Location |
|---------|----------|
| RSS curation | `.claude/skills/rss-curation/SKILL.md` |
| Archive suggest | `.claude/skills/archive-suggest/SKILL.md` |
| Newsletter to social | `.claude/skills/newsletter-to-social/SKILL.md` |
| Schedule approved | `.claude/skills/schedule-approved/SKILL.md` |
| Template library | `.claude/skills/text-content/references/templates/TEMPLATE_INDEX.md` |
| Nearbound people | `Studio/Nearbound Pipeline/people/` |
| Notion schema | `.claude/references/notion-content-schema.md` |

---

*Created: 2026-01-28*
