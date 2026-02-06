# OpenEd Vault Guide

Guided orientation to the OpenEd content production system. Use this for:
- **New team members / applicants** - self-guided tour + pick a real task
- **Charlie** - re-orient, explore ideas, find where things live
- **Any session** - understand what exists before starting work

---

## What Is This Place?

The **OpenEd Vault** is the content production system for OpenEd, an alternative education company helping families find and fund homeschooling, microschools, and learning pods across 9 US states (AR, IN, IA, KS, MN, MT, NV, OR, UT).

This workspace replaces a 5-7 person content team with AI-augmented workflows. It produces newsletters, podcasts, SEO articles, tool reviews, social content, and ad creative.

---

## Architectural Documents

These are the source-of-truth docs that describe how everything fits together. Read in this order for deepening understanding:

### Layer 1: Entry Points
| Document | Path | What it tells you |
|----------|------|------------------|
| **CLAUDE.md** | `CLAUDE.md` | Master routing, writing rules, skill reference, quality gates |
| **README.md** | `README.md` | System philosophy, quick start, folder overview |
| **NOW.md** | `NOW.md` | Current priorities, blockers, session state |

### Layer 2: System Architecture
| Document | Path | What it tells you |
|----------|------|------------------|
| **CONTENT_OS_MAP.md** | `Projects/OpenEd-Content-OS/CONTENT_OS_MAP.md` | 7-layer system diagram (Foundation > Input > Production > Distribution > Output > Post-Publication) |
| **SKILL_ARCHITECTURE_MAP.md** | `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md` | 932-line deep reference: folder architecture, skill dependency matrix, hub-specific workflow chains |
| **PROJECT.md (Content OS)** | `Projects/OpenEd-Content-OS/PROJECT.md` | Operational blueprint: pathway types, auto-invoke triggers, quality gates |

### Layer 3: Capability Inventories
| Document | Path | What it tells you |
|----------|------|------------------|
| **FORMAT_INVENTORY.md** | `Studio/Social Media/FORMAT_INVENTORY.md` | 20+ video formats (tiered), 118+ text templates, daily production targets |
| **Master_Content_Index.md** | `.claude/references/Master_Content_Index.md` | All 406 published articles indexed by tag |
| **SEO-REFACTOR-INVENTORY.md** | `.claude/skills/SEO-REFACTOR-INVENTORY.md` | 25+ SEO capabilities catalog |

