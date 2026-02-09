# OpenEd Vault - Master Context

**Content production system for OpenEd** - Alternative education company creating newsletters, podcasts, social media, SEO content, and educational resources.

**Operating States:** AR, IN, IA, KS, MN, MT, NV, OR, UT (9 states)\
**Program Details:** `.claude/references/opened-program-details.md`

---

## Start Here

| Need | Go To |
| --- | --- |
| Current state / priorities | NOW.md |
| Weekly tasks | EXECUTION.md |
| Content OS (pathways, skills, formats) | Projects/OpenEd-Content-OS/PROJECT.md |
| Project context | Studio/[project]/PROJECT.md |
| Published content | Master_Content_Index.md (406 articles by tag) |

---

## Where Things Live

| Need | Go To |
| --- | --- |
| Daily/Weekly newsletter | Studio/OpenEd Daily Studio/ + skill: opened-daily-newsletter-writer |
| SEO content | Studio/SEO Content Production/PROJECT.md |
| Podcast workflow | Studio/Podcast Studio/ + skill: podcast-production |
| Social posts | skill: text-content + Studio/Social Media/FORMAT_INVENTORY.md |
| Short-form video | skill: short-form-video + video-caption-creation |
| Meta ads | Studio/Meta Ads/PROJECT.md |
| Notion schema | .claude/references/notion-content-schema.md |

---

## Studio Projects

Each project has a `PROJECT.md` with full context. Navigate there first.

| Project | Location | Status |
| --- | --- | --- |
| Lead Magnet | Projects/Lead Magnet Project/ | Active (curriculove app) |
| Meta Ads | Studio/Meta Ads/PROJECT.md | 100 concepts ready |
| SEO Content | Studio/SEO Content Production/PROJECT.md | Active |
| Eddie Awards | Projects/Eddie Awards/PROJECT.md | Planning |
| Project Dandelion | Projects/Project-Dandelion/PROJECT.md | Active (paid acquisition) |
| ↳ Retargeting | Projects/Project-Dandelion/retargeting-strategy/ | Subfolder of Dandelion |

### Ongoing Workflows

| Workflow | Location | Cadence |
| --- | --- | --- |
| OpenEd Daily | Studio/OpenEd Daily Studio/ | Mon-Thu |
| Podcasts | Studio/Podcast Studio/ | Weekly |
| Open Education Hub | Studio/Open Education Hub/ | As needed |

---

## Writing Rules

**CRITICAL: Apply to ALL public-facing content.**

### Hard Rules (Never Break)

**No correlative constructions:**

- Never: "X isn't just Y - it's Z"

- Never: "It's not about X, it's about Y"

- This is the #1 AI tell - find another way

**Dash consistency:**

- Use: hyphens with spaces - like this

- Never: em dashes

**No emojis** in body content (rare exceptions for social captions).

### AI-isms to Avoid

**Words:** delve, comprehensive, crucial, vital, leverage, landscape, navigate, foster, facilitate, realm, paradigm, embark, journey, tapestry, myriad, multifaceted, seamless, cutting-edge

**Phrases:**

- "The best part? ..." / "The secret? ..."

- "What if I told you..." / "Here's the thing..." / "Let's be honest..."

- "In today's fast-paced..." / "In the ever-evolving..."

- "In conclusion" / "In summary"

- Staccato patterns: "No fluff. No filler. Just results."

### Deeper Voice Guidance

Load these skills for writing tasks:

- `ghostwriter` - Anti-AI patterns, authentic voice

- `opened-identity` - Sarah persona, brand voice

- `newsletter-subject-lines` - For email subject lines (10 Commandments + formulas)

- `article-titles` - For blog/SEO headlines (journalistic, formal)

---

## Framework Fitting (Core Technique)

**The central content repurposing methodology.**

```
SOURCE → EXTRACT SNIPPETS → MATCH TO TEMPLATES → GENERATE DRAFTS → QUALITY GATE
```

