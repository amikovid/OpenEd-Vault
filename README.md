# OpenEd Content Engine

An AI-first content production system for [OpenEd](https://myopened.com) - an alternative education company helping families find and fund homeschooling, microschools, and learning pods across 9 US states (AR, IN, IA, KS, MN, MT, NV, OR, UT).

This workspace replaces a 5-7 person content team with **60 specialized AI skills** that produce newsletters, podcasts, SEO articles, tool reviews, social content, and ad creative.

---

## Getting Started

**If you're a new team member or applicant**, run `/vault-guide` in Claude Code. It will walk you through the workspace interactively.

**For full system context**, start with `CLAUDE.md` - it's the master routing document.

**For current priorities**, check `NOW.md`.

---

## Folder Structure

```
OpenEd Vault/
├── CLAUDE.md                          ← Start here (master context)
├── NOW.md                             ← Current state & priorities
├── EXECUTION.md                       ← Weekly execution plan
├── tasks/                             ← Task files (source of truth)
├── task-dashboard/                    ← Kanban board (port 8002)
│
├── Studio/                            ← Where content gets made
│   ├── SEO Content Production/        ← Blog articles, deep dives, thinkers series
│   ├── Podcast Studio/                ← Episode production
│   ├── OpenEd Daily Studio/           ← Mon-Thu newsletter
│   ├── OpenEd Weekly/                 ← Friday roundup newsletter
│   ├── Social Media/                  ← Format inventory, post drafts
│   ├── Meta Ads/                      ← Ad concepts & creative
│   ├── Nearbound Pipeline/            ← Contact profiles + social handles
│   ├── Analytics & Attribution/       ← HubSpot, GA4
│   └── Nano/                          ← Image generation workspace
│
├── Projects/                          ← Discrete initiatives
│   ├── OpenEd-Content-OS/             ← System architecture docs
│   ├── Lead Magnet Project/           ← Curriculove quiz app
│   ├── Tools Directory/               ← Reviews + teacher quotes
│   ├── Eddie Awards/                  ← Awards program
│   ├── Project-Dandelion/             ← Paid acquisition
│   └── RSS-Curation/                  ← Feed pipeline
│
├── Published Content/                 ← Archive of shipped articles
├── CRM/                               ← Contact database
├── references/                        ← Research & reference docs
│
├── .claude/
│   ├── skills/                        ← 60 production skills
│   ├── commands/                      ← Slash commands
│   └── references/                    ← Program details, content index
│
└── agents/                            ← Automation scripts
```

---

## How Skills Work

Skills are markdown files that encode complete workflows - methodology, references, quality gates. Invoke with `/skill-name` or "use the [skill-name] skill."

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

Full skill dependency chains: `Projects/OpenEd-Content-OS/SKILL_ARCHITECTURE_MAP.md`

---

## Hub-and-Spoke Model

One hub piece generates multiple derivative spokes:

| Hub | Skill | Natural Spokes |
|-----|-------|----------------|
| Podcast | `podcast-production` | Blog, clips, LinkedIn, newsletter |
| Newsletter (Daily) | `opened-daily-newsletter-writer` | LinkedIn, X, Instagram |
| Newsletter (Weekly) | `opened-weekly-newsletter-writer` | LinkedIn roundup |
| Deep Dive | `open-education-hub-deep-dives` | LinkedIn, X threads |

---

## Setup

```bash
git clone [repo-url]
cd OpenEd-Vault
cp .env.example .env    # Add your API keys
claude                   # Opens Claude Code with full context
```

See `.env.example` for required credentials. Never commit `.env` files.

---

## External Integrations

| Service | Purpose |
|---------|---------|
| Slack | Read/search/post messages (MCP) |
| Notion | Podcast calendar, content database (MCP) |
| Webflow | Blog + tools CMS publishing (MCP) |
| Google Drive | Doc sharing & review (MCP) |
| Apify | YouTube scraping (MCP) |
| DataForSEO | Keyword research |
| Gemini | AI images, long context |

---

*Built with Claude Code. Last updated: 2026-02-09*