### Layer 4: Active Work
| Document | Path | What it tells you |
|----------|------|------------------|
| **tasks/** | `tasks/` | 53 task files with context, steps, file paths - source of truth for where things stand |
| **task-dashboard/** | `task-dashboard/` | Kanban board: `bun run server.ts` on port 8002 |

### Layer 5: Per-Project Context (33 PROJECT.md files)
Every project and studio subfolder has its own `PROJECT.md`. Key ones:
- `Studio/SEO Content Production/PROJECT.md` - SEO content coordination
- `Studio/Podcast Studio/` - Episode production (uses Notion Podcast Master Calendar)
- `Projects/Tools Directory/PROJECT.md` - Tool reviews + teacher quotes pipeline
- `Projects/Lead Magnet Project/PROJECT.md` - Curriculove quiz app
- `Projects/Eddie Awards/PROJECT.md` - Awards program
- `Projects/Project-Dandelion/PROJECT.md` - Paid acquisition (3 pillars)

---

## Where Things Live

```
OpenEd Vault/
├── CLAUDE.md                          ← START HERE
├── NOW.md                             ← Current state
├── tasks/                             ← 53 active task files
├── task-dashboard/                    ← Kanban board (port 8002)
│
├── Studio/                            ← WHERE CONTENT GETS MADE
│   ├── SEO Content Production/
│   │   ├── Open Education Hub/        ← Deep dives, thinkers series
│   │   ├── Versus/                    ← Comparison articles (5 ready)
│   │   ├── State Pages/               ← 9-state content
│   │   └── Guest Contributors/        ← Guest article pipeline
│   ├── Podcast Studio/                ← Episode folders per guest
│   ├── OpenEd Daily Studio/           ← Newsletter drafts
│   ├── Social Media/                  ← Format inventory, post drafts
│   ├── Meta Ads/                      ← 100+ ad concepts
│   ├── Nearbound Pipeline/people/     ← Contact profiles + social handles
│   └── Analytics & Attribution/       ← HubSpot, GA4
│
├── Projects/                          ← DISCRETE INITIATIVES
│   ├── OpenEd-Content-OS/             ← System architecture docs
│   ├── Lead Magnet Project/           ← Curriculove quiz app (curricu.love)
│   ├── Tools Directory/               ← Reviews + teacher quotes + templates
│   ├── Eddie Awards/                  ← Awards program
│   ├── Project-Dandelion/             ← Paid acquisition hub
│   └── RSS-Curation/                  ← Feed pipeline
│
├── Published Content/                 ← Archive of 406 shipped pieces
│
├── .claude/
│   ├── skills/                        ← 45+ active AI skills
│   ├── commands/                      ← Slash commands (like /vault-guide)
│   └── references/                    ← Master content index, program details
│
└── .env                               ← API keys (not in repo)
```

---

## Skills (45+ Active)

Invokable with `/skill-name`. Grouped by task:

| Category | Skills |
|----------|--------|
| **Writing** | `ghostwriter`, `de-ai-ify`, `quality-loop`, `opened-identity` |
| **Newsletter** | `opened-daily-newsletter-writer`, `opened-weekly-newsletter-writer`, `newsletter-subject-lines` |
| **Podcast** | `podcast-production`, `transcript-polisher`, `cold-open-creator`, `narrative-snippets` |
| **SEO** | `seo-content-production`, `seomachine`, `seo-research`, `open-education-hub-deep-dives` |
| **Social** | `text-content` (360+ templates), `content-repurposer`, `newsletter-to-social`, `short-form-video` |
| **Visual** | `nano-banana-image-generator`, `video-generator`, `video-caption-creation` |
| **Ads** | `meta-ads-creative`, `dude-with-sign-writer` |
| **Distribution** | `x-posting`, `x-article-converter`, `youtube-clip-extractor` |
| **Titles/Headlines** | `article-titles`, `newsletter-subject-lines`, `youtube-title-creator` |

Full dependency chains: `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md`

---

## External Integrations (MCP)

| Service | Capability | Status |
|---------|-----------|--------|
| **Slack** | Read/search/post messages | Working |
| **Notion** | Podcast calendar, content database | Working |
| **Webflow** | Publish blog + tools CMS | Working |
| **Google Drive** | Share docs for review/approval | Working |
| **Apify** | YouTube scraping | Working |

---

## For New Team Members / Applicants

### Your Mission
Pick a real task, do real work, push your changes. This is designed for you to succeed.

### Good First Tasks

**Writer path** - Draft a tool review:
- Pick a tool from `tasks/` tagged `tools-directory`
- Quotes compiled at `Projects/Tools Directory/teacher-takes-compilation.md`
- Template: `Projects/Tools Directory/TOOL_REVIEW_TEMPLATE.md`
- Voice: `Projects/Tools Directory/TEACHERS_TAKE_GUIDELINES.md`

**Editor path** - Polish a comparison article:
- Pick from `tasks/` tagged `comparison`
- Drafts at `Studio/SEO Content Production/Versus/`

**Strategist path** - Run SEO research:
- Pick from `tasks/` tagged `seo-research`
- Use `/seo-research` to run keyword analysis

### How to Work
1. Read the task file - Context tells you the state, Steps tells you what to do
2. Do the work with my help (I know this workspace)
3. Update the task file when done (status, checkboxes, notes)
4. Commit and push

### Writing Rules
- **No correlative constructions** ("It's not just X - it's Y" is the #1 AI tell)
- **No em dashes** - hyphens with spaces
- **No AI buzzwords** (delve, comprehensive, crucial, leverage, navigate, landscape)
- **Teacher quotes are real** - honor the authentic voice
- Full rules in `CLAUDE.md`

---

## For Charlie

### Quick lookups
| Question | Where to look |
|----------|--------------|
| Where did I leave off? | `tasks/` - filter `status: in_progress` |
| What's ready to ship? | `tasks/seo-batch-publish-reviews-comparisons.md` |
| What are my priorities? | `NOW.md` + sort `tasks/` by due date |
| What content exists? | `Master_Content_Index.md` (406 articles by tag) |
| What can the system do? | `CONTENT_OS_MAP.md` then `SKILL_ARCHITECTURE_MAP.md` |
| What formats work? | `FORMAT_INVENTORY.md` |
| Who are my contacts? | `Studio/Nearbound Pipeline/people/` |

### Exploring new ideas
1. Check `Master_Content_Index.md` - does it already exist?
2. Run `/seo-research` - is there search volume?
3. Check `SKILL_ARCHITECTURE_MAP.md` - which workflow applies?
4. Create a task file if it's worth doing