### Step 1: Extract Standalone Snippets

From any hub content, extract atomic insights:

- Hot takes (opinions that stand alone)

- Stats/data points (with interpretation)

- Story arcs (transformation moments)

- How-to tips (actionable advice)

- Quotes (memorable lines)

### Step 2: Match to Templates

Use `TEMPLATE_INDEX.md` (lightweight) to match snippet type to proven formats.

| Snippet Type | LinkedIn | X | Instagram |
| --- | --- | --- | --- |
| Hot take | Contrarian | Paradox Hook | Quote card |
| Stat | Authority | Commentary | Carousel |
| Story | Transformation | Thread | Reel/Carousel |
| How-to | List | Thread | Carousel |

### Step 3: Parallel Sub-Agents

For batch processing, spawn platform sub-agents in parallel:

- Each loads TEMPLATE_INDEX.md + brand voice

- Returns 2-3 draft options per platform

- Aggregates for human selection

**Sub-agent prompts:** `.claude/skills/content-repurposer/references/sub-agents/`

---

## Hub-and-Spoke Model

Create one **hub piece**, spin off derivative **spokes** using framework fitting.

| Hub | Skill | Primary Spokes | Output |
| --- | --- | --- | --- |
| Podcast | podcast-production | Clips (video), blog, LinkedIn | 12-25 posts |
| Newsletter (Daily) | opened-daily-newsletter-writer | LinkedIn, X, Instagram | 6-9 posts |
| Newsletter (Weekly) | opened-weekly-newsletter-writer | LinkedIn roundup | 2-3 posts |
| Deep Dive | open-education-hub-deep-dives | LinkedIn, X threads | 10-15 posts |

**Key routing skill:** `newsletter-to-social` - Transforms one newsletter into platform-optimized posts.

After completing a hub, **proactively offer spokes**.

---

## Quality Loop Triggers

**All public content goes through quality gates.**

| Content Type | Trigger Point | Mode |
| --- | --- | --- |
| Newsletter | After draft, before send | Full 5-judge |
| Deep Dive/Article | Before Webflow publish | Full 5-judge |
| Podcast blog | Before publish | Full 5-judge |
| LinkedIn post | After draft, before schedule | Lite 3-judge |
| X post | After draft, before schedule | Lite 3-judge |
| Instagram | After draft + visual | Lite 3-judge |

**Full 5-judge:** Human Detector, Accuracy, OpenEd Voice, Reader Advocate, SEO Advisor\
**Lite 3-judge:** AI-Tell, Voice, Platform (faster for social)

---

## Skills Quick Reference

| Content Type | Primary Skill |
| --- | --- |
| Text posts | text-content (360+ templates) |
| Multi-platform repurposing | content-repurposer (framework fitting specialist) |
| Newsletter → Social | newsletter-to-social (router) |
| Archive repurposing | archive-suggest (daily suggestions) |
| Slack distribution | slack-social-distribution (post to #market-daily) |
| Video production | short-form-video |
| Video hooks/captions | video-caption-creation |
| Podcast | podcast-production |
| Newsletter | opened-daily-newsletter-writer |
| Subject lines | newsletter-subject-lines |
| Article titles | article-titles |
| SEO content | seo-content-production |
| Deep dives | open-education-hub-deep-dives |
| Quality control | quality-loop |
| AI images | nano-banana-image-generator |
| Meta ads | meta-ads-creative + dude-with-sign-writer |
| Work summaries | work-summary (git → Slack updates) |

All skills: `.claude/skills/` (60 active)

---

## Nearbound Tagging

When creating social posts, check if any mentioned people are in the Nearbound index.

**Process:**

1. Note any names mentioned in content

2. Check `Studio/Nearbound Pipeline/people/` for profile

3. If found, add @handle to post

4. If not found, note for future profile creation

**Priority people:** Podcast guests, quoted experts, tool/curriculum founders.

---

## Proactive Behaviors

**The Content OS encourages automatic skill invocation at specific stages.**

### Auto-Invoke Triggers

| When | Automatically Invoke |
| --- | --- |
| Hub content complete (newsletter, podcast, article) | `content-repurposer` → offer social spokes |
| Article draft complete | `article-titles` → 10+ title options |
| Newsletter draft complete | `newsletter-subject-lines` → 10+ subject options |
| Any publishable content | `quality-loop` → appropriate judge panel |
| Names mentioned in content | Check nearbound → add @handles |
| Visual asset needed | `nano-banana-image-generator` |

### Continual Learning

- When a new format works well, document it in FORMAT_INVENTORY.md
- When a skill chain proves effective, add it to Content OS pathways
- When a transformation is requested multiple times, consider creating a dedicated pathway

---

## Key References

| Reference | Location |
| --- | --- |
| Template index | .claude/skills/text-content/references/templates/TEMPLATE_INDEX.md |
| Social format inventory | Studio/Social Media/FORMAT_INVENTORY.md |
| Video format evaluation | Archive/Andrew Muto/FORMAT_EVALUATION_Matrix.md |
| Master content index | .claude/references/Master_Content_Index.md |
| SEO commands | .claude/references/seo-commands.md |
| Program details | .claude/references/opened-program-details.md |
| Notion schema | .claude/references/notion-content-schema.md |

---

## Task Protocol

Before starting work, check `tasks/` for assigned tasks:

1. `glob tasks/*.md` to find all task files
2. Read any with `assignee: claude` and `status: todo`
3. Pick highest priority, update status to `in_progress`
4. Execute the steps/acceptance criteria in the task body
5. Update status to `done`, add completion notes to Context section

**Task files live in `tasks/`** - each is a `.md` file with YAML frontmatter (id, title, status, project, assignee, priority, effort, due, tags). The body contains Context, Steps (checkboxes), and Spec References.

**Dashboard:** `cd task-dashboard && bun run server.ts` → http://localhost:8002 (unified dashboard at root level, scans all project areas)

**Status values:** `todo` | `in_progress` | `done` | `later`

**Task hygiene (every session):**
- Update task status and check off steps as you work
- Capture loose ends and follow-ups as new task files
- At session end, update Context sections with where you left off (file paths, draft versions, blockers)
- Never leave useful knowledge only in conversation - put it in a task file

---

## Maintenance

### Structural Change Protocol (CRITICAL)
When you add, rename, or remove skills, projects, folders, or workflows, update these documents:
- **New skill** → Add to skill table in this file + `SKILL_ARCHITECTURE_MAP.md` + `vault-guide` SKILL.md
- **New project/folder** → Add to folder tree in this file + `vault-guide` SKILL.md
- **New task file** → Automatically handled by dashboard, but update batch task files if relevant
- **Changed workflow** → Update `CONTENT_OS_MAP.md` + `PROJECT.md` for affected project
- **New integration** → Update MCP table in `vault-guide` SKILL.md
- **Published content** → Add to `Master_Content_Index.md`

The vault-guide skill (`.claude/skills/vault-guide/SKILL.md`) is the onboarding document for new team members. It must stay current.

### Session End
- Update `NOW.md` at session end

- Use `/handoff` to capture session context

- Use `/work-summary` to generate Slack-friendly daily updates

- Update PROJECT.md when structural changes occur

- Sync from Webflow: `python3 agents/webflow_sync_agent.py`

### Key Folders

| Folder | Purpose |
| --- | --- |
| .claude/skills/ | 60 active skills |
| .claude/work-summaries/ | Daily work updates for Slack |
| Projects/OpenEd-Content-OS/ | Content OS - pathways, formats, architecture |
| Projects/Project-Dandelion/ | Paid acquisition hub |
| Studio/Nearbound Pipeline/people/ | Contact profiles with social handles |

---

*Last Updated: 2026-02-04*